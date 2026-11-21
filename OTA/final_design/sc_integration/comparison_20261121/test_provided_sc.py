"""Simulate the supplied SCB10H drawing and explicitly tagged wiring interpretations."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from itertools import product
import re
import subprocess

import numpy as np

from compare import Case, ROOT, deck, read_raw, save

VECTORS = (
    'v(outp) v(outn) v(sump) v(sumn) v(txp) v(txn) v(rxp) v(rxn) '
    'v(sensp) v(sensn) v(sensorcom) v(phi1) v(phi2) v(phit)'
)
WIRINGS = {
    'as_drawn': (True, 'drawn', 'floating'),
    'outputs_separate': (False, 'drawn', 'floating'),
    'negative_feedback': (False, 'negative', 'floating'),
    'sensor_common_grounded': (False, 'negative', 'grounded'),
}
ERRORS = r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small'


@dataclass(frozen=True)
class Trial:
    wiring: str
    cp: float
    cn: float = 10
    cs: float = 10
    vp: float = 5
    cycles: int = 4
    step: int = 80
    solver: str = 'trap'

    @property
    def name(self):
        return (f'drawing_{self.wiring}_cp{self.cp:g}_cn{self.cn:g}_'
                f'cs{self.cs:g}_vp{self.vp:g}_{self.cycles}cy_{self.step}ns_{self.solver}')


def build(trial, case):
    short, polarity, common = WIRINGS[trial.wiring]
    original = deck(case).split('.save ',1)[0]
    original = re.sub(r'(?m)^\.param .*$',(
        f'.param CP={trial.cp:g}p CN={trial.cn:g}p CS={trial.cs:g}p'),original)
    drop = (r'(?m)^(CSMP[pn]|M[NP]_(tr|pr)_[pn]|RPKG[pn]|CBOARD[pn]|RBUFFER[pn]|'
            r'CTXPAD[pn]|CRXPAD[pn]|XREF|VBUFDD|VDRIVE|MREFBYPASS)\s.*\n')
    original = re.sub(drop,'',original)
    original = re.sub(r'(?m)^CS([pn]) (tx[pn]) (rx[pn]) \{C[PN]\}$',
                      lambda m: (f'CS{m[1]} {m[2]} {m[3]} {{CS}}\n'
                                 f'CMEM{m[1]} sens{m[1]} sensorcom {{C{m[1].upper()}}}'),
                      original)
    for pattern, substitution in (
        (r'(?m)^(MN_drive_[pn]) vdd chg ',r'\1 vp phi1 '),
        (r'(?m)^(MP_drive_[pn]) vdd chgb ',r'\1 vp phi1b '),
        (r'(?m)^(M[NP]_discharge_([pn])) 0 ',r'\1 sens\2 '),
        (r'(?m)^(M[NP]_clamp_[pn]) vref_sw ',r'\1 0 '),
    ):
        original,count = re.subn(pattern,substitution,original)
        if count not in (2,4):
            raise ValueError(f'Fixture rewiring failed ({count}) for {pattern}')
    if polarity == 'drawn':
        original,count = re.subn(r'(?m)^XOTA sumn sump ', 'XOTA sump sumn ',original)
        if count!=1:
            raise ValueError('Expected one OTA instance')
    extra = f'VEXC vp 0 {trial.vp:g}\nRLEAKP sensp 0 1e12\nRLEAKN sensn 0 1e12\n'
    extra += ('RLEAKCOM sensorcom 0 1e12\n' if common=='floating' else 'VSCOM sensorcom 0 0\n')
    if short:
        extra += 'VSHORT outp outn 0\n'
    opts = ('klu method=trap reltol=4e-4 trtol=10' if trial.solver=='trap'
            else 'method=gear reltol=4e-4')
    stop = (trial.cycles-1)*100+95
    return (original+extra+f'.save {VECTORS}\n.options {opts}\n'
            f'.tran {trial.step}n {stop}u 0 {trial.step}n\n.end\n')


def run(trial):
    case = Case('telescopic_C','typ',100,step=trial.step,cycles=trial.cycles,
                solver=trial.solver)
    wrk = ROOT/'benches'/trial.name
    wrk.mkdir(exist_ok=True)
    (wrk/'bench.cir').write_text(build(trial,case))
    (wrk/'.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
    row=dict(wiring=trial.wiring,cp_pF=trial.cp,cn_pF=trial.cn,cs_each_pF=trial.cs,
             vp_V=trial.vp,cycles=trial.cycles,maxstep_ns=trial.step,solver=trial.solver,
             name=trial.name)
    try:
        subprocess.run(['ngspice','-b','-r','trace.raw','-o','run.log','bench.cir'],
                       cwd=wrk,check=True,timeout=120,stdout=subprocess.DEVNULL)
        if re.search(ERRORS,(wrk/'run.log').read_text()):
            raise ValueError('ngspice did not complete the transient')
        raw=read_raw(wrk/'trace.raw',case)
        t=raw['time']*1e6-100*(trial.cycles-1)
        at=lambda y,time: float(np.interp(time,t,y))
        op,on=raw['v(outp)'],raw['v(outn)']
        isum=(raw['v(sump)']+raw['v(sumn)'])/2
        diff=1e3*(op-on)
        track=(t>=40)&(t<=80)
        row.update(diff_80_mV=at(diff,80),diff_first_80_mV=at(diff,80-100*(trial.cycles-1)),
                   differential_change_78_to_86_mV=at(diff,86)-at(diff,78),
                   output_p_V=at(op,80),output_n_V=at(on,80),
                   output_cm_V=at((op+on)/2,80),input_cm_V=at(isum,80),
                   input_cm_min_V=float(np.min(isum[track])),
                   sensor_common_V=at(raw['v(sensorcom)'],80),
                   phi2_at_sample_V=at(raw['v(phi2)'],80),xfer_at_sample_V=at(raw['v(phit)'],80),
                   status='ok')
    except (OSError,KeyError,ValueError,subprocess.SubprocessError) as exc:
        row['status']=str(exc)
    print(trial.name,row['status'],flush=True)
    return row


def main():
    p=argparse.ArgumentParser()
    p.add_argument('group',choices=('smoke','sweep','diagnostics'))
    p.add_argument('--jobs',type=int,default=5)
    args=p.parse_args()
    if args.group=='smoke':
        tests=[Trial(w,10.5) for w in WIRINGS]
    elif args.group=='sweep':
        tests=[Trial(w,p) for w,p in product(WIRINGS,(7.82,9,10,10.5,11.79))]
    else:
        tests=[Trial(w,p,cs=cs) for w,p,cs in product(
            ('negative_feedback','sensor_common_grounded'),(8,12),(5,20))]
        tests += [Trial(w,p,cn=n) for w,(p,n) in product(
            ('negative_feedback','sensor_common_grounded'),((8,8),(12,12),(8,12),(12,8)))]
        tests += [Trial('negative_feedback',p,cycles=8,step=40,solver='gear') for p in (8,12)]
    with ThreadPoolExecutor(args.jobs) as pool:
        rows=list(pool.map(run,tests))
    save(ROOT/f'provided_sc_{args.group}.csv',rows)
    if any(r['status']!='ok' for r in rows):
        raise SystemExit(1)


if __name__=='__main__':
    main()

