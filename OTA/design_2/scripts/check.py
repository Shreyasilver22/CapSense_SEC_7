from pathlib import Path
import subprocess,json,numpy as np
R=Path(__file__).resolve().parents[1]
if not (R/'spice/models.inc').exists():raise SystemExit('First run: python3 scripts/configure_models.py /path/to/tntp49_5v')
def run(cmd,cwd):
 p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=90)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
for name in ['selected_ac','selected_small','selected_large','extracted_ac']:
 run(['ngspice','-b','-o','../results/'+name+'.log',name+'.cir'],R/'tb')
a=np.loadtxt(R/'results/selected_ac.dat',skiprows=1);b=np.loadtxt(R/'results/comparison/metal_8p_top_n2/ac.dat',skiprows=1)
assert np.allclose(a,b,rtol=1e-6,atol=1e-6)
run(['xschem','-x','-q','-n','-s','--rcfile',str(R/'xschemrc'),'-o',str(R/'results'),'-N','ota_extracted_cc_tb.spice',str(R/'tb/ota_extracted_cc_tb.sch')],R)
run(['ngspice','-b','-o','ota_extracted_cc_tb.log','ota_extracted_cc_tb.spice'],R/'results')
s=(R/'results/ota_extracted_cc_tb.spice').read_text();assert 'XCC n2 out vss scl08_cap_8p' in s
(R/'results/package_validation.json').write_text(json.dumps({'portable_SPICE_benches':'PASS','AC_matches_saved_comparison':'PASS','native_xschem_testbench':'netlisted and simulated','compensation_pin_mapping':'TOP=n2 BOT=out SUB=vss verified','model_qualification':'provisional; see README'},indent=2))
print('Portable design_2 testbenches and xschem simulation passed.')
