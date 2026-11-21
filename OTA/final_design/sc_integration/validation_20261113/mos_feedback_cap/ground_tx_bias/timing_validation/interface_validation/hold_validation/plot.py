"""Plot acquisition turn-off and the modeled sampled noise contributions."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parent
fig, axes = plt.subplots(1, 3, figsize=(12, 4.3), layout="constrained")
for cap, color in ((5,"#365b9a"),(10,"#187a68"),(20,"#ad542f")):
    wave = np.genfromtxt(root/f"wave_{cap}pf_0.5us.csv", delimiter=",", names=True)
    time = wave["time_us"]
    before = np.interp(79.73, time, wave["holdp"]-wave["holdn"])
    axes[0].plot(time, 1e3*(wave["holdp"]-wave["holdn"]-before), label=f"{cap} pF", color=color)
    axes[1].plot(time, (wave["holdp"]+wave["holdn"])/2, label=f"{cap} pF", color=color)
for ax, ylabel in zip(axes[:2], ("Held differential change (mV)", "Hold common-mode (V)")):
    ax.axvline(80, ls=":", color=".45")
    ax.set(xlabel="Time within cycle (µs)", ylabel=ylabel, xlim=(79.5,84))
    ax.legend()
n = np.genfromtxt(root/"noise_budget.csv", delimiter=",", names=True)
r = np.genfromtxt(root/"reset_noise.csv", delimiter=",", names=True)
for data, name in ((n["sensor_uv"],"Sensor"),(n["acquisition_ktc_uv"],"Acquisition"),
                   (r["reset_uv"],"Feedback reset"),(np.hypot(n["quadrature_uv"],r["reset_uv"]),"Combined estimate")):
    axes[2].plot(n["cap_pf"],data,"o-",label=name)
axes[2].set(xlabel="Hold capacitance per output (pF)",ylabel="Differential RMS noise (µV)",
            xticks=(5,10,20))
axes[2].legend(fontsize=8)
for ax in axes:
    ax.grid(alpha=.22)
fig.suptitle("10 kHz SC readout | acquisition switch opens around 80 µs")
fig.savefig(root/"hold_validation.pdf")
fig.savefig(root/"hold_validation.png",dpi=180)
