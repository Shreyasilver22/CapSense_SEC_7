# Fully integrated CapSense readout

This is the selected SCL 0.8 µm switched-capacitor readout. It uses transmission gates, the low-power fully differential telescopic OTA with NMOS MOSFET resistors and output CMFB, and PMOS input common-mode correction targeting 2.5 V. The testbench includes the track-and-hold and an illustrative external ADC input load.

- A single 10 kHz master clock supplies the timing circuit. The nominal track-close tap is 87 µs and external acquisition starts at 88.1 µs.
- The SC core uses 10 pF series capacitors, 60 PMOS feedback units and 40 PMOS correction units per branch. The input correction senses from 84 to 86 µs and applies the update on the next cycle.
- The OTA retains 12 output-linked MCM compensation units per output. The integration bench uses the OTA macro with inherited extracted capacitances. An editable OTA core is included separately for inspection.

## Run with ngspice

Run from this directory with Python 3, ngspice and locally installed SCL08 BSIM model cards. Point `SCL08_MODELS` at the model directory containing `mos/` and `res/`. The recorded flat reference runs used ngspice 42 with KLU.

~~~sh
export SCL08_MODELS=/path/to/scl08/ngspice_models49
python3 run_sc.py
python3 run_sc.py --corner cold --cp 7.82 --cn 10 --seeded
~~~

The first command runs the nominal startup for 795 µs with Cp = 11.79 pF and Cn = 10 pF. Pass `--cp` and `--cn` to change the capacitors in pF. The cold and hot matched checks use saved initial correction voltages listed in [sim/seeds.json](sim/seeds.json). Waveforms and logs go to `runs/`.

## Open in Xschem

~~~sh
./schematic/open_xschem.sh
~~~

This opens the full schematic with the input correction shown as an editable hierarchy. Use **Netlist** and then **Simulate** to run its nominal bench. The generated Xschem deck uses Gear and Sparse. If Xschem uses a different installation path, set `XSCHEM_SYSTEM_LIBRARY` to the directory containing `devices/`.

## Results

Held-output sensitivity from the flat reference deck, with Cn = 10 pF and Cp varied from 7.82 to 11.79 pF.

| Corner | Without input correction (mV/pF) | With input correction (mV/pF) | At illustrative ADC input (mV/pF) |
| --- | ---: | ---: | ---: |
| Typical | 48.03 | 93.85 | 72.53 |
| Cold | 48.25 | 78.25 | 60.48 |
| Hot | 46.63 | 74.05 | 57.26 |

All ten matched points and the nominal startup met the testbench settling criterion. At the nominal startup point the held differential output was 146.09 mV and the sampled OTA input common-mode was 2.500 V. See the [plot](results/sc_vcr_cm_baseline.png), [matched cases](results/matched_points.csv), and [startup result](results/startup_points.csv).

The flat nominal run with Gear and Sparse reproduced the 93.85 mV/pF slope. The hierarchical Xschem deck also settled, with 124.85 mV held at the same nominal startup capacitances. The difference appears during sensor charge transfer. Use the reported sensitivity as a reference-bench value until the discrepancy is resolved. [Solver checks](results/solver_crosscheck.csv)

The common-mode sensing, control and drive blocks are behavioral. The master 2.5 V reference and the external ADC load are testbench models. The correction circuit still requires transistor-level implementation and the integrated design requires physical verification and noise/mismatch qualification.
