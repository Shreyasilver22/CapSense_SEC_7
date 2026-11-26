#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,re,time,math,concurrent.futures,argparse,os,sys
import numpy as np
R=Path(__file__).resolve().parent;P=R.parent
SIZES={x['target_pF']:x for x in json.loads((R/'specified_sizes.json').read_text())}
RAW=(R/'sweep_template.spice').read_text()
# Archived study: use the circuit snapshot paired with sweep_template.spice.
SUPPORT=(R/'simulation_support_snapshot.spice').read_text()
MODEL=(P/'simulation/cosim_models.spice').read_text()
# Each worker has its own VVP log; no simulation-output files are shared.
MODEL=re.sub(r'"/tmp/capsense_phase_runtime/simulation/phase_v1_vvp.log"','"vvp.log"',MODEL)
REPLAY=os.environ.get('CAPSENSE_RTL_REPLAY')=='1'
EDGES=json.loads((R/'rtl_recorded_edges.json').read_text()) if REPLAY else None
DIGITAL=os.environ.get('CAPSENSE_DIGITAL_MASTER')=='1'
BASE_STEP=int(os.environ.get('CAPSENSE_MAXSTEP_NS','400'))
NAMES=['outp','outn','sump','sumn','sample_valid','phi1','phit','phi2']
def replay_sources(cycles):
 out=['* Output sequence recorded from unchanged RTL, replayed through the same 1us ideal voltage-edge model.']
 stop=(cycles*100-5)*1e-6
 for name,spec in EDGES['signals'].items():
  events=[tuple(e) for e in spec['initial_events']]
  for k in range(1,cycles):events.extend((t+k*100e-6,v) for t,v in spec['periodic_events'])
  events=sorted((t,v) for t,v in events if 0<t<stop)
  pts=[(0.,0.)];start=0.;v0=target=0.;end=0.
  for t,new in events:
   if end>start and t<end:current=v0+(target-v0)*(t-start)/(end-start)
   else:
    current=target
    if end>pts[-1][0]:pts.append((end,target))
   if t>pts[-1][0]:pts.append((t,current))
   start=t;v0=current;target=new;end=t+1e-6
  if end<stop and end>pts[-1][0]:pts.append((end,target))
  pts.append((stop,target))
  out.append(f'VRTL_{name} {name} 0 PWL(')
  out.extend(f'+ {t:.15g} {v:.12g}' for t,v in pts)
  out.append('+ )')
 return '\n'.join(out)+'\n'

def deck(cfb,cp,cn,cycles,maxstep_ns=BASE_STEP):
 s=RAW.replace('.include '+str(P/'simulation/analog_support.spice'),SUPPORT).replace('.include '+str(P/'simulation/cosim_models.spice'),MODEL)
 if REPLAY:
  s=re.sub(r'^(?:Vclk_1mhz |Vrst_n |AINPUTS |ADAC_).*\n','',s,flags=re.M)
  s=re.sub(r'^APHASE .*\n\+ capsense_phase_gen_cosim\n','',s,flags=re.M)
  s=s.replace('\n.control','\n'+replay_sources(cycles)+'\n.control')
 if DIGITAL:
  s=re.sub(r'^(?:Vclk_1mhz |Vrst_n |AINPUTS ).*\n','',s,flags=re.M)
  s=s.replace('\n.control', '\nAMASTER [ d_clk_1mhz d_rst_n ] sweep_master\n.model sweep_master d_source(input_file="clock.txt")\n.control')
 s=re.sub(r'^\.tran .*\n','',s,flags=re.M);s=re.sub(r'^\.save .*\n','',s,flags=re.M)
 s=re.sub(r'\.param CP=[^\n]+',f'.param CP={cp}p CN={cn}p CFB_L={SIZES[cfb]["L_um"]:.9g}u',s)
 ctl=f'''.control
set wr_singlescale
set wr_vecnames
set numdgt=12
set xtrtol=2
save {' '.join('v('+n+')' for n in NAMES)}
tran {maxstep_ns}n {cycles*100-5}u 0 {maxstep_ns}n
wrdata tail.dat {' '.join('v('+n+')' for n in NAMES)}
quit
.endc'''
 s=re.sub(r'\.control\n.*?\.endc',lambda m:ctl,s,flags=re.S);return s

def run(cfb,cp,cn,cycles=8,step=BASE_STEP,timeout=180):
 tag=f'cfb{cfb}_cp{cp:g}_cn{cn:g}'.replace('.','p');d=R/('runs_replay' if REPLAY else ('runs_digital' if DIGITAL else 'runs'))/tag
 if step!=BASE_STEP:d=R/('accuracy_replay' if REPLAY else 'accuracy')/f'{tag}_dt{step}'
 d.mkdir(parents=True,exist_ok=True)
 resultfile=d/'result.json'
 if resultfile.exists():
  old=json.loads(resultfile.read_text())
  if old.get('complete') and old.get('cycles',0)>=cycles:return old
 shutil_init=P/'simulation/.spiceinit'
 (d/'.spiceinit').write_text(shutil_init.read_text())
 started=time.time();row={'cfb_nominal_pF':cfb,'cp_pF':cp,'cn_pF':cn,'delta_c_pF':cp-cn,'mean_c_pF':(cp+cn)/2,'cycles':cycles,'maxstep_ns':step,'complete':False,'settled':False,'status':'failed','drive_mode':'recorded_RTL_replay' if REPLAY else 'live_Icarus','simulation_directory':str(d)}
 try:
  for n in ['tail.dat']:
   p=d/n
   if p.exists():p.unlink()
  (d/'bench.cir').write_text(deck(cfb,cp,cn,cycles,step))
  if DIGITAL:
   events=['0 0s 0s']
   for k in range(cycles*100):
    rst='1s' if k>=2 else '0s'
    events.extend([f'{k*1e-6+1.5e-9:.15g} 1s {rst}',f'{k*1e-6+501.5e-9:.15g} 0s {rst}'])
   (d/'clock.txt').write_text('\n'.join(events)+'\n')
  with (d/'launcher.log').open('w') as log:
   completed=subprocess.run(['nice','-n','10','ngspice','-b','-o','ngspice.log','bench.cir'],cwd=d,stdout=log,stderr=log,timeout=timeout)
  log=(d/'ngspice.log').read_text()
  errors=re.findall(r'^.*(?:timestep too small|aborted|no entry function|undefined symbol|fatal error|error:|d_cosim failed|Icarus shim failed).*$' ,log,re.M|re.I)
  if errors:raise RuntimeError('; '.join(errors)[:600])
  a=np.loadtxt(d/'tail.dat',skiprows=1)
  end=(cycles*100-5)*1e-6;sample=((cycles-1)*100+83)*1e-6;previous=sample-100e-6
  if abs(a[-1,0]-end)>1e-10 or not np.isfinite(a).all():raise RuntimeError('Incomplete/nonfinite transient')
  at=lambda t,c:float(np.interp(t,a[:,0],a[:,c]))
  op,on,ip,inn=[at(sample,c) for c in [1,2,3,4]]
  prevop,prevon,previp,previnn=[at(previous,c) for c in [1,2,3,4]]
  drift=max(abs(op-prevop),abs(on-prevon),abs((ip+inn-previp-previnn)/2))
  # Ensure actual phases toggled during saved complete frame and strobe is asserted at sample.
  for c in [5,6,7,8]:
   if a[:,c].max()<4.9 or a[:,c].min()>.1:raise RuntimeError('Phase/strobe does not toggle')
  strobe=at(sample,5)
  if strobe<2.5:raise RuntimeError('Measurement outside sample_valid')
  slope=abs((at(sample+200e-9,1)-at(sample+200e-9,2))-(at(sample-200e-9,1)-at(sample-200e-9,2)))/.4
  row.update(complete=True,settled=drift<=.001,status='settled' if drift<=.001 else 'unsettled',sample_us=sample*1e6,voutp_V=op,voutn_V=on,vdiff_V=op-on,input_vcm_V=(ip+inn)/2,output_vcm_V=(op+on)/2,previous_vdiff_V=prevop-prevon,cycle_drift_V=drift,local_vdiff_slope_V_per_us=slope,sample_valid_V=strobe,output_rail_excursion=bool(a[:,1:3].min()<-.3 or a[:,1:3].max()>5.3),output_min_V=float(a[:,1:3].min()),output_max_V=float(a[:,1:3].max()),seconds=round(time.time()-started,3))
 except Exception as e:row.update(error=str(e)[:800],seconds=round(time.time()-started,3))
 with (d/'attempt_history.jsonl').open('a') as history:history.write(json.dumps(row)+'\n')
 resultfile.write_text(json.dumps(row,indent=2));return row

def robust_run(cfb,cp,cn,cycles):
 row=run(cfb,cp,cn,cycles=cycles,timeout=max(180,cycles*20))
 if not row['complete']:
  errors=[row.get('error')]
  for step in [80,20]:
   row=run(cfb,cp,cn,cycles=cycles,step=step,timeout=max(300,cycles*25))
   if row['complete']:
    row['fallback_used']=True;row['previous_attempt_errors']=errors;break
   errors.append(row.get('error'))
 return row

def task(args):
 cfb,cp,cn=args
 effective_sum=10*cp/(10+cp)+10*cn/(10+cn)
 initial_cycles=(16 if effective_sum<5.2 else 8) if cfb==40 else (32 if cfb==60 and effective_sum<5.2 else 16)
 row=robust_run(cfb,cp,cn,initial_cycles)
 if row['complete'] and not row['settled']:
  for cycles in [n for n in [16,32] if n>initial_cycles]:
   last_good=row
   row=robust_run(cfb,cp,cn,cycles)
   if not row['complete']:
    row={**last_good,'status':'unsettled_extension_failed','settled':False,'extension_error':row.get('error')};break
   if row['settled']:break
 if REPLAY:
  tag=f'cfb{cfb}_cp{cp:g}_cn{cn:g}'.replace('.','p');d=R/'runs_replay'/tag;d.mkdir(exist_ok=True)
  (d/'result.json').write_text(json.dumps(row,indent=2))
 return row

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=6);parser.add_argument('--pilot',action='store_true');args=parser.parse_args()
 for name,target in [('capsense_phase_runtime',Path('/home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench')),('capsense_integrated',P)]:
  p=Path('/tmp')/name
  if p.is_symlink():assert p.resolve()==target
  elif p.exists():raise RuntimeError('Alias occupied')
  else:p.symlink_to(target,target_is_directory=True)
 points=[(c,float(cp),float(cn)) for cp in np.arange(1,12.01,.5) for cn in np.arange(1,12.01,.5) for c in [40,50,60]]
 if args.pilot:points=[(40,6.,6.),(40,1.,12.),(40,12.,1.),(60,12.,12.)]
 results=[];start=time.time()
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
  futures={pool.submit(task,p):p for p in points}
  for f in concurrent.futures.as_completed(futures):
   row=f.result();results.append(row)
   (R/'progress.json').write_text(json.dumps({'done':len(results),'total':len(points),'elapsed_s':time.time()-start,'settled':sum(x['settled'] for x in results),'failed':sum(not x['complete'] for x in results),'last':row},indent=2))
   with (R/'completed.jsonl').open('a') as out:out.write(json.dumps(row)+'\n')
   print(f'{len(results)}/{len(points)}: {futures[f]} {row["status"]} {row.get("seconds")}s',flush=True)
 (R/((('pilot_results' if args.pilot else 'sweep_results')+('_replay' if REPLAY else '')+'.json'))).write_text(json.dumps(results,indent=2))
 if not args.pilot and REPLAY:
  subprocess.run([sys.executable,str(R/'analyze_results.py')],cwd=R,check=True)
  (R/'FINISHED.json').write_text(json.dumps({'cases':len(results),'completed':sum(x['complete'] for x in results),'settled':sum(x['settled'] for x in results),'elapsed_seconds':time.time()-start},indent=2))
if __name__=='__main__':main()
