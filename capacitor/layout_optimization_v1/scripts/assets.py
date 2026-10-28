from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];caps=json.loads((R/'results/catalog.json').read_text())['capacitors']
(R/'models/catalog.tcl').write_text('array set capopt_cm_pf {\n'+'\n'.join('{'+c['name']+'} '+f"{c['Cmut_F']*1e12:.8g}" for c in caps)+'\n}\n')
for pins in [2,3]:
 s=f'''v {{xschem version=3.4.4 file_version=1.2}}
G {{}}
K {{type=primitive
format="tcleval(@name @pinlist [capopt_model @style @value {pins} ])"
template="name=XC style=slotted value=4p"}}
V {{}}
S {{}}
E {{}}
L 4 -35 -12 35 -12 {{}}
L 4 -35 12 35 12 {{}}
L 4 0 -60 0 -12 {{}}
L 4 0 12 0 60 {{}}
B 5 -2.5 -62.5 2.5 -57.5 {{name=TOP dir=inout}}
B 5 -2.5 57.5 2.5 62.5 {{name=BOT dir=inout}}
'''
 if pins==3:s+='''L 4 35 12 80 12 {}
L 4 80 12 80 60 {}
B 5 77.5 57.5 82.5 62.5 {name=SUB dir=inout}
T {SUB} 85 50 0 0 0.2 0.2 {}
'''
 s+='''T {@name} 105 -35 0 0 0.3 0.3 {}
T {@style} 105 -10 0 0 0.25 0.25 {}
T {Target: @value} 105 15 0 0 0.25 0.25 {}
T {tcleval([capopt_info @style @value ])} 105 40 0 0 0.2 0.2 {}
'''
 if pins==2:s+='T {SUB internally tied to 0} 105 62 0 0 0.17 0.17 {}\n'
 (R/'symbols'/f'capopt{pins}.sym').write_text(s)
s='''v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
'''
for i,style in enumerate(['baseline','compact','slotted']):
 x=350+i*550
 s+=f'''C {{capopt3.sym}} {x} 320 0 0 {{name=XC{i} style={style} value=4p}}
C {{devices/lab_pin.sym}} {x} 260 0 0 {{name=l{i}a lab=top{i}}}
C {{devices/lab_pin.sym}} {x} 380 0 0 {{name=l{i}b lab=0}}
C {{devices/lab_pin.sym}} {x+80} 380 0 0 {{name=l{i}c lab=0}}
C {{devices/res.sym}} {x} 180 0 0 {{name=R{i} value=1meg}}
C {{devices/lab_pin.sym}} {x} 150 0 0 {{name=l{i}d lab=drive}}
C {{devices/lab_pin.sym}} {x} 210 0 0 {{name=l{i}e lab=top{i}}}
'''
s+='''C {devices/vsource.sym} 100 320 0 0 {name=VIN value="pulse(0 1 1u 1n 1n 80u 160u)"}
C {devices/lab_pin.sym} 100 290 0 0 {name=ld lab=drive}
C {devices/lab_pin.sym} 100 350 0 0 {name=lg lab=0}
C {devices/code_shown.sym} 100 600 0 0 {name=MODELS only_toplevel=true value=".include ../models/cap_layouts.lib.spice"}
C {devices/code_shown.sym} 850 600 0 0 {name=RUN only_toplevel=true value=".control
set filetype=binary
tran 5n 100u
write capopt_demo.raw v(drive) v(top0) v(top1) v(top2)
quit
.endc"}
T {Layout comparison - select capacitor, press q, edit style/value} 100 40 0 0 0.4 0.4 {}
T {Prepared styles: baseline, compact, slotted. Prepared values: 3p, 4p, 8p.
All models retain substrate capacitance. Values are experimental extraction estimates.} 100 85 0 0 0.25 0.25 {}
B 2 2000 150 3200 850 {flags=graph,unlocked
y1=0
y2=1.1
x1=0
x2=0.0001
node="v(drive) v(top0) v(top1) v(top2)"
color="4 7 6 5"
dataset=-1
logx=0
logy=0}
C {devices/launcher.sym} 2000 1000 0 0 {name=RUNPLOT descr="Run simulation + plot (Ctrl-click)" tclcommand="xschem netlist; simulate {cap_load_plot}"}
'''
(R/'examples/layout_comparison.sch').write_text(s)
print('Generated editable style/value symbols and xschem comparison')
