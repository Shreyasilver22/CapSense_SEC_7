"""Sweep equal gate-at-output PMOS banks in the 10 kHz SC readout."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import runpy
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
base = runpy.run_path(str(OUT.parent / "study.py"))
sc_body, run_spice, write_csv = (base[key] for key in ("sc_body", "run_spice", "write_csv"))
TARGETS = (20, 25, 30, 40, 50, 60)
PAIRS = ((12, 7), (12, 12), (11.95, 7), (12.05, 7))
CAPS = {"p": 12, "n": 7}
TEMPERATURE_K = 300.15
BOLTZMANN = 1.380649e-23


def run(folder, units, cp, cn, step="30n", perturb=None, save=False):
    body = sc_body("reversed", cp, cn, units)
    if perturb:
        branch, sign = perturb
        current = sign * CAPS[branch] * 1e-7
        # 1 mV equivalent charge on the sensor after reset and before RX transfer.
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {current} 143u 1n 1n 9n 1m)\n"
    commands = f"set klu\ntran {step} 200u 0 {step}\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn)"
    wave = run_spice(folder, "bank_sweep", body, commands, "wave.dat")
    if wave[-1, 0] < 199.99e-6:
        raise RuntimeError(f"Incomplete transient in {folder}")
    t = wave[:, 0] * 1e6 - 100
    op, on, ip, inn = wave[:, 1:].T
    diff, icm, ocm = op - on, (ip + inn) / 2, (op + on) / 2
    sample = lambda x, at=80: float(np.interp(at, t, x))
    if perturb:
        return np.array([sample(diff), sample(ocm), sample(icm)])
    cycle = (t >= 0) & (t <= 100)
    if save:
        np.savetxt(OUT/f"wave_{units}_{cp}_{cn}.csv", np.column_stack((t[cycle],wave[cycle,1:])),
                   delimiter=",", header="time_us,outp,outn,sump,sumn", comments="")
    late = sample(diff, 88)
    band = max(abs(late) * .001, 100e-6)
    bad = np.flatnonzero((t >= 46) & (t <= 88) & (abs(diff - late) > band))
    return dict(units=units, cp_pf=cp, cn_pf=cn, step=step, diff_v=sample(diff),
                in_cm_v=sample(icm), out_cm_v=sample(ocm),
                min_in_cm_v=min(icm[cycle]), min_out_cm_v=min(ocm[cycle]),
                max_plate_minus_gate_v=max(max((ip-op)[cycle]),max((inn-on)[cycle])),
                min_plate_minus_gate_v=min(min((ip-op)[cycle]),min((inn-on)[cycle])),
                late_diff_change_v=late-sample(diff),
                settle_us=t[bad[-1]+1]-46 if len(bad) else 0)


def main():
    cv = np.genfromtxt(OUT.parent/"pmos_cv.csv", delimiter=",", names=True)
    unit_pf = np.interp(-.5, cv["plate_minus_gate_v"], cv["unit_cap_f"]) * 1e12
    counts = {target: round(target/unit_pf) for target in TARGETS}
    with tempfile.TemporaryDirectory(prefix="sc-mos-sweep-") as temp:
        work = Path(temp)
        with ThreadPoolExecutor(max_workers=6) as pool:
            signal = {(target,cp,cn): pool.submit(run,work/f"sig_{target}_{cp}_{cn}",
                       units,cp,cn,save=(cp,cn)==(12,12))
                      for target,units in counts.items() for cp,cn in PAIRS}
            noise = {(target,branch,sign): pool.submit(run,work/f"noise_{target}_{branch}_{sign}",
                      units,12,7,perturb=(branch,sign))
                     for target,units in counts.items() for branch,sign in product(CAPS,(-1,1))}
            fine = {target: pool.submit(run,work/f"fine_{target}",counts[target],12,7,step="10n")
                    for target in (20,30,40)}
            rows = {key: job.result() for key,job in signal.items()}
            write_csv(OUT/"transients.csv",[dict(target_pf=key[0],**row) for key,row in rows.items()])
            results = []
            for target,units in counts.items():
                variance = np.zeros(3)
                for branch,cap in CAPS.items():
                    gain = (noise[target,branch,1].result()-noise[target,branch,-1].result())/.002
                    variance += gain**2 * BOLTZMANN * TEMPERATURE_K/(cap*1e-12)
                diff_rms, ocm_rms, icm_rms = np.sqrt(variance)
                lo,hi = (rows[target,cp,7]["diff_v"] for cp in (11.95,12.05))
                sensitivity = (hi-lo)/.1
                unequal, balanced = rows[target,12,7], rows[target,12,12]
                results.append(dict(target_pf=target, nominal_cf_pf=units*unit_pf, units=units,
                                    diff_mv=unequal["diff_v"]*1e3, sensitivity_mv_per_pf=sensitivity*1e3,
                                    sensor_diff_rms_uv=diff_rms*1e6, sensor_output_cm_rms_nv=ocm_rms*1e9,
                                    sensor_input_cm_rms_uv=icm_rms*1e6,
                                    sensor_equiv_rms_af=diff_rms/sensitivity*1e6,
                                    in_cm_min_12_12_v=balanced["min_in_cm_v"],
                                    out_cm_min_12_12_v=balanced["min_out_cm_v"],
                                    out_cm_sample_12_7_v=unequal["out_cm_v"], settle_12_7_us=unequal["settle_us"]))
            write_csv(OUT/"summary.csv",results)
            write_csv(OUT/"timestep_check.csv",[dict(target_pf=t,**f.result()) for t,f in fine.items()])


if __name__ == "__main__":
    main()
