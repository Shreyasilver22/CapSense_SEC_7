# 16_sc_integrator_validation: SC integrator test with layout-v3 OTA

Development order: **16**. Date / ordering evidence: **30 October 2026**.

Assumed CS=2.5 pF, CF=7.5 pF, VREF=1.5 V; these are not the newly uploaded SCA values.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/sc_integrator_validation_20261030/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# SC charge-integrator validation with OTA physical_layout_v3

The simulated topology follows the supplied figure: phi1 connects TX to VP and RX to ground; phi2 grounds TX and connects RX to the OTA inverting summing node. CF remains between output and summing node. A reset switch shorts CF before each group of three integration cycles. OTA non-inverting input is VREF. Sensor CS represents CS0+delta CS.

## Assumptions, not finalized project specifications

- SCL08 nominal MOS cards, 5 V supply, 27 C.
- Actual OTA: nine PMOS compensation units, ideal Iref=3.5 uA, newly extracted v3 routing-capacitance model with physical finger/junction geometries.
- VREF=1.5 V; VP=0.3 V. This deliberate moderate excitation keeps three integrations within the previously checked OTA bias/output region. VP is a separate assumed driver voltage, not VDD.
- CS0=2.5 pF; delta CS=0/50/100 fF. CF=7.5 pF. These values are role assignments for this experiment, not a confirmed sensor or capacitor specification.
- Explicit output load 5 pF; nominal 50 kHz. Additional clock tests 25/100/200 kHz and nominal 10 pF load checks.
- Non-overlapping phi1/phi2 pulses, each about 43% of one period, with 10 ns edges. Two frames, three integration cycles per frame, one reset period between frames. Fifty-microsecond startup reset.
- Ideal-switch comparison: Ron=100 ohm, Roff=1e12 ohm. Transistor case: all five switches are CMOS transmission gates, NMOS W/L=10/0.8 um, PMOS=20/0.8 um, ideal complementary 0/5 V gate clocks; NMOS bulk=ground, PMOS bulk=VDD.
- CS and CF are ideal linear capacitors. Only the OTA compensation capacitor uses MOS devices. No claim is made that a suitable physical 7.5 pF SC feedback capacitor has been fabricated or verified.

## Analytical check

In phi1 the sensor RX plate charge is -CS*VP. In phi2 its final plate voltage is approximately VREF with TX=0, so the transferred charge is CS*(VP+VREF). Therefore each output increment is

    step = (CS/CF)*(VP+VREF)
    Vout(k) = VREF + k*step

For CS=2.5 pF and CF=7.5 pF, the step is 0.6 V: 2.1, 2.7 and 3.3 V after reset at 1.5 V. This circuit integrates the full baseline capacitance as drawn; it does not intrinsically cancel CS0. More cycles or a larger CS/CF ratio can saturate the OTA. Reversing the assumed 2.5/7.5 pF roles with these voltages would demand 5.4 V per cycle and is unsuitable on a 5 V supply.

## Measured nominal results, sampled late in phi2

| Amplifier / switches | Third-cycle output (V) | Maximum raw sample error (mV) |
|---|---:|---:|
| ideal / ideal | 3.299998 | 0.0022 |
| actual / ideal | 3.300245 | 0.2454 |
| ideal / tg | 3.355731 | 55.7311 |
| actual / tg | 3.356934 | 56.9367 |

The ideal-amplifier model is a zero-delay VCVS with finite gain 1e6, used only as an attribution control. Its output-stage power is not modeled, and the unused 3.5 uA reference branch remains connected; do not compare its supply power with the actual OTA.

With ideal switches the actual OTA's raw error is about 0.245 mV at 50 kHz. With transistor switches it is about 56.94 mV, or 3.16% of the ideal 1.8 V three-cycle excursion. A hypothetical 0.1% full-excursion accuracy budget would be 1.8 mV, so the raw transistor-switch circuit fails it. This budget is illustrative, not a finalized requirement. Summing-node error at sample times is approximately 0.16 mV, and late-phase output drift is only a few microvolts at 50 kHz. Most accumulated raw error persists with an ideal amplifier, identifying switch-related effects as the larger error source in this simulation. Charge injection, clock feedthrough and junction-capacitance effects have not been individually isolated.

## Clock and load checks

| Clock (kHz) | Actual OTA / ideal-switch maximum raw error (mV) | Actual OTA / TG maximum raw error (mV) |
|---|---:|---:|
| 25 | 0.2493 | 56.9040 |
| 50 | 0.2454 | 56.9367 |
| 100 | 0.2434 | 56.9704 |
| 200 | 0.2413 | 56.9775 |

The tested clock range does not materially change the raw offset; slowing the clock does not remove it. This does not establish a maximum operating clock. At 50 kHz and 10 pF load, raw error is 0.2452 mV with ideal switches and 56.8047 mV with transmission gates.

## Small sensor-change response

The following is numerical subtraction of the separately simulated nominal baseline at the same conditions, not an implemented on-chip cancellation circuit. It does not validate calibration across drift or mismatch.

| Sensor increase (fF) | Ideal third-cycle increase (mV) | Actual OTA + TG increase (mV) | Relative error of increase (%) |
|---|---:|---:|---:|
| 50 | 36.0000 | 36.0249 | 0.0690 |
| 100 | 72.0000 | 72.0556 | 0.0773 |

## Timestep, power and limitations

Nominal maximum timestep is 10 ns. Repeating both actual-OTA nominal switch cases with 2 ns leaves the ideal-switch third-cycle output unchanged at the displayed precision and shifts the TG result by about 0.014 mV, much less than the 56.9 mV raw error. Raw logs and separate timestep measurements are retained.

The waveform plot limits the summing-node error axis to +/-10 mV to show the settled behavior; larger switching spikes are clipped in that panel and remain in the raw data. Output traces also show transient switching undershoot; late-phase samples alone do not characterize those spikes.

Actual OTA + TG VDD power averages about 177.8 uW at nominal 50 kHz. This VDD-current metric excludes power delivered by the ideal VREF/VP sources and ideal clock drivers; it is not total readout or ASIC power.

Conclusion: for this assumed three-cycle, moderate-swing test the OTA's nominal speed is adequate over the tested clocks. The complete transistor-switch circuit is not accurate enough without addressing switch-related errors and baseline handling. Next steps are switch sizing/timing optimization, explicit sensor/routing parasitics, reset/baseline cancellation, and the real ADC/noise/timing budget.

The source OTA model uses the documented extraction-only import adaptation. Full-RC substrate errors and missing qualified well/substrate-junction extraction remain unresolved. The local ngspice translation ignores some PDK/HSPICE parameters, so quantitative clock-feedthrough/charge-injection conclusions are provisional. Sensor/package parasitics, switch interconnect extraction, capacitor voltage dependence/matching, thermal/flicker noise, leakage over temperature, PVT/mismatch, real references/drivers, and an attached ADC were not included. No claim of silicon qualification or final ASIC performance is made.

## Files

summary.csv/json: 28 base simulation results including per-cycle samples; timestep.json: two 2 ns checks; plots/sc_waveforms.png/pdf and sc_accuracy.png/pdf: plots; results/: actual decks, logs and time-series data; models/ota_C_only.spice: newly extracted v3 OTA (proprietary model cards referenced locally); scripts/simulate.py, check_timestep.py and report.py: reproduction; tb/: portable relative-model nominal decks. Run nominal decks from tb using ngspice -b. Scripts regenerate full-result benches using the current project location. Existing raw benches reference their staging paths. No PDK sources were altered and no GitHub publication was performed.
