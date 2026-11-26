#!/usr/bin/env python3
"""CapSense Experiment 3: pressure x reference capacitance x feedback bank.

Run ngspice for every combination; CSV only, NO plots or images.

- CP: Murata SCB10H-B012FB pressure model (calculated in pF).
- CN: independently varied reference capacitor (default 8,9,10,11,12 pF).
- CF: nominal PMOS feedback bank targets (default 30,40,50,60 pF), obtained
      by scaling schematic parameter CFB_L relative to 40 pF @ 202.7 um.
      These are design targets, NOT extracted capacitances.
- One completely independent ngspice work directory per configuration.
- Live terminal START / RUNNING heartbeat / OK / FAILED with elapsed time.
- Saves aggregate measurements.csv, summary.csv, case.spice, ngspice.log,
  and per-run waveform CSVs. Original Xschem/PDK/RTL files are untouched.

Default output:
  /home/shreyas/Desktop/Sec_7/Integrated_Design/experiment 3/

Prerequisite: a working Xschem-generated SPICE netlist of your *integrated*
CapSense testbench, which already runs successfully with ngspice.

Examples:
  python3 capsense_experiment_3.py --netlist ~/.xschem/simulations/capsense_cfb_40pf.spice --dry-run --start 100 --stop 100 --cn 10 --cf 40
  python3 capsense_experiment_3.py --netlist ~/.xschem/simulations/capsense_cfb_40pf.spice --start 100 --stop 100 --cn 10 --cf 40
  python3 capsense_experiment_3.py --netlist ~/.xschem/simulations/capsense_cfb_40pf.spice
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

PROJECT = Path('/home/shreyas/Desktop/Sec_7/Integrated_Design')
DEFAULT_OUT = PROJECT / 'experiment 3'
DEFAULT_NETLIST = Path.home() / '.xschem/simulations/capsense_cfb_40pf.spice'
SIGNALS = ('phi1', 'phi2', 'phit', 'outp', 'outn', 'txp', 'txn', 'sump', 'sumn', 'vp')
BASELINE_CF_PF = 40.0
BASELINE_CFB_L_UM = 202.7

# Stable columns, including all Experiment 1/2 measurement columns.
MEASURE_COLUMNS = [
    'pressure_kPa', 'CP_pF', 'CN_pF', 'deltaC_pF', 'CF_target_pF',
    'CFB_L_um', 'status', 'error', 'case_dir',
    'sample_time_us', 'clock_period_us', 'VEXC_V', 'VOUTP_V', 'VOUTN_V',
    'VDIFF_mV', 'VCM_OUT_V', 'VCM_IN_V', 'cycle_drift_mV',
    'TXP_MAX_LAST_V', 'TXN_MAX_LAST_V', 'TXP_MAX_ALL_V', 'TXN_MAX_ALL_V',
    'TX_over_5V_warning', 'local_sensitivity_mV_per_kPa',
    'local_sensitivity_mV_per_pF', 'elapsed_s',
]


def murata_cp_pf(pressure_kpa: float) -> float:
    """Rounded nominal Murata SCB10H-B012FB C(P) in pF; P is absolute kPa."""
    p = pressure_kpa
    return 0.9 + 2.24 / (1 - (2.24 / 509.0) * p) + 3.94016 / (1 - (2.24 / 755.865) * p)


def pressure_points(start: float, stop: float, step: float) -> list[float]:
    if not math.isfinite(start + stop + step) or step <= 0 or stop < start:
        raise ValueError('Pressure sweep requires finite start/stop and a positive step')
    if start < 30 or stop > 120:
        raise ValueError('Use the Murata specified 30..120 kPa range')
    n = math.floor((stop - start) / step + 1e-9)
    return [round(start + step * i, 8) for i in range(n + 1)]


def find_netlist(user: Path | None) -> Path:
    p = (user or DEFAULT_NETLIST).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f'Netlist not found: {p}. Generate it in Xschem, then pass --netlist /path/to/file.spice')
    return p


def replace_param(deck: str, name: str, value: str, *, required: bool) -> tuple[str, int]:
    """Remove all top-level assignments to a param, then create ONE assignment.

    Supports multi-assignment .param lines including simple {...} expressions.
    Does not touch subcircuit/model/include text. Only generated case deck edited.
    """
    pat = re.compile(r'(?i)(?<![A-Za-z0-9_])' + re.escape(name) +
                     r'\s*=\s*(?:\{[^{}]*\}|\S+)')
    output, count = [], 0
    for line in deck.splitlines(keepends=True):
        if re.match(r'^\s*\.param\b', line, flags=re.I):
            body = line.rstrip('\r\n')
            new_body, hits = pat.subn('', body)
            count += hits
            if hits:
                # Preserve any other variables on the same .param line.
                remaining = re.sub(r'^\s*\.param\b', '', new_body, count=1, flags=re.I).strip()
                if remaining:
                    output.append('.param ' + remaining + '\n')
                continue
        output.append(line)
    if not count and required:
        raise ValueError(f'No top-level .param {name}=... found in baseline netlist; check your schematic parameters')
    # SPICE's first line is a title: insert param after it.
    output.insert(min(1, len(output)), f'.param {name}={value}\n')
    return ''.join(output), count


def absolute_relative_includes(deck: str, base_dir: Path) -> str:
    pat = re.compile(r'^(\s*\.(?:include|inc|lib)\s+)("[^"]+"|\'[^\']+\'|\S+)(.*)$', re.I)
    output = []
    for line in deck.splitlines(keepends=True):
        m = pat.match(line.rstrip('\r\n'))
        if m:
            token = m.group(2).strip('"\'')
            if not token.startswith(('/', '$', '{')):
                path = (base_dir / token).resolve()
                if path.exists():
                    line = m.group(1) + f'"{path}"' + m.group(3) + '\n'
        output.append(line)
    return ''.join(output)


def build_deck(base_text: str, base_dir: Path, pressure: float, cn_pf: float,
               cf_pf: float, stop_us: float, timestep_ns: float) -> tuple[str, list[str]]:
    if stop_us < 320 or timestep_ns <= 0:
        raise ValueError('Use stop-us >= 320 and positive timestep-ns')
    cf_length_um = BASELINE_CFB_L_UM * cf_pf / BASELINE_CF_PF
    updates = (
        ('CP', f'{murata_cp_pf(pressure):.13g}p', True),
        ('CN', f'{cn_pf:.13g}p', True),
        ('PRESS_KPA', f'{pressure:.12g}', False),
        ('CFB_L', f'{cf_length_um:.12g}u', True),
        ('SIM_STOP', f'{stop_us:.12g}u', False),
    )
    deck = base_text
    warnings = []
    for name, value, required in updates:
        deck, count = replace_param(deck, name, value, required=required)
        if count > 1:
            warnings.append(f'Consolidated {count} .param {name}= definitions in case copy')
    deck = absolute_relative_includes(deck, base_dir)

    # Remove any pre-existing testbench .control blocks: plots or measurements
    # inside them might fail, and some run extra transient analyses.
    deck = re.sub(r'(?ims)^\s*\.control\b.*?^\s*\.endc\s*\n?', '', deck)
    # Only remove actual .end lines (NOT .ends for subcircuits).
    deck = re.sub(r'(?im)^\s*\.end\s*$', '', deck).rstrip() + '\n'

    saved = ' '.join('v(' + sig + ')' for sig in SIGNALS)
    deck += f'''\n* Experiment 3 ngspice-generated deck (baseline unchanged)
.control
set noaskquit
set wr_singlescale
set wr_vecnames
save {saved}
tran {timestep_ns:.12g}n {stop_us:.12g}u 0 {timestep_ns:.12g}n
wrdata waveforms.dat {saved}
.endc
.end
'''
    return deck, warnings


def read_waveforms(path: Path) -> list[list[float]]:
    if not path.is_file() or path.stat().st_size < 100:
        raise ValueError('ngspice did not generate waveforms.dat; check ngspice.log')
    rows = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        fields = line.split()
        if len(fields) != len(SIGNALS) + 1:
            continue
        try:
            vals = [float(x) for x in fields]
        except ValueError:
            continue
        if not all(math.isfinite(v) for v in vals):
            raise ValueError('NaN/Inf encountered in waveforms.dat')
        rows.append(vals)
    if len(rows) < 100 or any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise ValueError(f'Waveform export invalid or time not increasing ({len(rows)} rows)')
    return rows


def interpolate(rows: list[list[float]], t: float, col: int) -> float:
    if not (rows[0][0] <= t <= rows[-1][0]):
        raise ValueError('Requested sample time is outside waveform interval')
    lo, hi = 0, len(rows)-1
    while hi-lo > 1:
        mid = (lo+hi)//2
        if rows[mid][0] <= t:
            lo = mid
        else:
            hi = mid
    if rows[hi][0] == rows[lo][0]:
        return rows[lo][col]
    w = (t-rows[lo][0])/(rows[hi][0]-rows[lo][0])
    return rows[lo][col] + w*(rows[hi][col]-rows[lo][col])


def measure_waveforms(path: Path, stop_us: float, margin_us: float) -> dict:
    rows = read_waveforms(path)
    if rows[-1][0] < 0.98 * stop_us * 1e-6:
        raise ValueError(f'Transient stopped early at {rows[-1][0]*1e6:.2f} us')
    # time,phi1,phi2,phit,outp,outn,txp,txn,sump,sumn,vp
    for name, col in [('phi1',1),('phi2',2),('phit',3)]:
        vals = [row[col] for row in rows]
        if min(vals) > 1 or max(vals) < 4:
            raise ValueError(f'No valid 0-5 V switching on {name}; inspect ngspice.log and clock runtime')
    falls = [(a[0]+b[0])/2 for a,b in zip(rows, rows[1:]) if a[2] > 2.5 >= b[2]]
    if len(falls) < 3:
        raise ValueError('Fewer than 3 phi2 falling edges detected')
    last, previous = falls[-1], falls[-2]
    period = last-previous
    if not (97e-6 <= period <= 103e-6):
        raise ValueError(f'Incorrect phase period {period*1e6:.4f}us; expected 100us')
    current_t, old_t = last-margin_us*1e-6, previous-margin_us*1e-6
    if current_t <= previous or old_t <= 0:
        raise ValueError('Sample margin out of range')
    vp = interpolate(rows, current_t, 4)
    vn = interpolate(rows, current_t, 5)
    oldp = interpolate(rows, old_t, 4)
    oldn = interpolate(rows, old_t, 5)
    in_p = interpolate(rows, current_t, 8)
    in_n = interpolate(rows, current_t, 9)
    exc = interpolate(rows, current_t, 10)
    last_cycle = [r for r in rows if last-period <= r[0] <= last]
    return dict(
        sample_time_us=round(current_t*1e6, 6),
        clock_period_us=round(period*1e6, 6),
        VEXC_V=exc,
        VOUTP_V=vp,
        VOUTN_V=vn,
        VDIFF_mV=(vp-vn)*1000,
        VCM_OUT_V=(vp+vn)/2,
        VCM_IN_V=(in_p+in_n)/2,
        cycle_drift_mV=abs((vp-vn)-(oldp-oldn))*1000,
        TXP_MAX_LAST_V=max(r[6] for r in last_cycle),
        TXN_MAX_LAST_V=max(r[7] for r in last_cycle),
        TXP_MAX_ALL_V=max(r[6] for r in rows),
        TXN_MAX_ALL_V=max(r[7] for r in rows),
    )


def export_waveforms_csv(src_path: Path, target_path: Path) -> None:
    """Convert ngspice's whitespace `wrdata` output into actual CSV."""
    with src_path.open(encoding='utf-8', errors='replace') as src, \
         target_path.open('w', newline='', encoding='utf-8') as target:
        wr = csv.writer(target)
        wr.writerow(['time_s', *[f'{s}_V' for s in SIGNALS]])
        count = 0
        for line in src:
            fields = line.split()
            if len(fields) != len(SIGNALS)+1:
                continue
            try:
                if not all(math.isfinite(float(f)) for f in fields):
                    continue
            except ValueError:
                continue
            wr.writerow(fields)
            count += 1
        if count < 100:
            raise ValueError('Too few exported waveform rows')


def atomic_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def atomic_json(path: Path, data: dict) -> None:
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, allow_nan=False), encoding='utf-8')
    os.replace(tmp, path)


def linear_fit(x: list[float], y: list[float]) -> tuple[float,float,float,float]:
    xm, ym = sum(x)/len(x), sum(y)/len(y)
    ssx = sum((a-xm)**2 for a in x)
    if ssx == 0:
        raise ValueError('Need at least two distinct x values')
    slope = sum((a-xm)*(b-ym) for a,b in zip(x,y))/ssx
    intercept = ym-slope*xm
    errors = [b-(slope*a+intercept) for a,b in zip(x,y)]
    ssy = sum((b-ym)**2 for b in y)
    r2 = 1-sum(e*e for e in errors)/ssy if ssy else float('nan')
    span = max(y)-min(y)
    nlin = 100*max(map(abs,errors))/span if span else float('nan')
    return slope, intercept, r2, nlin


def summarize_group(group: list[dict], expected: int, cn: float, cf: float) -> dict:
    good = sorted([r for r in group if r['status']=='OK'], key=lambda r: r['pressure_kPa'])
    s = dict(CN_pF=cn, CF_target_pF=cf, successful_points=len(good),
             requested_points=expected, complete=int(len(good)==expected))
    if len(good)<3:
        s['error']='Too few successful points for a curve'
        return s
    p = [float(r['pressure_kPa']) for r in good]
    c = [float(r['CP_pF']) for r in good]
    v = [float(r['VDIFF_mV']) for r in good]
    ps, _, r2, nl = linear_fit(p,v)
    cs, _, _, _ = linear_fit(c,v)
    sp, sc = [], []
    for i in range(len(good)):
        lo,hi=max(0,i-1),min(len(good)-1,i+1)
        sp.append((v[hi]-v[lo])/(p[hi]-p[lo]))
        sc.append((v[hi]-v[lo])/(c[hi]-c[lo]))
        good[i]['local_sensitivity_mV_per_kPa']=sp[-1]
        good[i]['local_sensitivity_mV_per_pF']=sc[-1]
    s.update(avg_pressure_sensitivity_mV_per_kPa=ps,
             avg_cap_sensitivity_mV_per_pF=cs,
             min_local_abs_pressure_sensitivity_mV_per_kPa=min(map(abs,sp)),
             max_local_abs_pressure_sensitivity_mV_per_kPa=max(map(abs,sp)),
             R_squared=r2, nonlinearity_pct_FS=nl,
             vdiff_span_mV=max(v)-min(v),
             max_cycle_drift_mV=max(float(r['cycle_drift_mV']) for r in good),
             max_TX_voltage_V=max(max(float(r['TXP_MAX_ALL_V']),float(r['TXN_MAX_ALL_V'])) for r in good),
             max_VCM_OUT_error_mV=max(abs(float(r['VCM_OUT_V'])-2.5)*1000 for r in good),
             output_monotonic=int(all(b>=a-1e-4 for a,b in zip(v,v[1:])) or
                                  all(b<=a+1e-4 for a,b in zip(v,v[1:]))),
             error='' if len(good)==expected else 'Incomplete curve: do not rank')
    return s


def run_ngspice(case_dir: Path, total_timeout_s: float, heartbeat_s: float,
                number: int, total: int) -> tuple[int,float]:
    """Write live log; print terminal heartbeat while ngspice is still running."""
    logfile=case_dir/'ngspice.log'
    start=time.monotonic()
    with logfile.open('w',encoding='utf-8') as log:
        proc=subprocess.Popen(['ngspice','-b','case.spice'], cwd=case_dir,
                              stdout=log, stderr=subprocess.STDOUT)
        try:
            while True:
                elapsed=time.monotonic()-start
                remaining=total_timeout_s-elapsed
                if remaining<=0:
                    proc.kill();proc.wait()
                    raise TimeoutError(f'ngspice exceeded --timeout {total_timeout_s:g}s; see {logfile}')
                try:
                    rc=proc.wait(timeout=min(heartbeat_s,remaining))
                    return rc, time.monotonic()-start
                except subprocess.TimeoutExpired:
                    elapsed=time.monotonic()-start
                    kb=logfile.stat().st_size/1024 if logfile.exists() else 0
                    print(f'[{number:03}/{total:03}] RUNNING | elapsed={elapsed:.0f}s '
                          f'| log={kb:.1f}KB | {logfile}', flush=True)
        except KeyboardInterrupt:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill();proc.wait()
            raise


def case_path(root: Path, cf: float, cn: float, pressure: float) -> Path:
    return root/'runs'/f'CF_{cf:g}pF'/f'CN_{cn:g}pF'/f'P_{pressure:g}kPa'


def main(argv=None) -> int:
    ap=argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--netlist', type=Path, help='Xschem-generated baseline .spice file')
    ap.add_argument('--out',type=Path,default=DEFAULT_OUT,help='Experiment 3 result directory')
    ap.add_argument('--start',type=float,default=30,help='Start pressure in kPa (default 30)')
    ap.add_argument('--stop',type=float,default=120,help='Stop pressure in kPa (default 120)')
    ap.add_argument('--step',type=float,default=5,help='Pressure increment in kPa (default 5)')
    ap.add_argument('--cn',type=float,nargs='+',default=[8,9,10,11,12],
                    help='Reference CN pF values (default: 8 9 10 11 12)')
    ap.add_argument('--cf',type=float,nargs='+',default=[30,40,50,60],
                    help='Nominal feedback CF targets pF (default: 30 40 50 60)')
    ap.add_argument('--stop-us',type=float,default=1700,help='Transient duration in us')
    ap.add_argument('--timestep-ns',type=float,default=80,help='Max transient step in ns')
    ap.add_argument('--sample-margin-us',type=float,default=2,
                    help='Sample this many us before phi2 falling edge')
    ap.add_argument('--heartbeat',type=float,default=10,
                    help='Print RUNNING update every N seconds (default 10)')
    ap.add_argument('--timeout',type=float,default=900,help='Maximum ngspice runtime per case, seconds')
    ap.add_argument('--dry-run',action='store_true',help='Write case decks, do not execute ngspice')
    ap.add_argument('--restart',action='store_true',help='Rerun even previously successful cases')
    ap.add_argument('--no-waveforms',action='store_true',
                    help='Keep summary CSVs and logs but do not retain per-case waveform CSVs')
    ap.add_argument('--keep-raw',action='store_true',help='Retain raw ngspice waveforms.dat files')
    args=ap.parse_args(argv)

    try:
        netlist=find_netlist(args.netlist)
        ps=pressure_points(args.start,args.stop,args.step)
        if args.heartbeat<=0 or args.timeout<=0 or args.sample_margin_us<=0:
            raise ValueError('heartbeat, timeout and sample-margin-us must be positive')
        for label, vals in [('CN',args.cn),('CF',args.cf)]:
            if not vals or any(not math.isfinite(x) or x<=0 for x in vals) or len(vals)!=len(set(vals)):
                raise ValueError(f'{label} values must be distinct, finite positive numbers')
        if not args.dry_run and not shutil.which('ngspice'):
            raise RuntimeError('ngspice not found on PATH')
        root=args.out.expanduser().resolve()
        if args.dry_run:
            root = root / 'dry_run'  # Never overwrite real simulation results.
        root.mkdir(parents=True,exist_ok=True)
        text=netlist.read_text(encoding='utf-8',errors='replace')
        total=len(ps)*len(args.cf)*len(args.cn)
        print('=== CapSense Experiment 3: pressure × CN × CF ===',flush=True)
        print(f'Baseline: {netlist}',flush=True)
        print(f'Output:   {root}',flush=True)
        print(f'Cases:    {len(ps)} pressures × {len(args.cn)} CN × {len(args.cf)} CF = {total}',flush=True)
        print(f'Progress every {args.heartbeat:g}s during an active ngspice run. '
              'Ctrl+C stops safely; successful cases are reusable.',flush=True)
        if args.dry_run: print('DRY RUN: generating decks only, no ngspice.',flush=True)

        all_rows=[]
        summaries=[]
        number=0
        for cf in args.cf:
            for cn in args.cn:
                group=[]
                for pressure in ps:
                    number+=1
                    case=case_path(root,cf,cn,pressure)
                    case.mkdir(parents=True,exist_ok=True)
                    cp=murata_cp_pf(pressure)
                    row=dict(pressure_kPa=pressure, CP_pF=round(cp,10),
                             CN_pF=cn, deltaC_pF=round(cp-cn,10),
                             CF_target_pF=cf, CFB_L_um=BASELINE_CFB_L_UM*cf/BASELINE_CF_PF,
                             status='PENDING', error='', case_dir=str(case))
                    try:
                        deck,warnings=build_deck(text,netlist.parent,pressure,cn,cf,
                                                 args.stop_us,args.timestep_ns)
                        old_deck=(case/'case.spice').read_text(encoding='utf-8') if (case/'case.spice').exists() else None
                        state_path=case/'case_state.json'
                        old={}
                        if state_path.exists():
                            try: old=json.loads(state_path.read_text(encoding='utf-8'))
                            except (ValueError,OSError): pass
                        if (not args.restart and not args.dry_run and old_deck==deck and
                            old.get('status')=='OK' and
                            (args.no_waveforms or (case/'waveforms.csv').is_file())):
                            row.update(old)
                            row['status']='OK'
                            print(f'[{number:03}/{total:03}] SKIP OK  '
                                  f'P={pressure:g}kPa CN={cn:g}pF CF={cf:g}pF (saved result)',flush=True)
                        else:
                            (case/'case.spice').write_text(deck,encoding='utf-8')
                            if warnings:
                                print(f'[{number:03}/{total:03}] NOTE: '+ '; '.join(warnings),flush=True)
                            if args.dry_run:
                                row['status']='DRY_RUN'
                                print(f'[{number:03}/{total:03}] DRY RUN P={pressure:g}kPa '
                                      f'CP={cp:.4f}pF CN={cn:g}pF CF={cf:g}pF',flush=True)
                            else:
                                print(f'[{number:03}/{total:03}] START   P={pressure:g}kPa '
                                      f'CP={cp:.4f}pF CN={cn:g}pF CF={cf:g}pF',flush=True)
                                (case/'waveforms.dat').unlink(missing_ok=True)
                                (case/'waveforms.csv').unlink(missing_ok=True)
                                rc, elapsed=run_ngspice(case,args.timeout,args.heartbeat,number,total)
                                row['elapsed_s']=round(elapsed,2)
                                if rc!=0:
                                    raise RuntimeError(f'ngspice exit code {rc}; see {case / "ngspice.log"}')
                                row.update(measure_waveforms(case/'waveforms.dat',args.stop_us,
                                                             args.sample_margin_us))
                                if not args.no_waveforms:
                                    export_waveforms_csv(case/'waveforms.dat',case/'waveforms.csv')
                                if not args.keep_raw:
                                    (case/'waveforms.dat').unlink(missing_ok=True)
                                row['TX_over_5V_warning']=int(max(float(row['TXP_MAX_ALL_V']),
                                                                 float(row['TXN_MAX_ALL_V']))>5.0)
                                row['status']='OK'
                                print(f'[{number:03}/{total:03}] OK      elapsed={elapsed:.1f}s '
                                      f'VDIFF={row["VDIFF_mV"]:.4f}mV '
                                      f'TXmax={max(row["TXP_MAX_ALL_V"],row["TXN_MAX_ALL_V"]):.3f}V',flush=True)
                    except KeyboardInterrupt:
                        row['status']='INTERRUPTED'
                        row['error']='Interrupted by user'
                        group.append(row); all_rows.append(row)
                        atomic_csv(root/'measurements.csv',all_rows,MEASURE_COLUMNS)
                        atomic_json(case/'case_state.json',row)
                        print('\nInterrupted. Existing CSV/results have been saved.',flush=True)
                        return 130
                    except Exception as exc:
                        row['status']='FAILED'
                        row['error']=f'{type(exc).__name__}: {exc}'
                        print(f'[{number:03}/{total:03}] FAILED  {row["error"]}',flush=True)
                    group.append(row)
                    all_rows.append(row)
                    atomic_json(case/'case_state.json',row)
                    atomic_csv(root/'measurements.csv',all_rows,MEASURE_COLUMNS)
                summary=summarize_group(group,len(ps),cn,cf)
                summaries.append(summary)
                summary_fields=list(dict.fromkeys(k for r in summaries for k in r))
                atomic_csv(root/'summary.csv',summaries,summary_fields)
                # Now group local sensitivities are populated, so update main CSV.
                atomic_csv(root/'measurements.csv',all_rows,MEASURE_COLUMNS)
                print(f'== GROUP COMPLETE: CF={cf:g}pF CN={cn:g}pF '
                      f'OK={summary["successful_points"]}/{len(ps)} ==',flush=True)
        good=sum(r['status']=='OK' for r in all_rows)
        print(f'\nFinished: {good}/{total} successful cases.',flush=True)
        print(f'CSV files: {root / "measurements.csv"} | {root / "summary.csv"}',flush=True)
        print('CP_pF/CN_pF are INPUT capacitances; CF_target_pF is a NOMINAL geometry target.',flush=True)
        return 0 if (good==total or args.dry_run) else 2
    except (RuntimeError,ValueError,FileNotFoundError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr,flush=True)
        return 2


if __name__=='__main__':
    sys.exit(main())
