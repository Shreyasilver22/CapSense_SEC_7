v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {icm_inv - SCL transistor implementation} 0 -100 0 0 .5 .5 {}
T {Node labels connect equal names. Open child symbols to inspect their transistors.} 0 -60 0 0 .25 .25 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 0 0 0 {name=P0 lab=a}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 60 0 0 {name=P1 lab=y}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 120 0 0 {name=P2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 180 0 0 {name=P3 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 160 180 0 0 {name=N model=N W="2.5u" L=".8u" nf=1 mult="1" ad="'(2.5u)*4.5u'" as="'(2.5u)*4.5u'" pd="'2*(2.5u)+9u'" ps="'2*(2.5u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 150 0 0 {name=L1 lab=y}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 180 0 0 {name=L2 lab=a}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 210 0 0 {name=L3 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 180 0 0 {name=L4 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 530 180 0 0 {name=P model=P W="4.5u" L=".8u" nf=1 mult="1" ad="'(4.5u)*4.5u'" as="'(4.5u)*4.5u'" pd="'2*(4.5u)+9u'" ps="'2*(4.5u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 210 0 0 {name=L5 lab=y}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 510 180 0 0 {name=L6 lab=a}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 150 0 0 {name=L7 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 180 0 0 {name=L8 lab=vdd}
