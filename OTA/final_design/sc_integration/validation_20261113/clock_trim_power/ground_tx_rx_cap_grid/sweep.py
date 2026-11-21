"""Sweep 1–15 pF sensor pairs in the ground-discharge and ground-clamp readout."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import argparse
import csv
import os
import re
import shutil
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
VECTORS = 'v(sump) v(sumn) v(outp) v(outn) v(holdp) v(holdn)'
SELECTED = ((1,1),(1,15),(7,7),(12,7),(15,1),(15,15),(12,12))


def fixture():
    text = (BASE/'benches/bias3_7.cir').read_text()
    text, count = re.subn(r'(?m)^(M[NP]_(?:discharge|clamp)_[pn]) vref_sw ', r'\1 0 ', text)
    if count != 8:
        raise ValueError(f'Expected eight TX-discharge/RX-clamp devices, found {count}')
    if 'CP=12p CN=7p' not in text:
        raise ValueError('Expected original sensor values in the reference bench')
    text = text.split('.control',1)[0]
    return re.sub(r'(?m)^\.save .*$', '.save '+VECTORS, text)


def read_trace(path):
    header, raw = path.read_bytes().split(b'Binary:\n',1)
    count = int(re.search(rb'No\. Points:\s*(\d+)',header)[1])
    variables = [v.lower().decode() for v in re.findall(rb'(?m)^\s*\d+\s+(\S+)\s+(?:time|voltage)\s*$',header)]
    if variables != ['time', *VECTORS.split()] or len(raw) != count*7*8:
        raise ValueError('Unexpected ngspice raw data format')
    a = np.frombuffer(raw, dtype='<f8').reshape(count,7)
    if a[-1,0] < 82.995e-6 or not np.isfinite(a).all():
        raise ValueError('Incomplete or invalid transient')
    return a


def measurements(path):
    t, sp, sn, op, on, hp, hn = read_trace(path).T
    t = t*1e6
    transfer = (t >= 40)&(t <= 70)
    aq = (t >= 69.7)&(t <= 80)
    live = (t >= 40)&(t <= 81)
    icm, ocm, hcm = (sp+sn)/2, (op+on)/2, (hp+hn)/2
    row = {}
    for name,cm in [('input',icm),('output',ocm)]:
        extremum = np.argmin(cm[transfer])
        row[f'{name}_transfer_cm_min_V'] = float(cm[transfer][extremum])
        row[f'{name}_transfer_cm_min_time_us'] = float(t[transfer][extremum])
        row[f'{name}_transfer_cm_max_V'] = float(cm[transfer].max())
        row[f'{name}_track_cm_min_V'] = float(cm[aq].min())
        row[f'{name}_track_cm_max_V'] = float(cm[aq].max())
        row[f'{name}_cm_at_81us_V'] = float(np.interp(81,t,cm))
    row['ota_output_single_ended_min_V'] = float(min(op[live].min(),on[live].min()))
    row['ota_output_single_ended_max_V'] = float(max(op[live].max(),on[live].max()))
    row['held_cm_at_81us_V'] = float(np.interp(81,t,hcm))
    row['held_p_at_81us_V'] = float(np.interp(81,t,hp))
    row['held_n_at_81us_V'] = float(np.interp(81,t,hn))
    row['held_diff_at_81us_mV'] = float(np.interp(81,t,hp-hn)*1e3)
    row['live_diff_at_79p5us_mV'] = float(np.interp(79.5,t,op-on)*1e3)
    return row


def run(work, base, cp, cn, profiles):
    job = work/f'cp{cp:02}_cn{cn:02}'
    job.mkdir(parents=True,exist_ok=True)
    for name in ('blocks.spice','ota_bias.spice'):
        shutil.copyfile(BASE/name,job/name)
    original = base.replace('CP=12p CN=7p', f'CP={cp}p CN={cn}p')
    row = dict(cp_pF=cp, cn_pF=cn, cap_sum_pF=cp+cn, cap_diff_pF=cp-cn)
    errs = []
    (job/'.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
    for solver, method, timestep, tolerance, timeout in profiles:
        mode = f'{solver}_{method}'
        option = 'klu ' if solver=='klu' else ''
        deck = original + (f'\n.options {option}method={method} reltol={tolerance} trtol=10\n'
                           f'.tran {timestep}n 83u 0 {timestep}n\n.end\n')
        (job/'bench.cir').write_text(deck)
        trace_name = f'{mode}_{timestep}ns.raw'
        try:
            subprocess.run(['ngspice','-b','-r',trace_name,'-o',f'{mode}_{timestep}ns.log','bench.cir'],
                           cwd=job, env={**os.environ,'OMP_NUM_THREADS':'1'},
                           capture_output=True,check=True,timeout=timeout)
            log = (job/f'{mode}_{timestep}ns.log').read_text()
            if not re.search(r'No\. of Data Rows\s*:\s*[1-9]',log) or re.search(
                    r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
                raise ValueError('ngspice analysis failed')
            row.update(measurements(job/trace_name))
            row.update(solver=mode, max_step_ns=timestep, status='ok')
            return row
        except (OSError, ValueError, TypeError, IndexError, subprocess.SubprocessError) as err:
            errs.append(f'{mode}/{timestep} ns: {err}')
    row['status'] = ' | '.join(errs)
    return row


def restore(work, cp, cn, profiles):
    job=work/f'cp{cp:02}_cn{cn:02}'
    for solver, method, step, _, _ in profiles:
        mode=f'{solver}_{method}'
        try:
            log=(job/f'{mode}_{step}ns.log').read_text()
            # A partial output from an interrupted process cannot be resumed.
            if 'Total elapsed time' not in log or re.search(
                    r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
                continue
            result=measurements(job/f'{mode}_{step}ns.raw')
        except (OSError, ValueError, TypeError, IndexError):
            continue
        return dict(cp_pF=cp, cn_pF=cn, cap_sum_pF=cp+cn, cap_diff_pF=cp-cn,
                    **result, solver=mode, max_step_ns=step, status='ok')
    return None


def save(path, rows):
    rows=sorted(rows,key=lambda r: (r['cp_pF'],r['cn_pF']))
    fields=list(dict.fromkeys(k for r in rows for k in r))
    pending=path.with_suffix('.tmp')
    with pending.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    pending.replace(path)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('work',type=Path)
    parser.add_argument('--jobs',type=int,default=8)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--batch-size',type=int)
    resolution=parser.add_mutually_exclusive_group()
    resolution.add_argument('--refine',action='store_true')
    resolution.add_argument('--fine-grid',action='store_true')
    args=parser.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    pairs = SELECTED if args.refine else tuple(product(range(1,16),repeat=2))
    base = fixture()
    profiles=(('klu','trap',40,4e-4,60),('sparse','trap',40,4e-4,65),
              ('klu','gear',35,4e-4,80)) if args.refine or args.fine_grid else (
        ('klu','trap',120,1e-3,28),('sparse','trap',140,1e-3,31),('klu','gear',120,1e-3,38))
    rows = [r for cp,cn in pairs if (r:=restore(args.work,cp,cn,profiles))] if args.resume else []
    done={(r['cp_pF'],r['cn_pF']) for r in rows}
    pending=[pair for pair in pairs if pair not in done]
    pending=pending[:args.batch_size]
    print(f'{len(done)}/{len(pairs)} restored; running {len(pending)}',flush=True)
    with ThreadPoolExecutor(args.jobs) as pool:
        futures = [pool.submit(run,args.work,base,*pair,profiles) for pair in pending]
        for i, f in enumerate(as_completed(futures),1):
            row=f.result()
            rows.append(row)
            if row['status']!='ok' or i%10==0 or i==len(pending):
                print(f'{len(rows)}/{len(pairs)} complete; {sum(r["status"]=="ok" for r in rows)} passed',flush=True)
            if i%10==0 or i==len(pending):
                save(args.work/'results.csv',rows)


if __name__=='__main__':
    main()
