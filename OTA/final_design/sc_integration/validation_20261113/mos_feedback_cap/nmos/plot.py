"""Plot NMOS capacitance and the SC comparison."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parent
cv = np.genfromtxt(root/"cv.csv", delimiter=",", names=True)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), layout="constrained")
axes[0].plot(cv["gate_minus_plate_v"], cv["isolated_f"]*1e15, label="Bulk tied to S/D")
axes[0].plot(cv["gate_minus_plate_v"], cv["grounded_mutual_f"]*1e15, label="Bulk at 0 V")
axes[0].set(xlabel="Gate minus S/D voltage (V)", ylabel="Gate-to-S/D mutual C (fF)",
            title="One 20 × 10 µm SCL08 NMOS")
for key,label in (("ideal","Ideal 40 pF"),("pmos","97 PMOS, gate at OUT"),
                  ("isolated_sum","169 NMOS, gate at SUM, isolated bulk"),
                  ("isolated_out","191 NMOS, gate at OUT, isolated bulk"),
                  ("grounded_sum","3,575 NMOS, gate at SUM, bulk at ground")):
    data=np.genfromtxt(root/f"wave_{key}_12_7.csv",delimiter=",",names=True)
    axes[1].plot(data["time_s"]*1e6-100,(data["outp"]-data["outn"])*1e3,label=label)
axes[1].axvline(80,color=".5",ls=":")
axes[1].set(xlabel="Time in SC cycle (µs)",ylabel="SC differential output (mV)",
            xlim=(40,90),title="12/7 pF sensor pair")
for ax in axes:
    ax.legend(fontsize=8)
    ax.grid(alpha=.25)
fig.savefig(root/"nmos_comparison.pdf")
fig.savefig(root/"nmos_comparison.png",dpi=180)
