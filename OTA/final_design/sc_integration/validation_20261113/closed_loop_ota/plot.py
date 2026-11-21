"""Plot the unity-gain interface transient and resistor trade-off."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
def read(name):
    return np.genfromtxt(root / name, delimiter=",", names=True)

w = read("wave_12_7_500_13.3.csv")
r = read("scaled_screen.csv")
baseline = float(read("baseline.csv")["sc_diff_v"])
fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
ax = axes[0,0]
for p,n,name in (("outp","outn","SC output"),("amp_p","amp_n","Added OTA output")):
    ax.plot(w["time_us"], 1000*(w[p]-w[n]), label=name)
ax.set(ylabel="Differential voltage (mV)", title="Four 500 kΩ resistors, CP/CN = 12/7 pF")
ax = axes[0,1]
for p,n,name in (("outp","outn","SC output"),("amp_p","amp_n","Added OTA output")):
    ax.plot(w["time_us"], (w[p]+w[n])/2, label=name)
ax.set(ylabel="Common-mode voltage (V)", title="Common-mode during switching")
for ax in axes[0]:
    ax.axvline(80, ls=":", color="0.3", label="Sample")
    ax.set(xlim=(40,90), xlabel="Time in cycle (µs)")
    ax.legend()
ax = axes[1,0]
ax.plot(r["r_kohm"], 1000*r["sc_diff_v"], "o-", label="Loaded SC output")
ax.plot(r["r_kohm"], 1000*r["amp_diff_v"], "o-", label="Added OTA output")
ax.axhline(1000*baseline, color="0.3", ls=":", label="SC alone")
ax.set(ylabel="Sampled differential voltage (mV)", title="Output at 80 µs")
ax.legend()
ax = axes[1,1]
ax.plot(r["r_kohm"], r["amp_settle_us"], "o-")
ax.axhline(34, ls=":", color="0.3", label="Time to sample")
ax.set(ylabel="Time after TX starts (µs)", title="Settling to the 88 µs value")
ax.legend()
for ax in axes[1]:
    ax.set_xlabel("Resistance per resistor (kΩ)")
for ax in axes.flat:
    ax.grid(alpha=.22)
fig.savefig(root/"unity_feedback.png", dpi=180)
fig.savefig(root/"unity_feedback.pdf")
