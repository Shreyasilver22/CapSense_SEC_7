v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {scl08_cap2.sym} 350 300 0 0 {name=XC0 value=2.5p}
C {devices/lab_pin.sym} 350 240 0 0 {name=l0 lab=top0}
C {devices/lab_pin.sym} 350 360 0 0 {name=l1 lab=0}
C {devices/lab_pin.sym} 430 360 0 0 {name=l2 lab=0}
C {devices/res.sym} 350 170 0 0 {name=R0 value=1meg}
C {devices/lab_pin.sym} 350 140 0 0 {name=l3 lab=drive}
C {devices/lab_pin.sym} 350 200 0 0 {name=l4 lab=top0}
C {scl08_cap2.sym} 850 300 0 0 {name=XC1 value=7.5p}
C {devices/lab_pin.sym} 850 240 0 0 {name=l5 lab=top1}
C {devices/lab_pin.sym} 850 360 0 0 {name=l6 lab=0}
C {devices/lab_pin.sym} 930 360 0 0 {name=l7 lab=0}
C {devices/res.sym} 850 170 0 0 {name=R1 value=1meg}
C {devices/lab_pin.sym} 850 140 0 0 {name=l8 lab=drive}
C {devices/lab_pin.sym} 850 200 0 0 {name=l9 lab=top1}
C {scl08_cap2.sym} 1350 300 0 0 {name=XC2 value=3p}
C {devices/lab_pin.sym} 1350 240 0 0 {name=l10 lab=top2}
C {devices/lab_pin.sym} 1350 360 0 0 {name=l11 lab=0}
C {devices/lab_pin.sym} 1430 360 0 0 {name=l12 lab=0}
C {devices/res.sym} 1350 170 0 0 {name=R2 value=1meg}
C {devices/lab_pin.sym} 1350 140 0 0 {name=l13 lab=drive}
C {devices/lab_pin.sym} 1350 200 0 0 {name=l14 lab=top2}
C {devices/vsource.sym} 100 300 0 0 {name=VIN value="pulse(0 1 1u 1n 1n 80u 160u)"}
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
C {devices/launcher.sym} 1800 1200 0 0 {name=PREPARE descr="Save + generate layouts/models for edited values (Ctrl-click)" tclcommand="cap_prepare_current"}
