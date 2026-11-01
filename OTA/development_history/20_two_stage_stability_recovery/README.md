# 20_two_stage_stability_recovery: Two-stage stability recovery

Development order: **20**. Date / ordering evidence: **31 October 2026**.

12 MOS-cap units, 28 kohm RPP, widened output PMOS; minimum main-grid PM 62.22 degrees; slower settling.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/stability_recovery_20261031/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA stability recovery: low supply / high output

**Result:** a new physically drawn and re-extracted candidate recovers at least **62.22 degrees phase margin** across the 675 main PVT AC cases. All 405 extra bias/common-mode cases also exceed 60 degrees. This is a model-based stability recovery, not full foundry qualification. It costs area and settling speed, and does not resolve noise-model or substrate-extraction qualification.

The SC circuit, clock choices and capacitor assignments were not redesigned. A nominal regression used the existing SC bench with only the OTA model replaced.

## Diagnosis

At the former worst corner, the output PMOS still has saturation headroom: measured VSD about 1.00 V versus VDSAT about 0.277 V. Therefore output-transistor saturation loss alone was not the cause. The compensation gate/body bias changes strongly: about +1.188 V nominally, -0.36 V at the 3.3 V output corner, and -0.562 V at 3.5 V. A separate native-model AC capacitor test measured:

| Six-unit PMOS compensation test | Capacitance at 1 MHz |
|---|---:|
| Typical model, 27 C, VGB=+1.188 V | 2.475 pF |
| Worst N/P card, 85 C, same VGB | 2.276 pF |
| Worst card, 85 C, VGB=-0.36 V | 1.049 pF |
| Worst card, 85 C, VGB=-0.562 V | 0.679 pF |

These tests isolate modeled MOS C–V dependence. The OTA poles/gm also change with process/bias; the table does not attribute the complete PM loss exclusively to capacitance. Details are in diagnosis.log, cap_bias.json and scripts/diagnose.py/cap_bias.py.

## Physical change

- Compensation: **12 actual PMOS gate-capacitor units**, W20/L10 um, source/drain/body at OUT.
- PMOS output stage M6: **16 fingers W28/L3.2 um**, total W448 um, versus four fingers / W112 um before.
- Series resistor: **28 kohm typical native SCL08 RPP**, ten physical W2.4/L240 um resistor bodies. Best/worst body resistance is 24/32 kohm at 27 C using the native resistor cards.
- Ideal reference current remains **3.5 uA**. The NMOS output current-source stage and input-stage sizing are unchanged. This is not a class-AB output stage.

The new layout has 46 physical MOS devices and ten RPP sections. It uses a conservative seven-row floorplan with the resistor integrated above the core. Bounding size 364.1 x 502.2 um, area about 0.18285 mm2 versus 0.11557 mm2 before, about 58% larger. This floorplan is not area optimized; there is no claim that this exact area increase is fundamental. Missing well-leakage models also mean equal modeled DC power is not proof of identical silicon leakage.

Original local KLayout DRC: zero violations. LVS against the independent reference: match. Wrong gate and wrong width controls fail. C-extracted topology and resistor-contracted RC topology also match GDS. Native xschem core was netlisted and shows M6 m=16, MCAP m=12 and the 28k wrapper.

## Selection and rejected 32k trial

Initial screening varied capacitor count 6/9/12, output-PMOS scale 1/2/4, and RPP resistance scale 1/1.5/2/3/4, using fixed prior routing C for screening only. Additional current variants were screened. A 12-cap / widened-M6 / 32k candidate fixed the old low-voltage case but the fully re-extracted PVT sweep found a cold/best-device corner around 59.48 degrees, plus multiple unity crossings. That trial is retained under rejected_32k as a rejected AC/corner candidate, not accepted performance evidence. Its transient collection was interrupted by the revision move and is not used for any final claim.

The final 28k geometry was then regenerated and extracted anew. Native resistor bodies/contacts/routes, MOS fingers and routing capacitances are from that final geometry, not a copy of the sizing-study estimates. The final resistor-body ground capacitance from the adapted extraction flow is about **0.74650 pF**.

## Before/after performance

Nominal point: typical MOS, typical RPP, 5 V, 27 C, 5 pF load and 2.5 V follower operating point. Large-step settling is 1.5–3.5 V into 10 pF, worst rising/falling time to 0.1% about actual final output. Static error is measured separately and excluded from the settling band.

| Parameter | Previous six-cap / 16k design | Stability-first 12-cap / 28k design |
|---|---:|---:|
| Nominal DC gain | 87.57 dB | 91.90 dB |
| Nominal unity-gain bandwidth | 1.412 MHz | 0.918 MHz |
| Nominal phase margin | 81.76 deg | 113.30 deg |
| Minimum checked main-grid PM | 26.84 deg | 62.22 deg |
| Nominal VDD power | 176.84 uW | 176.84 uW |
| Nominal 2 V settling at 10 pF, 1 ns timestep | 1.9995 us | 4.2625 us |
| Nominal 100 mV settling at 10 pF | 0.671 us | 2.146 us |
| Nominal 2 V-step static final error, worst polarity | 0.181 mV | 0.851 mV |

This revision meets the tested stability target by accepting slower settling and more area. Higher DC gain did not remove systematic offset: changing the first-stage DC operating point changes current-mirror/drain-voltage balance. No mismatch Monte Carlo or offset trimming was included. Do not select it solely on gain or describe every parameter as improved.

The 5 ns large-step result is 4.2630 us; the 1 ns repeat is 4.2625 us, about 0.00053 us difference. Transients cover selected worst-PM, fastest-bandwidth, lowest-gain, largest modeled-noise and nominal cases. They are not exhaustive dynamic PVT bounds.

## Corner scope and crossing analysis

Actual native MOS cards: tntp49_5v, bnbp49_5v, bnwp49_5v, wnbp49_5v and wnwp49_5v. Native RPP best/typ/worst cards independently combined. Supply 4.5/5/5.5 V; temperature 0/27/85 C. These are assumed screening limits, not finalized chip requirements or foundry reliability certification.

135 physical-model/bias configurations, with five main load/bias points each: CL=1/5/10 pF at follower DC=2.5 V and CL=10 pF at DC=1.5/3.5 V, giving **675 main AC cases**. All completed and exceed 60 degrees. Worst case remains 4.5 V, 85 C, wnwp49_5v, best RPP, 10 pF, 3.5 V follower: **62.2199 degrees**. That point previously gave 26.8387 degrees.

Extra checks: 135 follower cases at 3.3 V plus 270 cases with input common-mode held near 1.5 V and output at 3.3/3.5 V through an ideal DC level-shift test fixture. All 405 exceed 60 degrees. At fixed input common-mode 1.5 V and output 3.3 V, the minimum is **89.5093 degrees**, versus 38.7871 degrees in the previous design.

Six main cases have three unity-gain crossings. Every interpolated crossing is retained in crossing_details; the reported PM is the smallest across all crossings, and reported UGF is the highest downward crossing. None was silently dropped. The sampled closed Nyquist path has zero winding about -1 (numerical absolute residual below 3e-16); high-frequency gain is below -40 dB by the end of the 1 Hz–1 GHz sweep. This supports the numerical loop-stability result assuming open-loop stability, but it is not a formal pole-count/all-frequency proof or silicon guarantee. The widest phase margins at nominal conditions do not imply faster settling.

## Unchanged SC regression

Same previous demonstration: 5 V, 27 C, CS=2.5 pF, CF=7.5 pF, VREF=1.5 V, VP=0.3 V, three cycles/frame, 5 pF load, same ideal or transmission-gate switches. Only the OTA model and its required native RPP include changed. Expected third-cycle output 3.3 V.

| Clock | Ideal-switch raw sample error | Transmission-gate raw sample error |
|---|---:|---:|
| 50 kHz | 1.601 mV | 58.343 mV |
| 100 kHz | 1.553 mV | 58.285 mV |
| 200 kHz | 5.550 mV | 50.099 mV |

Thus the assumed 50 kHz demonstration still settles, but the 200 kHz ideal-switch case loses accuracy. Raw TG error remains switch dominated; the smaller 200 kHz TG raw error must not be interpreted as improved accuracy because transient settling can partially cancel offset. These are nominal regression results, not complete SC PVT validation. The raw ideal-switch 50 kHz result is close to the earlier illustrative 1.8 mV full-excursion budget, so offset/noise budgeting remains important.

## Noise/extraction qualifications remain open

Raw nominal input-referred follower noise over 1 Hz–1 MHz is about 3.168 mV RMS in the new design, essentially unchanged from the previous raw 3.159 mV value. Across native process/resistor/V/T cases it spans about 2.567–4.257 mV RMS. These are unqualified ngspice model outputs. The known ignored HSPICE/MOS parameters (including nlev and PMOS overlap entries), missing resistor excess-noise model, no qualified transistor-noise reference, and no mismatch data remain. This work does not fix or approve the noise budget.

Extraction retains the prior temporary marker-import filter, resistor-body poly-capacitance alias extension and custom tee export from actual .ext records. The original PDK and DRC/LVS decks are unchanged. Full RC still emits substrate errors, with no qualified well/substrate junction capacitance/diode/resistance network. RC model outputs are diagnostic, not a complete signoff PEX. The final corner acceptance above uses the adapted C-extracted model. No assertion of 100% certainty, fabrication readiness, reliability qualification or complete system performance is made.

## Files and continuation

comparison.json: consolidated before/after and acceptance evidence. plots/stability_recovery.png/pdf: speed/gain/phase comparison. plots/stable_layout.png/pdf: actual final GDS view.

integrated_revision/layout/ota_design2_mos.gds: final physical macro. integrated_revision/designs/ota_stability_candidate.sch: updated xschem core; symbols/scl08_rpp_28k.sym and models/scl08_rpp_28k.spice are its native-PDK resistor wrapper. Include that wrapper and local MOS cards in the parent bench. xschemrc resolves local symbols.

integrated_revision/models/integrated_C.spice: final model used for PVT. integrated_RC_diagnostic.spice: diagnostic RC only. verification/ contains original-deck DRC/LVS, extraction-topology checks and final_status.json. PDK cards are referenced locally, not copied. Native intermediate tee export is not the final repaired model.

integrated_revision/pvt_ac.csv/json: main plus four RC diagnostics; fixed_input_common_mode.csv/json and output_3p3_stress.csv/json: extra checks; pvt_noise/transients files and results/: measurements, actual decks, logs/data. Portable final nominal benches are integrated_revision/tb/large_10p.cir and small_10p.cir; run ngspice from tb. Raw benches reference staging paths; regenerate scripts/pvt.py and bias-check scripts when moving.

sc_regression/: unchanged-topology nominal SC test benches and measurements. screening.json/csv, screen_candidates files, diagnosis.log, cap_bias.json and scripts/: initial investigation. rejected_32k/: rejected intermediate AC study, not final validation. Existing original OTA directories were preserved; nothing was pushed to GitHub.

Next step: agree on a settling/offset/power/area budget, then optimize speed from this stable baseline rather than reverting to a faster design that misses corner stability. A class-AB output stage or revised compensation architecture can be investigated separately; neither is implemented here.
