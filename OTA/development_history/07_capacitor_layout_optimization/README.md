# 07_capacitor_layout_optimization: Capacitor layout / OTA parasitic comparison

Development order: **7**. Date / ordering evidence: **Before MOS-only selection 2026**.

Historical layout-capacitance tradeoffs; does not qualify precision SC capacitors.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/layout_optimization_analysis/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Unchanged tuned OTA with layout-optimized capacitor models

Separate local comparison for the SCL800 OTA, preserving the published design_2 and earlier experiments. Capacitor layouts/generators live in ../../../capacitors/layout_optimization_v1; this folder contains only their OTA application and a frozen model snapshot.

## Outcome

The selected slotted 4p model (3.99574 pF mutual) produces approximately:

- Gain at 1 Hz: 88.77 dB; UGF: 742 kHz.
- Nominal phase margin: 69.23 degrees; minimum checked margin: 63.09 degrees.
- Worst 100 mV dynamic settling: 1.034 us; worst 2 V dynamic settling: 3.675 us.
- Static small-step tracking error remains approximately -0.206 mV.
- Quiescent power remains about 175 uW including the ideal reference branch; dynamic energy was not compared.

This compares with the previous baseline 8p model at about 364 kHz, 65.79 degrees nominal PM, 61.80 degrees minimum PM and 7.818 us large-step settling. The capacitor area decreases from about 0.799 mm2 (baseline 8p) to 0.1595 mm2 (slotted 4p). That comparison changes both capacitor geometry and value; same-capacitance layout comparisons are provided in the capacitor experiment's RESULTS.md.

The slotted 3p candidate gives 66.11-degree nominal margin but only 58.71 degrees at the worst checked point, so it fails the initial >=60-degree screen. Slotted 4p is the fastest qualifying choice among tested 3/4/8p variants, not a global optimum.

## Tests

Nine capacitor configurations (baseline/compact/slotted x near3/4/8p) with TOP=n2, BOT=out and SUB=vss. The eight-MOS core remains unchanged: M1/M2 W/L=7.5/2.4 um; M3/M4=10/3.2; M5/M8=20/3.2; M6=112/3.2; M7=160/3.2. Supply 5 V, 27 C, ideal reference current 2.5 uA.

81 AC cases span the full CL=1/5/10 pF x follower DC input1.5/2.5/3.5 V grid. 54 base transients cover small100mV and large2V steps at the three loads. Settling is last exit from +/-0.1% of the step amplitude around actual final output, worst polarity, measured from the start of each 10 ns input edge. Total error to ideal input is recorded separately: static error prevents meeting +/-100 uV total accuracy for the small-step test.

AC uses a 1e12 H DC feedback inductor and 1e12 F AC-ground capacitor; it estimates follower return ratio at the closed-loop DC operating point, not a full SC phase loop-injection test. AC uses 150 points/decade, 1 Hz--1 GHz. reltol=1e-5, vntol=1e-8, abstol=1e-12, numdgt=12. Transient max timestep=5 ns, duration90us, pulse plateaus40us. Selected large-step run repeated at1ns: worst settling changes by about3.39ns (~0.1%). This is a numerical repeatability check, not physical validation.

Native xschem extraction verified unchanged MOS connections/models/W/L and capacitor pin mapping. Extracted AC data match the parameterized hand netlist. Native follower testbench and selected portable SPICE benches were simulated. GUI clicks were not tested headlessly. Native demo inherits100ns edges; quantitative sweeps use10ns.

## Open and run

```bash
xschem --rcfile xschemrc tb/ota_layout_opt_tb.sch
```

The native schematic is designs/ota_layout_opt.sch. The local spice/models.inc points to the user's existing private SCL model file; no model cards are copied. For another machine update that include to an authorized local deck. Run selected_ac.cir, selected_small.cir or selected_large.cir from tb/. Capacitor models are frozen in models/cap_layouts.lib.spice.

Re-run the full comparison with:

```bash
python3 scripts/analyze.py --cap-project /path/to/capacitors/layout_optimization_v1 \
  --mos-model /path/to/tntp49_5v
```

scripts/finalize.py reconstructs/verifies the frozen schematic using the earlier local extracted-capacitor experiment as its reference template; its paths target this project's installed directories. The already-generated schematic/benches work independently of that reconstruction step. The capacitor project's report.py --ota-project /path/to/this/folder regenerates joint plots/tables. RESULTS.md and plots/ota_comparison.png/.pdf summarize all nine cases. Full numeric inputs, waveforms and logs are retained under results/.

## Limits

The capacitor extractor's installed Magic8.3.105 is below the PDK header's8.3.579 requirement, and native export drops a raw-.ext substrate capacitor. Frozen evaluation models retain the documented raw node/coupling records; that discrepancy is still unresolved. Slotted fringe/shielding behavior particularly needs a supported, reconciled extraction/independent validation flow. The transistor deck also emits ignored-HSPICE-parameter warnings. All dynamic numbers remain provisional.

Conductor resistance is NOT included in these capacitor models; the capacitor report's routing-R values are only geometric proxies. No PVT, mismatch, noise, dielectric loss/leakage/voltage coefficient, real reference generator, substrate noise, full SC switching, ADC kickback, OTA wiring parasitic extraction, startup or final-chip LVS qualification was performed. Capacitor DRC passes do not establish formal capacitor LVS or manufacturing acceptance. The 3.67 us large-step response still exceeds the illustrative2.45us SC amplification window; that window is not a finalized requirement.

No original geometry, shared library or published GitHub files were changed. This is a separately saved candidate and comparison; no push was performed.
