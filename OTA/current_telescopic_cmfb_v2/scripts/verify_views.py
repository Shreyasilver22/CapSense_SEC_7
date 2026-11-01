from pathlib import Path
import subprocess,json
import numpy as np
R=Path(__file__).resolve().parents[1]
deck='/home/berson_meshak/pdk/scl08/analog_pdk/Open_Source_SCL_0.8micron_PDK/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/klayout/tech/lvs/lvs_os_scl_cp8d.lvs'
p=subprocess.run(['klayout','-b','-r',deck,'-rd',f'input={R}/layout/ota_telescopic_layout.gds','-rd',f'schematic1={R}/schematic/xschem_reference.cdl','-rd',f'report={R}/verification/xschem.lvsdb','-rd',f'target_netlist1={R}/verification/xschem_reference.cir'],capture_output=True,text=True,timeout=180)
(R/'verification/xschem_lvs.log').write_text(p.stdout+p.stderr);assert p.returncode==0 and 'Netlists match.' in p.stdout,p.stdout+p.stderr
rows=json.loads((R/'SC_validation.json').read_text());ref=next(x for x in rows if x['arch']=='layout_C' and x['switch']=='tg' and x['fs_Hz']==50000 and x['dt_ns']==10 and x['VDD']==5 and x['load_pF']==5)
a=np.loadtxt(R/'tb/xschem_SC.dat',skiprows=1);b=np.loadtxt(R/'results'/ref['name']/'transient.dat',skiprows=1)
times=np.array([68.8,88.8,108.8,148.8,168.8,188.8])*1e-6
max_sample_difference=float(np.max(abs(np.interp(times,a[:,0],a[:,1])-np.interp(times,b[:,0],b[:,1]))))
assert a[-1,0]>=.00021*.999 and max_sample_difference<5e-6,max_sample_difference
orig=(R/'models/original_telescopic.spice').read_text().splitlines();new=(R/'models/source_telescopic.spice').read_text().splitlines();core=['MN1','MN2','MNC1','MNC2','MPC1','MPC2','MP1','MP2','MTAIL']
for name in core:assert next(x.split() for x in orig if x.startswith(name+' '))==next(x.split() for x in new if x.startswith(name+' ')),name
summary=dict(xschem_transistor_schematic_LVS='MATCH against GDS',xschem_symbol_SC_simulation='PASS: sampled outputs match generated deck within 5 uV; adaptive timestep grids can differ',max_sample_difference_uV=max_sample_difference*1e6,unchanged_signal_core_devices=core)
(R/'verification/views.json').write_text(json.dumps(summary,indent=2));print(summary)
