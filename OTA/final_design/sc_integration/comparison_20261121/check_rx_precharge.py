"""Screen RX-only precharge and measure transistor headroom in the extracted telescopic OTA."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from itertools import product
import re
import subprocess

import numpy as np

from compare import Case, ROOT, deck, measure, read_raw, save


MARGIN_SETS = {'tail': ('m1039',), 'input_pair': ('m1007','m1059')}
PROBES = [f'@m.xota.{m}[{a}]' for group in MARGIN_SETS.values()
          for m in group for a in ('vds','vdsat')]


def run(args):
    target, corner, pressure, offset, step = args
    case = Case('telescopic_C', corner, pressure, offset=offset, step=step,
                solver='gear' if corner=='hot' else 'trap')
    name = f'rx{target:g}_{case.name}'
    job = ROOT/'benches'/name
    job.mkdir(exist_ok=True)
    body, count = re.subn(r'(?m)^(M[NP]_clamp_[pn]) vref_sw ',r'\1 v_rx_pre ',deck(case))
    if count!=4:
        raise ValueError('Unexpected RX clamp network')
    body = body.replace('.save ',f'VRXTRIM v_rx_pre vref_sw {target-2.5:g}\n.save '
                        + ' '.join(PROBES) + ' ')
    (job/'bench.cir').write_text(body)
    (job/'.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
    row=dict(rx_precharge_nom_V=target, corner=corner, pressure_kPa=pressure,
             cp_offset_pF=offset, step_ns=step, case=name)
    try:
        subprocess.run(['ngspice','-b','-r','trace.raw','-o','run.log','bench.cir'],
                       cwd=job,check=True,timeout=95,stdout=subprocess.DEVNULL)
        log=(job/'run.log').read_text()
        if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
            raise ValueError('Simulation did not complete')
        r=measure(job/'trace.raw',case)
        raw=read_raw(job/'trace.raw',case)
        t=1e6*raw['time']
        icm=(raw['v(sump)']+raw['v(sumn)'])/2
        window=(t>=40)&(t<=r['track_stop_us'])
        track=(t>=r['track_start_us'])&(t<=r['track_stop_us'])
        i=np.flatnonzero(window)[np.argmin(icm[window])]
        row.update(icm_switch_min_V=icm[i],icm_min_time_us=t[i],
                   icm_at_sample_V=r['sampled_input_cm_V'],held_diff_mV=r['held_diff_mV'],
                   held_cm_V=r['held_cm_V'],settle_slack_us=r['settling_slack_us'],
                   ota_uW=r['ota_uW'],readout_mW=r['readout_mW'])
        for key,group in MARGIN_SETS.items():
            margins=[]
            for m in group:
                def vector(a):
                    k=f'@m.xota.{m}[{a}]'
                    return raw[k] if k in raw else raw[f'v({k})']
                margins.append(1e3*(abs(vector('vds'))-abs(vector('vdsat'))))
            margin=np.minimum.reduce(margins)
            if np.ptp(margin[window])<.01:
                raise ValueError(f'{key} probe was static')
            row[f'{key}_min_switch_mV']=min(margin[window])
            row[f'{key}_min_track_mV']=min(margin[track])
            row[f'{key}_at_sample_mV']=np.interp(r['sample_us'],t,margin)
        row['status']='ok'
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        row['status']=str(exc)
    print(name,row['status'],flush=True)
    return row


def main():
    tests=[(v,c,p,o,60) for v,(c,p,o) in product((2.5,2.65,2.8,3.0),
            [('typ',p,0) for p in (30,90,100,110,120)]
            + [('hot',120,0),('hot',120,2.71),('cold',120,0)])]
    with ThreadPoolExecutor(6) as pool:
        rows=list(pool.map(run,tests))
    save(ROOT/'input_common_mode_rx_precharge.csv',rows)
    if any(r['status']!='ok' for r in rows):
        raise SystemExit(1)


if __name__=='__main__':
    main()

