"""Screen the 97-unit gate-at-output bank against the ideal capacitor."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import runpy
import tempfile

import numpy as np

base = runpy.run_path(str(Path(__file__).with_name("study.py")))
deck = base["deck"]
mos = base["mos"]
run_spice = base["run_spice"]
write_csv = base["write_csv"]
OUT = Path(__file__).resolve().parent


def simulate(folder, kind, cp, cn, corner, supply, temperature, step="30n"):
    body = deck(cp, cn, "tx_only", corner, supply, temperature, 0)
    if kind == "mos97":
        body = "\n".join(line for line in body.splitlines() if not line.startswith(("CFp ", "CFn "))) + "\n"
        body += "\n".join(mos(f"CF{b}", f"out{b}", f"sum{b}", 97) for b in "pn") + "\n"
    commands = f"set klu\ntran {step} 200u 0 {step}\nwrdata wave.dat v(outp) v(outn) v(sump) v(sumn)"
    wave = run_spice(folder, "sc", body, commands, "wave.dat")
    if wave[-1, 0] < 199.99e-6:
        raise RuntimeError(f"Incomplete transient in {folder}")
    t, op, on, ip, inn = wave.T
    mask = (t >= 100e-6) & (t < 200e-6)
    diff, ocm, icm = op-on, (op+on)/2, (ip+inn)/2
    sample = lambda y, at=180: float(np.interp(at*1e-6,t,y))
    return dict(kind=kind,cp_pf=cp,cn_pf=cn,corner=corner,supply=supply,temp_c=temperature,
                step=step,diff_v=sample(diff),out_cm_v=sample(ocm),in_cm_v=sample(icm),
                out_cm_min_v=min(ocm[mask]),in_cm_min_v=min(icm[mask]),
                max_plate_minus_gate_v=max(max((ip-op)[mask]),max((inn-on)[mask])),
                min_plate_minus_gate_v=min(min((ip-op)[mask]),min((inn-on)[mask])),
                late_change_v=sample(diff,188)-sample(diff))


def main():
    typical = "tntp49_5v"
    nominal = [("mos97",cp,cn,typical,5,27) for cp,cn in product(range(7,13),repeat=2)]
    stress = [(kind,cp,cn,corner,supply,temp)
              for kind in ("ideal","mos97") for cp,cn in ((12,7),(12,12))
              for corner,supply,temp in (("wnwp49_5v",4.5,85),("bnbp49_5v",5.5,0),
                                         ("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0))]
    with tempfile.TemporaryDirectory(prefix="sc-mos-verify-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        for name,cases in (("nominal_grid",nominal),("corner_screen",stress)):
            jobs = [pool.submit(simulate,Path(tmp)/f"{name}_{i}",*case) for i,case in enumerate(cases)]
            write_csv(OUT/f"{name}.csv",[job.result() for job in jobs])
        row = simulate(Path(tmp)/"fine","mos97",12,7,typical,5,27,step="10n")
        write_csv(OUT/"reversed_fine.csv",[row])


if __name__ == "__main__":
    main()
