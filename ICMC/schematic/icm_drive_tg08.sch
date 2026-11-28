v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}

T {SCL08 CMOS driver transmission gate} 50 30 0 0 0.61 0.61 {layer=4}
C {devices/iopin.sym} 70 132 0 0 {name=PORT1 lab=a}
C {devices/iopin.sym} 255 132 0 0 {name=PORT2 lab=b}
C {devices/iopin.sym} 440 132 0 0 {name=PORT3 lab=en}
C {devices/iopin.sym} 625 132 0 0 {name=PORT4 lab=enb}
C {devices/iopin.sym} 810 132 0 0 {name=PORT5 lab=vdd}
C {devices/iopin.sym} 995 132 0 0 {name=PORT6 lab=vss}
C {devices/nmos4.sym} 355 378 0 0 {name=MN model=N w=12u l=.8u m=1 extra="ad=54p as=54p pd=33u ps=33u"}
N 375 348 375 319 {}
C {devices/lab_pin.sym} 375 319 0 0 {name=LABCM1 lab=a}
N 375 408 375 443 {}
C {devices/lab_pin.sym} 375 443 0 1 {name=LABCM2 lab=b}
N 335 378 291 378 {}
C {devices/lab_pin.sym} 291 378 0 0 {name=LABCM3 lab=en}
N 375 378 428 378 {}
C {devices/lab_pin.sym} 428 378 0 1 {name=LABCM4 lab=vss}
C {devices/pmos4.sym} 920 378 0 0 {name=MP model=P w=24u l=.8u m=1 extra="ad=108p as=108p pd=57u ps=57u"}
N 940 348 940 319 {}
C {devices/lab_pin.sym} 940 319 0 0 {name=LABCM5 lab=b}
N 940 408 940 443 {}
C {devices/lab_pin.sym} 940 443 0 1 {name=LABCM6 lab=a}
N 900 378 856 378 {}
C {devices/lab_pin.sym} 856 378 0 0 {name=LABCM7 lab=enb}
N 940 378 993 378 {}
C {devices/lab_pin.sym} 993 378 0 1 {name=LABCM8 lab=vdd}
