# SCL08 clock trim and reference power revision

The clock uses one external 10 kHz input. Three static CMOS trim bits select two end resistors on a common poly resistor string. The selected arms set the offset and voltage span of its seven timing thresholds. Each arm uses a native SCL08 switch transistor. The trim value is set before the clock starts. A production design still needs a way to store or load the trim code.

The default choices for the screened cases are decimal 0 (cold/low supply), 3 (nominal), and 5 (hot/high supply). The remaining codes include settings for the alternate MOS cards at nominal supply. The trim ratio inputs in `trim_profiles.json` define the nominal interior taps and the endpoints of each code. The corresponding poly lengths and decoder transistors are in `blocks.spice`.

The comparator's first CMOS buffer uses longer-channel devices to reduce the current when its analog input is close to the inverter threshold. RX opening is interlocked with a delayed copy of the actual reset release. The TX slew, precharge, feedback cap banks and 10 pF hold loads follow the preceding single-clock design. The reference driver uses lower continuous tail and output sink currents and retains the PMOS bypass bank. The upper trim codes enable a second NMOS sink branch for higher switching loads.

`ota_bias.spice` is a separate transistor-level prototype that generates VBN, VBP and IREF from a clean 2.5 V input. The baseline clock and power comparisons keep ideal OTA biases for comparability. The bias prototype regulates VBN and uses a regulated resistor current and mirrors for the other biases. The clean master reference is still an external input to the prototype and an ideal source in the testbench. A master reference generator, bias-current trim and startup/layout qualification remain separate work.

## Simulation

From this directory, regenerate the macro with `python3 build.py blocks.spice --profiles trim_profiles.json`. `check.py` generates clock, integrated and bias tests using the preceding Linux OTA project fixtures and the local SCL08 model paths. For example, `python3 check.py integrated /tmp/sc08_trim_run blocks.spice --codes 0 3 5 --jobs 3` generates and runs the selected full readout cases. The `--cycles 2 --klu` options run two cycles using ngspice's KLU solver. `clock` and `duty` exercise the clock separately. Each saved deck writes `trace.dat` in its working directory. Copy `blocks.spice` and, for bias tests, `ota_bias.spice` to that directory if necessary.

Track and reset timing use half-supply crossings. Held output is measured at 81 µs in the measured cycle. Reference error is the largest absolute deviation from the 2.5 V master in that cycle. Power is the average supply power over a 100 µs cycle. The design runs use native MOS and RPP models, an extracted-capacitance OTA, and schematic-level clock, trim and reference circuitry. The model compatibility warnings, alternate solver outcomes and any incomplete cases are recorded in the logs or CSV status columns.

## Verified measurements

| Selected case | Trim code | Track window (µs) | Previous power (mW) | Revised power (mW) | Peak reference error (mV) |
|---|---:|---:|---:|---:|---:|
| Cold 4.5 V / 0 °C, 12/7 pF | 0 | 70.18–79.95 | 4.55 | 2.27 | 8.12 |
| Nominal 5 V / 27 °C, 12/7 pF | 3 | 69.79–79.97 | 6.25 | 2.71 | 10.14 |
| Hot 5.5 V / 85 °C, 12/12 pF | 5 | 69.78–80.75 | 15.83 | 4.94 | 14.67 |

All eight first-cycle integrated cases in `integrated.csv` completed. The largest first-cycle reference error was 18.62 mV for the nominal 12/12 pF case. With the hot code, reset passed half supply at about 45.00 µs and RX opened at 45.17 µs. The standalone nominal clock tracked at 69.79–79.98 µs for both 40% and 60% input duty cycle. The hot 12/7 pF second-cycle rerun held 235.15 mV and used 4.94 mW. Four other two-cycle KLU cases reached the wall-time limit and are listed in `integrated_two_cycle.csv`.

In the three integrated bias-fanout tests, VBN was about 2.999 V and VDD − VBP was 2.179–2.214 V. Reference current was 4.52 µA nominal, 5.36 µA cold and 3.71 µA hot. The fanout itself used 0.30–0.32 mW. Production trim-code storage, reference generation, layout parasitics, mismatch and broader PVT qualification remain open.
