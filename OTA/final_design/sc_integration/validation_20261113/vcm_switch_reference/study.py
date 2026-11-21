"""Compare 0 V and VCM as switched-capacitor plate references."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import re
import sys
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from run import DESIGN, circuit, run_spice, write_csv

MODES = {"original": (False, False), "rx_only": (True, False),
         "tx_only": (False, True), "both": (True, True)}
KEY_PAIRS = ((7, 7), (12, 7), (7, 12), (12, 12), (7, 5))
MODELS = Path.home() / "pdk/scl08/ngspice_models49/mos"
VECTORS = "outp outn sump sumn txp rxp txn rxn vref".split()


def deck(cp, cn, mode, mos, supply, temperature, ref_ohm, load_to_ref=False):
    rx, tx = MODES[mode]
    body = circuit(cp, cn)
    body = body.replace("VDD vdd 0 5\n", f"VDD vdd 0 {supply}\n")
    body = body.replace(".temp 27\n", f".temp {temperature}\n")
    body = body.replace("PULSE(5 0", f"PULSE({supply} 0").replace("PULSE(0 5", f"PULSE(0 {supply}")
    body = body.replace("V=5-v(", f"V={supply}-v(")
    if mos != "tntp49_5v":
        include = (DESIGN / "models/scl08_models.inc").read_text()
        include = include.replace(str(MODELS / "tntp49_5v"), str(MODELS / mos))
        body = body.replace(f'.include "{DESIGN}/models/scl08_models.inc"', include)
    if rx:
        body, count = re.subn(r"^(M[NP]_clamp_[pn]) 0 ", r"\1 vref ", body, flags=re.M)
        assert count == 4
    if tx:
        body, count = re.subn(r"^(M[NP]_discharge_[pn]) 0 ", r"\1 vref ", body, flags=re.M)
        assert count == 4
    if load_to_ref:
        body = re.sub(r"^(CL[PN] out[pn]) 0 ", r"\1 vref ", body, flags=re.M)
    if ref_ohm:
        body = body.replace("VREF vref 0 2.5", f"VREF vref_ideal 0 2.5\nRREF vref_ideal vref {ref_ohm}")
    return body


def run(folder, mode, cp, cn, *, mos="tntp49_5v", supply=5, temperature=27,
        ref_ohm=0, load_to_ref=False, cycles=2, step="30n", perturb=None, save=False):
    body = deck(cp, cn, mode, mos, supply, temperature, ref_ohm, load_to_ref)
    start = (cycles - 1)*100
    if perturb:
        branch, sign = perturb
        cap = cp if branch == "p" else cn
        body += f"IPERT tx{branch} rx{branch} PULSE(0 {sign*cap*1e-7} {start+43}u 1n 1n 9n 1m)\n"
    vectors = " ".join(f"v({node})" for node in VECTORS)
    commands = f"set klu\ntran {step} {cycles*100}u 0 {step}\nwrdata wave.dat {vectors} i(vref) i(vdd)"
    data = run_spice(folder, "sc_vcm", body, commands, "wave.dat")
    if data[-1,0] < (cycles*100-.01)*1e-6:
        raise RuntimeError(f"Incomplete transient {folder}")
    t = data[:,0]*1e6-start
    pick = (t>=0)&(t<=100)
    sp, sn, ip, inn, tp, rp, tn, rn, ref, iref, idd = data[:,1:].T
    diff, ocm, icm = sp-sn, (sp+sn)/2, (ip+inn)/2
    sample = lambda v, at=80: float(np.interp(at,t,v))
    if perturb:
        return np.array([sample(diff), sample(icm), sample(ocm)])
    if save:
        np.savetxt(OUT/f"wave_{mode}_{cp}_{cn}.csv", np.column_stack((t[pick], data[pick,1:])),
                   delimiter=",", header="time_us,"+",".join(VECTORS+["iref_a","idd_a"]), comments="")
    rx, tx = MODES[mode]
    excitation = supply + 2.5 - 2.5*(rx+tx)
    late = sample(diff,88)
    band = max(100e-6,abs(late)*.001)
    bad = np.flatnonzero((t>=46)&(t<=88)&(abs(diff-late)>band))
    settled = t[bad[-1]+1]-46 if len(bad) else 0
    return dict(mode=mode,cp_pf=cp,cn_pf=cn,delta_pf=cp-cn,mos=mos,supply_v=supply,
                temp_c=temperature,load_to_ref=load_to_ref,ref_ohm=ref_ohm,cycles=cycles,step=step,
                outp_v=sample(sp),outn_v=sample(sn),diff_v=sample(diff),
                ideal_diff_v=2*excitation*(cp-cn)/(80+cp+cn),
                in_cm_v=sample(icm),out_cm_v=sample(ocm),
                in_cm_min_v=min(icm[pick]),in_cm_max_v=max(icm[pick]),
                out_cm_min_v=min(ocm[pick]),out_cm_max_v=max(ocm[pick]),
                sensor_rx_min_v=min(min(rp[pick]),min(rn[pick])),
                late_diff_change_v=late-sample(diff), settle_us=settled, settle_band_v=band,
                ref_peak_source_ua=max(0,-min(iref[pick])*1e6),
                ref_peak_sink_ua=max(0,max(iref[pick])*1e6),
                ref_peak_deviation_mv=max(abs(ref[pick]-2.5))*1e3,
                ref_avg_abs_ua=np.trapz(abs(iref[pick]),t[pick])*1e4,
                vdd_power_uw=-supply*np.trapz(idd[pick],t[pick])*1e4)


def main():
    with tempfile.TemporaryDirectory(prefix="sc-vcm-") as temp:
        with ThreadPoolExecutor(max_workers=6) as pool:
            jobs = []
            def queue(label, mode, cp, cn, **options):
                jobs.append((label,pool.submit(run,Path(temp)/str(len(jobs)),mode,cp,cn,**options)))
            for mode in MODES:
                for cp,cn in KEY_PAIRS:
                    queue("endpoints",mode,cp,cn,save=(cp,cn) in ((12,7),(12,12)))
            for cp,cn in product(range(7,13),repeat=2):
                if (cp,cn) not in KEY_PAIRS:
                    queue("grid", "both", cp,cn)
            for mode in ("original","both"):
                for cp in (11.95,12.05):
                    queue("slope",mode,cp,7)
            for mode in ("rx_only","both"):
                for resistance in (100,1000):
                    queue("reference",mode,12,7,ref_ohm=resistance)
            for resistance in (0,100,1000):
                queue("load_return","both",12,7,ref_ohm=resistance,load_to_ref=True)
            for mode in ("original","both"):
                queue("fine",mode,12,7,cycles=5,step="10n")
            for mos in ("wnwp49_5v","bnbp49_5v","wnbp49_5v","bnwp49_5v"):
                for supply, temperature in ((4.5,85),(5.5,0)):
                    for cp,cn in ((12,7),(12,12)):
                        queue("stress","both",cp,cn,mos=mos,supply=supply,temperature=temperature)
            noise = {}
            for mode, branch, sign in product(MODES,("p","n"),(-1,1)):
                key = (mode,branch,sign)
                noise[key] = pool.submit(run,Path(temp)/"_".join(map(str,key)),mode,12,7,
                                         perturb=(branch,sign))
            for label in dict.fromkeys(k for k,_ in jobs):
                write_csv(OUT/f"{label}.csv",[f.result() for k,f in jobs if k==label])
            rows = []
            for mode in MODES:
                variance = np.zeros(3)
                for branch, cap in (("p",12),("n",7)):
                    gain = (noise[mode,branch,1].result()-noise[mode,branch,-1].result())/.002
                    variance += gain**2 * 1.380649e-23 * 300.15 / (cap*1e-12)
                keys = ("diff_rms_v","in_cm_rms_v","out_cm_rms_v")
                rows.append(dict(mode=mode,**dict(zip(keys,np.sqrt(variance)))))
            write_csv(OUT/"sensor_noise.csv",rows)
    for mode in MODES:
        body = deck(12,7,mode,"tntp49_5v",5,27,0)
        (OUT/f"{mode}_12_7.cir").write_text(body+"\n.control\nset klu\nset wr_singlescale\nset wr_vecnames\n"
            f"tran 30n 200u 0 30n\nwrdata {mode}_wave.dat v(outp) v(outn) v(sump) v(sumn) i(vref)\nquit\n.endc\n.end\n")


if __name__ == "__main__":
    main()
