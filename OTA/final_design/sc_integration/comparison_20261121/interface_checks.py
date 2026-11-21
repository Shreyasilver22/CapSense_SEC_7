"""Check datasheet endpoint tolerances and a representative direct SAR sampling load."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
import re
import subprocess

import numpy as np

from compare import Case, OTAS, ROOT, deck, read_raw, run, save


def adc_trial(case):
    # 5 pF per ADC pin, initially discharged, acquires for 1 us in the hold interval.
    work = ROOT/'benches'/f'direct_adc_{case.ota}'
    work.mkdir(exist_ok=True)
    content = deck(case).replace('.save ','.save v(adcp) v(adcn) ')
    branch = '''
VADC adc_sw 0 PULSE(0 1 82u 1n 1n 1u 100u)
VDIS dis_sw 0 PULSE(1 0 81.9u 1n 1n 1.3u 100u)
.model SWMOD SW(Ron=100 Roff=1e13 Vt=.5 Vh=.01)
'''
    for b in 'pn':
        branch += f'CADC{b} adc{b} 0 5p\nSADC{b} pin{b} adc{b} adc_sw 0 SWMOD\nSDIS{b} adc{b} 0 dis_sw 0 SWMOD\n'
    (work/'bench.cir').write_text(content.replace('.save ',branch+'.save '))
    (work/'.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
    row = dict(ota=case.ota,pressure_kPa=case.pressure,acquisition_us=1,adc_cap_pF=5)
    try:
        subprocess.run(['ngspice','-b','-r','trace.raw','-o','run.log','bench.cir'],
                       cwd=work,check=True,timeout=105,stdout=subprocess.DEVNULL)
        raw=read_raw(work/'trace.raw',case)
        t=raw['time']*1e6
        pin=raw['v(pinp)']-raw['v(pinn)']
        adc=raw['v(adcp)']-raw['v(adcn)']
        row.update(pre_adc_diff_mV=1e3*np.interp(81.95,t,pin),
                   sampled_adc_diff_mV=1e3*np.interp(82.95,t,adc),
                   sampled_adc_cm_V=np.interp(82.95,t,(raw['v(adcp)']+raw['v(adcn)'])/2),
                   status='ok')
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        row['status']=str(exc)
    print(row,flush=True)
    return row


def main():
    cases = [Case(a,'typ',p,offset=c) for a in OTAS
             for p,c in ((30,-.50),(30,.50),(120,-1.58),(120,2.71))]
    with ThreadPoolExecutor(6) as pool:
        rows=list(pool.map(run,cases))
        save(ROOT/'sensor_endpoints.csv',rows)
        adc=list(pool.map(adc_trial,[Case(a,'typ',100) for a in OTAS]))
        save(ROOT/'direct_adc.csv',adc)


if __name__ == '__main__':
    main()

