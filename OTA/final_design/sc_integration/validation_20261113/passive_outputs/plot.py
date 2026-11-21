"""Plot direct SC outputs and compare against the existing OTA readout."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
grid = np.genfromtxt(folder / "grid.csv", delimiter=",", names=True, encoding=None, dtype=None)
reference = np.genfromtxt(folder.parent / "cap_sweep_7_to_12/sweep.csv", delimiter=",", names=True)
fig, axes = plt.subplots(2, 2, figsize=(11.5, 7), layout="constrained")
for variant, label, color in (("literal", "OTA removed", "#b54b30"),
                               ("precharged", "Passive, 2.5 V reset", "#3377a6")):
    wave = np.genfromtxt(folder / f"wave_{variant}_12_7.csv", delimiter=",", names=True)
    time = 1e6*wave["time_s"]-400
    axes[0,0].plot(time, wave["outp"], color=color, label=label+" OUTP")
    axes[0,0].plot(time, wave["outn"], "--", color=color, label=label+" OUTN")
    axes[0,1].plot(time, (wave["outp"]+wave["outn"])/2, color=color, label=label)
    rows = grid[(grid["variant"] == variant) & (grid["cn_pf"] == 7)]
    axes[1,0].plot(rows["cp_pf"], 1e3*rows["diff_v"], "o-", color=color, label=label)
    rows = grid[(grid["variant"] == variant) & (grid["cp_pf"] == grid["cn_pf"])]
    axes[1,1].plot(rows["cp_pf"], rows["cm_v"], "o-", color=color, label=label)
wave = np.genfromtxt(folder.parent/"cap_sweep_7_to_12/cycle_12_7.csv", delimiter=",", names=True)
axes[0,1].plot(1e6*wave["time_s"]-400, (wave["outp"]+wave["outn"])/2, color="#25785e",
               label="Telescopic OTA")
ref = reference[reference["cn_pf"] == 7]
axes[1,0].plot(ref["cp_pf"], 1e3*ref["out_diff_v"], "s-", color="#25785e", label="Telescopic OTA")
ref = reference[reference["cp_pf"] == reference["cn_pf"]]
axes[1,1].plot(ref["cp_pf"], ref["out_cm_v"], "s-", color="#25785e", label="Telescopic OTA")
for ax, ylabel in zip(axes[0], ("Branch voltage (V)", "Output common-mode (V)")):
    ax.axvline(80, color="0.4", ls=":", label="Sample")
    ax.set(xlabel="Time within fifth cycle (µs)", ylabel=ylabel, xlim=(36,94))
axes[0,0].set_title("Direct outputs at 12/7 pF")
axes[0,1].set_title("Common-mode at 12/7 pF")
axes[1,0].set(xlabel="CP (pF), CN held at 7 pF", ylabel="Sampled OUTP − OUTN (mV)")
axes[1,1].set(xlabel="Equal branch capacitance (pF)", ylabel="Sampled output common-mode (V)")
for ax in axes.flat:
    ax.grid(alpha=.22)
    ax.legend(fontsize=8)
fig.suptitle("10 kHz SC readout | direct output and telescopic OTA comparison")
fig.savefig(folder/"passive_outputs.png", dpi=175)
fig.savefig(folder/"passive_outputs.pdf")
