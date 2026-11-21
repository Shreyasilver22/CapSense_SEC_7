"""Plot the saved SC sweep, one nominal clock cycle, and held-phase noise."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
def read(name):
    return np.genfromtxt(folder / name, delimiter=",", names=True)

sweep = read("sampled_results.csv")
delta = sweep[:9]
wave = read("nominal_last_cycle.csv")
noise = read("noise_cp7_cn5.csv")
fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
ax = axes[0,0]
ax.plot(delta["delta_pf"], 1e3*delta["ideal_diff_v"], "--", label="Ideal charge balance")
ax.plot(delta["delta_pf"], 1e3*delta["out_diff_v"], "o", label="ngspice at 80 µs")
ax.set(xlabel="Capacitance difference (pF)", ylabel="Differential output (mV)",
       title="Sensitivity at 12 pF total capacitance")
ax.legend()
ax = axes[0,1]
total = sweep[(sweep["delta_pf"] == 0)]
total = np.sort(total, order="total_pf")
ax.plot(total["total_pf"], total["in_cm_v"], "o-", label="OTA input CM")
ax.plot(total["total_pf"], total["out_cm_v"], "s-", label="OTA output CM")
ax.set(xlabel="Total capacitance (pF), balanced branches", ylabel="Sampled common-mode (V)",
       title="Common-mode versus total sensor capacitance")
ax.legend()
ax = axes[1,0]
time = 1e6*wave["time_s"]-400
ax.plot(time, (wave["sump"]+wave["sumn"])/2, label="OTA input CM")
ax.plot(time, (wave["outp"]+wave["outn"])/2, label="OTA output CM")
ax.axvline(80, color="0.35", ls="--", label="Sample")
ax.set(xlabel="Time within cycle (µs)", ylabel="Common-mode (V)",
       title="Switching and recovery, 7 pF / 5 pF")
ax.legend()
ax = axes[1,1]
for name, label in (("differential", "Output differential"), ("output_cm", "Output CM"),
                    ("input_cm", "Input CM")):
    ax.loglog(noise["frequency_hz"], noise[f"{name}_v_per_sqrt_hz"]*1e9, label=label)
ax.set(xlabel="Frequency (Hz)", ylabel="Noise density (nV/√Hz)",
       title="Held transfer phase, 7 pF / 5 pF")
ax.legend()
for ax in axes.flat:
    ax.grid(alpha=.22)
fig.savefig(folder/"sc_ota_results.png", dpi=180)
fig.savefig(folder/"sc_ota_results.pdf")
