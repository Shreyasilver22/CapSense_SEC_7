from pathlib import Path
import argparse,subprocess,os,json,tempfile,xml.etree.ElementTree as ET,shlex,hashlib,csv,shutil
from common import ROOT as R, requests
p=argparse.ArgumentParser();p.add_argument('--pdk-root',required=True);args=p.parse_args();pdk=Path(args.pdk_root).resolve();tech=pdk/'libs.tech/magic/SCL_CP8D.tech';deck=pdk/'libs.tech/klayout/tech/drc/drc.lydrc';assert tech.is_file() and deck.is_file()
for folder in ['results','layouts','models','symbols','examples','plots']:(R/folder).mkdir(exist_ok=True)
def run(cmd,cwd,log):
 a=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=240,env={**os.environ,'QT_QPA_PLATFORM':'offscreen','CAP_PROJECT_ROOT':str(R)});log.write_text(a.stdout+a.stderr)
 if a.returncode:raise RuntimeError('Command failed; see '+str(log))
 return a.stdout+a.stderr
run(['klayout','-b','-r',str(R/'scripts/generate.py')],R,R/'results/generate.log')
geometry=json.loads((R/'results/geometry.json').read_text());records={};models=['* EXPERIMENTAL custom metal capacitors. Native extraction compatibility unresolved.\n* All substrate parasitics retained from raw .ext; no physical voltage/PVT qualification.\n']
with tempfile.TemporaryDirectory(prefix='sclcap_rules_') as temp:
 rule=Path(temp)/'local.drc';rule.write_text(ET.parse(deck).getroot().findtext('text'))
 for g in geometry:
  name=g['cell'];d=R/'results'/name;d.mkdir(exist_ok=True)
  run(['klayout','-b','-rd','input='+str(R/'layouts'/(name+'.gds')),'-rd','top_cell='+name,'-rd','report1='+str(d/'drc.lyrdb'),'-r',str(rule)],d,d/'drc.log')
  count=len(ET.parse(d/'drc.lyrdb').getroot().findall('.//item'));assert count==0,(name,count)
  tcl=f'''crashbackups stop
drc off
gds read {{{R/'layouts'/(name+'.gds')}}}
load {name}
select top cell
extract all
ext2spice default
ext2spice format ngspice
ext2spice scale off
ext2spice cthresh 0
ext2spice subcircuits top on
ext2spice -y 6 -o {name}.native.spice
save {name}
quit -noprompt
'''
  (d/'extract.tcl').write_text(tcl);log=run(['magic','-dnull','-noconsole','-norcfile','-T',str(tech),'extract.tcl'],d,d/'extract.log');assert "isn't a valid" not in log
  ls=[shlex.split(x) for x in (d/(name+'.ext')).read_text().splitlines()];scale=next((float(x[2]) for x in ls if x[0]=='scale'),1);nodes={x[1]:float(x[3])*scale*1e-18 for x in ls if x[0]=='node'};assert set(nodes)=={'TOP','BOT'}
  cm=sum(float(x[3])*scale*1e-18 for x in ls if x[0]=='cap' and set(x[1:3])=={'TOP','BOT'});assert cm>0
  rec=dict(**g,Cmut_F=cm,Ctop_sub_F=nodes['TOP'],Cbot_sub_F=nodes['BOT'],drc_markers=count);records[name]=rec
  block=f'.subckt {name} TOP BOT SUB\nCmut TOP BOT {cm:.12g}\nCtop TOP SUB {nodes["TOP"]:.12g}\nCbot BOT SUB {nodes["BOT"]:.12g}\n.ends {name}\n';models.append(block)
  print(name,'Cmut_pF=',cm*1e12,'DRC=0',flush=True)
catalog=[]
for item in requests():
 value=item['value'];rec=records[item['cell']];alias='scl08_cap_'+value
 models.append(f'.subckt {alias} TOP BOT SUB\nXCORE TOP BOT SUB {item["cell"]}\n.ends {alias}\n.subckt scl08_cap_gnd_{value} TOP BOT\nXCORE TOP BOT 0 {item["cell"]}\n.ends scl08_cap_gnd_{value}\n')
 catalog.append(dict(**item,**{k:v for k,v in rec.items() if k not in item},error_percent=100*(rec['Cmut_F']/item['target_F']-1)))
 # Human-readable filename alias, same internal cell as catalog identifies.
 safe=value.lower().replace('.','p').replace('+','').replace('-','m');shutil.copy2(R/'layouts'/(item['cell']+'.gds'),R/'layouts'/('requested_'+safe+'.gds'))
(R/'models/generated_caps.lib.spice').write_text('\n'.join(models))
meta=dict(status='EXPERIMENTAL: old Magic versus required 8.3.579+; raw-.ext conversion retained, no formal capacitor LVS or physical qualification',pdk_configuration='Set SCL08_CAP_PDK_ROOT or pass --pdk-root',magic_version=subprocess.run(['magic','--version'],capture_output=True,text=True).stdout.strip(),technology_sha256=hashlib.sha256(tech.read_bytes()).hexdigest(),drc_sha256=hashlib.sha256(deck.read_bytes()).hexdigest(),capacitors=catalog)
(R/'results/catalog.json').write_text(json.dumps(meta,indent=2));keys=list(dict.fromkeys(k for c in catalog for k in c))
with (R/'results/catalog.csv').open('w') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(catalog)
# Value lookup for display only. Simulation resolves the exact generated alias, never an ideal fallback.
lines=['array unset cap_actual_pf','array set cap_actual_pf {']+[f' {{{c["value"]}}} {c["Cmut_F"]*1e12:.8g}' for c in catalog]+['}']
(R/'models/catalog.tcl').write_text('\n'.join(lines)+'\nif {[info exists ::env(SCL08_CAP_PDK_ROOT)]} {set cap_pdk_root $::env(SCL08_CAP_PDK_ROOT)}\n')
print('Built',len(catalog),'value aliases and matching layouts')
