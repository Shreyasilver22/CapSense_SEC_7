.include "../models/scl08_tg.spice"
.include "../../models/scl08_models.inc"
.include "../../models/ota_cm2p5_C.spice"
.param CP=7p CN=5p CF=40p
.temp 27
.options reltol=1e-5 vntol=1e-8 abstol=1e-12 numdgt=12 method=gear maxord=2
VPHI1 phi1 0 PULSE(5 0 41u 1000n 1000n 58u 100u)
VPHI2 phi2 0 PULSE(0 5 46u 1000n 1000n 43u 100u)
B1 phi1b 0 V=5-v(phi1)
B2 phi2b 0 V=5-v(phi2)
CLP outp 0 5p
CLN outn 0 5p
VPHIT phit 0 PULSE(0 5 45u 1000n 1000n 44u 100u)
BT phitb 0 V=5-v(phit)
VBN vbn 0 3
VBP vbp vdd -2.2
IREF vdd bias 3.5u
.control
set wr_singlescale
set wr_vecnames
op
print v(outp) v(outn) v(sump) v(sumn) i(vdd)
tran 20n 500u
wrdata transient.dat v(outp) v(outn) v(sump) v(sumn) v(phi1) v(phi2) v(txp) v(rxp) v(txn) v(rxn) i(vdd)
write sc_cmfb.raw v(outp) v(outn) v(sump) v(sumn) v(phi1) v(phi2) v(phit) v(txp) v(rxp)
quit
.endc
