v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}

T {SCL08 input common-mode correction} 50 30 0 0 0.61 0.61 {layer=4}
T {Target 2.5 V   |   Sample the input error late in transfer   |   Apply the correction next cycle} 50 80 0 0 0.33 0.33 {layer=4}
C {devices/iopin.sym} 70 132 0 0 {name=PORT1 lab=sump}
C {devices/iopin.sym} 255 132 0 0 {name=PORT2 lab=sumn}
C {devices/iopin.sym} 440 132 0 0 {name=PORT3 lab=ref}
C {devices/iopin.sym} 625 132 0 0 {name=PORT4 lab=phi1}
C {devices/iopin.sym} 810 132 0 0 {name=PORT5 lab=phi1b}
C {devices/iopin.sym} 995 132 0 0 {name=PORT6 lab=phit}
C {devices/iopin.sym} 1180 132 0 0 {name=PORT7 lab=phitb}
C {devices/iopin.sym} 1365 132 0 0 {name=PORT8 lab=phi2}
C {devices/iopin.sym} 70 166 0 0 {name=PORT9 lab=vdd}
C {devices/iopin.sym} 255 166 0 0 {name=PORT10 lab=vss}
C {devices/iopin.sym} 440 166 0 0 {name=PORT11 lab=sample}
C {devices/iopin.sym} 625 166 0 0 {name=PORT12 lab=sampleb}
C {devices/iopin.sym} 810 166 0 0 {name=PORT13 lab=cm_x}
C {devices/iopin.sym} 995 166 0 0 {name=PORT14 lab=cm_hold}
C {devices/iopin.sym} 1180 166 0 0 {name=PORT15 lab=accum}
T {Bias and input error sensing} 50 223 0 0 0.44 0.44 {layer=4}
L 4 50 253 2180 253 {}
C {rpp_icm.sym} 355 378 0 0 {name=XRBIAS w=2.4u l=20000u}
N 240 357 209 357 {}
C {devices/lab_pin.sym} 209 357 0 0 {name=LABCM1 lab=vdd}
N 470 357 501 357 {}
C {devices/lab_pin.sym} 501 357 0 1 {name=LABCM2 lab=nb}
C {devices/nmos4.sym} 920 378 0 0 {name=MBIAS model=N w=20u l=2.4u m=1 extra=""}
N 940 348 940 319 {}
C {devices/lab_pin.sym} 940 319 0 0 {name=LABCM3 lab=nb}
N 940 408 940 443 {}
C {devices/lab_pin.sym} 940 443 0 1 {name=LABCM4 lab=vss}
N 900 378 856 378 {}
C {devices/lab_pin.sym} 856 378 0 0 {name=LABCM5 lab=nb}
N 940 378 993 378 {}
C {devices/lab_pin.sym} 993 378 0 1 {name=LABCM6 lab=vss}
C {icm_error08.sym} 1485 378 0 0 {name=XEP }
N 1370 325 1339 325 {}
C {devices/lab_pin.sym} 1339 325 0 0 {name=LABCM7 lab=sump}
N 1370 356 1339 356 {}
C {devices/lab_pin.sym} 1339 356 0 0 {name=LABCM8 lab=ref}
N 1370 387 1339 387 {}
C {devices/lab_pin.sym} 1339 387 0 0 {name=LABCM9 lab=current}
N 1370 418 1339 418 {}
C {devices/lab_pin.sym} 1339 418 0 0 {name=LABCM10 lab=sample}
N 1600 325 1631 325 {}
C {devices/lab_pin.sym} 1631 325 0 1 {name=LABCM11 lab=vdd}
N 1600 356 1631 356 {}
C {devices/lab_pin.sym} 1631 356 0 1 {name=LABCM12 lab=vss}
N 1600 387 1631 387 {}
C {devices/lab_pin.sym} 1631 387 0 1 {name=LABCM13 lab=nb}
C {icm_error08.sym} 2050 378 0 0 {name=XEN }
N 1935 325 1904 325 {}
C {devices/lab_pin.sym} 1904 325 0 0 {name=LABCM14 lab=sumn}
N 1935 356 1904 356 {}
C {devices/lab_pin.sym} 1904 356 0 0 {name=LABCM15 lab=ref}
N 1935 387 1904 387 {}
C {devices/lab_pin.sym} 1904 387 0 0 {name=LABCM16 lab=current}
N 1935 418 1904 418 {}
C {devices/lab_pin.sym} 1904 418 0 0 {name=LABCM17 lab=sample}
N 2165 325 2196 325 {}
C {devices/lab_pin.sym} 2196 325 0 1 {name=LABCM18 lab=vdd}
N 2165 356 2196 356 {}
C {devices/lab_pin.sym} 2196 356 0 1 {name=LABCM19 lab=vss}
N 2165 387 2196 387 {}
C {devices/lab_pin.sym} 2196 387 0 1 {name=LABCM20 lab=nb}
C {icm_tg08.sym} 355 608 0 0 {name=XUP }
N 240 571 209 571 {}
C {devices/lab_pin.sym} 209 571 0 0 {name=LABCM21 lab=current}
N 240 602 209 602 {}
C {devices/lab_pin.sym} 209 602 0 0 {name=LABCM22 lab=accum}
N 240 633 209 633 {}
C {devices/lab_pin.sym} 209 633 0 0 {name=LABCM23 lab=sample}
N 470 571 501 571 {}
C {devices/lab_pin.sym} 501 571 0 1 {name=LABCM24 lab=sampleb}
N 470 602 501 602 {}
C {devices/lab_pin.sym} 501 602 0 1 {name=LABCM25 lab=vdd}
N 470 633 501 633 {}
C {devices/lab_pin.sym} 501 633 0 1 {name=LABCM26 lab=vss}
C {icm_tg08.sym} 920 608 0 0 {name=XPRE }
N 805 571 774 571 {}
C {devices/lab_pin.sym} 774 571 0 0 {name=LABCM27 lab=drive}
N 805 602 774 602 {}
C {devices/lab_pin.sym} 774 602 0 0 {name=LABCM28 lab=current}
N 805 633 774 633 {}
C {devices/lab_pin.sym} 774 633 0 0 {name=LABCM29 lab=sampleb}
N 1035 571 1066 571 {}
C {devices/lab_pin.sym} 1066 571 0 1 {name=LABCM30 lab=sample}
N 1035 602 1066 602 {}
C {devices/lab_pin.sym} 1066 602 0 1 {name=LABCM31 lab=vdd}
N 1035 633 1066 633 {}
C {devices/lab_pin.sym} 1066 633 0 1 {name=LABCM32 lab=vss}
T {Integrator, hold and buffer} 50 757 0 0 0.44 0.44 {layer=4}
L 4 50 787 2180 787 {}
C {devices/pmos4.sym} 355 912 0 0 {name=MCINT model=P w=100u l=20u m=9 extra=""}
N 375 882 375 853 {}
C {devices/lab_pin.sym} 375 853 0 0 {name=LABCM33 lab=vdd}
N 375 942 375 977 {}
C {devices/lab_pin.sym} 375 977 0 1 {name=LABCM34 lab=vdd}
N 335 912 291 912 {}
C {devices/lab_pin.sym} 291 912 0 0 {name=LABCM35 lab=accum}
N 375 912 428 912 {}
C {devices/lab_pin.sym} 428 912 0 1 {name=LABCM36 lab=vdd}
C {devices/pmos4.sym} 920 912 0 0 {name=MCH model=P w=100u l=20u m=1 extra=""}
N 940 882 940 853 {}
C {devices/lab_pin.sym} 940 853 0 0 {name=LABCM37 lab=vdd}
N 940 942 940 977 {}
C {devices/lab_pin.sym} 940 977 0 1 {name=LABCM38 lab=vdd}
N 900 912 856 912 {}
C {devices/lab_pin.sym} 856 912 0 0 {name=LABCM39 lab=cm_hold}
N 940 912 993 912 {}
C {devices/lab_pin.sym} 993 912 0 1 {name=LABCM40 lab=vdd}
C {devices/nmos4.sym} 1485 912 0 0 {name=MLOW model=N w=2.5u l=4u m=1 extra=""}
N 1505 882 1505 853 {}
C {devices/lab_pin.sym} 1505 853 0 0 {name=LABCM41 lab=ref}
N 1505 942 1505 977 {}
C {devices/lab_pin.sym} 1505 977 0 1 {name=LABCM42 lab=accum}
N 1465 912 1421 912 {}
C {devices/lab_pin.sym} 1421 912 0 0 {name=LABCM43 lab=ref}
N 1505 912 1558 912 {}
C {devices/lab_pin.sym} 1558 912 0 1 {name=LABCM44 lab=vss}
C {devices/pmos4.sym} 2050 912 0 0 {name=MHIGH model=P w=2.5u l=4u m=1 extra=""}
N 2070 882 2070 853 {}
C {devices/lab_pin.sym} 2070 853 0 0 {name=LABCM45 lab=ref}
N 2070 942 2070 977 {}
C {devices/lab_pin.sym} 2070 977 0 1 {name=LABCM46 lab=accum}
N 2030 912 1986 912 {}
C {devices/lab_pin.sym} 1986 912 0 0 {name=LABCM47 lab=ref}
N 2070 912 2123 912 {}
C {devices/lab_pin.sym} 2123 912 0 1 {name=LABCM48 lab=vdd}
C {icm_tg08.sym} 355 1142 0 0 {name=XLATCH }
N 240 1105 209 1105 {}
C {devices/lab_pin.sym} 209 1105 0 0 {name=LABCM49 lab=accum}
N 240 1136 209 1136 {}
C {devices/lab_pin.sym} 209 1136 0 0 {name=LABCM50 lab=cm_hold}
N 240 1167 209 1167 {}
C {devices/lab_pin.sym} 209 1167 0 0 {name=LABCM51 lab=phi1}
N 470 1105 501 1105 {}
C {devices/lab_pin.sym} 501 1105 0 1 {name=LABCM52 lab=phi1b}
N 470 1136 501 1136 {}
C {devices/lab_pin.sym} 501 1136 0 1 {name=LABCM53 lab=vdd}
N 470 1167 501 1167 {}
C {devices/lab_pin.sym} 501 1167 0 1 {name=LABCM54 lab=vss}
C {icm_buffer08.sym} 920 1142 0 0 {name=XBUF }
N 805 1105 774 1105 {}
C {devices/lab_pin.sym} 774 1105 0 0 {name=LABCM55 lab=cm_hold}
N 805 1136 774 1136 {}
C {devices/lab_pin.sym} 774 1136 0 0 {name=LABCM56 lab=drive}
N 805 1167 774 1167 {}
C {devices/lab_pin.sym} 774 1167 0 0 {name=LABCM57 lab=vdd}
N 1035 1105 1066 1105 {}
C {devices/lab_pin.sym} 1066 1105 0 1 {name=LABCM58 lab=vss}
N 1035 1136 1066 1136 {}
C {devices/lab_pin.sym} 1066 1136 0 1 {name=LABCM59 lab=nb}
T {Two-phase correction drive} 50 1291 0 0 0.44 0.44 {layer=4}
L 4 50 1321 2180 1321 {}
C {inv08.sym} 355 1446 0 0 {name=XTXB w=3u}
N 240 1425 209 1425 {}
C {devices/lab_pin.sym} 209 1425 0 0 {name=LABCM60 lab=phi2}
N 240 1456 209 1456 {}
C {devices/lab_pin.sym} 209 1456 0 0 {name=LABCM61 lab=tx_b}
N 470 1425 501 1425 {}
C {devices/lab_pin.sym} 501 1425 0 1 {name=LABCM62 lab=vdd}
N 470 1456 501 1456 {}
C {devices/lab_pin.sym} 501 1456 0 1 {name=LABCM63 lab=vss}
C {inv08.sym} 920 1446 0 0 {name=XTXA w=12u}
N 805 1425 774 1425 {}
C {devices/lab_pin.sym} 774 1425 0 0 {name=LABCM64 lab=tx_b}
N 805 1456 774 1456 {}
C {devices/lab_pin.sym} 774 1456 0 0 {name=LABCM65 lab=tx_a}
N 1035 1425 1066 1425 {}
C {devices/lab_pin.sym} 1066 1425 0 1 {name=LABCM66 lab=vdd}
N 1035 1456 1066 1456 {}
C {devices/lab_pin.sym} 1066 1456 0 1 {name=LABCM67 lab=vss}
C {icm_drive_tg08.sym} 1485 1446 0 0 {name=XRXHI }
N 1370 1409 1339 1409 {}
C {devices/lab_pin.sym} 1339 1409 0 0 {name=LABCM68 lab=drive}
N 1370 1440 1339 1440 {}
C {devices/lab_pin.sym} 1339 1440 0 0 {name=LABCM69 lab=edge_r}
N 1370 1471 1339 1471 {}
C {devices/lab_pin.sym} 1339 1471 0 0 {name=LABCM70 lab=phit}
N 1600 1409 1631 1409 {}
C {devices/lab_pin.sym} 1631 1409 0 1 {name=LABCM71 lab=phitb}
N 1600 1440 1631 1440 {}
C {devices/lab_pin.sym} 1631 1440 0 1 {name=LABCM72 lab=vdd}
N 1600 1471 1631 1471 {}
C {devices/lab_pin.sym} 1631 1471 0 1 {name=LABCM73 lab=vss}
C {icm_drive_tg08.sym} 2050 1446 0 0 {name=XRXLO }
N 1935 1409 1904 1409 {}
C {devices/lab_pin.sym} 1904 1409 0 0 {name=LABCM74 lab=vss}
N 1935 1440 1904 1440 {}
C {devices/lab_pin.sym} 1904 1440 0 0 {name=LABCM75 lab=edge_r}
N 1935 1471 1904 1471 {}
C {devices/lab_pin.sym} 1904 1471 0 0 {name=LABCM76 lab=phitb}
N 2165 1409 2196 1409 {}
C {devices/lab_pin.sym} 2196 1409 0 1 {name=LABCM77 lab=phit}
N 2165 1440 2196 1440 {}
C {devices/lab_pin.sym} 2196 1440 0 1 {name=LABCM78 lab=vdd}
N 2165 1471 2196 1471 {}
C {devices/lab_pin.sym} 2196 1471 0 1 {name=LABCM79 lab=vss}
C {icm_drive_tg08.sym} 355 1676 0 0 {name=XTXHI }
N 240 1639 209 1639 {}
C {devices/lab_pin.sym} 209 1639 0 0 {name=LABCM80 lab=drive}
N 240 1670 209 1670 {}
C {devices/lab_pin.sym} 209 1670 0 0 {name=LABCM81 lab=edge_t}
N 240 1701 209 1701 {}
C {devices/lab_pin.sym} 209 1701 0 0 {name=LABCM82 lab=tx_a}
N 470 1639 501 1639 {}
C {devices/lab_pin.sym} 501 1639 0 1 {name=LABCM83 lab=tx_b}
N 470 1670 501 1670 {}
C {devices/lab_pin.sym} 501 1670 0 1 {name=LABCM84 lab=vdd}
N 470 1701 501 1701 {}
C {devices/lab_pin.sym} 501 1701 0 1 {name=LABCM85 lab=vss}
C {icm_drive_tg08.sym} 920 1676 0 0 {name=XTXLO }
N 805 1639 774 1639 {}
C {devices/lab_pin.sym} 774 1639 0 0 {name=LABCM86 lab=vss}
N 805 1670 774 1670 {}
C {devices/lab_pin.sym} 774 1670 0 0 {name=LABCM87 lab=edge_t}
N 805 1701 774 1701 {}
C {devices/lab_pin.sym} 774 1701 0 0 {name=LABCM88 lab=tx_b}
N 1035 1639 1066 1639 {}
C {devices/lab_pin.sym} 1066 1639 0 1 {name=LABCM89 lab=tx_a}
N 1035 1670 1066 1670 {}
C {devices/lab_pin.sym} 1066 1670 0 1 {name=LABCM90 lab=vdd}
N 1035 1701 1066 1701 {}
C {devices/lab_pin.sym} 1066 1701 0 1 {name=LABCM91 lab=vss}
C {rpp_icm.sym} 1485 1676 0 0 {name=XR1 w=2.4u l=350u}
N 1370 1655 1339 1655 {}
C {devices/lab_pin.sym} 1339 1655 0 0 {name=LABCM92 lab=edge_r}
N 1600 1655 1631 1655 {}
C {devices/lab_pin.sym} 1631 1655 0 1 {name=LABCM93 lab=cm_x}
C {rpp_icm.sym} 2050 1676 0 0 {name=XR2 w=2.4u l=744u}
N 1935 1655 1904 1655 {}
C {devices/lab_pin.sym} 1904 1655 0 0 {name=LABCM94 lab=edge_t}
N 2165 1655 2196 1655 {}
C {devices/lab_pin.sym} 2196 1655 0 1 {name=LABCM95 lab=cm_x}
T {Matched correction MOS capacitor banks} 50 1825 0 0 0.44 0.44 {layer=4}
L 4 50 1855 2180 1855 {}
C {devices/pmos4.sym} 355 1980 0 0 {name=MCORRP model=P w=20u l=10u m=40 extra="ad=90p as=90p pd=49u ps=49u"}
N 375 1950 375 1921 {}
C {devices/lab_pin.sym} 375 1921 0 0 {name=LABCM96 lab=sump}
N 375 2010 375 2045 {}
C {devices/lab_pin.sym} 375 2045 0 1 {name=LABCM97 lab=sump}
N 335 1980 291 1980 {}
C {devices/lab_pin.sym} 291 1980 0 0 {name=LABCM98 lab=cm_x}
N 375 1980 428 1980 {}
C {devices/lab_pin.sym} 428 1980 0 1 {name=LABCM99 lab=sump}
C {devices/pmos4.sym} 920 1980 0 0 {name=MCORRN model=P w=20u l=10u m=40 extra="ad=90p as=90p pd=49u ps=49u"}
N 940 1950 940 1921 {}
C {devices/lab_pin.sym} 940 1921 0 0 {name=LABCM100 lab=sumn}
N 940 2010 940 2045 {}
C {devices/lab_pin.sym} 940 2045 0 1 {name=LABCM101 lab=sumn}
N 900 1980 856 1980 {}
C {devices/lab_pin.sym} 856 1980 0 0 {name=LABCM102 lab=cm_x}
N 940 1980 993 1980 {}
C {devices/lab_pin.sym} 993 1980 0 1 {name=LABCM103 lab=sumn}
