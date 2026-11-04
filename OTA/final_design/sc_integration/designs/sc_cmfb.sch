v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {SCL CP8D 5 V | Differential SC sensor readout | First simulation prototype} -650 -380 0 0 0.55 0.55 {}
T {One extracted telescopic OTA with CMFB; differential output = V(outp)-V(outn). Explicit reconstructed SCL08 switches.} -650 -320 0 0 0.32 0.32 {}
C {scl08_tg.sym} -470 0 0 0 {name=xdrive_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} -620 -40 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -320 -40 0 0 {name=p2 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} -320 -20 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} -320 0 0 0 {name=p4 sig_type=std_logic lab=txp}
C {devices/lab_pin.sym} -320 20 0 0 {name=p5 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -320 40 0 0 {name=p6 sig_type=std_logic lab=phi1b}
C {scl08_tg.sym} -470 180 0 0 {name=xdischarge_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} -620 140 0 0 {name=p7 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} -320 140 0 0 {name=p8 sig_type=std_logic lab=phi2}
C {devices/lab_pin.sym} -320 160 0 0 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} -320 180 0 0 {name=p10 sig_type=std_logic lab=txp}
C {devices/lab_pin.sym} -320 200 0 0 {name=p11 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -320 220 0 0 {name=p12 sig_type=std_logic lab=phi2b}
C {devices/capa.sym} 0 0 1 0 {name=CSp value=\{CP\} m=1}
C {devices/lab_pin.sym} -30 0 0 0 {name=p13 sig_type=std_logic lab=txp}
C {devices/lab_pin.sym} 30 0 0 0 {name=p14 sig_type=std_logic lab=rxp}
C {scl08_tg.sym} 80 220 0 0 {name=xclamp_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} -70 180 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 230 180 0 0 {name=p16 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 230 200 0 0 {name=p17 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 230 220 0 0 {name=p18 sig_type=std_logic lab=rxp}
C {devices/lab_pin.sym} 230 240 0 0 {name=p19 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 230 260 0 0 {name=p20 sig_type=std_logic lab=phi1b}
C {scl08_tg.sym} 390 0 0 0 {name=xtransfer_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 240 -40 0 0 {name=p21 sig_type=std_logic lab=rxp}
C {devices/lab_pin.sym} 540 -40 0 0 {name=p22 sig_type=std_logic lab=phit}
C {devices/lab_pin.sym} 540 -20 0 0 {name=p23 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 540 0 0 0 {name=p24 sig_type=std_logic lab=sump}
C {devices/lab_pin.sym} 540 20 0 0 {name=p25 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 540 40 0 0 {name=p26 sig_type=std_logic lab=phitb}
C {scl08_tg.sym} 850 -190 0 0 {name=xreset_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 700 -230 0 0 {name=p27 sig_type=std_logic lab=sump}
C {devices/lab_pin.sym} 1000 -230 0 0 {name=p28 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 1000 -210 0 0 {name=p29 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1000 -190 0 0 {name=p30 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 1000 -170 0 0 {name=p31 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1000 -150 0 0 {name=p32 sig_type=std_logic lab=phi1b}
C {devices/capa.sym} 870 -80 1 0 {name=CFp value=\{CF\} m=1}
C {devices/lab_pin.sym} 840 -80 0 0 {name=p33 sig_type=std_logic lab=sump}
C {devices/lab_pin.sym} 900 -80 0 0 {name=p34 sig_type=std_logic lab=outp}
T {Sensor P | C=CP | Cf=40 pF | phi1=sample/reset; phiT=RX transfer; phi2=TX discharge} -650 320 0 0 0.3 0.3 {}
C {scl08_tg.sym} -470 650 0 0 {name=xdrive_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} -620 610 0 0 {name=p38 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -320 610 0 0 {name=p39 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} -320 630 0 0 {name=p40 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} -320 650 0 0 {name=p41 sig_type=std_logic lab=txn}
C {devices/lab_pin.sym} -320 670 0 0 {name=p42 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -320 690 0 0 {name=p43 sig_type=std_logic lab=phi1b}
C {scl08_tg.sym} -470 830 0 0 {name=xdischarge_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} -620 790 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} -320 790 0 0 {name=p45 sig_type=std_logic lab=phi2}
C {devices/lab_pin.sym} -320 810 0 0 {name=p46 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} -320 830 0 0 {name=p47 sig_type=std_logic lab=txn}
C {devices/lab_pin.sym} -320 850 0 0 {name=p48 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -320 870 0 0 {name=p49 sig_type=std_logic lab=phi2b}
C {devices/capa.sym} 0 650 1 0 {name=CSn value=\{CN\} m=1}
C {devices/lab_pin.sym} -30 650 0 0 {name=p50 sig_type=std_logic lab=txn}
C {devices/lab_pin.sym} 30 650 0 0 {name=p51 sig_type=std_logic lab=rxn}
C {scl08_tg.sym} 80 870 0 0 {name=xclamp_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} -70 830 0 0 {name=p52 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 230 830 0 0 {name=p53 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 230 850 0 0 {name=p54 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 230 870 0 0 {name=p55 sig_type=std_logic lab=rxn}
C {devices/lab_pin.sym} 230 890 0 0 {name=p56 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 230 910 0 0 {name=p57 sig_type=std_logic lab=phi1b}
C {scl08_tg.sym} 390 650 0 0 {name=xtransfer_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 240 610 0 0 {name=p58 sig_type=std_logic lab=rxn}
C {devices/lab_pin.sym} 540 610 0 0 {name=p59 sig_type=std_logic lab=phit}
C {devices/lab_pin.sym} 540 630 0 0 {name=p60 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 540 650 0 0 {name=p61 sig_type=std_logic lab=sumn}
C {devices/lab_pin.sym} 540 670 0 0 {name=p62 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 540 690 0 0 {name=p63 sig_type=std_logic lab=phitb}
C {scl08_tg.sym} 850 460 0 0 {name=xreset_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 700 420 0 0 {name=p64 sig_type=std_logic lab=sumn}
C {devices/lab_pin.sym} 1000 420 0 0 {name=p65 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 1000 440 0 0 {name=p66 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1000 460 0 0 {name=p67 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 1000 480 0 0 {name=p68 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1000 500 0 0 {name=p69 sig_type=std_logic lab=phi1b}
C {devices/capa.sym} 870 570 1 0 {name=CFn value=\{CF\} m=1}
C {devices/lab_pin.sym} 840 570 0 0 {name=p70 sig_type=std_logic lab=sumn}
C {devices/lab_pin.sym} 900 570 0 0 {name=p71 sig_type=std_logic lab=outn}
T {Sensor N | C=CN | Cf=40 pF | phi1=sample/reset; phiT=RX transfer; phi2=TX discharge} -650 970 0 0 0.3 0.3 {}


C {devices/vsource.sym} -500 -190 0 0 {name=VDD value=5}
C {devices/lab_pin.sym} -500 -220 0 0 {name=psupply lab=vdd}
C {devices/gnd.sym} -500 -160 0 0 {name=gsupply lab=0}
C {devices/vsource.sym} -200 -190 0 0 {name=VREF value=2.5}
C {devices/lab_pin.sym} -200 -220 0 0 {name=pref lab=vref}
C {devices/gnd.sym} -200 -160 0 0 {name=gref lab=0}

C {ota_cm2p5.sym} 1400 400 0 0 {name=XOTA}
C {devices/lab_pin.sym} 1290 310 0 0 {name=OTA_P0 lab=sumn}
C {devices/lab_pin.sym} 1290 340 0 0 {name=OTA_P1 lab=sump}
C {devices/lab_pin.sym} 1510 310 0 0 {name=OTA_P2 lab=outp}
C {devices/lab_pin.sym} 1510 340 0 0 {name=OTA_P3 lab=outn}
C {devices/lab_pin.sym} 1400 250 0 0 {name=OTA_P4 lab=vdd}
C {devices/lab_pin.sym} 1400 550 0 0 {name=OTA_P5 lab=0}
C {devices/lab_pin.sym} 1290 420 0 0 {name=OTA_P6 lab=bias}
C {devices/lab_pin.sym} 1290 455 0 0 {name=OTA_P7 lab=vref}
C {devices/lab_pin.sym} 1290 490 0 0 {name=OTA_P8 lab=vbn}
C {devices/lab_pin.sym} 1290 520 0 0 {name=OTA_P9 lab=vbp}
C {devices/code.sym} 800 1100 0 0 {name=SIM only_toplevel=false value=".include \"../tb/xschem_support.inc\""}
T {Output CM target=2.5 V; input CM floats during transfer.
IREF=3.5uA; VBN=3.0V; VBP=VDD-2.2V.
RX transfer starts 1 us before TX discharge; clock edges 1000 ns.
Cap values and simulation controls are in tb/xschem_support.inc.} 1170 650 0 0 0.23 0.23 {}
