v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {SCL08 fully differential telescopic OTA} 25 -80 0 0 0.48 0.48 {}
T {Continuous-time common-mode feedback   |   NMOS sense resistors and reduced follower current} 28 -36 0 0 0.24 0.24 {}
T {(a) Telescopic signal core and bias mirror} 18 14 0 0 0.39 0.39 {}
T {(b) Output common-mode sensing} 1293 14 0 0 0.39 0.39 {}
T {(c) CMFB error amplifier and current mirrors} 1293 694 0 0 0.39 0.39 {}
T {(d) Output-to-PC common-mode compensation} 18 1222 0 0 0.39 0.39 {}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 305 200 0 1 {name=MP1 model=P w=40u l=3.2u m=1 extra="AD=180p AS=180p PD=89u PS=89u" hide_texts=true}
T {MP1} 202 169 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 305 320 0 1 {name=MPC1 model=P w=60u l=2.4u m=1 extra="AD=270p AS=270p PD=129u PS=129u" hide_texts=true}
T {MPC1} 202 289 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 305 725 0 1 {name=MNC1 model=N w=30u l=2.4u m=1 extra="AD=135p AS=135p PD=69u PS=69u" hide_texts=true}
T {MNC1} 202 694 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 265 895 0 0 {name=MN1 model=N w=15u l=2.4u m=1 extra="AD=67.5p AS=67.5p PD=39u PS=39u" hide_texts=true}
T {MN1} 315 864 0 0 0.24 0.24 {}
N 245 895 210 895 {lab=INP}
N 285 170 285 147 {lab=VDD}
N 285 230 285 260 {lab=PX1}
N 285 260 285 290 {lab=PX1}
N 285 350 285 525 {lab=OUTM}
N 285 525 285 695 {lab=OUTM}
N 285 525 180 525 {lab=OUTM}
N 285 755 285 835 {lab=NX1}
N 285 835 285 865 {lab=NX1}
N 285 925 285 985 {lab=TAIL}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 645 200 0 0 {name=MP2 model=P w=40u l=3.2u m=1 extra="AD=180p AS=180p PD=89u PS=89u" hide_texts=true}
T {MP2} 695 169 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 645 320 0 0 {name=MPC2 model=P w=60u l=2.4u m=1 extra="AD=270p AS=270p PD=129u PS=129u" hide_texts=true}
T {MPC2} 695 289 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 645 725 0 0 {name=MNC2 model=N w=30u l=2.4u m=1 extra="AD=135p AS=135p PD=69u PS=69u" hide_texts=true}
T {MNC2} 695 694 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 685 895 0 1 {name=MN2 model=N w=15u l=2.4u m=1 extra="AD=67.5p AS=67.5p PD=39u PS=39u" hide_texts=true}
T {MN2} 582 864 0 0 0.24 0.24 {}
N 705 895 740 895 {lab=INN}
N 665 170 665 147 {lab=VDD}
N 665 230 665 260 {lab=PX2}
N 665 260 665 290 {lab=PX2}
N 665 350 665 525 {lab=OUTP}
N 665 525 665 695 {lab=OUTP}
N 665 525 770 525 {lab=OUTP}
N 665 755 665 835 {lab=NX2}
N 665 835 665 865 {lab=NX2}
N 665 925 665 985 {lab=TAIL}
N 285 147 665 147 {lab=VDD}
N 325 200 625 200 {lab=PC}
N 325 320 625 320 {lab=VBP}
N 325 725 625 725 {lab=VBN}
N 285 985 475 985 {lab=TAIL}
N 475 985 665 985 {lab=TAIL}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 455 1030 0 0 {name=MTAIL model=N w=80.0u l=3.2u m=1 extra="AD=360p AS=360p PD=169u PS=169u" hide_texts=true}
T {MTAIL} 505 999 0 0 0.24 0.24 {}
N 475 985 475 1000 {lab=TAIL}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 180 1030 0 1 {name=MREF model=N w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MREF} 77 999 0 0 0.24 0.24 {}
N 200 1030 218 1030 {lab=IREF}
N 218 1030 218 975 {lab=IREF}
N 218 975 160 975 {lab=IREF}
N 160 975 160 1000 {lab=IREF}
N 218 1030 435 1030 {lab=IREF}
N 160 1060 475 1060 {lab=VSS}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 1490 176 0 0 {name=MSP model=N w=20u l=1.6u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSP ×2} 1540 145 0 0 0.24 0.24 {}
N 1470 176 1435 176 {lab=OUTP}
N 1510 146 1510 100 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 1490 288 0 0 {name=MSIP model=N w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIP } 1540 257 0 0 0.24 0.24 {}
N 1470 288 1435 288 {lab=IREF}
N 1510 318 1510 336 {lab=VSS}
N 1510 206 1510 234 {lab=SP}
N 1510 234 1510 258 {lab=SP}
N 1510 234 1735 234 {lab=SP}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2090 176 0 0 {name=MSM model=N w=20u l=1.6u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSM ×2} 2140 145 0 0 0.24 0.24 {}
N 2070 176 2005 176 {lab=OUTM}
N 2110 146 2110 100 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2090 288 0 0 {name=MSIM model=N w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIM } 2140 257 0 0 0.24 0.24 {}
N 2070 288 2005 288 {lab=IREF}
N 2110 318 2110 336 {lab=VSS}
N 2110 206 2110 234 {lab=SM}
N 2110 234 2110 258 {lab=SM}
N 2110 234 2200 234 {lab=SM}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2605 176 0 0 {name=MSR model=N w=20u l=1.6u m=2 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSR ×2} 2655 145 0 0 0.24 0.24 {}
N 2585 176 2550 176 {lab=VCM}
N 2625 146 2625 100 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2605 288 0 0 {name=MSIR model=N w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MSIR } 2655 257 0 0 0.24 0.24 {}
N 2585 288 2550 288 {lab=IREF}
N 2625 318 2625 336 {lab=VSS}
N 2625 206 2625 234 {lab=SR}
N 2625 234 2625 258 {lab=SR}
N 2625 234 2715 234 {lab=SR}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/ota_tri_vcr.sym} 1890 431 0 0 {name=MVCRPN}
N 1890 401 1890 379 {lab=VDD}
N 1890 461 1890 487 {lab=VSS}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1890 379 0 0 {name=VGP lab=VDD}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1890 487 0 0 {name=VBP lab=VSS}
T {NMOS VCR P} 1850 515 0 0 0.26 0.26 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/ota_tri_vcr.sym} 2330 431 0 1 {name=MVCRMN}
N 2330 401 2330 379 {lab=VDD}
N 2330 461 2330 487 {lab=VSS}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2330 379 0 0 {name=VGM lab=VDD}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2330 487 0 0 {name=VBM lab=VSS}
T {NMOS VCR M} 2290 515 0 0 0.26 0.26 {}
N 1745 431 1860 431 {lab=SP}
N 1920 431 2090 431 {lab=SENSE}
N 2090 431 2300 431 {lab=SENSE}
N 2360 431 2420 431 {lab=SM}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 1960 840 0 0 {name=MCT model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCT} 2010 809 0 0 0.24 0.24 {}
N 1940 840 1905 840 {lab=CB}
N 1980 810 1980 751 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 1490 1055 0 1 {name=MCBI model=P w=20u l=3.2u m=1 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCBI} 1387 1024 0 0 0.24 0.24 {}
N 1510 1055 1528 1055 {lab=CB}
N 1528 1055 1528 1155 {lab=CB}
N 1528 1155 1470 1155 {lab=CB}
N 1470 1155 1470 1085 {lab=CB}
N 1470 1025 1470 986 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 1450 1460 0 0 {name=MCBN model=N w=11.428571u l=3.2u m=1 extra="AD=51.4286p AS=51.4286p PD=31.8571u PS=31.8571u" hide_texts=true}
T {MCBN} 1500 1429 0 0 0.24 0.24 {}
N 1430 1460 1345 1460 {lab=IREF}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 1850 1055 0 0 {name=MCS model=P w=5u l=2.4u m=1 extra="AD=22.5p AS=22.5p PD=19u PS=19u" hide_texts=true}
T {MCS} 1900 1024 0 0 0.24 0.24 {}
N 1830 1055 1824 1055 {lab=SENSE}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 2140 1055 0 1 {name=MCR model=P w=5u l=2.4u m=1 extra="AD=22.5p AS=22.5p PD=19u PS=19u" hide_texts=true}
T {MCR} 2037 1024 0 0 0.24 0.24 {}
N 2160 1055 2195 1055 {lab=SR}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 1850 1460 0 0 {name=MCFN1 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN1} 1900 1429 0 0 0.24 0.24 {}
N 1830 1460 1812 1460 {lab=CA}
N 1812 1460 1812 1405 {lab=CA}
N 1812 1405 1870 1405 {lab=CA}
N 1870 1405 1870 1430 {lab=CA}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2100 1460 0 0 {name=MCFN3 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN3} 2150 1429 0 0 0.24 0.24 {}
N 2080 1460 2062 1460 {lab=RCM}
N 2062 1460 2062 1405 {lab=RCM}
N 2062 1405 2120 1405 {lab=RCM}
N 2120 1405 2120 1430 {lab=RCM}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 2430 1055 0 1 {name=MCFP1 model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFP1} 2327 1024 0 0 0.24 0.24 {}
N 2450 1055 2468 1055 {lab=PBIAS}
N 2468 1055 2468 1155 {lab=PBIAS}
N 2468 1155 2410 1155 {lab=PBIAS}
N 2410 1155 2410 1085 {lab=PBIAS}
N 2410 1025 2410 986 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2390 1460 0 0 {name=MCFN4 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN4} 2440 1429 0 0 0.24 0.24 {}
N 2370 1460 2335 1460 {lab=RCM}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 2695 1055 0 0 {name=MCFP2 model=P w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFP2} 2745 1024 0 0 0.24 0.24 {}
N 2675 1055 2640 1055 {lab=PBIAS}
N 2715 1025 2715 986 {lab=VDD}
C {/usr/share/xschem/xschem_library/devices/nmos4.sym} 2695 1460 0 0 {name=MCFN2 model=N w=10u l=3.2u m=1 extra="AD=45p AS=45p PD=29u PS=29u" hide_texts=true}
T {MCFN2} 2745 1429 0 0 0.24 0.24 {}
N 2675 1460 2640 1460 {lab=CA}
N 1980 870 1980 915 {lab=CT}
N 1870 1025 1870 915 {lab=CT}
N 1870 915 1980 915 {lab=CT}
N 1980 915 2120 915 {lab=CT}
N 2120 915 2120 1025 {lab=CT}
N 1470 1155 1470 1303 {lab=CB}
N 1470 1303 1470 1430 {lab=CB}
N 1470 1303 1535 1303 {lab=CB}
N 1870 1085 1870 1303 {lab=CA}
N 1870 1303 1870 1405 {lab=CA}
N 1870 1303 1935 1303 {lab=CA}
N 2120 1085 2120 1303 {lab=RCM}
N 2120 1303 2120 1405 {lab=RCM}
N 2120 1303 2185 1303 {lab=RCM}
N 2410 1155 2410 1303 {lab=PBIAS}
N 2410 1303 2410 1430 {lab=PBIAS}
N 2410 1303 2475 1303 {lab=PBIAS}
N 2715 1085 2715 1303 {lab=PC}
N 2715 1303 2715 1430 {lab=PC}
N 2715 1303 2835 1303 {lab=PC}
N 1470 1490 1470 1602 {lab=VSS}
N 1870 1490 1870 1602 {lab=VSS}
N 2120 1490 2120 1602 {lab=VSS}
N 2410 1490 2410 1602 {lab=VSS}
N 2715 1490 2715 1602 {lab=VSS}
N 1470 1602 1870 1602 {lab=VSS}
N 1870 1602 2120 1602 {lab=VSS}
N 2120 1602 2410 1602 {lab=VSS}
N 2410 1602 2715 1602 {lab=VSS}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 455 1447 0 0 {name=MCM1 model=P w=20u l=10u m=12 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCM1 ×12} 505 1416 0 0 0.24 0.24 {}
N 475 1417 475 1338 {lab=OUTP}
N 475 1338 585 1338 {lab=OUTP}
N 585 1338 585 1501 {lab=OUTP}
N 585 1501 475 1501 {lab=OUTP}
N 475 1501 475 1477 {lab=OUTP}
N 475 1447 585 1447 {lab=OUTP}
N 435 1447 435 1605 {lab=PC}
C {/usr/share/xschem/xschem_library/devices/pmos4.sym} 740 1447 0 0 {name=MCM2 model=P w=20u l=10u m=12 extra="AD=90p AS=90p PD=49u PS=49u" hide_texts=true}
T {MCM2 ×12} 790 1416 0 0 0.24 0.24 {}
N 760 1417 760 1338 {lab=OUTM}
N 760 1338 860 1338 {lab=OUTM}
N 860 1338 860 1501 {lab=OUTM}
N 860 1501 760 1501 {lab=OUTM}
N 760 1501 760 1477 {lab=OUTM}
N 760 1447 860 1447 {lab=OUTM}
N 720 1447 720 1605 {lab=PC}
N 435 1605 720 1605 {lab=PC}
N 720 1605 855 1605 {lab=PC}
T {Nominal bias   VDD 5 V   VSS 0 V   IREF set by bias fanout   VBN 3.0 V   VBP = VDD - 2.2 V   VCM 2.5 V} 0 1886 0 0 0.24 0.24 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 210 895 0 1 {name=P0 lab=INP}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 740 895 0 0 {name=P1 lab=INN}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 770 610 0 0 {name=P2 lab=OUTP}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 180 610 0 1 {name=P3 lab=OUTM}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 35 90 0 1 {name=P4 lab=VDD}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 35 1755 0 1 {name=P5 lab=VSS}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 160 975 0 1 {name=P6 lab=IREF}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 2550 176 0 1 {name=P7 lab=VCM}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 475 750 0 0 {name=P8 lab=VBN}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 475 345 0 0 {name=P9 lab=VBP}
N 475 725 475 750 {lab=VBN}
N 475 320 475 345 {lab=VBP}
N 770 525 770 610 {lab=OUTP}
N 180 525 180 610 {lab=OUTM}
N 35 90 3165 90 {lab=VDD}
N 285 147 285 90 {lab=VDD}
N 285 200 250 200 {lab=VDD}
N 250 200 250 90 {lab=VDD}
N 285 320 250 320 {lab=VDD}
N 250 320 250 200 {lab=VDD}
N 665 200 700 200 {lab=VDD}
N 700 200 700 90 {lab=VDD}
N 665 320 700 320 {lab=VDD}
N 700 320 700 200 {lab=VDD}
N 1510 100 1510 90 {lab=VDD}
N 2110 100 2110 90 {lab=VDD}
N 2625 100 2625 90 {lab=VDD}
N 3165 90 3165 986 {lab=VDD}
N 3165 986 2715 986 {lab=VDD}
N 2715 986 2410 986 {lab=VDD}
N 2410 986 2310 986 {lab=VDD}
N 2310 986 2310 751 {lab=VDD}
N 2310 751 1980 751 {lab=VDD}
N 1980 840 2045 840 {lab=VDD}
N 2045 840 2045 751 {lab=VDD}
N 1470 986 1470 735 {lab=VDD}
N 1470 735 2310 735 {lab=VDD}
N 2310 735 2310 751 {lab=VDD}
N 1470 1055 1435 1055 {lab=VDD}
N 1435 1055 1435 986 {lab=VDD}
N 1435 986 1470 986 {lab=VDD}
N 1870 1055 1905 1055 {lab=VDD}
N 1905 1055 1905 992 {lab=VDD}
N 1905 992 2180 992 {lab=VDD}
N 2180 992 2180 735 {lab=VDD}
N 2120 1055 2085 1055 {lab=VDD}
N 2085 1055 2085 992 {lab=VDD}
N 2410 1055 2375 1055 {lab=VDD}
N 2375 1055 2375 986 {lab=VDD}
N 2715 1055 2750 1055 {lab=VDD}
N 2750 1055 2750 986 {lab=VDD}
N 260 1338 50 1338 {lab=VDD}
N 50 1338 50 90 {lab=VDD}
N 35 1755 3080 1755 {lab=VSS}
N 3080 1755 3080 336 {lab=VSS}
N 3080 336 2625 336 {lab=VSS}
N 2625 336 2110 336 {lab=VSS}
N 2110 336 1510 336 {lab=VSS}
N 1510 176 1640 176 {lab=VSS}
N 1640 176 1640 336 {lab=VSS}
N 1510 288 1640 288 {lab=VSS}
N 2110 176 2155 176 {lab=VSS}
N 2155 176 2155 336 {lab=VSS}
N 2110 288 2155 288 {lab=VSS}
N 2625 176 2670 176 {lab=VSS}
N 2670 176 2670 336 {lab=VSS}
N 2625 288 2670 288 {lab=VSS}
N 160 1060 65 1060 {lab=VSS}
N 65 1060 65 1755 {lab=VSS}
N 160 1030 135 1030 {lab=VSS}
N 135 1030 135 1060 {lab=VSS}
N 475 1030 505 1030 {lab=VSS}
N 505 1030 505 1060 {lab=VSS}
N 505 1060 475 1060 {lab=VSS}
N 285 725 230 725 {lab=VSS}
N 230 725 230 850 {lab=VSS}
N 230 850 345 850 {lab=VSS}
N 345 850 345 1060 {lab=VSS}
N 285 895 345 895 {lab=VSS}
N 665 725 720 725 {lab=VSS}
N 720 725 720 850 {lab=VSS}
N 720 850 605 850 {lab=VSS}
N 605 850 605 1060 {lab=VSS}
N 605 1060 505 1060 {lab=VSS}
N 665 895 605 895 {lab=VSS}
N 2715 1602 2715 1755 {lab=VSS}
N 1470 1460 1515 1460 {lab=VSS}
N 1515 1460 1515 1602 {lab=VSS}
N 1515 1602 1470 1602 {lab=VSS}
N 1870 1460 1915 1460 {lab=VSS}
N 1915 1460 1915 1602 {lab=VSS}
N 1915 1602 1870 1602 {lab=VSS}
N 2120 1460 2165 1460 {lab=VSS}
N 2165 1460 2165 1602 {lab=VSS}
N 2165 1602 2120 1602 {lab=VSS}
N 2410 1460 2455 1460 {lab=VSS}
N 2455 1460 2455 1602 {lab=VSS}
N 2455 1602 2410 1602 {lab=VSS}
N 2715 1460 2815 1460 {lab=VSS}
N 2815 1460 2815 1602 {lab=VSS}
N 2815 1602 2715 1602 {lab=VSS}
N 770 525 865 525 {lab=OUTP}
N 865 525 865 176 {lab=OUTP}
N 865 176 1435 176 {lab=OUTP}
N 585 1338 585 1228 {lab=OUTP}
N 585 1228 865 1228 {lab=OUTP}
N 865 1228 865 525 {lab=OUTP}
N 180 525 120 525 {lab=OUTM}
N 120 525 120 361 {lab=OUTM}
N 120 361 975 361 {lab=OUTM}
N 975 361 975 211 {lab=OUTM}
N 975 211 2005 211 {lab=OUTM}
N 2005 211 2005 176 {lab=OUTM}
N 860 1338 960 1338 {lab=OUTM}
N 960 1338 960 361 {lab=OUTM}
N 218 1030 218 1090 {lab=IREF}
N 218 1090 1070 1090 {lab=IREF}
N 1070 1090 1070 288 {lab=IREF}
N 1070 288 1435 288 {lab=IREF}
N 1435 288 1435 300 {lab=IREF}
N 1435 300 2550 300 {lab=IREF}
N 2550 300 2550 288 {lab=IREF}
N 2005 288 2005 300 {lab=IREF}
N 1070 1090 1070 1460 {lab=IREF}
N 1070 1460 1345 1460 {lab=IREF}
N 1735 234 1735 431 {lab=SP}
N 1735 431 1745 431 {lab=SP}
N 2200 234 2420 234 {lab=SM}
N 2420 234 2420 431 {lab=SM}
N 2715 234 2855 234 {lab=SR}
N 2855 234 2855 893 {lab=SR}
N 2855 893 2195 893 {lab=SR}
N 2195 893 2195 1055 {lab=SR}
N 2090 431 2090 615 {lab=SENSE}
N 2090 615 1824 615 {lab=SENSE}
N 1824 615 1824 1055 {lab=SENSE}
N 1535 1303 1640 1303 {lab=CB}
N 1640 1303 1640 840 {lab=CB}
N 1640 840 1905 840 {lab=CB}
N 1935 1303 1960 1303 {lab=CA}
N 1960 1303 1960 1575 {lab=CA}
N 1960 1575 2640 1575 {lab=CA}
N 2640 1575 2640 1460 {lab=CA}
N 2185 1303 2295 1303 {lab=RCM}
N 2295 1303 2295 1460 {lab=RCM}
N 2295 1460 2335 1460 {lab=RCM}
N 2475 1303 2600 1303 {lab=PBIAS}
N 2600 1303 2600 1055 {lab=PBIAS}
N 2600 1055 2640 1055 {lab=PBIAS}
N 2835 1303 2960 1303 {lab=PC}
N 2960 1303 2960 1680 {lab=PC}
N 2960 1680 855 1680 {lab=PC}
N 855 1680 855 1605 {lab=PC}
N 475 200 475 248 {lab=PC}
N 475 248 795 248 {lab=PC}
N 795 248 795 1605 {lab=PC}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 285 260 0 1 {name=PROBE0 lab=PX1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 665 260 0 0 {name=PROBE1 lab=PX2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 285 835 0 1 {name=PROBE2 lab=NX1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 665 835 0 0 {name=PROBE3 lab=NX2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 475 985 0 0 {name=PROBE4 lab=TAIL}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 855 1605 0 0 {name=PROBE5 lab=PC}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1735 234 0 0 {name=PROBE6 lab=SP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2200 234 0 0 {name=PROBE7 lab=SM}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2715 234 0 0 {name=PROBE8 lab=SR}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2090 431 0 0 {name=PROBE9 lab=SENSE}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1535 1303 0 0 {name=PROBE10 lab=CB}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1980 915 0 0 {name=PROBE11 lab=CT}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1935 1303 0 0 {name=PROBE12 lab=CA}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2185 1303 0 0 {name=PROBE13 lab=RCM}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2475 1303 0 0 {name=PROBE14 lab=PBIAS}
T {Crossings without a junction dot are separate wires.} 0 1925 0 0 0.22 0.22 {}
