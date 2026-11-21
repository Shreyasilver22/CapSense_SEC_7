from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv, json, re, subprocess
import numpy as np

ROOT=Path(__file__).resolve().parent
PDK=Path.home()/'pdk/scl08/ngspice_models49/mos/tntp49_5v'
export=(ROOT/'results/gm_ota_symbol_tb.spice').read_text()
dut=re.search(r'(?ims)^\.subckt gm_ota .*?^\.ends\s*$',export)[0]
(ROOT/'designs/gm_ota.inc').write_text(dut+'\n')
CTRL='.control\nset wr_singlescale\nset wr_vecnames\nset numdgt=12\n'
END='quit\n.endc\n.end\n'
DEV=('m1','m2','m3','m4','m5')
VECT='v(out) v(xg.n1) v(xg.tail) i(vdd) '+' '.join(
 f'@m.xg.{m}[{v}]' for m in DEV for v in ('id','gm','gds','vgs','vds','vdsat'))
def preamble():
 return f"""SCL08 uploaded five-transistor OTA, VBN = 0.8625 V
.include "{PDK}"
.include "{ROOT}/designs/gm_ota.inc"
.temp 27
.options reltol=1e-6 vntol=1e-9 abstol=1e-13 method=gear maxord=2
VDD vdd 0 5
VBN vbn 0 0.8625
XG sense sp vdd 0 vbn out gm_ota
CL out 0 5p
"""
def sim(name,body,standalone=False):
 folder=ROOT/'results'/name
 folder.mkdir(exist_ok=True)
 (folder/'.spiceinit').write_text('set ngbehavior=hsa\nset num_threads=1\n')
 (folder/'bench.cir').write_text((preamble() if not standalone else '')+body)
 process=subprocess.run(['ngspice','-b','-o','run.log','bench.cir'],cwd=folder,capture_output=True,check=True,timeout=80)
 log=(folder/'run.log').read_text()
 if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
  raise ValueError(folder.name+'\n'+log[-700:])
 return folder
def load(f):
 a=np.loadtxt(f,skiprows=1,ndmin=2)
 assert np.isfinite(a).all()
 return a
def crossover(f,g,p):
 idx=np.flatnonzero((g[:-1]>=0)&(g[1:]<0))
 if not len(idx): return np.nan,np.nan
 j=idx[0];a=g[j]/(g[j]-g[j+1])
 return f[j]*(f[j+1]/f[j])**a,180+p[j]+a*(p[j+1]-p[j])
def measure_ac(f):
 freq,re_h,im_h=load(f).T
 h=re_h+1j*im_h
 g=20*np.log10(abs(h));p=np.degrees(np.unwrap(np.angle(h)))
 ugf,pm=crossover(freq,g,p)
 ix=np.flatnonzero(g<=g[0]-3)
 fc=np.nan
 if len(ix):
  j=ix[0]
  fc=10**np.interp(g[0]-3,g[j-1:j+1][::-1],np.log10(freq[j-1:j+1][::-1]))
 return dict(gain_dB=float(g[0]),gain_V_per_V=float(abs(h[0])),UGBW_Hz=float(ugf),
             estimated_PM_deg=float(pm),open_loop_3dB_Hz=float(fc))
def op_rows(folder,label):
 a=load(folder/'op.dat')[0,1:]
 op,n1,tail,supply=a[:4]
 d=a[4:].reshape(5,6)
 rows=[]
 for m,values in zip(DEV,d):
  ids,gm,gds,vgs,vds,dsat=values
  rows.append(dict(case=label,device=m.upper(),current_uA=abs(ids)*1e6,gm_uS=gm*1e6,
   ro_Mohm=1/gds/1e6,VGS_V=vgs,VDS_V=vds,VDSAT_V=dsat,
   saturation_margin_mV=1e3*(abs(vds)-abs(dsat))))
 return dict(output_V=op,mirror_node_V=n1,tail_node_V=tail,
             supply_current_uA=-supply*1e6,power_uW=-supply*5e6),rows
def open_ac():
 body='VSP sp 0 2.5\nVSENSE sense 0 DC 2.5 AC 1\n'
 body+=CTRL+'op\nwrdata op.dat '+VECT+"""
ac dec 120 .01 1G
let gr=-real(v(out))
let gi=-imag(v(out))
wrdata ac.dat gr gi
"""+END
 f=sim('equal_inputs',body)
 values,rows=op_rows(f,'equal_inputs')
 return dict(case='Equal inputs, no DC output servo',input_CM_V=2.5,**values,**measure_ac(f/'ac.dat')),rows
def loop_ac(vcm):
 # Open the small-signal feedback while retaining the follower DC bias.
 body=f"""VSP sp 0 DC {vcm} AC 1
LDC out sense 1e12
CAC sense 0 1e12
"""+CTRL+'op\nwrdata op.dat '+VECT+"""
ac dec 120 .01 1G
let gr=real(v(out))
let gi=imag(v(out))
wrdata ac.dat gr gi
"""+END
 f=sim(f'follower_ac_cm{vcm:g}',body)
 op,rows=op_rows(f,f'follower_dc_cm{vcm:g}')
 return dict(case='Follower operating point',input_CM_V=vcm,**op,**measure_ac(f/'ac.dat')),rows
def gm():
 body="""VSP sp 0 DC 2.5 AC -.5
VSENSE sense 0 DC 2.5 AC .5
VCLAMP out 0 2.5
"""+CTRL+'op\nwrdata op.dat '+VECT+"""
ac dec 80 1 100Meg
let gmr=-real(i(vclamp))
let gmi=-imag(i(vclamp))
wrdata gm.dat gmr gmi
dc VSENSE 2.4 2.6 .0005
let idi=v(sense)-2.5
let iout=-i(vclamp)
wrdata gm_transfer.dat idi iout
"""+END
 f=sim('transconductance',body)
 data=load(f/'gm.dat')
 op,rows=op_rows(f,'clamped_output_2p5')
 return dict(effective_differential_gm_uS=float(data[0,1])*1e6,**op),rows
def dc():
 return sim('dc_transfer',
 """VSP sp 0 2.5
VSENSE sense 0 2.5
"""+CTRL+"""dc VSENSE 2.45 2.55 .0001
wrdata transfer.dat v(out)
"""+END)
def settle(t,y,target,tol,start,stop):
 ix=np.flatnonzero((t>=start)&(t<stop))
 bad=np.flatnonzero(abs(y[ix]-target)>tol)
 j=bad[-1]+1 if len(bad) else 0
 return float((t[ix[j]]-start)*1e6) if j<len(ix) else np.nan
def transient(step):
 lo,hi=((2.5,2.6) if step==.1 else (1.5,3.5))
 body=f"""VSP sp 0 PULSE({lo} {hi} 10u 10n 10n 40u 80u)
ESENSE sense 0 out 0 1
"""+CTRL+"""tran 5n 90u 0 5n
wrdata transient.dat v(sp) v(out)
"""+END
 f=sim(f'follower_step_{step:g}',body)
 t,inp,out=load(f/'transient.dat').T
 assert t[-1]>89.999e-6
 results=[]
 for name,start,stop,command in [('rise',10e-6,50.01e-6,hi),('fall',50.01e-6,90e-6,lo)]:
  target=float(np.mean(out[(t>=stop-4e-6)&(t<stop-1e-6)]))
  window=(t>=start)&(t<stop)
  peak=float(np.max(out[window]) if name=='rise' else np.min(out[window]))
  results.append(dict(step_V=step,edge=name,command_V=command,attained_output_V=target,
     static_error_mV=(target-command)*1e3,
     dynamic_settle_us=settle(t,out,target,step*.001,start,stop),
     ideal_settle_us=settle(t,out,command,step*.001,start,stop),
     peak_output_V=peak))
 return results
def save(name,rows):
 keys=list(dict.fromkeys(k for row in rows for k in row))
 with (ROOT/'results'/f'{name}.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
if __name__=='__main__':
 # The first job is the actual Xschem symbol-generated bench.
 native=(ROOT/'results/gm_ota_symbol_tb.spice').read_text()
 f=sim('symbol_export',native,True)
 with ThreadPoolExecutor(6) as pool:
  jobs=[pool.submit(open_ac),pool.submit(gm),pool.submit(dc),
        pool.submit(transient,.1),pool.submit(transient,2.)]
  common=[pool.submit(loop_ac,x) for x in (.6,.8,1.,1.2,1.5,2.,2.5,3.,3.5,4.)]
  native_result=jobs[0].result();gm_result=jobs[1].result()
  jobs[2].result();steps=jobs[3].result()+jobs[4].result()
  loop_results=[f.result() for f in common]
 save('ac_summary',[native_result[0]]+[x[0] for x in loop_results])
 save('device_operating_points',native_result[1]+gm_result[1]+[r for _,group in loop_results for r in group])
 save('settling',steps)
 result=dict(as_drawn=native_result[0],follower_2p5=next(x[0] for x in loop_results if x[0]['input_CM_V']==2.5),gm=gm_result[0],transient=steps)
 (ROOT/'results/summary.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
