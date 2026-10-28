v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {capopt2.sym} 350 320 0 0 {name=XC0 style=baseline value=4p}
C {devices/lab_pin.sym} 350 260 0 0 {name=l0a lab=top0}
C {devices/lab_pin.sym} 350 380 0 0 {name=l0b lab=0}
C {devices/lab_pin.sym} 430 380 0 0 {name=l0c lab=0}
C {devices/res.sym} 350 180 0 0 {name=R0 value=1meg}
C {devices/lab_pin.sym} 350 150 0 0 {name=l0d lab=drive}
C {devices/lab_pin.sym} 350 210 0 0 {name=l0e lab=top0}
C {capopt2.sym} 900 320 0 0 {name=XC1 style=compact value=4p}
C {devices/lab_pin.sym} 900 260 0 0 {name=l1a lab=top1}
C {devices/lab_pin.sym} 900 380 0 0 {name=l1b lab=0}
C {devices/lab_pin.sym} 980 380 0 0 {name=l1c lab=0}
C {devices/res.sym} 900 180 0 0 {name=R1 value=1meg}
C {devices/lab_pin.sym} 900 150 0 0 {name=l1d lab=drive}
C {devices/lab_pin.sym} 900 210 0 0 {name=l1e lab=top1}
C {capopt2.sym} 1450 320 0 0 {name=XC2 style=slotted value=4p}
C {devices/lab_pin.sym} 1450 260 0 0 {name=l2a lab=top2}
C {devices/lab_pin.sym} 1450 380 0 0 {name=l2b lab=0}
C {devices/lab_pin.sym} 1530 380 0 0 {name=l2c lab=0}
C {devices/res.sym} 1450 180 0 0 {name=R2 value=1meg}
C {devices/lab_pin.sym} 1450 150 0 0 {name=l2d lab=drive}
C {devices/lab_pin.sym} 1450 210 0 0 {name=l2e lab=top2}
C {devices/vsource.sym} 100 320 0 0 {name=VIN value="pulse(0 1 1u 1n 1n 80u 160u)"}
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
