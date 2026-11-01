# 24_telescopic_cmfb_revision_2: Telescopic OTA with corrected CMFB

Development order: **24**. Date / ordering evidence: **1 November, after extracted failure 2026**.

Current verified telescopic prototype: local DRC/LVS pass, 1442 successful AC checks, minimum CMFB PM 63.75 degrees. C-extraction only, not full signoff.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `architecture_exploration_20261031/cmfb_revision_20261101/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Telescopic OTA — CMFB revision 2, 1 November 2026

The CMFB was redesigned, laid out, checked and actually re-simulated in ngspice with extracted capacitance. The revised model has stable nominal SC behavior and meets the previous60-degree feedback-loop screening target throughout the tested AC grid. This is an improved prototype, not a final optimum or tapeout-qualified ASIC design.

## What changed

- Averaging resistance: **1 Mohm ->200 kohm per branch**. Native SCL08 RPP geometry and electrical model retained.
- Sensing: replaced the PMOS source followers and PMOS bias branches with **four W20/L1.6 NMOS followers per channel and two W20/L3.2 NMOS sink units per channel**, roughly7 uA nominal per channel. These include a matched reference follower.
- Detector: PMOS differential error pair, with NMOS/PMOS current mirrors translating its output current into the high-voltage PC control node. The PMOS input pair usesW5/L2.4; mirror unitsW10/L3.2; its tail is approximately1 uA. This avoids requiring a low-voltage detector output to drivePC directly. It also avoids the large-area PMOS sensing/bias devices tested as an alternative.
- Compensation: **12 PMOS W20/L10 units fromPC to each output**, plus the existing four units fromPC toVDD. Controller current and compensation were selected together; this increases intentional output loading relative to the first8-unit prototype.
- Layout: shortened the resistor banks and placed the high-impedance detector near them. Resistors use40 sections per200 kohm bank, eachW2.4/L428.571 um. Signal-core transistor W/L, topology, IREF3.5 uA and external cascode bias values **remain unchanged**. The exported transistor schematic was separately checked againstGDS; `verification/views.json` records the unchanged nine signal-core devices.

Resistor/current/compensation trials, alternative PMOS headroom changes and NMOS sensing variants are preserved in their JSON/CSV records. The final choice is `selected.json`; rejected trial results are not qualification data for the final candidate. A clocked CMFB was not implemented because this continuous-time version recovered the stability target; it remains an alternative if final area/power requirements demand it.

## Physical and extraction results

| Item | Previous layout | Revised layout |
|---|---:|---:|
| Native RPP resistance, each branch |1 Mohm |200 kohm |
| Extracted engineering resistor-body ground C, both banks |53.18 pF |10.64 pF |
| GDS bounding area |2.586 mm2 |1.297 mm2 |
| Physical MOS units |43 |67 |
| RPP body sections |200 |80 |
| Nominal CMFB phase margin |−48.73 degrees |70.71 degrees |

New GDS is `layout/ota_telescopic_layout.gds`. **Local SCL DRC:0 markers. LVS:MATCH**, with wrong-gate and wrong-width negative controls failing as expected. The repaired C-extracted model separately matches the GDS topology. These checks use the original unmodified local KLayout decks. Bounding area is an unoptimized macro floorplan, not a minimum die-area claim; density, matching, pad/ESD and full-chip signoff remain outside this check.

The model `models/layout_C.spice` includes594 explicit capacitances and native80-section resistor bodies exported as160 half-resistors. Native tee export drops a half for this PDK rsubckt type; both halves are restored from `.ext` terminals and geometry and independently checked by LVS. Do not simulate `pex/ota_C_raw.spice` as if it were complete.

## Extracted feedback-loop screening

**1442 AC cases completed, with no execution failures.** Five literal native MOS corner files; VDD4.5/5/5.5 V; temperature0/27/85 C; native best/typ/worst resistor models. Initial grid checks both common-mode and differential loops, center operation with1/10 pF per output, and output differential levels that cover the3.3 V integration endpoint. Extra reset-range tests cover output1.5 V and its complementary output up to4 V at5.5 V supply, CL10 pF, both polarities. Nominal CL5 pF points are also saved.

- Lowest tested CMFB margin: **63.75 degrees**.
- Lowest tested differential-loop margin: **88.83 degrees**.
- Nominal matched-model differential gain: **88.44 dB**.
- Nominal differential UGF: **1.343 MHz**, CL5 pF on each output, input CM1.5 V and output CM2.5 V.

Every unity crossing is retained in the JSON and the minimum margin is used. CMFB is checked by symmetric sensing-gate injection with differential feedback closed. These are engineering loop diagnostics, not a formal multi-loop pole-count/Nyquist proof, continuous-range guarantee, or foundry-certified PVT qualification. The ranges remain project screening assumptions. Nominal frequency/gain figures describe the differential benchmark, not the bandwidth of the entire SC readout.

Static common-mode setpoint error reaches 61.34 mV at large output imbalance in the saved bias-point grid. Improved loop stability does not establish exact common-mode regulation; this residual must fit the future ADC/interface budget.

## Same SC circuit: measured behavior

CS2.5 pF,CF7.5 pF,VREF1.5 V,VP0.3 V, output and complementary-output loads5 pF, 50 us startup reset and two frames of three integration cycles. Capacitors, clock sequence/edges/nonoverlap, switch dimensions and sensor stimulus stay as before. Only the OTA macro is layout extracted; the SC network remains schematic-level. Ideal expected staircase:1.5->2.1->2.7->3.3 V.

Previous and revised extracted layouts were both run with the **same native transistor switches and Gear solver**. Prior worst sampled common-mode error was898.1 mV; revised nominal error is**24.80 mV**. Large common-mode oscillation is removed in the revised nominal trace. Gear does not hide the old instability: the previous layout still fails in that same-method control run.

| Condition | Switch control | Last third sample (V) | Worst sampled output error (mV) | Worst sampled CM error (mV) |
|---|---|---:|---:|---:|
| 5 V, 27 C, 50 kHz | smooth | 3.299797 | 0.203 | 21.531 |
| 5 V, 27 C, 50 kHz | tg | 3.356381 | 56.381 | 24.802 |
| 5 V, 27 C, 100 kHz | smooth | 3.297816 | 2.184 | 13.679 |
| 5 V, 27 C, 100 kHz | tg | 3.354131 | 54.131 | 15.938 |
| 5 V, 27 C, 200 kHz | smooth | 3.294740 | 5.276 | 13.292 |
| 5 V, 27 C, 200 kHz | tg | 3.350130 | 50.130 | 12.951 |
| 4.5 V, 85 C, 50 kHz | smooth | 3.298503 | 1.497 | 39.334 |
| 4.5 V, 85 C, 50 kHz | tg | 3.351207 | 51.210 | 43.100 |
| 5.5 V, 0 C, 50 kHz | smooth | 3.299938 | 0.062 | 11.855 |
| 5.5 V, 0 C, 50 kHz | tg | 3.361314 | 61.314 | 11.391 |

At nominal50 kHz, the smooth100-ohm diagnostic control gives worst sampled error**0.203 mV**. The actual transistor-switch test retains about**56.38 mV raw error**, dominated by switching/readout effects; the CMFB fix does not eliminate that error. Higher clocks still degrade settling: at100 kHz the smooth-control final error is about2.18 mV. At the selected4.5 V/85 C corner the50 kHz smooth-control error is about1.50 mV. No final accuracy or clock-rate requirement has been established.

With a+50 fF sensor change, expected third-sample change is36 mV. The2 ns native-switch runs give**35.994788 mV** after subtracting a matching2 ns zero-change run. This is offline baseline subtraction, not an implemented calibration circuit, ADC resolution claim or noise-limited sensitivity measurement.

Nominal modeled VDD power during SC operation is**232.9 uW**, compared with about181.8 uW for the earlier schematic telescopic prototype. Increased sensing current is a real power cost. The unstable old layout's average power is not a useful efficiency baseline. External reference/clock drivers and a fabricated current/voltage-reference generator are excluded. The footprint remains much larger than the earlier simple two-stage OTA; this CMFB revision does not establish that telescopic is the optimum overall ASIC architecture.

## Numerical and model limits

The abrupt ideal SW control with extracted capacitances aborts with a timestep-too-small error at the firstphi2 event, with both trapezoidal and Gear attempts. Initial failed records are retained under`verification/numerical_trials/SC_aborted_trap.json` and raw result directories; those are not counted as successful final SC tests. Transistor switches converge with second-order Gear. For the ideal diagnostic only, a continuous conductance transitioning around the same clock threshold replaces the discontinuous SW element: Ron100 ohm, Roff1e12 ohm, tanh width0.025*VDD. The actual transistor-switch circuit and10 ns clocks are unchanged. Smooth-control results must be labeled as such; they are not a rerun of the original discontinuous ideal SW model.

Both smooth-control and transistor-switch nominal cases were repeated with2 ns maximum timestep. See`numerical_timestep.json`; adaptive grids and netlist ordering can change microvolt-scale values. The Xschem-symbol SC export was separately simulated and matches all six sampled native-deck outputs within**2.478 uV**. The transistor schematic also separately matches GDS in local LVS.

This is **engineering capacitance extraction**, including intentional resistor-body resistance. It is not qualified full wire/contact/diffusion/well/substrate RC. As in the prior work, temporary extraction-only import filtering prevents raw non-electrical marker paint overwriting electrical well/active planes. Original PDK files are unchanged. The poly capacitance alias is extended to resistor-body paint using existing coefficients; this body-C estimate is not a foundry-qualified resistor extraction model. The exact10.64 pF needs process/extractor validation before treating it as a silicon prediction. Shorted-terminal MOS capacitor warnings are recorded and their intended four-terminal topology is independently checked.

Full RC extraction was attempted again and reports**38 substrate-tile errors and142 missing-substrate messages**. Its raw output under`pex/rc_diagnostic/` is excluded from performance claims. Existing native HSPICE-to-ngspice ignored-parameter/noise limitations remain. Noise, mismatch Monte Carlo, reference startup/noise, routed SC/switch/sensor parasitics and final fabrication qualification remain pending. MOS compensation is not evidence that MOS devices can replace precision SC/SAR capacitors.

## Reuse and reproduction

- `designs/ota_telescopic_layout.sch`: transistor schematic, organized into signal core, NMOS sensing buffers, mirror-level-shift controller and MOS compensation. Global signal labels join repeated nodes; visible core wiring shows the signal path.
- `symbols/ota_cmfb_v2.sym`: reusable10-pin Xschem symbol. Include `models/ota_cmfb_v2_C.spice` and your native MOS/RPP cards. This export has unique subcircuit name`ota_telescopic_cmfb_v2`; the verified GDS/reference top cell remains`ota_telescopic_layout` with the same pin order.
- Pin order:`INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP`. Integrated reference diode; IREF3.5 uA,VSS0,VBN2.4 V,VBP=VDD-2.2 V,VCM=VDD/2. VBN/VBP/VCM generators remain external ideal references in these tests.
- `designs/sc_ota_cmfb_v2.sch`: visible OTA symbol with the unchanged SC network and simulation controls in the code block. Start Xschem from this project directory to load`xschemrc`. Netlist into`tb` and run from`tb` so relative model includes resolve. PDK includes expect`/home/berson_meshak/pdk/scl08/ngspice_models49`; collaborators must point those includes at their own authorized PDK.
- `./open_xschem.sh` opens that symbol testbench with the project configuration and `tb` as its simulation directory. Run it from a normal WSL desktop terminal with Xschem display access.
- `tb/layout_C_tg.cir` and`layout_C_smooth.cir`: standalone nominal decks. Run`ngspice -b -o layout_C_tg.log layout_C_tg.cir` from`tb`. Native PDK cards are referenced, not redistributed.
- Regenerate in order: `scripts/prepare.py`; `klayout -b -r scripts/generate.py`; `scripts/verify.py`; `scripts/extract.py`; `scripts/export_models.py`; `scripts/validate_layout.py`; `scripts/check_reset_range.py`. Add`--sc-only` to validation to repeat SC tests without repeating AC. `scripts/export_views.py` writes schematic/symbol/testbench exports; `scripts/verify_views.py` verifies their generated data. Raw decks preserve original run paths; regenerate after relocation. The previous study's`scripts/rebuild_magic.py` and bundled source restore`/tmp/magic_ota_tool` if it is missing.
- Plots:`plots/SC_before_after.png`, `CMFB_before_after.png`, `tradeoffs.png`, `layout.png`, plus PDFs and native schematic SVG.

`verification/final_status.json`, `loop_summary.json`, `SC_validation.json`, `selected.json`, hashes and raw logs preserve the final evidence. Intermediate sweeps are exploratory results and do not replace the final extracted-model data. Next work is a qualified full-RC/noise flow and a system accuracy/power budget, then switching-error/settling optimization if this architecture remains the preferred ASIC option.
