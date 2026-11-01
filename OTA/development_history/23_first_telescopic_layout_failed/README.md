# 23_first_telescopic_layout_failed: First telescopic layout: extracted CMFB failure

Development order: **23**. Date / ordering evidence: **1 November, first telescopic layout 2026**.

Historical failed candidate: local DRC/LVS pass, but resistor parasitics destabilize CMFB. Do not use as the current design.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `architecture_exploration_20261031/telescopic_layout_20261101/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Telescopic OTA layout and SC simulation — 1 November 2026

The ordinary telescopic OTA with buffered continuous-time CMFB was physically laid out, DRC/LVS checked, capacitance extracted, and actually simulated in the same single-ended SC circuit. **The layout passes connectivity/rule checks but the extracted-capacitance circuit fails stable common-mode control at nominal conditions.** This first-pass CMFB implementation should not proceed to fabrication.

Only the ordinary telescopic candidate was laid out in this step. The gain-boosted version is not claimed to have a verified layout; its shared CMFB concept should be corrected before investing in another macro.

## Physical implementation and checks

- Top cell: `ota_telescopic_layout`; actual GDS: `layout/ota_telescopic_layout.gds`.
- 43 physical MOS units, including integrated W20/L3.2 bias-reference diode and20 MOS compensation units. Original W/L and multiplicities retained; source/drain contact arrays were added. Single-poly/two-metal SCL08 layers, individual N-wells for output-tied PMOS capacitors, explicit well/substrate taps.
- Two native P-poly1 Mohm resistors:100 series sections each, sectionW2.4 um/L857.143 um. Each bank has approximately85.7 mm total resistor-body length. Geometry is snapped to the1 nm GDS database grid; extracted resistance agrees within the native LVS tolerance.
- Macro bounding box: 1905.086 by 1357.600 um = **2.586345 mm2**. This is an unoptimized floorplan bounding area, not a claimed minimum die area; resistor banks dominate the footprint.
- **DRC: 0 markers** using the original unmodified local SCL CP8D KLayout deck.
- **LVS: MATCH** against the source-transistor reference with both1 Mohm resistors. Wrong-gate and wrong-width negative controls both fail as expected.
- **Extracted C-netlist topology: separately MATCHES the GDS in KLayout**, retaining all resistor sections after correcting the native tee-export issue.
- These are local-deck macro checks, not foundry signoff, full-chip density/pad/ESD qualification, or matching-optimized layout.

Ports are `INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP`. The macro includes the reference diode; external current source feedsIREF. Cascode reference voltages remain external ideal supplies in the bench:VBN2.4 V andVBP=VDD-2.2 V. VCM=VDD/2. A fabricated reference generator and its power/noise are not included.

## Same SC testbench, nominal50 kHz

SCL800 native typical MOS and RPP,5 V,27 C,IREF3.5 uA. CS2.5 pF,CF7.5 pF,VP0.3 V,VREF1.5 V,OUTP5 pF,OUTM5 pF; identical switch sizes, timing, nonoverlap, reset and three-cycle integration sequence as the preceding SC comparison. Ideal expected output is1.5->2.1->2.7->3.3 V.

The OTA macro is layout extracted; the SC switches/sensor/feedback/load capacitors remain the original schematic models. This is not a layout extraction of the entire SC readout.

| Model | Switches | Third output (V) | Worst sampled error (mV) | Worst sampled CM error (mV) |
|---|---|---:|---:|---:|
| Schematic reference | ideal | 3.299926 | 0.074 | 5.622 |
| Schematic reference | tg | 3.356598 | 56.602 | 6.585 |
| Layout C model | ideal | 3.118464 | 181.536 | 1222.131 |
| Layout C model | tg | 3.281129 | 86.869 | 898.087 |
| Diagnostic: resistor ground C removed | ideal | 3.299962 | 0.061 | 5.537 |
| Diagnostic: resistor ground C removed | tg | 3.356605 | 56.608 | 6.493 |

Worst errors cover all six settled sampling instants across two frames. The third output shown is the last sample of the second frame. Main runs use10 ns maximum timestep. The apparently smaller final transistor-switch error is not a valid improvement: it can arise from switch-error cancellation with the unstable common-mode trajectory. Full traces show output excursions close to the rails, and sampled common-mode errors approaching1.2 V with ideal switches.

## Cause and controlled diagnostic

The extraction estimates **53.182 pF total resistor-body ground capacitance**, approximately26.6 pF per1 Mohm bank. This parasitic was absent from the architectural schematic benchmark. The same physical resistance now drives substantial distributed capacitance and long high-impedance sensing routes.

Symmetric sensing-gate CMFB loop injection, with differential feedback closed and5 pF on each output, gives:

| Model | CMFB phase margin |
|---|---:|
| Schematic | 71.19 degrees |
| Extracted capacitance model | **-48.73 degrees** |
| Diagnostic removing only resistor-body ground C | 40.69 degrees |

Removing exactly200 resistor-center ground-capacitor entries restores small SC errors in the diagnostic run, confirming that their contribution is dominant in this model. **This diagnostic is not a physical fix and is not an acceptable extracted model.** Its remaining CMFB margin is only about41 degrees, below our previous60-degree screening target; routing and other extracted capacitances also require attention. The injection result is an engineering loop diagnostic rather than a formal multi-loop pole-count/Nyquist certificate; the observed large transient oscillations independently support rejection of the nominal layout-C circuit.

Additional layout-C SC runs at5/25/100 kHz still show large errors. Lower clock alone does not cure the unstable continuous-time CMFB loop. Two2 ns repeats at50 kHz reproduce the failure; exact values are in`timestep_comparison.json`.

## Extraction validity and limitations

The simulation model is **capacitance-extracted, not qualified full interconnect/substrate RC**. It includes native MOS devices with extracted junction geometry, native200-section resistor bodies exported as400 half-resistor subcircuits, and1185 explicit capacitors. Resistance of those intentional P-poly bodies is included; distributed wire/contact/diffusion/well resistance is not qualified in this model.

Magic8.3.688 was rebuilt from the same pinned upstream source used previously. Original PDK files were not edited. As in the earlier OTA extraction work, temporary extraction-only adaptations omit raw marker paint that overwrites electrical device planes, retaining raw masks in boolean device derivation. The existing poly capacitance alias is extended to the resistor-body paint to include body capacitance. **This is an engineering extraction adaptation, not a foundry-qualified resistor-capacitance model.** The exact53 pF estimate needs PDK/extractor validation before treating it as a silicon prediction. It exposes a major sensitivity and prevents accepting the schematic result as layout-qualified.

Native ext2spice tee output forRPP drops one half. `export_models.py` restores both halves from actual`.ext` terminal/geometry records; independent numeric-resistor KLayout LVS verifies the corrected topology. The uncorrected`pex/ota_C_raw.spice` must not be used as a complete simulation model. Use`models/layout_C.spice`.

Shorted-source/drain PMOS capacitor extraction reports20 missing-terminal warnings and joins the remainder toOUTP/OUTM/VDD as appropriate. Their four-terminal connectivity was independently checked by the extracted-model LVS. These expected shorted-terminal warnings are not silently reinterpreted as full extractor qualification.

A separate full-RC attempt was actually made. It reports **33 substrate-tile errors and95 missing-substrate-connection messages**. Files under`pex/rc_diagnostic/` are unqualified and excluded from the performance simulations. No successful full-RC simulation or foundry signoff is claimed.

Existing SCL-HSPICE-to-ngspice ignored-parameter/noise limitations remain. No noise, mismatch, full PVT or reliability qualification was attempted for this nominally unstable layout. Testbench references and clock generators are ideal; CS/CF are ideal linear caps. No claim is made that MOS caps replace precision SC/SAR capacitors.

## Next design focus

Redesign the CMFB averaging/sensing network with a realistic parasitic and area budget. Investigate lower averaging resistance with suitably stronger, linear sensing buffers, a compact sensing topology, or clocked CMFB if its timing and charge-injection costs fit the system. Keep the high-impedance sense node and controller close in the revised layout. Re-extract and require both common-mode and signal-loop stability before continuing architecture selection. Increasing OTA gain or reducing the SC clock is not established as a solution to this failure.

## Reproduction and files

- `scripts/generate.py`: physical GDS and source-based reference generation; run using`klayout -b -r scripts/generate.py`.
- `scripts/verify.py`: original local SCL DRC/LVS and negative controls.
- `scripts/extract.py`: C extraction; `--rc` performs the separately recorded unqualified RC attempt. The system Magic8.3.105 is unchanged. If`/tmp/magic_ota_tool` is missing, run`scripts/rebuild_magic.py`; pinned source and Tk-header package are retained under`tools/build_inputs/`, requiring no system package installation. Upstream source:[Magic8.3.688](https://github.com/RTimothyEdwards/magic/releases/tag/8.3.688).
- `scripts/export_models.py`: native resistor tee correction, extracted-topology LVS, and same-interface schematic model.
- `scripts/run_sc.py`, `diagnose.py`, `check_cmfb.py`, `report.py`: actual SC/loop runs, diagnostics and report. Run extraction/model export before simulations; regenerate raw decks after relocating because they preserve original run paths.
- `tb/`: four standalone50 kHz SC decks using relative model paths. From this directory, run`ngspice -b -o layout_C_ideal.log layout_C_ideal.cir` or`layout_C_tg.cir`. PDK remains at`/home/berson_meshak/pdk/scl08/ngspice_models49`. Native PDK cards/decks are referenced, not redistributed.
- `plots/layout.png`, `sc_layout_comparison.png`, `cmfb_loop_comparison.png` plus PDFs.
- `verification/final_status.json`, DRC/LVS logs/databases,`comparison.csv`, `sc_nominal.json`, `sc_diagnostics.json`, `cmfb_comparison.json` retain the evidence.

SC runs:14; CMFB AC runs:3; execution failures:0. Completion means data was generated, not that performance passed. Source/layout/model hashes are recorded in`hashes.json` and`verification/model_export.json`.
