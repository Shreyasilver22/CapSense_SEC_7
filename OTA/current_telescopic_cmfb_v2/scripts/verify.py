from pathlib import Path
import subprocess,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
TECH=Path('/home/berson_meshak/pdk/scl08/analog_pdk/Open_Source_SCL_0.8micron_PDK/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/klayout/tech')
def run(kind,ref='reference.cdl',tag=''):
 args=['klayout','-b','-r',str(TECH/('drc/cp8d_drc.drc' if kind=='drc' else 'lvs/lvs_os_scl_cp8d.lvs')),'-rd',f'input={R}/layout/ota_telescopic_layout.gds']
 if kind=='drc':args+=['-rd',f'report1={R}/verification/drc.lyrdb']
 else:args+=['-rd',f'schematic1={R}/schematic/{ref}','-rd',f'target_netlist1={R}/verification/extracted{tag}.cir','-rd',f'report={R}/verification/lvs{tag}.lvsdb']
 p=subprocess.run(args,capture_output=True,text=True,timeout=180);(R/f'verification/{kind}{tag}.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
 return p.stdout+p.stderr
if __name__=='__main__':
 run('drc');items=ET.parse(R/'verification/drc.lyrdb').findall('.//items/item');log=run('lvs');match='Netlists match.' in log
 summary=dict(DRC_markers=len(items),LVS_match=match,deck='Unmodified local SCL CP8D KLayout DRC/LVS decks')
 (R/'verification/summary.json').write_text(json.dumps(summary,indent=2));print(summary,flush=True)
 if match:
  ref=(R/'schematic/reference.cdl').read_text()
  for tag,bad in [('wrong_gate',ref.replace('MN1 NX1 INP','MN1 NX1 VDD')),('wrong_size',ref.replace('W=80.0u','W=70u'))]:
   assert bad!=ref;name='negative_'+tag+'.cdl';(R/'schematic'/name).write_text(bad);s=run('lvs',name,'_negative_'+tag);assert "Netlists don't match" in s
   summary[tag]='MISMATCH as expected'
  (R/'verification/summary.json').write_text(json.dumps(summary,indent=2))
 assert not items and match,summary
