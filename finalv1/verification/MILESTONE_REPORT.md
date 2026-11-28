# Current CapSense implementation status

Updated 2026-11-28T11:10:55+00:00. **The connected layout is complete; tapeout electrical qualification is incomplete.** Optional placement/routing experiments are not selected.

## One selected layout

`/home/shreyas/Desktop/Sec_7/intergrate_gds/post_layout/manual_rule_clean_chip/CapSense_ASIC_ROUTED.gds`

- Whole-chip installed SCL DRC: **0 violations**.
- Whole-chip installed SCL LVS: **match**.
- Supplemental core checks: **no via-over-poly, via-over-contact or via-cut diffusion-edge overlaps**. These checks exclude the supplied padframe and ID; they do not replace all manual rules.
- Original analog circuits and transistor channel dimensions retained. The digital counter was remapped to avoid native cell types with forbidden via-over-poly geometry; its routed logic is formally equivalent to the unchanged RTL (**21 checks proven, 0 unproven**).
- Supplied 4 mm standard padframe and OS0223 physical mark retained. The current top is `CapSense_ASIC_CONNECTED`; final OS0223 naming/submission handling is not released.

GDS SHA256: `5006fc3c9b7107d935bbd16b5e139559dc34e84df2084e198679afa68037366a`. Reference SHA256: `70037fac601382d48fe318b5aa8216619839cf275877f2f3ca7a45b14eac6e72`. Verification files are next to the GDS. Analog references are unchanged; the digital gate-level reference follows the formally checked replacement mapping.

## Stage reached

| Milestone | Completed evidence | Remaining qualification |
|---|---|---|
| A — Extraction | Approved isolated Magic 8.3.579 reproduces all seven supplied inverter resistors and its delay. Four-terminal/bulk/geometry repairs verified. The contact-corrected 5 nm analog view has 402/402 reconstructed MOS devices, no connectivity/bulk mismatch and no negative distributed-node C. | Full pad/ESD coverage and validated distributed coupling/RC model. Current comparison uses explicit distributed R with original lumped C. |
| B — Physical layout | Selected whole-chip DRC/LVS/manual-overlap checks pass. ABBA input pair, 3 um power routes and custom contact-grid correction implemented. | Electrical acceptance of parasitic imbalance and dynamic power integrity. |
| C — Electrical tests | Nominal native mapped-counter test completed 110 us with all seven actual gate fanouts: **PASS**. Both 310 us analog-partition comparisons completed. Restarted readout samples reproduce continuous-run samples within 4 uV. | Settled sensitivity, reset recovery, full routed TG-terminal clock tests, full analog PVT and sampled noise. The 310 us data are still startup, not settled sensitivity. |
| D — Tapeout signoff | Supplied SCL documents and available limits audited; individual results retained. | **NOT PASSED.** Unsupported or unrun checks remain unqualified. |

## Checks currently completing

- `qualified_counter_slow_4p5V_85C`: finished, last reported 109.9 us; functional screen PASS.
- `qualified_counter_fast_5p5V_m20C`: finished, last reported 110.0 us; functional screen PASS.
- `checkpoint_validation/pre_continue_periodic_cycle3`: finished, last reported 99.8 us.

The nominal counter load screen uses native transistor cells with source/drain load nodes fixed at 2.5 V and a local syntax-only PMOS model translation. It excludes wire RC and complete analog feedback; it is not a full-chip post-route clock pass.

## Material findings

- **Model parsing:** ngspice ignores the supplied PMOS `CGS0/CGD0/CGB0` tokens and separated UC minus sign. Project-local trials translate these to supported syntax; installed PDK files remain unchanged. Vendor-only unsupported flags still require model qualification.
- **Pad capacitance:** original diode `CJA/PBSW` syntax gives zero area-junction capacitance in ngspice. A local `CJO/PHP` translation gives **1.629 pF at 2.5 V, 1 MHz** for the native analog pad. Perimeter factors are omitted in the supplied CDL, and pad metal/routing capacitance is additional. This is a unit screen, not complete pad/ESD qualification. It must be included before final sensor sensitivity is accepted.
- **MOS feedback capacitance:** the actual bank is five W=20 um, L=38.005 um devices. Its nominal-model C changes from **7.579 pF at Vgate−Vbody=0 V** to **1.806 pF at −0.5 V**. Area alone does not define its operating capacitance. Ten process/temperature unit cases completed; these are not full-chip PVT or noise results.
- **Power:** a predecessor analog-only RC screen observed about **5.5 mV VDD drop and 14.7 mV ground rise** at saved 250 ns sample times. Native counter mean supply current was **7.11 uA**, with a **4.79 mA** switching peak in its separate ideal-supply load test. These separate results do not establish combined dynamic IR/EM safety.
- **Available limits:** SCL CSCB03002Y gives M1 **1.5 mA/um**, M2 **2.5 mA/um**. Separate via-current, antenna and reliability criteria and a qualified periodic-noise workflow are not available from the supplied files. The user confirmed there are no additional files/tools. These checks cannot be invented or marked passed.
- **CM_X:** the previously deferred undershoot remains a reliability item. It has not been waived by a foundry check.

## What is not being claimed

No settled sensitivity or equivalent-pressure noise result is accepted yet. The completed analog comparison is a documented RTL-driven analog partition, not a full-chip transistor/pad/RC signoff run. Deterministic switching ripple is not device noise. The supplied-library/ID grid exceptions, final top-cell naming and submission package are not signed off.

Original RTL, original baseline GDS, source analog schematics and installed PDK are preserved. See `flow_completion/preservation_check.json`, `qualified_digital/reports/routed_equivalence.log`, the selected layout's `verification_status.json`, and `flow_completion/` for exact decks, snapshots and logs. Earlier experiments remain as history, not alternative current deliverables.
