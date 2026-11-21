"""Use SCL08 transmission gates for a precharged acquisition capacitor."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory

from stress import OUT, Trial, run_trial, write_csv
import stress

fixture = stress.body


def native_body(case):
    deck = fixture(case)
    if not case.acquisition_pf:
        return deck
    lines = [line for line in deck.splitlines()
             if not line.startswith(("VTR ", "VPR ", ".model SWLOAD", "SACQ", "SPRE"))]
    vdd = case.supply
    t = case.track_at_us
    lines += [
        f"VTR tr 0 PULSE(0 {vdd} {t}u .5u .5u {82-t-.5:g}u 100u)",
        f"VPR pr 0 PULSE({vdd} 0 65u .5u .5u 24.5u 100u)",
        f"BTR trb 0 V={vdd}-v(tr)", f"BPR prb 0 V={vdd}-v(pr)",
    ]
    for branch in "pn":
        for port, clock in ((f"out{branch}", "tr"), ("pre", "pr")):
            name = f"{clock}_{branch}"
            lines += [
                f"MN_{name} {port} {clock} hold{branch} 0 N W=10u L=.8u AD=45p AS=45p PD=29u PS=29u",
                f"MP_{name} {port} {clock}b hold{branch} vdd P W=20u L=.8u AD=90p AS=90p PD=49u PS=49u",
            ]
    return "\n".join(lines)+"\n"


def main():
    stress.body = native_body
    cases = [Trial("native", acquisition_pf=cap, precharge_v=pre, track_at_us=at,step_ns=30)
             for cap,pre,at in product((5,10),(0,2.5),(70,78))]
    cases += [Trial("native", acquisition_pf=20,precharge_v=0,track_at_us=70,step_ns=30)]
    cases += [Trial("native", acquisition_pf=cap,precharge_v=2.5,track_at_us=70,
                    model="wnbp49_5v",supply=4.5,temp=85,step_ns=30) for cap in (0,10)]
    cases += [Trial("native", step_ns=30)]
    with TemporaryDirectory(prefix="sc-native-load-") as temp, ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda pair:run_trial(Path(temp)/str(pair[0]),pair[1]),enumerate(cases)))
    rows = [x for x in results if x is not None]
    for row in rows:
        ref = next(r for r in rows if r["acquisition_pf"]==0 and r["model"]==row["model"])
        row["captured_error_mv"] = row["acquired_diff_mv"]-ref["diff_mv"] if row["acquisition_pf"] else ""
    write_csv(OUT/"native_load.csv",rows)
    (OUT/"native_load_10pf.cir").write_text(native_body(cases[6]) +
        "\n.tran 30n 200u 0 30n\n.meas tran captured_diff find par('v(holdp)-v(holdn)') at=180u\n.end\n")


if __name__=="__main__":
    main()
