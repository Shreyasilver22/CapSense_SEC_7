"""Plot PMOS feedback capacitance and SC conversion results."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parent


def read(name):
    return np.genfromtxt(root/name, delimiter=",", names=True, dtype=None, encoding=None)


cv = read("pmos_cv.csv")
screen = read("screen.csv")
fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
ax = axes[0,0]
ax.plot(cv["plate_minus_gate_v"], cv["unit_cap_f"]*1e15, color="#246596")
ax.axvline(0, ls=":", color=".4", label="Reset")
ax.set(xlabel="S/D/body plate minus gate (V)", ylabel="Incremental capacitance (fF)",
       title="One PMOS unit, W = 20 µm, L = 10 µm")
ax.legend()
for kind, label, color in (("ideal","Ideal 40 pF","#273747"),("local","417 units, gate at SUM","#b34c30"),
                           ("charge","260 units, gate at SUM","#82599b"),("reversed","97 units, gate at OUT","#18745a")):
    w = read(f"wave_{kind}_12_7.csv")
    axes[0,1].plot(w["time_us"],1e3*(w["outp"]-w["outn"]),label=label,color=color)
    w = read(f"wave_{kind}_12_12.csv")
    axes[1,0].plot(w["time_us"],(w["outp"]+w["outn"])/2,label=label,color=color)
    rows = screen[(screen["kind"]==kind)&(np.abs(screen["cp_pf"]-np.round(screen["cp_pf"]))<1e-6)]
    pairs = ("7/12","7/7","10/9","12/7","12/12")
    by_pair = {f"{r['cp_pf']:g}/{r['cn_pf']:g}":r["diff_v"]*1e3 for r in rows}
    axes[1,1].plot(pairs,[by_pair[p] for p in pairs],"o-",color=color,label=label)
axes[0,1].set(ylabel="Differential output (mV)", title="12/7 pF sensor pair")
axes[1,0].set(ylabel="SC output common-mode (V)", title="12/12 pF sensor pair")
for ax in (axes[0,1],axes[1,0]):
    ax.axvline(80,ls=":",color=".4")
    ax.set(xlim=(40,92),xlabel="Time within the 10 kHz cycle (µs)")
axes[1,1].set(xlabel="Sensor CP/CN (pF)",ylabel="Sampled differential output (mV)",title="Sample at 80 µs")
for ax in axes.flat:
    ax.grid(alpha=.22)
axes[0,1].legend(fontsize=8)
fig.savefig(root/"mos_feedback_comparison.png",dpi=180)
fig.savefig(root/"mos_feedback_comparison.pdf")
