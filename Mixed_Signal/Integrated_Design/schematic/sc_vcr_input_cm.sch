v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Differential SC readout with VCR OTA and input CM correction} 40 42 0 0 0.78 0.78 {layer=4}
T {Typical test point  |  CP = 11.79 pF, CN = 10 pF  |  10 kHz clock  |  87 us track tap} 40 86 0 0 0.43 0.43 {layer=4}
T {MEMS SENSOR} 55 145 0 0 0.37 0.37 {layer=4}
T {CHARGE TRANSFER} 360 145 0 0 0.37 0.37 {layer=4}
T {OTA AND FEEDBACK} 790 145 0 0 0.37 0.37 {layer=4}
T {ANALOG OUTPUT} 1140 145 0 0 0.37 0.37 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/ota_vcr_final.sym} 895 500 0 0 {name=XOTA}
N 780 482 745 482 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 745 482 0 0 {name=L1 lab=vref}
N 780 518 745 518 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 745 518 0 0 {name=L2 lab=vbn}
N 780 552 745 552 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 745 552 0 0 {name=L3 lab=vbp}
N 1010 448 1045 448 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/net_right.sym} 1045 448 0 0 {name=L4 lab=ota_vdd caption=ota_vdd}
N 1010 482 1045 482 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/net_right.sym} 1045 482 0 0 {name=L5 lab=0 caption=0}
N 1010 518 1045 518 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/net_right.sym} 1045 518 0 0 {name=L6 lab=bias caption=bias}
N 80 350 80 500 {}
N 80 500 80 650 {}
N 80 500 125 500 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 125 500 0 0 {name=G7 lab=0}
T {Shared MEMS} 95 450 0 0 0.31 0.31 {layer=4}
T {electrode} 95 470 0 0 0.31 0.31 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 149 350 0 0 {name=CMEMP value=11.79p}
T {CP = 11.79 pF} 108 303 0 0 0.37 0.37 {layer=8}
N 80 350 109 350 {}
N 189 350 235 350 {}
N 235 350 280 350 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_h.sym} 320 350 0 0 {name=XSENSEP phi=phi2 phib=phi2b}
T {phi2} 303 306 0 0 0.32 0.32 {layer=4}
N 360 350 430 350 {}
N 235 350 235 390 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_v.sym} 235 430 0 0 {name=XSRESETP phi=phi1 phib=phi1b}
N 235 470 235 478 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 235 478 0 0 {name=G8 lab=0}
T {phi1 sensor reset} 270 416 0 0 0.31 0.31 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 235 350 0 0 {name=L9 lab=sensp}
N 430 350 430 310 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_v.sym} 430 270 0 0 {name=XCHARGEP phi=phi1 phib=phi1b}
N 430 230 430 205 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 205 0 0 {name=L10 lab=vp}
T {phi1} 464 259 0 0 0.31 0.31 {layer=4}
N 430 350 462 350 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 502 350 0 0 {name=CSP value=10p}
T {CS = 10 pF} 460 303 0 0 0.35 0.35 {layer=4}
N 542 350 610 350 {}
N 610 350 627 350 {}
N 610 350 610 382 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_v.sym} 610 422 0 0 {name=XRRESETP phi=phi1 phib=phi1b}
N 610 462 610 470 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 610 470 0 0 {name=G11 lab=0}
T {phi1} 647 410 0 0 0.32 0.32 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_h.sym} 667 350 0 0 {name=XXFERP phi=phit phib=phitb}
T {phi2r} 645 306 0 0 0.32 0.32 {layer=4}
N 707 350 740 350 {}
N 740 350 780 350 {}
N 1010 350 1060 350 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 350 0 0 {name=L12 lab=txp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 350 0 0 {name=L13 lab=rxp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 350 0 0 {name=L14 lab=sump}
N 740 350 740 267 {}
N 740 267 740 218 {}
N 1060 350 1060 267 {}
N 1060 267 1060 218 {}
N 740 267 855 267 {}
N 935 267 1060 267 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/pmos_cfb.sym} 895 267 0 0 {name=XCFP}
T {CFB  PMOS bank} 831 290 0 0 0.31 0.31 {layer=8}
N 740 218 855 218 {}
N 935 218 1060 218 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_h.sym} 895 218 0 0 {name=XFBRESETP phi=phi1 phib=phi1b}
T {RST (phi1)} 859 168 0 0 0.31 0.31 {layer=4}
N 1060 350 1155 350 {}
N 1155 350 1292 350 {}
N 1155 350 1155 380 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_v.sym} 1155 420 0 0 {name=CLP value=5p}
N 1155 460 1155 467 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1155 467 0 0 {name=G15 lab=0}
T {CL = 5 pF} 1176 411 0 0 0.35 0.35 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/net_right.sym} 1292 350 0 0 {name=L16 lab=outp caption=VOUTP}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 149 650 0 0 {name=CMEMN value=10p}
T {CN = 10 pF} 108 603 0 0 0.37 0.37 {layer=8}
N 80 650 109 650 {}
N 189 650 235 650 {}
N 235 650 280 650 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_h.sym} 320 650 0 0 {name=XSENSEN phi=phi2 phib=phi2b}
T {phi2} 303 606 0 0 0.32 0.32 {layer=4}
N 360 650 430 650 {}
N 235 650 235 610 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_v.sym} 235 570 0 0 {name=XSRESETN phi=phi1 phib=phi1b}
N 235 530 235 522 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 235 522 2 0 {name=G17 lab=0}
T {phi1 sensor reset} 270 564 0 0 0.31 0.31 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 235 650 0 0 {name=L18 lab=sensn}
N 430 650 430 690 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_v.sym} 430 730 0 0 {name=XCHARGEN phi=phi1 phib=phi1b}
N 430 770 430 795 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 795 0 0 {name=L19 lab=vp}
T {phi1} 464 723 0 0 0.31 0.31 {layer=4}
N 430 650 462 650 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 502 650 0 0 {name=CSN value=10p}
T {CS = 10 pF} 460 603 0 0 0.35 0.35 {layer=4}
N 542 650 610 650 {}
N 610 650 627 650 {}
N 610 650 610 618 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_v.sym} 610 578 0 0 {name=XRRESETN phi=phi1 phib=phi1b}
N 610 538 610 530 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 610 530 2 0 {name=G20 lab=0}
T {phi1} 647 572 0 0 0.32 0.32 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_h.sym} 667 650 0 0 {name=XXFERN phi=phit phib=phitb}
T {phi2r} 645 606 0 0 0.32 0.32 {layer=4}
N 707 650 740 650 {}
N 740 650 780 650 {}
N 1010 650 1060 650 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 650 0 0 {name=L21 lab=txn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 650 0 0 {name=L22 lab=rxn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 650 0 0 {name=L23 lab=sumn}
N 740 650 740 733 {}
N 740 733 740 782 {}
N 1060 650 1060 733 {}
N 1060 733 1060 782 {}
N 740 733 855 733 {}
N 935 733 1060 733 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/pmos_cfb.sym} 895 733 0 0 {name=XCFN}
T {CFB  PMOS bank} 831 694 0 0 0.31 0.31 {layer=8}
N 740 782 855 782 {}
N 935 782 1060 782 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/tg_h.sym} 895 782 0 0 {name=XFBRESETN phi=phi1 phib=phi1b}
T {RST (phi1)} 859 810 0 0 0.31 0.31 {layer=4}
N 1060 650 1155 650 {}
N 1155 650 1292 650 {}
N 1155 650 1155 620 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_v.sym} 1155 580 0 0 {name=CLN value=5p}
N 1155 540 1155 533 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1155 533 2 0 {name=G24 lab=0}
T {CL = 5 pF} 1176 571 0 0 0.35 0.35 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/net_right.sym} 1292 650 0 0 {name=L25 lab=outn caption=VOUTN}
T {Vdiff = VOUTP - VOUTN} 1120 494 0 0 0.31 0.31 {layer=4}
T {VP = 5 V     VCM target = 2.5 V} 42 838 0 0 0.33 0.33 {layer=4}
T {phi1 also resets CFB and the RX nodes. The sensor electrodes reset through SCL08 transmission gates.} 42 872 0 0 0.3 0.3 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/bench_setup.sym} 1137 855 0 0 {name=BENCH value=".include /home/shreyas/Desktop/Sec_7/Integrated_Design/simulation/original_support.spice"}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/ota_input_cm_servo.sym} 430 503 0 0 {name=XICM}
N 525 479 547 479 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 547 479 0 1 {name=L30 lab=sump}
N 525 525 547 525 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 547 525 0 1 {name=L31 lab=sumn}
N 335 461 292 461 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 292 461 0 0 {name=L32 lab=vdd}
N 335 490 292 490 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 292 490 0 0 {name=L33 lab=phi1}
N 335 518 292 518 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 292 518 0 0 {name=L34 lab=phi2}
N 335 547 292 547 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 292 547 0 0 {name=L35 lab=phit}
T {CFB: 60 PMOS units per branch} 760 850 0 0 0.29 0.29 {layer=8}
