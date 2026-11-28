# CapSense finalized schematic revision

The selected front end uses programmable IREF, the SCL08 transistor-level input common-mode controller, and the telescopic OTA. This release is the verified flat SPICE bench. Fabrication sign-off remains open.

[Measured plots](results/capsense_integrated_iref.png) · [Integrated cases](results/integrated_cases.csv) · [Legacy startup](results/startup_legacy.csv) · [Trimmed startup](results/startup_trimmed.csv) · [Clock trim screen](results/clock_trim_screen.csv)

The tested circuit combines the existing switched-capacitor readout, the NMOS-VCR telescopic OTA, transistor-level input common-mode correction, the existing track-and-hold, and the new 8-bit MOS IREF. Both comparison decks use the same MOS midpoint reference and VBN/VBP fanout. The legacy deck sources IREF from the existing bias mirror. The candidate deck removes that output device and supplies the same OTA bias node from the clocked trim mirror. The feedback banks use the project default of 60 PMOS units per branch.

## Nominal comparison

Matched TT, 5.00 V, 27 °C, one 10 kHz clock and a 30 µs power ramp. Each transient runs 25 cycles. Sensitivity is the differential endpoint slope for CP = 7.82–11.79 pF at CN = 10 pF. Power comes from integrating the actual VDD rail waveform over a full settled cycle, including sensor excitation.

| Measurement | Legacy IREF | Programmable IREF |
|---|---:|---:|
| Live output sensitivity at 85 µs | 94.303 mV/pF | 94.353 mV/pF |
| Held output sensitivity | 94.301 mV/pF | 94.344 mV/pF |
| External ADC fixture sensitivity | 72.923 mV/pF | 72.956 mV/pF |
| Rail power at CP = 11.79 pF | 3.4042 mW | 3.4194 mW |
| IREF at CP = 11.79 pF | 3.3600 µA | 3.2794 µA |
| Input common mode at CP = 11.79 pF | 2.50132 V | 2.50140 V |
| Output common mode at CP = 11.79 pF | 2.50008 V | 2.50007 V |

At CP = 11.79 pF the trim design adds 15.2 µW (0.45%) to the main rail. With CP = CN = 10 pF it produced +0.004 mV differential output. Swapping the 11.79 pF and 10 pF sensor branches changed the output from +146.686 to -146.680 mV.

At the nominal high point, cycle-average IREF first remained inside 3.024–3.696 µA from cycle 15. The live output remained within the larger of 1 mV and 1% of its final value from cycle 14, compared with cycle 6 for the legacy bias. The cycle-16 live sample differed by -0.158 mV from the earlier 80 ns maximum-step run with the same trim, point, and rail ramp.

Integrated IREF accuracy is evaluated using cycle averages. The nominal trimmed high-point cycle shows instantaneous bias-node currents of 2.80–7.51 µA. The [per-cycle data](results/startup_trimmed.csv) record the minimum and maximum separately. The trimmed waveform is outside the ±10% band for approximately 58 ns in the measured 100 µs cycle, near the 42.6 µs clock transition. Review the bias-current transients with the extracted clock and OTA.

## Regulated-rail corner checks

The same CP = 11.79 pF and CN = 10 pF pair was used for both corner checks. The sensor sensitivity above is based on the nominal endpoint sweep. The corner values below measure a single sensor point. The 8-bit IREF word comes from the previous room calibration for each modeled process. The three-bit phase-clock word is a separate control.

| Corner and setting | Bias code | Clock code | Track window (µs) | IREF mean (µA) | Held differential (mV) | Rail (mW) | Nominal probe tracks at 85 µs |
|---|---:|---:|---|---:|---:|---:|---|
| SS, 0 °C, 4.95 V, nominal clock code | 147 | 3 | 53.85–68.90 | 3.127 | -0.00 | 3.384 | No |
| SS, 0 °C, 4.95 V, adjusted clock code | 147 | 0 | 69.00–84.60 | 3.127 | +0.01 | 3.385 | No |
| SS, trim IREF, earlier ADC trigger | 147 | 0 | 69.10–84.65 | 3.104 | +132.47 | 3.383 | No |
| SS, legacy IREF, earlier ADC trigger | — | 0 | 69.10–84.65 | 3.966 | +132.47 | 3.408 | No |
| SF, 85 °C, 5.05 V, nominal clock code | 57 | 3 | 86.30–≥95 | 3.514 | +362.72 | 5.112 | No |
| SF, 85 °C, 5.05 V, adjusted clock code | 57 | 5 | 64.90–92.50 | 3.514 | +381.19 | 6.043 | Yes |
| SF, legacy IREF, adjusted clock code | — | 5 | 64.90–92.50 | 2.796 | +381.24 | 5.951 | Yes |

The nominal ADC fixture probes at 89 µs. With the cold code the hold capacitor had already been precharged by the old trigger. Moving the probe to 86.6 µs gave +132.47 mV on the hold capacitors and +102.44 mV at the ADC fixture with trimmed IREF. With the hot code the ADC probe moves to 94 µs, after tracking ends at about 92.50 µs. The held hot differential was +381.19 mV with trimmed IREF and +381.24 mV with the legacy source under the matched timing. The project still needs a corner-calibrated acquisition schedule and a transfer check across sensor values at temperature. The analog held output is evaluated one microsecond before each probe. Power includes the additional precharge-buffer drive enabled by clock code 5.

## Run the nominal SPICE bench

Use ngspice with the local SCL08 0.8 µm model cards. Run from this release directory.

```bash
export SCL08_MODELS="$HOME/pdk/scl08/ngspice_models49"
bash run_ngspice.sh
```

The bench runs 25 cycles at 10 kHz with CP = 11.79 pF, CN = 10 pF and IREF code 115. The driver loads the installed model cards and generates the local simulator input and output files. CMEMP and CMEMN in [bench.cir](bench.cir) set the capacitances. XREFGEN in [support.spice.in](support.spice.in) supplies VREF and IREF. The held analog measurement is v(pinp) minus v(pinn).

## Work before fabrication

1. Sweep both sensor capacitances at cold, nominal and hot conditions. At the tested hot point both current sources produced about 381 mV held versus about 147 mV nominal. Establish the calibrated transfer and verify output range across the sensor.
2. Implement storage for the measured IREF trim and provide a clock/acquisition schedule. The bench uses 86.6 µs, 89 µs and 94 µs ADC probes at the selected cold, nominal and hot settings. The nominal master clock stays at 10 kHz.
3. Bring the editable Xschem hierarchy up to this netlist revision and reproduce the transfer measurement. Prior project runs showed different absolute sensitivity between the Xschem and flat-deck ordering.
4. Verify extracted full-chip timing and parasitics, mismatch, and sampled noise with the intended board and ADC load.
