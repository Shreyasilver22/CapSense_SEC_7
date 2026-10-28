from pathlib import Path
import subprocess,json,re,itertools,csv
import numpy as np
R=Path(__file__).resolve().parents[1]
model=R/'spice/models.inc'
caplib=R/'designs/capacitors.lib.spice'
source=(R/'designs/ota_tuned_base.inc').read_text()
variants=[dict(name='ideal_3p',value='3p',orientation='ideal'),dict(name='ideal_3p00538',value='3.00538p',orientation='ideal')]
variants += [dict(name='metal_'+v.replace('.','p')+'_'+o,value=v,orientation=o) for v,o in itertools.product(['2.5p','3p','4p'],['top_n2','top_out'])]
for v in variants:
 cap='Cc n2 out {CC}' if v['orientation']=='ideal' else ('XCC n2 out vss scl08_cap_'+v['value'] if v['orientation']=='top_n2' else 'XCC out n2 vss scl08_cap_'+v['value'])
 text=source.replace('Cc n2 out {CC}',cap)
 (R/'designs'/(v['name']+'.inc')).write_text(text)
# Capacitor snapshot is already included; do not overwrite it.
def net(v,cl,vc):
 return f'''Tuned SCL800 OTA compensation check {v['name']}
.include "{model}"
.include "{R}/designs/capacitors.lib.spice"
.include "{R}/designs/{v['name']}.inc"
.temp 27
.options reltol=1e-5 vntol=1e-8 abstol=1e-12 numdgt=12
VDD vdd 0 5
IREF vdd bias 2.5u
CL out 0 {cl}p
XU inp inn out vdd 0 bias ota_tuned LI=2.4u LM=3.2u LO=3.2u K=4 CC={v['value']}
'''
def run(d,name,s):
 d.mkdir(parents=True,exist_ok=True);(d/(name+'.cir')).write_text(s)
 p=subprocess.run(['ngspice','-b','-o',name+'.log',name+'.cir'],cwd=d,capture_output=True,text=True,timeout=45)
 if p.returncode:raise RuntimeError(str(d)+' '+p.stdout+p.stderr)
def ac(v,cl,vc):
 d=R/'results'/v['name']/f'cl{cl}_vc{vc}'
 s=net(v,cl,vc)+f'''VIN inp 0 dc {vc} ac 1
LDC out inn 1e12
CAC inn 0 1e12
.control
set wr_singlescale
set wr_vecnames
op
print v(out) i(vdd)
ac dec 150 1 1G
let gain_db=db(v(out))
let phase_deg=180/PI*cph(v(out))
wrdata ac.dat gain_db phase_deg
quit
.endc
.end
''';run(d,'ac',s)
 a=np.loadtxt(d/'ac.dat',skiprows=1);cross=np.where(a[:-1,1]*a[1:,1]<0)[0];pm=ugf=float('nan')
 if len(cross)==1:
  z=cross[0];f=-a[z,1]/(a[z+1,1]-a[z,1]);pm=180+a[z,2]+f*(a[z+1,2]-a[z,2]);ugf=10**(np.log10(a[z,0])+f*np.log10(a[z+1,0]/a[z,0]))/1e6
 log=(d/'ac.log').read_text();vals={m[1]:float(m[2]) for m in re.finditer(r'^([^\s=]+)\s*=\s*([-+\d.eE]+)',log,re.M)}
 return dict(**v,CL_pF=cl,VC_V=vc,gain_dB=a[0,1],UGF_MHz=ugf,PM_deg=pm,crossings=len(cross),power_uW=-5e6*vals['i(vdd)'])
def trans(v,cl,large,dt=5):
 lo,hi=(1.5,3.5) if large else (2.5,2.6);d=R/'results'/v['name']/f'cl{cl}_{"large" if large else "small"}_{dt}ns'
 s=net(v,cl,2.5)+f'''VIN inp 0 dc {lo} pulse({lo} {hi} 10u 10n 10n 40u 80u)
VFB inn out 0
.control
set wr_singlescale
set wr_vecnames
tran {dt}n 90u
wrdata tran.dat v(inp) v(out) i(vdd)
quit
.endc
.end
''';run(d,'tran',s);t=np.loadtxt(d/'tran.dat',skiprows=1);r=dict(**v,CL_pF=cl,large_step=large,timestep_ns=dt)
 for label,start,end,window,target in [('rise',10e-6,49e-6,(47e-6,49e-6),hi),('fall',50.01e-6,89e-6,(87e-6,89e-6),lo)]:
  final=float(np.mean(t[(t[:,0]>window[0])&(t[:,0]<window[1]),2]));mask=(t[:,0]>=start)&(t[:,0]<end);tt=t[mask,0];yy=t[mask,2]
  for mode,center in [('dynamic',final),('total',target)]:
   bad=np.where(abs(yy-center)>.001*(hi-lo))[0];r[label+'_'+mode+'_us']=float((tt[bad[-1]+1]-start)*1e6) if len(bad) and bad[-1]+1<len(tt) else (0.0 if not len(bad) else float('nan'))
  r[label+'_static_error_mV']=(final-target)*1e3
 r['worst_dynamic_us']=max(r['rise_dynamic_us'],r['fall_dynamic_us']);return r
acs=[];trs=[]
for i,v in enumerate(variants):
 for cl,vc in itertools.product([1,5,10],[1.5,2.5,3.5]):acs.append(ac(v,cl,vc))
 for cl,large in itertools.product([1,5,10],[False,True]):trs.append(trans(v,cl,large))
 print('Completed',i+1,'/',len(variants),v['name'],flush=True)
def csvwrite(name,rows):
 with (R/'results'/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite('ac_checks.csv',acs);csvwrite('settling_checks.csv',trs)
nom=[]
for v in variants:
 a=next(r for r in acs if r['name']==v['name'] and r['CL_pF']==5 and r['VC_V']==2.5);s=next(r for r in trs if r['name']==v['name'] and r['CL_pF']==5 and not r['large_step']);l=next(r for r in trs if r['name']==v['name'] and r['CL_pF']==5 and r['large_step']);nom.append(dict(**a,small_worst_dynamic_us=s['worst_dynamic_us'],large_worst_dynamic_us=l['worst_dynamic_us'],small_static_error_mV=s['rise_static_error_mV'],minimum_checked_PM_deg=min(x['PM_deg'] for x in acs if x['name']==v['name'])))
(R/'results/summary.json').write_text(json.dumps(dict(ac_runs=len(acs),transient_runs=len(trs),nominal=nom),indent=2));print(json.dumps(nom,indent=2))
