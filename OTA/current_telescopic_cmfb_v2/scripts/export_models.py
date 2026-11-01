from pathlib import Path
import shlex,re,json,subprocess,hashlib
R=Path(__file__).resolve().parents[1]
raw=[shlex.split(s) for s in (R/'pex/ota_telescopic_layout.ext').read_text().splitlines()]
scale=next(float(x[3])*1e-8 for x in raw if x and x[0]=='scale')
dev=[x for x in raw if x[:3]==['device','rsubckt','RPP']];assert len(dev)==80
halves=[]
for k,x in enumerate(dev):
 l=float(x[7].split('=')[1])*scale;w=float(x[8].split('=')[1])*scale
 for side,a,b in [('A',x[13],x[10]),('B',x[10],x[16])]:halves.append(f'XR{k}{side} {a} {b} RPP W={w:.12g} L={l/2:.12g}')
source=(R/'pex/ota_C_raw.spice').read_text();lines=[]
for line in source.splitlines():
 if line.startswith('X') and ' RPP ' in line:continue
 if line.lower().startswith('.ends'):lines+=halves
 if line.startswith('M'):line=re.sub(r'\s([np])\s',lambda m:' '+m[1].upper()+' ',line)
 lines.append(line)
(R/'models/layout_C.spice').write_text('\n'.join(lines)+'\n')
top=[]
for line in lines:
 a=line.split()
 if a and a[0].startswith('C'):continue
 if a and a[0].startswith('X') and 'RPP' in a:
  w=float(next(s[2:] for s in a if s.startswith('W=')));l=float(next(s[2:] for s in a if s.startswith('L=')));line=f'R{a[0]} {a[1]} {a[2]} {28*l/w:.12g} RPP'
 top.append(line)
(R/'schematic/layout_C.cdl').write_text('\n'.join(top)+'\n')
tech=Path('/home/berson_meshak/pdk/scl08/analog_pdk/Open_Source_SCL_0.8micron_PDK/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/klayout/tech/lvs/lvs_os_scl_cp8d.lvs')
p=subprocess.run(['klayout','-b','-r',str(tech),'-rd',f'input={R}/layout/ota_telescopic_layout.gds','-rd',f'schematic1={R}/schematic/layout_C.cdl','-rd',f'report={R}/verification/layout_C.lvsdb','-rd',f'target_netlist1={R}/verification/layout_C_reference.cir'],capture_output=True,text=True,timeout=180)
(R/'verification/layout_C_lvs.log').write_text(p.stdout+p.stderr);assert p.returncode==0 and 'Netlists match.' in p.stdout,p.stdout+p.stderr
# Matching pre-layout macro: same bias diode and external cascode-reference pins.
ren={'ip':'INP','im':'INN','op':'OUTP','om':'OUTM','vdd':'VDD','0':'VSS','bn':'IREF','vcm':'VCM','nb':'VBN','pb':'VBP'}
node=lambda x:ren.get(x,x.upper())
pre=['* Same source transistor circuit; integrated bias diode, external cascode references.','.subckt ota_telescopic_layout INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP']
for line in (R/'models/source_telescopic.spice').read_text().splitlines():
 if line.startswith(('M','X')):
  a=line.split();n=4 if a[0].startswith('M') else 2;a[1:n+1]=[node(x) for x in a[1:n+1]];pre.append(' '.join(a))
pre+=['MREF IREF IREF VSS VSS N W=20u L=3.2u AD=90p AS=90p PD=49u PS=49u','.ends ota_telescopic_layout']
(R/'models/schematic.spice').write_text('\n'.join(pre)+'\n')
caps={x[1]:float(x[3])*1e-18 for x in raw if x and x[0]=='node'}
meta=dict(native_RPP_sections=len(dev),exported_tee_halves=len(halves),topology_LVS='MATCH against GDS after restoring both native resistor halves',resistor_body_ground_C_pF=sum(caps[x[10]] for x in dev)*1e12,total_explicit_cap_count=sum(1 for x in lines if x.startswith('C')),gds_sha256=hashlib.sha256((R/'layout/ota_telescopic_layout.gds').read_bytes()).hexdigest(),limits='Resistor body C uses engineering alias of existing poly coefficients, not a qualified foundry extraction rule. C-only model; no full wire/substrate RC claim.')
(R/'verification/model_export.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
