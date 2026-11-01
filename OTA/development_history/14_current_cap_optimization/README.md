# 14_current_cap_optimization: Current versus MOS-capacitor optimization

Development order: **14**. Date / ordering evidence: **30 October 2026**.

Nine units / 3.5 uA balanced candidate under provisional screening limits.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/current_cap_optimization_20261030/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Current versus MOS compensation optimization — 30 October 2026

This study refines the current/capacitance tradeoff after the previous ten-unit choice slowed settling. It varies equivalent PMOS capacitor count and ideal reference current, preserving transistor sizing in the OTA core and the physical_layout_v2 routing-capacitance model.

The refined grid is N=8/9/10/11 with Iref=3/3.5/4/4.5/5 uA, plus six-unit/2.5 uA, eight-unit/2.5 uA and ten-unit/2.5 uA comparison points. Every pair has nine AC cases: CL=1/5/10 pF and follower DC input=1.5/2.5/3.5 V. Supply=5 V, temperature=27 C, local SCL08 transistor model, ngspice. Each pair has 100 mV and 2 V follower transient tests at 10 pF. Finalists have 2 V transients at 5 pF and a 1 ns timestep repeat at 10 pF, plus separate high-bias and extra-load stress AC checks.

## Selection criteria

All 23 pairs are retained so the user can change the objective. The study labels a candidate passing when its minimum phase margin across the nine checked points is >=63 degrees: a provisional three-degree reserve over the earlier 60-degree target. The balanced choice is the fastest large-step candidate within a provisional 180 uW supply-power ceiling. Neither 63 degrees nor 180 uW is a finalized ASIC requirement. A separate >=65-degree choice is also reported. Bandwidth is measured at the nominal 5 pF, 2.5 V point. Phase margin below is the worst of all nine AC points. Power includes the ideal current-reference branch, excluding a practical reference generator.

| Candidate | MOS units | Iref (uA) | Power (uW) | Nominal UGF (MHz) | Minimum PM (deg) | 100 mV settling at 10 pF (us) | 2 V settling at 10 pF (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Existing six-unit baseline | 6 | 2.5 | 126.44 | 1.091 | 55.56 | 1.355 | 2.958 |
| Previous ten-unit margin choice | 10 | 2.5 | 126.44 | 0.684 | 66.28 | 1.140 | 4.098 |
| Balanced study choice | 9 | 3.5 | 176.84 | 0.937 | 63.51 | 1.066 | 2.805 |
| Fastest at >=63 degrees | 10 | 5 | 252.39 | 1.048 | 64.67 | 0.730 | 2.221 |
| Fastest at >=65 degrees | 11 | 5 | 252.39 | 0.958 | 66.37 | 0.800 | 2.362 |

Settling uses a 0.1% band about actual final output for each applied step, worst of rising/falling edges, not total ideal conversion accuracy. Input transitions are 10 ns, transients 90 us, maximum step 5 ns except explicit repeats. Static final errors are recorded in transients_10p.csv. Power and speed must ultimately be assessed with the actual SC feedback factor and settling window.

## Limits and interpretation

This is a what-if sizing simulation using the previous extracted C model. Six capacitor branches are scaled by multiplicity N/6, including their existing junction geometry terms. Fixed extracted routing capacitances are not regenerated for changed array size. Larger arrays require new layout, DRC/LVS and extraction before these numerical advantages can be relied on. The source extraction uses the previously documented marker-import workaround; qualified well-junction capacitance/diode behavior and full RC remain unresolved. Model-translation warnings, PVT, mismatch, complete SC circuit loading, and physical current-reference overhead remain open. No PDK files were modified and no GitHub publication was performed.

Hypothetical extra 1 pF output-load tests are sensitivity checks, not estimates of well capacitance. The 4 V input tests remain outside the main selection grid; consult stress.csv before assuming high-swing operation. Passing a sparse nominal grid does not establish continuous-range or process-corner qualification.

## Files

all_candidates.csv/json: complete tradeoff table; ac_grid.csv/json: all 207 main-grid AC results; transients_10p.csv/json: 46 large/small transient results; selection.json: objective and choices; selected_checks.csv/json: repeat/5 pF settling; stress.csv/json: finalist checks; plots/current_cap_tradeoff.png/pdf: speed/power comparison; results/: native benches, logs and data. models/: sizing-study models without proprietary transistor cards. scripts/engine.py, transient.py and optimize.py reproduce the work against the local SCL08 installation. scripts/document.py builds this report and relative-path finalist benches in tb/. Saved raw benches reference staging paths; rerunning the scripts regenerates those paths from the current project directory.

## Finalist stress measurements

| Units | Iref (uA) | Load (pF) | DC input (V) | Extra hypothetical load (pF) | PM (degrees) |
|---:|---:|---:|---:|---:|---:|
| 10 | 5 | 10 | 2.5 | 1 | 64.27 |
| 9 | 3.5 | 10 | 2.5 | 1 | 63.04 |
| 11 | 5 | 10 | 2.5 | 1 | 66.01 |
| 10 | 5 | 5 | 4 | 0 | 46.87 |
| 9 | 3.5 | 5 | 4 | 0 | 47.30 |
| 11 | 5 | 5 | 4 | 0 | 49.38 |
