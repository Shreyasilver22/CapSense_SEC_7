# PVT and reference-drive verification for the 2.5 V TX/RX readout

The candidate uses 2.5 V TX discharge, 2.5 V RX precharge, the extracted-capacitance OTA macro, an ideal 4.5 µA OTA reference current, a nominal 50 pF PMOS feedback bank per branch, and a 10 pF hold capacitor per output. The single 10 kHz testbench clock has nominal 50% duty cycle. The behavioral phase generator preserves the timing across corners and scales the switch gates to the supply. OTA cascode biases are ideal, with VBN fixed at 3.0 V and VBP at VDD minus 2.2 V.

The PVT screen covers the five SCL08 MOS model cards. It pairs 4.5 V and 5.5 V with 0 °C / best RPP and 85 °C / worst RPP, and includes 5 V / 27 °C / typical RPP. It covers 12/7 pF and 12/12 pF. This is a selected engineering screen with no resistor-only extremes or mismatch distribution. Nominal reference-drive tests compare the Thevenin source resistance and bypass capacitance with shared or split CMFB reference wiring. The split model drives OTA VCM from a clean ideal 2.5 V source and uses the finite-impedance node for TX, RX, and hold precharge. Transient clock/bias implementation, reference buffer stability, noise, layout routing, and SAR loading remain open.

Common-mode extrema cover 40–70 µs within the final simulated cycle. Held voltages are evaluated at 81 µs. The held differential shift compares 81 µs with the live differential value at 79.5 µs. Reference peak deviation is measured over the whole final clock cycle. Headroom is the minimum native BSIM3 |VDS| minus |VDSAT| for each path during transfer and at 75–79 µs while tracking. Transient loop gain and noise are outside this screen.

Run `smoke`, `pvt`, `reference`, `followup`, `tx-slew`, and `combined` with `sweep.py`. Use the same `--work` directory so the follow-up can select the worst completed PVT cases. For example, run `python3 sweep.py pvt --work /tmp/sc_vcm` from this directory. Then run `python3 plot.py /tmp/sc_vcm` to regenerate the figures. Each case writes its netlist, log, and waveform to its subfolder. The scripts use the local SCL08 PDK and OTA paths in `base.cir`. ngspice reports inherited warnings about unsupported HSPICE model parameters.

### Initial operating point

Four of 50 baseline runs stopped at the transient operating point. Both capacitance pairs at 5.5 V and 85 °C failed for the `bnbp` and `wnbp` cards. The original baseline runs used algebraic behavioral equations for the supply-scaled clock amplitudes. The supplied generator uses equivalent linear gain sources for these fixed-supply tests. Tests with the longer TX ramp apply an ideal startup reset for the first 2 µs and report later cycles. Resolving the failed cases and designing the physical startup circuit remain open. The 1 kΩ split reference case at the cold, high-supply stress point also timed out. These cases remain in the CSVs with their respective statuses.

### Candidate timing and reference drive

Stretching the TX gate-control ramp from 8 µs to 20 µs improves the confirmed `bnwp` hot corner at 5.5 V and 12/12 pF. The 20 µs ramp starts at 46 µs and completes at 66 µs. Acquisition begins at 70 µs from the same 10 kHz clock. The combined screen used a 50 ns maximum time step with a second-cycle measurement. Initial 20 ns attempts on this combined setup stalled. The 8 µs reference stress reruns used a 20 ns step and measured the third cycle.

| Worst confirmed hot case | Output CM minimum | Minimum PMOS load margin | Peak reference deviation |
|---|---:|---:|---:|
| 8 µs TX control, ideal reference | 2.150 V | −74 mV | 0 mV |
| 20 µs TX control, ideal reference | 2.269 V | +66 mV | 0 mV |
| 20 µs TX control, 50 Ω source | 2.271 V | +68 mV | 17.7 mV |

The ideal reference in the completed baseline PVT runs absorbed up to 374 µA and supplied up to 18 µA. A 50 Ω source is a first-pass drive target based on selected simulated loads and an approximately 20 mV peak reference deviation budget. The physical reference driver and the 20 µs phase generator still require circuit implementation and broader corner verification.
