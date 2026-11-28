v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {SCL CONTROLLER CANDIDATE + PHYSICAL PHASE GENERATOR + EXISTING 7.5 pF AFE} 40 42 0 0 0.78 0.78 {layer=4}
T {Edit capacitor settings in CAP_VALUES | Verilog MOD-100 phases | 1 MHz master clock} 40 86 0 0 0.43 0.43 {layer=4}
T {MEMS SENSOR} 55 145 0 0 0.37 0.37 {layer=4}
T {CHARGE TRANSFER} 360 145 0 0 0.37 0.37 {layer=4}
T {OTA AND FEEDBACK} 790 145 0 0 0.37 0.37 {layer=4}
T {ANALOG OUTPUT} 1140 145 0 0 0.37 0.37 {layer=4}
T {Shared MEMS} 95 450 0 0 0.31 0.31 {layer=4}
T {electrode} 95 470 0 0 0.31 0.31 {layer=4}
T {CP: CAP_VALUES} 108 303 0 0 0.37 0.37 {layer=8}
T {phi2} 303 306 0 0 0.32 0.32 {layer=4}
T {phi1 sensor reset} 270 416 0 0 0.31 0.31 {layer=8}
T {phi1} 464 259 0 0 0.31 0.31 {layer=4}
T {CS PMOS: CAP_VALUES} 460 303 0 0 0.35 0.35 {layer=4}
T {phi1} 647 410 0 0 0.32 0.32 {layer=4}
T {phi2r} 645 306 0 0 0.32 0.32 {layer=4}
T {CFB: edit W/L/M with Q} 831 290 0 0 0.31 0.31 {layer=8}
T {RST (phi1)} 859 168 0 0 0.31 0.31 {layer=4}
T {CL = 5 pF} 1176 411 0 0 0.35 0.35 {layer=4}
T {CN: CAP_VALUES} 108 603 0 0 0.37 0.37 {layer=8}
T {phi2} 303 606 0 0 0.32 0.32 {layer=4}
T {phi1 sensor reset} 270 564 0 0 0.31 0.31 {layer=8}
T {phi1} 464 723 0 0 0.31 0.31 {layer=4}
T {CS PMOS: CAP_VALUES} 460 603 0 0 0.35 0.35 {layer=4}
T {phi1} 647 572 0 0 0.32 0.32 {layer=4}
T {phi2r} 645 606 0 0 0.32 0.32 {layer=4}
T {CFB: edit W/L/M with Q} 831 694 0 0 0.31 0.31 {layer=8}
T {RST (phi1)} 859 810 0 0 0.31 0.31 {layer=4}
T {CL = 5 pF} 1176 571 0 0 0.35 0.35 {layer=4}
T {Vdiff = VOUTP - VOUTN} 1120 494 0 0 0.31 0.31 {layer=4}
T {VP = 4.8 V     VCM target = 2.5 V} 42 838 0 0 0.33 0.33 {layer=4}
T {phi1 also resets CFB and the RX nodes. The sensor electrodes reset through SCL08 transmission gates.} 42 872 0 0 0.3 0.3 {layer=4}
T {CFB: PMOS devices; edit W/L/M with Q or use CAP_VALUES} 760 850 0 0 0.29 0.29 {layer=8}
T {PHYSICAL PHASE GENERATOR: 57 SCL cells / 564 MOSFETs / direct analog gate drive} 40 1050 0 0 0.4 0.4 {}
T {CAPACITOR SETTINGS: select CAP_VALUES, press Q, edit and save} 1400 190 0 0 0.3 0.3 {layer=4}
T {CS PMOS: source/drain/body = TX; gate = RX. 5 pF geometry target; bias dependent.} 360 910 0 0 0.28 0.28 {layer=8}
T {Edit CS_W, CS_L, CS_M in CAP_VALUES (Q). Defaults: 5 parallel devices, W=20u, L=25.3375u.} 360 940 0 0 0.28 0.28 {layer=8}
N 745 482 780 482 {
lab=vref}
N 745 518 780 518 {
lab=vbn}
N 745 552 780 552 {
lab=vbp}
N 1010 448 1045 448 {
lab=ota_vdd}
N 1010 482 1045 482 {
lab=0}
N 1010 518 1045 518 {
lab=bias}
N 80 350 80 500 {
lab=0}
N 80 500 80 650 {
lab=0}
N 80 500 125 500 {
lab=0}
N 80 350 109 350 {
lab=0}
N 189 350 235 350 {
lab=sensp}
N 235 350 280 350 {
lab=sensp}
N 360 350 430 350 {
lab=txp}
N 235 350 235 390 {
lab=sensp}
N 235 470 235 478 {
lab=0}
N 430 310 430 350 {
lab=txp}
N 430 205 430 230 {
lab=vp}
N 430 350 462 350 {
lab=txp}
N 542 350 610 350 {
lab=rxp}
N 610 350 627 350 {
lab=rxp}
N 610 350 610 382 {
lab=rxp}
N 610 462 610 470 {
lab=0}
N 707 350 740 350 {
lab=sump}
N 740 350 780 350 {
lab=sump}
N 1010 350 1060 350 {
lab=outp}
N 740 267 740 350 {
lab=sump}
N 740 218 740 267 {
lab=sump}
N 1060 267 1060 350 {
lab=outp}
N 1060 218 1060 267 {
lab=outp}
N 740 267 855 267 {
lab=sump}
N 935 267 1060 267 {
lab=outp}
N 740 218 855 218 {
lab=sump}
N 935 218 1060 218 {
lab=outp}
N 1060 350 1155 350 {
lab=outp}
N 1155 350 1292 350 {
lab=outp}
N 1155 350 1155 380 {
lab=outp}
N 1155 460 1155 467 {
lab=0}
N 80 650 109 650 {
lab=0}
N 189 650 235 650 {
lab=sensn}
N 235 650 280 650 {
lab=sensn}
N 360 650 430 650 {
lab=txn}
N 235 610 235 650 {
lab=sensn}
N 235 522 235 530 {
lab=0}
N 430 650 430 690 {
lab=txn}
N 430 770 430 795 {
lab=vp}
N 430 650 462 650 {
lab=txn}
N 542 650 610 650 {
lab=rxn}
N 610 650 627 650 {
lab=rxn}
N 610 618 610 650 {
lab=rxn}
N 610 530 610 538 {
lab=0}
N 707 650 740 650 {
lab=sumn}
N 740 650 780 650 {
lab=sumn}
N 1010 650 1060 650 {
lab=outn}
N 740 650 740 733 {
lab=sumn}
N 740 733 740 782 {
lab=sumn}
N 1060 650 1060 733 {
lab=outn}
N 1060 733 1060 782 {
lab=outn}
N 740 733 855 733 {
lab=sumn}
N 935 733 1060 733 {
lab=outn}
N 740 782 855 782 {
lab=sumn}
N 935 782 1060 782 {
lab=outn}
N 1060 650 1155 650 {
lab=outn}
N 1155 650 1292 650 {
lab=outn}
N 1155 620 1155 650 {
lab=outn}
N 1155 533 1155 540 {
lab=0}
C {../symbols/ota_vcr_final.sym} 895 500 0 0 {name=XOTA}
C {lab_pin.sym} 745 482 0 0 {name=L1 lab=vref}
C {lab_pin.sym} 745 518 0 0 {name=L2 lab=vbn}
C {lab_pin.sym} 745 552 0 0 {name=L3 lab=vbp}
C {../symbols/net_right.sym} 1045 448 0 0 {name=L4 lab=ota_vdd caption=ota_vdd}
C {../symbols/net_right.sym} 1045 482 0 0 {name=L5 lab=0 caption=0}
C {../symbols/net_right.sym} 1045 518 0 0 {name=L6 lab=bias caption=bias}
C {gnd.sym} 125 500 0 0 {name=G7 lab=0}
C {../symbols/cap_h.sym} 149 350 0 0 {name=CMEMP value=\{CP\}}
C {../symbols/Transmission_v1_26_h.sym} 320 350 0 0 {name=XSENSEP}
C {lab_pin.sym} 300 310 0 0 {name=TG_XSENSEP_0 lab=phi2}
C {lab_pin.sym} 300 390 0 0 {name=TG_XSENSEP_1 lab=0}
C {lab_pin.sym} 340 390 0 0 {name=TG_XSENSEP_2 lab=vdd}
C {lab_pin.sym} 340 310 0 0 {name=TG_XSENSEP_3 lab=phi2b}
C {../symbols/Transmission_v1_26_v.sym} 235 430 0 0 {name=XSRESETP}
C {lab_pin.sym} 195 410 0 0 {name=TG_XSRESETP_0 lab=phi1}
C {lab_pin.sym} 275 410 0 0 {name=TG_XSRESETP_1 lab=0}
C {lab_pin.sym} 275 450 0 0 {name=TG_XSRESETP_2 lab=vdd}
C {lab_pin.sym} 195 450 0 0 {name=TG_XSRESETP_3 lab=phi1b}
C {gnd.sym} 235 478 0 0 {name=G8 lab=0}
C {lab_pin.sym} 235 350 0 0 {name=L9 lab=sensp}
C {../symbols/Transmission_v1_26_v.sym} 430 270 0 0 {name=XCHARGEP}
C {lab_pin.sym} 390 250 0 0 {name=TG_XCHARGEP_0 lab=phi1}
C {lab_pin.sym} 470 250 0 0 {name=TG_XCHARGEP_1 lab=0}
C {lab_pin.sym} 470 290 0 0 {name=TG_XCHARGEP_2 lab=vdd}
C {lab_pin.sym} 390 290 0 0 {name=TG_XCHARGEP_3 lab=phi1b}
C {lab_pin.sym} 430 205 0 0 {name=L10 lab=vp}
C {../symbols/pmos_cfb.sym} 502 350 0 0 {name=MCSP model=P W=\{CS_W\} L=\{CS_L\} M=\{CS_M\}}
C {../symbols/Transmission_v1_26_v.sym} 610 422 0 0 {name=XRRESETP}
C {lab_pin.sym} 570 402 0 0 {name=TG_XRRESETP_0 lab=phi1}
C {lab_pin.sym} 650 402 0 0 {name=TG_XRRESETP_1 lab=0}
C {lab_pin.sym} 650 442 0 0 {name=TG_XRRESETP_2 lab=vdd}
C {lab_pin.sym} 570 442 0 0 {name=TG_XRRESETP_3 lab=phi1b}
C {gnd.sym} 610 470 0 0 {name=G11 lab=0}
C {../symbols/Transmission_v1_26_h.sym} 667 350 0 0 {name=XXFERP}
C {lab_pin.sym} 647 310 0 0 {name=TG_XXFERP_0 lab=phit}
C {lab_pin.sym} 647 390 0 0 {name=TG_XXFERP_1 lab=0}
C {lab_pin.sym} 687 390 0 0 {name=TG_XXFERP_2 lab=vdd}
C {lab_pin.sym} 687 310 0 0 {name=TG_XXFERP_3 lab=phitb}
C {lab_pin.sym} 430 350 0 0 {name=L12 lab=txp}
C {lab_pin.sym} 610 350 0 0 {name=L13 lab=rxp}
C {lab_pin.sym} 740 350 0 0 {name=L14 lab=sump}
C {../symbols/pmos_cfb.sym} 895 267 0 0 {name=MCFP model=P W=\{CFB_W\} L=\{CFB_L\} M=\{CFB_M\}}
C {../symbols/Transmission_v1_26_h.sym} 895 218 0 0 {name=XFBRESETP}
C {lab_pin.sym} 875 178 0 0 {name=TG_XFBRESETP_0 lab=phi1}
C {lab_pin.sym} 875 258 0 0 {name=TG_XFBRESETP_1 lab=0}
C {lab_pin.sym} 915 258 0 0 {name=TG_XFBRESETP_2 lab=vdd}
C {lab_pin.sym} 915 178 0 0 {name=TG_XFBRESETP_3 lab=phi1b}
C {../symbols/cap_v.sym} 1155 420 0 0 {name=CLP value=5p}
C {gnd.sym} 1155 467 0 0 {name=G15 lab=0}
C {../symbols/net_right.sym} 1292 350 0 0 {name=L16 lab=outp caption=VOUTP}
C {../symbols/pmos_cfb.sym} 149 650 0 0 {name=MCN model=P W=\{CN_W\} L=\{CN_L\} M=\{CN_M\}}
C {../symbols/Transmission_v1_26_h.sym} 320 650 0 0 {name=XSENSEN}
C {lab_pin.sym} 300 610 0 0 {name=TG_XSENSEN_0 lab=phi2}
C {lab_pin.sym} 300 690 0 0 {name=TG_XSENSEN_1 lab=0}
C {lab_pin.sym} 340 690 0 0 {name=TG_XSENSEN_2 lab=vdd}
C {lab_pin.sym} 340 610 0 0 {name=TG_XSENSEN_3 lab=phi2b}
C {../symbols/Transmission_v1_26_v.sym} 235 570 0 0 {name=XSRESETN}
C {lab_pin.sym} 195 550 0 0 {name=TG_XSRESETN_0 lab=phi1}
C {lab_pin.sym} 275 550 0 0 {name=TG_XSRESETN_1 lab=0}
C {lab_pin.sym} 275 590 0 0 {name=TG_XSRESETN_2 lab=vdd}
C {lab_pin.sym} 195 590 0 0 {name=TG_XSRESETN_3 lab=phi1b}
C {gnd.sym} 235 522 2 0 {name=G17 lab=0}
C {lab_pin.sym} 235 650 0 0 {name=L18 lab=sensn}
C {../symbols/Transmission_v1_26_v.sym} 430 730 0 0 {name=XCHARGEN}
C {lab_pin.sym} 390 710 0 0 {name=TG_XCHARGEN_0 lab=phi1}
C {lab_pin.sym} 470 710 0 0 {name=TG_XCHARGEN_1 lab=0}
C {lab_pin.sym} 470 750 0 0 {name=TG_XCHARGEN_2 lab=vdd}
C {lab_pin.sym} 390 750 0 0 {name=TG_XCHARGEN_3 lab=phi1b}
C {lab_pin.sym} 430 795 0 0 {name=L19 lab=vp}
C {../symbols/pmos_cfb.sym} 502 650 0 0 {name=MCSN model=P W=\{CS_W\} L=\{CS_L\} M=\{CS_M\}}
C {../symbols/Transmission_v1_26_v.sym} 610 578 0 0 {name=XRRESETN}
C {lab_pin.sym} 570 558 0 0 {name=TG_XRRESETN_0 lab=phi1}
C {lab_pin.sym} 650 558 0 0 {name=TG_XRRESETN_1 lab=0}
C {lab_pin.sym} 650 598 0 0 {name=TG_XRRESETN_2 lab=vdd}
C {lab_pin.sym} 570 598 0 0 {name=TG_XRRESETN_3 lab=phi1b}
C {gnd.sym} 610 530 2 0 {name=G20 lab=0}
C {../symbols/Transmission_v1_26_h.sym} 667 650 0 0 {name=XXFERN}
C {lab_pin.sym} 647 610 0 0 {name=TG_XXFERN_0 lab=phit}
C {lab_pin.sym} 647 690 0 0 {name=TG_XXFERN_1 lab=0}
C {lab_pin.sym} 687 690 0 0 {name=TG_XXFERN_2 lab=vdd}
C {lab_pin.sym} 687 610 0 0 {name=TG_XXFERN_3 lab=phitb}
C {lab_pin.sym} 430 650 0 0 {name=L21 lab=txn}
C {lab_pin.sym} 610 650 0 0 {name=L22 lab=rxn}
C {lab_pin.sym} 740 650 0 0 {name=L23 lab=sumn}
C {../symbols/pmos_cfb.sym} 895 733 0 0 {name=MCFN model=P W=\{CFB_W\} L=\{CFB_L\} M=\{CFB_M\}}
C {../symbols/Transmission_v1_26_h.sym} 895 782 0 0 {name=XFBRESETN}
C {lab_pin.sym} 875 742 0 0 {name=TG_XFBRESETN_0 lab=phi1}
C {lab_pin.sym} 875 822 0 0 {name=TG_XFBRESETN_1 lab=0}
C {lab_pin.sym} 915 822 0 0 {name=TG_XFBRESETN_2 lab=vdd}
C {lab_pin.sym} 915 742 0 0 {name=TG_XFBRESETN_3 lab=phi1b}
C {../symbols/cap_v.sym} 1155 580 0 0 {name=CLN value=5p}
C {gnd.sym} 1155 533 2 0 {name=G24 lab=0}
C {../symbols/net_right.sym} 1292 650 0 0 {name=L25 lab=outn caption=VOUTN}
C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 2300 250 0 0 {name=BENCH only_toplevel=false value=".include \"/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/mos/tntp49_5v\"
.include \"/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/res/typ/ppr\"
.include \"../models/vcr_low_total.spice\"
.temp 27
.options reltol=4e-4 vntol=3u abstol=1e-11 numdgt=12 method=gear maxord=2
VDD vdd 0 5
VOTA vdd ota_vdd 0
VREFSRC ref_src 0 2.5
VREFSENSE ref_src vref 0
.include \"../models/clock.spice\"
.include \"../models/vcr_low_total_bias.spice\"
VBIASDD vdd bias_vdd 0
XB ref_src bias_vdd 0 vbn vbp bias_src ota_bias08
VIREF bias_src bias 0
RLEAKP sensp 0 1e12
RLEAKN sensn 0 1e12
.save v(outp) v(outn) v(sump) v(sumn) v(txp) v(txn) v(rxp) v(rxn) v(sensp) v(sensn) v(phi1) v(phi2) v(phit) i(vdd) v(vbn) v(vbp) i(viref) i(vota) i(vbiasdd) i(vexc) v(xicm.xcore.cm_x) v(xicm.xcore.cm_hold)
.options method=gear reltol=4e-4 trtol=10
.tran 200n \{SIM_STOP\} 0 200n
.subckt corrected_tg A B PHI PHIB VDD VSS
MN A PHI B VSS N W=10u L=0.8u AD=45p AS=45p PD=29u PS=29u
MP A PHIB B VDD P W=20u L=0.8u AD=90p AS=90p PD=49u PS=49u
.ends corrected_tg

.subckt user_tg_control A B CTRL VDD
MINV_N cb CTRL 0 0 N W=2.5u L=.8u
MINV_P cb CTRL VDD VDD P W=4.5u L=.8u
XSW CTRL 0 A B VDD cb Transmission_v1_26
.ends user_tg_control

.options klu

.options maxord=2
.ic v(sump)=2.5 v(sumn)=2.5 v(outp)=2.5 v(outn)=2.5 v(rxp)=0 v(rxn)=0 v(txp)=4.8 v(txn)=4.8

.include ../models/used_scl_cells.spice
.include ../models/phase_generator_physical.spice"}
C {../symbols/capsense_phase_gen_physical.sym} 560 1350 0 0 {name=XPHASE}
C {lab_pin.sym} 300 1270 0 0 {name=LRTL_clk_1mhz lab=clk_1mhz}
C {lab_pin.sym} 300 1350 0 0 {name=LRTL_rst_n lab=rst_n}
C {lab_pin.sym} 820 1230 0 0 {name=LRTL_phi1 lab=phi1}
C {lab_pin.sym} 820 1270 0 0 {name=LRTL_phi1b lab=phi1b}
C {lab_pin.sym} 820 1310 0 0 {name=LRTL_phit lab=phit}
C {lab_pin.sym} 820 1350 0 0 {name=LRTL_phitb lab=phitb}
C {lab_pin.sym} 820 1390 0 0 {name=LRTL_phi2 lab=phi2}
C {lab_pin.sym} 820 1430 0 0 {name=LRTL_phi2b lab=phi2b}
C {lab_pin.sym} 820 1470 0 0 {name=LRTL_sample_valid lab=sample_valid}
C {vsource.sym} 0 1190 0 0 {name=Vclk_1mhz value="PULSE(0 5 0 1n 1n 499n 1u)"}
C {lab_pin.sym} 0 1160 0 0 {name=LSRC_clk_1mhz lab=clk_1mhz}
C {lab_pin.sym} 0 1220 0 0 {name=LGND_clk_1mhz lab=0}
C {vsource.sym} 0 1370 0 0 {name=Vrst_n value="PWL(0 5 1n 5 2n 0 2.25u 0 2.251u 5)"}
C {lab_pin.sym} 0 1340 0 0 {name=LSRC_rst_n lab=rst_n}
C {lab_pin.sym} 0 1400 0 0 {name=LGND_rst_n lab=0}
C {code_shown.sym} 1450 1100 0 0 {name=RESULTS only_toplevel=false value=".save v(sample_valid) v(clk_1mhz) v(rst_n) v(phi1b) v(phitb) v(phi2b)
.control
set xtrtol=2
set wr_singlescale
set wr_vecnames
run
let vdiff=v(outp)-v(outn)
let vcm_in=(v(sump)+v(sumn))/2
let vcm_out=(v(outp)+v(outn))/2
wrdata physical_drive_clocks.dat v(phi1) v(phit) v(phi2) v(phi1b) v(phitb) v(phi2b) v(sample_valid)
wrdata physical_drive_tx.dat v(txp) v(txn)
wrdata physical_drive_rx.dat v(rxp) v(rxn)
wrdata physical_drive_ota_inputs.dat v(sump) v(sumn)
wrdata physical_drive_ota_outputs.dat v(outp) v(outn)
wrdata physical_drive_commonmode.dat vcm_in vcm_out
wrdata physical_drive_differential.dat vdiff
write physical_drive.raw all
.endc"}
C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 1450 250 0 0 {name=CAP_VALUES only_toplevel=false value=".param PRESS_KPA=30
.param CP=\{0.9p + 2.24p/(1-(2.24/509)*PRESS_KPA) + 3.94016p/(1-(2.24/755.865)*PRESS_KPA)\}
.param CS_W=20u CS_L=25.3375u CS_M=5
.param CFB_W=20u CFB_L=38.0063u CFB_M=5
.param CN_W=20u CN_L=60.81u CN_M=5
.param VEXC=4.8
.param SIM_STOP=110u"}

C {/usr/share/xschem/xschem_library/devices/vsource.sym} -60 850 0 0 {name=VEXC value=\{VEXC\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -60 820 0 0 {name=LEXC lab=vp}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -60 880 0 0 {name=GEXC lab=0}
T {Candidate only: CS 5 pF / CFB 7.5 pF / CN 12 pF geometry targets; nominal model study.} 360 980 0 0 0.28 0.28 {layer=8}
T {Simulation reset has an explicit assert edge at 1-2 ns; original RTL unchanged.} 1450 700 0 0 0.25 0.25 {layer=8}

T {Physical drive check: set SIM_STOP in CAP_VALUES. 110 us tests one frame and counter rollover.} 40 2600 0 0 0.3 0.3 {layer=4}
T {SCL controller candidate: real MOS capacitors, RPP resistors, transistor amplifiers, user transmission gates.} 40 2640 0 0 0.28 0.28 {layer=4}
T {110 us is a digital drive check. Extend SIM_STOP for settled AFE measurements.} 40 2680 0 0 0.28 0.28 {layer=4}

T {PHYSICAL INPUT COMMON-MODE CONTROLLER - OPEN XICM TO INSPECT} 40 1610 0 0 .36 .36 {}
C {controller/ota_input_cm_servo.sym} 560 1900 0 0 {name=XICM}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1700 0 0 {name=LICM_0 lab=sump}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1740 0 0 {name=LICM_1 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1780 0 0 {name=LICM_2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1820 0 0 {name=LICM_3 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1860 0 0 {name=LICM_4 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1900 0 0 {name=LICM_5 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1940 0 0 {name=LICM_6 lab=phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 1980 0 0 {name=LICM_7 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 2020 0 0 {name=LICM_8 lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 2060 0 0 {name=LICM_9 lab=sample_valid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 410 2100 0 0 {name=LICM_10 lab=rst_n}
T {Testbench uses precharged summing nodes. Arbitrary power-on startup is not established.} 40 2540 0 0 .28 .28 {}
