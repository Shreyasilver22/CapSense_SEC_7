"""Plot the nominal sensitivity matrix and input common-mode waveforms."""
from pathlib import Path
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from sweep_sensitivity import OUT, Case, read_raw

def rows(name):
    return list(csv.DictReader((OUT/name).open()))


def main():
    matrix=rows('nominal_summary.csv')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,(a,b)=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
    colors=('#276276','#a35836','#098475')
    for cs,c in zip((10,20,40),colors):
        r=sorted([x for x in matrix if float(x['cs_pF'])==cs],key=lambda x:int(x['cfb_pmos_units']))
        n=np.array([int(x['cfb_pmos_units']) for x in r])
        y=np.array([float(x['avg_sensitivity_mV_pF']) for x in r])
        stable=np.array([int(x['settled_cases'])==int(x['total_cases']) for x in r])
        a.plot(n,np.where(stable,y,np.nan),marker='o',color=c,label=f'{cs} pF TX–RX',lw=1.8)
        a.scatter(n[~stable],y[~stable],color=c,marker='x',s=65)
    a.set(xlabel='Feedback PMOS units per branch',ylabel='Endpoint sensitivity (mV/pF)',
          title='Feedback and TX–RX capacitor sweep',xticks=[40,60,84,121])
    a.axhline(34.62,ls=':',lw=1,color='#536170')
    a.legend(fontsize=8,loc='upper right')
    a.text(.11,.06,'×  One or both endpoints missed the sample',transform=a.transAxes,
           fontsize=8,color='#46535d')
    names=[(Case(10,121,7.82).name,'Baseline',colors[0]),
           (Case(20,60,7.82).name,'20 pF, 60 units',colors[1])]
    for rx in (15,30):
        name=Case(20,60,7.82).name+f'_rxr{rx}k'
        if (OUT/name/'trace.raw').exists():
            names.append((name,f'20 pF, 60 units + {rx} kΩ RX',
                          '#078774' if rx==15 else '#7974a5'))
    for name,label,col in names:
        try:
            w=read_raw(OUT/name/'trace.raw')
        except (OSError,ValueError):
            continue
        t=w['time']*1e6-300
        icm=(w['v(sump)']+w['v(sumn)'])/2
        use=(t>=40)&(t<=54)
        b.plot(t[use],icm[use],label=label,color=col,lw=1.6)
    b.set(xlabel='Time in 10 kHz cycle (µs)',ylabel='OTA input common-mode (V)',
          title=r'Input during switching at $C_P=7.82$ pF')
    b.legend(fontsize=7,loc='lower right')
    for ax in (a,b):
        ax.grid(alpha=.22)
        ax.set_axisbelow(True)
    fig.suptitle('SCL08 SC readout sensitivity and switching headroom',fontsize=15,fontweight='bold')
    fig.savefig(OUT/'sensitivity_tradeoffs.png',dpi=180)
    plt.close(fig)

if __name__=='__main__':
    main()

