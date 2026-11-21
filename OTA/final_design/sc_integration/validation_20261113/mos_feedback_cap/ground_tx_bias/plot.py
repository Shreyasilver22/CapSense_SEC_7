"""Plot ground-TX switching waveforms and the OTA current trade-off."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent


def read(name):
    return np.genfromtxt(folder / name, delimiter=",", names=True)


rows = read("summary.csv")
fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
for current in (2.5, 3.5, 4.5, 7, 9):
    wave = read(f"wave_{current:g}u_12_12.csv")
    for ax, key in ((axes[0, 0], "input_cm_v"), (axes[0, 1], "output_cm_v")):
        ax.plot(wave["time_us"], wave[key], label=f"{current:g} µA")
for ax, label in zip(axes[0], ("OTA input common-mode (V)", "SC output common-mode (V)")):
    ax.set(xlim=(40, 65), xlabel="Time in cycle (µs)", ylabel=label)
axes[0, 0].axhline(0, ls=":", color=".4")
axes[0, 1].legend(fontsize=8)
axes[1, 0].plot(rows["iref_ua"], rows["settle_us"], "o-")
axes[1, 0].set(ylabel="Differential settling at 12/7 pF (µs)")
axes[1, 1].plot(rows["iref_ua"], rows["vdd_uw"], "s-", color="#a34832")
axes[1, 1].set(ylabel="Main-rail power at 12/7 pF (µW)")
for ax in axes[1]:
    ax.set_xlabel("OTA reference current (µA)")
for ax in axes.flat:
    ax.grid(alpha=.2)
fig.suptitle("TX transfer at ground | 40 pF PMOS feedback per branch")
fig.savefig(folder / "ground_tx_bias.pdf")
fig.savefig(folder / "ground_tx_bias.png", dpi=180)
