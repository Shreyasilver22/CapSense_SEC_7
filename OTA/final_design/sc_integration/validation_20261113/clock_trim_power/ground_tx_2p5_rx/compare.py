"""Compare TX discharge levels with RX held at the 2.5 V precharge reference."""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import re
import shutil
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PAIRS = ((7, 7), (12, 7), (12, 12), (15, 15), (15, 1), (1, 15))
DEVICES = {
    'input_pair': ('m1007', 'm1059'),
    'tail': ('m1039',),
    'n_cascode': ('m1015', 'm1033'),
    'p_cascode': ('m1041', 'm1042'),
    'p_load': ('m1008', 'm1045'),
}
NODES = ('sump', 'sumn', 'outp', 'outn', 'holdp', 'holdn', 'tr', 'phit',
         'phi2', 'txp', 'txn', 'rxp', 'rxn', 'vref_sw')
VECTORS = [f'v({node})' for node in NODES]
VECTORS += [f'@m.xota.{device}[{param}]' for devices in DEVICES.values()
            for device in devices for param in ('vds', 'vdsat')]
ERROR = r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small'


def raw_trace(path):
    header, raw = path.read_bytes().split(b'Binary:\n', 1)
    names = [m.decode().lower() for m in
             re.findall(rb'(?m)^\s*\d+\s+(\S+)\s+\S+[^\n]*$', header)]
    count = int(re.search(rb'No\. Points:\s*(\d+)', header)[1])
    data = np.frombuffer(raw, dtype='<f8').reshape(count, len(names))
    if data[-1, 0] < 89.999e-6 or not np.isfinite(data).all():
        raise ValueError('Incomplete or nonfinite waveform')
    return dict(zip(names, data.T))


def deck_for(tx, cp, cn, step, corner='nominal', solver='klu_trap'):
    template = {'nominal': 'bias3_7.cir', 'cold': 'bias0_7.cir', 'hot': 'bias5_12.cir'}[corner]
    deck = (BASE / 'benches' / template).read_text().split('.control', 1)[0]
    deck, params = re.subn(r'\bCP=12p CN=(?:7|12)p\b', f'CP={cp:g}p CN={cn:g}p', deck)
    discharge = r'(?m)^(M[NP]_discharge_[pn]) vref_sw '
    clamp = r'(?m)^M[NP]_clamp_[pn] vref_sw '
    if params != 1 or len(re.findall(discharge, deck)) != 4 or len(re.findall(clamp, deck)) != 4:
        raise ValueError('Unexpected TX discharge or RX precharge connections')
    if tx == 0:
        deck = re.sub(discharge, r'\1 0 ', deck)
    deck = re.sub(r'(?m)^\.save .*$', '.save ' + ' '.join(VECTORS), deck)
    options = {'klu_trap': 'klu method=trap reltol=4e-4 trtol=10',
               'sparse_gear': 'method=gear',
               'klu_gear_gmin': 'klu method=gear gmin=1e-11 itl1=400'}[solver]
    return deck + (f'\n.options {options}\n'
                   f'.tran {step}n 90u 0 {step}n\n.end\n')


def crossing(t, y, threshold, rising, window):
    left, right = y[:-1] - threshold, y[1:] - threshold
    crossed = (left < 0) & (right >= 0) if rising else (left >= 0) & (right < 0)
    where = np.flatnonzero(crossed & (t[:-1] >= window[0]) & (t[1:] <= window[1]))
    if len(where) != 1:
        raise ValueError(f'Expected one clock transition in {window}, got {len(where)}')
    i = where[0]
    return float(np.interp(threshold, y[i:i+2] if rising else y[i:i+2][::-1],
                           t[i:i+2] if rising else t[i:i+2][::-1]))


def measure(path, vdd):
    data = raw_trace(path)
    t = data['time'] * 1e6
    node = {key: data[f'v({key})'] for key in NODES}
    start = crossing(t, node['phi2'], vdd / 2, True, (40, 65))
    track_on = crossing(t, node['tr'], vdd / 2, True, (60, 78))
    track_off = crossing(t, node['tr'], vdd / 2, False, (75, 87))
    input_cm = (node['sump'] + node['sumn']) / 2
    output_cm = (node['outp'] + node['outn']) / 2
    hold_cm = (node['holdp'] + node['holdn']) / 2
    live = (node['outp'] - node['outn']) * 1e3
    hold = (node['holdp'] - node['holdn']) * 1e3
    late = (t >= 87) & (t <= 89)
    if min(node['phi2'][late].min(), node['phit'][late].min()) < vdd / 2:
        raise ValueError('Settled reference is outside the transfer phase')
    target = float(np.median(live[late]))
    error_band = max(abs(target) * .001, .1)
    transfer = (t >= 40) & (t <= track_off)
    post = (t >= 55) & (t <= track_off)
    tracking = (t >= track_on) & (t <= track_off)
    settled_edge = min(float(t[-1]), track_off - .15)
    before_sample = (t >= start) & (t <= settled_edge)
    misses = np.flatnonzero(before_sample & (np.abs(live - target) > error_band))
    if len(misses):
        idx = misses[-1] + 1
        settled = float(t[idx]) if t[idx] <= settled_edge else np.nan
    else:
        settled = start
    at = lambda y, instant: float(np.interp(instant, t, y))
    result = dict(
        tx_edge_us=start, track_start_us=track_on, track_end_us=track_off,
        input_cm_min_V=float(input_cm[transfer].min()),
        input_cm_min_after_55us_V=float(input_cm[post].min()),
        input_cm_at_81us_V=at(input_cm, 81),
        output_cm_min_V=float(output_cm[transfer].min()),
        held_cm_at_81us_V=at(hold_cm, 81), held_diff_mV=at(hold, 81),
        settled_live_diff_mV=target, band_mV=error_band,
        live_pre_hold_error_mV=at(live, settled_edge) - target,
        held_error_mV=at(hold, 81) - target,
        pre_hold_settle_us=settled, settle_slack_us=track_off - settled,
        live_settled_reference_span_mV=float(np.ptp(live[late])),
        min_output_V=float(min(node['outp'][transfer].min(), node['outn'][transfer].min())),
        max_output_V=float(max(node['outp'][transfer].max(), node['outn'][transfer].max())),
        min_rx_V=float(min(node['rxp'][transfer].min(), node['rxn'][transfer].min())),
        vref_min_V=float(node['vref_sw'][transfer].min()),
        vref_max_V=float(node['vref_sw'][transfer].max()),
    )
    for group, devices in DEVICES.items():
        margins = []
        for device in devices:
            def param(name):
                key = f'@m.xota.{device}[{name}]'
                return data[key] if key in data else data[f'v({key})']
            margins.append((np.abs(param('vds')) - np.abs(param('vdsat'))) * 1000)
        margin = np.min(margins, axis=0)
        if np.ptp(margin) < 1e-6:
            raise ValueError(f'{group} saved margin is static')
        result[f'{group}_transfer_margin_mV'] = float(margin[transfer].min())
        result[f'{group}_track_margin_mV'] = float(margin[tracking].min())
        t_transfer = t[transfer]
        margin_transfer = margin[transfer]
        result[f'{group}_min_margin_time_us'] = float(t_transfer[np.argmin(margin_transfer)])
        result[f'{group}_below_saturation_us'] = float(
            np.sum(np.diff(t_transfer)[(margin_transfer[:-1] < 0) & (margin_transfer[1:] < 0)]))
    return result


def case_folder(work, tx, cp, cn, step):
    return work / f'tx{tx:g}_cp{cp:g}_cn{cn:g}_{step}ns'


def run(work, case, corner='nominal', solver='klu_trap'):
    tx, cp, cn, step = case
    job = case_folder(work if corner == 'nominal' else work / corner, *case)
    if solver != 'klu_trap':
        job = job.with_name(f'{job.name}_{solver}')
    job.mkdir(parents=True, exist_ok=True)
    for name in ('blocks.spice', 'ota_bias.spice'):
        shutil.copyfile(BASE / name, job / name)
    (job / '.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
    (job / 'bench.cir').write_text(deck_for(*case, corner, solver))
    vdd = {'nominal': 5, 'cold': 4.5, 'hot': 5.5}[corner]
    row = dict(tx_discharge_V=tx, rx_precharge_nominal_V=2.5, cp_pF=cp, cn_pF=cn,
               max_step_ns=step, profile=corner, vdd_V=vdd, solver=solver)
    try:
        subprocess.run(['ngspice', '-b', '-r', 'trace.raw', '-o', 'run.log', 'bench.cir'],
                       cwd=job, capture_output=True, check=True, timeout=150)
        log = (job / 'run.log').read_text()
        if 'Total elapsed time' not in log or re.search(ERROR, log):
            raise ValueError('ngspice did not complete the transient')
        row.update(measure(job / 'trace.raw', vdd), status='ok')
    except (KeyError, OSError, ValueError, subprocess.SubprocessError) as exc:
        row['status'] = str(exc)
    print(f'{job.name} {row["status"]}', flush=True)
    return row


def save(path, rows):
    with path.open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('work', type=Path)
    parser.add_argument('sweep', choices=('nominal', 'sensitivity', 'refine', 'hot-retries'))
    parser.add_argument('--corner', choices=('nominal', 'cold', 'hot'), default='nominal')
    parser.add_argument('--jobs', type=int, default=8)
    args = parser.parse_args()
    if args.sweep == 'hot-retries':
        trials = list(product(((2.5, 12, 7, 40), (2.5, 15, 15, 40)),
                              ('sparse_gear', 'klu_gear_gmin')))
        with ThreadPoolExecutor(args.jobs) as pool:
            rows = list(pool.map(lambda trial: run(args.work, trial[0], 'hot', trial[1]), trials))
        save(args.work / 'hot_retries.csv', rows)
        if any(row['status'] != 'ok' for row in rows):
            raise SystemExit(1)
        return
    if args.sweep == 'sensitivity':
        pairs = [(round(cp + dp, 2), round(cn + dn, 2)) for cp, cn in PAIRS
                 for dp, dn in ((.1, 0), (-.1, 0), (0, .1), (0, -.1))]
        step = 40
    elif args.sweep == 'refine':
        pairs, step = ((12, 7), (15, 15), (15, 1), (1, 15)), 10
    else:
        pairs, step = (PAIRS if args.corner == 'nominal' else ((12, 7), (15, 15))), 40
    cases = [(tx, cp, cn, step) for tx, (cp, cn) in product((0, 2.5), pairs)]
    with ThreadPoolExecutor(args.jobs) as pool:
        rows = list(pool.map(lambda case: run(args.work, case, args.corner), cases))
    suffix = '' if args.corner == 'nominal' else f'_{args.corner}'
    save(args.work / f'{args.sweep}{suffix}.csv', rows)
    if any(row['status'] != 'ok' for row in rows):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
