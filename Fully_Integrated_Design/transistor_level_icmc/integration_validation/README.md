# Integrated SC + OTA sensitivity check

The circuit combines the existing final switched-capacitor readout, NMOS-VCR telescopic OTA with output CMFB, and transistor-level SCL08 input common-mode controller. The final 60-unit PMOS feedback bank remains the default. Both branches use the same feedback bank size. The candidate reduces the feedback bank to 40 units per branch and keeps the separate input correction capacitors and OTA compensation unchanged.

## Test conditions and results

The sensor endpoint sweep uses CP = 7.82–11.79 pF and CN = 10 pF. The existing 10 kHz timing, 2.5 V reference, board load, track-and-hold and illustrative external ADC acquisition are included. Sensitivity is an endpoint slope for the differential held output at 88 µs or the ADC input at 89 µs in each cycle. All runs use the installed SCL08 MOS and resistor cards in ngspice 42. The compared decks include the OTA macro's inherited extracted capacitances.

| Method and setting | Held slope (mV/pF) | ADC input slope (mV/pF) |
| --- | ---: | ---: |
| Flat deck, 60 feedback units, typical | 94.31 | 72.93 |
| Xschem deck, 60 feedback units, typical | 78.72 | 60.87 |
| Flat deck, 48 feedback units, typical | 120.75 | 93.37 |
| Flat deck, 40 feedback units, typical | 147.57 | 114.12 |
| Xschem deck, 40 feedback units, typical | 121.58 | 94.02 |
| Flat deck, 40 feedback units, 0 °C / 4.5 V | 117.87 | 91.15 |
| Flat deck, 40 feedback units, 85 °C / 5.5 V | 111.68 | 86.36 |

With 40 feedback units, all tested endpoints settled in 3–8 cycles. Settling uses the sustained ±5 mV input common-mode band and ±1 mV band about the final held value. The common-mode error across the final controller sampling window stayed within 3.7 mV. Settled held output agreed with the live value from 300 ns before track close to within 0.12 mV. The shortest interval from the track switch clock crossing half the supply to the ADC switch crossing its threshold was about 218 ns at the hot corner. These timing results use the existing corner-specific trim values.

The nominal 40-unit readout consumes about 3.30 mW at CP = 11.79 pF. The smaller feedback bank increased nominal held sensitivity by 54% in Xschem and 56% in the flat deck. The result depends on the external load model and is an electrical sensitivity measurement in simulation.

## Flat and Xschem sensitivity

Reordering the same sampling, acquisition and metering devices switched the result in both directions in a seeded diagnostic. The simulator-expanded records matched after sorting. Inserting the editable Xschem correction subcircuit into the original flat-deck ordering reproduced the flat result. The numerical origin of this order dependence and a converged absolute sensitivity remain open. The seeded diagnostic is separate from the unseeded startup and sensitivity tests. The 2.5 V reference and the external ADC remain bench interfaces. Mismatch, sampled noise, and full-chip extraction remain open.

## Reproduce

Keep this source folder alongside the existing `Fully_Integrated_Design` folder, or set `CAPSENSE_INTEGRATED_DIR` to its installed path. Python requires NumPy and Matplotlib. Point `SCL08_MODELS` to the local SCL08 model cards.

~~~sh
export SCL08_MODELS="$HOME/pdk/scl08/ngspice_models49"
python3 run_icm.py --feedback-units 40 --cp 11.79 --cn 10
./schematic/open_xschem.sh --feedback-units 40
~~~

To rerun the comparison matrix, start from this folder and build the nominal Xschem deck once.

~~~sh
python3 prepare_xschem.py
(cd schematic && xschem -x -q -n --rcfile "$PWD/xschemrc" sc_vcr_input_cm_scl08.sch)
python3 integration_validation/check_integrated.py --stage nominal
python3 integration_validation/check_integrated.py --stage candidate
python3 integration_validation/summarize_integrated.py
~~~

Test runs produce raw files and per-cycle results locally. The source bundle includes the summary CSVs and plot without the foundry cards or raw transients.
