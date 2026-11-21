"""Sweep the PMOS acquisition switch width with a 10 pF load per side."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from hold import Case, OUT, build, run_spice, write_csv


def sized_body(case, width):
    lines = build(case).splitlines()
    for index, line in enumerate(lines):
        if line.startswith(("MP_tr_p ", "MP_tr_n ")):
            lines[index] = (line.replace("W=20u", f"W={width}u")
                            .replace("AD=90p", f"AD={4.5*width}p")
                            .replace("AS=90p", f"AS={4.5*width}p")
                            )
    return "\n".join(lines) + "\n"


def simulate(folder, width, case=Case()):
    cmd = "set klu\ntran 20n 200u 0 20n\nwrdata wave.dat v(holdp) v(holdn)"
    t, p, n = run_spice(folder,"width",sized_body(case,width),cmd,"wave.dat").T
    if t[-1] < 199.99e-6:
        raise RuntimeError(f"Incomplete width transient in {folder}")
    track, held = np.interp([179.73e-6,181e-6],t,p-n)*1e6
    return dict(pmos_w_um=width,corner=case.corner,cp_pf=case.cp,cn_pf=case.cn,track_uv=track,held_uv=held,edge_shift_uv=held-track)


def main():
    widths = (7.5,10,15,20,25,30)
    with TemporaryDirectory(prefix="sc-hold-width-") as tmp, ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(simulate,Path(tmp)/str(w),w) for w in widths]
        write_csv(OUT/"width_screen.csv",[job.result() for job in jobs])
        check_corners(pool, Path(tmp))


def check_corners(pool, work):
    cases = [Case(cp, cn, corner=k) for k in range(5) for cp,cn in ((12,7),(7,12),(12,12))]
    jobs = [pool.submit(simulate,work/f"candidate_{j}",7.5,case) for j,case in enumerate(cases)]
    write_csv(OUT/"narrow_width_cases.csv",[job.result() for job in jobs])
    (OUT/"hold_10pf_narrow.cir").write_text(sized_body(Case(),7.5) +
        "\n.tran 20n 200u 0 20n\n.meas tran held_diff find par('v(holdp)-v(holdn)') at=181u\n.end\n")


if __name__=="__main__":
    main()
