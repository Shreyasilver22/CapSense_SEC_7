# Final telescopic OTA with the 10 kHz switched-capacitor readout

The two branch capacitors are CP and CN. The P branch returns OUTP to SUM_P at OTA INN, and the N branch returns OUTM to SUM_N at OTA INP. The test uses the released SC netlist with native transmission gates and the capacitance-extracted OTA. Nominal conditions are 5 V, 27 °C, typical MOS and RPP models, 40 pF feedback per branch, 5 pF load per output, and a 2.5 V output common-mode target. RX transfer starts 1 µs before TX discharge, the clock ramps are 1 µs, and reset follows phi1. Samples are taken at 480 µs, or 80 µs into the fifth cycle.

Nine complementary cases cover CP − CN from −2 to +2 pF at CP + CN = 12 pF. The fitted slope is 163.009 mV/pF, versus 163.043 mV/pF by ideal charge balance. The intercept is +0.284 mV and the maximum residual from the fitted line is 9.04 µV. The local slope from ±50 fF differential perturbations near 7/5 pF is 162.971 mV/pF. At 7/5 pF the simulated differential output is 326.294 mV versus 326.087 mV ideal. A 5 ns timestep rerun changes the sampled differential output by 0.19 µV relative to the 20 ns run.

At 7/5 pF the sampled input and output common-mode voltages are 1.52007 V and 2.49834 V. The last-cycle ranges are 0.476–2.502 V at the input and 1.246–2.595 V at the output. In the balanced sweep from 5/5 to 7/7 pF, sampled input common-mode drops from 1.665 to 1.383 V while sampled output common-mode stays near 2.499 V.

## Noise scope

Ngspice .noise linearizes the circuit with the transfer switches held in their settled state. Ideal voltage sources through large inductors reproduce the sampled node biases at DC. All transmission gates remain in the noise circuit. The tabulated spectra are diagnostics for this fixed operating point. At 7/5 pF the raw integration from 1 Hz to 10 kHz gives 442 mV differential RMS, 7.46 mV output common-mode RMS, and 191 mV input common-mode RMS. The differential integral is dominated by the lowest frequencies. Moving the lower bound from 1 Hz to 100 Hz reduces the differential integral to roughly 4.5 mV over the remaining band. Results inherit the PDK translation warnings in the logs and depend on the fixed-phase model and the way DC bias is held. The clocked circuit periodically resets, so these results cannot serve as its sampled noise floor or capacitance resolution.

The ideal sensor sampling contribution alone is sqrt(kT(CP+CN))/CF = 5.57 µV differential RMS at 27 °C, or about 34 aF when divided by nominal sensitivity. This calculation assumes independent sensor sampling noise and omits feedback reset noise, OTA and reference noise, clocked noise folding, and physical capacitor parasitics. Quantitative total sampled noise needs a clocked noise analysis.

Run python3 run.py and python3 plot.py from this folder with ngspice, NumPy, Matplotlib, and the Linux final design and PDK at the paths in run.py. CSVs contain nominal results, a timestep cross-check, one clock cycle, and the held-phase noise spectra and integrals.

The clocked sensor-only calculation also uses transient simulations. The script sensor_noise.py injects small positive and negative charge perturbations across each sensor after phi1 opens and before RX transfer, then measures their propagation to the sample. The resulting sensitivities are weighted by independent kT/C variance. This gives 5.555 µV differential RMS, 2.411 µV input common-mode RMS and 0.0271 µV output common-mode RMS for that contribution alone. Run with python3 sensor_noise.py. The held-phase differential noise integral from 1 Hz to 10 MHz changes from 442 mV at 10¹² H to 442 mV at 10¹⁵ H, and to 455 mV at 10⁹ H.


## Reproduction

This archive includes the original intermediate experiments and their results.
Archived scripts that refer to a local PDK or historical Linux workspace need
their paths updated on a different system. For the current reproducible
testbench, use [the integrated SC + OTA project](../integrated_sc_ota).
