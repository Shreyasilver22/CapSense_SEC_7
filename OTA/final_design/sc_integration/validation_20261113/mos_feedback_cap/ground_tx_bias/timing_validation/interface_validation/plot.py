"""Plot the switched-load transient and feedback mismatch error."""
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parent
fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), layout="constrained")
for filename, label in (
    ("wave_load_0pf_2.5v_70us.csv", "SC alone"),
    ("wave_load_10pf_2.5v_70us.csv", "10 pF, precharge 2.5 V, track at 70 µs"),
    ("wave_load_10pf_5v_78us.csv", "10 pF, precharge 5 V, track at 78 µs"),
):
    data = np.genfromtxt(root/filename, delimiter=",", names=True)
    axes[0].plot(data["time_us"], 1e3*data["diff_v"], label=label)
    axes[1].plot(data["time_us"], data["ocm_v"], label=label)
for ax,y in zip(axes[:2],("SC differential (mV)","SC common-mode (V)")):
    ax.axvline(80, ls=":", color=".4", label="Evaluation at 80 µs")
    ax.set(xlabel="Time in second cycle (µs)",ylabel=y,xlim=(68,82))
axes[0].legend(fontsize=7)
rows = list(csv.DictReader((root/"results.csv").open()))
for cp,cn in ((12,12),(12,7),(7,12)):
    points = [r for r in rows if r["group"]=="banks" and float(r["cp"])==cp and float(r["cn"])==cn
              and r["sum_shunt_pf"]=="0" and int(r["p_units"])+int(r["n_units"])==242]
    axes[2].plot([(int(r["p_units"])-int(r["n_units"]))/121*100 for r in points],
                 [float(r["sc_error_mv"]) for r in points],"o-",label=f"CP/CN = {cp}/{cn} pF")
axes[2].set(xlabel="P−N feedback bank size difference (%)",ylabel="Change at sample (mV)")
axes[2].legend(fontsize=8)
for ax in axes:
    ax.grid(alpha=.23)
fig.suptitle("SC and telescopic OTA | ideal acquisition switch and feedback bank mismatch")
fig.savefig(root/"interface_screen.pdf")
fig.savefig(root/"interface_screen.png",dpi=180)
