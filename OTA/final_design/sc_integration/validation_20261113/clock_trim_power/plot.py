"""Compare the programmed timing and integrated power to the previous prototype."""
from pathlib import Path
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'clock_reference_scl08/results.csv'


def entries(path):
    with path.open() as f:
        return {r['case']:r for r in csv.DictReader(f) if r.get('status','ok')=='ok'}


def main():
    clock=entries(HERE/'clock.csv')
    integrated=entries(HERE/'integrated.csv')
    prior=entries(PRIOR)
    fig,ax=plt.subplots(1,2,figsize=(12.3,5),layout='constrained')
    fig.suptitle('SCL08 readout · physical clock trim and reduced-power reference',fontweight='bold',fontsize=16)
    for i,r in enumerate(clock.values()):
        start,end=(float(r[key]) for key in ('track_on_us','track_off_us'))
        if np.isfinite([start,end]).all():
            ax[0].plot([start,end],[i,i],lw=6,solid_capstyle='round',c='#255aa4')
    ax[0].axvspan(70,80,color='#188675',alpha=.09)
    ax[0].set(yticks=range(len(clock)),yticklabels=[f'{r["code"]} · {r["mos"]}, {r["vdd"]} V, {r["temp"]} °C' for r in clock.values()],
              xlabel='Time within cycle (µs)',title='Track window with trim code selected')
    ax[0].invert_yaxis()
    pairs=[('Cold','bypass_cold_12_7','integrated0_7'),('Nominal','bypass_12_7','integrated3_7'),
           ('Hot','bypass_hot_12_12','integrated5_12')]
    x=0
    xticks=[]
    labels=[]
    for label,old,new in pairs:
        if new not in integrated:
            continue
        for delta,row,columns,name in ((0,prior[old],('clock_mW','buffer_mW','total_mW'),'Prior'),
                                      (.37,integrated[new],('clock_mw','buffer_mw','total_mw'),'Revised')):
            clock_mw,ref,total=(float(row[key]) for key in columns)
            ax[1].bar(x+delta,clock_mw,.33,color='#2455a6',label='Clock' if x==0 and delta==0 else None)
            ax[1].bar(x+delta,ref,.33,bottom=clock_mw,color='#177f70',label='Reference' if x==0 and delta==0 else None)
            ax[1].bar(x+delta,max(0,total-clock_mw-ref),.33,bottom=clock_mw+ref,color='#b46932',label='SC and OTA' if x==0 and delta==0 else None)
            xticks.append(x+delta)
            labels.append(label+'\n'+name)
        x+=1
    ax[1].set(xticks=xticks,xticklabels=labels,ylabel='Average supply power (mW)',title='Integrated power at 10 kHz')
    ax[1].legend(fontsize=9)
    for p in ax:
        p.grid(alpha=.22)
        p.spines[['top','right']].set_visible(False)
    fig.savefig(HERE/'trim_power.png',dpi=160)

if __name__=='__main__':
    main()
