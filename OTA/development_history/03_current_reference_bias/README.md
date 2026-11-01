# 03_current_reference_bias: Current-reference bias and channel-length sweep

Development order: **3**. Date / ordering evidence: **28 October 2026**.

Ideal current reference plus diode-connected mirror; length/current/compensation tradeoffs.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_1/current_reference_exploration/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Design 1: current-reference bias and sizing exploration

Exploratory SCL800 nominal simulations, 28 October 2026. Baseline files outside this folder are unchanged. No GitHub push is performed by this experiment.

## Circuit and experiment

Seven-transistor single-ended core plus M8, a diode-connected NMOS. An ideal IREF sources current from VDD into M8's drain/gate. The same voltage drives M5 and M7. M8 and M5 have equal W/L; M7 has twice that ratio. Drain-voltage differences mean actual mirror ratios are approximate. The ideal reference is a testbench element, not an implemented on-chip reference generator. Reported power includes its VDD current but excludes a future practical reference generator's additional overhead.

Sweep: all eight lengths = 0.8/1.6/2.4/3.2 um; widths scaled by the same multiplier to maintain W/L. IREF = 5/15/30/60 uA. Cc = 1/2.5/5/10/20/40 pF. Total 96 points. All runs: VDD=5 V, 27 C, CL=5 pF, follower input 2.5->2.6 V. reltol=1e-5, vntol=1e-8, abstol=1e-12. Reference characterization W=2.5 um, L=0.8 um remains the base geometry, not a universal sizing constraint.

AC uses a large DC feedback inductor and shunt AC-ground capacitor (each 1e12 SI units): the operating point is the closed-loop follower point, while the inverting input is AC grounded over the 1 Hz--1 GHz sweep. This estimates the follower return ratio under this configuration, including loading by the feedback elements. It is not an SC-phase loop-injection qualification. Phase margin is interpolated at the first descending unity crossing; sweep counts descending crossings, not all possible upward crossings. Inspect full curves before acceptance.

Transient is simulated separately without these AC fixtures. Settling is last exit from a +/-100 uV band about the measured final output for a 100 mV step (0.1%). It excludes static error to the ideal input. Final levels are averaged near the end of each plateau. Large-step check uses a 2 V step, +/-2 mV band, 2 ns maximum step. Small-step maximum timestep is 5 ns. Rise/fall time is measured after the input edge has completed; add 10 ns to reference the beginning of the edge.

## Main results

| Point | Gain at 1 Hz (dB) | UGF (MHz) | PM (deg) | Supply power (uW) |
|---|---:|---:|---:|---:|
| Original voltage-biased core, rechecked at follower DC point | 36.80 | 1.569 | 62.93 | about 545 (prior follower result) |
| L=0.8 um, IREF=5 uA, Cc=5 pF | 42.92 | 0.817 | 67.07 | 139.66 |
| L=1.6 um, IREF=5 uA, Cc=10 pF | 69.07 | 0.495 | 60.58 | 116.19 |
| L=3.2 um, IREF=5 uA, Cc=20 pF | 85.31 | 0.264 | 60.35 | 109.87 |
| L=3.2 um, IREF=5 uA, Cc=40 pF | 85.24 | 0.133 | 63.55 | 109.87 |

The selected run is 076: highest 1 Hz gain among points with PM>=60, positive model-reported DC saturation margins, one descending crossing, and measured small-step settling. This is a screening rule, not a globally optimum design or a complete requirement set. 30 of 96 points passed that screen. Model valid geometry ranges/design rules have not been established for every swept size.

Selected geometry (um): M1-M4 W=10,L=3.2; M5/M8 W=20,L=3.2; M6 W=28,L=3.2; M7 W=40,L=3.2; Cc=20 pF. M8 bias node = 0.852 V, total VDD current = 21.974 uA. Small-step rise/fall settling is 1.83/1.98 us relative to settled value. Static follower error is -0.226 mV at 2.5 V and -0.232 mV at 2.6 V. Minimum nominal model-reported saturation margin across M1-M8 = 0.727 V. MOS gate area proxy sum(W*L)=473.6 um^2, versus 29.6 um^2 for the shortest-channel eight-MOS design. This is not layout area; it excludes routing, contacts, bias generation and capacitor area.

Large step 1.5->3.5 V: final outputs 1.499821/3.499712 V; 0.1% settling ~8.89/9.06 us. Thus high DC gain does not establish fast SC operation. At the illustrative 200 kHz clock and 2.45 us amplification window from the behavioral model, this large-step case would miss timing; that clock/window is not a frozen requirement.

Selected-load check: PM=64.99/60.35/55.10 degrees at CL=1/5/10 pF. The selected point has almost no margin above the nominal 60-degree screen at 5 pF and fails it at 10 pF. More Cc improves margin but slows settling and consumes area. Current increases improve speed at the expense of gain/power in this grid. Longer channels increase gain and capacitance and require reconsidering compensation. The gain increase is from combined sizing/bias changes, not from adding a mirror alone.

## Files and reproduction

- designs/ota8.inc: parameterized core; designs/ota_current_ref.sch/.sym: fixed selected candidate.
- tb/selected_ac.cir, selected_tran.cir, large_step.cir: portable relative core includes; model include points to the local private model deck.
- tb/ota_current_ref_tb.sch: native xschem follower, with current source and embedded transient graphs. From this folder: `xschem --rcfile xschemrc tb/ota_current_ref_tb.sch`; Ctrl-click Run simulation + plot.
- results/sweep.csv, summary.json: all points and screening; results/runs/: full inputs, logs and numeric data for all 96 points.
- results/extracted_check.*: AC simulation of xschem-extracted schematic, matching authored netlist. All eight MOS connections/model types/dimensions and capacitor endpoints/value were checked. Native follower testbench also netlisted and simulated successfully; GUI display not tested in this headless environment.
- plots/tradeoffs.png, selected_candidate.png/.pdf.
- Reproduce sweep: `python3 run_sweep.py`; then `python3 finish.py`; netlist schematic with xschem into results/extracted.spice; then `python3 validate.py`. The last script also reconstructs the native follower testbench. NumPy and Matplotlib required. Full logs preserve foundry model compatibility warnings.

## Limits and next work

Actual ngspice runs used the existing local SCL CP8D nominal LEVEL49 deck; its hash is in summary.json. No foundry model cards are copied here. Ngspice ignores several HSPICE parameters, including PMOS capacitance entries: bandwidth, phase margin, settling and especially noise remain provisional pending compatible/qualified model validation. No noise claims are made. Only one process deck, supply, temperature and limited follower output conditions were tested. No mismatch, extracted parasitics, startup/power cycling, current-reference compliance sweep, PSRR/CMRR, actual SC feedback-factor test, or ADC kickback test. Ideal IREF suppresses real reference noise/drift. Saturation at one DC point does not prove saturation throughout transient swing. This single-ended core has no CMFB.

Next optimization should investigate length independently by device group and stage-current ratio, rather than scaling every device equally; evaluate compensation including a nulling resistor if appropriate; and optimize against actual SC sampled error and phase loads. Retain both the faster moderate-gain and slower high-gain candidates until timing and accuracy are frozen.
