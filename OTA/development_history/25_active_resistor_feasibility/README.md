# 25_active_resistor_feasibility: MOS active-resistor feasibility

Development order: **25**. Date / ordering evidence: **1 November, after CMFB revision 2 2026**.

Direct NMOS / complementary substitutions simulated; corner failures prevent replacing the verified poly network. No active-resistor layout.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `architecture_exploration_20261031/active_resistor_study_20261101/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# MOS active-resistor feasibility — 1 November 2026

MOSFET voltage-controlled resistors were actually simulated with the native SCL08 models in ngspice. The verified poly-resistor OTA design was not changed. This study tests a direct MOS substitution in its CMFB averaging network; it does not claim that all active-resistor topologies are unsuitable.

## What was tested

- Single NMOS in triode, gateVDD, bodyVSS.
- Parallel NMOS/PMOS resistor: gatesVDD/VSS, bodiesVSS/VDD. PMOS multiplicities1,2,4,8,16,24,32,40,48,64 were investigated. Both resistor branches use identical devices.
- UnitW2.5 um and length tuned to a differential resistance of200 kohm at terminal common-mode1.3359 V, VDD5 V,27 C, typical native model. The NMOS length is**51.218 um**. The best nominal common-mode cancellation in the explored set uses**one NMOS plus40 PMOS units per branch**, with length**51.218 um**. It is not a simple equal-size transmission gate.
- Full existing200 kohm RPP capacitance-extracted OTA as reference; a separate bank-parasitic-free200 kohm RPP model as a diagnostic.

All MOS variants are approximately200 kohm at the calibration point. That does not make them constant200 kohm components over their operating range. Effective resistance changes with both terminal voltages, gate overdrive, body effect and process/temperature. Consequently equal geometries in the two averaging branches can have unequal effective resistance when the outputs differ. The sensed voltage then differs from the arithmetic mean. The tuned complementary network can partly cancel this error at nominal conditions, but its P/N tracking changes across corners.

## Measured CMFB results

Nominal endpoints here mean commanded differential output plus/minus1.6 V at5 V/27 C; the full nominal sweep covers−2 to+2 V. The selected corner grid uses the same five native MOS files for every variant,4.5/5.5 V,0/85 C, and balanced or opposite-polarity differential levels covering SC integration/reset endpoints. CL5 pF per output. Native RPP corner remains typical for the reference; these selected cases are not the full prior1442-case qualification grid.

| CMFB averaging element | Nominal endpoint CM error (mV) | Worst screened CM error (mV) | Lowest CMFB margin |
|---|---:|---:|---:|
| Existing 200k RPP layout | 20.67 | 53.55 | 68.11 deg |
| Single NMOS resistor | 106.35 | 255.93 | 81.47 deg |
| Tuned complementary MOS resistor | 1.43 | 658.61 | 39.28 deg |

The complementary cell looks excellent at the nominal calibration range but reaches roughly0.66 V output-common-mode error in a selected corner and falls below the previous60-degree margin target. The single NMOS keeps adequate loop margin in this screen, but biases the common-mode average substantially. Thus **neither simple cell is accepted as a drop-in replacement** for the current verified200 kohm poly network.

`signal_range.json` and `corner_screen.json` include `averaging_error_mV`, the direct sensed-node deviation from `(SP+SM)/2`, separately from the OTA's output-common-mode error. The reference includes pre-existing sensing-buffer nonlinearity; a small output-common-mode error alone does not prove a linear resistor or an exact averaging function.

## SC checks

The original SC topology and stimulus remain unchanged:CS2.5 pF,CF7.5 pF,VREF1.5 V,VP0.3 V,50 kHz,3 cycles per frame, two frames,5 pF per output. Transistor switch sizes and clocks are unchanged. Both actual transistor switches and the prior smoothly controlled100-ohm diagnostic were tested with Gear integration.

Nominal transistor-switch SC sampled common-mode errors are about24.8 mV for the poly reference,94.9 mV for the single NMOS and24.1 mV for the tuned complementary cell. A nominal waveform therefore does not reject the complementary cell by itself. Additional nativebnbp49_5v,5.5 V tests reveal roughly264 mV CM error at0 C and375 mV at85 C for the complementary version, versus approximately11/13 mV for the poly reference. Raw output error can partially cancel against switching error; a smaller raw offset is not proof of improved common-mode regulation or calibrated accuracy.

SC simulations saved:22; completed:21; numerical failures:1. The single-NMOS/native-switch case atwnbp49_5v,5.5 V,0 C did not complete, and no valid result is claimed for it. Inspect its raw log for the convergence failure. Other cases and their six sampled values are in`SC_comparison.json`.

## Model scope and area interpretation

This is a **hybrid electrical preview**, not a new post-layout MOS-resistor result. The existing OTA's extracted core/controller capacitances are retained. The old poly-resistor bank resistances and capacitances touching resistor-only internal nodes are removed, and MOS channel/intrinsic capacitances plus estimated junction geometry are inserted. Remaining old metal capacitances at the three retained endpoints remain. `verification/replacement.json` records the endpoint mapping and removal counts. The bank-parasitic-free RPP control preserves the reference DC result, providing a check on the replacement operation.

No active-resistor GDS, DRC, LVS or new extraction was performed. Estimated gate-channel area is about128.0 um2 per NMOS branch or5249.9 um2 for the40-PMOS complementary branch. Those are channel areas only, excluding wells, contacts and routing; they are not total layout areas or measured parasitic improvements. Long-channel MOS model accuracy near51 um has not been validated against characterization or foundry geometry limits. Supply-noise coupling, mismatch, resistor noise, reference loading and final ASIC specifications remain unqualified. Existing native-model/ngspice translation and engineering C-extraction limitations carry over.

## Conclusion

MOS-based resistance is a reasonable area-reduction experiment. The simulated rail-gated cells need linearization, bias/process tracking or trimming before replacing this CMFB network. Keep the verified poly implementation as the reference for now. A different linearized MOS cell or clocked CMFB is a further design task; this study does not establish its performance.

## Files and reproduction

- `models/active_resistor_cells.spice`: standalone four-terminal nominal-only element definitions, pins`A B VDD VSS`; nativeN/P cards must be supplied by the user. Their resistance is not independently value-programmable or guaranteed200 kohm.
- `models/nmos.spice`, `complementary_40.spice`: OTA hybrid previews; `reference_layout_C.spice`: unchanged physical reference. Include one OTA variant at a time because they share the same subcircuit name.
- `tb/nmos.cir`, `complementary_40.cir`, `reference_layout_C.cir`: nominal native-switch SC tests. Run from`tb`, for example`ngspice -b -o nmos.log nmos.cir`. PDK remains at`/home/berson_meshak/pdk/scl08/ngspice_models49`; no native cards were copied here.
- Regenerate with`scripts/study.py`, then`qualify.py`, `additional.py`, `report.py`. Raw decks retain their original execution paths; regenerate after relocation. `scripts/sweep.py` and`sc_simulate.py` retain the previous study's measurement helpers; their standalone old sweep entry points are not this study's reproduction interface.
- `plots/bias_and_averaging.png`, `corner_comparison.png`, `SC_corner.png`, plus PDF copies.
- `candidates.json`, `iv_curves.json`, `cmfb_nominal.json`, `signal_range.json`, `corner_screen.json`, `SC_comparison.json` and raw logs preserve the conditions and results. The original verified OTA/SC design was not overwritten or published.
