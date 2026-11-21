"""Propagate sensor kT/C charge to the sample for ideal and PMOS feedback."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import runpy
import tempfile

import numpy as np

base = runpy.run_path(str(Path(__file__).with_name("study.py")))
OUT, sc_body, run_spice, write_csv = (base[key] for key in ("OUT","sc_body","run_spice","write_csv"))
CAPS = {"p": 12, "n": 7}


def sample(work, kind, branch, sign):
    deck = sc_body(kind, 12, 7, 97)
    current = sign * CAPS[branch] * 1e-7
    deck += f"IPERT tx{branch} rx{branch} PULSE(0 {current} 143u 1n 1n 9n 1m)\n"
    cmd = "set klu\ntran 30n 190u 0 30n\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn)"
    t, op, on, ip, inn = run_spice(work, "sensor", deck, cmd, "wave.dat").T
    if t[-1] < 189.99e-6:
        raise RuntimeError(f"Incomplete noise perturbation in {work}")
    return np.array([np.interp(180e-6,t,y) for y in (op-on,(op+on)/2,(ip+inn)/2)])


def main():
    kinds = ("ideal", "reversed")
    with tempfile.TemporaryDirectory(prefix="mos-cap-noise-") as tmp, ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {(kind,branch,sign): pool.submit(sample,Path(tmp)/f"{kind}_{branch}_{sign}",kind,branch,sign)
                for kind,branch,sign in product(kinds,CAPS,(-1,1))}
        rows = []
        for kind in kinds:
            variance = np.zeros(3)
            for branch,cap in CAPS.items():
                gain = (jobs[kind,branch,1].result()-jobs[kind,branch,-1].result())/.002
                variance += gain**2 * 1.380649e-23 * 300.15/(cap*1e-12)
            diff, out_cm, in_cm = np.sqrt(variance)
            rows.append(dict(kind=kind,diff_rms_v=diff,out_cm_rms_v=out_cm,in_cm_rms_v=in_cm))
    write_csv(OUT/"sensor_noise.csv",rows)


if __name__ == "__main__":
    main()
