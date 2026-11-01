# 13_extracted_compensation_retuning: Extracted MOS-compensation retuning

Development order: **13**. Date / ordering evidence: **30 October 2026**.

Capacitor-count and reference-current tradeoffs on the compact extracted model.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/extracted_retuning_20261030/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA extracted-capacitance retuning — 30 October 2026

Recommended next layout candidate: ten PMOS compensation units (each W=20 um, L=10 um) at the existing ideal reference current of 2.5 uA. This favors stability margin. Eight units at the same current are the smallest tested count meeting 60 degrees across the main grid, and are faster. Actual switched-capacitor timing and power requirements remain unspecified, so neither is declared globally optimal.

## Actual simulations

ngspice was run on the physical_layout_v2 capacitance-extracted model with five equivalent counts (6,7,8,10,12) and five reference currents (1.5,2,2.5,3.5,5 uA). The main grid contains 225 AC runs: each combination at 1/5/10 pF and follower DC inputs 1.5/2.5/3.5 V. Supply 5 V, temperature 27 C. Thirty transient tests cover five finalists at the three loads and 100 mV/2 V input steps. Twelve further AC tests check 4 V input or hypothetical extra output loading. One 1 ns timestep repeat checks the recommended candidate's 10 pF large step.

| Candidate | Iref (uA) | Minimum PM in main grid (deg) | Nominal UGF (MHz) | Nominal supply power (uW) | 2 V step settling at 10 pF (us) |
|---|---:|---:|---:|---:|---:|
| Existing 6 units | 2.5 | 55.56 | 1.091 | 126.44 | 2.958 |
| Minimum-change 8 units | 2.5 | 61.99 | 0.843 | 126.44 | 3.463 |
| Recommended-margin 10 units | 2.5 | 66.28 | 0.684 | 126.44 | 4.098 |
| Fastest nominal UGF passing grid: 8 units | 5 | 60.24 | 1.290 | 252.39 | 1.855 |
| Lowest power passing grid: 7 units | 1.5 | 60.47 | 0.666 | 75.99 | 4.993 |

Nominal means 5 pF explicit load and 2.5 V input. Minimum PM spans all nine load/bias combinations and is not nominal PM. Supply power was measured directly as -5*I(VDD), including the ideal reference branch, in this extracted-model sweep. It replaces assumptions from older schematic-power summaries for this comparison; practical bias-generator overhead is absent.

Ten units have nominal gain 89.60 dB, nominal PM 73.22 degrees, 100 mV settling 1.030 us at 5 pF and 1.140 us at 10 pF. Large-step settling is 4.034 us at 5 pF and 4.098 us at 10 pF. The 1 ns maximum-step repeat gives 4.09828 us versus 4.09838 us with 5 ns, agreeing to 0.00011 us. Settling is measured to 0.1% of the applied step around actual final output, with 10 ns input edges. Final static error is recorded separately; this is not a total ADC accuracy or complete SC-loop qualification.

## Stress results and decision

At 10 pF load, 2.5 V bias, and an additional hypothetical 3 pF output capacitor, ten units retain PM=63.65 degrees; eight units at 2.5 uA fall to 59.00 degrees. These added loads are sensitivity cases, not measured or extracted well capacitance. They do not cover all stress/load/bias combinations.

At 4 V input and 5 pF load, ten units give only 53.15 degrees PM (eight units: 47.30 degrees). High-output-voltage operation remains unresolved. Higher current alone worsens phase margin in the tested grid. The highest-speed passing option has very little reserve and falls below 60 degrees with only 1 pF extra output loading. The lowest-power passing option also has little reserve. Thus ten units at 2.5 uA are the preferred candidate when no tighter settling requirement has been supplied.

Ten units correspond to about 4.13 pF intrinsic modeled gate capacitance at the earlier nominal gate bias, versus 3.30 pF for eight and 2.48 pF for six. Actual incremental capacitance remains bias dependent.

## Modeling boundaries

This is a WHAT-IF sizing study, not a new physically extracted layout. The six capacitor branches in the verified v2 C model are scaled by m=N/6, including their modeled junction geometry contributions; all explicit extracted routing capacitances remain fixed. This provides an equivalent total gate area/count for screening. New routing, contacts, extra wells and their parasitics must be regenerated in the next layout revision. Existing v2 DRC/LVS results do not validate the proposed ten-unit layout.

The source model uses the documented extraction-only import filtering workaround. Full-RC substrate errors, missing qualified well-junction extraction, ngspice model-translation warnings, PVT, mismatch and actual SC loading remain open. No physical layout or PDK file was modified and nothing was pushed to GitHub.

## Files

- models/baseline.spice: copied v2 extracted C netlist; no proprietary transistor model cards.
- models/n6.spice through n12.spice: equivalent-count study models.
- ac_sweep.csv/json: all 225 main AC measurements.
- candidates.csv/json, selection.json: nominal and worst-grid comparisons.
- transients.csv/json, timestep_check.csv/json: settling and convergence checks.
- stress.csv/json: high-bias and hypothetical-load tests.
- results/: native benches, data and simulator logs.
- plots/retuning.png/pdf: phase-margin and step-response comparisons.
- scripts/run.py, finish.py: reproduce the sweep and finalist tests/plots. The model include points to the local SCL08 model installation. Saved benches use staging paths; rerunning scripts regenerates them using their current project location. Selected portable benches in tb/ use relative project model paths.
