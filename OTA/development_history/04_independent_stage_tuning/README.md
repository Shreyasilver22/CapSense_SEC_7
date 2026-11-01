# 04_independent_stage_tuning: Independent stage and device-group tuning

Development order: **4**. Date / ordering evidence: **28 October 2026**.

Selected high-gain compromise plus faster and lower-power alternatives.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_1/current_reference_exploration/stage_tuning/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Design 1: independent device-group and stage-current tuning

28 October 2026. Nominal SCL CP8D 800 nm exploration. Earlier baseline and current-reference results remain unchanged. No GitHub push performed.

## Outcome

The selected compromise has higher gain, faster settling and more nominal stability margin than the previous all-long-channel candidate, at increased supply power and transistor area. A faster, lower-gain option and a slower, lower-power option remain available. No system-level optimum is claimed because final timing, feedback factor, noise, swing and power requirements remain open.

| Candidate | Gain at 1 Hz (dB) | UGF (MHz) | PM at 5 pF (deg) | Supply power (uW) | Worst 2 V step settling (us) |
|---|---:|---:|---:|---:|---:|
| Previous all-long-channel control | 85.31 | 0.264 | 60.35 | 109.87 | 9.066 |
| Selected high-gain compromise | 88.77 | 1.003 | 73.44 | 174.74 | 2.876 |
| Fastest checked alternative | 81.98 | 1.849 | 69.14 | 329.23 | 1.211 |
| Lowest-power checked alternative | 84.20 | 0.164 | 65.02 | 55.67 | 18.180 |

Settling above is to +/-0.1% of the step amplitude around the actual final output (2 mV band for a 2 V step), worst of rising/falling edges. Time starts at the beginning of each 10 ns input edge. The previous control was rerun under these definitions: small differences from the preceding report reflect timing reference, data precision and waveform sampling. Selected large-step total-error settling to the ideal input is 2.682/2.871 us. Selected 100 mV dynamic settling is 0.684/0.689 us. Its static follower error is approximately -0.206 mV at 2.6 V and -0.202 mV at 2.5 V; it therefore does NOT meet a +/-100 uV total-error band for the 100 mV test. High gain does not eliminate systematic offset. No offset calibration was added.

## Selected circuit and geometry

Seven-MOS single-ended core plus diode-connected M8. IREF=2.5 uA is sourced from VDD into M8; ideal reference branch included in supply power. L_input=2.4 um, L_mirror=3.2 um, L_output=3.2 um. Tail/reference devices retain 3.2 um length. Cc=3 pF, external CL=5 pF. K=4 multiplies both M6 and M7 widths, preserving their approximate DC balance while increasing output drive. This is a mirror geometry multiplier, not a guaranteed current ratio. Measured output/tail current ratio is 11.92, versus nominal geometry ratio 2*K=8.

| Devices | W (um) | L (um) |
|---|---:|---:|
| M1, M2 input pair | 7.5 | 2.4 |
| M3, M4 PMOS mirror | 10 | 3.2 |
| M5 tail, M8 reference | 20 | 3.2 |
| M6 PMOS output | 112 | 3.2 |
| M7 NMOS output sink | 160 | 3.2 |

Gate-area proxy sum(W*L)=1098.4 um^2, compared with 473.6 um^2 for the control. Cc falls from 20 to 3 pF. Total layout area cannot be inferred without capacitor density, contacts, device folding and routing. Legal geometry/model qualification must still be checked with process documentation.

## Search and validation

- Initial grid: 864 AC points. LI/LM/LO independently 1.6,2.4,3.2 um; K=1,2,4,8; IREF=2.5,5 uA; Cc=2.5,5,10,20 pF. Within each group widths track length to maintain base W/L before K is applied. M5/M8 stay fixed.
- Refinement: 72 additional AC points. LI/LM=2.4,3.2 um; LO=3.2 um; K=2,4,6; IREF=2.5,5 uA; Cc=3,4,6 pF. Total 936 sizing/compensation points.
- 49 shortlisted points received both 100 mV and 2 V follower transients. Shortlist spans fastest UGF, low power, power/bandwidth tradeoff, high-gain refinement and the prior control; it is not exhaustive transient evaluation of all points.
- All 49 shortlisted points received extra AC checks at CL=1 and 10 pF at Vin=2.5 V, plus Vin=1.5 and 3.5 V at CL=5 pF. These are five separate conditions including nominal, not a full Cartesian product of load and bias. They are not PVT corners or full swing qualification.
- 26 shortlisted points passed gain>=80 dB, PM>=60 degrees, a single unity crossing and positive model-reported saturation margins across those conditions. Selected candidate is the fastest in large-step dynamic settling among these checked points with nominal gain>=85 dB. Faster and lower-power alternatives are retained. This is a documented screening preference, not a frozen system specification.
- Selected minimum checked phase margin=66.32 degrees; minimum checked gain=87.64 dB; minimum checked saturation margin=0.388 V.
- Selected large-step test repeated with 1 ns maximum timestep versus 5 ns: worst settling changes by 0.680 ns. This supports numerical repeatability, not physical model accuracy.
- xschem extraction verified all eight MOS terminal connections, N/P models, W/L values and Cc value/endpoints. Extracted AC data agree with the parameterized core within tolerance. Native xschem follower testbench and delivered SPICE testbenches were netlisted/simulated successfully. GUI plotting was not tested in this headless environment.

AC uses a 1e12 H DC-feedback inductor and 1e12 F AC-ground capacitor, biasing at a follower operating point and opening AC feedback over the measured range. It is an estimate of follower return ratio, not a phase-specific switched-capacitor loop-injection measurement. All sign changes through unity are counted. Settings: nominal model deck, 5 V, 27 C; reltol=1e-5, vntol=1e-8, abstol=1e-12, numdgt=12; AC 100 points/decade from 1 Hz to 1 GHz. Transient observations span 90 us with 40 us input plateaus. Plateau means near their end establish the settled value. CSV NaN / JSON null means the error band was not retained within the observation window.

## Open in xschem / run

From this stage_tuning folder:

```bash
xschem --rcfile xschemrc tb/ota_group_tuned_tb.sch
```

Ctrl-click Run simulation + plot. This demonstration uses the inherited 100 ns input rise/fall time; quantitative sweep testbenches use 10 ns. Open designs/ota_group_tuned.sch to inspect the selected transistor arrangement. The six pins are inp, inn, out, vdd, vss, iref. Source IREF into iref; do not apply the old fixed VBN source there.

Selected, fastest and lowest-power plain SPICE testbenches are in tb/. Run them from tb, for example `ngspice -b -o ../results/selected_large.log selected_large.cir`. The private foundry model is referenced at its existing local location; no model cards are redistributed.

## Reproduce and files

1. `python3 tune.py` runs the initial grid and shortlist transients.
2. `python3 refine.py` adds refinement points and selected transients.
3. `python3 finish.py` performs load/output checks, selects candidates, creates schematic/testbenches and plots.
4. Netlist designs/ota_group_tuned.sch into results/extracted.spice, and tb/ota_group_tuned_tb.sch into results/ota_group_tuned_tb.spice with xschem using the local xschemrc; simulate the native testbench from results/.
5. `python3 verify.py` checks extraction, reruns selected benches and records numerical validation. `python3 report.py` creates this report, alternative testbenches and verification plots.

NumPy, Matplotlib, ngspice and xschem are required. Full run inputs/logs/data are under results/runs/. Main tables: ac_sweep.csv, refinement_ac.csv, transient_shortlist.csv, load_output_checks.csv, validated_shortlist.csv. summary.json records selection, alternatives, Pareto subset among checked shortlisted points, provenance hash and verification. plots/comparison.png/.pdf compares performance; verification.png/.pdf shows selected phase, load margins and total error. Keep initial and refinement sweeps for evidence; this is a bounded search, not a proof of a global optimum.

## Limitations and next decision

Existing ngspice warnings include ignored HSPICE parameters and PMOS capacitance entries. All dynamic results remain provisional pending a compatible, qualified SCL model flow. No noise, mismatch, extracted parasitics, PVT, reference-generator startup/drift/noise, PSRR, CMRR, actual SC sampled-error test, ADC kickback or common-mode-feedback design is included. Power includes the ideal reference branch but excludes overhead of a practical reference generator. Single-point DC saturation checks do not prove transient saturation throughout a swing. The circuit remains single-ended.

The selected 2 V settling time is still longer than the illustrative 2.45 us amplification window in the behavioral model; that window is not a confirmed requirement. The faster candidate offers a different power/gain tradeoff. Next compare both in an explicit SC feedback configuration with the actual feedback factor and sampling schedule, then evaluate offset/noise and model compatibility before choosing the architecture.
