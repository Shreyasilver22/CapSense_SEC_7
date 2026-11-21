"""Propagate an independent feedback-reset kT/C charge estimate."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from hold import OUT, Case, build, run_spice, write_csv

CF_PF = 121 * .4125499322514286


def sample(folder, cap, branch, sign):
    body = build(Case(cap=cap))
    # Perturb each feedback branch after reset opens and before RX connects.
    body += f"IRST{branch} out{branch} sum{branch} PULSE(0 {sign*CF_PF*1e-7} 142.7u 1n 1n 9n 1m)\n"
    commands = "set klu\ntran 20n 190u 0 20n\nwrdata wave.dat v(holdp) v(holdn)"
    t, p, n = run_spice(folder,"reset",body,commands,"wave.dat").T
    if t[-1] < 189.99e-6:
        raise RuntimeError(f"Incomplete reset perturbation {folder}")
    return float(np.interp(181e-6,t,p-n))


def main():
    caps = (5,10,20)
    with TemporaryDirectory(prefix="sc-reset-noise-") as tmp, ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {(c,b,s):pool.submit(sample,Path(tmp)/f"{c}_{b}_{s}",c,b,s)
                for c in caps for b in "pn" for s in (-1,1)}
        rows = []
        for c in caps:
            variance = 0
            for b in "pn":
                gain = (jobs[c,b,1].result()-jobs[c,b,-1].result())/.002
                variance += gain**2 * 1.380649e-23 * 300.15 / (CF_PF*1e-12)
            rows.append(dict(cap_pf=c,reset_uv=np.sqrt(variance)*1e6))
        write_csv(OUT/"reset_noise.csv",rows)


if __name__ == "__main__":
    main()
