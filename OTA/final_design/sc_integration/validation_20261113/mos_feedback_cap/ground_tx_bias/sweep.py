"""Test OTA reference current with ground-referenced TX transfer."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import runpy
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
base = runpy.run_path(str(OUT.parent / "study.py"))
deck, mos, run_spice, write_csv = (base[key] for key in ("deck", "mos", "run_spice", "write_csv"))
CURRENTS = (2.5, 3.5, 4.5, 5.5, 7, 9)
PAIRS = ((12, 7), (12, 12), (7, 12), (11.95, 7), (12.05, 7))
PROBES = tuple(f"@mn_{device}_{side}[{terminal}]"
               for side in "pn" for device, terminal in (("clamp", "ibs"), ("transfer", "ibd")))


def build(current, cp, cn, model, supply, temp):
    body = deck(cp, cn, "original", model, supply, temp, 0)
    body = body.replace("IREF vdd bias 3.5u", f"IREF vdd bias {current}u")
    body = "\n".join(line for line in body.splitlines() if not line.startswith(("CFp ", "CFn ")))
    return body + "\n" + "\n".join(mos(f"CF{b}", f"out{b}", f"sum{b}", 97) for b in "pn") + "\n"


def simulate(folder, current, cp, cn, *, model="tntp49_5v", supply=5, temp=27, step="30n", save=False):
    body = build(current, cp, cn, model, supply, temp)
    probes = " ".join(PROBES)
    commands = (f"set klu\nsave all {probes}\ntran {step} 200u 0 {step}\n"
                "wrdata wave.dat v(outp) v(outn) v(sump) v(sumn) v(rxp) v(rxn) i(vdd) " + probes)
    wave = run_spice(folder, "ground_tx", body, commands, "wave.dat")
    if wave[-1,0] < 199.99e-6 or wave.shape[1] != 12:
        raise RuntimeError(f"Incomplete transient or missing probes in {folder}")
    t = wave[:,0]*1e6-100
    p, n, ip, inn, rp, rn, current_dd = wave[:,1:8].T
    diff, icm, ocm = p-n, (ip+inn)/2, (p+n)/2
    cycle = (t>=0)&(t<=100)
    window = (t>=45)&(t<=55)
    junction = np.abs(wave[:,8:])
    sample = lambda values, when=80: float(np.interp(when,t,values))
    late = sample(diff,88)
    band = max(.001*abs(late),100e-6)
    outside = np.flatnonzero((t>=46)&(t<=88)&(abs(diff-late)>band))
    if save:
        np.savetxt(OUT/f"wave_{current:g}u_{cp}_{cn}.csv",
                   np.column_stack((t[cycle],diff[cycle],icm[cycle],ocm[cycle],rp[cycle],rn[cycle])),
                   delimiter=",",header="time_us,diff_v,input_cm_v,output_cm_v,rxp_v,rxn_v",comments="")
    return dict(iref_ua=current,cp_pf=cp,cn_pf=cn,model=model,vdd_v=supply,temp_c=temp,step=step,
                diff_mv=1000*sample(diff),ideal_diff_mv=2000*(supply+2.5)*(cp-cn)/(80+cp+cn),
                input_cm_sample_v=sample(icm), output_cm_sample_v=sample(ocm),
                input_cm_min_v=min(icm[cycle]),output_cm_min_v=min(ocm[cycle]),
                min_rx_v=min(rp[cycle].min(),rn[cycle].min()),
                junction_peak_ua=1e6*junction[window].max(),
                junction_abs_charge_fc=1e9*np.trapz(junction[window].sum(axis=1),t[window]),
                late_diff_change_uv=1e6*(late-sample(diff)),
                settle_us=t[outside[-1]+1]-46 if len(outside) else 0,
                vdd_uw=-1e4*supply*np.trapz(current_dd[cycle],t[cycle]))


def main():
    with tempfile.TemporaryDirectory(prefix="ground-tx-bias-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        work = Path(tmp)
        jobs = {(i,cp,cn):pool.submit(simulate,work/f"{i}_{cp}_{cn}",i,cp,cn,save=(cp,cn) in PAIRS[:2])
                for i in CURRENTS for cp,cn in PAIRS}
        rows = {k:f.result() for k,f in jobs.items()}
        write_csv(OUT/"nominal.csv",list(rows.values()))
        summary = []
        for i in CURRENTS:
            row = rows[i,12,7].copy()
            row["sensitivity_mv_pf"] = (rows[i,12.05,7]["diff_mv"]-rows[i,11.95,7]["diff_mv"])/.1
            balanced = rows[i,12,12]
            for k in ("input_cm_min_v","output_cm_min_v","min_rx_v","junction_peak_ua","junction_abs_charge_fc"):
                row[f"balanced_{k}"] = balanced[k]
            summary.append(row)
        write_csv(OUT/"summary.csv",summary)
        selected = (3.5, min(summary,key=lambda r:r["settle_us"])["iref_ua"])
        stress = [pool.submit(simulate,work/f"stress_{i}_{j}_{cp}_{cn}",i,cp,cn,
                              model=m,supply=v,temp=t)
                  for i in dict.fromkeys(selected)
                  for j,(m,v,t) in enumerate((("wnwp49_5v",4.5,85),("bnbp49_5v",5.5,0),
                                               ("wnbp49_5v",4.5,85),("bnwp49_5v",5.5,0)))
                  for cp,cn in PAIRS[:2]]
        fine = [pool.submit(simulate,work/f"fine_{i}_{cp}_{cn}",i,cp,cn,step="10n")
                for i in dict.fromkeys(selected) for cp,cn in PAIRS[:2]]
        write_csv(OUT/"stress.csv",[f.result() for f in stress])
        write_csv(OUT/"fine.csv",[f.result() for f in fine])
    for i in dict.fromkeys(selected):
        body = build(i,12,7,"tntp49_5v",5,27)
        (OUT/f"ground_tx_{i:g}u.cir").write_text(body+"\n.control\nset klu\nset wr_singlescale\n"
            "set wr_vecnames\ntran 30n 200u 0 30n\nwrdata ground_tx_wave.dat v(outp) v(outn) v(sump) v(sumn)\nquit\n.endc\n.end\n")


if __name__ == "__main__":
    main()
