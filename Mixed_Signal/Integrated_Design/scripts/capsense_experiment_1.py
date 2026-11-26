#!/usr/bin/env python3
"""Experiment 1: Murata pressure -> CP -> transistor-level CapSense output.

Reads ONE runnable Xschem-generated .spice netlist (not a .sch file).
Copies/patches the netlist for each pressure and runs ngspice in separate
working directories. NEVER edits the original project, PDK or source deck.

CSV-only output: measurements.csv and summary.csv per experiment, and
waveforms.csv for each ngspice run. Does not generate graphs or PNG files.

Output directory (default):
  /home/shreyas/Desktop/Sec_7/Integrated_Design/experiment 1/

Required baseline: a top-level .param CP=..., .param CN=..., and accessible
included model files. The usual SCL project also defines CFB_L and SIM_STOP.
ngspice must already be able to run this baseline circuit successfully.

The CSV CP_pF value is the pressure-model input capacitance, not a transistor-
level extracted/effective capacitance measurement.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

PROJECT = Path('/home/shreyas/Desktop/Sec_7/Integrated_Design')
EXP1_DIR = PROJECT / 'experiment 1'
BASELINE_CANDIDATES = (
    Path.home() / '.xschem/simulations/capsense_cfb_40pf.spice',
    PROJECT / 'simulation/capsense_cfb_40pf.spice',
)
# Each datum is an ngspice wrdata column after the single time column.
SIGNALS = ('phi1', 'phi2', 'phit', 'outp', 'outn', 'txp', 'txn', 'sump', 'sumn', 'vp')
MURATA_MODEL = 'SCB10H-B012FB rounded nominal model, 30–120 kPa'


def murata_cp_pf(pressure_kpa: float) -> float:
    """Nominal Murata pressure capacitance (pF), pressure in absolute kPa."""
    p = pressure_kpa
    return (0.9 + 2.24 / (1.0 - (2.24 / 509.0) * p)
            + 3.94016 / (1.0 - (2.24 / 755.865) * p))


def pressure_points(start: float, stop: float, step: float) -> list[float]:
    if step <= 0 or stop < start:
        raise ValueError('Require --step > 0 and --stop >= --start')
    count = int(math.floor((stop - start) / step + 1e-9))
    points = [round(start + i * step, 8) for i in range(count + 1)]
    if not points or points[-1] > stop + 1e-7:
        raise ValueError('Invalid pressure range')
    if any(not (0 <= p <= 120) for p in points):
        raise ValueError('Murata rounded nominal pressure model: use 0..120 kPa; recommended 30..120')
    return points


def find_netlist(specified: Path | None) -> Path:
    if specified is not None:
        netlist = specified.expanduser().resolve()
        if not netlist.is_file():
            raise FileNotFoundError(f'No baseline SPICE netlist: {netlist}')
        return netlist
    for candidate in BASELINE_CANDIDATES:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(
        'Cannot find capsense_cfb_40pf.spice automatically. Netlist the Xschem '
        'schematic and pass --netlist /full/path/to/capsense_cfb_40pf.spice'
    )


def _patch_param(deck: str, name: str, value: str, *, required: bool = True) -> str:
    """Patch one assignment inside a .param line, handling {expressions with spaces}."""
    assignment = re.compile(r'(?i)(?<!\w)(' + re.escape(name) +
                            r'\s*=\s*)(\{[^{}]*\}|[^\s]+)')
    count = 0
    lines = []
    for line in deck.splitlines(keepends=True):
        if re.match(r'^\s*\.param\b', line, re.I):
            line, n = assignment.subn(lambda m: m.group(1) + value, line)
            count += n
        lines.append(line)
    if count > 1:
        raise ValueError(f'Multiple .param {name}= definitions found ({count}). '
                         'Remove duplicates in a COPY of the baseline before sweeping.')
    if not count and required:
        raise ValueError(f'Could not find .param {name}=... in the netlist. '
                         'Regenerate the Xschem netlist and check the parameter block.')
    if not count:
        # Insert only an optional informational pressure parameter; CP is patched separately.
        lines.insert(1, f'.param {name}={value}\n')
    return ''.join(lines)


def _absolute_relative_includes(deck: str, base_dir: Path) -> str:
    """Make relative .include/.lib file paths independent of the case workdir."""
    lines = []
    pat = re.compile(r'^(\s*\.(?:include|inc|lib)\s+)("[^"]+"|\'[^\']+\'|\S+)(.*)$', re.I)
    for line in deck.splitlines(keepends=True):
        m = pat.match(line.rstrip('\r\n'))
        if m:
            token = m.group(2)
            bare = token.strip('"\'')
            if (not bare.startswith(('/', '$', '{')) and
                    not re.match(r'^[A-Za-z]+:', bare)):
                resolved = (base_dir / bare).resolve()
                if resolved.exists():
                    line = m.group(1) + f'"{resolved}"' + m.group(3) + '\n'
        lines.append(line)
    return ''.join(lines)


def build_deck(base_text: str, base_dir: Path, pressure_kpa: float,
               cf_target_pf: float | None = None, stop_us: float = 1700.0,
               timestep_ns: float = 80.0) -> str:
    if stop_us < 320 or timestep_ns <= 0:
        raise ValueError('Use a run longer than 320 us and a positive timestep')
    cp_pf = murata_cp_pf(pressure_kpa)
    deck = base_text
    # Use numeric CP calculated directly from the Murata equation to prevent
    # ngspice multiline .param parser issues. Still record PRESS_KPA.
    deck = _patch_param(deck, 'CP', f'{cp_pf:.13g}p')
    deck = _patch_param(deck, 'CN', '10p')
    deck = _patch_param(deck, 'PRESS_KPA', f'{pressure_kpa:.9g}', required=False)
    # Existing analog_support.spice may refer to {SIM_STOP} in its .tran line.
    deck = _patch_param(deck, 'SIM_STOP', f'{stop_us:.9g}u', required=False)
    if cf_target_pf is not None:
        if cf_target_pf <= 0:
            raise ValueError('Target CF must be positive')
        # Calibrated schematic geometry: 40pF nominal CFB at L=202.7um,
        # five W=20um PMOS fingers per branch. Only a nominal scaling.
        new_l_um = 202.7 * cf_target_pf / 40.0
        deck = _patch_param(deck, 'CFB_L', f'{new_l_um:.9g}u')
    deck = _absolute_relative_includes(deck, base_dir)

    # Avoid running an old Xschem .control section that could plot, overwrite
    # outputs, or measure incompatible times in batch mode.
    deck = re.sub(r'(?ims)^\s*\.control\b.*?^\s*\.endc\s*\n?', '', deck)
    # Remove final .end: append our fresh dedicated measurement control instead.
    deck = re.sub(r'(?im)^\s*\.end\s*$', '', deck).rstrip() + '\n'

    saved = ' '.join(f'v({sig})' for sig in SIGNALS)
    deck += f'''\n* Generated experiment; original Xschem netlist is unchanged.
.control
set noaskquit
set wr_singlescale
set wr_vecnames
save {saved}
tran {timestep_ns:.9g}n {stop_us:.9g}u 0 {timestep_ns:.9g}n
wrdata waveforms.dat {saved}
.endc
.end
'''
    return deck


def _read_waveform(path: Path) -> list[list[float]]:
    if not path.is_file() or path.stat().st_size < 100:
        raise ValueError('No waveforms.dat from ngspice (netlist, runtime or convergence error)')
    rows: list[list[float]] = []
    with path.open(encoding='utf-8', errors='replace') as f:
        for line in f:
            if not line.strip():
                continue
            pieces = line.split()
            if not pieces[0][0].isdigit() and pieces[0][0] not in '+-.':
                continue  # wrdata header: 'time v(phi1) ...'
            try:
                nums = [float(v) for v in pieces]
            except ValueError:
                continue
            if len(nums) != len(SIGNALS) + 1:
                raise ValueError(f'Expected {len(SIGNALS)+1} wrdata columns, got {len(nums)}. '
                                 'Check set wr_singlescale and ngspice.log')
            if any(not math.isfinite(x) for x in nums):
                raise ValueError('NaN/Inf waveform value')
            rows.append(nums)
    if len(rows) < 100 or any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise ValueError(f'Invalid/non-increasing waveform data ({len(rows)} rows)')
    return rows


def _interpolate(rows: list[list[float]], t: float, col: int) -> float:
    if t < rows[0][0] or t > rows[-1][0]:
        raise ValueError('Sample time outside waveform interval')
    lo, hi = 0, len(rows) - 1
    while hi - lo > 1:
        mid = (hi + lo) // 2
        if rows[mid][0] <= t:
            lo = mid
        else:
            hi = mid
    a, b = rows[lo], rows[hi]
    weight = (t - a[0]) / (b[0] - a[0])
    return a[col] + weight * (b[col] - a[col])


def measure_waveforms(case_dir: Path, stop_us: float, sample_margin_us: float) -> dict:
    rows = _read_waveform(case_dir / 'waveforms.dat')
    if rows[-1][0] < 0.98 * stop_us * 1e-6:
        raise ValueError(f'Simulation stopped early at {rows[-1][0]*1e6:.1f}us')
    # Column 0=time; 1=phi1, 2=phi2, 3=phit, 4=outp, 5=outn, 6/7=TX.
    for name, col in (('phi1', 1), ('phit', 3), ('phi2', 2)):
        vals = [r[col] for r in rows]
        if min(vals) > 1 or max(vals) < 4:
            raise ValueError(f'No valid 0-to-5V {name} switching; inspect clock/Verilog runtime')
    fall_times = []
    for before, after in zip(rows, rows[1:]):
        if before[2] > 2.5 and after[2] <= 2.5:
            fall_times.append((before[0] + after[0]) / 2)
    if len(fall_times) < 3:
        raise ValueError('Need at least 3 phi2 falling edges for last-cycle measurements')
    last_fall, prior_fall = fall_times[-1], fall_times[-2]
    period_s = last_fall - prior_fall
    if abs(period_s - 100e-6) > 3e-6:
        raise ValueError(f'Invalid phase period: {period_s*1e6:.3f}us (expected 100us)')
    sample_t = last_fall - sample_margin_us * 1e-6
    prev_t = prior_fall - sample_margin_us * 1e-6
    if sample_t <= prior_fall or prev_t <= 0:
        raise ValueError('Sampling margin too large / not within previous phi2 high interval')
    vp = _interpolate(rows, sample_t, 4)
    vn = _interpolate(rows, sample_t, 5)
    vp_prev = _interpolate(rows, prev_t, 4)
    vn_prev = _interpolate(rows, prev_t, 5)
    inp = _interpolate(rows, sample_t, 8)
    inn = _interpolate(rows, sample_t, 9)
    ve = _interpolate(rows, sample_t, 10)
    # Only report maximum TX within last complete period, plus all startup as extra diagnostic.
    last_cycle = [r for r in rows if last_fall - period_s <= r[0] <= last_fall]
    if not last_cycle:
        raise ValueError('No last-cycle TX data')
    return {
        'sample_time_us': round(sample_t * 1e6, 6),
        'clock_period_us': round(period_s * 1e6, 6),
        'VEXC_V': ve, 'VOUTP_V': vp, 'VOUTN_V': vn,
        'VDIFF_mV': (vp - vn) * 1000,
        'VCM_OUT_V': (vp + vn) / 2,
        'VCM_IN_V': (inp + inn) / 2,
        'cycle_drift_mV': abs((vp-vn) - (vp_prev-vn_prev)) * 1000,
        'TXP_MAX_LAST_V': max(r[6] for r in last_cycle),
        'TXN_MAX_LAST_V': max(r[7] for r in last_cycle),
        'TXP_MAX_ALL_V': max(r[6] for r in rows),
        'TXN_MAX_ALL_V': max(r[7] for r in rows),
    }


def write_csv(path: Path, rows: list[dict], columns: list[str] | None = None) -> None:
    if not rows and not columns:
        return
    keys = columns or list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _linear_fit(x: list[float], y: list[float]) -> tuple[float, float, float, float]:
    xmean, ymean = sum(x)/len(x), sum(y)/len(y)
    ssx = sum((a-xmean)**2 for a in x)
    if ssx == 0:
        raise ValueError('Cannot fit identical x values')
    m = sum((a-xmean)*(b-ymean) for a, b in zip(x,y)) / ssx
    b0 = ymean - m*xmean
    residuals = [b - (m*a+b0) for a,b in zip(x,y)]
    span = max(y)-min(y)
    sst = sum((v-ymean)**2 for v in y)
    r2 = 1 - sum(err*err for err in residuals)/sst if sst else float('nan')
    nonlinearity_pct = 100*max(abs(e) for e in residuals)/span if span else float('nan')
    return m, b0, r2, nonlinearity_pct


def summarize_curve(rows: list[dict], expected_points: int, cf_target_pf: float) -> dict:
    ok = sorted((r for r in rows if r['status']=='OK'), key=lambda r: r['pressure_kPa'])
    summary = {'CF_target_pF': cf_target_pf, 'successful_points': len(ok),
               'requested_points': expected_points, 'complete': int(len(ok) == expected_points)}
    if len(ok) < 3:
        summary['error'] = 'Too few successful points for sensitivity analysis'
        return summary
    pressures = [float(r['pressure_kPa']) for r in ok]
    cp = [float(r['CP_pF']) for r in ok]
    vd = [float(r['VDIFF_mV']) for r in ok]
    slope_p, intercept, r2, nonlin = _linear_fit(pressures, vd)
    slope_c, _, _, _ = _linear_fit(cp, vd)
    slopes = []
    for i in range(len(ok)):
        lo, hi = max(0,i-1), min(len(ok)-1,i+1)
        slopes.append((vd[hi]-vd[lo])/(pressures[hi]-pressures[lo]))
        ok[i]['local_sensitivity_mV_per_kPa'] = slopes[-1]
    summary.update({
        'avg_pressure_sensitivity_mV_per_kPa': slope_p,
        'avg_cap_sensitivity_mV_per_pF': slope_c,
        'min_local_abs_pressure_sensitivity_mV_per_kPa': min(map(abs, slopes)),
        'max_local_abs_pressure_sensitivity_mV_per_kPa': max(map(abs, slopes)),
        'R_squared': r2, 'nonlinearity_pct_FS': nonlin,
        'vdiff_span_mV': max(vd)-min(vd),
        'max_cycle_drift_mV': max(float(r['cycle_drift_mV']) for r in ok),
        'max_TX_voltage_V': max(float(r['TXP_MAX_ALL_V']) for r in ok),
        'max_VCM_OUT_error_mV': max(abs(float(r['VCM_OUT_V'])-2.5)*1000 for r in ok),
        'output_monotonic': int(all((b-a)>=-1e-4 for a,b in zip(vd,vd[1:])) or
                                all((b-a)<=1e-4 for a,b in zip(vd,vd[1:]))),
        'error': '' if len(ok) == expected_points else 'Incomplete sweep: do not rank as valid',
    })
    return summary


def export_waveforms_csv(source_dat: Path, target_csv: Path) -> None:
    """Convert ngspice wrdata's whitespace table to genuine comma-delimited CSV.

    ngspice `wrdata` itself does NOT write comma-separated text; it writes
    whitespace-delimited numbers. This conversion preserves all time samples.
    """
    if not source_dat.is_file() or source_dat.stat().st_size == 0:
        raise ValueError(f'ngspice waveform export missing: {source_dat}')
    with target_csv.open('w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(['time_s', *[f'{name}_V' for name in SIGNALS]])
        with source_dat.open(encoding='utf-8', errors='replace') as src:
            for line in src:
                fields = line.split()
                if len(fields) != 1 + len(SIGNALS):
                    continue  # ngspice column headings, if enabled
                try:
                    numeric = [float(value) for value in fields]
                except ValueError:
                    continue
                if not all(math.isfinite(value) for value in numeric):
                    raise ValueError('Non-finite waveform value in ngspice export')
                writer.writerow(fields)


def run_cases(netlist: Path, target_dir: Path, pressures: list[float],
              cf_values: list[float | None], stop_us: float, timestep_ns: float,
              sample_margin_us: float, dry_run: bool, timeout_seconds: int) -> tuple[list[dict],list[dict]]:
    if shutil.which('ngspice') is None and not dry_run:
        raise RuntimeError('ngspice is not on PATH. Launch in the usual working simulation shell.')
    source = netlist.read_text(encoding='utf-8', errors='replace')
    target_dir.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict] = []
    summaries: list[dict] = []
    for cf in cf_values:
        grouped_rows: list[dict] = []
        for pressure in pressures:
            cp_pf = murata_cp_pf(pressure)
            cf_label = 'baseline' if cf is None else f'{cf:g}pF'
            case_dir = target_dir / 'runs' / f'CF_{cf_label}' / f'P_{pressure:g}kPa'
            case_dir.mkdir(parents=True, exist_ok=True)
            row = {
                'pressure_kPa': pressure, 'CP_pF': round(cp_pf, 10),
                'CN_pF': 10.0, 'deltaC_pF': round(cp_pf-10.0, 10),
                'CF_target_pF': 40.0 if cf is None else cf,
                'CFB_L_um': 202.7 if cf is None else 202.7*cf/40.0,
                'status': 'PENDING', 'error': '', 'case_dir': str(case_dir),
            }
            try:
                deck = build_deck(source, netlist.parent, pressure, cf,
                                  stop_us=stop_us, timestep_ns=timestep_ns)
                (case_dir/'case.spice').write_text(deck, encoding='utf-8')
                if dry_run:
                    row['status'] = 'DRY_RUN'
                else:
                    (case_dir/'waveforms.dat').unlink(missing_ok=True)
                    proc = subprocess.run(['ngspice', '-b', 'case.spice'], cwd=case_dir,
                                          capture_output=True, text=True, timeout=timeout_seconds)
                    (case_dir/'ngspice.log').write_text(proc.stdout + '\n' + proc.stderr,
                                                        encoding='utf-8')
                    if proc.returncode:
                        raise RuntimeError(f'ngspice exit {proc.returncode}; inspect ngspice.log')
                    row.update(measure_waveforms(case_dir, stop_us, sample_margin_us))
                    export_waveforms_csv(case_dir / 'waveforms.dat',
                                         case_dir / 'waveforms.csv')
                    row['TX_over_5V_warning'] = int(max(row['TXP_MAX_ALL_V'],
                                                        row['TXN_MAX_ALL_V']) > 5.0)
                    row['status'] = 'OK'
            except Exception as exc:
                row['status'] = 'FAILED'
                row['error'] = f'{type(exc).__name__}: {exc}'
            grouped_rows.append(row)
            all_rows.append(row)
            print(f'P={pressure:6g}kPa CF={cf_label:>8} CP={cp_pf:7.4f}pF '
                  f'-> {row["status"]}' + (f' ({row["error"]})' if row['error'] else ''), flush=True)
            write_csv(target_dir / 'measurements.csv', all_rows)
        summary = summarize_curve(grouped_rows, len(pressures), 40.0 if cf is None else cf)
        summaries.append(summary)
        write_csv(target_dir / 'summary.csv', summaries)
    if not dry_run:
        # The summary calculates local slopes; write those columns back to CSV.
        write_csv(target_dir / 'measurements.csv', all_rows)
    return all_rows, summaries


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, help='Path to your working Xschem-generated .spice file')
    parser.add_argument('--out', type=Path, default=EXP1_DIR)
    parser.add_argument('--start', type=float, default=30, help='Start pressure (kPa)')
    parser.add_argument('--stop', type=float, default=120, help='Stop pressure (kPa)')
    parser.add_argument('--step', type=float, default=5, help='Pressure increment (kPa)')
    parser.add_argument('--stop-us', type=float, default=1700, help='Transient run length in microseconds')
    parser.add_argument('--timestep-ns', type=float, default=80, help='Transient step and maximum step (ns)')
    parser.add_argument('--sample-margin-us', type=float, default=2, help='Sample 2us before last PHI2 falling edge')
    parser.add_argument('--timeout', type=int, default=900, help='Per-run timeout (seconds)')
    parser.add_argument('--dry-run', action='store_true', help='Generate decks without running ngspice')
    args = parser.parse_args(argv)
    try:
        points = pressure_points(args.start, args.stop, args.step)
        netlist = find_netlist(args.netlist)
        rows, summary = run_cases(netlist, args.out.expanduser(), points, [None],
                                  args.stop_us, args.timestep_ns,
                                  args.sample_margin_us, args.dry_run, args.timeout)
        print(f'\nResults: {args.out.expanduser().resolve()}')
        print('CSV-only: measurements.csv and summary.csv; each run also saves waveforms.csv')
        print('CP_pF is calculated from Murata model, not extracted from the circuit.')
        return 0 if any(r['status']=='OK' for r in rows) or args.dry_run else 2
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    sys.exit(cli())

