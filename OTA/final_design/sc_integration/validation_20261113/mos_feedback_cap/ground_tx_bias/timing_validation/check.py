"""Screen TX switch turn-on and RX lead, then check corners and loads."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from sweep import build, PROBES, run_spice, write_csv


@dataclass(frozen=True)
class Case:
    edge_us: float
    lead_us: float
    cp_pf: float
    cn_pf: float
    model: str = "tntp49_5v"
    supply: float = 5
    temp: float = 27
    load_pf: float = 5
    tx_v: float = 0
    step_ns: int = 30
    ideal_cf: bool = False


def timing_body(case):
    c = case
    body = build(4.5,c.cp_pf,c.cn_pf,c.model,c.supply,c.temp).replace("M=97 AD=","M=121 AD=")
    lines = []
    for line in body.splitlines():
        if c.ideal_cf and line.startswith(("MCFp ", "MCFn ")):
            branch = line[3]
            line = f"CF{branch} sum{branch} out{branch} {121*.4125499322514286:.12g}p"
        if line.startswith("VPHI2 "):
            line = f"VPHI2 phi2 0 PULSE(0 {c.supply} 46u {c.edge_us}u 1u {44-c.edge_us}u 100u)"
        if line.startswith("VPHIT "):
            line = f"VPHIT phit 0 PULSE(0 {c.supply} {46-c.lead_us}u 1u 1u {43+c.lead_us}u 100u)"
        if line.startswith(("CLP ","CLN ")):
            line = " ".join(line.split()[:3]) + f" {c.load_pf}p"
        if c.tx_v and line.startswith(("MN_discharge_", "MP_discharge_")):
            fields = line.split()
            fields[1] = "txref"
            line = " ".join(fields)
        lines.append(line)
    if c.tx_v:
        lines.append(f"VTXREF txref 0 {c.tx_v}")
    return "\n".join(lines) + "\n"


def simulate(folder, case):
    c = case
    probes = " ".join(PROBES)
    commands = (f"set klu\nsave all {probes}\ntran {c.step_ns}n 200u 0 {c.step_ns}n\n"
                f"wrdata wave.dat v(outp) v(outn) v(sump) v(sumn) v(rxp) v(rxn) v(txp) i(vdd) {probes}")
    wave = run_spice(folder,"timing",timing_body(c),commands,"wave.dat")
    if wave[-1,0] < 199.99e-6 or wave.shape[1] != 13:
        raise RuntimeError(f"Incomplete or malformed waveforms in {folder}")
    t,p,n,ip,inn,rp,rn,tx,idd,*junction = wave.T
    t = t*1e6-100
    cycle = (t>=0)&(t<=100)
    transfer = (t>=42)&(t<=89)
    diff,icm,ocm = p-n,(ip+inn)/2,(p+n)/2
    sample = lambda values, when=80: float(np.interp(when,t,values))
    d,late = sample(diff),sample(diff,88)
    ideal = 2*(c.supply+2.5-c.tx_v)*(c.cp_pf-c.cn_pf)/(2*121*.4125499322514286+c.cp_pf+c.cn_pf)
    band = max(abs(late)*.001,100e-6)
    outside=np.flatnonzero((t>=46)&(t<=88)&(abs(diff-late)>band))
    settle=t[outside[-1]+1]-46 if len(outside) else 0
    return dict(**vars(c), diff_mv=1000*d, ideal_diff_mv=1000*ideal, error_mv=1000*(d-ideal),
                late_drift_uv=1e6*(late-d), settle_us=settle, sampled_ocm_v=sample(ocm),
                min_ocm_v=min(ocm[cycle]), min_icm_v=min(icm[cycle]), min_rx_v=min(rp[cycle].min(),rn[cycle].min()),
                diode_abs_fc=1e9*np.trapz(np.abs(junction)[:,transfer].sum(axis=0),t[transfer]),
                mean_supply_power_uw=-1e4*c.supply*np.trapz(idd[cycle],t[cycle]))


def evaluate(pool,work,name,cases):
    jobs=[pool.submit(simulate,work/f"{name}_{i}",case) for i,case in enumerate(cases)]
    rows=[job.result() for job in jobs]
    write_csv(OUT/f"{name}.csv",rows)
    return rows


def main():
    pairs=((12,7),(12,12))
    with TemporaryDirectory(prefix="sc-timing-") as temp, ThreadPoolExecutor(max_workers=6) as pool:
        work=Path(temp)
        screen=evaluate(pool,work,"timing",[
            Case(edge,lead,*pair) for edge,lead,pair in product((1,2,4,8),(1,2,3),pairs)])
        # Select the lowest combined RX dip, then favor the shorter timing.
        grouped={(edge,lead):[r for r in screen if (r["edge_us"],r["lead_us"])==(edge,lead)]
                 for edge,lead in product((1,2,4,8),(1,2,3))}
        edge,lead=max(grouped,key=lambda key:(min(r["min_rx_v"] for r in grouped[key]),-sum(key)))
        print("Selected",edge,lead,flush=True)
        variants=((1,1,0),(edge,lead,0),(1,1,2))
        models=(("wnwp49_5v",4.5,85),("bnbp49_5v",5.5,0),
                ("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0))
        evaluate(pool,work,"corners",[
            Case(e,l,*pair,model=m,supply=v,temp=t,tx_v=x)
            for (e,l,x),pair,(m,v,t) in product(variants,pairs,models)])
        evaluate(pool,work,"loads",[
            Case(e,l,*pair,load_pf=load,tx_v=x)
            for (e,l,x),pair,load in product(variants,pairs,(2,5,10,20))])
        evaluate(pool,work,"shorter_candidates",[
            Case(e,1,*pair,model=m,supply=v,temp=t)
            for e,pair,(m,v,t) in product((4,8),pairs,models)])
        evaluate(pool,work,"capacitor_control",[
            Case(8,3,12,7,model=m,supply=v,temp=t,ideal_cf=True)
            for m,v,t in models])
        evaluate(pool,work,"fine",[
            Case(e,l,*pair,tx_v=x,step_ns=10) for (e,l,x),pair in product(variants,pairs)])


if __name__=="__main__":
    main()
