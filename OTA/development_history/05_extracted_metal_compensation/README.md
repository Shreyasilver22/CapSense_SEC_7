# 05_extracted_metal_compensation: Extracted metal-capacitor compensation

Development order: **5**. Date / ordering evidence: **28 October 2026**.

Parasitic and plate-orientation study; capacitor library itself remains in the existing capacitor directory.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_1/extracted_capacitor_analysis/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Tuned OTA with extracted metal compensation capacitors

28 October 2026. This is a separate analysis of the previously tuned SCL800 OTA. Its transistor geometry and 2.5 uA ideal reference current are unchanged. Earlier OTA results and the shared capacitor library are preserved.

## Main result

The ideal 3 pF result does not survive direct replacement by the extracted metal capacitor model. Substrate parasitics reduce phase margin and worsen settling. Plate orientation matters. Among tested extracted values, 8 pF with TOP=n2, BOT=out, SUB=vss is the smallest that meets the working PM>=60-degree screen throughout the full checked load/output grid. It is a conservative simulation candidate, not a global optimum or fabrication qualification.

All nominal numbers below: VDD=5 V, 27 C, explicit CL=5 pF, follower DC input 2.5 V. Gain is measured at 1 Hz; PM/UGF are from the follower-biased AC fixture. Settling is worst polarity of a 1.5-to-3.5 V follower step, within 0.1% of its actual settled value (2 mV band), measured from the beginning of the input edge.

| Compensation | UGF (MHz) | Nominal PM (deg) | Minimum PM over checked grid (deg) | 2 V settling (us) |
|---|---:|---:|---:|---:|
| Ideal 3 pF | 1.003 | 73.44 | 65.53 | 2.876 |
| Ideal 3.00538 pF | 1.002 | 73.46 | 65.56 | 2.886 |
| Extracted 3p, TOP=n2 | 0.905 | 57.86 | 50.74 | 3.154 |
| Extracted 3p, TOP=out | 0.860 | 53.81 | 45.08 | 3.573 |
| Extracted 4p, TOP=n2 | 0.700 | 60.85 | 54.68 | 4.094 |
| Extracted 6p, TOP=n2 | 0.479 | 64.03 | 59.19 | 5.978 |
| Extracted 8p, TOP=n2 | 0.364 | 65.79 | 61.80 | 7.818 |
| Extracted 10p, TOP=n2 | 0.293 | 66.81 | 63.38 | 9.608 |

The near-identical ideal 3/3.00538 pF results isolate the cause: the small mutual-capacitance rounding error is not responsible for the large PM change; added node loading is. TOP=n2 is preferable among the two orientations tested at 2.5/3/4 pF. The larger 6/8/10 pF trials use this orientation only; no universal orientation optimum is claimed.

Selected 8p candidate: gain at 1 Hz=88.7507 dB; quiescent supply power including ideal IREF branch=174.7375 uW; small-step dynamic settling (100 mV, +/-100 uV around final output) worst=2.124 us. Small-step static follower error remains about -0.206 mV, so it does not retain a +/-100 uV TOTAL-error band around the ideal input. Compensation does not remove this static error. Quiescent power stays unchanged because the supplied capacitor model has no DC conduction; dynamic energy was not compared.

The 8p capacitor's extracted mutual value is 8.00295 pF; n2-to-substrate=4.90149 pF and out-to-substrate=14.6206 pF. With explicit CL=5 pF, the output therefore has about 19.6206 pF of explicit ground-referenced capacitor loading before intrinsic transistor capacitances and mutual-C effects. These parasitics are retained in the simulation, not folded into an ideal Cc.

## Capacitor geometry and layout

Existing 2.5/3/4 pF models were copied from the shared v2 library. New 6/8/10 pF variants were generated and checked in this experiment's cap_variants subproject using the same 20 x 20 um metal-overlap unit and value-to-unit-count rules. This does not add them to the shared library's editable-value catalog automatically.

The selected layout is `cap_variants/layouts/requested_8p.gds`, containing `scl08_cap_n703` (703 units). Bounding footprint=912 x 876 um = 0.798912 mm^2. This excludes chip-level routing and guard rings. That is a substantial compensation-capacitor area cost; meeting the nominal stability screen this way is not proof of a practical area/power/speed optimum. Its supplied KLayout DRC report has zero markers. Native capacitor LVS is not supported by the stock device deck.

## What was simulated and verified

- 11 circuit configurations: two ideal controls; 2.5/3/4p extracted models in both orientations; 6/8/10p extracted models with TOP=n2.
- Each configuration: full Cartesian grid CL=1/5/10 pF and follower DC input=1.5/2.5/3.5 V. Total 99 AC runs. The original tuning report used fewer combined load/bias checks, so minimum margins should be compared using this rerun grid.
- Each configuration: 100 mV and 2 V follower transients at all three explicit loads. Total 66 base transient runs. These are continuous-time follower tests, not a switched-capacitor system simulation.
- Selected large-step case repeated at 1 ns maximum timestep versus 5 ns; worst settling changed by about 0.121 ns, supporting numerical repeatability only.
- Unchanged eight-MOS connectivity, models and geometry verified in the native xschem extraction. XCC pin order explicitly verified as n2/out/vss.
- AC simulated from the extracted schematic matches the authored parameterized netlist within tolerance. Native xschem follower testbench and all delivered selected SPICE testbenches were simulated successfully. GUI button clicks were not exercised in this headless environment.

All simulations used the local nominal SCL transistor deck and ngspice. reltol=1e-5, vntol=1e-8, abstol=1e-12, numdgt=12; AC 150 points/decade, 1 Hz--1 GHz; transient max timestep=5 ns (1 ns fine check), 90 us duration, 40 us pulse plateaus, 10 ns input edges. Final output is averaged near each plateau's end; last-exit settling is measured against that value and separately against ideal input. Full data/logs and both error definitions are in results/.

The AC fixture uses a 1e12 H DC feedback inductor and 1e12 F AC-ground capacitor. It estimates follower return ratio at the closed-loop DC operating point. It is not a full SC-phase loop-injection qualification. Crossings through unity are counted; final acceptance still requires broader stability checks.

## Open and simulate

From this experiment directory:

```bash
xschem --rcfile xschemrc tb/ota_extracted_cc_tb.sch
```

The testbench uses the 8p extracted model, retains the 5 pF explicit external load and provides the inherited Run simulation + plot launcher. The native demonstration uses the inherited 100 ns input edges and 120 us duration; quantitative comparisons use the 10 ns/90 us benches described above. Open designs/ota_extracted_cc.sch to inspect transistor-level wiring. It has the same six external OTA pins as the earlier current-reference design.

Plain SPICE benches in tb/: selected_ac.cir, selected_small.cir, selected_large.cir and extracted_ac.cir. Run from tb, for example `ngspice -b -o ../results/selected_large.log selected_large.cir`. Capacitor models are bundled locally in designs/capacitors.lib.spice; the private transistor model is referenced at its existing local path. No foundry model deck is copied.

Reproduce: `python3 scripts/analyze.py`; generate the local 6/8/10p capacitor variants with `python3 cap_variants/scripts/build.py --pdk-root /path/to/scl_cp8d`; then `python3 scripts/extend.py`; finally `python3 scripts/finalize.py`. NumPy, Matplotlib, ngspice, xschem, KLayout and Magic are required. The plotting library may need a writable MPLCONFIGDIR on a restricted machine. Model provenance/hashes are retained in the capacitor catalogs and the earlier transistor-model provenance records. recover_summary.py reconstructs the saved analysis tables if a report stage is interrupted; it is not needed for a normal reproduction.

## Interpretation and limits

The previous 88.8 dB/1 MHz/73-degree OTA numbers were for ideal Cc. They must not be presented as the performance of the extracted-capacitor implementation. The new result is approximately 88.75 dB/364 kHz/65.8 degrees with an 8p target and the modeled parasitics. A 2 V transition still takes about 7.82 us, longer than the illustrative 2.45 us SC amplification window in the behavioral model. That window is not a frozen requirement. Smaller transitions/feedback factors and actual SC sampling need separate simulation.

No transistor-current or geometry optimization was performed here. An eventual remedy may involve better capacitor geometry/modeling, a revised compensation network, or stage-current retuning. This report does not claim that increasing Cc alone is the final design solution.

Both existing limitations remain: ngspice ignores some transistor-deck HSPICE parameters, including capacitance entries; installed Magic 8.3.105 is below the capacitor technology's 8.3.579 requirement and native export drops one substrate capacitance. Evaluation models retain documented raw-.ext node/coupling terms, but that discrepancy remains unresolved in a supported flow. Dynamic numbers are provisional, not silicon-qualified.

Only one process deck, 5 V and 27 C were tested. No transistor mismatch, capacitor tolerance/matching, voltage coefficients, leakage, dielectric loss, conductor-resistance extraction, substrate disturbance, real current-reference generator, startup, noise, full SC switching, ADC kickback or extracted OTA wiring was included. Capacitor SUB is tied to quiet vss. DC saturation throughout every transient was not established. No final PVT, formal capacitor LVS, tape-out acceptance or optimum claim is made. No public upload or GitHub push was performed.
