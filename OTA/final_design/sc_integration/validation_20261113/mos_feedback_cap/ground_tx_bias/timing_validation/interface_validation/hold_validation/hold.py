"""Evaluate the held sample after the SCL08 acquisition gates turn off."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from native_load import native_body
from stress import Trial, run_spice, write_csv

START = 80
CORNERS = (("tntp49_5v",5,27),("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0),
           ("wnwp49_5v",4.5,85),("bnbp49_5v",5.5,0))


@dataclass(frozen=True)
class Case:
    cp: float = 12
    cn: float = 7
    cap: float = 10
    fall: float = .5
    skew: float = 0
    corner: int = 0
    step: int = 20


def build(c, perturb=None):
    model, supply, temp = CORNERS[c.corner]
    trial = Trial("hold", c.cp, c.cn, acquisition_pf=c.cap, model=model, supply=supply, temp=temp)
    body = native_body(trial)
    if c.cap:
        # 70–70.5 us tracking edge. The nominal 50% turn-off point is 80 us.
        fall_start = START - c.fall/2
        clock = f"VTR tr 0 PULSE(0 {supply} 70u .5u {c.fall}u {fall_start-70.5:g}u 100u)"
        lines = [clock if line.startswith("VTR ") else line for line in body.splitlines()]
        body = "\n".join(lines) + "\n"
        if c.skew:
            # Offset the negative branch turn-off only. Positive skew means later.
            body += f"VTRN trn 0 PULSE(0 {supply} 70u .5u {c.fall}u {fall_start-70.5+c.skew:g}u 100u)\n"
            body += f"BTRN trnb 0 V={supply}-v(trn)\n"
            body = body.replace("MN_tr_n outn tr ", "MN_tr_n outn trn ")
            body = body.replace("MP_tr_n outn trb ", "MP_tr_n outn trnb ")
    if perturb:
        branch, sign = perturb
        cap = c.cp if branch == "p" else c.cn
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*cap*1e-7} 142.7u 1n 1n 9n 1m)\n"
    return body


def run(folder, c, perturb=None):
    nodes = "v(outp) v(outn)"
    if c.cap:
        nodes += " v(holdp) v(holdn) v(tr)"
    commands = f"set klu\ntran {c.step}n 200u 0 {c.step}n\nwrdata wave.dat {nodes}"
    wave = run_spice(folder,"hold",build(c,perturb),commands,"wave.dat")
    if wave[-1,0] < 199.99e-6:
        raise RuntimeError(f"Incomplete case {folder}: {wave[-1,0]:g} s")
    t = wave[:,0]*1e6-100
    p,n = wave[:,1:3].T
    sample = lambda y, when:float(np.interp(when,t,y))
    if not c.cap:
        return dict(**asdict(c),sc_uv=1e6*sample(p-n,80), sc_cm_v=sample((p+n)/2,80),
                    track_uv="", held_uv="", hold_cm_v="", edge_shift_uv="", drift_uv="")
    hp,hn,clock = wave[:,3:6].T
    h, cm = hp-hn,(hp+hn)/2
    if perturb:
        return sample(h,81)
    keep = (t>=69)&(t<=89)
    if c in (Case(),Case(cap=5),Case(cap=20),Case(fall=.05)):
        key = f"{c.cap:g}pf_{c.fall:g}us"
        np.savetxt(OUT/f"wave_{key}.csv",np.column_stack((t[keep],p[keep],n[keep],hp[keep],hn[keep],clock[keep])),
                   delimiter=",",header="time_us,outp,outn,holdp,holdn,tr_v",comments="")
    before=START - c.fall/2 + min(0,c.skew) - .02
    return dict(**asdict(c),sc_uv=1e6*sample(p-n,80),sc_cm_v=sample((p+n)/2,80),
                track_uv=1e6*sample(h,before),held_uv=1e6*sample(h,81),hold_cm_v=sample(cm,81),
                edge_shift_uv=1e6*(sample(h,81)-sample(h,before)),
                drift_uv=1e6*(sample(h,88)-sample(h,81)))


def main():
    pairs=((12,7),(7,12),(12,12))
    references=[Case(cp,cn,cap=0,corner=k) for k in range(5) for cp,cn in pairs]
    tests=[Case(cp,cn,cap=cap) for cp,cn in pairs for cap in (5,10,20)]
    tests += [Case(cp,cn,fall=fall) for cp,cn in pairs for fall in (.05,.2,1.0)]
    tests += [Case(skew=skew) for skew in (-.1,.1)]
    tests += [Case(cp,cn,corner=k) for k in range(1,5) for cp,cn in pairs]
    tests += [Case(step=5),Case(fall=.05,step=5)]
    slopes=[Case(cp=cp,cap=cap) for cp in (11.95,12.05) for cap in (5,10,20)]
    with TemporaryDirectory(prefix="sc-hold-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        work=Path(tmp)
        cases=references+tests+slopes
        jobs=[pool.submit(run,work/str(i),c) for i,c in enumerate(cases)]
        noise={(cap,b,s):pool.submit(run,work/f"noise_{cap}_{b}_{s}",Case(cap=cap),(b,s))
               for cap in (5,10,20) for b in "pn" for s in (-1,1)}
        rows=[j.result() for j in jobs]
        ref={(r["cp"],r["cn"],r["corner"]):r for r in rows if not r["cap"]}
        for r in rows:
            baseline=ref.get((r["cp"],r["cn"],r["corner"]))
            r["held_error_uv"]=r["held_uv"]-baseline["sc_uv"] if r["cap"] and baseline else ""
            r["held_cm_shift_mv"]=1000*(r["hold_cm_v"]-baseline["sc_cm_v"]) if r["cap"] and baseline else ""
        write_csv(OUT/"hold_cases.csv",rows)
        noise_rows=[]
        for cap in (5,10,20):
            kt=1.380649e-23*300.15
            sensor=np.sqrt(sum(kt/(c*1e-12)*((noise[cap,b,1].result()-noise[cap,b,-1].result())/.002)**2
                               for b,c in (("p",12),("n",7))))
            floor=np.sqrt(2*kt/(cap*1e-12))
            lower,upper=(next(r for r in rows if r["cp"]==cp and r["cap"]==cap)
                         for cp in (11.95,12.05))
            slope=(upper["held_uv"]-lower["held_uv"])/.1
            noise_rows.append(dict(cap_pf=cap,sensor_uv=sensor*1e6,acquisition_ktc_uv=floor*1e6,
                                   quadrature_uv=np.hypot(sensor,floor)*1e6,
                                   sensitivity_mv_pf=slope/1000,
                                   equivalent_af=np.hypot(sensor,floor)*1e12/abs(slope)))
        write_csv(OUT/"noise_budget.csv",noise_rows)
    (OUT/"hold_10pf.cir").write_text(build(Case())+"\n.tran 20n 200u 0 20n\n"
        ".meas tran held_diff find par('v(holdp)-v(holdn)') at=181u\n.end\n")


if __name__ == "__main__":
    main()
