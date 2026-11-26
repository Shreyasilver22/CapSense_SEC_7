v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {RTL PHASE GENERATOR — XSPICE digital nodes use d_ prefix; DAC outputs are 0/5 V} 40 1050 0 0 0.4 0.4 {}
C {capsense_phase_gen.sym} 560 1350 0 0 {name=APHASE model=capsense_phase_gen_cosim}
C {devices/lab_pin.sym} 300 1270 0 0 {name=LRTL_clk_1mhz lab=d_clk_1mhz}
C {devices/lab_pin.sym} 300 1350 0 0 {name=LRTL_rst_n lab=d_rst_n}
C {devices/lab_pin.sym} 820 1230 0 0 {name=LRTL_phi1 lab=d_phi1}
C {devices/lab_pin.sym} 820 1270 0 0 {name=LRTL_phi1b lab=d_phi1b}
C {devices/lab_pin.sym} 820 1310 0 0 {name=LRTL_phit lab=d_phit}
C {devices/lab_pin.sym} 820 1350 0 0 {name=LRTL_phitb lab=d_phitb}
C {devices/lab_pin.sym} 820 1390 0 0 {name=LRTL_phi2 lab=d_phi2}
C {devices/lab_pin.sym} 820 1430 0 0 {name=LRTL_phi2b lab=d_phi2b}
C {devices/lab_pin.sym} 820 1470 0 0 {name=LRTL_sample_valid lab=d_sample_valid}
C {devices/vsource.sym} 0 1190 0 0 {name=Vclk_1mhz value="PULSE(0 5 0 1n 1n 499n 1u)"}
C {devices/lab_pin.sym} 0 1160 0 0 {name=LSRC_clk_1mhz lab=clk_1mhz}
C {devices/lab_pin.sym} 0 1220 0 0 {name=LGND_clk_1mhz lab=0}
C {devices/vsource.sym} 0 1370 0 0 {name=Vrst_n value="PWL(0 0 2u 0 2.001u 5)"}
C {devices/lab_pin.sym} 0 1340 0 0 {name=LSRC_rst_n lab=rst_n}
C {devices/lab_pin.sym} 0 1400 0 0 {name=LGND_rst_n lab=0}
C {capsense_adc.sym} 150 1540 0 0 {name=AINPUTS model=capsense_adc}
C {devices/lab_pin.sym} 70 1520 0 0 {name=LADC_clk_1mhz lab=clk_1mhz}
C {devices/lab_pin.sym} 70 1560 0 0 {name=LADC_rst_n lab=rst_n}
C {devices/lab_pin.sym} 230 1520 0 0 {name=LADC_d_clk_1mhz lab=d_clk_1mhz}
C {devices/lab_pin.sym} 230 1560 0 0 {name=LADC_d_rst_n lab=d_rst_n}
C {capsense_dac.sym} 1150 1150 0 0 {name=ADAC_phi1 model=capsense_dac}
C {devices/lab_pin.sym} 1070 1150 0 0 {name=LDACD_phi1 lab=d_phi1}
C {devices/lab_pin.sym} 1230 1150 0 0 {name=LDACA_phi1 lab=phi1}
C {capsense_dac.sym} 1150 1250 0 0 {name=ADAC_phi1b model=capsense_dac}
C {devices/lab_pin.sym} 1070 1250 0 0 {name=LDACD_phi1b lab=d_phi1b}
C {devices/lab_pin.sym} 1230 1250 0 0 {name=LDACA_phi1b lab=phi1b}
C {capsense_dac.sym} 1150 1350 0 0 {name=ADAC_phit model=capsense_dac}
C {devices/lab_pin.sym} 1070 1350 0 0 {name=LDACD_phit lab=d_phit}
C {devices/lab_pin.sym} 1230 1350 0 0 {name=LDACA_phit lab=phit}
C {capsense_dac.sym} 1150 1450 0 0 {name=ADAC_phitb model=capsense_dac}
C {devices/lab_pin.sym} 1070 1450 0 0 {name=LDACD_phitb lab=d_phitb}
C {devices/lab_pin.sym} 1230 1450 0 0 {name=LDACA_phitb lab=phitb}
C {capsense_dac.sym} 1150 1550 0 0 {name=ADAC_phi2 model=capsense_dac}
C {devices/lab_pin.sym} 1070 1550 0 0 {name=LDACD_phi2 lab=d_phi2}
C {devices/lab_pin.sym} 1230 1550 0 0 {name=LDACA_phi2 lab=phi2}
C {capsense_dac.sym} 1150 1650 0 0 {name=ADAC_phi2b model=capsense_dac}
C {devices/lab_pin.sym} 1070 1650 0 0 {name=LDACD_phi2b lab=d_phi2b}
C {devices/lab_pin.sym} 1230 1650 0 0 {name=LDACA_phi2b lab=phi2b}
C {capsense_dac.sym} 1150 1750 0 0 {name=ADAC_sample_valid model=capsense_dac}
C {devices/lab_pin.sym} 1070 1750 0 0 {name=LDACD_sample_valid lab=d_sample_valid}
C {devices/lab_pin.sym} 1230 1750 0 0 {name=LDACA_sample_valid lab=sample_valid}
C {devices/code_shown.sym} 1450 1100 0 0 {name=SIM only_toplevel=false value=".include /home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench/simulation/models.spice
Rphi1 phi1 0 1meg
Rphi1b phi1b 0 1meg
Rphit phit 0 1meg
Rphitb phitb 0 1meg
Rphi2 phi2 0 1meg
Rphi2b phi2b 0 1meg
Rsv sample_valid 0 1meg
.control
set wr_singlescale
set wr_vecnames
tran 10n 305u
write phases.raw all
wrdata phases.dat v(clk_1mhz) v(rst_n) v(phi1) v(phi1b) v(phit) v(phitb) v(phi2) v(phi2b) v(sample_valid)
set hcopydevtype svg
hardcopy phases.svg v(phi1) v(phit) v(phi2) v(sample_valid)
plot v(phi1) 
plot v(phi2)
plot v(phit)
.endc"}
