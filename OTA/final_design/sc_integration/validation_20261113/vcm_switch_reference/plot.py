"""Compare reference choices using the simulated last cycle and capacitance grid."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parent


def read(name):
    return np.genfromtxt(root / name, delimiter=",", names=True, dtype=None, encoding=None)


fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
for mode, label, color in (
        ("original", "Both at ground", "#a44738"), ("rx_only", "RX clamp at 2.5 V", "#2775a7"),
        ("tx_only", "TX discharge at 2.5 V", "#795294"), ("both", "Both at 2.5 V", "#17715b")):
    w = read(f"wave_{mode}_12_12.csv")
    for ax, a, b in ((axes[0,0], "sump", "sumn"), (axes[0,1], "outp", "outn")):
        ax.plot(w["time_us"], (w[a]+w[b])/2, label=label, color=color)
    w = read(f"wave_{mode}_12_7.csv")
    axes[1,0].plot(w["time_us"], 1000*(w["outp"]-w["outn"]), color=color)
    axes[1,1].plot(w["time_us"], -1e6*w["iref_a"], color=color)
for ax in axes.flat:
    ax.axvline(80, ls=":", color=".4")
    ax.set(xlim=(39,93), xlabel="Time within 10 kHz cycle (µs)")
    ax.grid(alpha=.22)
axes[0,0].set(ylabel="Input common-mode (V)", title="OTA input average, CP/CN = 12/12 pF")
axes[0,1].set(ylabel="Output common-mode (V)", title="SC output average, CP/CN = 12/12 pF")
axes[0,0].legend(fontsize=8)
axes[1,0].set(ylabel="Differential output (mV)", title="SC signal, CP/CN = 12/7 pF")
axes[1,1].set(ylabel="Reference current into circuit (µA)", title="2.5 V reference load, CP/CN = 12/7 pF")
fig.suptitle("Replacing the SC switch ground references with 2.5 V")
for ext in ("pdf", "png"):
    fig.savefig(root/f"vcm_switch_comparison.{ext}", dpi=180)
