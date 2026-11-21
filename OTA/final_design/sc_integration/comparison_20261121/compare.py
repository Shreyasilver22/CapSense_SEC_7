"""Matched SCB10H transient comparison. Run in WSL with ngspice."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from itertools import product
from pathlib import Path
import argparse
import os
import csv
import re
import shutil
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT.parent / 'validation_20261113/clock_trim_power'
CIRCUITS = ROOT / 'fixtures'
PDK = Path(os.environ.get('SCL08_MODELS', Path.home() / 'pdk/scl08/ngspice_models49')).expanduser()
OTA_C = ROOT.parent / 'integrated_sc_ota/models/telescopic_C.spice'
BASELINES = {'typ': ('bias3_7.cir', 5), 'cold': ('bias0_7.cir', 4.5),
             'hot': ('bias5_12.cir', 5.5)}
OTAS = ('telescopic', 'boosted', 'telescopic_C', 'boosted_C')
NODES = ('outp','outn','holdp','holdn','pinp','pinn','sump','sumn',
         'txp','rxp','phi2','phit','tr','pr','vref_sw','vbn','vbp')
VECTORS = [f'v({node})' for node in NODES] + ['i(vdd)','i(vota)','i(vbiasdd)','i(vclkdd)',
                                                 'i(vbufdd)','i(viref)','i(vrefsrc)']
PRESSURES = (30,45,60,75,90,100,110,120)


def capacitance(p):
    # Murata doc 82 1251 00 C, SCB10H-B012FB, nominal pF and kPa.
    c0, k = 2.24, 509
    return 0.9 + c0/(1-c0*p/k) + 1.759*c0/(1-c0*p/(1.485*k))


@dataclass(frozen=True)
class Case:
    ota: str
    corner: str
    pressure: int
    load: str = 'board'
    offset: float = 0
    step: int = 60
    cycles: int = 1
    solver: str = 'trap'
    bias_v: float = 1.7

    @property
    def name(self):
        return (f'{self.ota}_{self.corner}_{self.pressure}kPa_{self.load}_'
                f'{self.offset:+g}pF_{self.step}ns_{self.cycles}cycle_'
                f'{self.solver}_{self.bias_v:g}V')


def subckt_files():
    model_dir = ROOT / 'models'
    model_dir.mkdir(exist_ok=True)
    schematic = (CIRCUITS/'cmfb_revision_20261101/models/schematic.spice').read_text()
    if schematic.count('ota_telescopic_layout') != 2:
        raise ValueError('Unexpected telescopic schematic source')
    (model_dir/'telescopic.spice').write_text(
        schematic.replace('ota_telescopic_layout','ota_telescopic_cm2p5'))
    shutil.copyfile(OTA_C, model_dir/'telescopic_C.spice')
    boosted = (CIRCUITS/'models/gain_boosted.spice').read_text()
    if len(re.findall(r'(?m)^VR vr 0 1\.1$', boosted)) != 1:
        raise ValueError('Unexpected gain booster reference source')
    (model_dir/'boosted.spice').write_text(re.sub(
        r'(?m)^VR vr 0 1\.1$', 'VR vr 0 {NBOOST}', boosted))
    shutil.copyfile(FIXTURES/'blocks.spice', model_dir/'blocks.spice')
    shutil.copyfile(FIXTURES/'ota_bias.spice', model_dir/'ota_bias.spice')


def deck(case):
    fixture, vdd = BASELINES[case.corner]
    content = (FIXTURES/'benches'/fixture).read_text().split('.save',1)[0]
    content = content.replace('/home/your-user/pdk/scl08/ngspice_models49', str(PDK))
    content, count = re.subn(r'(?m)^\.include .*ota_cm2p5_C\.spice"$',
                             f'.include "../../models/{case.ota}.spice"',content)
    assert count == 1
    content, count = re.subn(r'(?m)^\.param CP=.*$',
        f'.param CP={capacitance(case.pressure)+case.offset:.9f}p CN=10p NBOOST={case.bias_v:g}',
        content)
    assert count == 1
    content, count = re.subn(r'(?m)^(M[NP]_discharge_[pn]) vref_sw ',r'\1 0 ',content)
    assert count == 4
    content = content.replace('.include blocks.spice','.include "../../models/blocks.spice"')
    content = content.replace('.include ota_bias.spice','.include "../../models/ota_bias.spice"')
    old = 'XOTA sumn sump outp outn vdd 0 bias vref vbn vbp ota_telescopic_cm2p5'
    if old not in content:
        raise ValueError('Missing OTA instance')
    if case.ota == 'boosted':
        new = ('XOTA sumn sump outp outn ota_vdd bias vref ota_gain_boosted\n'
               'MREF_OTA bias bias 0 0 N W=20u L=3.2u AD=90p AS=90p PD=49u PS=49u')
    elif case.ota.startswith('boosted_C'):
        new = ('XOTA sumn sump outp outn ota_vdd 0 bias vref nboost pboost ota_boosted_layout\n'
               'VNBOOST nboost 0 {NBOOST}\nVPBOOST pboost ota_vdd -1.2')
    else:
        new = old.replace('outn vdd','outn ota_vdd')
    content = content.replace(old, 'VOTA vdd ota_vdd 0\n'+new)
    # Representative load for a high-impedance board buffer. Both axes are symmetric.
    caps = {'board': (2,7), 'heavy': (4,22), 'bare': (0,0)}
    input_pf, output_pf = caps[case.load]
    for branch in 'pn':
        content += (f'\nCTXPAD{branch} tx{branch} 0 {input_pf + 0.01}p'
                    f'\nCRXPAD{branch} rx{branch} 0 {input_pf + 0.01}p'
                    f'\nRPKG{branch} hold{branch} pin{branch} 5'
                    f'\nCBOARD{branch} pin{branch} 0 {output_pf + 0.01}p'
                    f'\nRBUFFER{branch} pin{branch} 0 100Meg\n')
    options = {'trap': 'klu method=trap reltol=4e-4 trtol=10', 'gear': 'method=gear',
               'klugear': 'klu method=gear gmin=1e-11 itl1=400'}
    end = (case.cycles-1)*100+95
    return (content + '\n.save ' + ' '.join(VECTORS) + f'\n.options {options[case.solver]}'
            f'\n.tran {case.step}n {end}u 0 {case.step}n\n.end\n')


def read_raw(path, case):
    header, raw = path.read_bytes().split(b'Binary:\n',1)
    names = [m.decode().lower() for m in
             re.findall(rb'(?m)^\s*\d+\s+(\S+)\s+\S+[^\n]*$',header)]
    count = int(re.search(rb'No\. Points:\s*(\d+)',header)[1])
    a = np.frombuffer(raw,dtype='<f8').reshape(count,len(names))
    if a[-1,0] < ((case.cycles-1)*100 + 94.999)*1e-6 or not np.isfinite(a).all():
        raise ValueError('Incomplete or nonfinite waveform')
    return dict(zip(names,a.T))


def crossing(t, y, threshold, rising, start, stop):
    z = y-threshold
    crossed = ((z[:-1]<0)&(z[1:]>=0)) if rising else ((z[:-1]>=0)&(z[1:]<0))
    where = np.flatnonzero(crossed & (t[:-1]>=start) & (t[1:]<=stop))
    if len(where) != 1:
        raise ValueError(f'Expected one crossing {start} to {stop}, found {len(where)}')
    i = where[0]
    return float(t[i] - z[i] * (t[i+1]-t[i]) / (z[i+1]-z[i]))


def measure(path, case):
    d = read_raw(path,case)
    voltage = lambda node: d[f'v({node})']
    t = 1e6*d['time']-(case.cycles-1)*100
    vdd = BASELINES[case.corner][1]
    start = crossing(t,voltage('phi2'),vdd/2,True,40,65)
    track = crossing(t,voltage('tr'),vdd/2,True,60,77)
    stop = crossing(t,voltage('tr'),vdd/2,False,75,87)
    late = (t>=87)&(t<=89)
    if np.min(voltage('phi2')[late]) < vdd/2 or np.min(voltage('phit')[late]) < vdd/2:
        raise ValueError('Late live reference is outside transfer window')
    transfer = (t>=start)&(t<=stop)
    live = 1e3*(voltage('outp')-voltage('outn'))
    held = 1e3*(voltage('pinp')-voltage('pinn'))
    input_cm = (voltage('sump')+voltage('sumn'))/2
    held_cm = (voltage('pinp')+voltage('pinn'))/2
    target = float(np.median(live[late]))
    # Keep the live-settling metric separate from actual held error and droop.
    band = max(abs(target)*.001, .1)
    early = (t>=start)&(t<=stop-.15)
    misses = np.flatnonzero(early & (abs(live-target)>band))
    stable = t[misses[-1]+1] if len(misses) else start
    slack = stop-stable if stable<=stop-.15 else float('nan')
    sample = max(81,stop+.2)
    at = lambda y, us: float(np.interp(us,t,y))
    avg = lambda vector: vdd*np.trapz(d[vector][(t>=0)&(t<=95)],t[(t>=0)&(t<=95)])/95
    return dict(track_start_us=track,track_stop_us=stop,sample_us=sample,
                held_diff_mV=at(held,sample), held_cm_V=at(held_cm,sample),
                pin_p_V=at(voltage('pinp'),sample),pin_n_V=at(voltage('pinn'),sample),
                min_in_cm_V=float(np.min(input_cm[transfer])),
                min_pin_V=float(min(np.min(voltage('pinp')[t>=0]),np.min(voltage('pinn')[t>=0]))),
                max_pin_V=float(max(np.max(voltage('pinp')[t>=0]),np.max(voltage('pinn')[t>=0]))),
                sampled_input_cm_V=at(input_cm,sample),
                late_live_diff_mV=target,settle_band_mV=band,settling_slack_us=slack,
                held_minus_late_live_mV=at(held,sample)-target,
                hold_droop_7us_mV=at(held,sample+7)-at(held,sample),
                ota_uW=1e6*avg('i(vota)'),readout_mW=-1000*avg('i(vdd)'),
                bias_uA=1e6*at(d['i(viref)'],sample),
                clock_mW=1000*avg('i(vclkdd)'),refbuf_mW=1000*avg('i(vbufdd)'))


def run(case):
    work = ROOT/'benches'/case.name
    work.mkdir(parents=True,exist_ok=True)
    row = dict(ota=case.ota,corner=case.corner,pressure_kPa=case.pressure,
               cp_pF=capacitance(case.pressure)+case.offset,cn_pF=10,
               extra_sensor_pF=case.offset,load=case.load,step_ns=case.step,
               cycles=case.cycles,solver=case.solver,booster_ref_V=case.bias_v,
               case=case.name)
    (work/'bench.cir').write_text(deck(case))
    (work/'.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
    try:
        subprocess.run(['ngspice','-b','-r','trace.raw','-o','run.log','bench.cir'],
                       cwd=work,check=True,timeout=105,stdout=subprocess.DEVNULL)
        log = (work/'run.log').read_text()
        if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
            raise ValueError('Ngspice aborted. See run.log.')
        row.update(measure(work/'trace.raw',case),status='ok')
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        row['status'] = str(exc)
    print(case.name,row['status'],flush=True)
    return row


def save(path, rows):
    keys = list(dict.fromkeys(key for row in rows for key in row))
    with path.open('w',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('group',choices=('smoke','nominal','pvt','stress','fine'))
    p.add_argument('--jobs',type=int,default=5)
    p.add_argument('--only',choices=OTAS)
    args = p.parse_args()
    subckt_files()
    if args.group == 'smoke':
        cases = [Case(a,'typ',100) for a in OTAS]
    elif args.group == 'nominal':
        cases = [Case(a,'typ',p) for a,p in product(OTAS,PRESSURES)]
    elif args.group == 'pvt':
        cases = [Case(a,c,p, solver='gear' if c=='hot' else 'trap')
                 for a,c,p in product(OTAS,('cold','hot'),(30,60,90,100,120))]
    elif args.group == 'stress':
        cases = [Case(a,'typ',p,l,o) for a,p,l,o in product(
            OTAS,(30,100,120),('heavy',),(0,-.5,2.71))]
        cases += [Case(a,c,p,bias_v=b,solver='gear' if c=='hot' else 'trap')
                  for a,c,p,b in product(('boosted','boosted_C'),('typ','hot'),(100,120),(1.65,1.75))]
    else:
        cases = [Case(a,'typ',100,step=20,cycles=2) for a in OTAS]
        cases += [Case(a,'typ',100,load='bare') for a in OTAS]
    if args.only:
        cases = [c for c in cases if c.ota == args.only]
    with ThreadPoolExecutor(args.jobs) as pool:
        rows = list(pool.map(run,cases))
    suffix = f'_{args.only}' if args.only else ''
    save(ROOT/f'{args.group}{suffix}.csv',rows)
    if any(r['status']!='ok' for r in rows):
        raise SystemExit(1)


if __name__ == '__main__':
    main()

