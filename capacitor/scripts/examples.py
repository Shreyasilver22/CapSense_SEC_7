from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
# Place the SAME symbol three times; value alone selects the generated physical variant.
s='''v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
'''
labels=0
for idx,(val,x) in enumerate([('2.5p',350),('7.5p',850),('3p',1350)]):
 s+=f'''C {{scl08_cap3.sym}} {x} 300 0 0 {{name=XC{idx} value={val}}}
C {{devices/lab_pin.sym}} {x} 240 0 0 {{name=l{labels} lab=top{idx}}}
C {{devices/lab_pin.sym}} {x} 360 0 0 {{name=l{labels+1} lab=0}}
C {{devices/lab_pin.sym}} {x+80} 360 0 0 {{name=l{labels+2} lab=0}}
C {{devices/res.sym}} {x} 170 0 0 {{name=R{idx} value=1meg}}
C {{devices/lab_pin.sym}} {x} 140 0 0 {{name=l{labels+3} lab=drive}}
C {{devices/lab_pin.sym}} {x} 200 0 0 {{name=l{labels+4} lab=top{idx}}}
''';labels+=5
s+='''C {devices/vsource.sym} 100 300 0 0 {name=VIN value="pulse(0 1 1u 1n 1n 80u 160u)"}
C {devices/lab_pin.sym} 100 270 0 0 {name=ld lab=drive}
C {devices/lab_pin.sym} 100 330 0 0 {name=lg lab=0}
C {devices/code_shown.sym} 100 500 0 0 {name=MODEL only_toplevel=true value=".include ../models/generated_caps.lib.spice"}
C {devices/code_shown.sym} 850 500 0 0 {name=RUN only_toplevel=true value=".control
set filetype=binary
tran 5n 100u
write capacitor_demo.raw v(drive) v(top0) v(top1) v(top2)
quit
.endc"}
T {Editable capacitors: select instance, press q, change value} 100 30 0 0 0.4 0.4 {}
T {2.5p, 7.5p and 3p are prepared. For a new value, run scripts/prepare.py before simulating.
Symbol shows requested and extracted Cmut. All parasitics remain in the model.} 100 65 0 0 0.25 0.25 {}
B 2 1800 150 3000 850 {flags=graph,unlocked
y1=0
y2=1.1
x1=0
x2=0.0001
divy=5
divx=5
node="v(drive) v(top0) v(top1) v(top2)"
color="4 7 6 5"
dataset=-1
logx=0
logy=0}
C {devices/launcher.sym} 1800 1000 0 0 {name=RUN_AND_PLOT descr="Run simulation + plot (Ctrl-click)" tclcommand="xschem netlist; simulate {cap_load_plot}"}
C {devices/launcher.sym} 1800 1100 0 0 {name=LOAD descr="Load / refresh plot (Ctrl-click)" tclcommand="cap_load_plot"}
'''
s+='C {devices/launcher.sym} 1800 1200 0 0 {name=PREPARE descr="Save + generate layouts/models for edited values (Ctrl-click)" tclcommand="cap_prepare_current"}\n'
(R/'examples/value_demo.sch').write_text(s)
# A reusable connection fragment for C_FB in the user's figure; no value assignment is frozen.
frag='''v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {scl08_cap3.sym} 400 300 0 0 {name=XCFB value=2.5p}
C {devices/iopin.sym} 400 180 0 0 {name=p1 lab=SUM}
N 400 180 400 240 {lab=SUM}
C {devices/iopin.sym} 400 420 0 0 {name=p2 lab=VOUT}
N 400 360 400 420 {lab=VOUT}
C {devices/iopin.sym} 580 420 0 0 {name=p3 lab=VSUB}
N 480 360 580 360 {lab=VSUB}
N 580 360 580 420 {lab=VSUB}
T {C_FB connection fragment for the attached SC integrator} 100 40 0 0 0.4 0.4 {}
T {SUM = OTA inverting input after the phase-2 switch.
VOUT = OTA output. VSUB = substrate ground, not VREF.
Place reset switch across SUM and VOUT as in the figure.
2.5p is illustrative; capacitor roles are not yet assigned.
This fragment is not a complete SC integrator simulation.} 100 520 0 0 0.28 0.28 {}
'''
(R/'examples/sc_feedback_fragment.sch').write_text(frag)
# Plain SPICE: passive CDAC illustration only, not a SAR ADC implementation.
cdac='''Illustrative 4-weight capacitive DAC with substrate parasitics, not a SAR ADC
.include "../models/generated_caps.lib.spice"
RINIT dac 0 1e12
'''
for idx,value in enumerate(['11.384f','22.768f','45.536f','91.072f']):
 cdac+=f'VBIT{idx} b{idx} 0 pulse(0 1 {1+idx*2}u 1n 1n 30u 60u)\nXBIT{idx} dac b{idx} 0 scl08_cap_{value}\n'
cdac+='''.control
set wr_singlescale
set wr_vecnames
tran 1n 10u
wrdata ../results/cdac.dat v(dac) v(b0) v(b1) v(b2) v(b3)
quit
.endc
.end
'''
(R/'examples/cdac_four_weights.cir').write_text(cdac)
# Explicit two-pin example proves substrate parasitics are retained, not removed.
(R/'examples/two_pin_demo.cir').write_text('''Two-pin convenience symbol model, substrate internally grounded
.include "../models/generated_caps.lib.spice"
VTOP top 0 dc 0 ac 1
VBOT bot 0 0
XCAP top bot scl08_cap_gnd_2.5p
.control
set wr_singlescale
set wr_vecnames
ac dec 10 1meg 2meg
wrdata ../results/two_pin.dat real(i(VTOP)) imag(i(VTOP)) real(i(VBOT)) imag(i(VBOT))
quit
.endc
.end
''')
print('Generated value-editing, SC wiring fragment, two-pin and CDAC examples')
