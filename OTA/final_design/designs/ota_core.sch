v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {SCL08 fully differential telescopic OTA} 25 -80 0 0 0.48 0.48 {}
T {Continuous-time common-mode feedback   |   Final SC integration bias} 28 -36 0 0 0.24 0.24 {}
B 4 0 0 785 695 {fill=false}
T {(a) Telescopic signal core and bias mirror} 18 14 0 0 0.32 0.32 {}
B 4 815 0 2070 352 {fill=false}
T {(b) Output common-mode sensing} 833 14 0 0 0.32 0.32 {}
B 4 815 385 2070 1000 {fill=false}
T {(c) CMFB error amplifier and current mirrors} 833 399 0 0 0.32 0.32 {}
B 4 0 728 785 1000 {fill=false}
T {(d) Miller-style and shunt compensation} 18 742 0 0 0.32 0.32 {}
C {devices/pmos4.sym} 270 130 0 1 {name=MP1 model=P w=40u l=3.2u m=1 extra="AD=180p AS=180p PD=89u PS=89u" hide_texts=true}
T {MP1} 130 107 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 250 130 0 0 {name=L1 lab=VDD}
C {devices/pmos4.sym} 270 250 0 1 {name=MPC1 model=P w=60u l=2.4u m=1 extra="AD=270p AS=270p PD=129u PS=129u" hide_texts=true}
T {MPC1} 130 227 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 250 250 0 0 {name=L2 lab=VDD}
C {devices/nmos4.sym} 270 430 0 1 {name=MNC1 model=N w=30u l=2.4u m=1 extra="AD=135p AS=135p PD=69u PS=69u" hide_texts=true}
T {MNC1} 130 407 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 250 430 0 0 {name=L3 lab=VSS}
C {devices/nmos4.sym} 230 550 0 0 {name=MN1 model=N w=15u l=2.4u m=1 extra="AD=67.5p AS=67.5p PD=39u PS=39u" hide_texts=true}
T {MN1} 277 527 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 250 550 0 1 {name=L4 lab=VSS}
N 210 550 175 550 {lab=INP}
C {devices/lab_pin.sym} 175 550 0 0 {name=L5 lab=INP}
N 250 100 250 77 {lab=VDD}
N 250 160 250 190 {lab=PX1}
N 250 190 250 220 {lab=PX1}
C {devices/lab_pin.sym} 250 190 0 0 {name=L6 lab=PX1}
N 250 280 250 340 {lab=OUTM}
N 250 340 250 400 {lab=OUTM}
N 250 340 145 340 {lab=OUTM}
C {devices/lab_pin.sym} 145 340 0 0 {name=L7 lab=OUTM}
N 250 460 250 490 {lab=NX1}
N 250 490 250 520 {lab=NX1}
C {devices/lab_pin.sym} 250 490 0 0 {name=L8 lab=NX1}
N 250 580 250 595 {lab=TAIL}
C {devices/pmos4.sym} 520 130 0 0 {name=MP2 model=P w=40u l=3.2u m=1 extra="AD=180p AS=180p PD=89u PS=89u" hide_texts=true}
T {MP2} 567 107 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 540 130 0 1 {name=L9 lab=VDD}
C {devices/pmos4.sym} 520 250 0 0 {name=MPC2 model=P w=60u l=2.4u m=1 extra="AD=270p AS=270p PD=129u PS=129u" hide_texts=true}
T {MPC2} 567 227 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 540 250 0 1 {name=L10 lab=VDD}
C {devices/nmos4.sym} 520 430 0 0 {name=MNC2 model=N w=30u l=2.4u m=1 extra="AD=135p AS=135p PD=69u PS=69u" hide_texts=true}
T {MNC2} 567 407 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 540 430 0 1 {name=L11 lab=VSS}
C {devices/nmos4.sym} 560 550 0 1 {name=MN2 model=N w=15u l=2.4u m=1 extra="AD=67.5p AS=67.5p PD=39u PS=39u" hide_texts=true}
T {MN2} 420 527 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 540 550 0 0 {name=L12 lab=VSS}
N 580 550 615 550 {lab=INN}
C {devices/lab_pin.sym} 615 550 0 1 {name=L13 lab=INN}
N 540 100 540 77 {lab=VDD}
N 540 160 540 190 {lab=PX2}
N 540 190 540 220 {lab=PX2}
C {devices/lab_pin.sym} 540 190 0 1 {name=L14 lab=PX2}
N 540 280 540 340 {lab=OUTP}
N 540 340 540 400 {lab=OUTP}
N 540 340 645 340 {lab=OUTP}
C {devices/lab_pin.sym} 645 340 0 1 {name=L15 lab=OUTP}
N 540 460 540 490 {lab=NX2}
N 540 490 540 520 {lab=NX2}
C {devices/lab_pin.sym} 540 490 0 1 {name=L16 lab=NX2}
N 540 580 540 595 {lab=TAIL}
N 250 77 540 77 {lab=VDD}
C {devices/lab_pin.sym} 250 77 0 0 {name=L17 lab=VDD}
N 290 130 500 130 {lab=PC}
C {devices/lab_pin.sym} 395 130 0 1 {name=L18 lab=PC}
N 290 250 500 250 {lab=VBP}
C {devices/lab_pin.sym} 395 250 0 1 {name=L19 lab=VBP}
N 290 430 500 430 {lab=VBN}
C {devices/lab_pin.sym} 395 430 0 1 {name=L20 lab=VBN}
N 250 595 395 595 {lab=TAIL}
N 395 595 540 595 {lab=TAIL}
C {devices/lab_pin.sym} 395 595 0 1 {name=L21 lab=TAIL}
C {devices/nmos4.sym} 375 640 0 0 {name=MTAIL model=N w=80.0u l=3.2u m=1 extra="AD=360p AS=360p PD=169u PS=169u" hide_texts=true}
T {MTAIL} 422 617 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 395 640 0 1 {name=L22 lab=VSS}
N 395 595 395 610 {lab=TAIL}
C {devices/nmos4.sym} 145 640 0 1 {name=MREF model=N w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MREF} 5 617 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 125 640 0 0 {name=L23 lab=VSS}
N 165 640 183 640 {lab=IREF}
N 183 640 183 585 {lab=IREF}
N 183 585 125 585 {lab=IREF}
N 125 585 125 610 {lab=IREF}
C {devices/lab_pin.sym} 125 585 0 0 {name=L24 lab=IREF}
N 165 640 183 640 {lab=IREF}
N 183 640 355 640 {lab=IREF}
N 125 670 395 670 {lab=VSS}
C {devices/lab_pin.sym} 125 670 0 0 {name=L25 lab=VSS}
C {devices/nmos4.sym} 980 106 0 0 {name=MSP model=N w=20u l=1.6u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSP ×4} 1027 83 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1000 106 0 1 {name=L26 lab=VSS}
N 960 106 925 106 {lab=OUTP}
C {devices/lab_pin.sym} 925 106 0 0 {name=L27 lab=OUTP}
N 1000 76 1000 65 {lab=VDD}
C {devices/lab_pin.sym} 1000 65 0 1 {name=L28 lab=VDD}
C {devices/nmos4.sym} 980 218 0 0 {name=MSIP model=N w=20u l=3.2u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIP ×2} 1027 195 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1000 218 0 1 {name=L29 lab=VSS}
N 960 218 925 218 {lab=IREF}
C {devices/lab_pin.sym} 925 218 0 0 {name=L30 lab=IREF}
N 1000 248 1000 266 {lab=VSS}
C {devices/lab_pin.sym} 1000 266 0 1 {name=L31 lab=VSS}
N 1000 136 1000 164 {lab=SP}
N 1000 164 1000 188 {lab=SP}
N 1000 164 1090 164 {lab=SP}
C {devices/lab_pin.sym} 1090 164 0 1 {name=L32 lab=SP}
C {devices/nmos4.sym} 1360 106 0 0 {name=MSM model=N w=20u l=1.6u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSM ×4} 1407 83 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1380 106 0 1 {name=L33 lab=VSS}
N 1340 106 1305 106 {lab=OUTM}
C {devices/lab_pin.sym} 1305 106 0 0 {name=L34 lab=OUTM}
N 1380 76 1380 65 {lab=VDD}
C {devices/lab_pin.sym} 1380 65 0 1 {name=L35 lab=VDD}
C {devices/nmos4.sym} 1360 218 0 0 {name=MSIM model=N w=20u l=3.2u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIM ×2} 1407 195 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1380 218 0 1 {name=L36 lab=VSS}
N 1340 218 1305 218 {lab=IREF}
C {devices/lab_pin.sym} 1305 218 0 0 {name=L37 lab=IREF}
N 1380 248 1380 266 {lab=VSS}
C {devices/lab_pin.sym} 1380 266 0 1 {name=L38 lab=VSS}
N 1380 136 1380 164 {lab=SM}
N 1380 164 1380 188 {lab=SM}
N 1380 164 1470 164 {lab=SM}
C {devices/lab_pin.sym} 1470 164 0 1 {name=L39 lab=SM}
C {devices/nmos4.sym} 1740 106 0 0 {name=MSR model=N w=20u l=1.6u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSR ×4} 1787 83 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1760 106 0 1 {name=L40 lab=VSS}
N 1720 106 1685 106 {lab=VCM}
C {devices/lab_pin.sym} 1685 106 0 0 {name=L41 lab=VCM}
N 1760 76 1760 65 {lab=VDD}
C {devices/lab_pin.sym} 1760 65 0 1 {name=L42 lab=VDD}
C {devices/nmos4.sym} 1740 218 0 0 {name=MSIR model=N w=20u l=3.2u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIR ×2} 1787 195 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1760 218 0 1 {name=L43 lab=VSS}
N 1720 218 1685 218 {lab=IREF}
C {devices/lab_pin.sym} 1685 218 0 0 {name=L44 lab=IREF}
N 1760 248 1760 266 {lab=VSS}
C {devices/lab_pin.sym} 1760 266 0 1 {name=L45 lab=VSS}
N 1760 136 1760 164 {lab=SR}
N 1760 164 1760 188 {lab=SR}
N 1760 164 1850 164 {lab=SR}
C {devices/lab_pin.sym} 1850 164 0 1 {name=L46 lab=SR}
C {scl08_rpp_cmfb.sym} 1190 311 0 0 {name=XSP w=2.4u l=17142.857143u}
C {scl08_rpp_cmfb.sym} 1530 311 0 1 {name=XSM w=2.4u l=17142.857143u}
N 1100 311 1160 311 {lab=SP}
C {devices/lab_pin.sym} 1100 311 0 0 {name=L47 lab=SP}
N 1220 311 1360 311 {lab=SENSE}
N 1360 311 1500 311 {lab=SENSE}
C {devices/lab_pin.sym} 1360 311 0 1 {name=L48 lab=SENSE}
N 1560 311 1620 311 {lab=SM}
C {devices/lab_pin.sym} 1620 311 0 1 {name=L49 lab=SM}
C {devices/pmos4.sym} 1260 495 0 0 {name=MCT model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCT} 1307 472 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1280 495 0 1 {name=L50 lab=VDD}
N 1240 495 1205 495 {lab=CB}
C {devices/lab_pin.sym} 1205 495 0 0 {name=L51 lab=CB}
N 1280 465 1280 456 {lab=VDD}
C {devices/lab_pin.sym} 1280 456 0 1 {name=L52 lab=VDD}
C {devices/pmos4.sym} 980 665 0 1 {name=MCBI model=P w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCBI} 840 642 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 960 665 0 0 {name=L53 lab=VDD}
N 1000 665 1018 665 {lab=CB}
N 1018 665 1018 720 {lab=CB}
N 1018 720 960 720 {lab=CB}
N 960 720 960 695 {lab=CB}
N 960 635 960 596 {lab=VDD}
C {devices/lab_pin.sym} 960 596 0 1 {name=L54 lab=VDD}
C {devices/nmos4.sym} 940 875 0 0 {name=MCBN model=N w=11.428571u l=3.2u m=1 extra="AD=51.4286p AS=51.4286p PD=31.8571u PS=31.8571u" hide_texts=true}
T {MCBN} 987 852 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 960 875 0 1 {name=L55 lab=VSS}
N 920 875 885 875 {lab=IREF}
C {devices/lab_pin.sym} 885 875 0 0 {name=L56 lab=IREF}
C {devices/pmos4.sym} 1150 665 0 0 {name=MCS model=P w=5u l=2.4u m=1 extra="AD=22.5p AS=22.5p PD=19u PS=19u" hide_texts=true}
T {MCS} 1197 642 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1170 665 0 1 {name=L57 lab=VDD}
N 1130 665 1124 665 {lab=SENSE}
C {devices/lab_pin.sym} 1124 665 0 0 {name=L58 lab=SENSE}
C {devices/pmos4.sym} 1410 665 0 1 {name=MCR model=P w=5u l=2.4u m=1 extra="AD=22.5p AS=22.5p PD=19u PS=19u" hide_texts=true}
T {MCR} 1270 642 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1390 665 0 0 {name=L59 lab=VDD}
N 1430 665 1465 665 {lab=SR}
C {devices/lab_pin.sym} 1465 665 0 1 {name=L60 lab=SR}
C {devices/nmos4.sym} 1150 875 0 0 {name=MCFN1 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN1} 1197 852 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1170 875 0 1 {name=L61 lab=VSS}
N 1130 875 1112 875 {lab=CA}
N 1112 875 1112 820 {lab=CA}
N 1112 820 1170 820 {lab=CA}
N 1170 820 1170 845 {lab=CA}
C {devices/nmos4.sym} 1370 875 0 0 {name=MCFN3 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN3} 1417 852 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1390 875 0 1 {name=L62 lab=VSS}
N 1350 875 1332 875 {lab=RCM}
N 1332 875 1332 820 {lab=RCM}
N 1332 820 1390 820 {lab=RCM}
N 1390 820 1390 845 {lab=RCM}
C {devices/pmos4.sym} 1630 665 0 1 {name=MCFP1 model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFP1} 1490 642 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1610 665 0 0 {name=L63 lab=VDD}
N 1650 665 1668 665 {lab=PBIAS}
N 1668 665 1668 720 {lab=PBIAS}
N 1668 720 1610 720 {lab=PBIAS}
N 1610 720 1610 695 {lab=PBIAS}
N 1610 635 1610 596 {lab=VDD}
C {devices/lab_pin.sym} 1610 596 0 1 {name=L64 lab=VDD}
C {devices/nmos4.sym} 1590 875 0 0 {name=MCFN4 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN4} 1637 852 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1610 875 0 1 {name=L65 lab=VSS}
N 1570 875 1535 875 {lab=RCM}
C {devices/lab_pin.sym} 1535 875 0 0 {name=L66 lab=RCM}
C {devices/pmos4.sym} 1830 665 0 0 {name=MCFP2 model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFP2} 1877 642 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1850 665 0 1 {name=L67 lab=VDD}
N 1810 665 1775 665 {lab=PBIAS}
C {devices/lab_pin.sym} 1775 665 0 0 {name=L68 lab=PBIAS}
N 1850 635 1850 596 {lab=VDD}
C {devices/lab_pin.sym} 1850 596 0 1 {name=L69 lab=VDD}
C {devices/nmos4.sym} 1830 875 0 0 {name=MCFN2 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN2} 1877 852 0 0 0.2 0.2 {}
C {devices/lab_pin.sym} 1850 875 0 1 {name=L70 lab=VSS}
N 1810 875 1775 875 {lab=CA}
C {devices/lab_pin.sym} 1775 875 0 0 {name=L71 lab=CA}
N 1280 525 1280 570 {lab=CT}
N 1170 635 1170 570 {lab=CT}
N 1170 570 1280 570 {lab=CT}
N 1280 570 1390 570 {lab=CT}
N 1390 570 1390 635 {lab=CT}
C {devices/lab_pin.sym} 1280 570 0 1 {name=L72 lab=CT}
N 960 720 960 773 {lab=CB}
N 960 773 960 845 {lab=CB}
N 960 773 1025 773 {lab=CB}
C {devices/lab_pin.sym} 1025 773 0 1 {name=L73 lab=CB}
N 1170 695 1170 773 {lab=CA}
N 1170 773 1170 820 {lab=CA}
N 1170 773 1235 773 {lab=CA}
C {devices/lab_pin.sym} 1235 773 0 1 {name=L74 lab=CA}
N 1390 695 1390 773 {lab=RCM}
N 1390 773 1390 820 {lab=RCM}
N 1390 773 1455 773 {lab=RCM}
C {devices/lab_pin.sym} 1455 773 0 1 {name=L75 lab=RCM}
N 1610 720 1610 773 {lab=PBIAS}
N 1610 773 1610 845 {lab=PBIAS}
N 1610 773 1675 773 {lab=PBIAS}
C {devices/lab_pin.sym} 1675 773 0 1 {name=L76 lab=PBIAS}
N 1850 695 1850 773 {lab=PC}
N 1850 773 1850 845 {lab=PC}
N 1850 773 1915 773 {lab=PC}
C {devices/lab_pin.sym} 1915 773 0 1 {name=L77 lab=PC}
N 960 905 960 952 {lab=VSS}
N 1170 905 1170 952 {lab=VSS}
N 1390 905 1390 952 {lab=VSS}
N 1610 905 1610 952 {lab=VSS}
N 1850 905 1850 952 {lab=VSS}
N 960 952 1170 952 {lab=VSS}
N 1170 952 1390 952 {lab=VSS}
N 1390 952 1610 952 {lab=VSS}
N 1610 952 1850 952 {lab=VSS}
C {devices/lab_pin.sym} 960 952 0 0 {name=L78 lab=VSS}
C {devices/pmos4.sym} 140 862 0 0 {name=MCC model=P w=20u l=10u m=4 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCC ×4} 187 839 0 0 0.2 0.2 {}
N 160 832 160 808 {lab=VDD}
N 160 808 225 808 {lab=VDD}
N 225 808 225 916 {lab=VDD}
N 225 916 160 916 {lab=VDD}
N 160 916 160 892 {lab=VDD}
N 160 862 225 862 {lab=VDD}
C {devices/lab_pin.sym} 225 808 0 1 {name=L79 lab=VDD}
N 120 862 120 955 {lab=PC}
C {devices/pmos4.sym} 375 862 0 0 {name=MCM1 model=P w=20u l=10u m=12 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCM1 ×12} 422 839 0 0 0.2 0.2 {}
N 395 832 395 808 {lab=OUTP}
N 395 808 460 808 {lab=OUTP}
N 460 808 460 916 {lab=OUTP}
N 460 916 395 916 {lab=OUTP}
N 395 916 395 892 {lab=OUTP}
N 395 862 460 862 {lab=OUTP}
C {devices/lab_pin.sym} 460 808 0 1 {name=L80 lab=OUTP}
N 355 862 355 955 {lab=PC}
C {devices/pmos4.sym} 615 862 0 0 {name=MCM2 model=P w=20u l=10u m=12 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCM2 ×12} 662 839 0 0 0.2 0.2 {}
N 635 832 635 808 {lab=OUTM}
N 635 808 700 808 {lab=OUTM}
N 700 808 700 916 {lab=OUTM}
N 700 916 635 916 {lab=OUTM}
N 635 916 635 892 {lab=OUTM}
N 635 862 700 862 {lab=OUTM}
C {devices/lab_pin.sym} 700 808 0 1 {name=L81 lab=OUTM}
N 595 862 595 955 {lab=PC}
N 120 955 355 955 {lab=PC}
N 355 955 595 955 {lab=PC}
N 595 955 695 955 {lab=PC}
C {devices/lab_pin.sym} 695 955 0 1 {name=L82 lab=PC}
C {devices/iopin.sym} 85 1055 0 0 {name=P0 lab=INP}
C {devices/iopin.sym} 289 1055 0 0 {name=P1 lab=INN}
C {devices/iopin.sym} 493 1055 0 0 {name=P2 lab=OUTP}
C {devices/iopin.sym} 697 1055 0 0 {name=P3 lab=OUTM}
C {devices/iopin.sym} 901 1055 0 0 {name=P4 lab=VDD}
C {devices/iopin.sym} 1105 1055 0 0 {name=P5 lab=VSS}
C {devices/iopin.sym} 1309 1055 0 0 {name=P6 lab=IREF}
C {devices/iopin.sym} 1513 1055 0 0 {name=P7 lab=VCM}
C {devices/iopin.sym} 1717 1055 0 0 {name=P8 lab=VBN}
C {devices/iopin.sym} 1921 1055 0 0 {name=P9 lab=VBP}
T {Nominal bias   VDD 5 V   VSS 0 V   IREF 3.5 uA   VBN 3.0 V   VBP = VDD - 2.2 V   VCM 2.5 V} 0 1091 0 0 0.24 0.24 {}
T {Matching labels connect across panels. MOS capacitor bulks connect to their local source and drain.} 0 1120 0 0 0.2 0.2 {}
