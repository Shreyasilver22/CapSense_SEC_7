# OTA design_2 — tuned current-reference OTA with extracted compensation capacitor

Single-ended SCL CP8D 800 nm two-stage OTA, using an eight-MOS core/bias circuit and the experimental metal-overlap capacitor model. Design_1 is preserved. Standalone capacitor generation/layouts live in ../../capacitor; this folder contains the OTA integration and a frozen capacitor-model snapshot for reproducibility.

## Selected configuration and measured nominal behavior

- Supply 5 V, 27 C, ideal reference current 2.5 uA, explicit load 5 pF.
- Compensation target 8 pF: extracted mutual C=8.00295 pF, first-stage-node substrate loading=4.90149 pF, output-node substrate loading=14.6206 pF.
- TOP=n2, BOT=out, SUB=vss. The external 5 pF load is additional to the capacitor parasitics.
- Gain at 1 Hz ~88.75 dB, UGF ~364 kHz, nominal phase margin ~65.8 degrees.
- Minimum phase margin ~61.8 degrees over the full CL=1/5/10 pF by follower bias=1.5/2.5/3.5 V grid (one process deck, supply and temperature).
- Worst 2 V follower-step settling to 0.1% of final output ~7.82 us; 100 mV dynamic settling ~2.12 us. Static follower error remains approximately -0.206 mV; dynamic settling does not prove total accuracy to the ideal input.
- Quiescent supply power ~175 uW including ideal reference branch, excluding a practical reference generator's overhead. No dynamic-energy or noise qualification.

The selected transistor geometry (W/L in um): M1/M2=7.5/2.4; M3/M4=10/3.2; M5/M8=20/3.2; M6=112/3.2; M7=160/3.2. M8 is diode-connected and IREF sources current into its drain/gate. Reference current generation remains ideal.

## Why 8 pF

The prior ideal 3 pF result was about 1.003 MHz UGF, 73.4-degree phase margin and 2.88 us settling. An extracted near-3 pF capacitor reduces nominal phase margin to about 57.9 degrees (TOP=n2), or 53.8 degrees when reversed. An extracted 4p target gives 60.9 degrees nominally but only 54.7 degrees at the worst checked point. The 6p trial reaches only 59.2 degrees minimum. Among tested values, 8p is the smallest passing the working >=60-degree screen everywhere checked. It is slower and is not a global optimum.

The selected capacitor layout is ../../capacitor/layouts/requested_8p.gds (internal cell scl08_cap_n703), footprint 912 x 876 um (~0.799 mm2). That is a substantial area cost, excluding surroundings/guard rings. This is a conservative compensation candidate, not a finalized area/power/speed optimum or proof that the illustrative SC timing window is met.

## Configure private transistor models and run

Requirements: Python 3, NumPy/Matplotlib, ngspice and xschem. The SCL transistor deck is NOT included. Configure an authorized local copy:

```bash
cd OTA/design_2
python3 scripts/configure_models.py /your/path/to/tntp49_5v
python3 scripts/check.py
xschem --rcfile xschemrc tb/ota_extracted_cc_tb.sch
```

The ignored spice/models.inc points at the user's model file. No model cards are copied. Run the plain .cir benches from tb/; includes are relative to that working directory. In xschem, the inherited Run simulation + plot launcher uses the project-local batch ngspice configuration, including a process-local fix for directory names containing spaces.

The native follower demonstration uses inherited 100 ns input edges; quantitative comparison benches use 10 ns edges. GUI clicks were not exercised headlessly, but native netlisting and actual ngspice simulations were checked. All six OTA interface pins are required: inp, inn, out, vdd, vss, iref. This is single-ended and has no CMFB.

## Evidence and full comparison

results/ac_checks.csv and settling_checks.csv record 99 AC and 66 base transient runs over 11 compensation configurations. results/summary.json records the selected case, capacitor metadata and extraction verification. results/comparison retains compact numeric AC and large-step traces used by plots/compensation_comparison.png/.pdf. The selected large-step run was repeated at a 1 ns maximum timestep: settling changed by about 0.121 ns.

To regenerate the full bounded comparison after configuring models:

```bash
python3 scripts/analyze.py
python3 scripts/extend.py
```

The first script covers ideal 3/3.00538 pF controls and extracted 2.5/3/4p in both orientations; the extension adds 6/8/10p with TOP=n2. Models are frozen locally, so capacitor regeneration is unnecessary for these OTA runs. Full waveforms can be regenerated. plots/ contains the saved comparison. scripts/check.py reruns selected portable benches, compares AC data, netlists/simulates the native schematic and verifies capacitor pin mapping.

AC uses a 1e12 H DC feedback inductor and 1e12 F AC-ground capacitor to estimate follower return ratio at its closed-loop DC point. AC is 150 points/decade from 1 Hz to 1 GHz. Settings: reltol=1e-5, vntol=1e-8, abstol=1e-12, numdgt=12. Transients use a 5 ns max timestep and 90 us duration. This is a continuous-time follower comparison, not a complete phase-specific switched-capacitor verification.

## Limitations

Dynamic numbers remain provisional: ngspice ignores some HSPICE transistor-model parameters, including capacitance entries. Installed Magic 8.3.105 was below the capacitor PDK header's required 8.3.579; native export omits one substrate capacitor, so the evaluation models retain documented raw-.ext node/coupling records. That discrepancy is unresolved in a supported flow. The stock device deck provides no formal capacitor LVS. DRC and numerical model checks do not establish foundry acceptance or physical capacitance accuracy.

No PVT sweep, mismatch, capacitor voltage coefficient/leakage/loss, extracted conductor resistance, real reference generator, startup, noise, substrate disturbance, full SC switching or ADC kickback was qualified. The OTA wiring itself is not post-layout extracted. No fabrication/sign-off or final optimum claim is made. Standalone capacitor code/layout reuse and applicable foundry-derived data terms are documented in ../../capacitor.
