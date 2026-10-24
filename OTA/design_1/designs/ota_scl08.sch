v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/pmos4.sym} 300 180 0 1 {name=M3 model=P w=2.5u l=0.8u m=1}
C {devices/pmos4.sym} 620 180 0 0 {name=M4 model=P w=2.5u l=0.8u m=1}
C {devices/nmos4.sym} 260 440 0 0 {name=M1 model=N w=2.5u l=0.8u m=1}
C {devices/nmos4.sym} 660 440 0 1 {name=M2 model=N w=2.5u l=0.8u m=1}
C {devices/nmos4.sym} 440 650 0 0 {name=M5 model=N w=5u l=0.8u m=1}
C {devices/pmos4.sym} 940 300 0 0 {name=M6 model=P w=7u l=0.8u m=1}
C {devices/nmos4.sym} 940 650 0 0 {name=M7 model=N w=10u l=0.8u m=1}
N 280 100 460 100 {lab=vdd}
N 460 100 640 100 {lab=vdd}
N 640 100 960 100 {lab=vdd}
N 280 100 280 150 {lab=vdd}
N 640 100 640 150 {lab=vdd}
N 960 100 960 270 {lab=vdd}
N 320 180 400 180 {lab=n1}
N 400 180 600 180 {lab=n1}
N 280 210 280 260 {lab=n1}
N 280 260 280 410 {lab=n1}
N 280 260 400 260 {lab=n1}
N 400 180 400 260 {lab=n1}
N 640 210 640 300 {lab=n2}
N 640 300 640 410 {lab=n2}
N 280 470 280 520 {lab=tail}
N 280 520 460 520 {lab=tail}
N 460 520 640 520 {lab=tail}
N 640 470 640 520 {lab=tail}
N 460 520 460 620 {lab=tail}
N 460 680 460 740 {lab=vss}
N 960 680 960 740 {lab=vss}
C {devices/lab_pin.sym} 960 740 0 0 {name=l1 sig_type=std_logic lab=vss}
N 640 300 760 300 {lab=n2}
N 760 300 920 300 {lab=n2}
N 960 330 960 380 {lab=out}
N 960 380 960 500 {lab=out}
N 960 500 960 620 {lab=out}
N 960 500 1100 500 {lab=out}
C {devices/capa.sym} 840 380 1 0 {name=Cc value=5p m=1 hide_texts=true}
N 760 300 760 380 {lab=n2}
N 760 380 810 380 {lab=n2}
N 870 380 960 380 {lab=out}
N 200 650 360 650 {lab=vbn}
N 360 650 420 650 {lab=vbn}
N 360 650 360 780 {lab=vbn}
N 360 780 900 780 {lab=vbn}
N 900 650 900 780 {lab=vbn}
N 900 650 920 650 {lab=vbn}
N 200 440 240 440 {lab=inn}
N 680 440 720 440 {lab=inp}
N 280 180 220 180 {lab=vdd}
C {devices/lab_pin.sym} 220 180 0 0 {name=l2 sig_type=std_logic lab=vdd}
N 640 180 700 180 {lab=vdd}
C {devices/lab_pin.sym} 700 180 2 0 {name=l3 sig_type=std_logic lab=vdd}
N 960 300 1020 300 {lab=vdd}
C {devices/lab_pin.sym} 1020 300 2 0 {name=l4 sig_type=std_logic lab=vdd}
N 280 440 340 440 {lab=vss}
C {devices/lab_pin.sym} 340 440 2 0 {name=l5 sig_type=std_logic lab=vss}
N 640 440 580 440 {lab=vss}
C {devices/lab_pin.sym} 580 440 0 0 {name=l6 sig_type=std_logic lab=vss}
N 460 650 520 650 {lab=vss}
C {devices/lab_pin.sym} 520 650 2 0 {name=l7 sig_type=std_logic lab=vss}
N 960 650 1020 650 {lab=vss}
C {devices/lab_pin.sym} 1020 650 2 0 {name=l8 sig_type=std_logic lab=vss}
C {devices/ipin.sym} 720 440 2 0 {name=p_inp lab=inp}
C {devices/ipin.sym} 200 440 0 0 {name=p_inn lab=inn}
C {devices/opin.sym} 1100 500 0 0 {name=p_out lab=out}
C {devices/iopin.sym} 460 100 0 0 {name=p_vdd lab=vdd}
C {devices/iopin.sym} 460 740 0 0 {name=p_vss lab=vss}
C {devices/ipin.sym} 200 650 0 0 {name=p_vbn lab=vbn}
C {devices/lab_pin.sym} 280 340 0 0 {name=l9 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 640 260 0 0 {name=l10 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 460 560 0 0 {name=l11 sig_type=std_logic lab=tail}
T {SCL08 two-stage OTA - seven-transistor baseline} 180 -20 0 0 0.55 0.55 {}
T {PMOS mirror load} 300 45 0 0 0.3 0.3 {}
T {Input differential pair} 300 485 0 0 0.3 0.3 {}
T {Second gain stage} 890 45 0 0 0.3 0.3 {}
T {W/L shown in um; all L = 0.8 um. Cc = 5 pF.
Nominal test: VDD = 5 V, VBN = 0.95 V, input CM = 2.5 V, external CL = 5 pF.
Single-ended baseline. inp is noninverting; inn is inverting. Body labels connect to vdd/vss.} 180 850 0 0 0.28 0.28 {}
T {Cc = 5 pF} 795 345 0 0 0.3 0.3 {}
