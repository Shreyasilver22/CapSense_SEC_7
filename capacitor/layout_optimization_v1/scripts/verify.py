from pathlib import Path
import json,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];j=json.loads((R/'results/catalog.json').read_text());checks=[]
def run(cmd,d,log):
 p=subprocess.run(cmd,cwd=d,capture_output=True,text=True,timeout=60);log.write_text(p.stdout+p.stderr);assert p.returncode==0,(cmd,p.stdout,p.stderr)
for c in j['capacitors']:
 name=c['name'];d=R/'results'/name
 net=f'''Transfer current check {name}
.include "../../models/cap_layouts.lib.spice"
VT t 0 dc 0 ac 1
VB b 0 0
VS s 0 0
XC t b s {name}
.control
set wr_singlescale
set wr_vecnames
ac dec 10 1meg 2meg
let cm=abs(imag(i(VB)))/(2*PI*frequency)
let cs=abs(imag(i(VS)))/(2*PI*frequency)
wrdata top.dat real(cm) real(cs)
quit
.endc
.end
''';(d/'top.cir').write_text(net);run(['ngspice','-b','-o','top.log','top.cir'],d,d/'top_run.log');a=np.loadtxt(d/'top.dat',skiprows=1);assert np.allclose(a[:,1],c['Cmut_F'],rtol=1e-6,atol=0);assert np.allclose(a[:,2],c['Ctop_sub_F'],rtol=1e-6,atol=0)
 net=net.replace('VT t 0 dc 0 ac 1','VT t 0 0').replace('VB b 0 0','VB b 0 dc 0 ac 1').replace('imag(i(VB))','imag(i(VT))').replace('top.dat','bottom.dat');(d/'bottom.cir').write_text(net);run(['ngspice','-b','-o','bottom.log','bottom.cir'],d,d/'bottom_run.log');a=np.loadtxt(d/'bottom.dat',skiprows=1);assert np.allclose(a[:,1],c['Cmut_F'],rtol=1e-6,atol=0);assert np.allclose(a[:,2],c['Cbot_sub_F'],rtol=1e-6,atol=0)
 assert abs(c['target_error_percent'])<.2,c['name'];checks.append(dict(name=name,model_currents='PASS',drc_markers=c['drc_markers'],target_error_percent=c['target_error_percent']))
for pins in [3,2]:
 sch=R/'examples/layout_comparison.sch'
 if pins==2:sch=R/'results/two_pin.sch';sch.write_text((R/'examples/layout_comparison.sch').read_text().replace('{capopt3.sym}','{capopt2.sym}'))
 run(['xschem','-x','-q','-n','-s','--rcfile',str(R/'xschemrc'),'-o',str(R/'results'),'-N',f'demo{pins}.spice',str(sch)],R,R/'results'/f'demo{pins}_netlisting.log')
 text=(R/'results'/f'demo{pins}.spice').read_text();suffix='_gnd' if pins==2 else '';expect=f'XC2 top2 0'+(' 0' if pins==3 else '')+' capopt_slotted_4p'+suffix;assert expect in text,text
 (R/'results'/f'demo{pins}.spice').write_text(text.replace('write capopt_demo.raw',f'write demo{pins}.raw'))
 run(['ngspice','-b','-o',f'demo{pins}.log',f'demo{pins}.spice'],R/'results',R/'results'/f'demo{pins}_run.log')
(R/'results/verification.json').write_text(json.dumps(dict(checks=checks,native_symbols='two-pin and three-pin style/value variants netlisted and simulated',physical_qualification='UNRESOLVED extraction-version discrepancy; no formal capacitor LVS or PVT validation'),indent=2));print('All layout-model and native symbol checks passed.')
