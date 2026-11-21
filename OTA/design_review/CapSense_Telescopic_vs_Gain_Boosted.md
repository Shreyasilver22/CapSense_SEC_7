# CapSense OTA comparison

The 1.70 V value is the retuned NMOS booster reference. Both OTA architectures target 2.5 V output common-mode at a 5 V supply. The standalone comparison used nominal SCL08 MOS and RPP models, 27 °C, 3.5 µA reference current and 5 pF per output for AC and noise.

## Nominal results at 1.5 V input common-mode

| Metric | Final telescopic | Original gain boost, 1.10 V | Retuned gain boost, 1.70 V |
|---|---:|---:|---:|
| Near-DC differential gain (dB) | 88.53 | 129.51 | 129.66 |
| Open-loop gain at 10 kHz (dB) | 43.04 | 44.59 | 44.63 |
| Open-loop −3 dB bandwidth (Hz) | 53.006 | 0.566 | 0.559 |
| Unity-gain bandwidth (MHz) | 1.419 | 1.698 | 1.704 |
| Differential phase margin (°) | 89.41 | 89.45 | 89.46 |
| OTA power (µW) | 231.96 | 226.83 | 227.03 |
| Input-pair saturation margin (mV) | 1054.5 | 529.1 | 1120.3 |
| 0.2 V step settling (µs) | 0.836 | 0.726 | 0.719 |
| 2 V step settling (µs) | 7.928 | 3.496 | 3.806 |
| 2 V step late differential error (mV) | 0.3299 | 0.0007 | 0.2477 |
| 2 V step late output common-mode error magnitude (mV) | 32.57 | 9.60 | 9.60 |
| Input-referred spot noise at 10 kHz (µV/√Hz) | 4.088 | 4.106 | 4.090 |
| Input-referred spot noise at 1 MHz (nV/√Hz) | 409.5 | 412.2 | 410.5 |

## Nominal results at 2.5 V input common-mode

| Metric | Final telescopic | Original gain boost, 1.10 V | Retuned gain boost, 1.70 V |
|---|---:|---:|---:|
| Near-DC differential gain (dB) | 87.53 | 84.81 | 128.31 |
| Open-loop gain at 10 kHz (dB) | 43.15 | 34.92 | 44.77 |
| Open-loop −3 dB bandwidth (Hz) | 60.238 | 31.955 | 0.664 |
| Unity-gain bandwidth (MHz) | 1.437 | 0.557 | 1.732 |
| Differential phase margin (°) | 89.41 | 87.51 | 89.44 |
| OTA power (µW) | 233.04 | 227.81 | 228.11 |
| Input-pair saturation margin (mV) | 283.5 | −237.3 | 349.9 |
| 0.2 V step settling (µs) | 0.832 | 1.912 | 0.721 |
| 2 V step settling (µs) | 7.870 | 4.668 | 3.795 |
| 2 V step late differential error (mV) | 1.4679 | 0.1466 | 1.1081 |
| 2 V step late output common-mode error magnitude (mV) | 32.54 | 9.60 | 9.59 |
| Input-referred spot noise at 10 kHz (µV/√Hz) | 4.047 | 95.261 | 4.043 |
| Input-referred spot noise at 1 MHz (nV/√Hz) | 405.4 | 9547.4 | 405.8 |

Settling is the worst edge among both outputs, measured in a band of ±0.1% of the commanded step amplitude around each attained output level. The small step uses 5 pF per output and the large step uses 10 pF. Noise density is from stationary open-loop AC noise simulations. Total clocked SC noise, including switching, reset, and folding, remains unmeasured.

## Common-mode limits and selected corners

| Metric | Final telescopic | Original gain boost, 1.10 V | Retuned gain boost, 1.70 V |
|---|---:|---:|---:|
| Gain at 10 kHz, 0.5 V input CM (dB) | −17.13 | −15.66 | −15.57 |
| Gain at 10 kHz, 0.8 V input CM (dB) | 33.29 | 34.83 | 34.87 |
| Tail saturation margin, 0.8 V input CM (mV) | −107.2 | −107.3 | −107.2 |
| Gain span at 2.5 V input CM (dB) | 86.34–90.78 | 76.71–106.48 | 127.91–130.73 |
| UGBW span at 2.5 V input CM (MHz) | 1.311–1.447 | 0.232–1.340 | 1.570–1.736 |
| OTA power span at 2.5 V input CM (µW) | 209.5–255.6 | 193.6–239.8 | 195.0–240.3 |
| Minimum input-pair margin at 2.5 V input CM (mV) | 277.2 | −514.8 | 62.3 |
| Worst common-mode loop phase margin (°) | 85.49 | 70.04 | 70.04 |
| Worst 2 V step settling at 2.5 V input CM (µs) | 8.507 | 8.013 | 4.397 |

The selected conditions are typical at 5 V and 27 °C, BNWP with the worst resistor model at 5.5 V and 85 °C, and WNWP with the best resistor model at 4.5 V and 0 °C. Output CM follows half the supply in this test. CMFB margins include 1.5 V and 2.5 V input CM at balanced output and 1 V differential command. Tail saturation is lost below approximately 1.08 V for all three in the nominal sweep. The retuned auxiliary gates recovered to a ±100 µV band within 0.29 µs in the tested pulse transients. Full auxiliary-loop, mismatch, and layout verification remain pending.

## Nominal 10 kHz SC readout

One external 10 kHz clock, TX discharge at 0 V, RX precharge at 2.5 V, ideal 40 pF feedback per branch, 5 pF live output load and 10 pF hold capacitance per side. Results are sampled at 81 µs into the second cycle. OTA power includes the OTA bias current at an ideal reference, with clock and external reference circuits excluded.

| Metric | Final telescopic | Original gain boost, 1.10 V | Retuned gain boost, 1.70 V |
|---|---:|---:|---:|
| Held differential output, 12/7 pF (mV) | 505.734 | 506.048 | 506.027 |
| Local Cp sensitivity at 12/7 pF (mV/pF) | 96.00 | 96.14 | 96.15 |
| Held CM error, 12/7 pF (mV) | −2.215 | 0.458 | 0.458 |
| Settling slack before track ends, 12/7 pF (µs) | 7.82 | 7.95 | 7.98 |
| Average OTA power, 12/7 pF (µW) | 236.8 | 231.7 | 231.9 |
| Held CM error, 15/15 pF (mV) | −0.297 | −0.157 | −0.157 |
| Minimum OTA input CM, 15/15 pF (V) | 0.891 | 1.004 | 1.004 |

## Design decision

Keep the final telescopic as the baseline. The 1.70 V retuned OTA is a candidate if an ADC common-mode requirement or system noise budget calls for a change. It improves gain, large-step settling and nominal held common-mode. The nominal sensitivity and spot-noise improvements are small, and the simulated power difference may disappear when the 1.70 V reference circuit is included.

[Retuning plots](CapSense_OTA_Gain_Boost_Retuning.png) · [Retuning simulation data](CapSense_OTA_Gain_Boost_Retuning_Results.csv) · [Supplemental simulation data](CapSense_OTA_Comparison_Supplemental.csv)
