"""Plot the nominal timing screen and sampled errors at selected corners."""
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
with (folder / "timing.csv").open() as f:
    rows = [{k: float(v) for k, v in row.items() if k != "model"}
            for row in csv.DictReader(f)]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
for lead in (1, 2, 3):
    balanced = [r for r in rows if r["lead_us"] == lead and r["cn_pf"] == 12]
    signal = [r for r in rows if r["lead_us"] == lead and r["cn_pf"] == 7]
    axes[0].plot([r["edge_us"] for r in balanced], [r["min_rx_v"] for r in balanced],
                 "o-", label=f"{lead} µs RX lead")
    axes[1].plot([r["edge_us"] for r in signal], [r["settle_us"] for r in signal],
                 "o-", label=f"{lead} µs RX lead")
axes[0].set(ylabel="Lowest RX voltage (V)", title="12/12 pF sensors")
axes[0].axhline(0, ls=":", color=".4")
axes[1].set(ylabel="Differential settling from TX command (µs)", title="12/7 pF sensors")
axes[1].axhline(34, ls=":", color=".4", label="Time to sample")
for ax in axes:
    ax.set_xlabel("TX switch-control rise time (µs)")
    ax.set_xticks((1, 2, 4, 8))
    ax.legend(fontsize=8)
    ax.grid(alpha=.25)
fig.suptitle("SC timing sweep | 0 V TX transfer, 50 pF PMOS feedback, 4.5 µA OTA bias")
fig.savefig(folder / "timing_screen.pdf")
