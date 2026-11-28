v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {icm_buffer - SCL transistor implementation} 0 -100 0 0 .5 .5 {}
T {Node labels connect equal names. Open child symbols to inspect their transistors.} 0 -60 0 0 .25 .25 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 0 0 0 {name=P0 lab=command}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 60 0 0 {name=P1 lab=output}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 120 0 0 {name=P2 lab=nb}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 180 0 0 {name=P3 lab=pb}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 240 0 0 {name=P4 lab=enable}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 300 0 0 {name=P5 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 360 0 0 {name=P6 lab=vss}
C {./icm_inv.sym} 160 180 0 0 {name=XI}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 120 0 0 {name=L1 lab=enable}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 160 0 0 {name=L2 lab=disabled}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 200 0 0 {name=L3 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 240 0 0 {name=L4 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 530 180 0 0 {name=T model=P W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 210 0 0 {name=L5 lab=bt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 510 180 0 0 {name=L6 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 150 0 0 {name=L7 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 180 0 0 {name=L8 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 900 180 0 0 {name=L model=P W="8u" L="2.4u" nf=1 mult="1" ad="'(8u)*4.5u'" as="'(8u)*4.5u'" pd="'2*(8u)+9u'" ps="'2*(8u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 210 0 0 {name=L9 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 180 0 0 {name=L10 lab=output}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 150 0 0 {name=L11 lab=bt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 180 0 0 {name=L12 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 180 0 0 {name=R model=P W="8u" L="2.4u" nf=1 mult="1" ad="'(8u)*4.5u'" as="'(8u)*4.5u'" pd="'2*(8u)+9u'" ps="'2*(8u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 210 0 0 {name=L13 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 180 0 0 {name=L14 lab=command}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 150 0 0 {name=L15 lab=bt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 180 0 0 {name=L16 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 1640 180 0 0 {name=NL model=N W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 150 0 0 {name=L17 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 180 0 0 {name=L18 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 210 0 0 {name=L19 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 180 0 0 {name=L20 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 160 680 0 0 {name=NR model=N W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 650 0 0 {name=L21 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 680 0 0 {name=L22 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 710 0 0 {name=L23 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 680 0 0 {name=L24 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 530 680 0 0 {name=OUT model=N W="20u" L="2.4u" nf=1 mult="1" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 650 0 0 {name=L25 lab=output}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 510 680 0 0 {name=L26 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 710 0 0 {name=L27 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 680 0 0 {name=L28 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 900 680 0 0 {name=LOAD model=P W="100u" L="3.2u" nf=1 mult="1" ad="'(100u)*4.5u'" as="'(100u)*4.5u'" pd="'2*(100u)+9u'" ps="'2*(100u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 710 0 0 {name=L29 lab=output}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 680 0 0 {name=L30 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 650 0 0 {name=L31 lab=lp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 680 0 0 {name=L32 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 680 0 0 {name=EN model=P W="30u" L=".8u" nf=1 mult="1" ad="'(30u)*4.5u'" as="'(30u)*4.5u'" pd="'2*(30u)+9u'" ps="'2*(30u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 710 0 0 {name=L33 lab=lp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 680 0 0 {name=L34 lab=disabled}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 650 0 0 {name=L35 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 680 0 0 {name=L36 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1640 680 0 0 {name=COMP model=P W="20u" L="101.35u" nf=1 mult="5" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 710 0 0 {name=L37 lab=output}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 680 0 0 {name=L38 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 650 0 0 {name=L39 lab=output}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 680 0 0 {name=L40 lab=output}
C {./icm_switch.sym} 160 1180 0 0 {name=XR}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 1100 0 0 {name=L41 lab=output}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 1140 0 0 {name=L42 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 1180 0 0 {name=L43 lab=disabled}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 1220 0 0 {name=L44 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 1260 0 0 {name=L45 lab=vss}
