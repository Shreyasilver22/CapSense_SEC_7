"""Test differential capacitor trim against an imposed feedback mismatch."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile

from stress import OUT, Trial, body, run_spice, write_csv
import numpy as np


def test(folder, cp, cn, p_units, n_units, trim_pf):
    netlist = body(Trial("trim", cp, cn, p_units, n_units))
    if trim_pf:
        netlist += f"CTRIM sumn outn {trim_pf}p\n"
    commands = "set klu\ntran 30n 200u 0 30n\nwrdata wave.dat v(outp) v(outn)"
    time, p, n = run_spice(folder, "trim", netlist, commands, "wave.dat").T
    if time[-1] < 199.99e-6:
        raise RuntimeError(f"Incomplete trim transient in {folder}")
    return dict(cp_pf=cp, cn_pf=cn, p_units=p_units, n_units=n_units, trim_pf=trim_pf,
                diff_mv=1000*np.interp(180e-6,time,p-n))


def main():
    pairs = ((12,12), (12,7), (7,12), (7,7), (10,9))
    # Two 412.55 fF units restore equality. Half a unit is a trim-step residual.
    configs = ((121,121,0), (122,120,0), (122,120,.8250998645), (122,120,.6188248984))
    with tempfile.TemporaryDirectory(prefix="sc-trim-") as tmp, ThreadPoolExecutor(max_workers=5) as pool:
        jobs = [pool.submit(test,Path(tmp)/f"{cp}-{cn}-{trim}-{p}",cp,cn,p,n,trim)
                for cp,cn in pairs for p,n,trim in configs]
        rows = [job.result() for job in jobs]
    baseline = {(r["cp_pf"], r["cn_pf"]):r["diff_mv"] for r in rows if r["p_units"]==121}
    for r in rows:
        r["shift_mv"] = r["diff_mv"] - baseline[r["cp_pf"],r["cn_pf"]]
    write_csv(OUT/"trim.csv",rows)


if __name__ == "__main__":
    main()
