# November 14 switched-capacitor readout comparison

Source: https://github.com/Shreyasilver22/CapSense_SEC_7/blob/main/SCA/14_Nov/diff_1411.sch
Schematic blob: 0b54e46491b9ea360f27a7dc6409e0f918b0518f.

Xschem generated the original design netlist using local equivalents of Shreyas's transmission gate and OTA symbols. The simulation decks resolve model/include paths to the local SCL08 installation and give the two default-named PMOS feedback devices unique SPICE instance names. The original deck retains the actual 2.7 V VBP and its gate-at-SUM feedback wiring. The matched-load variant adds the same 10 pF hold capacitors, precharge network and acquisition switches used by the single-clock deck, driven at the same nominal times by pulse sources. The single-clock deck uses ideal timing derived from one external clock.

Each run uses the same SCL08 typical MOS/resistor models and the same OTA subcircuit. Supply is 5 V and temperature is 27 °C. The output load is 5 pF per side in each circuit before the switched acquisition load. Measurements use the third 100 µs cycle, 81 µs after the cycle starts. The reported hold-edge shift compares the held sample to the live output at 79.5 µs, while the acquisition switch is still in track.

Run a deck from testbenches with ngspice -b -o run.log <name>.cir. The embedded control block writes a waveform .dat file. The provided logs show the 12 pF / 7 pF cases. The decks refer to the local installation's model paths. ngspice reports warnings for unsupported model parameters in the supplied HSPICE-style model files and completed the transient runs. The comparison covers nominal transient response only. It does not measure sampled noise, process corners, or SAR loading.
