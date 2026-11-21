from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
res=root/'results';out=root/'plots'
out.mkdir(exist_ok=True)
summary=json.loads((res/'summary.json').read_text())
teal='#007D7A';orange='#B15D35';navy='#173047';gray='#62798C'
plt.rcParams.update({'font.family':'Lato','font.size':12,'axes.spines.top':False,'axes.spines.right':False,
 'axes.grid':True,'grid.alpha':.17,'axes.titleweight':'bold','axes.titlecolor':navy})
def data(p):
 return np.loadtxt(p,skiprows=1)
fig,a=plt.subplots(2,2,figsize=(12,7.3),layout='constrained')
for folder,name,color in [('equal_inputs','Equal inputs, natural output bias',gray),
                          ('follower_ac_cm2.5','Follower DC operating point',teal)]:
 f,re_h,im_h=data(res/folder/'ac.dat').T
 h=re_h+1j*im_h
 a[0,0].semilogx(f,20*np.log10(abs(h)),color=color,lw=1.7,label=name)
 a[0,1].semilogx(f,np.unwrap(np.angle(h))*180/np.pi,color=color,lw=1.7)
a[0,0].axhline(0,lw=.8,ls=':',color=gray)
a[0,0].set(xlabel='Frequency (Hz)',ylabel='Open-loop gain (dB)',title='Voltage-gain response',xlim=(1,1e7),ylim=(-45,50))
a[0,0].legend(fontsize=8.4,frameon=False,loc='lower left')
a[0,1].set(xlabel='Frequency (Hz)',ylabel='Phase (°)',title='Phase of noninverting voltage response',xlim=(1,1e7),ylim=(-115,4))
for step,color in [(.1,teal),(2.,orange)]:
 t,vin,vout=data(res/f'follower_step_{step:g}/transient.dat').T
 target=next(r['attained_output_V'] for r in summary['transient'] if r['step_V']==step and r['edge']=='rise')
 select=(t>=9.5e-6)&(t<=31e-6)
 ax=a[1,0] if step==.1 else a[1,1]
 ax.plot((t[select]-10e-6)*1e6,vin[select],ls='--',color=gray,lw=1.2,label='Command')
 ax.plot((t[select]-10e-6)*1e6,vout[select],color=color,lw=1.8,label='Output')
 ax.axhline(target,ls=':',color=color,lw=.8)
 ax.set(xlabel='Time after rising edge (µs)',ylabel='Voltage (V)',title=f'{step:g} V follower step · 5 pF load')
 ax.legend(fontsize=9,frameon=False,loc='lower right')
fig.suptitle('Uploaded five-transistor OTA · VBN 0.8625 V · 5 V supply · 27 °C',fontsize=15,weight='bold',color=navy)
fig.savefig(out/'gm_ota_gain_and_settling.png',dpi=175,facecolor='white')
plt.close(fig)

fig,a=plt.subplots(1,2,figsize=(11.9,4.2),layout='constrained')
v,output=data(res/'dc_transfer/transfer.dat').T
a[0].plot((v-2.5)*1e3,output,color=teal,lw=1.8)
a[0].set(xlabel='SENSE − SP (mV)',ylabel='IOUT node voltage (V)',title='Open-loop DC voltage transfer')
scale,vid,io=data(res/'transconductance/gm_transfer.dat').T
a[1].plot(vid*1e3,io*1e6,color=teal,lw=1.8)
a[1].set(xlabel='SENSE − SP (mV)',ylabel='Current sunk into IOUT (µA)',title='Transconductance transfer · IOUT clamped at 2.5 V')
a[1].axhline(0,lw=.8,color=gray);a[1].axvline(0,lw=.8,color=gray)
fig.savefig(out/'gm_ota_dc_and_current_transfer.png',dpi=175,facecolor='white')
plt.close(fig)

with (res/'ac_summary.csv').open() as file:
 rows=[r for r in csv.DictReader(file) if r['case']=='Follower operating point']
x=[float(r['input_CM_V']) for r in rows]
fig,a=plt.subplots(1,2,figsize=(11.9,4.2),layout='constrained')
a[0].plot(x,[float(r['gain_dB']) for r in rows],color=teal,lw=1.8,marker='o')
a[1].plot(x,np.array([float(r['UGBW_Hz']) for r in rows])/1e3,color=teal,lw=1.8,marker='o')
for ax,title,y in [(a[0],'Gain versus follower DC input','Gain (dB)'),(a[1],'Unity-gain bandwidth versus bias','UGBW (kHz)')]:
 ax.set(xlabel='SP DC bias (V)',ylabel=y,title=title)
fig.savefig(out/'gm_ota_input_bias_sweep.png',dpi=175,facecolor='white')
