"""Sweep both sensor branches in the nominal integrated readout."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import argparse
import csv
import re
import shutil
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
VALUES = (7, 9.5, 12)
VECTORS = 'v(sump) v(sumn) v(outp) v(outn) v(holdp) v(holdn)'

def run(work, cp, cn, tx_low):
    job = work / f'tx{tx_low:g}_cp{cp:g}_cn{cn:g}'
    job.mkdir(parents=True, exist_ok=True)
    for name in ('blocks.spice', 'ota_bias.spice'):
        shutil.copyfile(BASE / name, job / name)
    deck = (BASE / 'benches/bias3_7.cir').read_text()
    deck = deck.replace('CP=12p CN=7p', f'CP={cp:g}p CN={cn:g}p')
    if tx_low == 0:
        deck = re.sub(r'(?m)^(M[NP]_discharge_[pn]) vref_sw ', r'\1 0 ', deck)
    deck = re.sub(r'(?m)^\.save .*$', '.save ' + VECTORS, deck)
    deck = re.sub(r'(?m)^wrdata trace.dat .*$', 'wrdata trace.dat ' + VECTORS, deck)
    (job / 'bench.cir').write_text(deck)
    row = {'tx_low_V': tx_low, 'cp_pF': cp, 'cn_pF': cn, 'sum_pF': cp+cn, 'difference_pF': cp-cn}
    try:
        subprocess.run(['ngspice', '-b', '-o', 'run.log', 'bench.cir'], cwd=job,
                       capture_output=True, check=True, timeout=105)
        errors = re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',
                           (job / 'run.log').read_text())
        data = np.loadtxt(job / 'trace.dat', skiprows=1)
        if errors or data[-1,0]<102.99e-6 or not np.isfinite(data).all():
            raise ValueError('Incomplete transient')
        time, sp, sn, op, on, hp, hn = data.T
        time *= 1e6
        # Same phase window as previous validation, before the end of acquisition.
        transfer = (time>=40)&(time<=70)
        for name, node in [('input', (sp+sn)/2), ('output', (op+on)/2)]:
            row[f'{name}_transfer_cm_min_V'] = float(node[transfer].min())
            row[f'{name}_transfer_cm_max_V'] = float(node[transfer].max())
            row[f'{name}_cm_at_81us_V'] = float(np.interp(81,time,node))
        row['held_cm_at_81us_V'] = float(np.interp(81,time,(hp+hn)/2))
        row['held_diff_at_81us_mV'] = float(1000*np.interp(81,time,hp-hn))
        row['ideal_input_cm_V'] = 2.5 - (5-tx_low)*(cp+cn)/(100+cp+cn)
        row['status'] = 'ok'
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        row['status'] = str(exc)
    print(f'TX {tx_low:g} V · {cp:g}/{cn:g} pF {row["status"]}', flush=True)
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('work', type=Path)
    parser.add_argument('--jobs', type=int, default=5)
    parser.add_argument('--ground-check', action='store_true')
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    if args.ground_check:
        cases = ((7,7,0), (12,7,0), (12,12,0))
    else:
        cases = [(p,n,2.5) for p,n in product(VALUES,repeat=2)]
    with ThreadPoolExecutor(args.jobs) as pool:
        rows = list(pool.map(lambda case:run(args.work,*case), cases))
    with (args.work / 'results.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=list(dict.fromkeys(k for row in rows for k in row)))
        writer.writeheader()
        writer.writerows(rows)

if __name__=='__main__':
    main()
