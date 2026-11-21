"""Plot completed PVT and reference sweeps."""
from pathlib import Path
import csv
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

work = Path(sys.argv[1])
out = Path(__file__).resolve().parent

def load(name):
    with (work/f'{name}.csv').open() as f:
        return [r for r in csv.DictReader(f) if r['status'] == 'ok']

pvt, refs = load('pvt'), load('reference')
fig, axes = plt.subplots(2, 2, figsize=(12.5,8), layout='constrained')
fig.suptitle('SCL08 readout with 2.5 V TX discharge and RX precharge',fontsize=17,fontweight='bold')
plt.rcParams.update({'font.size':10})
axes[0,0].axhline(2.5,c='#7e8998',ls='--',lw=1)
colors = ('#2455a6','#12786a')
for j, ((cp,cn), color) in enumerate(zip(((12,7),(12,12)), colors)):
    subset = [r for r in pvt if r['cp']==str(cp) and r['cn']==str(cn)]
    for supply in (4.5,5.0,5.5):
        items = [r for r in subset if float(r['vdd'])==supply]
        x = supply + (-.06 if j==0 else .06)
        low = min(float(r['outcm_min']) for r in items)
        high = max(float(r['outcm_max']) for r in items)
        axes[0,0].plot([x,x], [low,high], color=color, marker='_', markersize=8, lw=3,
                       label=f'{cp}/{cn} pF' if supply == 4.5 else None)
        ys = [float(r['held_mv']) for r in items]
        axes[0,1].scatter([x]*len(items), ys, color=color, alpha=.6, s=18)
axes[0,0].set(title='Output common-mode envelope during transfer',
              xlabel='Supply (V)',ylabel='Output common-mode (V)',xticks=[4.5,5,5.5])
axes[0,0].legend()
axes[0,1].set(title='Held differential sample across PVT', xlabel='Supply (V)',
              ylabel='Differential sample (mV)',xticks=[4.5,5,5.5])
for j,(label, cap, split, color) in enumerate((
    ('Shared, no bypass',0,False,'#2455a6'),
    ('Shared, 100 pF bypass',100,False,'#a85b20'),
    ('Split, 100 pF bypass',100,True,'#147a68'),
)):
    rows = sorted((r for r in refs if r['cn']=='12' and int(r['pf'])==cap
                   and (r['split']=='True')==split), key=lambda r:int(r['ohms']))
    axes[1,0].loglog([int(r['ohms']) for r in rows],
                    [float(r['ref_switch_max_error_mv']) for r in rows],
                    color=color, marker=('o','s','^')[j], lw=1.7, label=label)
axes[1,0].set(title='Peak switch-reference error, 12/12 pF',xlabel='Modeled source resistance (Ω)',
              ylabel='Peak deviation from 2.5 V (mV)')
axes[1,0].legend(fontsize=9)
for r,color in zip(('ref_100_0_False_12_12','ref_1000_100_False_12_12','ref_1000_100_True_12_12'),
                   ('#2455a6','#a85b20','#147a68')):
    data=np.load(work/r/'wave.npz')
    resistance, capacitance, split=r.split('_')[1:4]
    label = f'{int(resistance):,} Ω · {capacitance} pF · '+ ('split' if split=='True' else 'shared')
    axes[1,1].plot(data['t'],1e3*(data['cm']-2.5),color=color,lw=1.7,label=label)
axes[1,1].set(title='Output common-mode with finite reference drive',
              xlabel='Time within the cycle (µs)',ylabel='Deviation from 2.5 V (mV)',xlim=(40,65))
axes[1,1].legend(fontsize=9)
for ax in axes.flat:
    ax.grid(alpha=.24)
    ax.spines[['top','right']].set_visible(False)
fig.savefig(out/'pvt_reference.png',dpi=160)

fig, axes = plt.subplots(2, 1, figsize=(10.5, 6), sharex=True, layout='constrained')
fig.suptitle('Worst confirmed hot corner · 5.5 V, 85 °C, 12/12 pF', fontsize=16, fontweight='bold')
for case, label, color in (
    ('stress_bnwp_5.5_85_12_12_0_0_False', '8 µs TX control · ideal reference', '#b45324'),
    ('slew_bnwp_5.5_85_12_20', '20 µs TX control · ideal reference', '#2455a6'),
    ('combined_bnwp_5.5_85_12_50', '20 µs TX control · 50 Ω reference', '#12786a'),
):
    wave = work / case / 'wave.npz'
    if not wave.exists():
        continue
    trace = np.load(wave)
    axes[0].plot(trace['t'], trace['cm'], label=label, color=color, lw=1.8)
    axes[1].plot(trace['t'], 1e3*trace['min_margin'], color=color, lw=1.8)
axes[0].axhline(2.5, color='#7e8998', ls='--', lw=1)
axes[1].axhline(0, color='#7e8998', ls='--', lw=1)
axes[0].set(ylabel='Output common-mode (V)', xlim=(40,70))
axes[1].set(xlabel='Time within the 10 kHz cycle (µs)', ylabel='Lowest saturation margin (mV)')
axes[0].legend()
for ax in axes:
    ax.grid(alpha=.24)
    ax.spines[['top','right']].set_visible(False)
fig.savefig(out/'hot_corner.png', dpi=160)
