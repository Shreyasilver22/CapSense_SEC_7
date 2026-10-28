from pathlib import Path
import os,subprocess,argparse,json,tempfile,xml.etree.ElementTree as ET,shlex,hashlib,csv
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--pdk-root',required=True,type=Path);a=p.parse_args();tech=a.pdk_root/'libs.tech/magic/SCL_CP8D.tech';deck=a.pdk_root/'libs.tech/klayout/tech/drc/drc.lydrc'
def run(cmd,d,log):
 p=subprocess.run(cmd,cwd=d,capture_output=True,text=True,timeout=180,env={**os.environ,'QT_QPA_PLATFORM':'offscreen','CAP_OPT_ROOT':str(R)});log.write_text(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError(str(log))
run(['klayout','-b','-r',str(R/'scripts/generate.py')],R,R/'results/generate.log');records=json.loads((R/'results/geometry.json').read_text());out=[];models=['* Experimental custom layout extraction. Old-Magic compatibility remains unresolved.\n']
with tempfile.TemporaryDirectory(prefix='scl_capopt_') as temp:
 rule=Path(temp)/'private.drc';rule.write_text(ET.parse(deck).getroot().findtext('text'))
 for g in records:
  name=g['name'];d=R/'results'/name;d.mkdir(exist_ok=True);run(['klayout','-b','-rd','input='+str(R/'layouts'/(name+'.gds')),'-rd','top_cell='+name,'-rd','report1='+str(d/'drc.lyrdb'),'-r',str(rule)],d,d/'drc.log');items=ET.parse(d/'drc.lyrdb').getroot().findall('.//item');assert not items,(name,len(items))
  s=f'''crashbackups stop
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
''';(d/'extract.tcl').write_text(s);run(['magic','-dnull','-noconsole','-norcfile','-T',str(tech),'extract.tcl'],d,d/'extract.log')
  ls=[shlex.split(s) for s in (d/(name+'.ext')).read_text().splitlines()];scale=next((float(x[2]) for x in ls if x[0]=='scale'),1);nodes={x[1]:float(x[3])*scale*1e-18 for x in ls if x[0]=='node'};assert set(nodes)=={'TOP','BOT'}
  cm=sum(float(x[3])*scale*1e-18 for x in ls if x[0]=='cap' and set(x[1:3])=={'TOP','BOT'});assert cm>0
  rec={k:v for k,v in g.items() if k!='polygons'};rec.update(Cmut_F=cm,Ctop_sub_F=nodes['TOP'],Cbot_sub_F=nodes['BOT'],drc_markers=0,target_error_percent=100*(cm/g['target_F']-1));out.append(rec)
  models.append(f'.subckt {name} TOP BOT SUB\nCmut TOP BOT {cm:.12g}\nCtop TOP SUB {nodes["TOP"]:.12g}\nCbot BOT SUB {nodes["BOT"]:.12g}\n.ends {name}\n.subckt {name}_gnd TOP BOT\nXC TOP BOT 0 {name}\n.ends {name}_gnd\n')
  print(name,'Cmut/topSub/botSub pF',cm*1e12,nodes['TOP']*1e12,nodes['BOT']*1e12,'DRC=0',flush=True)
(R/'models/cap_layouts.lib.spice').write_text('\n'.join(models));(R/'results/catalog.json').write_text(json.dumps(dict(technology_sha256=hashlib.sha256(tech.read_bytes()).hexdigest(),drc_sha256=hashlib.sha256(deck.read_bytes()).hexdigest(),magic_version=subprocess.run(['magic','--version'],capture_output=True,text=True).stdout.strip(),capacitors=out),indent=2));keys=list(dict.fromkeys(k for r in out for k in r))
with (R/'results/catalog.csv').open('w') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(out)
