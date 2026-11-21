v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {SCL08 5t ota gm-resistor} 180 -20 0 0 0.55 0.55 {}
T {PMOS mirror load} 300 45 0 0 0.3 0.3 {}
T {Input differential pair} 300 485 0 0 0.3 0.3 {}
T {W/L shown in um; all L = 0.8 um. Cc = 5 pF.
Nominal test: VDD = 5 V, VBN = 0.95 V, input CM = 2.5 V, external CL = 5 pF.
Single-ended baseline. inp is noninverting; inn is inverting. Body labels connect to vdd/vss.} 180 850 0 0 0.28 0.28 {}
N 280 100 460 100 {lab=vdd}
N 460 100 640 100 {lab=vdd}
N 280 100 280 150 {lab=vdd}
N 640 100 640 150 {lab=vdd}
N 320 180 400 180 {lab=IOUT}
N 400 180 600 180 {lab=IOUT}
N 280 210 280 260 {lab=IOUT}
N 280 260 280 410 {lab=IOUT}
N 280 260 400 260 {lab=IOUT}
N 400 180 400 260 {lab=IOUT}
N 640 210 640 300 {lab=IOUT}
N 640 300 640 410 {lab=IOUT}
N 280 470 280 520 {lab=tail}
N 280 520 460 520 {lab=tail}
N 460 520 640 520 {lab=tail}
N 640 470 640 520 {lab=tail}
N 460 520 460 620 {lab=tail}
N 460 680 460 740 {lab=vss}
N 200 650 360 650 {lab=vbn}
N 360 650 420 650 {lab=vbn}
N 200 440 240 440 {lab=SP}
N 680 440 720 440 {lab=SENSE}
N 220 180 280 180 {lab=vdd}
N 640 180 700 180 {lab=vdd}
N 280 440 340 440 {lab=vss}
N 580 440 640 440 {lab=vss}
N 460 650 520 650 {lab=vss}
C {devices/pmos4.sym} 300 180 0 1 {name=M3 model=P w=2.5u l=3.2u m=1}
C {devices/pmos4.sym} 620 180 0 0 {name=M4 model=P w=2.5u l=3.2u m=1}
C {devices/nmos4.sym} 260 440 0 0 {name=M1 model=N w=2.5u l=3.2u m=1}
C {devices/nmos4.sym} 660 440 0 1 {name=M2 model=N w=2.5u l=3.2u m=1}
C {devices/nmos4.sym} 440 650 0 0 {name=M5 model=N w=5u l=3.2u m=1}
C {devices/lab_pin.sym} 220 180 0 0 {name=l2 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 700 180 2 0 {name=l3 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 340 440 2 0 {name=l5 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 580 440 0 0 {name=l6 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 520 650 2 0 {name=l7 sig_type=std_logic lab=vss}
C {devices/ipin.sym} 720 440 2 0 {name=p_inp lab=SENSE}
C {devices/ipin.sym} 200 440 0 0 {name=p_inn lab=SP}
C {devices/iopin.sym} 460 100 0 0 {name=p_vdd lab=vdd}
C {devices/iopin.sym} 460 740 0 0 {name=p_vss lab=vss}
C {devices/ipin.sym} 200 650 0 0 {name=p_vbn lab=vbn}
C {devices/lab_pin.sym} 280 340 0 0 {name=l9 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 460 560 0 0 {name=l11 sig_type=std_logic lab=tail}
C {devices/ipin.sym} 640 330 2 0 {name=p_inp1 lab=IOUT}
