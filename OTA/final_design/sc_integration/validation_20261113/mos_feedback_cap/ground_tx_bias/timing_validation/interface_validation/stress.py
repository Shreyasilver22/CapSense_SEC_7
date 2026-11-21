"""PN feedback mismatch, summing-node capacitance, and switched-load screens."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, replace
from pathlib import Path
import sys
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from check import Case, timing_body, run_spice, write_csv


@dataclass(frozen=True)
class Trial:
    group: str
    cp: float = 12
    cn: float = 7
    p_units: int = 121
    n_units: int = 121
    sum_shunt_pf: float = 0
    acquisition_pf: float = 0
    precharge_v: float = 2.5
    track_at_us: float = 70
    model: str = "tntp49_5v"
    supply: float = 5
    temp: float = 27
    step_ns: int = 20


def body(c):
    text = timing_body(Case(8, 3, c.cp, c.cn, model=c.model, supply=c.supply, temp=c.temp))
    lines = []
    for line in text.splitlines():
        for branch, count in (("p", c.p_units), ("n", c.n_units)):
            if line.startswith(f"MCF{branch} "):
                line = line.replace("M=121 AD=", f"M={count} AD=")
        lines.append(line)
    if c.sum_shunt_pf:
        lines.extend(f"Cwell{b} sum{b} 0 {c.sum_shunt_pf}p" for b in "pn")
    if c.acquisition_pf:
        lines.extend((
            f"VPRE pre 0 {c.precharge_v}",
            f"VTR tr 0 PULSE(0 5 {c.track_at_us}u 20n 20n {82-c.track_at_us-.02:.5g}u 100u)",
            "VPR pr 0 PULSE(5 0 65u 20n 20n 25u 100u)",
            ".model SWLOAD SW(RON=100 ROFF=1e12 VT=2.5 VH=0.1)",
        ))
        for b in "pn":
            lines.extend((f"SACQ{b} out{b} hold{b} tr 0 SWLOAD",
                          f"SPRE{b} pre hold{b} pr 0 SWLOAD",
                          f"CSMP{b} hold{b} 0 {c.acquisition_pf}p"))
    return "\n".join(lines) + "\n"


def simulate(folder, c, *, klu=True):
    vectors = "v(outp) v(outn) v(sump) v(sumn) v(rxp) v(rxn)"
    if c.acquisition_pf:
        vectors += " v(holdp) v(holdn)"
    solver = "set klu\n" if klu else ""
    commands = (f"{solver}tran {c.step_ns}n 200u 0 {c.step_ns}n\n"
                f"wrdata wave.dat {vectors}")
    wave = run_spice(folder, "interface", body(c), commands, "wave.dat")
    if wave[-1, 0] < 199.99e-6:
        raise RuntimeError(f"Transient stopped early in {folder} at {wave[-1, 0]:g} s")
    t = wave[:, 0] * 1e6 - 100
    p, n, ip, inn, rp, rn = wave[:, 1:7].T
    d, ocm, icm = p-n, (p+n)/2, (ip+inn)/2
    sample = lambda y, at=80: float(np.interp(at, t, y))
    cycle = (t>=0)&(t<=100)
    row = dict(**asdict(c), diff_mv=1e3*sample(d), ocm_v=sample(ocm), icm_v=sample(icm),
               min_rx_v=min(rp[cycle].min(), rn[cycle].min()), min_icm_v=icm[cycle].min(),
               min_ocm_v=ocm[cycle].min())
    if c.acquisition_pf:
        hp, hn = wave[:, 7:9].T
        row["acquired_diff_mv"] = 1e3*sample(hp-hn)
        row["acquired_cm_v"] = sample((hp+hn)/2)
        acq = (t>=c.track_at_us)&(t<=80)
        row["max_cm_step_mv"] = 1e3*np.max(abs(ocm[acq]-sample(ocm,c.track_at_us)))
        row["max_diff_step_mv"] = 1e3*np.max(abs(d[acq]-sample(d,c.track_at_us)))
    else:
        row.update(acquired_diff_mv="", acquired_cm_v="", max_cm_step_mv="", max_diff_step_mv="")
    if c.group in ("load", "fine") and c.acquisition_pf in (0, 10):
        keep = (t>=65)&(t<=83)
        np.savetxt(OUT / f"wave_{c.group}_{c.acquisition_pf:g}pf_{c.precharge_v:g}v_{c.track_at_us:g}us.csv",
                   np.column_stack((t[keep],d[keep],ocm[keep],wave[keep,7:])),
                   delimiter=",", header="time_us,diff_v,ocm_v"+(",holdp,holdn" if c.acquisition_pf else ""), comments="")
    return row


def run_trial(folder, trial):
    for step in dict.fromkeys((trial.step_ns, 30, 10, 5)):
        try:
            return simulate(folder / str(step), replace(trial, step_ns=step), klu=(step==trial.step_ns))
        except RuntimeError as error:
            print(f"{trial.group}: {error}", flush=True)
    return None


def main():
    trials = [Trial("banks",cp,cn,p,n,shunt)
              for cp,cn in ((12,12),(12,7),(7,12))
              for p,n,shunt in ((121,121,0),(122,120,0),(124,118,0),
                                (127,127,0),(121,121,1),(121,121,3))]
    trials += [Trial("load")]
    trials += [Trial("load",acquisition_pf=cap,precharge_v=pre,track_at_us=at)
               for cap,pre,at in ((2,2.5,70),(5,2.5,70),(10,2.5,70),
                                  (10,0,70),(10,5,70),(10,0,76),(10,0,78),
                                  (10,5,78),(20,0,70),(20,0,78))]
    for m,v,t in (("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0)):
        for cap,at in ((0,70),(10,70),(10,78)):
            trials.append(Trial("load_corner",acquisition_pf=cap,precharge_v=0,track_at_us=at,
                                model=m,supply=v,temp=t))
    trials += [Trial("fine",acquisition_pf=10,precharge_v=0,track_at_us=78,step_ns=5)]
    with tempfile.TemporaryDirectory(prefix="sc-interface-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        jobs = [pool.submit(run_trial,Path(tmp)/str(i),c) for i,c in enumerate(trials)]
        results = [j.result() for j in jobs]
    rows = [r for r in results if r is not None]
    failures = [asdict(c) for c, r in zip(trials, results) if r is None]
    if failures:
        write_csv(OUT/"failed_cases.csv", failures)
    for row in rows:
        reference = next(r for r in rows if r["cp"]==row["cp"] and r["cn"]==row["cn"]
                         and r["model"]==row["model"] and r["acquisition_pf"]==r["sum_shunt_pf"]==0
                         and r["p_units"]==r["n_units"]==121)
        row["sc_error_mv"] = row["diff_mv"] - reference["diff_mv"]
        row["captured_error_mv"] = (row["acquired_diff_mv"]-reference["diff_mv"]
                                    if row["acquisition_pf"] else "")
    write_csv(OUT/"results.csv",rows)


if __name__ == "__main__":
    main()
