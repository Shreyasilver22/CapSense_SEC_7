# TX transfer level with 40 pF PMOS feedback

This compares TX transfer levels of 0, 2.0 and 2.5 V in the 10 kHz SC bench with 97 gate-at-output PMOS units per feedback branch, 5 V supply, typical SCL08 models at 27 °C, 5 pF output loads and the same reset and receive timing. RX clamps to 0 V during sampling and the OTA output common-mode reference stays at 2.5 V. The TX level is an ideal source. Results are sampled at 80 µs into the second cycle.

Local sensitivity is a centered ±0.05 pF change of CP around 12 pF with CN held at 7 pF. The 12/12 pF case tests the switching dip. The reported thermal noise is the sensor-only estimate from propagating independent kT/C charge through the clocked circuit. These nominal comparisons do not qualify a physical TX reference driver, switch-junction stress, total sampled noise, PVT or an ADC load.

Run python3 compare.py from this directory. The script reuses the parent PMOS capacitor study and the existing SC netlist.
