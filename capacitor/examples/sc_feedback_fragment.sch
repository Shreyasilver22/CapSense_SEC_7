v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {scl08_cap3.sym} 400 300 0 0 {name=XCFB value=2.5p}
C {devices/iopin.sym} 400 180 0 0 {name=p1 lab=SUM}
N 400 180 400 240 {lab=SUM}
C {devices/iopin.sym} 400 420 0 0 {name=p2 lab=VOUT}
N 400 360 400 420 {lab=VOUT}
C {devices/iopin.sym} 580 420 0 0 {name=p3 lab=VSUB}
N 480 360 580 360 {lab=VSUB}
N 580 360 580 420 {lab=VSUB}
T {C_FB connection fragment for the attached SC integrator} 100 40 0 0 0.4 0.4 {}
T {SUM = OTA inverting input after the phase-2 switch.
VOUT = OTA output. VSUB = substrate ground, not VREF.
Place reset switch across SUM and VOUT as in the figure.
2.5p is illustrative; capacitor roles are not yet assigned.
This fragment is not a complete SC integrator simulation.} 100 520 0 0 0.28 0.28 {}
