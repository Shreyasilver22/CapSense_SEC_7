"""Estimate the sensor-only sampled contribution for selected OTA currents."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile

import numpy as np

from sweep import OUT, build, run_spice, write_csv

CAPS = {"p":12,"n":7}


def sample(path, current, branch, sign):
    body = build(current,12,7,"tntp49_5v",5,27)
    body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*CAPS[branch]*1e-7} 143u 1n 1n 9n 1m)\n"
    command = "set klu\ntran 30n 190u 0 30n\nwrdata wave.dat v(outp) v(outn)"
    t, p, n = run_spice(path,"perturb",body,command,"wave.dat").T
    if t[-1] < 189.99e-6:
        raise RuntimeError(f"Incomplete transient {path}")
    return np.interp(180e-6,t,p-n)


def main():
    with tempfile.TemporaryDirectory(prefix="sc-ground-bias-noise-") as tmp, ThreadPoolExecutor(max_workers=5) as pool:
        jobs = {(i,b,s):pool.submit(sample,Path(tmp)/f"{i}_{b}_{s}",i,b,s)
                for i in (3.5,4.5,9) for b in CAPS for s in (-1,1)}
        rows = []
        for i in (3.5,4.5,9):
            variance = 0
            for b,cap in CAPS.items():
                gain = (jobs[i,b,1].result()-jobs[i,b,-1].result())/.002
                variance += gain**2 * 1.380649e-23 * 300.15/(cap*1e-12)
            rows.append(dict(iref_ua=i,sensor_diff_uv_rms=np.sqrt(variance)*1e6))
        write_csv(OUT/"sensor_noise.csv",rows)


if __name__ == "__main__":
    main()
