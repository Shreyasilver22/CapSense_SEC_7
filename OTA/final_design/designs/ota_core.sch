v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/nmos4.sym} 900 120 0 0 {name=MSP model=N w=20u l=1.6u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSP: 20u/1.6u x4} 835 190 0 0 0.18 0.18 {}
N 880 120 830 120 {lab=OUTP}
C {devices/lab_pin.sym} 830 120 0 0 {name=L1 lab=OUTP}
N 920 120 985 120 {lab=VSS}
C {devices/lab_pin.sym} 985 120 0 0 {name=L2 lab=VSS}
N 920 90 920 65 {lab=VDD}
C {devices/lab_pin.sym} 920 65 0 0 {name=L3 lab=VDD}
N 920 150 920 175 {lab=SP}
C {devices/lab_pin.sym} 920 175 0 0 {name=L4 lab=SP}
C {devices/nmos4.sym} 1200 120 0 0 {name=MSM model=N w=20u l=1.6u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSM: 20u/1.6u x4} 1135 190 0 0 0.18 0.18 {}
N 1180 120 1130 120 {lab=OUTM}
C {devices/lab_pin.sym} 1130 120 0 0 {name=L5 lab=OUTM}
N 1220 120 1285 120 {lab=VSS}
C {devices/lab_pin.sym} 1285 120 0 0 {name=L6 lab=VSS}
N 1220 90 1220 65 {lab=VDD}
C {devices/lab_pin.sym} 1220 65 0 0 {name=L7 lab=VDD}
N 1220 150 1220 175 {lab=SM}
C {devices/lab_pin.sym} 1220 175 0 0 {name=L8 lab=SM}
C {devices/nmos4.sym} 1500 120 0 0 {name=MSR model=N w=20u l=1.6u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSR: 20u/1.6u x4} 1435 190 0 0 0.18 0.18 {}
N 1480 120 1430 120 {lab=VCM}
C {devices/lab_pin.sym} 1430 120 0 0 {name=L9 lab=VCM}
N 1520 120 1585 120 {lab=VSS}
C {devices/lab_pin.sym} 1585 120 0 0 {name=L10 lab=VSS}
N 1520 90 1520 65 {lab=VDD}
C {devices/lab_pin.sym} 1520 65 0 0 {name=L11 lab=VDD}
N 1520 150 1520 175 {lab=SR}
C {devices/lab_pin.sym} 1520 175 0 0 {name=L12 lab=SR}
C {devices/nmos4.sym} 900 320 0 0 {name=MSIP model=N w=20u l=3.2u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIP: 20u/3.2u x2} 835 390 0 0 0.18 0.18 {}
N 880 320 830 320 {lab=IREF}
C {devices/lab_pin.sym} 830 320 0 0 {name=L13 lab=IREF}
N 920 320 985 320 {lab=VSS}
C {devices/lab_pin.sym} 985 320 0 0 {name=L14 lab=VSS}
N 920 290 920 265 {lab=SP}
C {devices/lab_pin.sym} 920 265 0 0 {name=L15 lab=SP}
N 920 350 920 375 {lab=VSS}
C {devices/lab_pin.sym} 920 375 0 0 {name=L16 lab=VSS}
C {devices/nmos4.sym} 1200 320 0 0 {name=MSIM model=N w=20u l=3.2u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIM: 20u/3.2u x2} 1135 390 0 0 0.18 0.18 {}
N 1180 320 1130 320 {lab=IREF}
C {devices/lab_pin.sym} 1130 320 0 0 {name=L17 lab=IREF}
N 1220 320 1285 320 {lab=VSS}
C {devices/lab_pin.sym} 1285 320 0 0 {name=L18 lab=VSS}
N 1220 290 1220 265 {lab=SM}
C {devices/lab_pin.sym} 1220 265 0 0 {name=L19 lab=SM}
N 1220 350 1220 375 {lab=VSS}
C {devices/lab_pin.sym} 1220 375 0 0 {name=L20 lab=VSS}
C {devices/nmos4.sym} 1500 320 0 0 {name=MSIR model=N w=20u l=3.2u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIR: 20u/3.2u x2} 1435 390 0 0 0.18 0.18 {}
N 1480 320 1430 320 {lab=IREF}
C {devices/lab_pin.sym} 1430 320 0 0 {name=L21 lab=IREF}
N 1520 320 1585 320 {lab=VSS}
C {devices/lab_pin.sym} 1585 320 0 0 {name=L22 lab=VSS}
N 1520 290 1520 265 {lab=SR}
C {devices/lab_pin.sym} 1520 265 0 0 {name=L23 lab=SR}
N 1520 350 1520 375 {lab=VSS}
C {devices/lab_pin.sym} 1520 375 0 0 {name=L24 lab=VSS}
C {devices/pmos4.sym} 900 800 0 0 {name=MCBI model=P w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCBI: 20u/3.2u x1} 835 870 0 0 0.18 0.18 {}
N 880 800 830 800 {lab=CB}
C {devices/lab_pin.sym} 830 800 0 0 {name=L25 lab=CB}
N 920 800 985 800 {lab=VDD}
C {devices/lab_pin.sym} 985 800 0 0 {name=L26 lab=VDD}
N 920 770 920 745 {lab=VDD}
C {devices/lab_pin.sym} 920 745 0 0 {name=L27 lab=VDD}
N 920 830 920 855 {lab=CB}
C {devices/lab_pin.sym} 920 855 0 0 {name=L28 lab=CB}
C {devices/nmos4.sym} 900 1000 0 0 {name=MCBN model=N w=11.428571u l=3.2u m=1 extra="AD=51.4286p AS=51.4286p PD=31.8571u PS=31.8571u" hide_texts=true}
T {MCBN: 11.428571u/3.2u x1} 835 1070 0 0 0.18 0.18 {}
N 880 1000 830 1000 {lab=IREF}
C {devices/lab_pin.sym} 830 1000 0 0 {name=L29 lab=IREF}
N 920 1000 985 1000 {lab=VSS}
C {devices/lab_pin.sym} 985 1000 0 0 {name=L30 lab=VSS}
N 920 970 920 945 {lab=CB}
C {devices/lab_pin.sym} 920 945 0 0 {name=L31 lab=CB}
N 920 1030 920 1055 {lab=VSS}
C {devices/lab_pin.sym} 920 1055 0 0 {name=L32 lab=VSS}
C {devices/pmos4.sym} 2100 140 0 0 {name=MCC model=P w=20u l=10u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCC: 20u/10u x4} 2035 210 0 0 0.18 0.18 {}
N 2080 140 2030 140 {lab=PC}
C {devices/lab_pin.sym} 2030 140 0 0 {name=L33 lab=PC}
N 2120 140 2185 140 {lab=VDD}
C {devices/lab_pin.sym} 2185 140 0 0 {name=L34 lab=VDD}
N 2120 110 2120 85 {lab=VDD}
C {devices/lab_pin.sym} 2120 85 0 0 {name=L35 lab=VDD}
N 2120 170 2120 195 {lab=VDD}
C {devices/lab_pin.sym} 2120 195 0 0 {name=L36 lab=VDD}
C {devices/pmos4.sym} 2100 340 0 0 {name=MCM1 model=P w=20u l=10u m=12 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCM1: 20u/10u x12} 2035 410 0 0 0.18 0.18 {}
N 2080 340 2030 340 {lab=PC}
C {devices/lab_pin.sym} 2030 340 0 0 {name=L37 lab=PC}
N 2120 340 2185 340 {lab=OUTP}
C {devices/lab_pin.sym} 2185 340 0 0 {name=L38 lab=OUTP}
N 2120 310 2120 285 {lab=OUTP}
C {devices/lab_pin.sym} 2120 285 0 0 {name=L39 lab=OUTP}
N 2120 370 2120 395 {lab=OUTP}
C {devices/lab_pin.sym} 2120 395 0 0 {name=L40 lab=OUTP}
C {devices/pmos4.sym} 2100 540 0 0 {name=MCM2 model=P w=20u l=10u m=12 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCM2: 20u/10u x12} 2035 610 0 0 0.18 0.18 {}
N 2080 540 2030 540 {lab=PC}
C {devices/lab_pin.sym} 2030 540 0 0 {name=L41 lab=PC}
N 2120 540 2185 540 {lab=OUTM}
C {devices/lab_pin.sym} 2185 540 0 0 {name=L42 lab=OUTM}
N 2120 510 2120 485 {lab=OUTM}
C {devices/lab_pin.sym} 2120 485 0 0 {name=L43 lab=OUTM}
N 2120 570 2120 595 {lab=OUTM}
C {devices/lab_pin.sym} 2120 595 0 0 {name=L44 lab=OUTM}
C {devices/nmos4.sym} 370 740 0 0 {name=MTAIL model=N w=80.0u l=3.2u m=1 extra="AD=360p AS=360p PD=169u PS=169u" hide_texts=true}
T {MTAIL: 80.0u/3.2u x1} 305 810 0 0 0.18 0.18 {}
N 350 740 300 740 {lab=IREF}
C {devices/lab_pin.sym} 300 740 0 0 {name=L45 lab=IREF}
N 390 740 455 740 {lab=VSS}
C {devices/lab_pin.sym} 455 740 0 0 {name=L46 lab=VSS}
N 390 710 390 685 {lab=TAIL}
C {devices/lab_pin.sym} 390 685 0 0 {name=L47 lab=TAIL}
N 390 770 390 795 {lab=VSS}
C {devices/lab_pin.sym} 390 795 0 0 {name=L48 lab=VSS}
C {devices/nmos4.sym} 220 550 0 0 {name=MN1 model=N w=15u l=2.4u m=1 extra="AD=67.5p AS=67.5p PD=39u PS=39u" hide_texts=true}
T {MN1: 15u/2.4u x1} 155 620 0 0 0.18 0.18 {}
N 200 550 150 550 {lab=INP}
C {devices/lab_pin.sym} 150 550 0 0 {name=L49 lab=INP}
N 240 550 305 550 {lab=VSS}
C {devices/lab_pin.sym} 305 550 0 0 {name=L50 lab=VSS}
N 240 520 240 495 {lab=NX1}
C {devices/lab_pin.sym} 240 495 0 0 {name=L51 lab=NX1}
N 240 580 240 605 {lab=TAIL}
C {devices/lab_pin.sym} 240 605 0 0 {name=L52 lab=TAIL}
C {devices/nmos4.sym} 520 550 0 0 {name=MN2 model=N w=15u l=2.4u m=1 extra="AD=67.5p AS=67.5p PD=39u PS=39u" hide_texts=true}
T {MN2: 15u/2.4u x1} 455 620 0 0 0.18 0.18 {}
N 500 550 450 550 {lab=INN}
C {devices/lab_pin.sym} 450 550 0 0 {name=L53 lab=INN}
N 540 550 605 550 {lab=VSS}
C {devices/lab_pin.sym} 605 550 0 0 {name=L54 lab=VSS}
N 540 520 540 495 {lab=NX2}
C {devices/lab_pin.sym} 540 495 0 0 {name=L55 lab=NX2}
N 540 580 540 605 {lab=TAIL}
C {devices/lab_pin.sym} 540 605 0 0 {name=L56 lab=TAIL}
C {devices/nmos4.sym} 220 400 0 0 {name=MNC1 model=N w=30u l=2.4u m=1 extra="AD=135p AS=135p PD=69u PS=69u" hide_texts=true}
T {MNC1: 30u/2.4u x1} 155 470 0 0 0.18 0.18 {}
N 200 400 150 400 {lab=VBN}
C {devices/lab_pin.sym} 150 400 0 0 {name=L57 lab=VBN}
N 240 400 305 400 {lab=VSS}
C {devices/lab_pin.sym} 305 400 0 0 {name=L58 lab=VSS}
N 240 370 240 345 {lab=OUTM}
C {devices/lab_pin.sym} 240 345 0 0 {name=L59 lab=OUTM}
N 240 430 240 455 {lab=NX1}
C {devices/lab_pin.sym} 240 455 0 0 {name=L60 lab=NX1}
C {devices/nmos4.sym} 520 400 0 0 {name=MNC2 model=N w=30u l=2.4u m=1 extra="AD=135p AS=135p PD=69u PS=69u" hide_texts=true}
T {MNC2: 30u/2.4u x1} 455 470 0 0 0.18 0.18 {}
N 500 400 450 400 {lab=VBN}
C {devices/lab_pin.sym} 450 400 0 0 {name=L61 lab=VBN}
N 540 400 605 400 {lab=VSS}
C {devices/lab_pin.sym} 605 400 0 0 {name=L62 lab=VSS}
N 540 370 540 345 {lab=OUTP}
C {devices/lab_pin.sym} 540 345 0 0 {name=L63 lab=OUTP}
N 540 430 540 455 {lab=NX2}
C {devices/lab_pin.sym} 540 455 0 0 {name=L64 lab=NX2}
C {devices/pmos4.sym} 220 250 0 0 {name=MPC1 model=P w=60u l=2.4u m=1 extra="AD=270p AS=270p PD=129u PS=129u" hide_texts=true}
T {MPC1: 60u/2.4u x1} 155 320 0 0 0.18 0.18 {}
N 200 250 150 250 {lab=VBP}
C {devices/lab_pin.sym} 150 250 0 0 {name=L65 lab=VBP}
N 240 250 305 250 {lab=VDD}
C {devices/lab_pin.sym} 305 250 0 0 {name=L66 lab=VDD}
N 240 220 240 195 {lab=PX1}
C {devices/lab_pin.sym} 240 195 0 0 {name=L67 lab=PX1}
N 240 280 240 305 {lab=OUTM}
C {devices/lab_pin.sym} 240 305 0 0 {name=L68 lab=OUTM}
C {devices/pmos4.sym} 520 250 0 0 {name=MPC2 model=P w=60u l=2.4u m=1 extra="AD=270p AS=270p PD=129u PS=129u" hide_texts=true}
T {MPC2: 60u/2.4u x1} 455 320 0 0 0.18 0.18 {}
N 500 250 450 250 {lab=VBP}
C {devices/lab_pin.sym} 450 250 0 0 {name=L69 lab=VBP}
N 540 250 605 250 {lab=VDD}
C {devices/lab_pin.sym} 605 250 0 0 {name=L70 lab=VDD}
N 540 220 540 195 {lab=PX2}
C {devices/lab_pin.sym} 540 195 0 0 {name=L71 lab=PX2}
N 540 280 540 305 {lab=OUTP}
C {devices/lab_pin.sym} 540 305 0 0 {name=L72 lab=OUTP}
C {devices/pmos4.sym} 220 100 0 0 {name=MP1 model=P w=40u l=3.2u m=1 extra="AD=180p AS=180p PD=89u PS=89u" hide_texts=true}
T {MP1: 40u/3.2u x1} 155 170 0 0 0.18 0.18 {}
N 200 100 150 100 {lab=PC}
C {devices/lab_pin.sym} 150 100 0 0 {name=L73 lab=PC}
N 240 100 305 100 {lab=VDD}
C {devices/lab_pin.sym} 305 100 0 0 {name=L74 lab=VDD}
N 240 70 240 45 {lab=VDD}
C {devices/lab_pin.sym} 240 45 0 0 {name=L75 lab=VDD}
N 240 130 240 155 {lab=PX1}
C {devices/lab_pin.sym} 240 155 0 0 {name=L76 lab=PX1}
C {devices/pmos4.sym} 520 100 0 0 {name=MP2 model=P w=40u l=3.2u m=1 extra="AD=180p AS=180p PD=89u PS=89u" hide_texts=true}
T {MP2: 40u/3.2u x1} 455 170 0 0 0.18 0.18 {}
N 500 100 450 100 {lab=PC}
C {devices/lab_pin.sym} 450 100 0 0 {name=L77 lab=PC}
N 540 100 605 100 {lab=VDD}
C {devices/lab_pin.sym} 605 100 0 0 {name=L78 lab=VDD}
N 540 70 540 45 {lab=VDD}
C {devices/lab_pin.sym} 540 45 0 0 {name=L79 lab=VDD}
N 540 130 540 155 {lab=PX2}
C {devices/lab_pin.sym} 540 155 0 0 {name=L80 lab=PX2}
C {devices/pmos4.sym} 1150 920 0 0 {name=MCS model=P w=5u l=2.4u m=1 extra="AD=22.5p AS=22.5p PD=19u PS=19u" hide_texts=true}
T {MCS: 5u/2.4u x1} 1085 990 0 0 0.18 0.18 {}
N 1130 920 1080 920 {lab=SENSE}
C {devices/lab_pin.sym} 1080 920 0 0 {name=L81 lab=SENSE}
N 1170 920 1235 920 {lab=VDD}
C {devices/lab_pin.sym} 1235 920 0 0 {name=L82 lab=VDD}
N 1170 890 1170 865 {lab=CT}
C {devices/lab_pin.sym} 1170 865 0 0 {name=L83 lab=CT}
N 1170 950 1170 975 {lab=CA}
C {devices/lab_pin.sym} 1170 975 0 0 {name=L84 lab=CA}
C {devices/pmos4.sym} 1450 920 0 0 {name=MCR model=P w=5u l=2.4u m=1 extra="AD=22.5p AS=22.5p PD=19u PS=19u" hide_texts=true}
T {MCR: 5u/2.4u x1} 1385 990 0 0 0.18 0.18 {}
N 1430 920 1380 920 {lab=SR}
C {devices/lab_pin.sym} 1380 920 0 0 {name=L85 lab=SR}
N 1470 920 1535 920 {lab=VDD}
C {devices/lab_pin.sym} 1535 920 0 0 {name=L86 lab=VDD}
N 1470 890 1470 865 {lab=CT}
C {devices/lab_pin.sym} 1470 865 0 0 {name=L87 lab=CT}
N 1470 950 1470 975 {lab=RCM}
C {devices/lab_pin.sym} 1470 975 0 0 {name=L88 lab=RCM}
C {devices/pmos4.sym} 1250 720 0 0 {name=MCT model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCT: 10u/3.2u x1} 1185 790 0 0 0.18 0.18 {}
N 1230 720 1180 720 {lab=CB}
C {devices/lab_pin.sym} 1180 720 0 0 {name=L89 lab=CB}
N 1270 720 1335 720 {lab=VDD}
C {devices/lab_pin.sym} 1335 720 0 0 {name=L90 lab=VDD}
N 1270 690 1270 665 {lab=VDD}
C {devices/lab_pin.sym} 1270 665 0 0 {name=L91 lab=VDD}
N 1270 750 1270 775 {lab=CT}
C {devices/lab_pin.sym} 1270 775 0 0 {name=L92 lab=CT}
C {devices/nmos4.sym} 1150 1120 0 0 {name=MCFN1 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN1: 10u/3.2u x1} 1085 1190 0 0 0.18 0.18 {}
N 1130 1120 1080 1120 {lab=CA}
C {devices/lab_pin.sym} 1080 1120 0 0 {name=L93 lab=CA}
N 1170 1120 1235 1120 {lab=VSS}
C {devices/lab_pin.sym} 1235 1120 0 0 {name=L94 lab=VSS}
N 1170 1090 1170 1065 {lab=CA}
C {devices/lab_pin.sym} 1170 1065 0 0 {name=L95 lab=CA}
N 1170 1150 1170 1175 {lab=VSS}
C {devices/lab_pin.sym} 1170 1175 0 0 {name=L96 lab=VSS}
C {devices/nmos4.sym} 2050 1120 0 0 {name=MCFN2 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN2: 10u/3.2u x1} 1985 1190 0 0 0.18 0.18 {}
N 2030 1120 1980 1120 {lab=CA}
C {devices/lab_pin.sym} 1980 1120 0 0 {name=L97 lab=CA}
N 2070 1120 2135 1120 {lab=VSS}
C {devices/lab_pin.sym} 2135 1120 0 0 {name=L98 lab=VSS}
N 2070 1090 2070 1065 {lab=PC}
C {devices/lab_pin.sym} 2070 1065 0 0 {name=L99 lab=PC}
N 2070 1150 2070 1175 {lab=VSS}
C {devices/lab_pin.sym} 2070 1175 0 0 {name=L100 lab=VSS}
C {devices/nmos4.sym} 1450 1120 0 0 {name=MCFN3 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN3: 10u/3.2u x1} 1385 1190 0 0 0.18 0.18 {}
N 1430 1120 1380 1120 {lab=RCM}
C {devices/lab_pin.sym} 1380 1120 0 0 {name=L101 lab=RCM}
N 1470 1120 1535 1120 {lab=VSS}
C {devices/lab_pin.sym} 1535 1120 0 0 {name=L102 lab=VSS}
N 1470 1090 1470 1065 {lab=RCM}
C {devices/lab_pin.sym} 1470 1065 0 0 {name=L103 lab=RCM}
N 1470 1150 1470 1175 {lab=VSS}
C {devices/lab_pin.sym} 1470 1175 0 0 {name=L104 lab=VSS}
C {devices/nmos4.sym} 1750 1120 0 0 {name=MCFN4 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN4: 10u/3.2u x1} 1685 1190 0 0 0.18 0.18 {}
N 1730 1120 1680 1120 {lab=RCM}
C {devices/lab_pin.sym} 1680 1120 0 0 {name=L105 lab=RCM}
N 1770 1120 1835 1120 {lab=VSS}
C {devices/lab_pin.sym} 1835 1120 0 0 {name=L106 lab=VSS}
N 1770 1090 1770 1065 {lab=PBIAS}
C {devices/lab_pin.sym} 1770 1065 0 0 {name=L107 lab=PBIAS}
N 1770 1150 1770 1175 {lab=VSS}
C {devices/lab_pin.sym} 1770 1175 0 0 {name=L108 lab=VSS}
C {devices/pmos4.sym} 1750 920 0 0 {name=MCFP1 model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFP1: 10u/3.2u x1} 1685 990 0 0 0.18 0.18 {}
N 1730 920 1680 920 {lab=PBIAS}
C {devices/lab_pin.sym} 1680 920 0 0 {name=L109 lab=PBIAS}
N 1770 920 1835 920 {lab=VDD}
C {devices/lab_pin.sym} 1835 920 0 0 {name=L110 lab=VDD}
N 1770 890 1770 865 {lab=VDD}
C {devices/lab_pin.sym} 1770 865 0 0 {name=L111 lab=VDD}
N 1770 950 1770 975 {lab=PBIAS}
C {devices/lab_pin.sym} 1770 975 0 0 {name=L112 lab=PBIAS}
C {devices/pmos4.sym} 2050 920 0 0 {name=MCFP2 model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFP2: 10u/3.2u x1} 1985 990 0 0 0.18 0.18 {}
N 2030 920 1980 920 {lab=PBIAS}
C {devices/lab_pin.sym} 1980 920 0 0 {name=L113 lab=PBIAS}
N 2070 920 2135 920 {lab=VDD}
C {devices/lab_pin.sym} 2135 920 0 0 {name=L114 lab=VDD}
N 2070 890 2070 865 {lab=VDD}
C {devices/lab_pin.sym} 2070 865 0 0 {name=L115 lab=VDD}
N 2070 950 2070 975 {lab=PC}
C {devices/lab_pin.sym} 2070 975 0 0 {name=L116 lab=PC}
C {devices/nmos4.sym} 70 740 0 0 {name=MREF model=N w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MREF: 20u/3.2u x1} 5 810 0 0 0.18 0.18 {}
N 50 740 0 740 {lab=IREF}
C {devices/lab_pin.sym} 0 740 0 0 {name=L117 lab=IREF}
N 90 740 155 740 {lab=VSS}
C {devices/lab_pin.sym} 155 740 0 0 {name=L118 lab=VSS}
N 90 710 90 685 {lab=IREF}
C {devices/lab_pin.sym} 90 685 0 0 {name=L119 lab=IREF}
N 90 770 90 795 {lab=VSS}
C {devices/lab_pin.sym} 90 795 0 0 {name=L120 lab=VSS}
N 240 155 240 195 {lab=PX1}
N 240 305 240 345 {lab=OUTM}
N 240 455 240 495 {lab=NX1}
N 240 605 240 670 {lab=TAIL}
N 540 155 540 195 {lab=PX2}
N 540 305 540 345 {lab=OUTP}
N 540 455 540 495 {lab=NX2}
N 540 605 540 670 {lab=TAIL}
N 240 670 540 670 {lab=TAIL}
N 390 670 390 685 {lab=TAIL}
N 920 175 920 265 {lab=SP}
N 1220 175 1220 265 {lab=SM}
N 1520 175 1520 265 {lab=SR}
C {scl08_rpp_cmfb.sym} 900 520 0 0 {name=XSP w=2.4u l=17142.857143u}
N 870 520 830 520 {lab=SP}
C {devices/lab_pin.sym} 830 520 0 0 {name=L121 lab=SP}
N 930 520 980 520 {lab=SENSE}
C {devices/lab_pin.sym} 980 520 0 0 {name=L122 lab=SENSE}
C {scl08_rpp_cmfb.sym} 1200 520 0 0 {name=XSM w=2.4u l=17142.857143u}
N 1170 520 1130 520 {lab=SM}
C {devices/lab_pin.sym} 1130 520 0 0 {name=L123 lab=SM}
N 1230 520 1280 520 {lab=SENSE}
C {devices/lab_pin.sym} 1280 520 0 0 {name=L124 lab=SENSE}
N 1270 775 1270 810 {lab=CT}
N 1170 810 1470 810 {lab=CT}
N 1170 810 1170 865 {lab=CT}
N 1470 810 1470 865 {lab=CT}
N 1170 975 1170 1065 {lab=CA}
N 1470 975 1470 1065 {lab=RCM}
C {devices/iopin.sym} -180 80 0 0 {name=P0 lab=INP}
C {devices/iopin.sym} -180 140 0 0 {name=P1 lab=INN}
C {devices/iopin.sym} -180 200 0 0 {name=P2 lab=OUTP}
C {devices/iopin.sym} -180 260 0 0 {name=P3 lab=OUTM}
C {devices/iopin.sym} -180 320 0 0 {name=P4 lab=VDD}
C {devices/iopin.sym} -180 380 0 0 {name=P5 lab=VSS}
C {devices/iopin.sym} -180 440 0 0 {name=P6 lab=IREF}
C {devices/iopin.sym} -180 500 0 0 {name=P7 lab=VCM}
C {devices/iopin.sym} -180 560 0 0 {name=P8 lab=VBN}
C {devices/iopin.sym} -180 620 0 0 {name=P9 lab=VBP}
T {SCL800 telescopic OTA: unchanged signal core} 20 -30 0 0 0.35 0.35 {}
T {NMOS sensing buffers + 200k averaging} 800 -30 0 0 0.35 0.35 {}
T {CMFB error amplifier and mirror level shift} 800 620 0 0 0.35 0.35 {}
T {MOS compensation} 1950 -30 0 0 0.35 0.35 {}
T {IREF=3.5uA; VBN=3.0V; VBP=VDD-2.2V; VCM=2.5V; input CM=2.5V (nominal VDD=5V).
Drawing is the transistor schematic; simulate supplied extracted macro for layout results.
Signal labels join repeated nodes. Resistor layout uses 40 series sections per 200k bank.} 20 1250 0 0 0.25 0.25 {}
