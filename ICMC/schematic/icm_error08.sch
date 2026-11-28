v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}

T {Sample-enabled input error transconductor} 50 30 0 0 0.61 0.61 {layer=4}
C {devices/iopin.sym} 70 132 0 0 {name=PORT1 lab=inp}
C {devices/iopin.sym} 255 132 0 0 {name=PORT2 lab=ref}
C {devices/iopin.sym} 440 132 0 0 {name=PORT3 lab=drive}
C {devices/iopin.sym} 625 132 0 0 {name=PORT4 lab=sample}
C {devices/iopin.sym} 810 132 0 0 {name=PORT5 lab=vdd}
C {devices/iopin.sym} 995 132 0 0 {name=PORT6 lab=vss}
C {devices/iopin.sym} 1180 132 0 0 {name=PORT7 lab=nb}
C {devices/nmos4.sym} 355 378 0 0 {name=MREF model=N w=12u l=2.4u m=1 extra=""}
N 375 348 375 319 {}
C {devices/lab_pin.sym} 375 319 0 0 {name=LABCM1 lab=mirror}
N 375 408 375 443 {}
C {devices/lab_pin.sym} 375 443 0 1 {name=LABCM2 lab=tail}
N 335 378 291 378 {}
C {devices/lab_pin.sym} 291 378 0 0 {name=LABCM3 lab=ref}
N 375 378 428 378 {}
C {devices/lab_pin.sym} 428 378 0 1 {name=LABCM4 lab=vss}
C {devices/nmos4.sym} 920 378 0 0 {name=MSIG model=N w=12u l=2.4u m=1 extra=""}
N 940 348 940 319 {}
C {devices/lab_pin.sym} 940 319 0 0 {name=LABCM5 lab=drive}
N 940 408 940 443 {}
C {devices/lab_pin.sym} 940 443 0 1 {name=LABCM6 lab=tail}
N 900 378 856 378 {}
C {devices/lab_pin.sym} 856 378 0 0 {name=LABCM7 lab=inp}
N 940 378 993 378 {}
C {devices/lab_pin.sym} 993 378 0 1 {name=LABCM8 lab=vss}
C {devices/nmos4.sym} 1485 378 0 0 {name=MEN model=N w=8u l=.8u m=1 extra=""}
N 1505 348 1505 319 {}
C {devices/lab_pin.sym} 1505 319 0 0 {name=LABCM9 lab=tail}
N 1505 408 1505 443 {}
C {devices/lab_pin.sym} 1505 443 0 1 {name=LABCM10 lab=sink}
N 1465 378 1421 378 {}
C {devices/lab_pin.sym} 1421 378 0 0 {name=LABCM11 lab=sample}
N 1505 378 1558 378 {}
C {devices/lab_pin.sym} 1558 378 0 1 {name=LABCM12 lab=vss}
C {devices/nmos4.sym} 2050 378 0 0 {name=MT model=N w=6u l=8u m=1 extra=""}
N 2070 348 2070 319 {}
C {devices/lab_pin.sym} 2070 319 0 0 {name=LABCM13 lab=sink}
N 2070 408 2070 443 {}
C {devices/lab_pin.sym} 2070 443 0 1 {name=LABCM14 lab=vss}
N 2030 378 1986 378 {}
C {devices/lab_pin.sym} 1986 378 0 0 {name=LABCM15 lab=nb}
N 2070 378 2123 378 {}
C {devices/lab_pin.sym} 2123 378 0 1 {name=LABCM16 lab=vss}
C {devices/pmos4.sym} 355 608 0 0 {name=MP0 model=P w=12u l=4u m=1 extra=""}
N 375 578 375 549 {}
C {devices/lab_pin.sym} 375 549 0 0 {name=LABCM17 lab=vdd}
N 375 638 375 673 {}
C {devices/lab_pin.sym} 375 673 0 1 {name=LABCM18 lab=mirror}
N 335 608 291 608 {}
C {devices/lab_pin.sym} 291 608 0 0 {name=LABCM19 lab=mirror}
N 375 608 428 608 {}
C {devices/lab_pin.sym} 428 608 0 1 {name=LABCM20 lab=vdd}
C {devices/pmos4.sym} 920 608 0 0 {name=MP1 model=P w=12u l=4u m=1 extra=""}
N 940 578 940 549 {}
C {devices/lab_pin.sym} 940 549 0 0 {name=LABCM21 lab=vdd}
N 940 638 940 673 {}
C {devices/lab_pin.sym} 940 673 0 1 {name=LABCM22 lab=drive}
N 900 608 856 608 {}
C {devices/lab_pin.sym} 856 608 0 0 {name=LABCM23 lab=mirror}
N 940 608 993 608 {}
C {devices/lab_pin.sym} 993 608 0 1 {name=LABCM24 lab=vdd}
