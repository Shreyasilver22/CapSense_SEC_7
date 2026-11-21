"""Sweep the released 10 kHz readout over both sensor capacitances."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import sys
import tempfile

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run import SAMPLE_US, circuit, metrics, run_spice, transient, write_csv

OUTPUT = Path(__file__).resolve().parent
GRID = tuple(product(range(7, 13), repeat=2))
NOISE_CASES = ((7, 7), (7, 12), (12, 7), (12, 12))
FINE_CASES = ((7, 12), (12, 7), (12, 12))


def simulate(folder, cp, cn, step):
    wave = transient(folder, cp, cn, step)
    result = metrics(wave, cp, cn)
    time_us = wave[:, 0] * 1e6
    outp, outn = (np.interp(SAMPLE_US, time_us, wave[:, i]) for i in (1, 2))
    late_diff = np.interp(488, time_us, wave[:, 1] - wave[:, 2])
    result.update(out_p_v=outp, out_n_v=outn,
                  diff_error_v=result["out_diff_v"] - result["ideal_diff_v"],
                  late_diff_change_v=late_diff - result["out_diff_v"])
    if (cp, cn) in NOISE_CASES and step == "20n":
        cycle = wave[wave[:, 0] >= 400e-6, :5]
        np.savetxt(OUTPUT / f"cycle_{cp}_{cn}.csv", cycle, delimiter=",",
                   header="time_s,outp,outn,sump,sumn", comments="")
    return result


def sample_response(folder, cp, cn, branch, sign):
    cap = cp if branch == "p" else cn
    # Independent sensor voltage perturbation after sampling, before RX transfer.
    current = sign * cap * 1e-12 * 1e-3 / 10e-9
    deck = circuit(cp, cn) + f"IPERT tx{branch} rx{branch} PULSE(0 {current} 443u 1n 1n 9n 1m)\n"
    commands = "tran 20n 482u 0 20n\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn)"
    wave = run_spice(folder, "charge_perturbation", deck, commands, "wave.dat")
    if wave[-1, 0] < SAMPLE_US * 1e-6:
        raise ValueError(f"Transient failed to reach sample in {folder}")
    op, on, ip, inn = [np.interp(SAMPLE_US * 1e-6, wave[:, 0], x) for x in wave[:, 1:].T]
    return np.array([op - on, (op + on) / 2, (ip + inn) / 2])


def main():
    with tempfile.TemporaryDirectory(prefix="sc-cap-sweep-") as temp:
        work = Path(temp)
        with ThreadPoolExecutor(max_workers=6) as pool:
            runs = {(cp, cn): pool.submit(simulate, work / f"grid_{cp}_{cn}", cp, cn, "20n")
                    for cp, cn in GRID}
            fine = {pair: pool.submit(simulate, work / f"fine_{pair}", *pair, "5n")
                    for pair in FINE_CASES}
            noise = {(cp, cn, branch, sign): pool.submit(
                sample_response, work / f"noise_{cp}_{cn}_{branch}_{sign}", cp, cn, branch, sign)
                for cp, cn in NOISE_CASES for branch in ("p", "n") for sign in (-1, 1)}
            rows = [future.result() for future in runs.values()]
            write_csv(OUTPUT / "sweep.csv", rows)
            write_csv(OUTPUT / "timestep_check.csv", [f.result() for f in fine.values()])
            results = []
            for cp, cn in NOISE_CASES:
                gain_p, gain_n = [(noise[cp, cn, branch, 1].result() -
                                   noise[cp, cn, branch, -1].result()) / 2e-3
                                  for branch in ("p", "n")]
                rms = np.sqrt(1.380649e-23 * 300.15 *
                              (gain_p**2 / (cp * 1e-12) + gain_n**2 / (cn * 1e-12)))
                results.append(dict(cp_pf=cp, cn_pf=cn, diff_rms_v=rms[0],
                                    output_cm_rms_v=rms[1], input_cm_rms_v=rms[2]))
            write_csv(OUTPUT / "sensor_sampled_noise.csv", results)


if __name__ == "__main__":
    main()
