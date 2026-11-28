v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {SCL INPUT COMMON-MODE CONTROLLER - STANDALONE TEST} 0 -160 0 0 .55 .55 {}
T {Open XICM to inspect the physical circuit. Supplies and PULSE sources below are testbench stimuli only.} 0 -110 0 0 .28 .28 {}
T {Forced inputs: 2.50 V, then 2.49 V at 181 us, then 2.51 V at 281 us. This tests correction direction, not closed-loop AFE settling.} 0 -70 0 0 .24 .24 {}
C {./ota_input_cm_servo.sym} 460 320 0 0 {name=XICM}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 120 0 0 {name=L1 lab=sump}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 160 0 0 {name=L2 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 200 0 0 {name=L3 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 240 0 0 {name=L4 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 280 0 0 {name=L5 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 320 0 0 {name=L6 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 360 0 0 {name=L7 lab=phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 400 0 0 {name=L8 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 440 0 0 {name=L9 lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 480 0 0 {name=L10 lab=sample_valid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 520 0 0 {name=L11 lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 950 100 0 0 {name=VDD value="5"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 70 0 0 {name=L12 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 950 130 0 0 {name=G0 lab=0}
T {vdd} 850 25 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1600 100 0 0 {name=VREF value="2.5"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 70 0 0 {name=L13 lab=vref}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1600 130 0 0 {name=G1 lab=0}
T {vref} 1500 25 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 950 320 0 0 {name=VP value="PWL(0 2.5 180u 2.5 181u 2.49 280u 2.49 281u 2.51)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 290 0 0 {name=L14 lab=sump}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 950 350 0 0 {name=G2 lab=0}
T {sump} 850 245 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1600 320 0 0 {name=VN value="PWL(0 2.5 180u 2.5 181u 2.49 280u 2.49 281u 2.51)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 290 0 0 {name=L15 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1600 350 0 0 {name=G3 lab=0}
T {sumn} 1500 245 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 950 540 0 0 {name=VCLK value="PULSE(0 5 0 1n 1n 499n 1u)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 510 0 0 {name=L16 lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 950 570 0 0 {name=G4 lab=0}
T {clk_1mhz} 850 465 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1600 540 0 0 {name=VRST value="PWL(0 0 2.25u 0 2.251u 5)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 510 0 0 {name=L17 lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1600 570 0 0 {name=G5 lab=0}
T {rst_n} 1500 465 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 950 760 0 0 {name=VPHI1 value="PULSE(0 5 3u 1n 1n 41u 100u)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 730 0 0 {name=L18 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 950 790 0 0 {name=G6 lab=0}
T {phi1} 850 685 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1600 760 0 0 {name=VPHIT value="PULSE(0 5 48u 1n 1n 45u 100u)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 730 0 0 {name=L19 lab=phit}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1600 790 0 0 {name=G7 lab=0}
T {phit} 1500 685 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 950 980 0 0 {name=VPHI2 value="PULSE(0 5 49u 1n 1n 44u 100u)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 950 0 0 {name=L20 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 950 1010 0 0 {name=G8 lab=0}
T {phi2} 850 905 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1600 980 0 0 {name=VVALID value="PULSE(0 5 83.01u 1n 1n 999n 100u)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 950 0 0 {name=L21 lab=sample_valid}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1600 1010 0 0 {name=G9 lab=0}
T {sample_valid} 1500 905 0 0 .24 .24 {}
C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 30 1200 0 0 {name=SIM only_toplevel=false value=".include /home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/mos/tntp49_5v
.include /home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/res/typ/ppr
.options reltol=4e-4 vntol=3u abstol=1e-11 method=gear maxord=2 klu
.control
set wr_singlescale
set wr_vecnames
set numdgt=12
save v(sump) v(sumn) v(xicm.sample_en) v(sample_valid) v(xicm.xcore.vint) v(xicm.xcore.cm_hold) v(xicm.xcore.cm_x)
tran 100n 400u 0 100n
wrdata controller_standalone.dat v(sump) v(sumn) v(xicm.sample_en) v(sample_valid) v(xicm.xcore.vint) v(xicm.xcore.cm_hold) v(xicm.xcore.cm_x)
.endc"}
