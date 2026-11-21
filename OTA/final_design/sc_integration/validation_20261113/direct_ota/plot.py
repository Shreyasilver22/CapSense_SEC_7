"""Show the SC voltages arriving at the OTA and its open-loop response."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
fig, axes = plt.subplots(3, 2, figsize=(11, 9), layout="constrained", sharex=True)
for row, (mode, label) in zip(axes, (
        ("literal", "SC switches and capacitors"),
        ("precharged", "Passive SC with 2.5 V reset"),
        ("active_sc", "Existing SC readout feeding a second OTA"))):
    data = np.genfromtxt(folder / f"wave_{mode}_12_7.csv", delimiter=",", names=True)
    time = data["time_s"] * 1e6 - 400
    for ax, nodes, ylabel in zip(row, (("outp", "outn"), ("amp_p", "amp_n")),
                                 ("OTA input (V)", "OTA output (V)")):
        for node, color, polarity in zip(nodes, ("#17659b", "#b54034"), ("+", "−")):
            ax.plot(time, data[node], label=polarity, color=color)
        ax.axvline(80, ls=":", color="0.4", label="Sample")
        ax.set(ylabel=ylabel, xlim=(38, 93), title=label)
        ax.grid(alpha=.22)
        ax.legend(loc="best")
for ax in axes[-1]:
    ax.set_xlabel("Time in fifth cycle (µs)")
fig.suptitle("SC outputs connected directly to the telescopic OTA | 12 pF / 7 pF")
fig.savefig(folder/"direct_ota.png", dpi=180)
fig.savefig(folder/"direct_ota.pdf")
