v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {EXPERIMENTAL POST-AFE GAIN: SCL OTA, RPP resistors and real transmission gates} 20 -250 0 0 0.45 0.45 {layer=4}
T {PG_GAIN=1 / 2 / 4 in top-level PG_SETTINGS. Static controls; change between acquisitions.} 20 -210 0 0 0.3 0.3 {layer=4}
T {Not selected for precision sign-off: native model predicts excessive input-pair flicker noise.} 20 -175 0 0 0.3 0.3 {layer=4}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 100 1800 0 0 {name=VPGDD value=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 1770 2 0 {name=L_VPGDD_P lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 1830 2 0 {name=L_VPGDD_N lab=pg_vdd}
C {./postgain_bias.sym} 400 1400 0 0 {name=XPG_BIAS }
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 1328 0 0 {name=L_XPG_BIAS_REF lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 1360 0 0 {name=L_XPG_BIAS_VDD lab=pg_vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 275 1392 0 0 {name=L_XPG_BIAS_VSS lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 525 1328 2 0 {name=L_XPG_BIAS_VBN lab=pg_vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 525 1360 2 0 {name=L_XPG_BIAS_VBP lab=pg_vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 525 1392 2 0 {name=L_XPG_BIAS_IREF lab=pg_bias}
C {./ota_vcr_final.sym} 1000 500 0 0 {name=XPG }
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 885 650 0 0 {name=L_XPG_INP lab=pg_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 885 350 0 0 {name=L_XPG_INN lab=pg_p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1115 350 2 0 {name=L_XPG_OUTP lab=pg_outp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1115 650 2 0 {name=L_XPG_OUTN lab=pg_outn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1115 448 2 0 {name=L_XPG_VDD lab=pg_vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1115 482 2 0 {name=L_XPG_VSS lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1115 518 2 0 {name=L_XPG_IREF lab=pg_bias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 885 482 0 0 {name=L_XPG_VCM lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 885 518 0 0 {name=L_XPG_VBN lab=pg_vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 885 552 0 0 {name=L_XPG_VBP lab=pg_vbp}
C {./postgain_rpp.sym} 300 350 0 0 {name=XPG_IP W=\{PG_RW\} L=\{PG_RW*PG_RIN/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 350 0 0 {name=L_XPG_IP_P lab=outn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 350 2 0 {name=L_XPG_IP_N lab=pg_p}
C {./postgain_rpp.sym} 300 650 0 0 {name=XPG_IN W=\{PG_RW\} L=\{PG_RW*PG_RIN/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 650 0 0 {name=L_XPG_IN_P lab=outp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 650 2 0 {name=L_XPG_IN_N lab=pg_n}
C {./postgain_rpp.sym} 350 180 0 0 {name=XPG_FP0 W=\{PG_RW\} L=\{PG_RW*PG_RIN/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 180 0 0 {name=L_XPG_FP0_P lab=pg_p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 180 2 0 {name=L_XPG_FP0_N lab=pg_fp1}
C {./postgain_rpp.sym} 650 180 0 0 {name=XPG_FP1 W=\{PG_RW\} L=\{PG_RW*PG_RIN/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 180 0 0 {name=L_XPG_FP1_P lab=pg_fp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 730 180 2 0 {name=L_XPG_FP1_N lab=pg_fp2}
C {./postgain_rpp.sym} 950 180 0 0 {name=XPG_FP2 W=\{PG_RW\} L=\{PG_RW*PG_RIN*2/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 870 180 0 0 {name=L_XPG_FP2_P lab=pg_fp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1030 180 2 0 {name=L_XPG_FP2_N lab=pg_outp}
C {./postgain_rpp.sym} 350 850 0 0 {name=XPG_FN0 W=\{PG_RW\} L=\{PG_RW*PG_RIN/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 850 0 0 {name=L_XPG_FN0_P lab=pg_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 850 2 0 {name=L_XPG_FN0_N lab=pg_fn1}
C {./postgain_rpp.sym} 650 850 0 0 {name=XPG_FN1 W=\{PG_RW\} L=\{PG_RW*PG_RIN/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 850 0 0 {name=L_XPG_FN1_P lab=pg_fn1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 730 850 2 0 {name=L_XPG_FN1_N lab=pg_fn2}
C {./postgain_rpp.sym} 950 850 0 0 {name=XPG_FN2 W=\{PG_RW\} L=\{PG_RW*PG_RIN*2/28\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 870 850 0 0 {name=L_XPG_FN2_P lab=pg_fn2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1030 850 2 0 {name=L_XPG_FN2_N lab=pg_outn}
C {./Transmission_v1_26_h.sym} 650 -70 0 0 {name=XPG_SW1P }
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 630 -110 0 0 {name=L_XPG_SW1P_phi lab=pg_sw1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 630 -30 0 0 {name=L_XPG_SW1P_VSS1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 -70 0 0 {name=L_XPG_SW1P_In lab=pg_fp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 -70 2 0 {name=L_XPG_SW1P_Out lab=pg_fp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -30 2 0 {name=L_XPG_SW1P_VDD lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -110 2 0 {name=L_XPG_SW1P_phibar lab=pg_sw1b}
C {./Transmission_v1_26_h.sym} 950 -70 0 0 {name=XPG_SW2P }
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 930 -110 0 0 {name=L_XPG_SW2P_phi lab=pg_sw2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 930 -30 0 0 {name=L_XPG_SW2P_VSS1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 -70 0 0 {name=L_XPG_SW2P_In lab=pg_fp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 -70 2 0 {name=L_XPG_SW2P_Out lab=pg_outp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -30 2 0 {name=L_XPG_SW2P_VDD lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -110 2 0 {name=L_XPG_SW2P_phibar lab=pg_sw2b}
C {./Transmission_v1_26_h.sym} 650 1050 0 0 {name=XPG_SW1N }
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 630 1010 0 0 {name=L_XPG_SW1N_phi lab=pg_sw1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 630 1090 0 0 {name=L_XPG_SW1N_VSS1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 1050 0 0 {name=L_XPG_SW1N_In lab=pg_fn1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 1050 2 0 {name=L_XPG_SW1N_Out lab=pg_fn2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 1090 2 0 {name=L_XPG_SW1N_VDD lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 1010 2 0 {name=L_XPG_SW1N_phibar lab=pg_sw1b}
C {./Transmission_v1_26_h.sym} 950 1050 0 0 {name=XPG_SW2N }
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 930 1010 0 0 {name=L_XPG_SW2N_phi lab=pg_sw2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 930 1090 0 0 {name=L_XPG_SW2N_VSS1 lab=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 1050 0 0 {name=L_XPG_SW2N_In lab=pg_fn2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 1050 2 0 {name=L_XPG_SW2N_Out lab=pg_outn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 1090 2 0 {name=L_XPG_SW2N_VDD lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 1010 2 0 {name=L_XPG_SW2N_phibar lab=pg_sw2b}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 330 1800 0 0 {name=VPG_SW1 value=\{5*(PG_GAIN<1.5)\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 330 1770 2 0 {name=L_VPG_SW1_P lab=pg_sw1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 330 1830 2 0 {name=L_VPG_SW1_N lab=0}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 560 1800 0 0 {name=VPG_SW1B value=\{5*(PG_GAIN>=1.5)\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 560 1770 2 0 {name=L_VPG_SW1B_P lab=pg_sw1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 560 1830 2 0 {name=L_VPG_SW1B_N lab=0}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 790 1800 0 0 {name=VPG_SW2 value=\{5*(PG_GAIN<3)\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 1770 2 0 {name=L_VPG_SW2_P lab=pg_sw2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 1830 2 0 {name=L_VPG_SW2_N lab=0}
C {/usr/share/xschem/xschem_library/devices/vsource.sym} 1020 1800 0 0 {name=VPG_SW2B value=\{5*(PG_GAIN>=3)\}}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1020 1770 2 0 {name=L_VPG_SW2B_P lab=pg_sw2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1020 1830 2 0 {name=L_VPG_SW2B_N lab=0}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 1250 1800 0 0 {name=CPG_LP value=5p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 1770 2 0 {name=L_CPG_LP_P lab=pg_outp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 1830 2 0 {name=L_CPG_LP_N lab=0}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 1480 1800 0 0 {name=CPG_LN value=5p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1480 1770 2 0 {name=L_CPG_LN_P lab=pg_outn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1480 1830 2 0 {name=L_CPG_LN_N lab=0}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 100 2000 0 0 {name=PORT_outp lab=outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 330 2000 0 0 {name=PORT_outn lab=outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 560 2000 0 0 {name=PORT_pg_outp lab=pg_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 790 2000 0 0 {name=PORT_pg_outn lab=pg_outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1020 2000 0 0 {name=PORT_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1250 2000 0 0 {name=PORT_vref lab=vref}
T {5 pF output capacitors are testbench loads. Existing AFE, reference and phase generator unchanged.} 20 2100 0 0 0.28 0.28 {layer=4}
