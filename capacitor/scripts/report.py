from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import ROOT as R
j=json.loads((R/'results/catalog.json').read_text());caps=j['capacitors'];v=json.loads((R/'results/verification.json').read_text());main=[next(c for c in caps if c['value']==x) for x in ['2.5p','7.5p','3p']]
fig,axs=plt.subplots(1,3,figsize=(15,4))
x=np.arange(3);w=.25
for i,(key,label) in enumerate([('Cmut_F','Between plates'),('Ctop_sub_F','TOP to substrate'),('Cbot_sub_F','BOT to substrate')]):axs[0].bar(x+(i-1)*w,[c[key]*1e12 for c in main],w,label=label)
axs[0].set(xticks=x,xticklabels=[c['value'] for c in main],ylabel='Capacitance (pF)',title='Parasitics remain in both symbol types');axs[0].legend(fontsize=7)
axs[1].bar([c['value'] for c in main],[c['footprint_um2']/1e6 for c in main]);axs[1].set(ylabel='GDS bounding area (mm2)',title='Available layouts: area cost')
t=np.loadtxt(R/'results/cdac.dat',skiprows=1);axs[2].plot(t[:,0]*1e6,t[:,1]);axs[2].set(xlabel='Time (us)',ylabel='DAC node (V)',title='4-weight charge-sharing illustration')
for ax in axs:ax.grid(axis='y',alpha=.25)
fig.tight_layout();fig.savefig(R/'plots/usage_tradeoffs.png',dpi=180);fig.savefig(R/'plots/usage_tradeoffs.pdf');plt.close(fig)
table='| Requested | Units | Extracted mutual C | Error | GDS footprint | Layout |\n|---|---:|---:|---:|---|---|\n'
for c in caps:
 safe=c['value'].lower().replace('.','p').replace('+','').replace('-','m');table+=f"| {c['value']} | {c['units']} | {c['Cmut_F']*1e12:.8g} pF | {c['error_percent']:+.4f}% | {c['width_um']:g} x {c['height_um']:g} um | layouts/requested_{safe}.gds |\n"
(R/'CATALOG.md').write_text('# Prepared capacitor values and layouts\n\nEXPERIMENTAL extraction estimates, not silicon measurements. TOP/BOT are plate ports; SUB is the substrate reference.\n\n'+table+'\nThe requested 2.5p/7.5p pair uses 220/660 units for a nominal exact 3:1 mutual-capacitance ratio. This is not statistical matching qualification. Nearest independent rounding would use 659 units for 7.5p; the shipped pair intentionally prioritizes the nominal ratio. The larger target is +0.1792% above its requested value, like the smaller one.\n\nSubstrate capacitances and verification are in results/catalog.csv and verification.json. Footprint includes intra-array routing, excludes guard rings and chip surroundings. No common-centroid/dummy layout, conductor-resistance extraction, mismatch or PVT qualification is claimed.\n')
print('Usage plots and catalog written')
