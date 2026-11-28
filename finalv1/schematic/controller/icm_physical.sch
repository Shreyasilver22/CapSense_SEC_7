v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {icm_physical - SCL transistor implementation} 0 -100 0 0 .5 .5 {}
T {Node labels connect equal names. Open child symbols to inspect their transistors.} 0 -60 0 0 .25 .25 {}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 0 0 0 {name=P0 lab=sump}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 60 0 0 {name=P1 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 120 0 0 {name=P2 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 180 0 0 {name=P3 lab=vss}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 240 0 0 {name=P4 lab=vref}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 300 0 0 {name=P5 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 360 0 0 {name=P6 lab=phit}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 420 0 0 {name=P7 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 480 0 0 {name=P8 lab=sample_en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 540 0 0 {name=P9 lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 50 -20 0 0 {name=CONTROLLER_VALUES only_toplevel=false value=".param CINT_L=506.75u CINT_M=5 ERR_W=160u ERR_L=4.8u"}
C {./native_rpp.sym} 160 180 0 0 {name=XRB W=2.4u L=85714.285u}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 180 0 0 {name=L1 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 180 0 0 {name=L2 lab=nb}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 530 180 0 0 {name=B model=N W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 150 0 0 {name=L3 lab=nb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 510 180 0 0 {name=L4 lab=nb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 210 0 0 {name=L5 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 180 0 0 {name=L6 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 900 180 0 0 {name=NB model=N W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 150 0 0 {name=L7 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 180 0 0 {name=L8 lab=nb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 210 0 0 {name=L9 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 180 0 0 {name=L10 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 180 0 0 {name=PB model=P W="20u" L="3.2u" nf=1 mult="1" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 210 0 0 {name=L11 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 180 0 0 {name=L12 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 150 0 0 {name=L13 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 180 0 0 {name=L14 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 1640 180 0 0 {name=AVG_P model=N W="2.5u" L="50u" nf=1 mult="1" ad="'(2.5u)*4.5u'" as="'(2.5u)*4.5u'" pd="'2*(2.5u)+9u'" ps="'2*(2.5u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 150 0 0 {name=L15 lab=sump}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 180 0 0 {name=L16 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 210 0 0 {name=L17 lab=sense}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 180 0 0 {name=L18 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 160 680 0 0 {name=AVG_N model=N W="2.5u" L="50u" nf=1 mult="1" ad="'(2.5u)*4.5u'" as="'(2.5u)*4.5u'" pd="'2*(2.5u)+9u'" ps="'2*(2.5u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 650 0 0 {name=L19 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 680 0 0 {name=L20 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 710 0 0 {name=L21 lab=sense}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 680 0 0 {name=L22 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 530 680 0 0 {name=ERRTAIL model=P W="50u" L="3.2u" nf=1 mult="1" ad="'(50u)*4.5u'" as="'(50u)*4.5u'" pd="'2*(50u)+9u'" ps="'2*(50u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 710 0 0 {name=L23 lab=tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 510 680 0 0 {name=L24 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 650 0 0 {name=L25 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 680 0 0 {name=L26 lab=vdd}
C {./icm_inv.sym} 900 680 0 0 {name=XSE}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 620 0 0 {name=L27 lab=sample_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 660 0 0 {name=L28 lab=sample_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 700 0 0 {name=L29 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 740 0 0 {name=L30 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 680 0 0 {name=ERR_L model=P W="\{ERR_W\}" L="\{ERR_L\}" nf=1 mult="1" ad="'(\{ERR_W\})*4.5u'" as="'(\{ERR_W\})*4.5u'" pd="'2*(\{ERR_W\})+9u'" ps="'2*(\{ERR_W\})+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 710 0 0 {name=L31 lab=err_left}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 680 0 0 {name=L32 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 650 0 0 {name=L33 lab=tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 680 0 0 {name=L34 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1640 680 0 0 {name=ERR_R model=P W="\{ERR_W\}" L="\{ERR_L\}" nf=1 mult="1" ad="'(\{ERR_W\})*4.5u'" as="'(\{ERR_W\})*4.5u'" pd="'2*(\{ERR_W\})+9u'" ps="'2*(\{ERR_W\})+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 710 0 0 {name=L35 lab=err_right}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 680 0 0 {name=L36 lab=sense}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 650 0 0 {name=L37 lab=tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 680 0 0 {name=L38 lab=vdd}
C {./native_rpp.sym} 160 1180 0 0 {name=XPC1 W=2.4u L=8571.43u}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 1180 0 0 {name=L39 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 1180 0 0 {name=L40 lab=pcas}
C {./native_rpp.sym} 530 1180 0 0 {name=XPC2 W=2.4u L=17142.855u}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 1180 0 0 {name=L41 lab=pcas}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 1180 0 0 {name=L42 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 900 1180 0 0 {name=ERRCL model=P W="40u" L="10u" nf=1 mult="1" ad="'(40u)*4.5u'" as="'(40u)*4.5u'" pd="'2*(40u)+9u'" ps="'2*(40u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 1210 0 0 {name=L43 lab=left}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 1180 0 0 {name=L44 lab=pcas}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 1150 0 0 {name=L45 lab=err_left}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 1180 0 0 {name=L46 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 1180 0 0 {name=ERRCR model=P W="40u" L="10u" nf=1 mult="1" ad="'(40u)*4.5u'" as="'(40u)*4.5u'" pd="'2*(40u)+9u'" ps="'2*(40u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 1210 0 0 {name=L47 lab=error_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 1180 0 0 {name=L48 lab=pcas}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 1150 0 0 {name=L49 lab=err_right}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 1180 0 0 {name=L50 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 1640 1180 0 0 {name=NERR_L model=N W="125u" L="20u" nf=1 mult="1" ad="'(125u)*4.5u'" as="'(125u)*4.5u'" pd="'2*(125u)+9u'" ps="'2*(125u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 1150 0 0 {name=L51 lab=left}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 1180 0 0 {name=L52 lab=left}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 1210 0 0 {name=L53 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 1180 0 0 {name=L54 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 160 1680 0 0 {name=NERR_R model=N W="125u" L="20u" nf=1 mult="1" ad="'(125u)*4.5u'" as="'(125u)*4.5u'" pd="'2*(125u)+9u'" ps="'2*(125u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 1650 0 0 {name=L55 lab=error_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 1680 0 0 {name=L56 lab=left}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 1710 0 0 {name=L57 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 1680 0 0 {name=L58 lab=vss}
C {./icm_switch.sym} 530 1680 0 0 {name=XSAMPLE}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 1600 0 0 {name=L59 lab=error_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 1640 0 0 {name=L60 lab=vint}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 1680 0 0 {name=L61 lab=sample_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 1720 0 0 {name=L62 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 1760 0 0 {name=L63 lab=vss}
C {./icm_switch.sym} 900 1680 0 0 {name=XDUMP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 1600 0 0 {name=L64 lab=error_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 1640 0 0 {name=L65 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 1680 0 0 {name=L66 lab=sample_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 1720 0 0 {name=L67 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 1760 0 0 {name=L68 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 1680 0 0 {name=CINT model=P W="20u" L="\{CINT_L\}" nf=1 mult="\{CINT_M\}" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 1710 0 0 {name=L69 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 1680 0 0 {name=L70 lab=vint}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 1650 0 0 {name=L71 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 1680 0 0 {name=L72 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1640 1680 0 0 {name=CHOLD model=P W="20u" L="101.35u" nf=1 mult="5" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 1710 0 0 {name=L73 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 1680 0 0 {name=L74 lab=cm_hold}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 1650 0 0 {name=L75 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 1680 0 0 {name=L76 lab=vdd}
C {./icm_switch.sym} 160 2180 0 0 {name=XHOLD}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2100 0 0 {name=L77 lab=vint}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2140 0 0 {name=L78 lab=cm_hold}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2180 0 0 {name=L79 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2220 0 0 {name=L80 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2260 0 0 {name=L81 lab=vss}
C {./icm_inv.sym} 530 2180 0 0 {name=XRINV}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2120 0 0 {name=L82 lab=rst_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2160 0 0 {name=L83 lab=reset_active}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2200 0 0 {name=L84 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2240 0 0 {name=L85 lab=vss}
C {./icm_switch.sym} 900 2180 0 0 {name=XINIT}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2100 0 0 {name=L86 lab=vint}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2140 0 0 {name=L87 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2180 0 0 {name=L88 lab=reset_active}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2220 0 0 {name=L89 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2260 0 0 {name=L90 lab=vss}
C {./icm_switch.sym} 1270 2180 0 0 {name=XINITH}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2100 0 0 {name=L91 lab=cm_hold}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2140 0 0 {name=L92 lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2180 0 0 {name=L93 lab=reset_active}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2220 0 0 {name=L94 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2260 0 0 {name=L95 lab=vss}
C {./icm_nor.sym} 1640 2180 0 0 {name=XRN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2100 0 0 {name=L96 lab=phi1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2140 0 0 {name=L97 lab=reset_active}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2180 0 0 {name=L98 lab=reset_bar}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2220 0 0 {name=L99 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2260 0 0 {name=L100 lab=vss}
C {./icm_inv.sym} 160 2680 0 0 {name=XRI}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2620 0 0 {name=L101 lab=reset_bar}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2660 0 0 {name=L102 lab=reset_all}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2700 0 0 {name=L103 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 2740 0 0 {name=L104 lab=vss}
C {./icm_sr.sym} 530 2680 0 0 {name=XL1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2580 0 0 {name=L105 lab=phit}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2620 0 0 {name=L106 lab=reset_all}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2660 0 0 {name=L107 lab=e1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2700 0 0 {name=L108 lab=e1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2740 0 0 {name=L109 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 2780 0 0 {name=L110 lab=vss}
C {./icm_sr.sym} 900 2680 0 0 {name=XL2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2580 0 0 {name=L111 lab=phi2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2620 0 0 {name=L112 lab=reset_all}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2660 0 0 {name=L113 lab=e2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2700 0 0 {name=L114 lab=e2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2740 0 0 {name=L115 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 2780 0 0 {name=L116 lab=vss}
C {./icm_nand.sym} 1270 2680 0 0 {name=XPREN}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2600 0 0 {name=L117 lab=e1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2640 0 0 {name=L118 lab=e2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2680 0 0 {name=L119 lab=pre_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2720 0 0 {name=L120 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 2760 0 0 {name=L121 lab=vss}
C {./icm_inv.sym} 1640 2680 0 0 {name=XPREI}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2620 0 0 {name=L122 lab=pre_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2660 0 0 {name=L123 lab=pre}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2700 0 0 {name=L124 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 2740 0 0 {name=L125 lab=vss}
C {./icm_buffer.sym} 160 3180 0 0 {name=XCOMMANDBUF}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3060 0 0 {name=L126 lab=cm_hold}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3100 0 0 {name=L127 lab=held_buffer}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3140 0 0 {name=L128 lab=nb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3180 0 0 {name=L129 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3220 0 0 {name=L130 lab=e1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3260 0 0 {name=L131 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3300 0 0 {name=L132 lab=vss}
C {./icm_switch.sym} 530 3180 0 0 {name=XTOP}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3100 0 0 {name=L133 lab=held_buffer}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3140 0 0 {name=L134 lab=rt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3180 0 0 {name=L135 lab=e1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3220 0 0 {name=L136 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3260 0 0 {name=L137 lab=vss}
C {./native_rpp.sym} 900 3180 0 0 {name=XRT W=2.4u L=5485.715u}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 840 3180 0 0 {name=L138 lab=rt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 960 3180 0 0 {name=L139 lab=mix}
C {./native_rpp.sym} 1270 3180 0 0 {name=XRBOT W=2.4u L=11657.145u}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1210 3180 0 0 {name=L140 lab=mix}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1330 3180 0 0 {name=L141 lab=rb}
C {./icm_switch.sym} 1640 3180 0 0 {name=XBOTTOM}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 3100 0 0 {name=L142 lab=rb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 3140 0 0 {name=L143 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 3180 0 0 {name=L144 lab=pre}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 3220 0 0 {name=L145 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1490 3260 0 0 {name=L146 lab=vss}
C {./icm_switch.sym} 160 3680 0 0 {name=XBYPASS}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3600 0 0 {name=L147 lab=held_buffer}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3640 0 0 {name=L148 lab=mix}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3680 0 0 {name=L149 lab=e2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3720 0 0 {name=L150 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 3760 0 0 {name=L151 lab=vss}
C {./icm_switch.sym} 530 3680 0 0 {name=XMIXRESET}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3600 0 0 {name=L152 lab=mix}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3640 0 0 {name=L153 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3680 0 0 {name=L154 lab=e1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3720 0 0 {name=L155 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 3760 0 0 {name=L156 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 900 3680 0 0 {name=BTAIL model=P W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 3710 0 0 {name=L157 lab=bt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 3680 0 0 {name=L158 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 3650 0 0 {name=L159 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 3680 0 0 {name=L160 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 3680 0 0 {name=BL model=P W="8u" L="2.4u" nf=1 mult="1" ad="'(8u)*4.5u'" as="'(8u)*4.5u'" pd="'2*(8u)+9u'" ps="'2*(8u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 3710 0 0 {name=L161 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 3680 0 0 {name=L162 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 3650 0 0 {name=L163 lab=bt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 3680 0 0 {name=L164 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1640 3680 0 0 {name=BR model=P W="8u" L="2.4u" nf=1 mult="1" ad="'(8u)*4.5u'" as="'(8u)*4.5u'" pd="'2*(8u)+9u'" ps="'2*(8u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 3710 0 0 {name=L165 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 3680 0 0 {name=L166 lab=mix}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 3650 0 0 {name=L167 lab=bt}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 3680 0 0 {name=L168 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 160 4180 0 0 {name=BNL model=N W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 4150 0 0 {name=L169 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 4180 0 0 {name=L170 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 4210 0 0 {name=L171 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 4180 0 0 {name=L172 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 530 4180 0 0 {name=BNR model=N W="10u" L="3.2u" nf=1 mult="1" ad="'(10u)*4.5u'" as="'(10u)*4.5u'" pd="'2*(10u)+9u'" ps="'2*(10u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 4150 0 0 {name=L173 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 510 4180 0 0 {name=L174 lab=bl}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 4210 0 0 {name=L175 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 4180 0 0 {name=L176 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 900 4180 0 0 {name=OUT model=N W="20u" L="2.4u" nf=1 mult="1" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 4150 0 0 {name=L177 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 4180 0 0 {name=L178 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 4210 0 0 {name=L179 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 4180 0 0 {name=L180 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 4180 0 0 {name=LOAD model=P W="100u" L="3.2u" nf=1 mult="1" ad="'(100u)*4.5u'" as="'(100u)*4.5u'" pd="'2*(100u)+9u'" ps="'2*(100u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 4210 0 0 {name=L181 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 4180 0 0 {name=L182 lab=pb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 4150 0 0 {name=L183 lab=lp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 4180 0 0 {name=L184 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1640 4180 0 0 {name=LOADEN model=P W="30u" L=".8u" nf=1 mult="1" ad="'(30u)*4.5u'" as="'(30u)*4.5u'" pd="'2*(30u)+9u'" ps="'2*(30u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 4210 0 0 {name=L185 lab=lp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 4180 0 0 {name=L186 lab=e1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 4150 0 0 {name=L187 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 4180 0 0 {name=L188 lab=vdd}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 160 4680 0 0 {name=COMP model=P W="20u" L="101.35u" nf=1 mult="5" ad="'(20u)*4.5u'" as="'(20u)*4.5u'" pd="'2*(20u)+9u'" ps="'2*(20u)+9u'" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 4710 0 0 {name=L189 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 4680 0 0 {name=L190 lab=gain}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 4650 0 0 {name=L191 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 4680 0 0 {name=L192 lab=cm_x}
C {./icm_switch.sym} 530 4680 0 0 {name=XOUTRESET}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 4600 0 0 {name=L193 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 4640 0 0 {name=L194 lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 4680 0 0 {name=L195 lab=e1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 4720 0 0 {name=L196 lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 4760 0 0 {name=L197 lab=vss}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 900 4680 0 0 {name=CORRP model=P W="20u" L="10u" nf=1 mult="40" ad="90p" as="90p" pd="49u" ps="49u" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 4710 0 0 {name=L198 lab=sump}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 4680 0 0 {name=L199 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 4650 0 0 {name=L200 lab=sump}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 4680 0 0 {name=L201 lab=sump}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 1270 4680 0 0 {name=CORRN model=P W="20u" L="10u" nf=1 mult="40" ad="90p" as="90p" pd="49u" ps="49u" nrd=0 nrs=0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 4710 0 0 {name=L202 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 4680 0 0 {name=L203 lab=cm_x}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 4650 0 0 {name=L204 lab=sumn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1290 4680 0 0 {name=L205 lab=sumn}
