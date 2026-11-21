"""Run the balanced 2.5 V TX/RX readout across selected SCL08 conditions."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, replace
from pathlib import Path
import argparse
import csv
import re
import subprocess
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
PDK = Path.home() / 'pdk/scl08/ngspice_models49'
DEVICES = ('m1007', 'm1059', 'm1015', 'm1033', 'm1041', 'm1042', 'm1039', 'm1008', 'm1045')
MODELS = ('tntp', 'bnbp', 'bnwp', 'wnbp', 'wnwp')
CONDITIONS = ((5, 27, 'typ'), (4.5, 0, 'best'), (4.5, 85, 'worst'),
              (5.5, 0, 'best'), (5.5, 85, 'worst'))
PAIRS = ((12, 7), (12, 12))
BASE = (HERE / 'base.cir').read_text()


@dataclass(frozen=True)
class Case:
    name: str
    mos: str = 'tntp'
    vdd: float = 5.0
    temp: int = 27
    rpp: str = 'typ'
    cp: int = 12
    cn: int = 7
    ohms: int = 0
    pf: int = 0
    split: bool = False
    dt_ns: int = 50
    cycles: int = 2
    vbp: float | None = None
    nodeset: bool = False
    startup_reset: bool = False
    skip_dc: bool = False
    tx_ramp_us: int = 8


def vector(device, parameter):
    return f'@m.xota.{device}[{parameter}]'


def deck(case):
    mos = PDK / 'mos' / f'{case.mos}49_5v'
    res = PDK / 'res' / case.rpp / 'ppr'
    body = BASE[:BASE.index('.control')]
    body = re.sub(r'(?m)^\.include .*scl08_models.inc.*$', f'.include "{mos}"\n.include "{res}"', body)
    body = body.replace('.param CP=12p CN=7p',f'.param CP={case.cp}p CN={case.cn}p')
    body = body.replace('.temp 27',f'.temp {case.temp}')
    body = body.replace('VDD vdd 0 5',f'VDD vdd 0 {case.vdd}')
    body = re.sub(r'(?m)^V(TXL|REF|PRE) .*\n','',body)
    body = body.replace(' txlo ', ' vref_sw ').replace(' pre pr', ' vref_sw pr')
    body = re.sub(r'(?m)^(M[NP]_clamp_[pn]) vref ',r'\1 vref_sw ',body)
    ref = 'VREFSRC ref_src 0 2.5\n'
    if case.ohms:
        ref += f'RREF ref_src vref_sw {case.ohms}\n'
    else:
        ref += 'VREFWIRE ref_src vref_sw 0\n'
    if case.pf:
        ref += f'CREF vref_sw 0 {case.pf}p\n'
    ref += 'VREFSENSE ref_src vref 0\n' if case.split else 'VREFSENSE vref_sw vref 0\n'
    body = body.replace('VCLK clk10k 0 PULSE(0 5 ',f'VCLK clk10k 0 PULSE(0 {case.vdd} ')
    high = case.vdd / 5
    body = body.replace('XPHASE clk10k phi1 phit phi2 pr tr phases_10k',f'''
ENORM clk_normal 0 clk10k 0 {1/high}
XPHASE clk_normal phi1_raw phit_raw phi2_raw pr_raw tr_raw phases_10k
ESC1 phi1 0 phi1_raw 0 {high}
ESCT phit 0 phit_raw 0 {high}
ESC2 phi2 0 phi2_raw 0 {high}
ESCP pr 0 pr_raw 0 {high}
ESCR tr 0 tr_raw 0 {high}
''')
    body = re.sub(r'(?m)^(B\w+ \w+b 0 V=)5-v\(',r'\1v(vdd)-v(',body)
    if case.tx_ramp_us != 8:
        taps = range(46,46 + case.tx_ramp_us)
        delayed = '\n'.join(f'Xtx_{k} clk tx_{k} delay_ideal td={k}u' for k in taps)
        body = re.sub(r'(?m)^Xtx_46 .*\n(?:^Xtx_\d+ .*\n)*', delayed + '\n', body)
        terms = [f'v(tx_{k})' for k in taps]
        groups = ['+'.join(terms[k:k+4]) for k in range(0,len(terms),4)]
        drive = 'Bphitx tx_slew 0 V=(' + '\n+ +'.join(groups) + f')/{case.tx_ramp_us}\n'
        body = re.sub(r'(?m)^Bphitx .*\n(?:^\+.*\n)*',drive,body)
    if case.vbp is not None:
        body = body.replace('VBP vbp vdd -2.2',f'VBP vbp 0 {case.vbp}')
    if case.nodeset:
        body += '\n.nodeset V(outp)=2.5 V(outn)=2.5 V(sump)=2.5 V(sumn)=2.5\n'
    if case.startup_reset:
        body = body.replace('ESC1 phi1 0', 'ESC1 phi1_run 0')
        body += (f'\nVSTART start_reset 0 PWL(0 {case.vdd} 1u {case.vdd} 2u 0)\n'
                 'BSTART phi1 0 V=max(v(phi1_run),v(start_reset))\n')
    nodes = 'v(outp) v(outn) v(sump) v(sumn) v(holdp) v(holdn) v(vref_sw) v(vref) i(VREFSRC) i(VDD)'
    mos_vectors = ' '.join(vector(device, param) for device in DEVICES for param in ('vds','vdsat'))
    # Save native BSIM3 operating-point vectors throughout the transient.
    dt = f'{case.dt_ns}n'
    startup = ' uic' if case.skip_dc else ''
    return f"""{body}
{ref}
.save {nodes} {mos_vectors}
.control
set wr_singlescale
set wr_vecnames
set numdgt=12
tran {dt} {100*case.cycles}u 0 {dt}{startup}
wrdata trace.dat {nodes} {mos_vectors}
quit
.endc
.end
"""


def evaluate(case, job):
    log = (job/'run.log').read_text()
    if re.search(r'(?im)^Error|aborted|timestep too small',log):
        raise RuntimeError('check ngspice log')
    trace = np.loadtxt(job/'trace.dat',skiprows=1)
    if trace[-1,0] < (case.cycles*100-.01)*1e-6 or trace.shape[1] != 11+2*len(DEVICES):
        raise RuntimeError('incomplete transition or missing BSIM3 data')
    t = trace[:,0]*1e6 - (case.cycles-1)*100
    op,on,sp,sn,hp,hn,ref,sense,ref_i,supply_i = trace[:,1:11].T
    cm,incm,vd = (op+on)/2,(sp+sn)/2,op-on
    transfer = (t>=40)&(t<=70)
    cycle = (t>=0)
    tail = (t>=75)&(t<=79)
    heldcm = np.interp(81,t,(hp+hn)/2)
    held = np.interp(81,t,hp-hn)
    margin = abs(trace[:,11::2])-abs(trace[:,12::2])
    def pair_margin(rows, indices):
        return float(np.min(margin[rows][:,indices])*1e3)
    i = np.flatnonzero(transfer)[int(np.argmin(cm[transfer]))]
    j = np.flatnonzero(transfer)[int(np.argmin(incm[transfer]))]
    m = np.flatnonzero(transfer)[int(np.argmin(margin[transfer,6]))]
    result = dict(
        outcm_min=float(cm[i]), outcm_max=float(np.max(cm[transfer])),
        outcm_min_us=float(t[i]), incm_min=float(incm[j]), incm_min_us=float(t[j]),
        incm_track=float(np.interp(79,t,incm)), held_cm=float(heldcm), held_mv=float(held*1e3),
        shift_mv=float((held-np.interp(79.5,t,vd))*1e3),
        ref_switch_max_error_mv=float(np.max(abs(ref[cycle]-2.5))*1e3),
        ref_cm_max_error_mv=float(np.max(abs(sense[cycle]-2.5))*1e3),
        ref_switch_sample_error_mv=float((np.interp(81,t,ref)-2.5)*1e3),
        peak_ref_source_ua=float(np.max(abs(ref_i[cycle]))*1e6),
        mean_supply_uw=float(-np.trapz(supply_i[cycle],t[cycle])*case.vdd/(t[cycle][-1]-t[cycle][0])*1e6),
        tail_min_margin_time_us=float(t[m]),
    )
    for group, indices in [('input',[0,1]), ('ncas',[2,3]), ('pcas',[4,5]), ('tail',[6]), ('pload',[7,8])]:
        result[f'{group}_transfer_margin_mv']=pair_margin(transfer,indices)
        result[f'{group}_track_margin_mv']=pair_margin(tail,indices)
    # Retain a compact trace for plotting relevant transients.
    np.savez_compressed(job/'wave.npz',t=t[cycle],cm=cm[cycle],incm=incm[cycle],
                        ref=ref[cycle],sense=sense[cycle],held=(hp-hn)[cycle],
                        min_margin=np.min(margin,axis=1)[cycle],tail_margin=margin[:,6][cycle])
    return result


def run(case, work):
    job = work/case.name
    job.mkdir(exist_ok=True)
    (job/'run.cir').write_text(deck(case))
    result = asdict(case)
    try:
        with (job/'console.log').open('w') as console:
            subprocess.run(['ngspice','-b','-o','run.log','run.cir'], cwd=job,
                           stdout=console, stderr=subprocess.STDOUT, timeout=180, check=True)
        result.update(evaluate(case,job),status='ok')
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        result['status'] = str(exc)
    print(case.name,result['status'],flush=True)
    return result


def write_csv(path, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def stress_cases(work):
    with (work/'pvt.csv').open() as f:
        pvt = [row for row in csv.DictReader(f) if row['status'] == 'ok']
    worst_headroom = min(pvt, key=lambda r: min(float(r[f'{group}_transfer_margin_mv'])
                         for group in ('input', 'ncas', 'pcas', 'tail', 'pload')))
    worst_drive = max(pvt, key=lambda r: float(r['peak_ref_source_ua']))
    worst_cm = max(pvt, key=lambda r: max(2.5 - float(r['outcm_min']),
                                         float(r['outcm_max']) - 2.5))
    selected = {row['name']: row for row in (worst_headroom, worst_drive, worst_cm)}
    cases = []
    for name, row in selected.items():
        case = Case(name, row['mos'], float(row['vdd']), int(row['temp']), row['rpp'],
                    int(row['cp']), int(row['cn']))
        for r, c, split in ((0, 0, False), (50, 0, False), (100, 100, False), (1000, 100, True)):
            cases.append(replace(case, name=f'stress_{name}_{r}_{c}_{split}',
                                 ohms=r, pf=c, split=split, dt_ns=20, cycles=3))
    return cases


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('group',choices=('smoke','pvt','reference','followup','hot-check','startup','tx-slew','combined'))
    parser.add_argument('--work',type=Path,default=None)
    parser.add_argument('--jobs',type=int,default=6)
    args=parser.parse_args()
    work=args.work or Path(tempfile.mkdtemp(prefix='vcm-pvt-'))
    work.mkdir(parents=True,exist_ok=True)
    if args.group=='smoke':
        cases=[Case('smoke'),Case('smoke_20ns',dt_ns=20,cycles=3)]
    elif args.group=='pvt':
        cases=[Case(f'{mos}_{vdd}_{temp}_{cp}_{cn}',mos,vdd,temp,rpp,cp,cn)
               for mos in MODELS for vdd,temp,rpp in CONDITIONS for cp,cn in PAIRS]
    elif args.group=='reference':
        cases=[Case(f'ref_{r}_{c}_{s}_{cp}_{cn}',cp=cp,cn=cn,ohms=r,pf=c,split=s)
               for r,c,s in ((10,0,False),(100,0,False),(1000,0,False),(10000,0,False),
                             (100,100,False),(1000,100,False),(1000,1000,False),
                             (1000,0,True),(1000,100,True),(10000,100,True))
               for cp,cn in PAIRS]
    elif args.group=='followup':
        cases=stress_cases(work)
    elif args.group=='hot-check':
        cases=[Case(f'hot_{mos}_{vbp}_{cn}',mos,5.5,85,'worst',12,cn,
                    vbp=vbp,nodeset=True)
               for mos in ('bnbp','wnbp','bnwp','wnwp')
               for vbp in ((None,3.0,2.8) if mos in ('bnbp','wnbp') else (3.0,2.8))
               for cn in (7,12)]
    elif args.group=='startup':
        cases=[Case(f'start_{mos}_{cn}',mos,5.5,85,'worst',12,cn,
                    startup_reset=True,dt_ns=20,cycles=3)
               for mos in ('bnbp','wnbp','bnwp') for cn in (7,12)]
    elif args.group=='tx-slew':
        cases=[Case(f'slew_{mos}_{vdd}_{temp}_{cn}_{ramp}',mos,vdd,temp,rpp,12,cn,
                    tx_ramp_us=ramp,startup_reset=True)
               for mos,vdd,temp,rpp in (('tntp',5,27,'typ'),('bnwp',5.5,85,'worst'))
               for cn in (7,12) for ramp in (12,20)]
    else:
        cases=[Case(f'combined_{mos}_{vdd}_{temp}_{cn}_{r}',mos,vdd,temp,rpp,12,cn,
                    ohms=r,tx_ramp_us=20,startup_reset=True)
               for mos,vdd,temp,rpp in (('tntp',5,27,'typ'),('bnwp',5.5,85,'worst'))
               for cn in (7,12) for r in (0,50)]
    with ThreadPoolExecutor(args.jobs) as pool:
        rows=list(pool.map(lambda case:run(case,work),cases))
    write_csv(work/f'{args.group}.csv',rows)
    if any(row['status']!='ok' for row in rows):
        raise SystemExit('One or more simulations did not complete. See logs and CSV.')


if __name__=='__main__':
    main()
