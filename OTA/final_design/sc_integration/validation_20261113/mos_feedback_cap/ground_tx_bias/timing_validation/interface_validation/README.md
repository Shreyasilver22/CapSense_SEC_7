# SC and telescopic OTA interface stress tests

The baseline is the 10 kHz SC circuit with TX transfer to 0 V, an 8 µs TX switch-control ramp, a 3 µs RX lead, OTA IREF = 4.5 µA and 121 gate-at-output PMOS devices per feedback branch. Both output loads are 5 pF before adding the switched acquisition fixture. The evaluation point is 80 µs into cycle two.

The feedback-bank study changes PMOS unit count to impose a known difference and adds equal capacitors to ground at the summing nodes to screen sensitivity to well and routing capacitance. The imposed changes are deterministic stress cases. A foundry mismatch model and actual well extraction are needed to estimate yield.

The acquisition fixture uses one capacitor per output and ideal voltage-controlled switches with 100 Ω on-resistance. Precharge opens near 65 µs, then track begins at 70, 76 or 78 µs. The fixture reads both capacitor voltages at 80 µs before the modeled track switch opens. The results cover charge sharing and recovery through the chosen acquisition time. They exclude turn-off charge injection, comparator kickback, and SAR conversion. Errors are relative to the unloaded ADC interface at the same model corner. The SC itself still has 5 pF per output in the control.

Run python3 stress.py, python3 trim.py and python3 plot.py in this folder. The scripts reuse the surrounding timing study and installed SCL08 models. The trim fixture uses an ideal linear parallel capacitor on the smaller branch as a diagnostic for static offset correction. No physical trim device is included.

## Results and design implications

A 122/120 bank mismatch shifts the 12/12 pF sample by −23.99 mV relative to matched banks. Adding an ideal 0.8251 pF to the smaller bank brings the balanced sample from −23.653 mV to +0.332 mV, within 5 µV of the matched result. The unequal sensor pairs retain up to 4.36 mV of error after trim alone. With both the ideal trim and two-point gain/offset correction, the three nominal holdout pairs are within 0.85 µV of the matched simulation. Without trim, the same correction leaves up to 8.79 mV on those pairs. These results assume exact trim and same-condition calibration. They do not establish practical trim resolution or tracking.

Equal 1 pF and 3 pF shunts per summing node shift the nominal 12/7 pF sample by +1.98 mV and +5.74 mV. Increasing both banks from 121 to 127 units shifts it by −25.26 mV. This makes bank extraction and matching higher-priority than further OTA bias tuning.

A second acquisition fixture uses native SCL08 transmission gates with 0.5 µs control edges. At 10 pF per output, precharging to 2.5 V and beginning track at 70 µs gives a captured differential error of −1.79 µV at the 80 µs evaluation. The same precharge and a 78 µs track start give −2.19 mV. With 0 V precharge and a 70 µs start the error is −0.152 mV. The 2.5 V precharge also reduces the largest common-mode disturbance from 526 mV to 22 mV for the 10 pF, 70 µs case. One selected 4.5 V/85 °C MOS corner with 2.5 V precharge and 70 µs start gives −1.77 µV acquisition error relative to its own unloaded baseline. All 12 native fixture cases completed. Ten cases in the separate abrupt ideal-switch sweep failed to converge after retries and are recorded in failed_cases.csv. Those failures are not evidence of physical instability.

Use python3 native_load.py to regenerate the transmission-gate results. The standalone native_load_10pf.cir runs the 10 pF, 2.5 V precharge, 70 µs case. To translate the 80 µs acquisition result into an ADC timing requirement, include the actual hold transition and its charge injection. Total sampled noise and physical clock/reference generation remain open.
