"""Plot the effect of OTA reference current on the SC interface."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
rows = np.genfromtxt(root/"summary.csv",delimiter=",",names=True)
r = rows[(rows["vbn_v"]==3)&(rows["vbp_v"]==2.8)]
r.sort(order="iref_ua")
n = np.genfromtxt(root/"ota_noise_summary.csv",delimiter=",",names=True)
fig, axes = plt.subplots(2, 2, figsize=(10,6.8),layout="constrained")
for ax, y, label, color in (
    (axes[0,0],r["sensitivity_mv_per_pf"],"SC sensitivity (mV/pF)","#255c94"),
    (axes[0,1],r["settle_us"],"Differential settling (µs)","#167868"),
    (axes[1,0],r["vdd_power_uw"],"SC and OTA VDD power (µW)","#aa5635"),
):
    ax.plot(r["iref_ua"],y,"o-",color=color)
    ax.set_ylabel(label)
    if ax is axes[0,0]:
        ax.ticklabel_format(axis="y",style="plain",useOffset=False)
axes[1,1].plot(n["iref_ua"],n["noise_1e06hz_nv_rt_hz"],"o-",color="#76518e")
axes[1,1].set_ylabel("Standalone OTA noise at 1 MHz (nV/√Hz)")
for ax in axes.flat:
    ax.set_xlabel("OTA reference current (µA)")
    ax.axvline(3.5,color=".55",ls=":",lw=1)
    ax.grid(alpha=.22)
fig.suptitle("OTA bias sweep with 40 pF PMOS feedback banks | 10 kHz SC")
fig.savefig(root/"ota_bias_sweep.pdf")
fig.savefig(root/"ota_bias_sweep.png",dpi=180)
