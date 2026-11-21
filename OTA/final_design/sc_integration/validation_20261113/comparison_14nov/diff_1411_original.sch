v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {SCL CP8D 5 V | Differential SC sensor readout | First simulation prototype} 520 290 0 0 0.55 0.55 {}
T {One extracted telescopic OTA with CMFB; differential output = V(outp)-V(outn). Explicit reconstructed SCL08 switches.} 520 350 0 0 0.32 0.32 {}
T {Sensor P | C=CP | Cf=40 pF | phi1=sample/reset; phiT=RX transfer; phi2=TX discharge} 520 990 0 0 0.3 0.3 {}
T {Sensor N | C=CN | Cf=40 pF | phi1=sample/reset; phiT=RX transfer; phi2=TX discharge} 520 1640 0 0 0.3 0.3 {}
T {Output CM target=2.5 V; input CM floats during transfer.
IREF=3.5uA; VBN=3.0V; VBP=VDD-2.2V.
RX transfer starts 1 us before TX discharge; clock edges 1000 ns.
Cap values and simulation controls are in tb/xschem_support.inc.} 2340 1320 0 0 0.23 0.23 {}
N 2020 620 2020 640 {
lab=outp}
N 2050 570 2050 580 {
lab=sump}
N 2000 570 2050 570 {
lab=sump}
N 2080 620 2090 620 {
lab=outp}
N 2090 590 2090 620 {
lab=outp}
N 2050 620 2050 640 {
lab=outp}
N 2050 640 2090 640 {
lab=outp}
N 2090 620 2090 640 {
lab=outp}
N 2020 640 2050 640 {
lab=outp}
N 1970 1240 2030 1240 {
lab=sumn}
N 2000 1280 2000 1300 {
lab=outn}
N 2000 1300 2120 1300 {
lab=outn}
N 2120 1240 2120 1300 {
lab=outn}
N 2030 1280 2030 1300 {
lab=outn}
N 2060 1280 2060 1300 {
lab=outn}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 700 670 0 0 {name=xdrive_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 550 630 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 850 630 0 0 {name=p2 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 850 650 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 850 670 0 0 {name=p4 sig_type=std_logic lab=txp}
C {devices/lab_pin.sym} 850 690 0 0 {name=p5 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 850 710 0 0 {name=p6 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 700 850 0 0 {name=xdischarge_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 850 810 0 0 {name=p8 sig_type=std_logic lab=phi2}
C {devices/lab_pin.sym} 850 830 0 0 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 850 850 0 0 {name=p10 sig_type=std_logic lab=txp}
C {devices/lab_pin.sym} 850 870 0 0 {name=p11 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 850 890 0 0 {name=p12 sig_type=std_logic lab=phi2b}
C {devices/capa.sym} 1170 670 1 0 {name=CSp value=\{CP\} m=1}
C {devices/lab_pin.sym} 1140 670 0 0 {name=p13 sig_type=std_logic lab=txp}
C {devices/lab_pin.sym} 1200 670 0 0 {name=p14 sig_type=std_logic lab=rxp}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 1250 890 0 0 {name=xclamp_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 1100 850 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1400 850 0 0 {name=p16 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 1400 870 0 0 {name=p17 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1400 890 0 0 {name=p18 sig_type=std_logic lab=rxp}
C {devices/lab_pin.sym} 1400 910 0 0 {name=p19 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1400 930 0 0 {name=p20 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 1560 670 0 0 {name=xtransfer_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 1410 630 0 0 {name=p21 sig_type=std_logic lab=rxp}
C {devices/lab_pin.sym} 1710 630 0 0 {name=p22 sig_type=std_logic lab=phit}
C {devices/lab_pin.sym} 1710 650 0 0 {name=p23 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1710 670 0 0 {name=p24 sig_type=std_logic lab=sump}
C {devices/lab_pin.sym} 1710 690 0 0 {name=p25 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1710 710 0 0 {name=p26 sig_type=std_logic lab=phitb}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 2020 480 0 0 {name=xreset_p wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 1870 440 0 0 {name=p27 sig_type=std_logic lab=sump}
C {devices/lab_pin.sym} 2170 440 0 0 {name=p28 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 2170 460 0 0 {name=p29 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2170 480 0 0 {name=p30 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 2170 500 0 0 {name=p31 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2170 520 0 0 {name=p32 sig_type=std_logic lab=phi1b}
C {devices/lab_pin.sym} 2090 590 2 0 {name=p34 sig_type=std_logic lab=outp}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 700 1320 0 0 {name=xdrive_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 550 1280 0 0 {name=p38 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 850 1280 0 0 {name=p39 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 850 1300 0 0 {name=p40 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 850 1320 0 0 {name=p41 sig_type=std_logic lab=txn}
C {devices/lab_pin.sym} 850 1340 0 0 {name=p42 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 850 1360 0 0 {name=p43 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 700 1500 0 0 {name=xdischarge_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 850 1460 0 0 {name=p45 sig_type=std_logic lab=phi2}
C {devices/lab_pin.sym} 850 1480 0 0 {name=p46 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 850 1500 0 0 {name=p47 sig_type=std_logic lab=txn}
C {devices/lab_pin.sym} 850 1520 0 0 {name=p48 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 850 1540 0 0 {name=p49 sig_type=std_logic lab=phi2b}
C {devices/capa.sym} 1170 1320 1 0 {name=CSn value=\{CN\} m=1}
C {devices/lab_pin.sym} 1140 1320 0 0 {name=p50 sig_type=std_logic lab=txn}
C {devices/lab_pin.sym} 1200 1320 0 0 {name=p51 sig_type=std_logic lab=rxn}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 1250 1540 0 0 {name=xclamp_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 1100 1500 0 0 {name=p52 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1400 1500 0 0 {name=p53 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 1400 1520 0 0 {name=p54 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1400 1540 0 0 {name=p55 sig_type=std_logic lab=rxn}
C {devices/lab_pin.sym} 1400 1560 0 0 {name=p56 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1400 1580 0 0 {name=p57 sig_type=std_logic lab=phi1b}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 1560 1320 0 0 {name=xtransfer_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 1410 1280 0 0 {name=p58 sig_type=std_logic lab=rxn}
C {devices/lab_pin.sym} 1710 1280 0 0 {name=p59 sig_type=std_logic lab=phit}
C {devices/lab_pin.sym} 1710 1300 0 0 {name=p60 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1710 1320 0 0 {name=p61 sig_type=std_logic lab=sumn}
C {devices/lab_pin.sym} 1710 1340 0 0 {name=p62 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1710 1360 0 0 {name=p63 sig_type=std_logic lab=phitb}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/scl08_tg.sym} 2020 1130 0 0 {name=xreset_n wn=10u wp=20u l=0.8u}
C {devices/lab_pin.sym} 1870 1090 0 0 {name=p64 sig_type=std_logic lab=sumn}
C {devices/lab_pin.sym} 2170 1090 0 0 {name=p65 sig_type=std_logic lab=phi1}
C {devices/lab_pin.sym} 2170 1110 0 0 {name=p66 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2170 1130 0 0 {name=p67 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 2170 1150 0 0 {name=p68 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2170 1170 0 0 {name=p69 sig_type=std_logic lab=phi1b}
C {devices/lab_pin.sym} 1970 1240 0 0 {name=p70 sig_type=std_logic lab=sumn}
C {devices/lab_pin.sym} 2120 1240 0 0 {name=p71 sig_type=std_logic lab=outn}
C {devices/vsource.sym} 670 480 0 0 {name=VDD value=5}
C {devices/lab_pin.sym} 670 450 0 0 {name=psupply lab=vdd}
C {devices/gnd.sym} 670 510 0 0 {name=gsupply lab=0}
C {devices/vsource.sym} 970 480 0 0 {name=VREF value=2.5}
C {devices/lab_pin.sym} 970 450 0 0 {name=pref lab=vref}
C {devices/gnd.sym} 970 510 0 0 {name=gref lab=0}
C {/home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/symbols/ota_cm2p5.sym} 2570 1070 0 0 {name=XOTA}
C {devices/lab_pin.sym} 2460 980 0 0 {name=OTA_P0 lab=sumn}
C {devices/lab_pin.sym} 2460 1010 0 0 {name=OTA_P1 lab=sump}
C {devices/lab_pin.sym} 2680 980 0 0 {name=OTA_P2 lab=outp}
C {devices/lab_pin.sym} 2680 1010 0 0 {name=OTA_P3 lab=outn}
C {devices/lab_pin.sym} 2570 920 0 0 {name=OTA_P4 lab=vdd}
C {devices/lab_pin.sym} 2570 1220 0 0 {name=OTA_P5 lab=0}
C {devices/lab_pin.sym} 2460 1090 0 0 {name=OTA_P6 lab=bias}
C {devices/lab_pin.sym} 2460 1125 0 0 {name=OTA_P7 lab=vref}
C {devices/lab_pin.sym} 2460 1160 0 0 {name=OTA_P8 lab=vbn}
C {devices/lab_pin.sym} 2460 1190 0 0 {name=OTA_P9 lab=vbp}
C {devices/code.sym} 1580 1490 0 0 {name=SIM
only_toplevel=false
value="
* Models
.include /home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/mos/tntp49_5v
.include /home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/res/typ/ppr

.include /home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/sc_integration/models/scl08_tg.spice
.include /home/shreyas/Desktop/CapSense_SEC_7/OTA/final_design/models/ota_cm2p5_C.spice

.param CP=7p CN=5p

.temp 27
.options reltol=1e-5 vntol=1e-8 abstol=1e-12
.options method=gear maxord=2 numdgt=12

* Feed current into the existing OTA bias node
IREF vdd bias DC 3.5u

* Clocks
VPHI1 phi1 0 PULSE(5 0 41u 1u 1u 58u 100u)
VPHI2 phi2 0 PULSE(0 5 46u 1u 1u 43u 100u)
VPHIT phit 0 PULSE(0 5 45u 1u 1u 44u 100u)

BPHI1B phi1b 0 V=5-v(phi1)
BPHI2B phi2b 0 V=5-v(phi2)
BPHITB phitb 0 V=5-v(phit)

* Output loads
CLP outp 0 5p
CLN outn 0 5p

.control
set wr_singlescale
set wr_vecnames
set numdgt=12

save v(outp) v(outn) v(sump) v(sumn)
tran 50n 500u 0 50n

let vdiff = v(outp)-v(outn)

wrdata waveforms.dat v(outp) v(outn) vdiff v(sump) v(sumn)
plot v(outp) v(outn)
plot vdiff
.endc
"}
C {pmos4_p_cp8d.sym} 2050 600 1 0 {W=100u
L=202.7u
nf=5
mult=1
ad=186p
as=186p
pd=138.6u
ps=138.6u
nrd=0.018
nrs=0.018
}
C {devices/lab_pin.sym} 2000 570 0 0 {name=p35 sig_type=std_logic lab=sump}
C {pmos4_p_cp8d.sym} 2030 1260 1 0 {W=100u
L=202.7u
nf=5
mult=1
ad=186p
as=186p
pd=138.6u
ps=138.6u
nrd=0.018
nrs=0.018
}
C {devices/lab_pin.sym} 550 810 0 0 {name=pref1 lab=vref}
C {devices/lab_pin.sym} 550 1460 0 0 {name=pref2 lab=vref}
C {devices/vsource.sym} 1090 490 0 0 {name=Vbn value=3}
C {devices/lab_pin.sym} 1090 460 0 0 {name=pref3 lab=vbn}
C {devices/gnd.sym} 1090 520 0 0 {name=gref1 lab=0}
C {devices/vsource.sym} 1220 490 0 0 {name=vbp value=2.7}
C {devices/lab_pin.sym} 1220 460 0 0 {name=pref4 lab=vbp}
C {devices/gnd.sym} 1220 520 0 0 {name=gref2 lab=0}
