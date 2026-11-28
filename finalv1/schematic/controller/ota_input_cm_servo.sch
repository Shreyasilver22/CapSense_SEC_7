v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ota_input_cm_servo - SCL transistor implementation} 0 -100 0 0 .5 .5 {}
T {Node labels connect equal names. Open child symbols to inspect their transistors.} 0 -60 0 0 .25 .25 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 0 0 0 {name=P0 lab=sump}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 60 0 0 {name=P1 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 120 0 0 {name=P2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 180 0 0 {name=P3 lab=vss}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 240 0 0 {name=P4 lab=vref}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 300 0 0 {name=P5 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 360 0 0 {name=P6 lab=phit}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 420 0 0 {name=P7 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 480 0 0 {name=P8 lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 540 0 0 {name=P9 lab=sample_valid}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 600 0 0 {name=P10 lab=rst_n}
C {./icm_frame_sample.sym} 160 180 0 0 {name=XTIMING}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 80 0 0 {name=L1 lab=clk_1mhz}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 120 0 0 {name=L2 lab=sample_valid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 160 0 0 {name=L3 lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 200 0 0 {name=L4 lab=sample_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 240 0 0 {name=L5 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 280 0 0 {name=L6 lab=vss}
C {./icm_physical.sym} 530 180 0 0 {name=XCORE}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 0 0 0 {name=L7 lab=sump}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 40 0 0 {name=L8 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 80 0 0 {name=L9 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 120 0 0 {name=L10 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 160 0 0 {name=L11 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 200 0 0 {name=L12 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 240 0 0 {name=L13 lab=phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 280 0 0 {name=L14 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 320 0 0 {name=L15 lab=sample_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 360 0 0 {name=L16 lab=rst_n}
