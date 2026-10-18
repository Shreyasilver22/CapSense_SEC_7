#!/usr/bin/env bash
set -euo pipefail

cat > scl_pmos_transfer_sweep.spice <<'SPICE'
SCL CP8D PMOS Transfer Characteristics
.lib /home/berson_meshak/pdk/scl08/ngspice_models49/header.lib NOM

VDD s 0 5
VG g 0 5
VD d 0 4.5
MP1 d g s s P W=2.5u L=0.8u

.control
* VSD = 0.5 V
alter VD = 4.5
dc VG 5 0 -0.05
let vsg = 5-v(g)
let idp = abs(i(VD))
wrdata /tmp/scl_pmos_transfer_vsd_0p5.dat vsg idp

* VSD = 1 V
alter VD = 4
dc VG 5 0 -0.05
let vsg = 5-v(g)
let idp = abs(i(VD))
wrdata /tmp/scl_pmos_transfer_vsd_1.dat vsg idp

* VSD = 2 V
alter VD = 3
dc VG 5 0 -0.05
let vsg = 5-v(g)
let idp = abs(i(VD))
wrdata /tmp/scl_pmos_transfer_vsd_2.dat vsg idp

* VSD = 3 V
alter VD = 2
dc VG 5 0 -0.05
let vsg = 5-v(g)
let idp = abs(i(VD))
wrdata /tmp/scl_pmos_transfer_vsd_3.dat vsg idp

* VSD = 4 V
alter VD = 1
dc VG 5 0 -0.05
let vsg = 5-v(g)
let idp = abs(i(VD))
wrdata /tmp/scl_pmos_transfer_vsd_4.dat vsg idp

* VSD = 5 V
alter VD = 0
dc VG 5 0 -0.05
let vsg = 5-v(g)
let idp = abs(i(VD))
wrdata /tmp/scl_pmos_transfer_vsd_5.dat vsg idp

quit
.endc
.end
SPICE

ngspice -b scl_pmos_transfer_sweep.spice

mkdir -p /mnt/c/Users/HP/Final_Year_Project_Sim
cp /tmp/scl_pmos_transfer_vsd_*.dat /mnt/c/Users/HP/Final_Year_Project_Sim/

echo
echo "Done. Netlist: $(pwd)/scl_pmos_transfer_sweep.spice"
echo "Output data copied to /mnt/c/Users/HP/Final_Year_Project_Sim/"
