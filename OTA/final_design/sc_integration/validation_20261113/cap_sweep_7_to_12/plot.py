"""Plot the capacitance sweep and the clocked common-mode traces."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

folder = Path(__file__).resolve().parent
sweep = np.genfromtxt(folder / "sweep.csv", delimiter=",", names=True)
fig, axes = plt.subplots(2, 3, figsize=(13, 7.2), layout="constrained")
for ax, key, scale, title, unit, color in zip(
        axes[0], ("out_diff_v", "in_cm_v", "out_cm_v"), (1000, 1, 1),
        ("Differential output", "OTA input common-mode", "OTA output common-mode"),
        ("mV", "V", "V"), ("RdBu_r", "viridis", "viridis")):
    values = (sweep[key] * scale).reshape(6, 6).T
    norm = TwoSlopeNorm(0) if key == "out_diff_v" else None
    chart = ax.imshow(values, origin="lower", extent=(6.5,12.5,6.5,12.5),
                      cmap=color, norm=norm)
    for y, row in enumerate(values, 7):
        for x, val in enumerate(row, 7):
            rgb = chart.cmap(chart.norm(val))[:3]
            brightness = np.dot(rgb, [0.2126, 0.7152, 0.0722])
            digits = 1 if scale == 1000 else 3
            ax.text(x, y, f"{val:.{digits}f}", color="black" if brightness > .53 else "white",
                    ha="center", va="center", fontsize=8)
    ax.set(title=f"{title} ({unit})", xlabel="CP (pF)", ylabel="CN (pF)",
           xticks=range(7,13), yticks=range(7,13))
    fig.colorbar(chart, ax=ax, shrink=.77)
for cp, cn in ((7,7), (12,7), (7,12), (12,12)):
    data = np.genfromtxt(folder / f"cycle_{cp}_{cn}.csv", delimiter=",", names=True)
    time = data["time_s"]*1e6 - 400
    for ax, values in zip(axes[1], (1000*(data["outp"]-data["outn"]),
                                    (data["sump"]+data["sumn"])/2,
                                    (data["outp"]+data["outn"])/2)):
        ax.plot(time, values, label=f"{cp}/{cn} pF")
for ax, label in zip(axes[1], ("Differential output (mV)", "Input common-mode (V)",
                              "Output common-mode (V)")):
    ax.axvline(80, ls="--", color="0.25", lw=1)
    ax.set(xlabel="Time in fifth cycle (µs)", ylabel=label, xlim=(39,91))
    ax.grid(alpha=.25)
axes[1,0].legend(fontsize=8)
fig.suptitle("Final telescopic OTA and 10 kHz SC readout | sample at 80 µs", fontsize=14)
fig.savefig(folder / "capacitance_sweep.png", dpi=180)
fig.savefig(folder / "capacitance_sweep.pdf")
