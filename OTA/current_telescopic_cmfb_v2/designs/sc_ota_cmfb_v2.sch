v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {ota_cmfb_v2.sym} 400 300 0 0 {name=XOTA}
C {devices/lab_pin.sym} 290 210 0 0 {name=PIN_INP lab=ref}
C {devices/lab_pin.sym} 290 240 0 0 {name=PIN_INN lab=sum}
C {devices/lab_pin.sym} 510 210 0 0 {name=PIN_OUTP lab=out}
C {devices/lab_pin.sym} 510 240 0 0 {name=PIN_OUTM lab=other}
C {devices/lab_pin.sym} 400 150 0 0 {name=PIN_VDD lab=vdd}
C {devices/lab_pin.sym} 400 450 0 0 {name=PIN_VSS lab=0}
C {devices/lab_pin.sym} 290 320 0 0 {name=PIN_IREF lab=bias}
C {devices/lab_pin.sym} 290 355 0 0 {name=PIN_VCM lab=vcm}
C {devices/lab_pin.sym} 290 390 0 0 {name=PIN_VBN lab=vbn}
C {devices/lab_pin.sym} 290 420 0 0 {name=PIN_VBP lab=vbp}
C {devices/code.sym} 700 100 0 0 {name=SC_network only_toplevel=false value=".include \"/home/berson_meshak/pdk/scl08/ngspice_models49/mos/tntp49_5v\"
.include \"/home/berson_meshak/pdk/scl08/ngspice_models49/res/typ/ppr\"
.include \"../models/ota_cmfb_v2_C.spice\"
.temp 27
.options reltol=1e-5 vntol=1e-8 abstol=1e-12 numdgt=12 method=gear maxord=2
VDD vdd 0 5
VREF ref 0 1.5
VP vp 0 0.3
IREF vdd bias 3.5u
CS tx rx 2.5p
CF sum out 7.5p
CL out 0 5p
VCM vcm 0 2.5
VBN vbn 0 2.4
VBP vbp vdd -2.2
COM other 0 5p
Vp1 p1 0 PWL(0 0 5.04e-05 0 5.041e-05 5 5.9e-05 5 5.901e-05 0 7.04e-05 0 7.041e-05 5 7.9e-05 5 7.901e-05 0 9.04e-05 0 9.041e-05 5 9.9e-05 5 9.901e-05 0 0.0001304 0 0.00013041 5 0.000139 5 0.00013901 0 0.0001504 0 0.00015041 5 0.000159 5 0.00015901 0 0.0001704 0 0.00017041 5 0.000179 5 0.00017901 0 0.00021 0)
Vp2 p2 0 PWL(0 0 6.04e-05 0 6.041e-05 5 6.9e-05 5 6.901e-05 0 8.04e-05 0 8.041e-05 5 8.9e-05 5 8.901e-05 0 0.0001004 0 0.00010041 5 0.000109 5 0.00010901 0 0.0001404 0 0.00014041 5 0.000149 5 0.00014901 0 0.0001604 0 0.00016041 5 0.000169 5 0.00016901 0 0.0001804 0 0.00018041 5 0.000189 5 0.00018901 0 0.00021 0)
Vrst rst 0 PWL(0 5 4.9e-05 5 4.901e-05 0 0.0001104 0 0.00011041 5 0.000129 5 0.00012901 0 0.00021 0)
Bp1b p1b 0 V=5-v(p1)
Bp2b p2b 0 V=5-v(p2)
Brstb rstb 0 V=5-v(rst)
MN0 tx p1 vp 0 N W=10u L=0.8u
MP0 tx p1b vp vdd P W=20u L=0.8u
MN1 tx p2 0 0 N W=10u L=0.8u
MP1 tx p2b 0 vdd P W=20u L=0.8u
MN2 rx p1 0 0 N W=10u L=0.8u
MP2 rx p1b 0 vdd P W=20u L=0.8u
MN3 rx p2 sum 0 N W=10u L=0.8u
MP3 rx p2b sum vdd P W=20u L=0.8u
MN4 sum rst out 0 N W=10u L=0.8u
MP4 sum rstb out vdd P W=20u L=0.8u
.control
set wr_singlescale
set wr_vecnames
tran 10n 0.00021
wrdata xschem_SC.dat v(out) v(sum) v(other) v(p1) v(p2) v(rst) i(vdd)
quit
.endc"}
T {Verified-layout OTA symbol in the original SC testbench
Double-click SC_network for the capacitor, switch, clock and analysis definitions.
Model includes and output data are relative to the tb directory.} 100 520 0 0 0.3 0.3 {}
