"""Run design_1 ngspice checks; optionally regenerate native xschem testbenches."""
from pathlib import Path
import subprocess, argparse,re,json,shutil,sys
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--xschem',action='store_true');p.add_argument('--plots',action='store_true');a=p.parse_args()
if not (root/'spice/models.inc').is_file():p.error('Configure the model first: python3 scripts/configure_models.py /path/to/tntp49_5v')
if not shutil.which('ngspice'):p.error('ngspice is required.')
r=root/'results';r.mkdir(exist_ok=True)
for name in ['reference','open_loop','follower']:
 subprocess.run(['ngspice','-b','-o',str(r/(name+'.log')),name+'.cir'],cwd=root/'tb',check=True)
if a.xschem:
 if not shutil.which('xschem'):p.error('xschem is required for --xschem.')
 for name in ['ota_follower_tb','ota_ac_tb']:
  with (r/(name+'_netlist.log')).open('w') as f:
   subprocess.run(['xschem','-x','-q','-r','-n','-s','--rcfile',str(root/'xschemrc'),'-o',str(r),str(root/'tb'/(name+'.sch'))],cwd=root,stdout=f,stderr=f,check=True)
  if 'IS MISSING' in (r/(name+'.spice')).read_text():raise RuntimeError('Missing xschem symbol; inspect '+name+'_netlist.log')
  subprocess.run(['ngspice','-b','-o',name+'.log',name+'.spice'],cwd=r,check=True)
def value(text,key):return float(re.search(r'^'+re.escape(key)+r'\s*=\s*([-+0-9.eE]+)',text,re.M).group(1))
ol=(r/'open_loop.log').read_text();fl=(r/'follower.log').read_text()
for log in [ol,fl,(r/'reference.log').read_text()]:
 if re.search(r'(^|\n)Error|simulation interrupted',log,re.I):raise RuntimeError('Simulator error; inspect results logs.')
summary={'simulator':'ngspice','supply_V':5,'temperature_C':27,'external_load_F':5e-12,'compensation_F':5e-12,'external_bias_V':.95,'gain_dB':value(ol,'gain_1hz'),'unity_gain_Hz':value(ol,'ugf'),'phase_at_UGF_deg':value(ol,'phase_ugf'),'estimated_phase_margin_deg':180+value(ol,'phase_ugf'),'follower_high_V':value(fl,'output_high'),'follower_low_V':value(fl,'output_low'),'scope':'Seven-MOS single-ended voltage-biased baseline; not the planned current-reference or fully differential CMFB design.','limitations':'PDK HSPICE compatibility warnings remain; nominal only, no precision SC/noise/PVT/layout qualification.'}
(r/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if a.plots:subprocess.run([sys.executable,str(root/'scripts/plot_results.py')],cwd=root,check=True)
