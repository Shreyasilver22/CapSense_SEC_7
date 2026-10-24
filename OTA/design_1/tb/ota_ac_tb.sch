v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {ota_scl08.sym} 500 300 0 0 {name=XU}
C {devices/lab_pin.sym} 380 250 0 0 {name=l24 sig_type=std_logic lab=inp}
C {devices/lab_pin.sym} 380 350 0 0 {name=l25 sig_type=std_logic lab=inn}
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
C {devices/vsource.sym} 1000 600 0 0 {name=VIN value="dc 2.5 ac 0.5"}
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
ac dec 100 1 1G
let gain_db = db(v(out))
let phase_deg = 180/PI*cph(v(out))
meas ac gain_1hz find gain_db at=1
meas ac ugf when gain_db=0 fall=1
meas ac phase_ugf find phase_deg when gain_db=0 fall=1
write ota_ac_tb.raw v(out) gain_db phase_deg
quit
.endc"}
T {SCL08 OTA - open-loop differential AC test} 100 30 0 0 0.5 0.5 {}
T {AC differential input = 1 V. Equal DC inputs = 2.5 V.
Same seven-transistor baseline; CL = 5 pF.} 100 80 0 0 0.3 0.3 {}
C {devices/vsource.sym} 450 600 0 0 {name=VINN value="dc 2.5 ac 0.5 180"}
C {devices/lab_pin.sym} 450 570 0 0 {name=l_ac_inn lab=inn}
C {devices/lab_pin.sym} 450 630 0 0 {name=l_ac_gnd lab=0}
B 2 1200 150 2400 650 {flags=graph,unlocked
y1=-100
y2=45
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=9
divx=6
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="\"Gain_dB;v(out) db20()\""
color="4"
dataset=-1
unitx=1
logx=1
logy=0
rainbow=0}
B 2 1200 750 2400 1250 {flags=graph,unlocked
y1=-270
y2=0
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=9
divx=6
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="\"Phase_deg;phase_deg -1 *\""
color="7"
dataset=-1
unitx=1
logx=1
logy=0
rainbow=0}
T {Open-loop gain (dB), frequency (Hz)} 1200 100 0 0 0.4 0.4 {}
T {Unwrapped phase (degrees), frequency (Hz)} 1200 700 0 0 0.4 0.4 {}
C {devices/launcher.sym} 1200 1380 0 0 {name=LOAD_AC descr="Load / refresh AC plots (Ctrl-click)" tclcommand="xschem raw_clear; xschem raw_read $netlist_dir/ota_ac_tb.raw ac; xschem redraw"}
C {devices/launcher.sym} 1200 1480 0 0 {name=RUN_AND_PLOT descr="Run simulation + plot (Ctrl-click)" tclcommand="xschem netlist; simulate {ota_load_plot ota_ac_tb.raw ac}"}
