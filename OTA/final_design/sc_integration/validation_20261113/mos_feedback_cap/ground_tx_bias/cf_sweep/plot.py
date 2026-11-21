"""Plot feedback capacitor sizing at 0 V TX."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
rows = np.genfromtxt(folder/"summary.csv",delimiter=",",names=True)
cf = rows["nominal_cf_pf"]
fig, axes = plt.subplots(2,2,figsize=(10.5,7),layout="constrained")
axes[0,0].plot(cf,rows["sensitivity_mv_pf"],"o-",color="#255c94")
axes[0,0].set(ylabel="Local sensitivity (mV/pF)",title="Signal near 12/7 pF")
axes[0,1].plot(cf,rows["sensor_noise_af"],"o-",color="#137768")
axes[0,1].set(ylabel="Sensor noise (aF RMS)",title="Referred to capacitance")
axes[1,0].plot(cf,rows["balanced_min_rx_v"],"o-",label="Lowest RX")
axes[1,0].plot(cf,rows["balanced_min_in_cm_v"],"s-",label="Lowest OTA input average")
axes[1,0].axhline(0,color=".4",ls=":")
axes[1,0].set(ylabel="Minimum voltage (V)",title="Switching excursion at 12/12 pF")
axes[1,0].legend()
axes[1,1].semilogy(cf,rows["balanced_junction_charge_fc"],"o-",color="#9b4f2c")
axes[1,1].set(ylabel="Integrated junction current (fC)",title="RX junctions at 12/12 pF")
for ax in axes.flat:
    ax.set_xlabel("Nominal feedback capacitance per branch (pF)")
    ax.axvline(cf[2],color=".5",ls=":")
    ax.grid(alpha=.22)
fig.suptitle("0 V TX transfer | 4.5 µA OTA reference current | 10 kHz")
fig.savefig(folder/"ground_tx_cf_sweep.pdf")
fig.savefig(folder/"ground_tx_cf_sweep.png",dpi=180)
