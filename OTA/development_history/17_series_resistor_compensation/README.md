# 17_series_resistor_compensation: Series-resistor / MOS compensation study

Development order: **17**. Date / ordering evidence: **31 October 2026**.

Six units plus 16 kohm ideal resistor screening; later physically implemented separately.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/architecture_study_20261031/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA architectural improvement study — 31 October 2026

The SC design is unchanged. This study compares an OTA compensation-topology modification quantitatively and assesses subsequent core-architecture directions. It does not claim that class-AB, cascode or fully differential cores have been implemented or simulated.

## First tested architectural change: series-R MOS compensation

The current direct compensation path is N2 -> PMOS gate capacitance -> OUT. The candidate introduces one series resistor between N2 and a common capacitor-gate node GCOMP; capacitor sources/drains/bodies stay OUT. The OTA core transistor geometries and ideal reference current remain unchanged. Six equivalent W20/L10 um PMOS units plus RNULL=16 kohm were the fastest large-step candidate among the tested transient finalists satisfying >=65 degrees across the main grid.

    RNULL N2 GCOMP 16k
    MCAP OUT GCOMP OUT OUT P W=20u L=10u M=6

The series resistor modifies the compensation zero and pole locations. It can improve phase margin without increasing compensation capacitance, allowing smaller gate area and higher speed. This principle is described in the primary teaching source: https://iic-jku.github.io/analog-circuit-design/slides/ota_diff.html (Miller compensation/zero discussion). The numerical benefit below is from actual local ngspice simulation, not inferred from the source.

## Actual comparisons

5 V supply, 27 C, ideal reference Iref=3.5 uA. Nominal point: 5 pF explicit output load, follower DC input 2.5 V. Minimum PM spans CL=1/5/10 pF and DC input=1.5/2.5/3.5 V. All models retain physical_layout_v3 core device/junction geometry and extracted routing C. MOS-count changes and added resistor are what-if modifications, not re-extracted layouts.

| Parameter | Existing 9-unit direct compensation | 6 units + 16 kohm |
|---|---:|---:|
| Nominal DC gain (dB) | 87.57 | 87.57 |
| Nominal unity-gain bandwidth (MHz) | 0.936 | 1.412 |
| Nominal phase margin (degrees) | 71.04 | 81.71 |
| Minimum checked phase margin (degrees) | 63.26 | 69.71 |
| Nominal VDD supply power (uW) | 176.84 | 176.84 |
| 2 V settling at 5 pF (us) | 2.616 | 1.913 |
| 2 V settling at 10 pF (us) | 2.815 | 1.962 |
| 100 mV settling at 5 pF (us) | 0.576 | 0.676 |
| 100 mV settling at 10 pF (us) | 1.081 | 0.651 |

Bandwidth improves about 51%; large-step settling at 10 pF improves about 30%. Not every parameter improves: small-step settling at 5 pF is about 17% slower. DC gain and nominal DC power are unchanged in this model. Intentional nominal MOS compensation is about 2.48 pF rather than 3.71 pF, using the earlier gate-bias characterization; capacitance is bias dependent. Gate area decreases from 1800 to 1200 um2, but total layout area including the new resistor is unknown.

Twenty-four models were screened (N=6/7/8/9; R=0/1k/2k/4k/8k/16k), giving 216 main AC cases. The top four nominal-UGF candidates under each of >=63- and >=65-degree grid filters, plus baseline, received small/large-step tests at 5 and 10 pF. Selection is the fastest 10 pF large-step result among the tested >=65-degree finalists, not a global optimum over all resistor values or architectures. Main transients use 5 ns maximum timestep, 10 ns edges, 90 us duration, and 0.1% settling around actual final output. A 1 ns repeat gives 1.96054 us versus 1.96200 us, agreeing within about 0.0015 us. Static final errors are recorded separately; full conversion accuracy has not been assessed.

## Stress and unresolved issues

With 10 pF explicit load plus a hypothetical extra 3 pF at OUT, at 2.5 V bias, selected-candidate PM is 65.35 degrees. Extra 1 pF gives 68.71 degrees. These extra loads are sensitivity checks, not extracted well-capacitance estimates and not a full bias/load stress grid.

At 4 V input and 5 pF load, PM is only 44.18 degrees, compared with 46.80 degrees in the baseline. This modification does not solve high-output-voltage stability and slightly worsens that stress case. MOS capacitance bias dependence and OTA headroom need separate investigation before extending the operating range.

RNULL is an ideal resistor here. No physical SCL resistor type, geometry, voltage coefficient, resistor noise or resistor routing parasitics has been validated. Transient tests do not include thermal/flicker noise; adding a resistor can change the noise budget. Existing DRC/LVS checks apply to the old direct-compensation layout, not this new topology. New models use nine physical extracted capacitor branches scaled by N/9 to represent count. Their MOS gates are rerouted to GCOMP while old explicit parasitic capacitors retain their v3 node connections. This is a screening approximation; gate-route parasitics must be reassigned and re-extracted in a real layout.

Known extraction-only marker-import adaptation, missing qualified well-junction extraction, substrate errors in full-RC extraction, and ignored HSPICE model parameters remain. There is no PVT/mismatch, noise, practical bias/reference, updated physical-layout, or full system qualification. The SC circuit and its switch-related accuracy limitation were not altered or re-optimized.

## Other architecture directions: proposals, not simulated results

1. Class-AB output stage or adaptive bias: next candidate when large-step settling per quiescent power is the main objective. It provides signal-dependent drive but needs a proper quiescent-current controller and checks of crossover distortion, recovery, additional poles and stability. Keep a single-ended output to retain the current SC interface. TI's LMV60x primary datasheet is an example of class-AB/complementary-output CMOS design: https://www.ti.com/lit/gpn/lmv604 . Its product performance is not a prediction for our SCL08 design.
2. Cascoded first stage, then optional gain boosting: a direction for higher DC gain/output resistance. Stacked devices consume voltage headroom, introduce bias requirements and internal poles, and do not automatically improve large-step speed. Primary source: https://iic-jku.github.io/analog-circuit-design/slides/ota_improved.html and https://iic-jku.github.io/analog-circuit-design/slides/cascode.html . Our current gain is already about 87.6 dB; establish the accuracy/noise budget before paying for more gain.
3. Fully differential OTA with CMFB: useful only if the system adopts a differential signal interface. It requires common-mode loop verification and changes to the current single-ended SC connection, so it is deferred while SC is held unchanged. Primary source: https://iic-jku.github.io/analog-circuit-design/slides/ota_diff.html . CMFB controls output common-mode; it is not itself a guarantee of higher differential gain.

Recommendation: retain the existing OTA/layout as baseline; treat six MOS units plus 16 kohm as the first compensation-topology candidate for implementation. If a larger core change is needed afterward, compare a class-AB output stage at a matched quiescent-power budget. Do not label it an improvement until stability, small/large-step behavior, noise and current are simulated.

## Files and reproduction

selection.json: selected and baseline measurements; ac_grid.csv/json: all main AC cases; candidates.csv/json: AC screening; all_candidates.csv/json: transient finalist measurements; transients.csv/json: sampled step tests; stress.csv/json and fine.csv/json: checks; models/: actual trial netlists without proprietary transistor model cards; results/: decks, data and logs; tb/selected.cir and baseline.cir: relative-include runnable 10 pF large-step benches; plots/compensation_comparison.png/pdf: comparison plot. Run portable benches from tb using ngspice -b selected.cir. scripts/compare.py and finalize.py reproduce experiments and plots with the local SCL PDK model include. Raw result decks reference staging paths; regenerating scripts resolves paths for their current directory. No PDK sources were altered or GitHub publication performed.
