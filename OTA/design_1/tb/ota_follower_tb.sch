v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {ota_scl08.sym} 500 300 0 0 {name=XU}
C {devices/lab_pin.sym} 380 250 0 0 {name=l24 sig_type=std_logic lab=inp}
C {devices/lab_pin.sym} 380 350 0 0 {name=l25 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 640 300 0 0 {name=l26 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 500 160 0 0 {name=l27 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 500 440 0 0 {name=l28 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 460 440 0 0 {name=l29 sig_type=std_logic lab=vbn}
C {devices/vsource.sym} 100 600 0 0 {name=VDD value="5"}
C {devices/lab_pin.sym} 100 570 0 0 {name=l30 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 100 630 0 0 {name=l31 sig_type=std_logic lab=0}
C {devices/vsource.sym} 240 600 0 0 {name=VBN value="0.95"}
C {devices/lab_pin.sym} 240 570 0 0 {name=l32 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 240 630 0 0 {name=l33 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1000 600 0 0 {name=VIN value="dc 2.5 pulse(2.5 2.6 20u 100n 100n 40u 80u)"}
C {devices/lab_pin.sym} 1000 570 0 0 {name=l34 sig_type=std_logic lab=inp}
C {devices/lab_pin.sym} 1000 630 0 0 {name=l35 sig_type=std_logic lab=0}
C {devices/capa.sym} 800 350 0 0 {name=CL value=5p m=1}
C {devices/lab_pin.sym} 800 320 0 0 {name=l36 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 800 380 0 0 {name=l37 sig_type=std_logic lab=0}
C {devices/code_shown.sym} 100 800 0 0 {name=MODELS only_toplevel=true value=".include ../spice/models.inc
.temp 27"}
C {devices/code_shown.sym} 700 800 0 0 {name=RUN only_toplevel=true value=".control
set noaskquit
set filetype=binary
op
print v(out) i(VDD)
tran 20n 120u
let tracking_error = v(out)-v(inp)
meas tran output_high find v(out) at=59u
meas tran output_low find v(out) at=99u
write ota_follower_tb.raw v(inp) v(out) tracking_error
quit
.endc"}
T {SCL08 OTA - unity-gain follower demonstration} 100 30 0 0 0.5 0.5 {}
T {Use the ota_scl08 symbol in your switched-capacitor circuit.
Connect all six pins; keep the external VBN bias supply.} 100 80 0 0 0.3 0.3 {}
B 2 1200 150 2400 650 {flags=graph,unlocked
y1=2.48
y2=2.64
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.00012
divx=6
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="v(inp) v(out)"
color="4 7"
dataset=-1
unitx=1
logx=0
logy=0
rainbow=0}
B 2 1200 750 2400 1250 {flags=graph,unlocked
y1=-0.1
y2=0.12
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.00012
divx=6
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="tracking_error"
color="6"
dataset=-1
unitx=1
logx=0
logy=0
rainbow=0}
T {Transient: input and output (V)} 1200 100 0 0 0.4 0.4 {}
T {Tracking error: Vout - Vin (V)} 1200 700 0 0 0.4 0.4 {}
C {devices/launcher.sym} 1200 1380 0 0 {name=LOAD_TRAN descr="Load / refresh transient plots (Ctrl-click)" tclcommand="xschem raw_clear; xschem raw_read $netlist_dir/ota_follower_tb.raw tran; xschem redraw"}
C {devices/launcher.sym} 1200 1480 0 0 {name=RUN_AND_PLOT descr="Run simulation + plot (Ctrl-click)" tclcommand="xschem netlist; simulate {ota_load_plot ota_follower_tb.raw tran}"}
