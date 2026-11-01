# 02_behavioral_system_model: Behavioral SC / OTA / SAR model

Development order: **2**. Date / ordering evidence: **Before 28 October 2026**.

Supporting system model; not a transistor-level PDK simulation.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_1/behavioural_model/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# SC / OTA / SAR behavioural model — version 1

This extends the idea in `C:\Users\HP\Untitled1.ipynb` without changing that notebook. It supports parameterized SC charge conversion, clock phases, finite OTA gain, slew-limited settling, residual offset/charge injection, sampled Gaussian noise, output headroom and a generic ideal SAR. It is a reduced model to derive conditional requirements, **not an SCL transistor simulation or measured sensor model**.

## Files and use

- `notebooks/SC_OTA_ADC_behavioural_v1.ipynb`: walkthrough with saved outputs and editable experiment settings.
- `config.json`: default illustrative scenario and explicit assumptions.
- `scripts/sc_model.py`: equations and simulation functions.
- `scripts/run_analysis.py`: plots, numerical sweeps, summary and conditional requirements.
- `scripts/check_model.py`: analytical/limiting-case checks.
- `plots/`: six PNG/PDF figure pairs.
- `results/`: transfer/sweep CSVs, SUMMARY.md, summary.json, config_used.json and provenance.

From this folder:

```sh
python3 scripts/check_model.py
python3 scripts/run_analysis.py
jupyter notebook notebooks/SC_OTA_ADC_behavioural_v1.ipynb
```

Requires Python, NumPy and Matplotlib; the notebook additionally uses IPython/Jupyter for display. No new packages were installed for this work. The saved notebook plots can be viewed before rerunning cells. Notebook experiments pass their own config explicitly to the analysis function; the default file remains unchanged. Each run replaces generated outputs in plots/ and results/; copy a scenario folder first if you want to preserve multiple experiments.

## Explicit SC architecture assumed

For lack of physical sensor data, choose a complementary bridge:

- Cp = C, with C from 5 to 10 pF.
- Cn = 15 pF − C, also 10 to 5 pF.
- Midpoint C0=7.5 pF.
- Each branch has the same feedback capacitor Cf.
- An ideal excitation step Vexc charges each sensor capacitor during sampling. Ideal switching transfers the differential stored charge into the feedback capacitors during amplification. Clock polarity/connections are chosen to make increasing Cp produce positive differential output.
- Each feedback capacitor/output is reset to common mode in the default sampling/reset phase. The model assumes this reset is ideal and complete; there is no input waveform tracking or analog memory across sampling intervals.

Define Vdiff=Vout+−Vout−. With ideal charge transfer,

Qdiff=Vexc(Cp−Cn),

Vdiff,ideal=Qdiff/Cf=2 Vexc(C−C0)/Cf.

This is an assumed switched charge-amplifier architecture, not a netlist of the existing SC prototype. It must be checked against the final switch connections. Baseline subtraction is differential: both nominal sensor charges cancel at Cp=Cn. There is no arbitrary endpoint scaling in the analog core.

Defaults Vexc=1 V and Cf=3.0303 pF per branch produce 0.66 V/pF sensitivity, matching the original notebook's slope. The original unipolar 0–3.3 V coordinate is now represented as **−1.65 to +1.65 V differential**. It can be recovered algebraically as Vdiff+1.65 V; this does not imply adding a physical output summing stage.

At VCM=2.5 V:

Vout+=VCM+Vdiff/2 and Vout−=VCM−Vdiff/2.

The ideal output legs span 1.675–3.325 V. The ADC is treated as an ideal differential converter accepting Vdiff from −1.65 to +1.65 V. The 5 V supply limits model headroom only; changing it does not automatically change excitation or ADC full scale.

## Clock and switch model

The illustrative clock is 200 kHz (5 µs period), with a nominal half-period for sampling and half for amplification. Subtract 50 ns overhead from each phase, giving 2.45 µs usable time in each. No overlap is allowed.

Each sensor capacitor is assumed to start discharged in the sampling model, with a constant switch resistance Ron. The acquired charge is

Qp=Vexc Cp [1−exp(−Tsample/(Ron Cp))],

and likewise for Qn. Differential acquired output is (Qp−Qn)/Cf. Ron=0 gives complete acquisition. This neglects the actual voltage dependence, multiple series switches, reference impedance and parasitics of a transistor switch network. Sensor capacitance is quasi-static during each conversion.

The `hold_previous` option retains the previous deterministic output as the initial amplification state instead of resetting to zero differential. It is useful for reversal stress testing. It is **not** an exact charge-conserving model of a non-reset integrator: such a circuit needs its own recurrence and switch-state equations. Prior stochastic noise is not propagated between cycles in this option. `initial_differential_kick_v` allows a specified kick but does not predict charge redistribution from physical parasitics.

SAR comparison cycles are instantaneous in this model. The 200 kHz SC clock does not establish a feasible end-to-end ADC throughput: acquisition, hold/extra storage, SAR clock cycles and scheduling need a separate timing budget. The phase waveform includes explicit sample/reset and amplification clocks, not a transistor-level clock generator.

## OTA model

For the symmetric differential screening model, use the nominal per-branch C0 and lumped input capacitance:

beta=Cf/(Cf+C0+Cin+Cpar), A0=10^(gain_dB/20), k=A0 beta/(1+A0 beta).

This assumes sufficiently controlled input/common-mode behavior. Actual per-branch parasitics, capacitance dependence and asymmetric/common-mode coupling are not solved. Differential steady target is the acquired charge-transfer output times k, plus residual input offset multiplied by approximately k/beta and user-specified residual differential charge injection times k/Cf. Offset is a **residual after any CDS/calibration**, not proof that CDS removes the specified device offset.

Output response follows the intentionally simple equation

dVdiff/dt=clip[(Vtarget−Vdiff)/tau, −SRnegative, +SRpositive],

tau=1/(2 pi beta fu).

This equation is integrated analytically through slew and exponential regions, avoiding timestep-dependent settling. SR is specified for the **differential output** in V/µs. UGF and SR are assumed at the stated load; they are not calculated from device sizing/current. A reported Ceff=CL+Cf(1−beta) is informational and does not secretly rescale UGF when CL changes. Supply/headroom clipping is applied separately from ADC range saturation.

CMFB is explicitly ideal: it fixes the output mean to VCM, with no common-mode pole, startup or recovery prediction. `cmfb_assumed_ideal=false` raises an error instead of pretending a nonideal CMFB is implemented. One-pole settling cannot predict phase margin, ringing or a multistage compensation zero. Actual OTA validation must include these effects.

## Noise model

The optional sampled charge-noise approximation is

sigma_Qdiff² = n_samples kB T (Cp+Cn),

sigma_Vdiff,SC² = k² sigma_Qdiff²/Cf².

It assumes independent equilibrium sample-charge noises on the two sensor capacitors. n_samples=2 is a tunable approximation for two uncorrelated white-noise samples in CDS. It does not simulate CDS clock-dependent correlations, flicker suppression, noise folding or the final circuit's exact kT/C factors. Finite sampling-time changes to noise variance are not modeled.

OTA sampled input-referred noise is separately specified as a differential rms voltage and mapped to the output with approximately k/beta. This parameter represents the already integrated/sampled **OTA-only** contribution; it must not also contain the SC charge noise if that option is enabled, or noise is counted twice. Independent Gaussian samples are drawn with a fixed seed for reproducibility. No noise spectrum or SCL noise model is implied.

## ADC correction

The original notebook used a hard-coded DAC denominator 255. Here the ideal SAR uses 2^N levels and thresholds Vmin+code*(Vmax−Vmin)/2^N. It supports arbitrary configured bit count, clips out-of-range inputs and matches an ideal floor quantizer. Therefore it intentionally differs from the original endpoint-based 255 convention. At 10 bits and a 3.3 V span, one nominal LSB is 3.222656 mV and one capacitance bin is 4.8828125 fF for the assumed linear transfer. Neither is a demonstrated physical resolution.

## Error accounting and conditional targets

Keep separate:

1. Acquisition error from incomplete sampling charge.
2. Finite-gain static error.
3. Residual offset and charge injection.
4. Dynamic error at sampling relative to the actual final target.
5. Sampled random noise and headroom clipping.
6. ADC quantization and range clipping.

The report derives a gain minimum from the configured finite-gain allowance and signal amplitude. It solves a worst-case differential reversal with the exact scalar slew/exponential model to obtain a minimum UGF at configured SR; no solution is reported when slew alone makes the deadline impossible. The allocations (0.125 LSB each for finite gain, dynamic settling and residual offset; 0.1 LSB rms noise) are illustrative engineering choices. They are not a complete statistical/system error budget and do not guarantee all samples lie within half an LSB. Sampling-switch error, mismatch, references, comparator noise and other budgets must still be allocated.

No power, energy, pressure resolution, DNL/INL, ENOB, Monte Carlo silicon yield or PDK performance is claimed. Plots compare model assumptions; they are not ngspice results. The original project requirements are not automatically replaced by the conditional results.

## Literature basis

The reason to track sampled static/dynamic error, capacitive feedback and phase history comes from the locally reviewed papers, particularly Ruiz-Amaya et al., *Accurate Settling-Time Modeling and Design Procedures…*, TCAS-I 2009 (DOI 10.1109/TCSI.2008.2008509), and the 2007 SC Miller power-optimization paper. This implementation is a deliberately simplified screening model; it does **not** implement their full event-driven, output-dependent, multistage model.
