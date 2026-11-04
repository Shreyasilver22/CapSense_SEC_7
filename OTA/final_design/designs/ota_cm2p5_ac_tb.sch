v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {ota_cm2p5.sym} 400 300 0 0 {name=XOTA}
C {devices/lab_pin.sym} 290 210 0 0 {name=PIN_INP lab=inp}
C {devices/lab_pin.sym} 290 240 0 0 {name=PIN_INN lab=inn}
C {devices/lab_pin.sym} 510 210 0 0 {name=PIN_OUTP lab=op}
C {devices/lab_pin.sym} 510 240 0 0 {name=PIN_OUTM lab=om}
C {devices/lab_pin.sym} 400 150 0 0 {name=PIN_VDD lab=vdd}
C {devices/lab_pin.sym} 400 450 0 0 {name=PIN_VSS lab=0}
C {devices/lab_pin.sym} 290 320 0 0 {name=PIN_IREF lab=bn}
C {devices/lab_pin.sym} 290 355 0 0 {name=PIN_VCM lab=vcm}
C {devices/lab_pin.sym} 290 390 0 0 {name=PIN_VBN lab=vbn}
C {devices/lab_pin.sym} 290 420 0 0 {name=PIN_VBP lab=vbp}
C {devices/code.sym} 700 100 0 0 {name=TESTBENCH only_toplevel=false value=".include \"../models/scl08_models.inc\"
.include \"../models/ota_cm2p5_C.spice\"
.temp 27
.options reltol=1e-5 vntol=1e-8 abstol=1e-12
VDD vdd 0 5
IREF vdd bn 3.5u
VCM vcm 0 2.5
VBN vbn 0 3
VBP vbp vdd -2.2
CLP op 0 5p
CLM om 0 5p
VCMD cmd 0 dc 0 ac 1
VICM icm 0 2.5
EIP inp icm cmd fb 0.5
EIM inn icm fb cmd 0.5
EOD od 0 op om 1
LDC od fb 1e12
CAC fb 0 1e12
.control
set wr_singlescale
set wr_vecnames
op
print v(op) v(om) i(vdd)
ac dec 80 0.01 1G
let gr=real(v(od))
let gi=imag(v(od))
wrdata ac.dat gr gi
write ota_cm2p5_ac.raw
quit
.endc"}
T {Input CM = 2.5 V; output CM target = 2.5 V; VBN = 3.0 V.
ac benchmark; ideal bias sources and feedback fixture.} 100 520 0 0 0.3 0.3 {}
