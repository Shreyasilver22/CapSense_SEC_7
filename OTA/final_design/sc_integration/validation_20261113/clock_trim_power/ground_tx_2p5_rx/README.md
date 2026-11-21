# Grounded TX discharge with 2.5 V RX precharge

The candidate connects all four TX-discharge transmission-gate devices to ground. The control connects TX discharge to the buffered 2.5 V reference. Both use a 2.5 V RX precharge and hold precharge, a 2.5 V OTA output common-mode target, a single 10 kHz clock, the existing PMOS feedback banks and 10 pF per held output. TX charges to VDD. The bench includes transistor-level timing, switched-reference and bias circuits and the capacitance-extracted OTA. The 2.5 V master source is ideal.

The nominal comparison covers six fixed capacitor pairs at 5 V, 27 °C, typical SCL08 and trim code 3. Separate perturbations of each sensor by ±0.1 pF give the local slopes of the held differential output. The fixed-sum slope represents equal and opposite capacitor changes and is expressed per pF change of CP minus CN. The corner screen reuses project trim codes 0 and 5 for cold and hot respectively.

The measured sample is 81 µs into cycle one. To assess settling, the test compares the live differential output with the median over 87–89 µs during charge transfer. The live output is checked through 150 ns before the track clock crosses half supply on its falling edge. The test band is 0.1% of the settled differential or 100 µV, whichever is larger. Held error at 81 µs is also measured against the same late live differential value. The difference between these errors includes sample-and-hold turn-off effects. OTA saturation margin uses BSIM3 |VDS| − |VDSAT|. Transfer extrema are measured from 40 µs through the falling track-clock midpoint.

Run from this directory with the project model includes available.

```bash
python3 compare.py /tmp/mixed_bias nominal
python3 compare.py /tmp/mixed_bias sensitivity
python3 compare.py /tmp/mixed_bias refine
python3 compare.py /tmp/mixed_bias nominal --corner cold
python3 compare.py /tmp/mixed_bias nominal --corner hot
python3 compare.py /tmp/mixed_bias hot-retries
python3 report.py /tmp/mixed_bias
```

The runs save decks, logs and waveforms in the work directory. Nominal comparison and slope runs use a 40 ns maximum step and the four key capacitor pairs are rechecked at 10 ns. The files published here summarize electrical transients and the selected corner screen.

The two hot control cases failed to find a startup operating point with KLU and trapezoidal integration. Both completed with the original Sparse solver and Gear integration and with a separate KLU/Gear convergence retry. The hot screen uses the Sparse/Gear control rows and retains both retries in `hot_solver_checks.csv`. The hot candidate rows use KLU/trapezoidal integration.
