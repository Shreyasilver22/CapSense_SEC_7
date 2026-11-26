v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {OTA input common-mode correction} 25 10 0 0 0.72 0.72 {layer=4}
T {SCL08 switched-capacitor readout  |  10 kHz  |  Target input common-mode: 2.5 V} 25 65 0 0 0.34 0.34 {layer=8}
L 7 20 118 750 118 {}
L 7 750 118 750 470 {}
L 7 750 470 20 470 {}
L 7 20 470 20 118 {}
L 7 778 118 1510 118 {}
L 7 1510 118 1510 470 {}
L 7 1510 470 778 470 {}
L 7 778 470 778 118 {}
L 7 20 500 750 500 {}
L 7 750 500 750 930 {}
L 7 750 930 20 930 {}
L 7 20 930 20 500 {}
L 7 778 500 1510 500 {}
L 7 1510 500 1510 930 {}
L 7 1510 930 778 930 {}
L 7 778 930 778 500 {}
T {1   Sample and integrate the common-mode error} 42 137 0 0 0.43 0.43 {layer=4}
T {sump and sumn are sensed through the behavioral source.} 42 180 0 0 0.28 0.28 {layer=8}
T {I = 1 mS x cm_sample x [2.5 V - (V(sump) + V(sumn))/2]} 42 210 0 0 0.3 0.3 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_behavior.sym} 100 320 2 0 {name=BICMERR kind=I expr=1m*v(cm_sample)*(2.5-(v(sump)+v(sumn))/2)}
N 100 265 100 290 {}
N 100 350 100 368 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 100 368 0 0 {name=L1 lab=0}
T {BICMERR} 47 405 0 0 0.26 0.26 {layer=4}
N 100 265 235 265 {}
N 235 265 387 265 {}
N 387 265 465 265 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 465 265 0 1 {name=L2 lab=cm_acc}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 235 320 0 0 {name=CICMINT value=1n m=1}
N 235 265 235 290 {}
N 235 350 235 368 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 235 368 0 0 {name=L3 lab=0}
C {/usr/share/xschem/xschem_library/devices/res.sym} 387 320 0 0 {name=RICMINT value=1e13 m=1}
N 387 265 387 290 {}
N 387 350 387 368 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 387 368 0 0 {name=L4 lab=0}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 550 320 0 0 {name=VICMSAMPLE value="PULSE(0 1 84u 10n 10n 2u 100u)"}
N 550 265 550 290 {}
N 550 350 550 368 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 265 0 1 {name=L5 lab=cm_sample}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 550 368 0 0 {name=L6 lab=0}
T {Late-transfer sampling window} 470 405 0 0 0.26 0.26 {layer=4}
T {Starts at 84 us, lasts 2 us} 470 433 0 0 0.25 0.25 {layer=8}
T {2   Hold the command for the next cycle} 801 137 0 0 0.43 0.43 {layer=4}
T {V(cm_ctrl) = limit [2.5 V + V(cm_acc), 0 V, VDD]} 801 185 0 0 0.29 0.29 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_behavior.sym} 838 320 0 0 {name=BICMCTRL kind=V expr=max(0,min(v(vdd),2.5+v(cm_acc)))}
N 838 258 838 290 {}
N 838 350 838 365 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 838 365 0 0 {name=L7 lab=0}
T {BICMCTRL} 794 405 0 0 0.25 0.25 {layer=4}
N 838 258 873 258 {}
N 873 258 930 258 {}
N 873 258 873 241 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 873 241 0 1 {name=L8 lab=cm_ctrl}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_switch.sym} 970 258 0 0 {name=SICMHOLD model=icm_hold}
N 970 290 970 310 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 310 0 0 {name=L9 lab=phi1}
T {SICMHOLD} 925 222 0 0 0.24 0.24 {layer=4}
N 1010 258 1100 258 {}
N 1100 258 1310 258 {}
N 1100 258 1100 241 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 241 0 1 {name=L10 lab=cm_hold}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 1100 320 0 0 {name=CICMHOLD value=20p m=1}
N 1100 258 1100 290 {}
N 1100 350 1100 365 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1100 365 0 0 {name=L11 lab=0}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1340 258 3 0 {name=RICMHOLD value=1e13 m=1}
N 1370 258 1440 258 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1440 258 0 1 {name=L12 lab=cm_init}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1440 335 0 0 {name=VICMINIT value=2.5}
N 1440 258 1440 305 {}
N 1440 365 1440 381 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1440 381 0 0 {name=L13 lab=0}
T {phi1 loads the hold capacitor during reset.} 887 431 0 0 0.26 0.26 {layer=8}
T {3   Shape the drive across both transfer phases} 42 517 0 0 0.43 0.43 {layer=4}
T {phit sets cm_edge1} 48 572 0 0 0.28 0.28 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_switch.sym} 166 638 0 0 {name=SICMEDGE1 model=icm_edge_set}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 95 638 0 1 {name=L14 lab=vdd}
N 95 638 126 638 {}
N 206 638 294 638 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 294 638 0 1 {name=L15 lab=cm_edge1}
N 166 670 166 688 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 166 688 0 0 {name=L16 lab=phit}
T {SICMEDGE1} 123 606 0 0 0.24 0.24 {layer=4}
N 294 638 294 764 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_switch.sym} 166 764 0 0 {name=SICMRST1 model=icm_edge_reset}
N 206 764 294 764 {}
N 126 764 95 764 {}
N 95 764 95 781 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 95 781 0 0 {name=L17 lab=0}
N 166 796 166 816 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 166 816 0 0 {name=L18 lab=phi1}
T {SICMRST1} 129 733 0 0 0.24 0.24 {layer=4}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 294 822 0 0 {name=CICMEDGE1 value=10p m=1}
N 294 764 294 792 {}
N 294 852 294 871 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 294 871 0 0 {name=L19 lab=0}
T {phi2 sets cm_edge2} 404 572 0 0 0.28 0.28 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_switch.sym} 522 638 0 0 {name=SICMEDGE2 model=icm_edge_set}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 451 638 0 0 {name=L20 lab=vdd}
N 451 638 482 638 {}
N 562 638 650 638 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 638 0 1 {name=L21 lab=cm_edge2}
N 522 670 522 688 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 522 688 0 0 {name=L22 lab=phi2}
T {SICMEDGE2} 479 606 0 0 0.24 0.24 {layer=4}
N 650 638 650 764 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_switch.sym} 522 764 0 0 {name=SICMRST2 model=icm_edge_reset}
N 562 764 650 764 {}
N 482 764 451 764 {}
N 451 764 451 781 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 451 781 0 0 {name=L23 lab=0}
N 522 796 522 816 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 522 816 0 0 {name=L24 lab=phi1}
T {SICMRST2} 485 733 0 0 0.24 0.24 {layer=4}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 650 822 0 0 {name=CICMEDGE2 value=10p m=1}
N 650 764 650 792 {}
N 650 852 650 871 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 650 871 0 0 {name=L25 lab=0}
T {User TG cells: NMOS 2.5u / PMOS 4.5u, L=0.8u} 42 893 0 0 0.27 0.27 {layer=8}
T {4   Inject the same correction into both OTA inputs} 800 517 0 0 0.43 0.43 {layer=4}
T {V(cm_x) = V(cm_hold) x [0.68 V(cm_edge1) + 0.32 V(cm_edge2)] / VDD} 800 560 0 0 0.26 0.26 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_behavior.sym} 830 760 0 0 {name=BICMDRIVE kind=V expr=((.68*v(cm_edge1)+.32*v(cm_edge2))/max(.1,v(vdd)))*v(cm_hold)}
N 830 664 830 730 {}
N 830 790 830 820 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 830 820 0 0 {name=L26 lab=0}
T {BICMDRIVE} 792 855 0 0 0.25 0.25 {layer=4}
N 830 664 880 664 {}
N 880 664 950 664 {}
N 880 664 880 641 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 641 0 1 {name=L27 lab=cm_x}
N 950 664 950 804 {}
N 950 664 1030 664 {}
N 950 804 1030 804 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_pmos40.sym} 1050 664 0 0 {name=MCORRp}
N 1070 634 1150 634 {}
N 1070 664 1150 664 {}
N 1070 694 1150 694 {}
N 1150 634 1150 664 {}
N 1150 664 1150 694 {}
N 1150 664 1260 664 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1260 664 0 0 {name=L28 lab=sump}
T {MCORRp   40 x (20 um / 10 um)} 1010 591 0 0 0.255 0.255 {layer=4}
T {to OTA INN} 1385 655 0 0 0.28 0.28 {layer=8}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_pmos40.sym} 1050 804 0 0 {name=MCORRn}
N 1070 774 1150 774 {}
N 1070 804 1150 804 {}
N 1070 834 1150 834 {}
N 1150 774 1150 804 {}
N 1150 804 1150 834 {}
N 1150 804 1260 804 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1260 804 0 0 {name=L29 lab=sumn}
T {MCORRn   40 x (20 um / 10 um)} 1010 731 0 0 0.255 0.255 {layer=4}
T {to OTA INP} 1385 795 0 0 0.28 0.28 {layer=8}
T {Each bank has source, drain, and well tied to its summing node.} 890 895 0 0 0.27 0.27 {layer=8}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/icm_models.sym} 32 959 0 0 {name=ICM_SWITCH_MODELS only_toplevel=false value=".model icm_hold SW(Ron=10 Roff=1e14 Vt=2 Vh=.1)
.model icm_edge_set SW(Ron=3000 Roff=1e13 Vt=1 Vh=.05)
.model icm_edge_reset SW(Ron=100k Roff=1e13 Vt=2 Vh=.1)"}
T {Sensing remains behavioral; switching uses user TG cells with transistor complement drivers.} 80 947 0 0 0.27 0.27 {layer=8}
