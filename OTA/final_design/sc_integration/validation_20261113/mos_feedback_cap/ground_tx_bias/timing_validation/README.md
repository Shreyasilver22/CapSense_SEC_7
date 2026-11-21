# SC and OTA validation without a SAR ADC

The simulations use the 10 kHz SC readout, the capacitance-extracted telescopic OTA, 121 PMOS units per feedback branch (49.92 pF nominal), and 4.5 µA OTA reference current. Unless specified, TX transfers to ground, the supply is 5 V, the output common-mode target is 2.5 V, and each output has a 5 pF load. The result is sampled at 80 µs of the second cycle. The timing sweep changes the rise time of the TX discharge switch control at 46 µs. TX voltage itself falls in response to the transmission gate. RX lead is measured between the starts of the two gate commands. Both transfer commands finish falling at 91 µs. The slow edges are ideal clock voltage ramps rather than a transistor-level driver.

## Timing, corners, and loading

The timing sweep covers 1, 2, 4, and 8 µs TX control ramps and 1, 2, and 3 µs RX leads at 12/7 and 12/12 pF. The candidate uses the 8 µs ramp and 3 µs lead. At nominal 12/12 pF its RX minimum is essentially ground, versus −0.460 V with the original 1 µs ramp and 1 µs lead. Its minimum output common-mode is 1.736 V versus 0.645 V. At 12/7 pF it delivers 631.17 mV differential, settles within the defined band in 7.33 µs, and draws 308 µW from the main supply, including the SC and OTA. A 10 ns timestep rerun changes the nominal 12/7 pF sample by 0.48 µV.

Across four selected process, supply and temperature combinations at two sensor pairs, the original 1/1 timing gives a worst RX minimum of −0.703 V and a maximum absolute selected junction-current integral of 41.5 fC. The 8/3 timing reduces those excursions to −0.0195 V and 0.283 fC, with worst differential settling of 8.88 µs. The integrated absolute junction currents are diagnostic, and include leakage. The 4 µs ramp with 1 µs lead still allows about −0.135 V at the selected corners. The 8 µs ramp with a 1 µs lead gives similar sampled performance and −0.0207 V worst RX. The 2 V TX comparison uses the same capacitor and bias and achieves similar RX excursion bounds in this subset, with lower nominal differential output at 462.75 mV.

With the 8/3 timing, increasing equal static output loads from 2 to 20 pF changes the 12/7 pF sample by less than 1 µV. Worst nominal settling is 10.47 µs across the tested loads and the two sensor pairs. Settling is measured from the TX command to the last entry within a band of 0.1% of the 88 µs value, with a 100 µV minimum band. A static capacitor tests analog drive and settling. A switched capacitor or lumped charge pulse is needed to model kickback.

## Identifying the remaining error

With the slower timing still in place, the largest sampled error at 12/7 pF relative to the nominal feedback capacitance charge-balance prediction is 50.52 mV across the four selected corners. Replacing the PMOS bank with an ideal capacitor of the same nominal value reduces it to 0.295 mV. This control isolates the modeled feedback-bank effect.

Next simulate jitter and skew using a transistor-level clock driver, feedback-bank mismatch and leakage with extracted well and interconnect parasitics, and sampled output noise including the OTA, reset switches and clock source. A resolution target requires the minimum sensor capacitance change and signal bandwidth. More process, supply, and temperature combinations are needed before treating the measured limits as design bounds.

Run python3 check.py, python3 calibration.py and python3 plot.py. The standalone ground_tx_slow_edge.cir uses the installed Linux PDK and final OTA macro. Results are ngspice simulations with ideal bias and clock sources.
