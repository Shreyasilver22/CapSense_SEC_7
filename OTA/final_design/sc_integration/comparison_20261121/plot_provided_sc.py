"""Plot the sensor-network checks for the supplied drawing."""
import csv
from dataclasses import replace

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from compare import Case, ROOT, read_raw
from test_provided_sc import Trial

LABELS = {
    'negative_feedback': ('Floating common, separate outputs and negative feedback','#497084'),
    'sensor_common_grounded': ('Grounded common, no sensor reset','#af5129'),
    'sensor_reset_diagnostic': ('Grounded common with sensor reset','#087b73'),
}

def read(name):
    with (ROOT/f'provided_sc_{name}.csv').open() as stream:
        return [r for r in csv.DictReader(stream) if r['status']=='ok']


def main():
    rows = read('sweep') + read('sensor_reset_diagnostic')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,(cycle,sweep)=plt.subplots(1,2,figsize=(11.6,5.25))
    fig.subplots_adjust(left=.078,right=.974,top=.755,bottom=.22,wspace=.30)
    fig.text(.078,.94,'Capacitance response of the supplied SC circuit',fontsize=19,fontweight='bold',
             color='#193849',ha='left',va='top')
    fig.text(.078,.86,'SCL08 at 5 V  •  10 kHz  •  10 pF TX–RX capacitor on each branch',
             color='#536575',fontsize=11,ha='left',va='top')
    for key,(label,color) in LABELS.items():
        r=sorted([x for x in rows if x['wiring']==key and x['cycles']=='4'],
                 key=lambda x:float(x['cp_pF']))
        sweep.plot([float(x['cp_pF']) for x in r],[float(x['diff_80_mV']) for x in r],
                   color=color,marker='o',lw=2,label=label)
        t=Trial(key,10.5,cycles=4)
        c=Case('telescopic_C','typ',100,cycles=t.cycles,step=t.step,solver=t.solver)
        a=read_raw(ROOT/'benches'/t.name/'trace.raw',c)
        n=np.arange(1,5)
        diff=1e3*(a['v(outp)']-a['v(outn)'])
        cycle.plot(n,np.interp(80+100*(n-1),a['time']*1e6,diff),
                   label=label,color=color,marker='o',lw=2)
    cycle.set(title=r'Repeated samples at $C_P=10.5$ pF',xlabel='Clock cycle',
              ylabel='Differential output at 80 µs (mV)',xticks=[1,2,3,4])
    sweep.set(title='Capacitance response in cycle 4',xlabel=r'$C_P$ (pF) with $C_N=10$ pF',
              ylabel='Differential output at 80 µs (mV)')
    for a in (cycle,sweep):
        a.grid(alpha=.20)
        a.set_axisbelow(True)
    h,l=cycle.get_legend_handles_labels()
    fig.legend(h,l,loc='lower center',bbox_to_anchor=(.50,.025),ncols=2,frameon=False,fontsize=9)
    fig.savefig(ROOT/'provided_sc_results.png',dpi=180)
    plt.close(fig)
    for k in LABELS:
        r=sorted([x for x in rows if x['wiring']==k and x['cycles']=='4'],
                 key=lambda x:float(x['cp_pF']))
        a,b=r[0],r[-1]
        d=(float(b['diff_80_mV'])-float(a['diff_80_mV']))/(float(b['cp_pF'])-float(a['cp_pF']))
        print(k,'average mV/pF',d,'endpoints',a['diff_80_mV'],b['diff_80_mV'])
        for x in r:
            if float(x['cp_pF'])==10.5:
                print('80 us at 10.5 pF cycle1/cycle4',x['diff_first_80_mV'],x['diff_80_mV'])


if __name__=='__main__':
    main()

