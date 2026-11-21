"""Run the differential unity-gain interface with native RPP resistors."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import tempfile

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from run import circuit, run_spice, write_csv

BIASES = """VDDAMP va 0 5
VBNAMP vbna 0 3
VBPAMP vbpa va -2.2
IREFAMP va ba 3.5u
XAMP ip im amp_p amp_n va 0 ba vref vbna vbpa ota_telescopic_cm2p5
CLAP amp_p 0 5p
CLAN amp_n 0 5p
"""
NODES = "outp outn ip im amp_p amp_n"


def body(cp, cn, resistance_k, parasitic_pf, buffered=True):
    deck = circuit(cp, cn)
    if not buffered:
        return deck
    deck += BIASES
    length_um = resistance_k * 1000 * 2.4 / 28
    for name, a, b in (("IP", "outp", "ip"), ("IN", "outn", "im"),
                       ("FP", "amp_n", "ip"), ("FN", "amp_p", "im")):
        deck += f"XR{name} {a} {b} RPP W=2.4u L={length_um:.10g}u\n"
        if parasitic_pf:
            deck += f"CP{name}A {a} 0 {parasitic_pf/2}p\n"
            deck += f"CP{name}B {b} 0 {parasitic_pf/2}p\n"
    return deck


def simulate(work, cp, cn, r, parasitic=0, *, buffered=True, cycles=2, step="30n", save=False):
    vectors = " ".join(f"v({node})" for node in (NODES.split() if buffered else NODES.split()[:2]))
    deck = body(cp, cn, r, parasitic, buffered)
    commands = f"set klu\ntran {step} {cycles*100}u 0 {step}\nwrdata wave.dat {vectors} i(vdd)"
    if buffered:
        commands += " i(vddamp)"
    data = run_spice(work, "unity", deck, commands, "wave.dat")
    if data[-1,0] < (cycles*100-.01)*1e-6:
        raise RuntimeError(f"Incomplete run: {work}")
    t = data[:,0]*1e6 - (cycles-1)*100
    take = (t>=0) & (t<=100)
    sp, sn = data[:,1:3].T
    diff = sp-sn
    sample = lambda y, time=80: float(np.interp(time,t,y))
    row = dict(cp_pf=cp, cn_pf=cn, r_kohm=r, parasitic_pf_per_r=parasitic,
               cycles=cycles, maxstep=step, sc_diff_v=sample(diff), sc_cm_v=sample((sp+sn)/2),
               sc_late_delta_v=sample(diff,88)-sample(diff), sc_power_uw=-.05*np.trapz(data[take,-2 if buffered else -1],t[take])*1e6)
    if buffered:
        ip, im, op, on = data[:,3:7].T
        amp, cm = op-on, (op+on)/2
        error = amp-diff
        # Last time outside a 0.1% band about the 88 us sampled value.
        late = sample(amp,88)
        band = max(abs(late)*.001, 100e-6)
        bad = np.flatnonzero((t>=46)&(t<=88)&(abs(amp-late)>band))
        settle = max(0,t[min(bad[-1]+1,len(t)-1)]-46) if len(bad) else 0
        row.update(amp_diff_v=sample(amp), amp_cm_v=sample(cm), tracking_error_v=sample(error),
                   ota_input_cm_v=sample((ip+im)/2), amp_late_delta_v=late-sample(amp),
                   amp_settle_us=settle, settle_band_v=band, amp_cm_min_v=min(cm[take]),
                   amp_cm_max_v=max(cm[take]), amp_power_uw=-.05*np.trapz(data[take,-1],t[take])*1e6)
    if save:
        np.savetxt(OUT/f"wave_{cp}_{cn}_{r}_{parasitic}.csv",np.column_stack((t[take],data[take,1:7])),
                   delimiter=",",header="time_us,outp,outn,ip,im,amp_p,amp_n",comments="")
    return row


def bench(path, cp, cn, r, parasitic):
    path.write_text(body(cp,cn,r,parasitic) +
        "\n.control\nset klu\nset wr_singlescale\nset wr_vecnames\ntran 30n 200u 0 30n\n"
        "wrdata unity_wave.dat v(outp) v(outn) v(ip) v(im) v(amp_p) v(amp_n)\nquit\n.endc\n.end\n")


def screen():
    with tempfile.TemporaryDirectory(prefix="sc-unity-") as tmp:
        work = Path(tmp)
        tests = [(r,c) for r in (20,100,200,500) for c in (0,)]
        tests += [(100,1.3),(200,2.7),(500,6.7)]
        with ThreadPoolExecutor(max_workers=5) as pool:
            baseline = pool.submit(simulate,work/"baseline",12,7,0,buffered=False)
            jobs = [pool.submit(simulate, work/f"r{r}c{c}",12,7,r,c) for r,c in tests]
            write_csv(OUT/"screen.csv",[job.result() for job in jobs])
            write_csv(OUT/"baseline.csv",[baseline.result()])


if __name__ == "__main__":
    screen()
