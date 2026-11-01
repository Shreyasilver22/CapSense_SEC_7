# 09_mos_only_compensation: MOS-only compensation selection

Development order: **9**. Date / ordering evidence: **Before first physical OTA layout 2026**.

Six PMOS gate-capacitor units selected in the original schematic-level experiment.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# MOS-only OTA compensation experiment

Six parallel PMOS gate capacitors are the selected first-pass candidate. No capacitance multiplier or behavioral compensation source is used. Simulated with ngspice 42 using the local SCL08 nominal N/P model cards, 5 V supply, 27 C, ideal 2.5 uA current reference, and the existing tuned OTA transistor sizes.

## Connection and size

MCAP has gate at first-stage node n2 and source, drain and body tied together at out. Each unit is W=20 um, L=10 um; m=6. The nominal modeled gate capacitance is approximately 2.475 pF. Total gate area is 1200 um2; this is not a finished layout footprint. A separate properly tapped N-well tied to out is required. Do not substitute a body connection to VDD without re-analysis.

## Selected result

At 5 pF explicit load and 2.5 V follower DC bias: gain 88.77 dB, UGF 1.199 MHz, phase margin 70.80 degrees, modeled quiescent power 174.74 uW. Worst phase margin across checked loads 1/5/10 pF and biases 1.5/2.5/3.5 V is 61.73 degrees. Follower settling to 0.1% of actual final step: approximately 0.604 us for 100 mV and 2.350 us for 2 V. These are not complete switched-capacitor settling or accuracy qualifications.

| Parallel units | Nominal gate C (pF) | Nominal PM (degrees) | Minimum checked PM (degrees) | UGF (MHz) | 2 V settling (us) |
|---|---:|---:|---:|---:|---:|
|4|1.650|63.57|52.44|1.712|1.725|
|5|2.063|67.83|57.73|1.413|1.940|
|6|2.475|70.80|61.73|1.199|2.350|
|8|3.300|74.58|67.24|0.917|3.176|
|10|4.125|76.86|70.78|0.741|3.991|

Six is the smallest tested count meeting 60 degrees throughout that grid. Extra bias tests at 4 and 4.5 V give only 46.15 and 33.40 degrees: this implementation is not qualified for rail-to-rail use. MOS capacitance changes with gate/body bias, and OTA headroom also changes; these tests do not isolate their individual contributions.

## Files and running

- designs/ota_mos_only.sch and .sym: native xschem cell and symbol.
- tb/ota_mos_only_tb.sch: native xschem testbench, netlisted and simulated.
- tb/selected_ac.cir, selected_small.cir, selected_large.cir: runnable benches. From tb, run `ngspice -b selected_ac.cir` (similarly for the other files).
- plots/mos_only_comparison.png and .pdf: comparison plots.
- results/: raw simulations, CSV measurements, summary.json and simulator logs.
- scripts/run.py: full sweep; scripts/finalize.py: schematic verification and plotting. These regeneration scripts also reference the existing neighboring research projects; the selected benches are self-contained apart from the PDK model include.
- spice/models.inc: private local model path; proprietary model cards are not copied. Update that include when moving machines.

Open xschem from this directory so its xschemrc is loaded, then open tb/ota_mos_only_tb.sch. Netlist/simulate using the local SCL model installation.

## Verification and limits

45 base AC cases and 30 base transient cases were run, plus selected-case bias, hypothetical well-loading and timestep checks. Extracted native schematic connectivity and transistor geometry were checked against the original core; native AC matches the hand-written bench. The selected large step was repeated with a 1 ns maximum step.

Physical well/substrate capacitance, well resistance/diode behavior, routing and extracted layout are absent. Added output loads of 1/3/5 pF are sensitivity tests only, not extracted well estimates; their nominal phase margins are 69.00/65.64/62.58 degrees. No MOS capacitor layout is supplied by this experiment. No PVT, mismatch, noise, reliability or silicon validation was performed. Ngspice reports ignored HSPICE model parameters, so dynamic results remain provisional. Reference-generator overhead is excluded. Do not infer SC-loop performance from the unity-gain follower tests.
