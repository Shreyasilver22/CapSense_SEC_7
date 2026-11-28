v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -30 70 -30 240 {
lab=In}
N 30 70 60 70 {
lab=Out}
N 60 70 60 240 {
lab=Out}
N 30 240 60 240 {
lab=Out}
N -0 70 0 80 {
lab=VSS1}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/nmos4_n_cp8d.sym} 0 50 1 0 {name=M1
ad=7.75e-12
as=7.75e-12
pd=1.12e-05
ps=1.12e-05
nrd=0.72
nrs=0.72
W=2.5u
L=0.8u
nf=1 
mult=1
hide_texts="true"
sa=0 sb=0 sd=0
model=n
spiceprefix=M
}
C {/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/xschem/scl_pcell/pmos4_p_cp8d.sym} 0 260 3 0 {name=M2
ad=1.395e-11
as=1.395e-11
pd=1.52e-05
ps=1.52e-05
nrd=0.4
nrs=0.4
W=4.5u
L=0.8u
nf=1
mult=1
hide_texts="true"
sa=0 sb=0 sd=0
model=p
spiceprefix=M
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 60 160 0 0 {name=p2 lab=Out
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -30 155 0 0 {name=p1 lab=In}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 0 280 0 0 {name=p4 lab=phibar

}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 0 30 0 0 {name=p3 lab=phi
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 0 80 1 0 {name=p6 lab=VSS1
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 0 240 3 0 {name=p5 lab=VDD


}
