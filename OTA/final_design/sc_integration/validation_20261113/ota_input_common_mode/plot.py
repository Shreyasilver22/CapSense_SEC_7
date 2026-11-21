"""Plot nominal common-mode and low-end saturation checks."""
from pathlib import Path
import csv
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

work = Path(sys.argv[1])
out = Path(__file__).resolve().parent

def load(group, measurement):
    with (work/f'{group}_{measurement}.csv').open() as f:
        return [r for r in csv.DictReader(f) if r['status']=='ok' and float(r['iref_uA'])==4.5]

def field(rows, name):
    return np.array([float(r[name]) for r in rows])

ac=sorted(load('nominal','ac')+load('boundary','ac'),key=lambda r:float(r['input_cm_V']))
lo=[r for r in ac if .6<=float(r['input_cm_V'])<=1.5]
tran=load('nominal','transient')
fig, axes = plt.subplots(2,2,figsize=(12,7.8),layout='constrained')
fig.suptitle('Final SCL08 OTA · input common-mode sweep',fontsize=18,fontweight='bold')
gain, tail, timing, response = axes.flat
vx=field(ac,'input_cm_V')
gain.plot(vx,field(ac,'gain_db'),c='#2455a6',lw=2)
gain.axvspan(.6,1.5,color='#4266a0',alpha=.09)
gain.set(xlabel='Input common-mode (V)',ylabel='Low-frequency gain (dB)',title='Differential open-loop gain at 0.01 Hz',xlim=(.5,3.2))

vlow=field(lo,'input_cm_V')
tail.plot(vlow,field(lo,'tail_min_margin_mV'),c='#ad551e',lw=2,label='Tail margin')
tail.axhline(0,c='#6e7583',lw=1)
tail.axvline(1.122,c='#6e7583',ls='--',lw=1)
tail.set(xlabel='Input common-mode (V)',ylabel='Tail saturation margin (mV)',title='Tail bias at 4.5 µA reference current')
tail2=tail.twinx()
tail2.plot(vlow,field(lo,'tail_mean_current_uA'),c='#147b6d',lw=2)
tail2.set_ylabel('Tail drain current (µA)',color='#147b6d')
tail2.tick_params(axis='y',colors='#147b6d')

for step,color in ((.1,'#2455a6'),(.25,'#ad551e')):
    rows=sorted((r for r in tran if float(r['input_cm_V'])<=1.5 and float(r['output_step_per_side_V'])==step),
                key=lambda r:float(r['input_cm_V']))
    y=field(rows,'worst_settle_us')
    x=field(rows,'input_cm_V')
    timing.semilogy(x,y,marker='o',ms=4,color=color,label=f'{step:g} V step per output')
    fail=~np.isfinite(y)
    timing.scatter(x[fail],np.full(fail.sum(),40),marker='x',color=color)
timing.axhline(40,c='#6e7583',ls='--',lw=1)
timing.set(xlabel='Input common-mode (V)',ylabel='Settling time (µs)',title='Both outputs within 0.1% · × missed 40 µs')
timing.legend(fontsize=9)

for v,color in ((.6,'#aa432b'),(.7,'#b37919'),(.8,'#168577'),(1.5,'#2455a6')):
    p=work/f'tran_tntp_5_27_typ_cm{v:.2f}_i4.5_step0.1_dt20'/'tran.dat'
    a=np.loadtxt(p,skiprows=1)
    t=a[:,0]*1e6-10
    m=(t>=-.5)&(t<=25)
    response.plot(t[m],1e3*(a[m,1]-a[m,2]),color=color,lw=1.8,label=f'{v:g} V input CM')
response.axhline(100,c='#6e7583',ls='--',lw=1)
response.set(xlabel='Time after step (µs)',ylabel='Differential output (mV)',title='Small-step response')
response.legend(fontsize=8)
for ax in axes.flat:
    ax.grid(alpha=.24)
    ax.spines[['top','right']].set_visible(False)
fig.savefig(out/'input_common_mode.png',dpi=160)
