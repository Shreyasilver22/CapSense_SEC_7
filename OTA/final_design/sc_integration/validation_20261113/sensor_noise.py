"""Propagate independent sensor kT/C charge through the actual clocked circuit."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile

import numpy as np

from run import OUTPUT, SAMPLE_US, circuit, run_spice, write_csv


def sample_response(folder, branch, cap, sign):
    # 1 mV equivalent perturbation on the floating sensor capacitor.
    # The flat pulse is 9 ns with 1 ns edges, giving a 10 ns effective width.
    charge = sign * cap * 1e-12 * 1e-3
    current = charge / 10e-9
    deck = circuit(7, 5) + f"IPERT tx{branch} rx{branch} PULSE(0 {current} 443u 1n 1n 9n 1m)\n"
    commands = "tran 20n 482u 0 20n\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn)"
    wave = run_spice(folder, "sensor_charge", deck, commands, "wave.dat")
    assert wave[-1, 0] >= SAMPLE_US * 1e-6
    op, on, ip, inn = [np.interp(SAMPLE_US*1e-6, wave[:,0], column) for column in wave[:,1:].T]
    return np.array([op-on, (op+on)/2, (ip+inn)/2])


def main():
    sensors = {"p": 7, "n": 5}
    with tempfile.TemporaryDirectory(prefix="sc-sensor-noise-") as temp:
        with ThreadPoolExecutor(max_workers=4) as pool:
            jobs = {(branch,sign): pool.submit(sample_response, Path(temp)/f"{branch}{sign}", branch, cap, sign)
                    for branch,cap in sensors.items() for sign in (-1,1)}
            gains = {branch: (jobs[branch,1].result()-jobs[branch,-1].result())/2e-3
                     for branch in sensors}
    kT = 1.380649e-23 * 300.15
    rms = np.sqrt(sum(gains[branch]**2 * kT/(cap*1e-12) for branch,cap in sensors.items()))
    modes = ("differential", "output_cm", "input_cm")
    write_csv(OUTPUT/"sensor_sampled_noise.csv",
              [dict(mode=mode, p_v_per_v=gains["p"][i], n_v_per_v=gains["n"][i], rms_v=rms[i])
               for i,mode in enumerate(modes)])


if __name__ == "__main__":
    main()
