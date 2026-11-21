v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {gm_ota.sym} 600 300 0 0 {name=XG}
C {devices/lab_pin.sym} 500 250 0 0 {name=l1 lab=sense}
C {devices/lab_pin.sym} 500 350 0 0 {name=l2 lab=sp}
C {devices/lab_pin.sym} 600 200 0 0 {name=l3 lab=vdd}
C {devices/lab_pin.sym} 600 400 0 0 {name=l4 lab=0}
C {devices/lab_pin.sym} 560 400 0 0 {name=l5 lab=vbn}
C {devices/lab_pin.sym} 740 300 2 0 {name=l6 lab=out}
C {devices/code_shown.sym} 150 100 0 0 {name=BENCH only_toplevel=true value="
.include /home/your-user/pdk/scl08/ngspice_models49/mos/tntp49_5v
.temp 27
.options reltol=1e-6 vntol=1e-9 abstol=1e-13
VDD vdd 0 5
VBN vbn 0 0.8625
VSP sp 0 2.5
VSENSE sense 0 DC 2.5 AC 1
CL out 0 5p
.control
set wr_singlescale
set wr_vecnames
set numdgt=12
op
print v(out) v(xg.n1) v(xg.tail) i(vdd)
ac dec 100 1 1G
let gr=real(v(out))
let gi=imag(v(out))
wrdata symbol_ac.dat gr gi
quit
.endc
"}
