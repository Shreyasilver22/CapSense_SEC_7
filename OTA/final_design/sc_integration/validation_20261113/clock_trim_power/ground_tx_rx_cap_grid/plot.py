"""Render readout metrics over the full capacitor-pair grid."""
from pathlib import Path
import argparse
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np

from sweep import read_trace

parser=argparse.ArgumentParser()
parser.add_argument('results',type=Path)
parser.add_argument('--waveforms',type=Path,
                    help='Directory with cp12_cn07 and cp15_cn15 10 ns runs')
args=parser.parse_args()
out=Path(__file__).resolve().parent
with args.results.open() as file:
    rows=list(csv.DictReader(file))

def grid(key, transform=lambda value:value):
    values=np.full((15,15),np.nan)
    for r in rows:
        if r['status']=='ok':
            values[int(r['cn_pF'])-1,int(r['cp_pF'])-1]=transform(float(r[key]))
    return values

plt.rcParams.update({'font.family':'Lato','font.size':10.5})
fig, axs=plt.subplots(2,2,figsize=(10.9,9.1),layout='constrained')
fig.suptitle('Grounded TX discharge and RX precharge',fontsize=21,
             fontweight='bold',color='#132840')
entries=[
    ('Minimum OTA input common-mode during transfer','V',grid('input_transfer_cm_min_V'),'viridis',False),
    ('OTA input common-mode at 81 µs','V',grid('input_cm_at_81us_V'),'viridis',False),
    ('Held differential output at 81 µs','mV',grid('held_diff_at_81us_mV'),'RdBu_r',True),
    ('Held common-mode error at 81 µs','mV vs 2.5 V',grid('held_cm_at_81us_V',lambda x:1000*(x-2.5)),'magma',False),
]
for i,(ax,(title,unit,values,cmap,diverge)) in enumerate(zip(axs.flat,entries)):
    norm = TwoSlopeNorm(vmin=-np.nanmax(np.abs(values)),vcenter=0,
                        vmax=np.nanmax(np.abs(values))) if diverge else None
    image=ax.imshow(values,origin='lower',extent=(.5,15.5,.5,15.5),
                    cmap=cmap,norm=norm,interpolation='nearest',aspect='equal')
    ax.set(title=title,xlabel='$C_P$ (pF)',ylabel='$C_N$ (pF)',
           xticks=[1,3,5,7,9,11,13,15],yticks=[1,3,5,7,9,11,13,15])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if i<2 and np.nanmin(values)<1.5<np.nanmax(values):
        contour=ax.contour(range(1,16),range(1,16),values,levels=[1.5],
                           colors=['white'],linestyles=['--'],linewidths=1.3)
        ax.clabel(contour,fmt='1.50 V',fontsize=8,inline=True)
    fig.colorbar(image,ax=ax,shrink=.84,pad=.04,label=unit)
fig.savefig(out/'ground_cap_grid.png',dpi=180)
fig.savefig(out/'ground_cap_grid.pdf')

if args.waveforms:
    fig, axs = plt.subplots(2,1,figsize=(9.4,6.4),sharex=True,layout='constrained')
    fig.suptitle('Common-mode waveforms with grounded TX discharge and RX precharge',
                 fontsize=15,fontweight='bold',color='#132840')
    for ax, case, cp, cn in zip(axs,('cp12_cn07','cp15_cn15'),(12,15),(7,15)):
        t,sp,sn,op,on,hp,hn=read_trace(args.waveforms/case/'tight.raw').T
        for voltage,label,color in [((sp+sn)/2,'OTA input','#087e8b'),
                                    ((op+on)/2,'OTA output','#2858bd'),
                                    ((hp+hn)/2,'Held output','#b84b24')]:
            ax.plot(t*1e6,voltage,label=label,color=color,linewidth=1.2)
        ax.axhline(1.5,color='#727c8d',linestyle='--',linewidth=.8)
        ax.axvline(81,color='#727c8d',linestyle=':',linewidth=.9)
        ax.set(title=f'$C_P$ = {cp} pF, $C_N$ = {cn} pF',ylabel='Common-mode (V)',
               xlim=(40,83),ylim=(.3,2.83))
        ax.grid(axis='y',alpha=.16)
    axs[0].legend(loc='lower right',ncol=3)
    axs[-1].set_xlabel('Time (µs)')
    fig.savefig(out/'ground_cap_waveforms.png',dpi=180)
    fig.savefig(out/'ground_cap_waveforms.pdf')
