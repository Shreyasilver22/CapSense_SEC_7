# SCL08 input common-mode correction (ICMC)

The controller keeps the average of the two OTA summing-node voltages near an external 2.5 V reference during late charge transfer. It is a separate on-chip block in the SC + OTA readout. It uses SCL08 NMOS and PMOS devices, CMOS transmission gates, MOS capacitor banks, and the P-poly resistor model.

Two differential pairs sum the input error currents while `sample` is high. A MOS capacitor stores the correction. During the next reset phase, a transmission gate copies it to the hold capacitor. A buffer and weighted driver apply the resulting correction through the two PMOS capacitor banks. The integrated design derives the sample phase from its single 10 kHz clock.

## Xschem

Add the absolute path to this `schematic/` directory to the project's `XSCHEM_LIBRARY_PATH`. Place `icm_cell08.sym`. Its editable hierarchy contains the error transconductor, transmission gates, and voltage buffer. For a standalone view, run from `ICMC/schematic`.

~~~sh
xschem --rcfile "$PWD/xschemrc" icm_cell08.sch
~~~

The schematic uses the installed Xschem `devices/` library. Set `XSCHEM_SYSTEM_LIBRARY` to its parent directory if the standard Linux location differs.

## SPICE interface

Include the local SCL08 5 V MOS (`N`, `P`) and P-poly (`RPP`) cards plus [icm_scl08.spice](models/icm_scl08.spice). The clock model in the integrated readout already declares `inv08`. For another host that needs the inverter, include [inv08.spice](models/inv08.spice) once. For the editable hierarchy, Xschem emits the ICMC subcircuits. For a hand-written bench, include the standalone ICMC model.

~~~spice
XICM sump sumn vref phi1 phi1b phit phitb phi2 vdd 0 sample sampleb cm_x cm_hold accum icm_cell08
~~~

| Pins | Purpose |
| --- | --- |
| `sump`, `sumn` | OTA summing nodes that the controller senses and corrects |
| `ref` | Input common-mode reference, 2.5 V in the integrated design |
| `phi1`, `phi1b` | Reset/hold sampling phase and its complement |
| `phit`, `phitb` | RX transfer phase and its complement |
| `phi2` | TX discharge phase |
| `vdd`, `vss` | Supply and return |
| `sample`, `sampleb` | Late update window and its complement |
| `cm_x`, `cm_hold`, `accum` | Internal correction, hold, and integration nodes exposed for simulation |

Use separate unloaded internal nets for the three monitor nodes. Default parameters are `mi=9` integrator units and `drive_w=40` correction MOS capacitor units per branch. The feedback capacitor bank is a separate element of the host SC circuit.

The [integrated testbench](../Fully_Integrated_Design/transistor_level_icmc) drives the phases and records startup, sensitivity and power. Nominal transistor-level verification used ngspice 42. Full-chip layout and extraction, mismatch, and sampled noise checks remain open.
