"""Connect the two SC outputs directly to the final OTA's INP and INN."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[0] / "passive_outputs"))
from simulate import DESIGN, circuit, passive, run_spice, write_csv

OTA = f'.include "{DESIGN}/models/ota_cm2p5_C.spice"\n'
BIASES = """VDDAMP va 0 5
VBNAMP vbna 0 3
VBPAMP vbpa va -2.2
IREFAMP va ba 3.5u
XAMP outp outn amp_p amp_n va 0 ba vref vbna vbpa ota_telescopic_cm2p5
CLAP amp_p 0 5p
CLAN amp_n 0 5p
"""
OUTPUTS = ("outp", "outn", "amp_p", "amp_n")
CORNERS = ((7, 7), (12, 7), (7, 12), (12, 12))


def deck_for(mode, cp, cn, load):
    if mode == "active_sc":
        body = circuit(cp, cn)
    else:
        body = passive(cp, cn, mode == "precharged", load)
        body += OTA
    return body + BIASES


def run(work, mode, cp, cn, load=5, step="20n", perturb=None, save=False, first_cycle=False):
    sample_time = 80e-6 if first_cycle else 480e-6
    stop_us = 100 if first_cycle else 500
    body = deck_for(mode, cp, cn, load)
    if perturb:
        branch, sign = perturb
        cap = cp if branch == "p" else cn
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*cap*1e-7} {43 if first_cycle else 443}u 1n 1n 9n 1m)\n"
    vectors = " ".join(f"v({node})" for node in OUTPUTS) + " i(vdd) i(vddamp)"
    commands = f"set klu\ntran {step} {stop_us}u 0 {step}\nwrdata wave.dat {vectors}"
    wave = run_spice(work, "direct", body, commands, "wave.dat")
    if wave[-1,0] < (stop_us - .01)*1e-6:
        raise RuntimeError(f"Incomplete run at {work}")
    t, ip, inn, op, on, isc, iamp = wave.T
    signals = (ip - inn, (ip + inn)/2, op - on, (op + on)/2)
    at_sample = np.array([np.interp(sample_time, t, y) for y in signals])
    if perturb:
        return at_sample
    use = (t >= 400e-6) & (t <= 500e-6)
    if save:
        np.savetxt(OUT/f"wave_{mode}_{cp}_{cn}.csv", wave[use,:5], delimiter=",",
                   header="time_s," + ",".join(OUTPUTS), comments="")
    row = dict(mode=mode, cp_pf=cp, cn_pf=cn, extra_load_pf=load, step=step)
    for name, y, s in zip(("in_diff","in_cm","out_diff","out_cm"), signals, at_sample):
        row.update({f"{name}_v":s, f"{name}_min_v":min(y[use]), f"{name}_max_v":max(y[use]),
                    f"{name}_late_delta_v":np.interp(sample_time+8e-6,t,y)-s})
    for name, y in zip(OUTPUTS, (ip,inn,op,on)):
        row[f"{name}_v"] = np.interp(sample_time,t,y)
    for name, current in (("sc",isc),("amp",iamp)):
        row[f"{name}_vdd_power_uw"] = -5e10*np.trapz(current[use],t[use])
    return row


def main():
    modes = ("literal", "precharged", "active_sc")
    with tempfile.TemporaryDirectory(prefix="sc-direct-") as temp:
        work = Path(temp)
        with ThreadPoolExecutor(max_workers=4) as pool:
            endpoints = [pool.submit(run, work/f"{mode}_{cp}_{cn}", mode, cp, cn,
                                     step="50n", save=True)
                         for mode in modes for cp,cn in CORNERS]
            sensitivity = [pool.submit(run, work/f"slope_{cp}", "active_sc", cp, 7, step="50n")
                           for cp in (11.95,12.05)]
            noise = {(branch,sign):pool.submit(run, work/f"noise_{branch}_{sign}",
                                              "active_sc", 12, 7, step="50n",
                                              perturb=(branch,sign), first_cycle=True)
                     for branch in ("p","n") for sign in (-1,1)}
            write_csv(OUT/"rerun_endpoints.csv", [job.result() for job in endpoints])
            write_csv(OUT/"rerun_sensitivity.csv", [job.result() for job in sensitivity])
            variance = np.zeros(4)
            for branch, cap in (("p",12),("n",7)):
                gain = (noise[branch,1].result()-noise[branch,-1].result())/.002
                variance += gain**2 * 1.380649e-23 * 300.15 / (cap*1e-12)
            keys = ("in_diff_rms_v","in_cm_rms_v","out_diff_rms_v","out_cm_rms_v")
            write_csv(OUT/"rerun_sensor_noise.csv", [dict(zip(keys, np.sqrt(variance)))])


if __name__ == "__main__":
    main()
