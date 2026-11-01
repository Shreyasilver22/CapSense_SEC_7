from pathlib import Path
import subprocess,json,itertools,concurrent.futures,csv,shutil,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1]
PDK=Path('/home/berson_meshak/pdk/scl08/ngspice_models49')
ARCH=Path('/home/berson_meshak/final year project/ota/architecture_exploration_20261031')

def prepare():
 for f in ['models','results','plots','tb']:(R/f).mkdir(parents=True,exist_ok=True)
 for a in ['telescopic','gain_boosted','baseline']:
  shutil.copy2(ARCH/'models'/(a+'.spice'),R/'models'/(a+'.spice'))
 (R/'model_hashes.json').write_text(json.dumps({a:hashlib.sha256((R/'models'/(a+'.spice')).read_bytes()).hexdigest() for a in ['telescopic','gain_boosted','baseline']},indent=2))

def pwl(events,stop):
 events=sorted(events);return 'PWL('+' '.join(f'{t:.12g} {v}' for t,v in events+[(stop,events[-1][1])])+')'

def run(arch='layout_C',switch='ideal',fs=50000,delta=0,load=5,other_load=5,dt=10,mos='tntp49_5v',vdd=5,temp=27,vbn=2.4,method='trap'):
 T=1/fs;warm=50e-6;edge=10e-9;stop=warm+8*T;ev={'p1':[(0,0)],'p2':[(0,0)],'rst':[(0,vdd)]};samples=[]
 def toggle(k,start,end):ev[k]+=[(start,0),(start+edge,vdd),(end,vdd),(end+edge,0)]
 ev['rst'] += [(warm-.05*T,vdd),(warm-.05*T+edge,0)]
 for frame in [0,1]:
  base=warm+frame*4*T
  if frame:ev['rst'] += [(base-T+.02*T,0),(base-T+.02*T+edge,vdd),(base-.05*T,vdd),(base-.05*T+edge,0)]
  for k in range(3):
   t=base+k*T;toggle('p1',t+.02*T,t+.45*T);toggle('p2',t+.52*T,t+.95*T);samples.append((frame,k+1,t+.94*T,t+.52*T+edge,t+.95*T))
 name=f'{arch}_{switch}_{fs}_d{delta}_cl{load}_om{other_load}_{mos}_{vdd}_{temp}_dt{dt}_bn{vbn}_{method}'
 d=R/'results'/name;d.mkdir(parents=True,exist_ok=True)
 text=f'''SC same figure circuit, one output used: {name}
.include "{PDK}/mos/{mos}"
.include "{PDK}/res/typ/ppr"
.include "{R}/models/{arch}.spice"
.temp {temp}
.options reltol=1e-5 vntol=1e-8 abstol=1e-12 numdgt=12 method={method} maxord=2
VDD vdd 0 {vdd}
VREF ref 0 1.5
VP vp 0 0.3
IREF vdd bias 3.5u
CS tx rx {2.5+delta}p
CF sum out 7.5p
CL out 0 {load}p
'''
 text+=f'''VCM vcm 0 {vdd/2}
VBN vbn 0 {vbn}
VBP vbp vdd -2.2
XOTA ref sum out other vdd 0 bias vcm vbn vbp ota_telescopic_layout
COM other 0 {other_load}p
'''
 for k in ev:text+=f'V{k} {k} 0 {pwl(ev[k],stop)}\n'
 if switch=='smooth':
  for idx,(a,b,g) in enumerate([('tx','vp','p1'),('tx','0','p2'),('rx','0','p1'),('rx','sum','p2'),('sum','out','rst')]):
   text+=f'BS{idx} {a} {b} I=V({a},{b})*(1e-12+(0.01-1e-12)*0.5*(1+tanh((V({g})-{vdd/2})/{vdd*.025})))\n'
 elif switch=='ideal':
  text+='.model SW SW(Ron=100 Roff=1e12 Vt=2.5 Vh=0)\n'
  # Clock comparator follows half supply; nominal model identical to old 5 V deck.
  if vdd!=5:text=text.replace('Vt=2.5',f'Vt={vdd/2}')
  for a,b,g in [('tx','vp','p1'),('tx','0','p2'),('rx','0','p1'),('rx','sum','p2'),('sum','out','rst')]:text+=f'S{a}_{b} {a} {b} {g} 0 SW\n'
 else:
  for k in ev:text+=f'B{k}b {k}b 0 V={vdd}-v({k})\n'
  for idx,(a,b,g) in enumerate([('tx','vp','p1'),('tx','0','p2'),('rx','0','p1'),('rx','sum','p2'),('sum','out','rst')]):
   text+=f'MN{idx} {a} {g} {b} 0 N W=10u L=0.8u\nMP{idx} {a} {g}b {b} vdd P W=20u L=0.8u\n'
 text+=f'''.control
set wr_singlescale
set wr_vecnames
tran {dt}n {stop:.12g}
wrdata transient.dat v(out) v(sum) v(other) v(p1) v(p2) v(rst) i(vdd)
quit
.endc
.end
'''
 (d/'tb.cir').write_text(text)
 rec=dict(name=name,arch=arch,switch=switch,fs_Hz=fs,delta_pF=delta,load_pF=load,other_load_pF=other_load,dt_ns=dt,mos=mos,VDD=vdd,temp=temp,vbn=vbn,method=method,status='FAILED')
 try:
  p=subprocess.run(['ngspice','-b','-o','sim.log','tb.cir'],cwd=d,capture_output=True,text=True,timeout=180)
  assert p.returncode==0,(p.returncode,p.stderr)
  a=np.loadtxt(d/'transient.dat',skiprows=1);assert a[-1,0]>=stop*.999
  step=(2.5+delta)/7.5*(1.5+.3);records=[]
  for frame,k,t,start,end in samples:
   out=float(np.interp(t,a[:,0],a[:,1]));summ=float(np.interp(t,a[:,0],a[:,2]));other=float(np.interp(t,a[:,0],a[:,3]));expected=1.5+k*step
   final=float(np.interp(end-20e-9,a[:,0],a[:,1]));early=float(np.interp(end-.15*T,a[:,0],a[:,1]));mask=(a[:,0]>=start)&(a[:,0]<=end-20e-9);tt=a[mask,0];yy=a[mask,1]
   band=.001*step;bad=np.where(abs(yy-final)>band)[0];sett=float((tt[bad[-1]+1]-start)*1e6) if len(bad) and bad[-1]+1<len(tt) else (0.0 if not len(bad) else None)
   records.append(dict(frame=frame,cycle=k,expected_V=expected,out_V=out,error_mV=(out-expected)*1000,sum_error_mV=(summ-1.5)*1000,other_V=other,CM_error_mV=((out+other)/2-vdd/2)*1000 if arch!='baseline' else None,late_change_mV=abs(final-early)*1000,tail_settling_us=sett))
  mask=(a[:,0]>=warm)&(a[:,0]<=warm+7*T);power=float(np.trapz(-vdd*a[mask,7],a[mask,0])/(7*T)*1e6)
  rec.update(status='OK',ideal_step_V=step,max_sample_error_mV=max(abs(x['error_mV']) for x in records),max_sum_error_mV=max(abs(x['sum_error_mV']) for x in records),max_CM_error_mV=max((abs(x['CM_error_mV']) for x in records if x['CM_error_mV'] is not None),default=None),last_out_V=records[-1]['out_V'],min_out_V=float(a[mask,1].min()),max_out_V=float(a[mask,1].max()),other_min_V=float(a[mask,3].min()),other_max_V=float(a[mask,3].max()),avg_VDD_power_uW=power,max_late_change_mV=max(x['late_change_mV'] for x in records),samples=records)
 except Exception as e:rec['error']=str(e)
 (d/'measurements.json').write_text(json.dumps(rec,indent=2));print(name,rec.get('last_out_V'),rec.get('max_sample_error_mV'),rec['status'],flush=True)
 return rec

def save(name,rows):
 (R/(name+'.json')).write_text(json.dumps(rows,indent=2))
 with (R/(name+'.csv')).open('w') as f:
  keys=list(dict.fromkeys(k for x in rows for k in x if k!='samples'));w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:v for k,v in x.items() if k!='samples'} for x in rows)
