"""Sensitivity sweep for the corrected SC readout using the extracted OTA."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import csv
import re
import subprocess

import numpy as np

from verify import ROOT, read_raw

OUT = ROOT/'sensitivity_optimization'
BASE = (ROOT/'results/sc_ota_extracted.spice').read_text()
SUPPORT = (ROOT/'bench_support.spice').read_text()
CORNERS = {
    'typ': ('tntp','typ',5,27,3),
    'cold': ('wnwp','best',4.5,0,0),
    'hot': ('bnwp','worst',5.5,85,5),
}
PROBES = ['@m.xota.m1039[vds]','@m.xota.m1039[vdsat]']
CP_ENDS = (7.82,11.79)
BASELINE = (10,121)


@dataclass(frozen=True)
class Case:
    cs: float
    bank: int
    cp: float
    corner: str = 'typ'
    load: int = 5
    step: int = 80

    @property
    def name(self):
        return f'cs{self.cs:g}_m{self.bank}_cp{self.cp:g}_{self.corner}_load{self.load}_{self.step}ns'


def write_csv(name, data):
    keys=list(dict.fromkeys(key for row in data for key in row))
    with (OUT/name).open('w',newline='') as file:
        w=csv.DictWriter(file,fieldnames=keys)
        w.writeheader()
        w.writerows(data)


def make_files(c):
    work = OUT/c.name
    work.mkdir(exist_ok=True)
    net = BASE
    for pattern,new,count in (
        (r'(?im)^(CMEMP\s+\S+\s+\S+\s+)\S+',f'{c.cp:g}p',1),
        (r'(?im)^(CS[PN]\s+\S+\s+\S+\s+)\S+',f'{c.cs:g}p',2),
        (r'(?im)^(CL[PN]\s+\S+\s+\S+\s+)\S+',f'{c.load:g}p',2),
    ):
        net,n=re.subn(pattern,lambda m:m[1]+new,net)
        if n!=count:
            raise ValueError('Unexpected base SC topology')
    mos,res,supply,temp,trim = CORNERS[c.corner]
    model=SUPPORT.replace('tntp49_5v',mos+'49_5v').replace('/res/typ/',f'/res/{res}/')
    model=model.replace('.temp 27',f'.temp {temp}')
    model=model.replace('VDD vdd 0 5',f'VDD vdd 0 {supply:g}')
    model=model.replace('VCLK clk10k 0 PULSE(0 5 ',f'VCLK clk10k 0 PULSE(0 {supply:g} ')
    model=model.replace('VEXC vp 0 5',f'VEXC vp 0 {supply:g}')
    for i in range(3):
        model=re.sub(rf'(?m)^VTRIM{i} d{i} 0 \S+',f'VTRIM{i} d{i} 0 {supply if trim&(1<<i) else 0:g}',model)
    model=model.replace('M=121 AD=90p',f'M={c.bank} AD=90p')
    model=model.replace('.tran 80n 395u 0 80n',f'.tran {c.step}n 395u 0 {c.step}n')
    model=re.sub(r'(?m)^\.save .+',lambda m:m[0]+' '+' '.join(PROBES),model)
    if c.corner=='hot':
        model=model.replace('klu method=trap','klu method=gear')
    support=work/'bench_sensitivity.spice'
    support.write_text(model)
    net=net.replace('.include bench_support.spice',f'.include "{support}"')
    deck=work/'bench.cir'
    deck.write_text(net)
    return work,deck


def measure(c, raw):
    w=read_raw(raw)
    t=1e6*w['time']-300
    at=lambda y,us=80:float(np.interp(us,t,y))
    vin=(w['v(sump)']+w['v(sumn)'])/2
    op,on=w['v(outp)'],w['v(outn)']
    diff=1e3*(op-on)
    at4=np.array([at(diff,80-100*k) for k in range(4)])
    wc=(t>=40)&(t<=80)
    if min(at(w['v(phi2)'],86),at(w['v(phit)'],86))<CORNERS[c.corner][2]/2:
        raise ValueError('Late settling window outside charge transfer')
    steady=float(np.median(diff[(t>=84)&(t<=86)]))
    band=max(.1,.001*abs(steady))
    check=np.flatnonzero((t>=48)&(t<=80)&(np.abs(diff-steady)>band))
    stable=float(t[check[-1]+1]) if len(check) else 48
    if abs(at(diff)-steady)>band:
        slack=float('nan')
    else:
        slack=max(0,80-stable)
    def p(name):
        return w[name] if name in w else w[f'v({name})']
    m=1e3*(np.abs(p(PROBES[0]))-np.abs(p(PROBES[1])))
    if np.ptp(m[wc])<0.1:
        raise ValueError('Tail saturation probe was static')
    return dict(diff_sample_mV=at(diff),diff_late_mV=steady,
                settling_band_mV=band,settle_slack_us=slack,
                late_change_uV=1000*(at(diff,86)-at(diff)),
                repeat_change_uV=1000*np.ptp(at4), input_cm_min_V=np.min(vin[wc]),
                input_cm_sample_V=at(vin),output_cm_sample_V=at((op+on)/2),
                output_low_V=min(op[wc].min(),on[wc].min()),
                output_high_V=max(op[wc].max(),on[wc].max()),
                tail_min_switch_mV=m[wc].min(),tail_sample_mV=at(m),
                tail_below_sat_ns=1000*np.diff(t)[wc[:-1] & wc[1:] & (m[:-1]<0)&(m[1:]<0)].sum())


def run(c):
    row=dict(cs_pF=c.cs,cfb_pmos_units=c.bank,cp_pF=c.cp,cn_pF=10,
             corner=c.corner,load_pF=c.load,step_ns=c.step,case=c.name)
    work,deck=make_files(c)
    raw,log=work/'trace.raw',work/'run.log'
    try:
        p=subprocess.run(['ngspice','-b','-r',str(raw),'-o',str(log),str(deck)],cwd=ROOT,
                         capture_output=True,text=True,timeout=130)
        p.check_returncode()
        if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log.read_text()):
            raise ValueError('Transient error')
        row.update(measure(c,raw),status='ok')
    except (ValueError,KeyError,OSError,subprocess.SubprocessError) as e:
        row['status']=str(e)
    print(c.name,row['status'],flush=True)
    return row


def summarize(rows,name):
    groups = {}
    for r in rows:
        if r['status']!='ok':
            continue
        key=tuple(r[k] for k in ('cs_pF','cfb_pmos_units','corner','load_pF','step_ns'))
        groups.setdefault(key,{})[r['cp_pF']]=r
    out=[]
    for (cs,bank,corner,load,step),g in groups.items():
        if not all(p in g for p in CP_ENDS):
            continue
        a,b=(g[p]['diff_sample_mV'] for p in CP_ENDS)
        avg=(b-a)/(CP_ENDS[-1]-CP_ENDS[0])
        mid=g.get(10.5)
        near=((g[11.08761]['diff_sample_mV']-g[9.98234]['diff_sample_mV'])/1.10527
              if 11.08761 in g and 9.98234 in g else float('nan'))
        out.append(dict(cs_pF=cs,cfb_pmos_units=bank,corner=corner,load_pF=load,step_ns=step,
                        avg_sensitivity_mV_pF=avg,near100kPa_sensitivity_mV_pF=near,
                        vdiff_low_mV=a,vdiff_high_mV=b,
                        midpoint_residual_mV=(mid['diff_sample_mV']-(a+avg*(10.5-CP_ENDS[0]))) if mid else float('nan'),
                        settled_cases=sum(np.isfinite(r['settle_slack_us']) for r in g.values()),
                        total_cases=len(g), min_settle_slack_us=min(r['settle_slack_us'] for r in g.values()),
                        min_input_cm_V=min(r['input_cm_min_V'] for r in g.values()),
                        min_tail_sample_mV=min(r['tail_sample_mV'] for r in g.values()),
                        min_tail_switch_mV=min(r['tail_min_switch_mV'] for r in g.values()),
                        max_tail_below_sat_ns=max(r['tail_below_sat_ns'] for r in g.values()),
                        min_output_V=min(r['output_low_V'] for r in g.values()),
                        max_output_V=max(r['output_high_V'] for r in g.values()),
                        max_repeat_uV=max(r['repeat_change_uV'] for r in g.values())))
    if out:
        write_csv(name,out)
        for r in out:
            print(r['cs_pF'],r['cfb_pmos_units'],r['corner'],r['load_pF'],
                  'mV/pF',round(r['avg_sensitivity_mV_pF'],2),
                  'settled',r['settled_cases'],r['total_cases'],
                  'minTail',round(r['min_tail_switch_mV']),flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('group',choices=('nominal','refine'))
    p.add_argument('--design',action='append',default=[],metavar='CS,UNITS')
    p.add_argument('--jobs',type=int,default=6)
    arg=p.parse_args()
    OUT.mkdir(exist_ok=True)
    if arg.group=='nominal':
        cases=[Case(cs,m,cp) for cs,m,cp in product((10,20,40),(121,84,60,40),CP_ENDS)]
    else:
        specs=[(float(a),int(b)) for a,b in (x.split(',') for x in arg.design)]
        cases=[]
        for cs,m in specs:
            cases += [Case(cs,m,cp,step=60) for cp in (*CP_ENDS,10.5,9.98234,11.08761)]
            cases += [Case(cs,m,cp,c) for c,cp in product(('cold','hot'),CP_ENDS)]
            cases += [Case(cs,m,cp,load=15) for cp in CP_ENDS]
    with ThreadPoolExecutor(arg.jobs) as pool:
        rows=list(pool.map(run,cases))
    write_csv(f'{arg.group}_points.csv',rows)
    summarize(rows,f'{arg.group}_summary.csv')


if __name__=='__main__':
    main()

