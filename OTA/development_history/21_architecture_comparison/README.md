# 21_architecture_comparison: Alternative OTA architecture comparison

Development order: **21**. Date / ordering evidence: **31 October 2026**.

Basic fully differential, telescopic, folded, gain-boosted telescopic and class-AB prototypes versus the two-stage baseline.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `architecture_exploration_20261031/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# SCL800 OTA architectural exploration — 31 October 2026

Five new transistor-level alternatives were constructed and actually simulated in ngspice 42 against the current extracted-capacitance OTA. These are first-pass architectural candidates, not new tapeout-qualified designs. The original OTA and SC circuit were not edited. No GitHub publication was performed.

## What was built

- `fully_diff`: simple NMOS differential pair with PMOS current-source loads and continuous-time CMFB. This is a low-gain control, not a two-stage fully differential implementation.
- `telescopic`: NMOS input pair, NMOS and PMOS cascodes, PMOS source loads, continuous-time CMFB.
- `folded`: NMOS input pair, PMOS folding branches, cascoded NMOS sinks, continuous-time CMFB.
- `gain_boosted`: telescopic core with four finite-bandwidth transistor auxiliary amplifiers regulating both NMOS drain nodes and both PMOS source nodes. These are not ideal gain blocks. NMOS targets 1.1 V; PMOS targets VDD minus 1.2 V.
- `class_ab`: two-stage single-ended amplifier followed by diode-level-shifted complementary source followers. Both output devices conduct at rest and transient output current increases during steps. The internal second-stage sink uses four units, the PMOS second stage four units, the output followers eight units each, compensation ten W20/L10 PMOS units and nominal 16 kohm native RPP.
- `baseline`: prior 12-cap/28k/16-finger-PMOS C-extracted design, unchanged.

These are overlapping architectural choices: all three cascode candidates are fully differential and include CMFB. Only the class-AB prototype retains the tested single-ended interface of the current SC circuit. The differential candidates were tested with a differential external feedback interface. They could also be investigated using only one output in the current SC circuit, with the complementary output maintained by CMFB, but that changes gain, loading and loop behavior and has not been verified here. These differential performance numbers must not be applied to that untested connection.

## Nominal measured results

5 V, 27 C, typical native MOS/resistor models, input common mode 1.5 V for differential candidates, output common mode 2.5 V, CL=5 pF **per output** for AC. A fully differential candidate therefore drives two external load capacitors. Settling uses CL=10 pF per output and a 2 V step on each output. Fully differential command steps -2 to +2 V; outputs ideally exchange 1.5 and 3.5 V.

| Candidate | Gain (dB) | UGF (MHz) | Power (uW) | 10 pF settling (us) |
|---|---:|---:|---:|---:|
| Current OTA (extracted C) | 91.9 | 0.918 | 176.8 | 4.264 |
| Basic fully differential | 40.3 | 2.472 | 285.7 | 1.998 |
| Telescopic + CMFB | 88.4 | 1.696 | 180.9 | 3.491 |
| Folded cascode + CMFB | 83.1 | 1.691 | 264.4 | 4.067 |
| Dual-side gain-boosted + CMFB | 129.5 | 1.698 | 226.8 | 3.492 |
| Class-AB buffered two-stage | 89.5 | 0.873 | 136.6 | 3.423 |

Gain is measured at 0.001 Hz, UGF interpolated at the downward unity crossing. Settling is the worst of both edges and both output pins, to within 2 mV of each pin's final value (0.1% of its 2 V step). **Static error is separate; a short settling time does not imply accurate absolute output.** See `comparison.csv` for both common-mode and differential final errors.

The class-AB and telescopic 10 pF steps were repeated with a 1 ns maximum step: class-AB 3.419 us versus 3.423 us at 5 ns; telescopic 3.491 us versus 3.491 us. These confirm the nominal timing measurement, not transient PVT qualification. `timestep_check.json` retains exact values.

The extra schematic-only current-OTA control measures gain 91.91 dB, UGF 0.858 MHz and power 176.84 uW. Its geometry is also estimated; the extracted baseline remains the reliable physical comparison.

## Corner and feedback checks

246 main AC cases: each architecture has one nominal case plus 40 combinations of five native MOS files, VDD 4.5/5.5 V, temperature 0/85 C, CL 1/10 pF, centered output CM 2.5 V. These are assumed exploratory ranges, not established chip requirements or reliability limits. Resistor corner is typical in this study.

240 additional output-level checks: the same endpoint MOS/supply/temperature grid, CL10 pF, output setpoint 1.5 or 3.5 V. For differential cores these change **both outputs' common-mode setpoint**, not the individual output endpoints of an opposite-polarity signal. Large-signal transient testing separately checks the latter at nominal conditions. A large DC tracking error invalidates the intended operating point even if a phase margin is returned.

8 nominal feedback-loop checks plus 160 endpoint feedback-loop checks: CMFB return is injected symmetrically at its sensing gates, keeping its compensation network connected. The four gain-booster loops are individually voltage-injected with other loops closed. These are engineering small-signal loop diagnostics, not a formal multi-loop Nyquist/pole-count certification. CMFB loops are measured from 100 Hz to avoid ill-conditioning of the DC-closing fixture; low-frequency gain in those records is gain at 100 Hz.

- Current OTA (extracted C): center-CM differential PM minimum 99.27 deg; output-CM/end-point minimum 63.53 deg; largest DC output-CM tracking error 1.06 mV.
- Basic fully differential: center-CM differential PM minimum 90.31 deg; output-CM/end-point minimum 90.39 deg; largest DC output-CM tracking error 684.87 mV. Additional CMFB/booster loop screening minimum 74.03 deg.
- Telescopic + CMFB: center-CM differential PM minimum 88.57 deg; output-CM/end-point minimum 89.47 deg; largest DC output-CM tracking error 689.17 mV. Additional CMFB/booster loop screening minimum 60.96 deg.
- Folded cascode + CMFB: center-CM differential PM minimum 84.41 deg; output-CM/end-point minimum 87.81 deg; largest DC output-CM tracking error 674.53 mV. Additional CMFB/booster loop screening minimum 71.95 deg.
- Dual-side gain-boosted + CMFB: center-CM differential PM minimum 88.76 deg; output-CM/end-point minimum 89.61 deg; largest DC output-CM tracking error 684.51 mV. Additional CMFB/booster loop screening minimum 61.35 deg.
- Class-AB buffered two-stage: center-CM differential PM minimum 75.44 deg; output-CM/end-point minimum 11.04 deg; largest DC output-CM tracking error 362.24 mV.

Simulation execution failures in these final datasets: 0. Completion means that data was generated, not that a design met accuracy, stability or headroom requirements. All unity crossings are retained in JSON; no case is discarded for a poor result.

## CMFB development and remaining cost

An initial two-differential-pair detector lost common-mode control for large differential signals: each pair became fully steered. These rejected results are retained in `uncompensated_*` records. Direct 100k resistive averaging also loaded the high-impedance outputs and destroyed cascode gain. The final prototype buffers each output with a PMOS source follower, averages buffered voltages with two **1 Mohm native RPP** resistors, and compares against an identically shifted reference using a transistor error amplifier.

Its local compensation is four PMOS units to VDD plus eight PMOS Miller units from its control node to each output. It consumes extra current and loads the differential outputs capacitively. Source-follower nonlinearity introduces signal-dependent CM offset; the nominal 2 V pin steps show about 10 mV common-mode error in the cascode prototypes, which must not be mistaken for differential signal error. Two 1 Mohm poly resistors and many MOS compensation units may be expensive in area and parasitics. No compact CMFB layout has been demonstrated here.

## Interpretation and next design choice

The simple fully differential core has insufficient gain for a precision integrator. Telescopic is a useful speed/power candidate **if input common mode is held near 1.5 V**; the saved 2.5 V input-CM check exposes its headroom/gain loss. Folded cascode preserves input-CM flexibility but consumes more current in these initial sizes. Gain boosting raises matched-model low-frequency gain greatly but does not improve the dominant load-limited bandwidth or nominal large-step settling much over telescopic, and adds four loops and ideal bias references. Its very high gain is a simulation result, not a promised fabricated gain.

Class-AB retains the existing single-ended interface and shows useful nominal power/settling improvement, but this source-follower implementation fails the full assumed output/supply screen: inspect `range_screen.json` for low-supply/output endpoint failures and DC swing limitations. Its output loses rail headroom. It needs an output-stage/bias revision before layout. The nominal improvement cannot be extended to all PVT conditions. No architecture is yet selected as the optimum.

For fully differential SC redesign, compare telescopic against folded cascode after compact CMFB/bias optimization and extracted layout. The current single-ended OTA remains the physical reference until a new candidate passes the complete required signal-range, PVT, noise and extraction checks.

## Model and comparison limitations

- Original native SCL08 five LEVEL49/BSIM3 5 V MOS files were included directly, plus native typical `ppr`. No PDK model card was copied into this package. The existing ngspice model-translation/ignored-parameter warnings remain; raw noise is not qualified and no architecture noise ranking is claimed.
- Intentional compensation uses real PMOS devices; resistors use native `RPP`. External test loads and feedback/DC-closing fixtures are ideal testbench elements.
- New MOS instances have **estimated** source/drain areas W*4.5 um and perimeters 2*(W+4.5 um), per unit device. These estimate junction loading; they are not extracted geometry. Defaults with zero junction area were retained only as preliminary results in `pre_junction_estimates/` and are excluded from final comparison.
- New candidates have no routed interconnect/well/substrate extraction, DRC, LVS, matching layout or Monte Carlo verification. The baseline already includes adapted-extractor routing capacitances and previously documented resistor-body capacitance. This difference can favor the new schematics.
- Ideal external 3.5 uA reference, noiseless cascode/reference voltage supplies, ideal CM reference. Power includes modeled VDD core/controller/booster currents but excludes a real reference generator, external reference/clock drivers and their noise. Current allocations and total output loads are not equal across architectures; these results are not a global optimization or an equal-power proof.
- No transient PVT qualification, SAR/SC integration of the new architectures, capacitor matching, noise budget, PSRR/CMRR qualification or physical area claim. The original SC circuit is unchanged.

## Reproduction and files

`models/`: uniquely named exported candidate subcircuits and the original extracted baseline. `tb/`: standalone nominal AC and large-step decks. From `tb`, run `ngspice -b -o folded_ac.log folded_ac.cir` (or another candidate). AC data and log are saved locally. PDK is expected at `/home/berson_meshak/pdk/scl08/ngspice_models49`.

All twelve exported standalone decks (AC and transient for six designs including the baseline) were separately simulated and their data matched the generator-run results. See `export_verification.json`; PASS there means export equivalence, not specification compliance.

`scripts/study.py`: transistor generator and measurement; `validate.py`: main screening and nominal loops; `stress.py`: output-range and loop stress; `report.py`: export/report/plots. Run validate, stress, then report in that order. Raw generation benches in `results/` preserve their original execution paths; regenerate using scripts after relocating. The standalone `tb/` decks use relative local model includes.

Plots: `plots/ac_comparison.png`, `plots/transient_comparison.png`, `plots/power_and_class_ab.png` (PDFs also supplied). `comparison.json/csv` contains compact metrics. Raw simulation logs and data are under `results/`. Exploratory tags such as `initial`, `tune_*`, `buffer_*` and `cm_comp_test` are intermediate trials, not final candidates. The final selected parameters are `validate.PARS` and exported `models/`.

Conceptual background: [Analog Devices, multistage and cascode configurations](https://wiki.analog.com/university/courses/electronics/text/chapter-10), and [C. G. Myers, pipeline ADC thesis (gain boosting and common-mode control)](https://web.engr.oregonstate.edu/~moon/research/files/Charlie_Myers.pdf). Numerical findings above come from this project's saved simulations, not those references.
