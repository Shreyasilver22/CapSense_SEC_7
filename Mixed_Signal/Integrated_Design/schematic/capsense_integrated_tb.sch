v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Differential SC readout with VCR OTA and input CM correction} 40 42 0 0 0.78 0.78 {layer=4}
T {Edit capacitor settings in CAP_VALUES | Verilog MOD-100 phases | 1 MHz master clock} 40 86 0 0 0.43 0.43 {layer=4}
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
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 149 350 0 0 {name=CMEMP value=\{CP\}}
T {CP: CAP_VALUES} 108 303 0 0 0.37 0.37 {layer=8}
N 80 350 109 350 {}
N 189 350 235 350 {}
N 235 350 280 350 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_h.sym} 320 350 0 0 {name=XSENSEP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 310 0 0 {name=TG_XSENSEP_0 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 390 0 0 {name=TG_XSENSEP_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 390 0 0 {name=TG_XSENSEP_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 310 0 0 {name=TG_XSENSEP_3 lab=phi2b}
T {phi2} 303 306 0 0 0.32 0.32 {layer=4}
N 360 350 430 350 {}
N 235 350 235 390 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_v.sym} 235 430 0 0 {name=XSRESETP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 195 410 0 0 {name=TG_XSRESETP_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 410 0 0 {name=TG_XSRESETP_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 450 0 0 {name=TG_XSRESETP_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 195 450 0 0 {name=TG_XSRESETP_3 lab=phi1b}
N 235 470 235 478 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 235 478 0 0 {name=G8 lab=0}
T {phi1 sensor reset} 270 416 0 0 0.31 0.31 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 235 350 0 0 {name=L9 lab=sensp}
N 430 350 430 310 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_v.sym} 430 270 0 0 {name=XCHARGEP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 390 250 0 0 {name=TG_XCHARGEP_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 250 0 0 {name=TG_XCHARGEP_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 290 0 0 {name=TG_XCHARGEP_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 390 290 0 0 {name=TG_XCHARGEP_3 lab=phi1b}
N 430 230 430 205 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 205 0 0 {name=L10 lab=vp}
T {phi1} 464 259 0 0 0.31 0.31 {layer=4}
N 430 350 462 350 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 502 350 0 0 {name=CSP value=\{CS\}}
T {CS: CAP_VALUES} 460 303 0 0 0.35 0.35 {layer=4}
N 542 350 610 350 {}
N 610 350 627 350 {}
N 610 350 610 382 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_v.sym} 610 422 0 0 {name=XRRESETP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 402 0 0 {name=TG_XRRESETP_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 402 0 0 {name=TG_XRRESETP_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 442 0 0 {name=TG_XRRESETP_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 442 0 0 {name=TG_XRRESETP_3 lab=phi1b}
N 610 462 610 470 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 610 470 0 0 {name=G11 lab=0}
T {phi1} 647 410 0 0 0.32 0.32 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_h.sym} 667 350 0 0 {name=XXFERP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 647 310 0 0 {name=TG_XXFERP_0 lab=phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 647 390 0 0 {name=TG_XXFERP_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 687 390 0 0 {name=TG_XXFERP_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 687 310 0 0 {name=TG_XXFERP_3 lab=phitb}
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
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/pmos_cfb.sym} 895 267 0 0 {name=MCFP model=P W=\{CFB_W\} L=\{CFB_L\} M=\{CFB_M\}}
T {CFB: edit W/L/M with Q} 831 290 0 0 0.31 0.31 {layer=8}
N 740 218 855 218 {}
N 935 218 1060 218 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_h.sym} 895 218 0 0 {name=XFBRESETP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 875 178 0 0 {name=TG_XFBRESETP_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 875 258 0 0 {name=TG_XFBRESETP_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 915 258 0 0 {name=TG_XFBRESETP_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 915 178 0 0 {name=TG_XFBRESETP_3 lab=phi1b}
T {RST (phi1)} 859 168 0 0 0.31 0.31 {layer=4}
N 1060 350 1155 350 {}
N 1155 350 1292 350 {}
N 1155 350 1155 380 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_v.sym} 1155 420 0 0 {name=CLP value=5p}
N 1155 460 1155 467 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1155 467 0 0 {name=G15 lab=0}
T {CL = 5 pF} 1176 411 0 0 0.35 0.35 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/net_right.sym} 1292 350 0 0 {name=L16 lab=outp caption=VOUTP}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 149 650 0 0 {name=CMEMN value=\{CN\}}
T {CN: CAP_VALUES} 108 603 0 0 0.37 0.37 {layer=8}
N 80 650 109 650 {}
N 189 650 235 650 {}
N 235 650 280 650 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_h.sym} 320 650 0 0 {name=XSENSEN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 610 0 0 {name=TG_XSENSEN_0 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 690 0 0 {name=TG_XSENSEN_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 690 0 0 {name=TG_XSENSEN_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 610 0 0 {name=TG_XSENSEN_3 lab=phi2b}
T {phi2} 303 606 0 0 0.32 0.32 {layer=4}
N 360 650 430 650 {}
N 235 650 235 610 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_v.sym} 235 570 0 0 {name=XSRESETN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 195 550 0 0 {name=TG_XSRESETN_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 550 0 0 {name=TG_XSRESETN_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 590 0 0 {name=TG_XSRESETN_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 195 590 0 0 {name=TG_XSRESETN_3 lab=phi1b}
N 235 530 235 522 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 235 522 2 0 {name=G17 lab=0}
T {phi1 sensor reset} 270 564 0 0 0.31 0.31 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 235 650 0 0 {name=L18 lab=sensn}
N 430 650 430 690 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_v.sym} 430 730 0 0 {name=XCHARGEN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 390 710 0 0 {name=TG_XCHARGEN_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 710 0 0 {name=TG_XCHARGEN_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 750 0 0 {name=TG_XCHARGEN_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 390 750 0 0 {name=TG_XCHARGEN_3 lab=phi1b}
N 430 770 430 795 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 795 0 0 {name=L19 lab=vp}
T {phi1} 464 723 0 0 0.31 0.31 {layer=4}
N 430 650 462 650 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/cap_h.sym} 502 650 0 0 {name=CSN value=\{CS\}}
T {CS: CAP_VALUES} 460 603 0 0 0.35 0.35 {layer=4}
N 542 650 610 650 {}
N 610 650 627 650 {}
N 610 650 610 618 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_v.sym} 610 578 0 0 {name=XRRESETN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 558 0 0 {name=TG_XRRESETN_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 558 0 0 {name=TG_XRRESETN_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 598 0 0 {name=TG_XRRESETN_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 598 0 0 {name=TG_XRRESETN_3 lab=phi1b}
N 610 538 610 530 {}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 610 530 2 0 {name=G20 lab=0}
T {phi1} 647 572 0 0 0.32 0.32 {layer=4}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_h.sym} 667 650 0 0 {name=XXFERN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 647 610 0 0 {name=TG_XXFERN_0 lab=phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 647 690 0 0 {name=TG_XXFERN_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 687 690 0 0 {name=TG_XXFERN_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 687 610 0 0 {name=TG_XXFERN_3 lab=phitb}
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
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/pmos_cfb.sym} 895 733 0 0 {name=MCFN model=P W=\{CFB_W\} L=\{CFB_L\} M=\{CFB_M\}}
T {CFB: edit W/L/M with Q} 831 694 0 0 0.31 0.31 {layer=8}
N 740 782 855 782 {}
N 935 782 1060 782 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/Transmission_v1_26_h.sym} 895 782 0 0 {name=XFBRESETN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 875 742 0 0 {name=TG_XFBRESETN_0 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 875 822 0 0 {name=TG_XFBRESETN_1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 915 822 0 0 {name=TG_XFBRESETN_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 915 742 0 0 {name=TG_XFBRESETN_3 lab=phi1b}
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
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/bench_setup.sym} 1137 855 0 0 {name=BENCH value=".include /home/shreyas/Desktop/Sec_7/Integrated_Design/simulation/analog_support.spice
.include /home/shreyas/Desktop/Sec_7/Integrated_Design/simulation/cosim_models.spice"}
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
T {CFB: PMOS devices; edit W/L/M with Q or use CAP_VALUES} 760 850 0 0 0.29 0.29 {layer=8}
T {RTL PHASE GENERATOR — XSPICE digital nodes use d_ prefix; DAC outputs are 0/5 V} 40 1050 0 0 0.4 0.4 {}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_phase_gen.sym} 560 1350 0 0 {name=APHASE model=capsense_phase_gen_cosim}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 1270 0 0 {name=LRTL_clk_1mhz lab=d_clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 1350 0 0 {name=LRTL_rst_n lab=d_rst_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1230 0 0 {name=LRTL_phi1 lab=d_phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1270 0 0 {name=LRTL_phi1b lab=d_phi1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1310 0 0 {name=LRTL_phit lab=d_phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1350 0 0 {name=LRTL_phitb lab=d_phitb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1390 0 0 {name=LRTL_phi2 lab=d_phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1430 0 0 {name=LRTL_phi2b lab=d_phi2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 1470 0 0 {name=LRTL_sample_valid lab=d_sample_valid}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 0 1190 0 0 {name=Vclk_1mhz value="PULSE(0 5 0 1n 1n 499n 1u)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 1160 0 0 {name=LSRC_clk_1mhz lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 1220 0 0 {name=LGND_clk_1mhz lab=0}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 0 1370 0 0 {name=Vrst_n value="PWL(0 0 2u 0 2.001u 5)"}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 1340 0 0 {name=LSRC_rst_n lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 1400 0 0 {name=LGND_rst_n lab=0}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_adc.sym} 150 1540 0 0 {name=AINPUTS model=capsense_adc}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 70 1520 0 0 {name=LADC_clk_1mhz lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 70 1560 0 0 {name=LADC_rst_n lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 230 1520 0 0 {name=LADC_d_clk_1mhz lab=d_clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 230 1560 0 0 {name=LADC_d_rst_n lab=d_rst_n}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1150 0 0 {name=ADAC_phi1 model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1150 0 0 {name=LDACD_phi1 lab=d_phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1150 0 0 {name=LDACA_phi1 lab=phi1}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1250 0 0 {name=ADAC_phi1b model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1250 0 0 {name=LDACD_phi1b lab=d_phi1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1250 0 0 {name=LDACA_phi1b lab=phi1b}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1350 0 0 {name=ADAC_phit model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1350 0 0 {name=LDACD_phit lab=d_phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1350 0 0 {name=LDACA_phit lab=phit}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1450 0 0 {name=ADAC_phitb model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1450 0 0 {name=LDACD_phitb lab=d_phitb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1450 0 0 {name=LDACA_phitb lab=phitb}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1550 0 0 {name=ADAC_phi2 model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1550 0 0 {name=LDACD_phi2 lab=d_phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1550 0 0 {name=LDACA_phi2 lab=phi2}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1650 0 0 {name=ADAC_phi2b model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1650 0 0 {name=LDACD_phi2b lab=d_phi2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1650 0 0 {name=LDACA_phi2b lab=phi2b}
C {/home/shreyas/Desktop/Sec_7/Integrated_Design/symbols/capsense_dac.sym} 1150 1750 0 0 {name=ADAC_sample_valid model=capsense_dac}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 1750 0 0 {name=LDACD_sample_valid lab=d_sample_valid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1230 1750 0 0 {name=LDACA_sample_valid lab=sample_valid}
C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 1450 1100 0 0 {name=RESULTS only_toplevel=false value=".save v(sample_valid) v(clk_1mhz) v(rst_n) v(phi1b) v(phitb) v(phi2b)
.control
set xtrtol=2
shell ln -sfn /home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench /tmp/capsense_phase_runtime
shell ln -sfn /home/shreyas/Desktop/Sec_7/Integrated_Design /tmp/capsense_integrated
set wr_singlescale
set wr_vecnames
run
let vdiff=v(outp)-v(outn)
let vcm_in=(v(sump)+v(sumn))/2
let vcm_out=(v(outp)+v(outn))/2
wrdata exp1_clocks.dat v(phi1) v(phit) v(phi2) v(phi1b) v(phitb) v(phi2b) v(sample_valid)
wrdata exp1_tx.dat v(txp) v(txn)
wrdata exp1_rx.dat v(rxp) v(rxn)
wrdata exp1_ota_inputs.dat v(sump) v(sumn)
wrdata exp1_ota_outputs.dat v(outp) v(outn)
wrdata exp1_commonmode.dat vcm_in vcm_out
wrdata exp1_differential.dat vdiff
write integrated.raw all
.endc"}
C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 1450 1600 0 0 {name=CAP_VALUES only_toplevel=false value=".param CP=11.79p CN=10p CFB_L=202.7u SIM_STOP=795u"}

T {CAPACITOR SETTINGS: select CAP_VALUES, press Q, edit and save} 1400 190 0 0 0.3 0.3 {layer=4}
