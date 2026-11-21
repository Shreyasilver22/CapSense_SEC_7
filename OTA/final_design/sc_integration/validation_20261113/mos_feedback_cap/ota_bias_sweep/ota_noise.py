"""Standalone OTA differential input-referred noise at the SC transfer bias."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile

import numpy as np

from sweep import base, run_spice, write_csv

OUT = Path(__file__).resolve().parent
DESIGN = base["DESIGN"]


def run(folder, current):
    body = (DESIGN/"tb/ac.cir").read_text().split(".control")[0]
    body = body.replace('"../models/', f'"{DESIGN}/models/')
    body = body.replace("VICM icm 0 2.5", "VICM icm 0 1.538")
    body = body.replace("IREF vdd bn 3.5u", f"IREF vdd bn {current}u")
    # Identical input drive and DC servo for all current settings.
    commands = "noise v(od) VCMD dec 50 1 10Meg\nsetplot noise1\nwrdata noise.dat inoise_spectrum"
    data = run_spice(folder,"ota",body,commands,"noise.dat")
    assert data[0,0] == 1 and data[-1,0] >= 9.999e6 and min(data[:,1]) > 0
    return data


def main():
    currents = (2.5,3.5,4.5,5.5,7.0)
    with tempfile.TemporaryDirectory(prefix="ota-bias-noise-") as tmp, ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda i:run(Path(tmp)/str(i),i),currents))
    f = results[0][:,0]
    np.savetxt(OUT/"ota_noise_spectra.csv",np.column_stack([f,*[r[:,1] for r in results]]),
               delimiter=",",header="hz,"+",".join(f"i_{i:g}_v_per_sqrt_hz" for i in currents),comments="")
    write_csv(OUT/"ota_noise_summary.csv",[
        dict(iref_ua=i,**{f"noise_{hz:g}hz_nv_rt_hz":np.interp(hz,f,d[:,1])*1e9
                          for hz in (10,1000,100000,1000000)}) for i,d in zip(currents,results)])


if __name__ == "__main__":
    main()
