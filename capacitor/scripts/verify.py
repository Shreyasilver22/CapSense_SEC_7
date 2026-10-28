from pathlib import Path
import json,subprocess,os
import numpy as np
from common import ROOT as R
j=json.loads((R/'results/catalog.json').read_text());checks=[]
def run(cmd,cwd,log):
 p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=90,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'});log.write_text(p.stdout+p.stderr);assert p.returncode==0,(cmd,p.stdout,p.stderr)
for c in j['capacitors']:
 token=c['value'];d=R/'results'/('verify_'+token.replace('.','p'));d.mkdir(exist_ok=True)
 net=f'''Check extracted alias for {token}
.include "../../models/generated_caps.lib.spice"
VTOP top 0 dc 0 ac 1
VBOT bot 0 0
VSUB sub 0 0
XC top bot sub scl08_cap_{token}
.control
set wr_singlescale
set wr_vecnames
ac dec 10 1meg 2meg
let cm=abs(imag(i(VBOT)))/(2*PI*frequency)
let ct=abs(imag(i(VSUB)))/(2*PI*frequency)
wrdata top.dat real(cm) real(ct)
quit
.endc
.end
'''
 (d/'top.cir').write_text(net);run(['ngspice','-b','-o','top.log','top.cir'],d,d/'top_run.log');a=np.atleast_2d(np.loadtxt(d/'top.dat',skiprows=1));assert np.allclose(a[:,1],c['Cmut_F'],rtol=1e-6,atol=0);assert np.allclose(a[:,2],c['Ctop_sub_F'],rtol=1e-6,atol=0)
 net=net.replace('VTOP top 0 dc 0 ac 1','VTOP top 0 0').replace('VBOT bot 0 0','VBOT bot 0 dc 0 ac 1').replace('imag(i(VBOT))','imag(i(VTOP))').replace('top.dat','bottom.dat')
 (d/'bottom.cir').write_text(net);run(['ngspice','-b','-o','bottom.log','bottom.cir'],d,d/'bottom_run.log');a=np.atleast_2d(np.loadtxt(d/'bottom.dat',skiprows=1));assert np.allclose(a[:,1],c['Cmut_F'],rtol=1e-6,atol=0);assert np.allclose(a[:,2],c['Cbot_sub_F'],rtol=1e-6,atol=0)
 checks.append(dict(value=token,plate_transfer_and_substrate_currents='PASS',cell=c['cell'],drc_markers=c['drc_markers']))
for sch,out in [('value_demo.sch','value_demo.spice'),('sc_feedback_fragment.sch','sc_feedback_fragment.spice')]:
 run(['xschem','-x','-q','-n','-s','--rcfile',str(R/'xschemrc'),'-o',str(R/'results'),'-N',out,str(R/'examples'/sch)],R,R/'results'/(out+'.netlisting.log'))
text=(R/'results/sc_feedback_fragment.spice').read_text();assert 'XCFB SUM VOUT VSUB scl08_cap_2.5p' in text,text
run(['ngspice','-b','-o','value_demo.log','value_demo.spice'],R/'results',R/'results/value_demo_run.log')
assert 'Error' not in (R/'results/value_demo.log').read_text()
# Netlist the two-pin SYMBOL too, rather than only testing its SPICE wrapper.
s=(R/'examples/value_demo.sch').read_text().replace('{scl08_cap3.sym}','{scl08_cap2.sym}');(R/'results/two_pin_symbols.sch').write_text(s)
run(['xschem','-x','-q','-n','-s','--rcfile',str(R/'xschemrc'),'-o',str(R/'results'),'-N','two_pin_symbols.spice',str(R/'results/two_pin_symbols.sch')],R,R/'results/two_pin_symbols_netlist.log')
s=(R/'results/two_pin_symbols.spice').read_text().replace('write capacitor_demo.raw','write two_pin_symbols.raw');(R/'results/two_pin_symbols.spice').write_text(s);assert 'XC0 top0 0 scl08_cap_gnd_2.5p' in s
run(['ngspice','-b','-o','two_pin_symbols.log','two_pin_symbols.spice'],R/'results',R/'results/two_pin_symbols_run.log')
# Run the additional two-pin current and four-weight CDAC examples.
for name in ['two_pin_demo','cdac_four_weights']:run(['ngspice','-b','-o',str(R/'results'/(name+'.log')),name+'.cir'],R/'examples',R/'results'/(name+'_run.log'))
c=next(x for x in j['capacitors'] if x['value']=='2.5p');a=np.loadtxt(R/'results/two_pin.dat',skiprows=1);freq=a[:,0];assert np.allclose(abs(a[:,2])/(2*np.pi*freq),c['Cmut_F']+c['Ctop_sub_F'],rtol=1e-6,atol=0);assert np.allclose(abs(a[:,4])/(2*np.pi*freq),c['Cmut_F'],rtol=1e-6,atol=0)
# Verify the charge-sharing plateaus, not ADC resolution or conversion behavior.
weights=[next(x for x in j['capacitors'] if x['units']==n) for n in [1,2,4,8]];den=sum(x['Cmut_F']+x['Ctop_sub_F'] for x in weights);t=np.loadtxt(R/'results/cdac.dat',skiprows=1);expected=[];measured=[]
for i,time in enumerate([2e-6,4e-6,6e-6,8e-6]):
 v=sum(x['Cmut_F'] for x in weights[:i+1])/den;actual=float(np.interp(time,t[:,0],t[:,1]));assert abs(v-actual)<1e-4,(v,actual);expected.append(v);measured.append(actual)
# Confirm independent value preparation generated the requested model and layout.
workflow=R/'results/prepare_workflow/request_4p.sch';assert workflow.exists()
run(['xschem','-x','-q','-n','-s','--rcfile',str(R/'xschemrc'),'-o',str(R/'results'),'-N','prepared_4p.spice',str(workflow)],R,R/'results/prepared_4p_netlist.log')
s=(R/'results/prepared_4p.spice').read_text().replace('write capacitor_demo.raw','write prepared_4p.raw');(R/'results/prepared_4p.spice').write_text(s);assert 'XC0 top0 0 0 scl08_cap_4p' in s;run(['ngspice','-b','-o','prepared_4p.log','prepared_4p.spice'],R/'results',R/'results/prepared_4p_run.log');assert (R/'layouts/requested_4p.gds').exists()
ratio=next(x for x in j['capacitors'] if x['value']=='7.5p')['Cmut_F']/c['Cmut_F'];assert abs(ratio-3)<1e-8
summary=dict(status='PASS for documented layout, model, symbol and value-to-layout workflow checks; not foundry qualification',checks=checks,nominal_7p5_to_2p5_ratio=ratio,cdac_expected_V=expected,cdac_measured_V=measured,three_pin_symbol='netlisted and simulated',two_pin_symbol='netlisted and simulated; substrate parasitics retained',sc_feedback_pin_mapping='SUM VOUT VSUB verified',new_value_workflow='4p scanned from schematic, model/layout generated and simulated',magic_compatibility='UNRESOLVED; inherited old-version/native-export discrepancy',capacitor_LVS='NOT provided by stock device deck')
run(['xschem','-x','-q','-r','--rcfile',str(R/'xschemrc'),'--command','xschem print svg {'+str(R/'plots/value_symbols.svg')+'} 1600 700 40 0 1750 760',str(R/'examples/value_demo.sch')],R,R/'results/symbol_export.log')
svg=(R/'plots/value_symbols.svg').read_text()
for value in ['2.5p','7.5p','3p']:
 cell=next(c for c in j['capacitors'] if c['value']==value)
 assert ('Extracted: %.8g pF' % (cell['Cmut_F']*1e12)) in svg
summary['displayed_target_and_extracted_values']='native SVG strings verified'
(R/'results/verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
