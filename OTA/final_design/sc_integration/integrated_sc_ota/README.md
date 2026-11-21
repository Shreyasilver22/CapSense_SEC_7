# Integrated SCL08 switched-capacitor circuit and telescopic OTA

Open sc_ota_integrated.sch in Xschem to see the complete two-branch SC circuit,
sensor and RX reset, PMOS feedback banks and separate analog outputs. The
XOTA symbol opens ota_core.sch, the editable transistor-level telescopic
core, common-mode sensing, error amplifier and MOS compensation. The top
schematic netlists that child circuit directly. The 10 kHz clock, bias
fanout and references are instantiated by the bench support SPICE files.

    xschem --rcfile "$PWD/xschemrc" sc_ota_integrated.sch

Select the OTA block and press e to open the child schematic. The child can
also be opened directly using the same rc file with ota_core.sch.

## Simulation

From this directory in WSL, run python3 verify.py with Xschem, ngspice and
NumPy available. Generate the simulation includes from your licensed or installed SCL08 PDK.

    python3 setup_models.py /path/to/scl08/ngspice_models49
    python3 verify.py

The upstream foundry model cards are supplied separately.

The editable design was checked with the nominal 5 V, 10 kHz bench. At
CP = 10.5 pF and CN = 10 pF it gave +16.36 mV differential at the 80 us
sample. Its average sensitivity was 34.62 mV/pF across 7.82–11.79 pF with
CN held at 10 pF. The corresponding prior capacitance-extracted OTA run
gave +16.52 mV, with the same 34.62 mV/pF sensitivity to two decimals.
Minimum input common-mode in the editable schematic sweep was about
0.74 V during switching, recovering to about 1.8 V at sampling. The
capacitance-extracted OTA version measured a minimum of about 0.81 V.
Switching headroom and full integrated layout verification remain open.

For the separate capacitance-extracted OTA run:

    ngspice -b -r results/extracted.raw -o results/extracted.log results/sc_ota_extracted.spice

The edited hierarchy generated results/sc_ota_integrated.spice. The
capacitance-extracted deck in results/sc_ota_extracted.spice uses the
frozen extracted OTA model in models/telescopic_C.spice. Both
sets of sweep measurements are included under results/.

The previews show the top-level SC wiring and the editable OTA child.


## Later engineering results

- [Transmission-gate verification](transmission_gate_verification/integrated_tg_sweep.csv)
  tests all 12 SC switches with complementary SCL08 MOSFETs.
- [Sensitivity sizing](sensitivity_optimization/nominal_summary.csv) compares feedback-bank
  and TX–RX capacitance combinations. The 84-unit feedback candidate gives
  48.01 mV/pF nominally. The editable reference schematic still uses 121 units.
- [Corner data](sensitivity_optimization/baseline_84_corner_summary.csv) capture the
  remaining hot-sample settling limitation.
- [OTA and SC comparison](../comparison_20261121) contains the sensor-reset diagnostic,
  matched architecture sweep and layout comparison.

[Pad-frame and board-output planning](pad_and_output_planning.md) summarizes the die pad budget and ADC interface.
