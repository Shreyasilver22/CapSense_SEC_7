"""Characterize and test a PMOS bank in place of each SC feedback capacitor."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import sys
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "vcm_switch_reference"))
from study import DESIGN, deck, run_spice, write_csv

MODELS = DESIGN / "models/scl08_models.inc"
NODES = "outp outn sump sumn rxp rxn".split()


def mos(name, gate, plate, units):
    return (f"M{name} {plate} {gate} {plate} {plate} P W=20u L=10u M={units} "
            "AD=90p AS=90p PD=49u PS=49u")


def characterize(work):
    body = f'PMOS feedback capacitor C-V\n.include "{MODELS}"\n'
    body += "VPLATE plate 0 2.5\nVG gate 0 DC 2.5 AC 1\n" + mos("UNIT", "gate", "plate", 1)
    # Positive bias means the gate is below the shorted S/D/body plate.
    biases = np.arange(-40, 81) * .025
    commands = ["set appendwrite"]
    for bias in biases:
        commands.extend([f"alter VG {2.5-bias:.8g}", "ac lin 1 10k 10k",
                         f"let bias = {bias:.8g}", "let cap = -imag(i(vg))/(2*pi*10000)",
                         "wrdata cv.dat bias cap", "unset wr_vecnames"])
    raw = run_spice(work, "characterize", body, "\n".join(commands), "cv.dat")
    cv = raw[:, 1:3]
    assert len(cv) == len(biases) and min(cv[:,1]) > 0
    write_csv(OUT/"pmos_cv.csv",[dict(plate_minus_gate_v=v,unit_cap_f=c) for v,c in cv])
    return cv


def sc_body(kind, cp, cn, units):
    body = deck(cp, cn, "tx_only", "tntp49_5v", 5, 27, 0)
    if kind != "ideal":
        body, count = re.subn(r"^CF[pn] .*\n", "", body, flags=re.M)
        assert count == 2
        for branch in "pn":
            gate, plate = f"sum{branch}", f"out{branch}"
            if kind == "reversed":
                gate, plate = plate, gate
            body += mos(f"CF{branch}", gate, plate, units) + "\n"
    return body


def transient(folder, kind, cp, cn, units=0, step="30n", cycles=2, save=False):
    body = sc_body(kind, cp, cn, units)
    vectors = " ".join(f"v({node})" for node in NODES)
    command = f"set klu\ntran {step} {cycles*100}u 0 {step}\nwrdata wave.dat {vectors} i(vdd) i(vref)"
    wave = run_spice(folder, "feedback", body, command, "wave.dat")
    if wave[-1,0] < (cycles*100-.01)*1e-6:
        raise ValueError(f"Incomplete run {folder}")
    t = wave[:,0]*1e6-(cycles-1)*100
    pick = (t>=0)&(t<=100)
    op,on,ip,inn,rp,rn,idd,iref = wave[:,1:].T
    diff,icm,ocm = op-on,(ip+inn)/2,(op+on)/2
    sample = lambda x, at=80: float(np.interp(at,t,x))
    if save:
        np.savetxt(OUT/f"wave_{kind}_{cp}_{cn}.csv", np.column_stack((t[pick],wave[pick,1:])),
                   delimiter=",",header="time_us,"+",".join(NODES+["idd_a","iref_a"]),comments="")
    late = sample(diff,88)
    band = max(abs(late)*.001,100e-6)
    bad = np.flatnonzero((t>=46)&(t<=88)&(abs(diff-late)>band))
    return dict(kind=kind,cp_pf=cp,cn_pf=cn,units=units,maxstep=step,cycles=cycles,
                diff_v=sample(diff),outp_v=sample(op),outn_v=sample(on),in_cm_v=sample(icm),
                out_cm_v=sample(ocm),in_cm_min_v=min(icm[pick]),out_cm_min_v=min(ocm[pick]),
                vcf_p_v=sample(op-ip),vcf_n_v=sample(on-inn),
                late_change_v=late-sample(diff),settle_us=t[bad[-1]+1]-46 if len(bad) else 0,
                vdd_uw=-.05e6*np.trapz(idd[pick],t[pick]),ref_sink_ua=max(iref[pick])*1e6)


def main():
    with tempfile.TemporaryDirectory(prefix="sc-moscap-") as tmp:
        work = Path(tmp)
        v,c = characterize(work/"cv").T
        bias = .96
        active = (v>0)&(v<bias)
        x = np.r_[0,v[active],bias]
        secant = np.trapz(np.interp(x,v,c),x)/bias
        sizes = {"local": round(40e-12/np.interp(bias,v,c)), "charge": round(40e-12/secant),
                 "reversed": round(40e-12/np.interp(-bias,v,c))}
        write_csv(OUT/"sizing.csv",[dict(kind=k,units=m,unit_w_um=20,unit_l_um=10,
                                       total_gate_um2=200*m) for k,m in sizes.items()])
        print(sizes,flush=True)
        with ThreadPoolExecutor(max_workers=5) as pool:
            cases = [(kind,cp,cn,sizes.get(kind,0)) for kind in ("ideal",*sizes)
                     for cp,cn in ((7,7),(12,7),(7,12),(12,12),(10,9),(11.95,7),(12.05,7))]
            futures = [pool.submit(transient,work/str(i),*case,save=case[1:3] in ((12,7),(12,12)))
                       for i,case in enumerate(cases)]
            write_csv(OUT/"screen.csv",[f.result() for f in futures])
            fine = [pool.submit(transient,work/f"fine_{kind}",kind,12,7,sizes[kind],step="10n",cycles=5)
                    for kind in ("local","charge")]
            write_csv(OUT/"fine.csv",[f.result() for f in fine])
        for kind in ("local","charge","reversed"):
            (OUT/f"{kind}_12_7.cir").write_text(sc_body(kind,12,7,sizes[kind]) +
                "\n.control\nset klu\nset wr_singlescale\nset wr_vecnames\ntran 30n 200u 0 30n\n"
                "wrdata wave.dat v(outp) v(outn) v(sump) v(sumn)\nquit\n.endc\n.end\n")


if __name__ == "__main__":
    main()
