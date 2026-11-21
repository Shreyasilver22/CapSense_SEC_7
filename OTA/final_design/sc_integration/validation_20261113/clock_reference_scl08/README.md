# SCL08 single-clock and reference-driver prototype

`blocks.spice` contains the `phase08` and `refbuf08` transistor-level subcircuits. The integrated decks use the existing SCL08 OTA extraction, native MOS and RPP models, 2.5 V TX discharge and RX precharge, and a 10 pF hold load per output. The clock block receives only one timing signal, CLK_IN at 10 kHz.

## Timing and reference circuits

- The clock detects CLK_IN rising with a CMOS edge detector, resets a MOS timing capacitor, and reads the discharge ramp with transistor comparators and a poly resistor ladder. Logic masks internal transfer and track during the ramp reset. Current-limited drivers slew the TX discharge and recharge edges. A delay between transfer-off and reset gives the TX switches time to turn off. RC shaping slows the hold-precharge edges.
- The unity-gain reference buffer uses an NMOS differential pair, a PMOS output device and an NMOS sink biased continuously. The buffer supplies the switched 2.5 V node. OTA CMFB senses the quiet master reference. The master 2.5 V source, OTA bias sources, supply and incoming clock remain ideal bench stimuli.
- The ladder lengths are fixed for each test deck. Separate hot and cold tap settings illustrate the range a physical trim circuit would need. The nominal block itself uses the default tap settings in `blocks.spice`. No automatic calibration circuit, layout, extracted clock routing, mismatch or complete PVT closure has been performed.

## Running the tests

From this directory use `ngspice -b -o nominal.log benches/bypass_12_7.cir`. Each integrated simulation writes `trace.dat`. Keep runs in separate working directories or rename their output files between runs. If running from another directory, copy `blocks.spice` into the working directory. The decks refer to the local installed SCL08 models and the project OTA. `test_blocks.cir` generates clock waveforms, then uses a 400 µA current pulse and AC injection to exercise the buffer with a 25 pF fixture load. Model warnings about ignored HSPICE parameters appear in ngspice logs.

Use `integrate.py` to generate a new case. It reads the preceding `vcm_pvt_20261115` fixture and allows the clock and reference subcircuits to be switched in independently. `results.csv` includes isolation tests, integration variants and the selected process cases. `clock_timing.csv` records nominal duty-cycle and untrimmed corner checks. Track edges use half supply and the held differential sample is measured at 81 µs. Reference peak deviation is reported over the full cycle and separately during the 40–81 µs transfer and acquisition interval.

## Measured circuit settings

The selected tests place 150 parallel 20 µm / 10 µm PMOS cells on the buffered reference as a bypass bank. Their gates connect to the buffered reference and their drain, source and bulk connect to VDD. The nominal 12/7 pF case shows 2.52 mV full-cycle peak reference deviation, compared with 33.33 mV in the same circuit without bypass. The selected hot 12/12 pF case reaches 8.76 mV peak reference deviation. The actual voltage-dependent capacitance comes from the MOS models.

| Integrated bench | Track window | OTA transfer CM | Held differential | Bench supply power |
|---|---|---|---:|---:|
| Nominal 12/7 pF | 70.088–80.053 µs | 2.469–2.524 V | 210.629 mV | 6.246 mW |
| Nominal 12/12 pF | 70.088–80.053 µs | 2.462–2.529 V | 0.113 mV | 6.246 mW |
| Hot with case-specific tap settings, 12/12 pF | 69.964–80.009 µs | 2.372–2.555 V | 0.115 mV | 15.826 mW |
| Cold with case-specific tap settings, 12/7 pF | 70.062–79.982 µs | 2.485–2.515 V | 180.839 mV | 4.554 mW |

The untrimmed clock in standalone tests tracks at about 82.36–92.16 µs at 5.5 V/85 °C and 53.84–63.39 µs at 4.5 V/0 °C. Nominal 40–60% duty-cycle tests have negligible track-edge shift. A physical trim scheme and lower clock and buffer power are design priorities before layout.
