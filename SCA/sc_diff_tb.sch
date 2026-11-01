v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {SCL CP8D 5 V | Differential SC sensor readout | First simulation prototype} -650 -380 0 0 0.55 0.55 {}
T {Two copies of the supplied charge amplifier; differential output = V(outp)-V(outn). Amplifiers are behavioral placeholders.} -650 -320 0 0 0.32 0.32 {}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} -470 0 0 0 {name=xdrive_p}
C {lab_pin.sym} -620 -40 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -320 -40 0 0 {name=p2 sig_type=std_logic lab=phi1}
C {lab_pin.sym} -320 -20 0 0 {name=p3 sig_type=std_logic lab=0}
C {lab_pin.sym} -320 0 0 0 {name=p4 sig_type=std_logic lab=txp}
C {lab_pin.sym} -320 20 0 0 {name=p5 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -320 40 0 0 {name=p6 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} -470 180 0 0 {name=xdischarge_p}
C {lab_pin.sym} -620 140 0 0 {name=p7 sig_type=std_logic lab=0}
C {lab_pin.sym} -320 140 0 0 {name=p8 sig_type=std_logic lab=phi2}
C {lab_pin.sym} -320 160 0 0 {name=p9 sig_type=std_logic lab=0}
C {lab_pin.sym} -320 180 0 0 {name=p10 sig_type=std_logic lab=txp}
C {lab_pin.sym} -320 200 0 0 {name=p11 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -320 220 0 0 {name=p12 sig_type=std_logic lab=phi2b}
C {capa.sym} 0 0 1 0 {name=CSp value=\{CP\} m=1}
C {lab_pin.sym} -30 0 0 0 {name=p13 sig_type=std_logic lab=txp}
C {lab_pin.sym} 30 0 0 0 {name=p14 sig_type=std_logic lab=rxp}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} 80 220 0 0 {name=xclamp_p}
C {lab_pin.sym} -70 180 0 0 {name=p15 sig_type=std_logic lab=0}
C {lab_pin.sym} 230 180 0 0 {name=p16 sig_type=std_logic lab=phi1}
C {lab_pin.sym} 230 200 0 0 {name=p17 sig_type=std_logic lab=0}
C {lab_pin.sym} 230 220 0 0 {name=p18 sig_type=std_logic lab=rxp}
C {lab_pin.sym} 230 240 0 0 {name=p19 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 230 260 0 0 {name=p20 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} 390 0 0 0 {name=xtransfer_p}
C {lab_pin.sym} 240 -40 0 0 {name=p21 sig_type=std_logic lab=rxp}
C {lab_pin.sym} 540 -40 0 0 {name=p22 sig_type=std_logic lab=phi2}
C {lab_pin.sym} 540 -20 0 0 {name=p23 sig_type=std_logic lab=0}
C {lab_pin.sym} 540 0 0 0 {name=p24 sig_type=std_logic lab=sump}
C {lab_pin.sym} 540 20 0 0 {name=p25 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 540 40 0 0 {name=p26 sig_type=std_logic lab=phi2b}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} 850 -190 0 0 {name=xreset_p}
C {lab_pin.sym} 700 -230 0 0 {name=p27 sig_type=std_logic lab=sump}
C {lab_pin.sym} 1000 -230 0 0 {name=p28 sig_type=std_logic lab=phi1}
C {lab_pin.sym} 1000 -210 0 0 {name=p29 sig_type=std_logic lab=0}
C {lab_pin.sym} 1000 -190 0 0 {name=p30 sig_type=std_logic lab=outp}
C {lab_pin.sym} 1000 -170 0 0 {name=p31 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1000 -150 0 0 {name=p32 sig_type=std_logic lab=phi1b}
C {capa.sym} 870 -80 1 0 {name=CFp value=\{CF\} m=1}
C {lab_pin.sym} 840 -80 0 0 {name=p33 sig_type=std_logic lab=sump}
C {lab_pin.sym} 900 -80 0 0 {name=p34 sig_type=std_logic lab=outp}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/amp_behavioral.sym} 850 80 0 0 {name=xamp_p}
C {lab_pin.sym} 770 50 0 0 {name=p35 sig_type=std_logic lab=vref}
C {lab_pin.sym} 770 110 0 0 {name=p36 sig_type=std_logic lab=sump}
C {lab_pin.sym} 930 80 0 0 {name=p37 sig_type=std_logic lab=outp}
T {Sensor P | C=CP | Cf=40 pF | phi1=sample/reset, phi2=transfer} -650 320 0 0 0.3 0.3 {}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} -470 650 0 0 {name=xdrive_n}
C {lab_pin.sym} -620 610 0 0 {name=p38 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -320 610 0 0 {name=p39 sig_type=std_logic lab=phi1}
C {lab_pin.sym} -320 630 0 0 {name=p40 sig_type=std_logic lab=0}
C {lab_pin.sym} -320 650 0 0 {name=p41 sig_type=std_logic lab=txn}
C {lab_pin.sym} -320 670 0 0 {name=p42 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -320 690 0 0 {name=p43 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} -470 830 0 0 {name=xdischarge_n}
C {lab_pin.sym} -620 790 0 0 {name=p44 sig_type=std_logic lab=0}
C {lab_pin.sym} -320 790 0 0 {name=p45 sig_type=std_logic lab=phi2}
C {lab_pin.sym} -320 810 0 0 {name=p46 sig_type=std_logic lab=0}
C {lab_pin.sym} -320 830 0 0 {name=p47 sig_type=std_logic lab=txn}
C {lab_pin.sym} -320 850 0 0 {name=p48 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -320 870 0 0 {name=p49 sig_type=std_logic lab=phi2b}
C {capa.sym} 0 650 1 0 {name=CSn value=\{CN\} m=1}
C {lab_pin.sym} -30 650 0 0 {name=p50 sig_type=std_logic lab=txn}
C {lab_pin.sym} 30 650 0 0 {name=p51 sig_type=std_logic lab=rxn}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} 80 870 0 0 {name=xclamp_n}
C {lab_pin.sym} -70 830 0 0 {name=p52 sig_type=std_logic lab=0}
C {lab_pin.sym} 230 830 0 0 {name=p53 sig_type=std_logic lab=phi1}
C {lab_pin.sym} 230 850 0 0 {name=p54 sig_type=std_logic lab=0}
C {lab_pin.sym} 230 870 0 0 {name=p55 sig_type=std_logic lab=rxn}
C {lab_pin.sym} 230 890 0 0 {name=p56 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 230 910 0 0 {name=p57 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} 390 650 0 0 {name=xtransfer_n}
C {lab_pin.sym} 240 610 0 0 {name=p58 sig_type=std_logic lab=rxn}
C {lab_pin.sym} 540 610 0 0 {name=p59 sig_type=std_logic lab=phi2}
C {lab_pin.sym} 540 630 0 0 {name=p60 sig_type=std_logic lab=0}
C {lab_pin.sym} 540 650 0 0 {name=p61 sig_type=std_logic lab=sumn}
C {lab_pin.sym} 540 670 0 0 {name=p62 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 540 690 0 0 {name=p63 sig_type=std_logic lab=phi2b}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/TG_scl_checked.sym} 850 460 0 0 {name=xreset_n}
C {lab_pin.sym} 700 420 0 0 {name=p64 sig_type=std_logic lab=sumn}
C {lab_pin.sym} 1000 420 0 0 {name=p65 sig_type=std_logic lab=phi1}
C {lab_pin.sym} 1000 440 0 0 {name=p66 sig_type=std_logic lab=0}
C {lab_pin.sym} 1000 460 0 0 {name=p67 sig_type=std_logic lab=outn}
C {lab_pin.sym} 1000 480 0 0 {name=p68 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1000 500 0 0 {name=p69 sig_type=std_logic lab=phi1b}
C {capa.sym} 870 570 1 0 {name=CFn value=\{CF\} m=1}
C {lab_pin.sym} 840 570 0 0 {name=p70 sig_type=std_logic lab=sumn}
C {lab_pin.sym} 900 570 0 0 {name=p71 sig_type=std_logic lab=outn}
C {/home/shreyas/Desktop/Sec_7/designs/sc_diff_scl/amp_behavioral.sym} 850 730 0 0 {name=xamp_n}
C {lab_pin.sym} 770 700 0 0 {name=p72 sig_type=std_logic lab=vref}
C {lab_pin.sym} 770 760 0 0 {name=p73 sig_type=std_logic lab=sumn}
C {lab_pin.sym} 930 730 0 0 {name=p74 sig_type=std_logic lab=outn}
T {Sensor N | C=CN | Cf=40 pF | phi1=sample/reset, phi2=transfer} -650 970 0 0 0.3 0.3 {}
C {code_shown.sym} -650 1100 0 0 {name=SIM only_toplevel=true value="
.param CP=7p CN=5p CF=40p
* 10 kHz; 5 us dead time; complementary gates generated behaviorally.
VPHI1 phi1 0 PULSE(5 0 41u 10n 10n 59.98u 100u)
VPHI2 phi2 0 PULSE(0 5 46u 10n 10n 44.98u 100u)
B1 phi1b 0 V=5-v(phi1)
B2 phi2b 0 V=5-v(phi2)
.subckt amp_behavioral plus minus out
EAMP raw plus plus minus 100k
RPOLE raw pole 1k
CPOLE pole 0 15.915494u
EBUF out 0 pole 0 1
.ends amp_behavioral
.options reltol=1e-4 abstol=1e-12 method=gear maxord=2
.temp 27
.control
set noaskquit
set wr_singlescale
set wr_vecnames
set filetype=ascii
save v(phi1) v(phi2) v(txp) v(rxp) v(sump) v(outp) v(outn)
tran 50n 500u
let vdiff=v(outp)-v(outn)
meas tran outp_sample FIND v(outp) AT=480u
meas tran outn_sample FIND v(outn) AT=480u
meas tran diff_sample FIND vdiff AT=480u
meas tran reset_outp FIND v(outp) AT=420u
wrdata sc_waveforms.dat v(phi1) v(phi2) v(outp) v(outn) vdiff v(rxp) v(sump)
write sc_diff.raw
.endc
"}
C {code_shown.sym} 600 1100 0 0 {name=MODELS only_toplevel=true value=".include /home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/mos/tntp49_5v"}
C {vsource.sym} -500 -190 0 0 {name=VDD value=5}
C {lab_pin.sym} -500 -220 0 0 {name=psupply lab=vdd}
C {gnd.sym} -500 -160 0 0 {name=gsupply lab=0}
C {vsource.sym} -200 -190 0 0 {name=VREF value=2.5}
C {lab_pin.sym} -200 -220 0 0 {name=pref lab=vref}
C {gnd.sym} -200 -160 0 0 {name=gref lab=0}
