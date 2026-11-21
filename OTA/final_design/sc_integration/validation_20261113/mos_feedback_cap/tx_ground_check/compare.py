"""Compare TX transfer levels using the 97-device PMOS feedback banks."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import runpy
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
base = runpy.run_path(str(OUT.parent / "study.py"))
sc_body, run_spice, write_csv = (base[k] for k in ("sc_body", "run_spice", "write_csv"))
LEVELS = (0, 2, 2.5)
PAIRS = ((12, 7), (12, 12), (11.95, 7), (12.05, 7), (7, 12))


def simulate(work, tx, cp, cn, perturb=None):
    body = sc_body("reversed", cp, cn, 97)
    body = body.replace("VREF vref 0 2.5", f"VREF vref 0 2.5\nVTX vtx 0 {tx}")
    body = body.replace(" vref phi2", " vtx phi2")
    if perturb:
        branch, sign = perturb
        cap = cp if branch == "p" else cn
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*cap*1e-7} 143u 1n 1n 9n 1m)\n"
    cmd = ("set klu\ntran 30n 200u 0 30n\n"
           "wrdata wave.dat v(outp) v(outn) v(sump) v(sumn) v(rxp) v(rxn)")
    t, p, n, ip, inn, rp, rn = run_spice(work, "tx", body, cmd, "wave.dat").T
    if t[-1] < 199.99e-6:
        raise RuntimeError(f"Incomplete transient: {work}")
    diff = p-n
    sample = lambda v, when=180: float(np.interp(when*1e-6,t,v))
    if perturb:
        return sample(diff)
    cycle = t >= 100e-6
    icm, ocm = (ip+inn)/2, (p+n)/2
    late = sample(diff,88+100)
    band = max(abs(late)*.001,100e-6)
    bad = np.flatnonzero((t>=146e-6)&(t<=188e-6)&(abs(diff-late)>band))
    return dict(tx_v=tx,cp_pf=cp,cn_pf=cn,diff_v=sample(diff),
                ideal_diff_v=2*(7.5-tx)*(cp-cn)/(80+cp+cn),
                input_cm_v=sample(icm),output_cm_v=sample(ocm),
                min_input_cm_v=min(icm[cycle]),min_output_cm_v=min(ocm[cycle]),
                min_rx_v=min(rp[cycle].min(),rn[cycle].min()),
                late_change_v=late-sample(diff),
                settle_us=t[bad[-1]+1]*1e6-146 if len(bad) else 0)


def main():
    with tempfile.TemporaryDirectory(prefix="sc-pmos-tx-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        work = Path(tmp)
        jobs = {(tx,cp,cn):pool.submit(simulate,work/f"{tx}_{cp}_{cn}",tx,cp,cn)
                for tx in LEVELS for cp,cn in PAIRS}
        noise = {(tx,b,s):pool.submit(simulate,work/f"noise_{tx}_{b}_{s}",tx,12,7,(b,s))
                 for tx in LEVELS for b in "pn" for s in (-1,1)}
        rows = {k:f.result() for k,f in jobs.items()}
        write_csv(OUT/"transients.csv",list(rows.values()))
        summary = []
        for tx in LEVELS:
            slope = (rows[tx,12.05,7]["diff_v"]-rows[tx,11.95,7]["diff_v"])/.1
            rms = np.sqrt(sum(1.380649e-23*300.15/(cap*1e-12) *
                              ((noise[tx,b,1].result()-noise[tx,b,-1].result())/.002)**2
                              for b,cap in (("p",12),("n",7))))
            row = rows[tx,12,7].copy()
            row.update(sensitivity_mv_per_pf=slope*1e3,sensor_diff_rms_uv=rms*1e6,
                       sensor_equiv_af=rms/abs(slope)*1e6,
                       balanced_min_input_cm_v=rows[tx,12,12]["min_input_cm_v"],
                       balanced_min_output_cm_v=rows[tx,12,12]["min_output_cm_v"])
            summary.append(row)
        write_csv(OUT/"summary.csv",summary)


if __name__ == "__main__":
    main()
