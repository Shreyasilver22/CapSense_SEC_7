# 19_integrated_resistor_pvt: Integrated OTA / RPP extraction and PVT

Development order: **19**. Date / ordering evidence: **31 October 2026**.

Six-unit / 16 kohm layout passes local DRC/LVS but fails the assumed full stability envelope.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/integrated_rpp_pvt_20261031/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Integrated OTA + RPP: extraction, PVT and noise comparison

**Outcome:** the integrated six-capacitor/RPP layout passes local DRC/LVS and is nominally faster than the nine-capacitor baseline. It does **not** pass the assumed 4.5–5.5 V/high-output PVT envelope. Full-RC substrate modeling and quantitative noise qualification remain blocked by the available extraction/model translation, despite completed simulations. These results must not be presented as full signoff.

## Physical circuit

The modified macro contains the unchanged OTA core, six actual PMOS compensation units W20/L10 um, and ten actual P-poly RPP sections W2.4/L137.143 um. The resistor body sums to 16.0000167 kohm at typical/27 C. It connects N2 to GCOMP; compensation gates connect to GCOMP, while source/drain/isolated-well bodies connect to OUT. Bias is an ideal external Iref=3.5 uA. The SC circuit was not changed.

The entire resistor and OTA are drawn in a single editable GDS top cell, including connections between them. Extent is 364.1 x 317.4 um, bounding area about 0.11557 mm2, versus 0.11280 mm2 for the baseline nine-unit macro. Reducing capacitor count does not reduce overall area in this initial resistor placement. No complete guard-ring/dummy/current-density optimization is claimed.

Final DRC: zero markers using the original local SCL KLayout deck. Initial four via/contact-spacing violations were corrected by moving the two resistor-port vias away from contacts. LVS against the independent reference passes. Deliberate incorrect capacitor-gate and output-transistor-width references fail as expected. Original source rule decks and PDK cards remain unchanged.

## Integrated extraction: actual work and qualifications

Both C-only and distributed-wire-RC extraction were run on the complete integrated GDS with Magic 8.3.688. The final simulation model contains newly extracted core/resistor-route capacitances and resistor-body capacitance, not the old fixed-routing model or the earlier generic 0.48 pF estimate.

Three extraction/export adaptations were necessary:

1. As in prior work, raw non-electrical mask marker painting was omitted in a temporary extraction technology copy to preserve wells and implants. Resistor terminal marker `respin` also had to be omitted as raw paint to preserve actual contact connectivity. All masks remain in the original GDS and original KLayout DRC/LVS.
2. The technology's poly capacitance alias excludes resistor-body paint. The temporary extraction alias was extended to include the existing mrp1/mrp2 resistor-body types, applying the existing poly area/perimeter coefficients. The resulting resistor-body ground capacitance is **0.426574 pF**, with additional terminal/metal/coupling terms separately extracted. This is an engineering extraction extension, not a foundry-qualified capacitance model.
3. Native ext2spice resistor-tee export emitted only one half of each `rsubckt` RPP device. scripts/export_models.py emits both halves from the actual .ext device terminals, length, width and body-capacitance node. Each physical resistor section becomes two native PDK RPP half-length instances around its extracted body-capacitance node. The twenty instances sum to the correct resistance; no native resistor model equations are copied or modified. A geometry-derived numeric RPP view is used only for topology comparison.

The C-model transistor/resistor topology and resistor-contracted RC topology each independently match the integrated GDS through KLayout LVS. That validates connectivity and aggregate device/resistor values; it does not validate capacitance coefficients or missing substrate physics. Native intermediate exports showing the marker/body-C/export problems are retained as diagnostics and are not the final simulation models.

The full RC run still reports substrate-tile and missing-substrate-connection errors. Missing qualified well/substrate junction capacitance, diode behavior and distributed substrate/well resistance remain. **Full RC is diagnostic only**, even though its contracted topology matches. Wire RC values are nominal and are not a qualified process/temperature extraction corner. No manual transistor bulk substitution was used.

## PVT experiment scope

Actual local transistor cards: tntp49_5v (typical), bnbp49_5v (best N/best P), bnwp49_5v (best N/worst P), wnbp49_5v (worst N/best P), wnwp49_5v (worst N/worst P). Native resistor cards: best/typ/worst RPP, independently combined with MOS cards. Model names are preserved; they are not assumed identical to modern fast/slow foundry corner conventions.

Supplies: 4.5/5.0/5.5 V. Temperatures: 0/27/85 C. These are assumed screening ranges, not user-specified ASIC requirements or certified PDK reliability limits. References remain ideal and Iref remains fixed across PVT. No mismatch Monte Carlo was performed.

Baseline has 45 MOS/V/T configurations. Integrated circuit has 135 MOS/resistor/V/T configurations. Main AC measurements are at CL=1/5/10 pF and follower DC=2.5 V, plus CL=10 pF at follower DC=1.5 and 3.5 V: 900 main AC cases. Additional CL=10 pF follower DC=3.3 V checks add 180 cases. To separate input common-mode and output voltage, another 360 cases hold inputs near 1.5 V while biasing output to 3.3/3.5 V through an ideal DC feedback level shift; the AC loop remains broken through the standard L/C fixture. Four nominal RC diagnostic AC cases complete 1444 AC cases. All analyses completed without SPICE run failures; that does not mean all requirements passed.

PVT noise runs: 180 core configurations plus one nominal RC diagnostic. Selected transient runs: 22, covering nominal points and configurations selected for worst PM, fastest UGF, minimum gain and maximum modeled noise. Thus transient extrema are only among selected cases, not exhaustive PVT transient bounds.

## Nominal comparison

Conditions: typical MOS, typical RPP, 5 V, 27 C, 5 pF load, follower DC=2.5 V. Large-step settling: 1.5–3.5 V into 10 pF, 0.1% band about actual final output, worst rising/falling edge. It excludes static error from the settling band; static errors are separately reported. Fine result uses 1 ns maximum step and 10 ns input edges.

| Metric | Baseline: 9 MOS caps, direct compensation | Integrated: 6 MOS caps + PDK RPP |
|---|---:|---:|
| DC gain (dB) | 87.57 | 87.57 |
| Unity-gain bandwidth (MHz) | 0.936 | 1.412 |
| Phase margin at nominal point (degrees) | 71.04 | 81.76 |
| VDD quiescent power (uW) | 176.84 | 176.84 |
| 2 V settling at 10 pF, fine timestep (us) | 2.8122 | 1.9995 |
| Raw follower input-noise RMS, 1 Hz–1 MHz (mV) | 3.1673 | 3.1595 |

Nominal speed improves about 51% in UGF and 29% in large-step settling. Gain and DC power do not improve. Small-step response depends on load. The integrated full-RC diagnostic gives about 1.9766 us large-step settling at 10 pF; this numerical value is not a validated full-RC result.

## PVT failures and output/common-mode distinction

| Main-grid comparison | Baseline | Integrated |
|---|---:|---:|
| Worst PM at fixed 5 V supply across tested process, temperature, resistor, load and bias points | 61.81 deg | 62.61 deg |
| Worst PM over complete assumed supply range | 33.16 deg | 26.84 deg |
| Main AC points below 60 degrees | 15/225 | 45/675 |

The integrated circuit has three resistor corners versus baseline's one, so raw failure counts are not directly equal-sized samples. Both fractions are about 6.7%. Baseline resistor-corner duplication would not change its circuit.

The worst main-grid integrated case is wnwp49_5v MOS, best (lower resistance) RPP, VDD=4.5 V, 85 C, CL=10 pF, follower DC=3.5 V. It has PM=26.84 degrees. Its selected 2 V step settles in about 2.79 us but overshoots to about 3.64 V, so a short settling time alone must not be interpreted as adequate stability margin. No tested steady-state DC tracking failures were found in the main AC sweep.

A follower DC test changes both input common-mode and output level. Therefore a separate test held input common-mode near **1.5 V**, with output at **3.3 V**, matching the nominal SC reference/output region more closely. The worst integrated result is **38.79 degrees**, at 4.5 V, 85 C, wnwp49_5v, best RPP and 10 pF. The baseline gives 44.66 degrees in the analogous worst case. At output 3.5 V with fixed 1.5 V input common-mode, the modified design reaches 27.09 degrees. This confirms that changing the input common-mode alone does not remove the high-output/low-supply problem.

These are OTA loop tests, not complete SC PVT simulations. SC noise gain, phase-dependent load and clock disturbances were not re-simulated. The existing nominal SC demonstration must not be claimed valid across this PVT range. All tested 5 V main-grid cases exceed 60 degrees, but this is not a guarantee for arbitrary intermediate points, mismatch or untested loads.

## Noise: run, but not qualified

Noise was simulated in a unity-gain follower at 2.5 V and 5 pF, integrated from 1 Hz to 1 MHz. Raw nominal input-referred RMS is about 3.167 mV baseline and 3.159 mV integrated, a negligible difference for design selection. Across the tested PVT configurations, raw input noise spans about 2.567–4.254 mV for baseline and 2.562–4.240 mV for integrated. These numbers do not establish ADC resolution, SNR, actual silicon noise or a low-noise design.

The MOS translation still ignores `nlev` and other HSPICE/model parameters, including PMOS overlap entries. The complete list is in verification/qualification.json; native simulator logs are retained. Since `nlev` affects noise-model interpretation and no independent noise-model qualification exists, the full-OTA numbers cannot be accepted as a verified noise budget. Native RPP includes ordinary thermal noise but no excess/flicker-noise coefficients. Standalone resistor thermal noise was verified in the preceding resistor-validation work; that narrow check does not qualify full transistor/excess noise. Neither HSPICE nor Spectre was found in the local command path during this task. A supported/qualified model flow or independent reference data is required to close this item.

## Decision

The RPP compensation change remains the faster nominal candidate at matched current. It is **not ready for full-envelope approval**. Fix the low-supply/high-output bias behavior before finalizing architecture or claiming the SC output swing is supported across PVT. Establish a qualified MOS/noise/extraction flow before interpreting the raw noise and RC numbers as signoff. Layout refinement alone cannot establish those missing model properties.

## Files and reproduction

layout/ota_design2_mos.gds: complete integrated layout; plots/integrated_layout.png/pdf: actual layout view. schematic/reference.cdl and verification/drc.lyrdb/lvs.lvsdb: original-deck checks. verification/integrated_C.lvsdb and integrated_RC_diagnostic.lvsdb: extracted-model topology checks. verification/resistor_export.json, qualification.json and hashes.json: adaptations, limitations and provenance.

models/integrated_C.spice: integrated extracted-C/tee model, native RPP card supplied separately by each bench. models/integrated_RC_diagnostic.spice: resistor-network diagnostic; models/baseline9_C.spice: unchanged baseline. PDK cards are referenced locally, not copied. pex/: native intermediate exports and raw .ext/.res.ext records. Invalid intermediate native tee export is not a final model.

pvt_ac.csv/json, output_3p3_stress.csv/json, fixed_input_common_mode.csv/json: all AC results. pvt_noise.csv/json and pvt_transients.csv/json: noise and selected step tests. comparison_summary.json: consolidated results. results/: actual benches, data and logs. plots/integrated_pvt_comparison.png/pdf: comparison. tb/: relative-include nominal large-step benches for both C models and RC diagnostic; run ngspice from tb. Raw full-run decks reference staging paths; regenerate with scripts/pvt.py after moving.

scripts/generate.py creates the layout; verify.py checks original DRC/LVS and negative controls; extract.py uses the existing Magic8.3.688 tool under /tmp/magic_ota_tool and a temporary extraction technology copy; export_models.py repairs resistor tee export and checks extracted topology. pvt.py, check_3p3.py and check_common_mode.py reproduce the sweeps. report.py regenerates figures and consolidated output. The temporary tool binary may need rebuilding after cleanup; build instructions are retained in physical_layout_v3's report. No source PDK, system packages, SC design or previous OTA revision was modified. Nothing was pushed to GitHub.
