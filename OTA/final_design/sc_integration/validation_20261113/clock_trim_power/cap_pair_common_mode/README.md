# Sensor-capacitance sweep and OTA common-mode

These nominal ngspice runs use the current transistor-level SCL08 clock, reference buffer and OTA bias generator. The bench uses 5 V, 27 °C, typical process models, one 10 kHz clock, trim code 3 and 10 pF per held output. The two sensor capacitors are independently set to fixed capacitance values in each test.

The 2.5 V TX discharge configuration covers every combination of 7, 9.5 and 12 pF. Three matched cases use ground for TX discharge while RX clamping and hold precharge stay connected to the 2.5 V switching reference. The transfer extrema cover 40–70 µs of the first clock cycle. The held differential voltage and held common-mode are read at 81 µs. The ideal input common-mode column assumes a constant 50 pF feedback capacitance per side and ideal settled charge balance.

From this directory, run the nominal sweep with `python3 sweep.py /tmp/cap_pair_nominal` and the ground checks with `python3 sweep.py /tmp/cap_pair_ground --ground-check`. The script reads the parent clock-trim testbench and models, and writes each case's deck, log and waveform to its working directory. These nominal runs do not characterize process corners or a pressure-to-capacitance curve.
