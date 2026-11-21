"""Compare the literal OTA removal with a passive readout reset to 2.5 V."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import re
import sys
import tempfile

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run import DESIGN, SIGNALS, circuit, run_spice, write_csv

OUT = Path(__file__).resolve().parent
ENDPOINTS = [(7, 7), (12, 7), (7, 12), (12, 12)]
MODEL_DIR = Path.home() / "pdk/scl08/ngspice_models49/mos"


def passive(cp, cn, precharge, load_pf=5, load_mohm=None, corner="typ", temp=27):
    deck = circuit(cp, cn)
    deck = re.sub(r"^(?:XOTA |VBN |VBP |IREF |\.include .*ota_cm2p5_C).*\n", "", deck, flags=re.M)
    if corner != "typ":
        include = (DESIGN / "models/scl08_models.inc").read_text()
        include = include.replace(str(MODEL_DIR / "tntp49_5v"), str(MODEL_DIR / corner))
        deck = deck.replace(f'.include "{DESIGN}/models/scl08_models.inc"', include)
    deck = deck.replace(".temp 27", f".temp {temp}")
    for branch in ("p", "n"):
        deck = re.sub(rf"^CL{branch.upper()} out{branch} 0 5p", f"CL{branch.upper()} out{branch} 0 {load_pf}p",
                      deck, flags=re.M)
        if load_mohm is not None:
            deck += f"RL{branch} out{branch} 0 {load_mohm}Meg\n"
        if precharge:
            deck += (f"MN_PRE_{branch} vref phi1 out{branch} 0 N W=10u L=0.8u "
                     f"AD=45p AS=45p PD=29u PS=29u\n"
                     f"MP_PRE_{branch} vref phi1b out{branch} vdd P W=20u L=0.8u "
                     f"AD=90p AS=90p PD=49u PS=49u\n")
    return deck


def sample(wave, time_us):
    p, n = [np.interp(time_us * 1e-6, wave[:, 0], v) for v in wave[:, 1:3].T]
    return p, n, p - n, (p + n) / 2


def run(folder, cp, cn, variant, load=5, load_r=None, corner="typ", temp=27,
        step="20n", perturb=None, save=False):
    deck = passive(cp, cn, variant == "precharged", load, load_r, corner, temp)
    if perturb:
        branch, sign = perturb
        cap = cp if branch == "p" else cn
        deck += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*cap*1e-7} 443u 1n 1n 9n 1m)\n"
    commands = f"tran {step} 500u 0 {step}\nwrdata wave.dat " + " ".join(f"v({n})" for n in SIGNALS)
    wave = run_spice(folder, "passive", deck, commands, "wave.dat")
    if wave[-1, 0] < 499.99e-6:
        raise RuntimeError(f"Incomplete transient {folder}")
    p, n, diff, cm = sample(wave, 480)
    if perturb:
        return np.array([diff, cm])
    cycle = wave[(wave[:, 0] >= 400e-6) & (wave[:, 0] < 500e-6)]
    cm_trace = (cycle[:, 1] + cycle[:, 2]) / 2
    if save:
        np.savetxt(OUT / f"wave_{variant}_{cp}_{cn}.csv", cycle, delimiter=",",
                   header="time_s," + ",".join(SIGNALS), comments="")
    return dict(variant=variant, cp_pf=cp, cn_pf=cn, load_pf=load, load_mohm=load_r,
                corner=corner, temp_c=temp, maxstep=step, reset_cm_v=sample(wave,430)[3],
                outp_v=p, outn_v=n, diff_v=diff, cm_v=cm, cycle_cm_min_v=min(cm_trace),
                cycle_cm_max_v=max(cm_trace), late_diff_change_v=sample(wave,488)[2]-diff,
                late_cm_change_v=sample(wave,488)[3]-cm, prior_cycle_diff_v=sample(wave,380)[2],
                prior_cycle_cm_v=sample(wave,380)[3])


def main():
    with tempfile.TemporaryDirectory(prefix="sc-passive-") as temp:
        work = Path(temp)
        with ThreadPoolExecutor(max_workers=8) as pool:
            tests = []
            def queue(label, cp, cn, variant, **kwargs):
                tests.append((label, pool.submit(run, work / str(len(tests)), cp, cn, variant, **kwargs)))

            for variant in ("literal", "precharged"):
                for cp, cn in product(range(7,13), repeat=2):
                    queue("grid", cp, cn, variant, save=(cp,cn) in ENDPOINTS)
                for cp, cn in ((11.95,7),(12.05,7),(9.45,9.55),(9.55,9.45)):
                    queue("slope", cp, cn, variant)
                for load, load_r in ((1,None),(20,None),(5,1),(5,100)):
                    queue("load", 12, 7, variant, load=load, load_r=load_r)
                for cp, cn in ((12,7),(12,12)):
                    queue("fine", cp, cn, variant, step="5n")
                for corner, temp_c in (("wnwp49_5v",85),("bnbp49_5v",0)):
                    queue("stress", 12, 7, variant, corner=corner, temp=temp_c)
            jobs = {}
            for variant in ("literal", "precharged"):
                for cp,cn in ((7,7),(12,7),(12,12)):
                    for branch, sign in product(("p","n"), (-1,1)):
                        key = (variant,cp,cn,branch,sign)
                        jobs[key] = pool.submit(run, work / "_".join(map(str,key)),
                                                cp, cn, variant, perturb=(branch,sign))
            for label in ("grid", "slope", "load", "fine", "stress"):
                write_csv(OUT / f"{label}.csv", [f.result() for k,f in tests if k == label])
            noise_rows = []
            for variant,cp,cn in dict.fromkeys(k[:3] for k in jobs):
                variance = np.zeros(2)
                for branch,cap in (("p",cp),("n",cn)):
                    gain = (jobs[variant,cp,cn,branch,1].result() -
                            jobs[variant,cp,cn,branch,-1].result()) / .002
                    variance += gain**2 * 1.380649e-23 * 300.15 / (cap * 1e-12)
                noise_rows.append(dict(variant=variant, cp_pf=cp, cn_pf=cn,
                                       diff_rms_v=np.sqrt(variance[0]), cm_rms_v=np.sqrt(variance[1])))
            write_csv(OUT / "sensor_noise.csv", noise_rows)
    for variant in ("literal","precharged"):
        (OUT / f"{variant}_12_7.cir").write_text(
            passive(12,7,variant=="precharged") +
            "\n.control\ntran 20n 500u 0 20n\nplot v(outp) v(outn)\n.endc\n.end\n")


if __name__ == "__main__":
    main()
