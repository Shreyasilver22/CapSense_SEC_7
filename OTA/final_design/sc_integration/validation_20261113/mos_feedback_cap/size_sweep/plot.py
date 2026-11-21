"""Plot sensitivity, sensor thermal noise, and common-mode headroom."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
results = np.genfromtxt(folder / "summary.csv", delimiter=",", names=True)
cf = results["nominal_cf_pf"]
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), layout="constrained")
for ax, field, label, color in (
    (axes[0, 0], "sensitivity_mv_per_pf", "Sensitivity (mV/pF)", "#235c91"),
    (axes[0, 1], "sensor_diff_rms_uv", "Output sensor noise (µV RMS)", "#a5532f"),
    (axes[1, 0], "sensor_equiv_rms_af", "Equivalent sensor noise (aF RMS)", "#157266"),
):
    ax.plot(cf, results[field], "o-", color=color)
    ax.set_ylabel(label)

ax = axes[1, 1]
ax.plot(cf, results["in_cm_min_12_12_v"], "o-", label="OTA input")
ax.plot(cf, results["out_cm_min_12_12_v"], "s-", label="SC output")
ax.set_ylabel("Minimum common-mode (V)")
ax.set_title("Switching transient at 12/12 pF")
ax.legend()

for ax in axes.flat:
    ax.axvline(cf[3], color=".6", ls=":", lw=1)
    ax.set_xlabel("Nominal PMOS feedback capacitance per branch (pF)")
    ax.grid(alpha=.23)
fig.suptitle("10 kHz SC readout with 2.5 V TX transfer level", fontweight="bold")
fig.savefig(folder / "pmos_feedback_size_sweep.pdf")
fig.savefig(folder / "pmos_feedback_size_sweep.png", dpi=180)
