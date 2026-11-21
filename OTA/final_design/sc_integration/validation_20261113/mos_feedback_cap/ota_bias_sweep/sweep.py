"""Sweep OTA biases with the 97-unit PMOS feedback bank."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import runpy
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
base = runpy.run_path(str(OUT.parent / "study.py"))
sc_body, run_spice, write_csv = (base[key] for key in ("sc_body", "run_spice", "write_csv"))
BASELINE = (3.5, 3.0, 2.8)
CASES = [BASELINE] + [(i, 3.0, 2.8) for i in (2.5, 4.5, 5.5, 7.0)]
CASES += [(3.5, v, 2.8) for v in (2.4, 2.7, 3.3)]
CASES += [(3.5, 3.0, v) for v in (2.6, 3.0)]
CASES += [(4.5, 2.7, 2.8), (5.5, 2.7, 2.8)]
CAPS = {"p":12,"n":7}


def run(folder, bias, cp, cn, perturb=None, step="30n"):
    current, vbn, vbp = bias
    body = sc_body("reversed", cp, cn, 97)
    body = body.replace("IREF vdd bias 3.5u", f"IREF vdd bias {current}u")
    body = body.replace("VBN vbn 0 3", f"VBN vbn 0 {vbn}")
    body = body.replace("VBP vbp vdd -2.2", f"VBP vbp vdd {vbp-5:.6g}")
    if perturb:
        branch, sign = perturb
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*CAPS[branch]*1e-7} 143u 1n 1n 9n 1m)\n"
    commands = f"set klu\ntran {step} 200u 0 {step}\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn) i(vdd)"
    t, op, on, ip, inn, idd = run_spice(folder,"bias",body,commands,"wave.dat").T
    if t[-1]<199.99e-6:
        raise RuntimeError(f"Incomplete transient {folder}")
    us = t*1e6-100
    diff,icm,ocm = op-on,(ip+inn)/2,(op+on)/2
    sample = lambda v, at=80: float(np.interp(at,us,v))
    if perturb:
        return sample(diff)
    cycle = us>=0
    if (cp, cn) in ((12,7),(12,12)) and step == "30n":
        tag = "_".join(f"{value:g}" for value in bias)
        np.savetxt(OUT/f"wave_{tag}_{cp}_{cn}.csv",
                   np.column_stack((us[cycle],diff[cycle],icm[cycle],ocm[cycle])),
                   delimiter=",",header="time_us,diff_v,in_cm_v,out_cm_v",comments="")
    late = sample(diff,88)
    band = max(abs(late)*.001,100e-6)
    bad = np.flatnonzero((us>=46)&(us<=88)&(abs(diff-late)>band))
    return dict(iref_ua=current,vbn_v=vbn,vbp_v=vbp,cp_pf=cp,cn_pf=cn,step=step,
                diff_v=sample(diff),output_cm_v=sample(ocm),input_cm_v=sample(icm),
                min_input_cm_v=min(icm[cycle]),min_output_cm_v=min(ocm[cycle]),
                reset_output_cm_v=sample(ocm,39),late_diff_delta_v=late-sample(diff),
                settle_us=us[bad[-1]+1]-46 if len(bad) else 0,
                vdd_power_uw=-5e4*np.trapz(idd[cycle],us[cycle]))


def main():
    pairs = [(12,7),(12,12),(11.95,7),(12.05,7)]
    with tempfile.TemporaryDirectory(prefix="ota-bias-sc-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        work = Path(tmp)
        jobs = {(b,cp,cn):pool.submit(run,work/f"sig_{i}_{cp}_{cn}",b,cp,cn)
                for i,b in enumerate(CASES) for cp,cn in pairs}
        results = {k:j.result() for k,j in jobs.items()}
        rows = []
        for b in CASES:
            row = results[b,12,7].copy()
            row["sensitivity_mv_per_pf"] = 1e4*(results[b,12.05,7]["diff_v"]-results[b,11.95,7]["diff_v"])
            row["balanced_min_icm_v"] = results[b,12,12]["min_input_cm_v"]
            row["balanced_min_ocm_v"] = results[b,12,12]["min_output_cm_v"]
            rows.append(row)
        write_csv(OUT/"summary.csv",rows)
        write_csv(OUT/"transients.csv",list(results.values()))
        selected = (BASELINE, (4.5,3.0,2.8), (5.5,3.0,2.8), (3.5,2.7,2.8))
        noise = {(b,branch,sign):pool.submit(run,work/f"noise_{i}_{branch}_{sign}",b,12,7,perturb=(branch,sign))
                 for i,b in enumerate(selected) for branch,sign in product(CAPS,(-1,1))}
        write_csv(OUT/"sensor_noise.csv",[
            dict(iref_ua=b[0],vbn_v=b[1],vbp_v=b[2],
                 sensor_rms_uv=1e6*np.sqrt(sum(1.380649e-23*300.15/(cap*1e-12) *
                         ((noise[b,branch,1].result()-noise[b,branch,-1].result())/.002)**2
                         for branch,cap in CAPS.items()))) for b in selected])


if __name__ == "__main__":
    main()
