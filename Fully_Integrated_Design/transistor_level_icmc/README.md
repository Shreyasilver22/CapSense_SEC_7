# Fully integrated CapSense with transistor-level ICMC

This is the SCL08 switched-capacitor readout with its existing NMOS-VCR telescopic OTA, output CMFB, and [transistor-level input common-mode correction](../../ICMC). It uses the single 10 kHz phase generator from the [integrated baseline](..), expanded with a transistor-level late-sample comparator. The 2.5 V master reference and the external ADC acquisition load are testbench interfaces.

The default is **60 PMOS feedback capacitor units per branch**. The **40-unit** setting is the higher-sensitivity candidate. The ICMC injection capacitors are 40 units per branch in both settings.

## Run

Clone the full repository so the OTA/clock models and shared symbol tree resolve. Run the following commands from this revision directory in Linux or WSL. Install Python 3 with NumPy, ngspice, and optionally Xschem. Matplotlib is used for plots. The locally installed SCL08 model directory should contain `mos/` and `res/`. The verified runs used ngspice 42.

~~~sh
export SCL08_MODELS="$HOME/pdk/scl08/ngspice_models49"
python3 run_icm.py
python3 run_icm.py --feedback-units 40 --cp 11.79 --cn 10
./schematic/open_xschem.sh
~~~

Pass `--feedback-units 40` to the launcher to use the same setting in Xschem. The full schematic is `schematic/sc_vcr_input_cm_scl08.sch`. Use **Netlist** and **Simulate** in Xschem, and descend into `XICM` to inspect the shared editable block. The flat runner writes its deck, output and per-cycle measurements to `runs/`.

## Results

The nominal 60-unit input common-mode stays within 3.5 mV of 2.5 V during the final sampling window in the tested flat-deck cases across the selected typical, cold and hot conditions. For the 40-unit feedback candidate, the largest corresponding measured error was 3.7 mV across the integration tests. Nominal main-rail power is about 3.30 mW, including about 0.49 mW in the controller branch.

The sensitivity figures use the differential held output and loaded ADC input. The sensor sweep varies CP from 7.82 to 11.79 pF with CN fixed at 10 pF.

| Nominal deck | Feedback units per branch | Held slope (mV/pF) | ADC input slope (mV/pF) |
| --- | ---: | ---: | ---: |
| Xschem-generated | 60 | 78.72 | 60.87 |
| Xschem-generated | 40 | 121.58 | 94.02 |
| Flat | 60 | 94.31 | 72.93 |
| Flat | 40 | 147.57 | 114.12 |

The relative improvement appears in both decks. Reordering electrically identical netlist entries reproduced the amplitude discrepancy, so the absolute sensitivity remains provisional. The shortest observed track-to-ADC interval for the 40-unit candidate was 218 ns at the tested hot corner. These are circuit simulations with the existing OTA macro and its inherited extracted capacitances. Integrated layout, extraction, noise, and mismatch verification remain open.

[Sensitivity results and reproduction commands](integration_validation/README.md) · [Sensitivity plot](integration_validation/Integrated_Sensitivity.png) · [Startup and corner data](results/case_summary.csv)
