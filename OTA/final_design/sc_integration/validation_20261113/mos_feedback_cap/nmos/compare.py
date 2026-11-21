"""Compare isolated-body and grounded-body NMOS feedback banks."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import runpy
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
base = runpy.run_path(str(OUT.parent / "study.py"))
deck, run_spice, write_csv, MODELS = (base[k] for k in ("deck", "run_spice", "write_csv", "MODELS"))
CONFIGS = ("isolated_out", "isolated_sum", "grounded_out", "grounded_sum")


def device(name, gate, plate, bulk, count):
    return (f"M{name} {plate} {gate} {plate} {bulk} N W=20u L=10u M={count} "
            "AD=90p AS=90p PD=49u PS=49u")


def cv(work, isolated):
    bulk = "plate" if isolated else "0"
    body = f'NMOS capacitance\n.include "{MODELS}"\n'
    body += "VPL plate 0 2.5 AC 1\nVG gate 0 2.5\n" + device("UNIT", "gate", "plate", bulk, 1)
    commands = ["set appendwrite"]
    for offset in np.linspace(-2, 2, 161):
        commands.extend([f"alter VG {2.5+offset:.10g}", "ac lin 1 10k 10k",
                         f"let vgp = {offset:.10g}", "let cmut = imag(i(vg))/(2*pi*10000)",
                         "wrdata cv.dat vgp cmut", "unset wr_vecnames"])
    data = run_spice(work, "cv", body, "\n".join(commands), "cv.dat")[:,1:3]
    assert len(data) == 161
    return data


def circuit(kind, cp, cn, count, corner="tntp49_5v", supply=5, temp=27):
    body = deck(cp, cn, "tx_only", corner, supply, temp, 0)
    if kind == "ideal":
        return body
    if kind == "pmos":
        body = "\n".join(line for line in body.splitlines() if not line.startswith(("CFp ", "CFn "))) + "\n"
        return body + "\n".join(base["mos"](f"CF{b}", f"out{b}", f"sum{b}", 97) for b in "pn") + "\n"
    body = "\n".join(line for line in body.splitlines() if not line.startswith(("CFp ", "CFn "))) + "\n"
    for b in "pn":
        gate, plate = (f"out{b}", f"sum{b}") if kind.endswith("_out") else (f"sum{b}", f"out{b}")
        bulk = plate if kind.startswith("isolated") else "0"
        body += device(f"CF{b}", gate, plate, bulk, count) + "\n"
    return body


def simulate(work, kind, cp, cn, count, *, corner="tntp49_5v", supply=5, temp=27,
             perturb=None, step="30n", save=False):
    body = circuit(kind, cp, cn, count, corner, supply, temp)
    if perturb:
        branch, sign = perturb
        cap = cp if branch == "p" else cn
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*cap*1e-7} 143u 1n 1n 9n 1m)\n"
    command = f"set klu\ntran {step} 200u 0 {step}\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn)"
    wave = run_spice(work, "sc", body, command, "wave.dat")
    t, p, n, ip, inn = wave.T
    if t[-1] < 199.99e-6:
        raise ValueError(f"Incomplete transient in {work}")
    sample = lambda v, at=180: float(np.interp(at*1e-6,t,v))
    diff, ocm, icm = p-n,(p+n)/2,(ip+inn)/2
    if perturb:
        return np.array([sample(diff),sample(ocm),sample(icm)])
    mask = t >= 100e-6
    if save:
        np.savetxt(OUT/f"wave_{kind}_{cp}_{cn}.csv",wave[mask],delimiter=",",
                   header="time_s,outp,outn,sump,sumn",comments="")
    return dict(kind=kind,units=count,cp_pf=cp,cn_pf=cn,corner=corner,supply=supply,
                temp_c=temp,maxstep=step,diff_v=sample(diff),in_cm_v=sample(icm),
                out_cm_v=sample(ocm),in_cm_min_v=min(icm[mask]),out_cm_min_v=min(ocm[mask]),
                late_delta_v=sample(diff,188)-sample(diff),
                min_out_minus_sum_v=min(min((p-ip)[mask]),min((n-inn)[mask])),
                max_out_minus_sum_v=max(max((p-ip)[mask]),max((n-inn)[mask])))


def main():
    with tempfile.TemporaryDirectory(prefix="sc-nmos-") as temp, ThreadPoolExecutor(max_workers=6) as pool:
        work = Path(temp)
        isolated, grounded = list(pool.map(lambda iso: cv(work/f"cv_{iso}",iso),(True,False)))
        write_csv(OUT/"cv.csv", [dict(gate_minus_plate_v=v, isolated_f=i, grounded_mutual_f=g)
                                for (v,i),(_,g) in zip(isolated,grounded)])
        sizes = {"ideal":0,"pmos":97}
        for kind in CONFIGS:
            curve = isolated if kind.startswith("isolated") else grounded
            x = np.linspace(0, .96 if kind.endswith("_out") else -.96, 101)
            secant = np.mean(np.interp(x,curve[:,0],curve[:,1]))
            sizes[kind] = round(40e-12/secant)
        write_csv(OUT/"sizing.csv",[dict(kind=k,units=m) for k,m in sizes.items()])
        print(sizes,flush=True)
        pairs = ((12,7),(12,12),(7,7),(7,12),(11.95,7),(12.05,7))
        jobs = {(k,cp,cn):pool.submit(simulate,work/f"{k}_{cp}_{cn}",k,cp,cn,m,
                                      save=(cp,cn) in pairs[:2])
                for k,m in sizes.items() for cp,cn in pairs}
        rows = {key:future.result() for key,future in jobs.items()}
        write_csv(OUT/"nominal.csv",list(rows.values()))
        slopes = {k:(rows[k,12.05,7]["diff_v"]-rows[k,11.95,7]["diff_v"])/.1 for k in sizes}
        kinds = ("isolated_sum","grounded_sum","isolated_out","grounded_out")
        noise = {(k,b,s):pool.submit(simulate,work/f"noise_{k}_{b}_{s}",k,12,7,sizes[k],perturb=(b,s))
                 for k in kinds for b in "pn" for s in (-1,1)}
        corners = [(k,model,supply,temp) for k in ("ideal","pmos","isolated_sum","grounded_sum")
                   for model,supply,temp in (("wnwp49_5v",4.5,85),("bnbp49_5v",5.5,0),
                                             ("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0))]
        corner_runs = [pool.submit(simulate,work/f"corner_{i}",k,12,7,sizes[k],corner=model,supply=supply,temp=temp)
                       for i,(k,model,supply,temp) in enumerate(corners)]
        summary = []
        for k in sizes:
            rms = float("nan")
            if k in kinds:
                variance = sum(1.380649e-23*300.15/(cap*1e-12) *
                               ((noise[k,b,1].result()[0]-noise[k,b,-1].result()[0])/.002)**2
                               for b,cap in (("p",12),("n",7)))
                rms = np.sqrt(variance)
            summary.append(dict(kind=k,units=sizes[k],diff_mv=rows[k,12,7]["diff_v"]*1e3,
                                slope_mv_per_pf=slopes[k]*1e3,sensor_rms_uv=rms*1e6,
                                sensor_equiv_af=rms/abs(slopes[k])*1e6,
                                sample_ocm_v=rows[k,12,7]["out_cm_v"],
                                min_icm_12_12_v=rows[k,12,12]["in_cm_min_v"],
                                min_ocm_12_12_v=rows[k,12,12]["out_cm_min_v"]))
        write_csv(OUT/"summary.csv",summary)
        write_csv(OUT/"corners.csv",[f.result() for f in corner_runs])
        for kind in CONFIGS:
            body = circuit(kind,12,7,sizes[kind])
            (OUT/f"{kind}_12_7.cir").write_text(body+"\n.tran 30n 200u 0 30n\n"
                 ".print tran v(outp) v(outn) v(sump) v(sumn)\n.end\n")


if __name__ == "__main__":
    main()
