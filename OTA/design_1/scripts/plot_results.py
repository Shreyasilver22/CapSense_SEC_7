from pathlib import Path
import os
os.environ['MPLCONFIGDIR']='/tmp/ota_matplotlib'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).resolve().parent.parent
out=p/'results'/'plots';out.mkdir(exist_ok=True)
a=np.loadtxt(p/'results/ac.dat',skiprows=1);d=np.loadtxt(p/'results/dc.dat',skiprows=1);t=np.loadtxt(p/'results/transient.dat',skiprows=1)
plt.rcParams.update({'font.size':11,'axes.grid':True,'grid.alpha':.25,'figure.dpi':140})
foot='SCL08 nominal model • 5 V • 27 °C • CL = Cc = 5 pF\nProvisional: ngspice ignores some HSPICE model parameters; no extracted layout parasitics.'
def save(fig,name):
 fig.text(.5,.015,foot,ha='center',fontsize=8,color='#555555');fig.tight_layout(rect=(0,.075,1,.96))
 fig.savefig(out/(name+'.png'),dpi=180);fig.savefig(out/(name+'.pdf'));plt.close(fig)
f,ax=plt.subplots(2,1,figsize=(9,7),sharex=True)
ax[0].semilogx(a[:,0],a[:,1],color='#1864ab',lw=2);ax[0].axhline(0,color='gray',ls='--');ax[0].set_ylabel('Gain (dB)');ax[0].set_title('OTA open-loop frequency response')
ugf=1.554635e6
for x in ax:x.axvline(ugf,color='#d9480f',ls='--',alpha=.8)
ax[0].text(.04,.12,'Low-frequency gain: 35.57 dB\nUnity-gain crossing: 1.55 MHz',transform=ax[0].transAxes)
ax[1].semilogx(a[:,0],a[:,2],color='#1864ab',lw=2);ax[1].axhline(-180,color='gray',ls='--');ax[1].plot(ugf,-118.6105,'o',color='#d9480f');ax[1].set_ylabel('Unwrapped phase (degrees)');ax[1].set_xlabel('Frequency (Hz)');ax[1].text(.04,.12,'Estimated phase margin: 61.39°\nAt equal-input open-loop operating point',transform=ax[1].transAxes)
save(f,'01_gain_phase')
f,ax=plt.subplots(figsize=(9,5));ax.plot(d[:,0]*1e3,d[:,1],lw=2);ax.axvline(0,color='gray',ls='--');ax.axhline(3.276283,color='gray',ls=':');ax.set(xlabel='Differential input, Vin+ − Vin− (mV)',ylabel='Output voltage (V)',title='OTA DC differential transfer — VCM = 2.5 V');ax.text(.04,.82,'Vout at zero differential input: 3.276 V\nLocal sweep only: ±10 mV',transform=ax.transAxes);save(f,'02_dc_transfer')
f,ax=plt.subplots(2,1,figsize=(9,7),sharex=True);us=t[:,0]*1e6
ax[0].plot(us,t[:,1],label='Input',color='#555555',ls='--',lw=2);ax[0].plot(us,t[:,2],label='Output',color='#1864ab',lw=1.8);ax[0].set(ylabel='Voltage (V)',title='Unity-gain follower — 100 mV input step');ax[0].legend()
ax[1].plot(us,(t[:,2]-t[:,1])*1e3,color='#d9480f');ax[1].axhline(0,color='gray',ls='--');ax[1].set(xlabel='Time (µs)',ylabel='Output − input (mV)');save(f,'03_follower_step')
f,ax=plt.subplots(figsize=(9,5));m=(us>=19)&(us<=25);ax.plot(us[m],t[m,1],label='Input',ls='--',color='#555555',lw=2);ax.plot(us[m],t[m,2],label='Output',color='#1864ab',lw=2);ax.set(xlabel='Time (µs)',ylabel='Voltage (V)',title='Follower rising-edge detail');ax.legend();save(f,'04_step_detail')
print('\n'.join(str(x) for x in out.glob('*.png')))
