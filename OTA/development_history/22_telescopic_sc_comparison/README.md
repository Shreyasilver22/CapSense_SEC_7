# 22_telescopic_sc_comparison: Telescopic / gain-boosted OTA SC comparison

Development order: **22**. Date / ordering evidence: **31 October 2026**.

Both candidates tested in the previously assumed SC circuit; gain boosting provides little sampled benefit in that benchmark.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `architecture_exploration_20261031/sc_comparison/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Same SC circuit: telescopic versus gain-boosted telescopic — 31 October 2026

Both exported OTA transistor models were actually run in ngspice 42 in the supplied single-ended switched-capacitor integrator. One output drives the original circuit; the other output remains internal to the OTA test setup and is controlled by its unchanged continuous-time CMFB. **A fully differential SC redesign was not required to perform this test.** The preceding differential-benchmark figures alone did not establish this connection's performance; these new tests do.

The original SC topology, switch dimensions, capacitor values, references and clock sequence were preserved. The current extracted-capacitance two-stage OTA was added as a reference. Neither OTA candidate was resized or retuned here.

## Assumptions and wiring

- SCL800 native MOS models; nominal `tntp49_5v`, VDD5 V,27 C, native typical RPP, ideal current reference3.5 uA.
- CS=2.5 pF plus sensor change; CF=7.5 pF; VREF=1.5 V; VP=0.3 V; active output load5 pF.
- Candidate noninverting input=VREF, inverting input=summing node, OUTP=SC output. OUTM is **not grounded or shorted to OUTP**; it receives an assumed5 pF load, and the existing CMFB targets `(OUTP+OUTM)/2=VDD/2`. Other-load0.1/10 pF and active-output10 pF tests were also run.
- NMOS W20/L3.2 reference diode supplies the candidates' bias mirror from the same3.5 uA source; this diode is included in VDD power.
- Phi1: TX->VP and RX->ground. Phi2: TX->ground and RX->summing node. CF remains between summing node and SC output; reset shorts CF.
- Same10 ns clock edges,43% phase duty, nonoverlap;50 us startup reset; two frames, three integration cycles per frame, reset between frames.
- Ideal-switch control: Ron100 ohm, Roff1e12. Actual-switch test: complementary N W10/L0.8 and P W20/L0.8 transmission gates, bodies0/VDD, ideal complementary clock generators. As in the prior SC deck, switch junction areas are left at their existing defaults; no switch/layout redesign or new extracted switch parasitics were introduced.

Expected ideal step is `CS/CF*(VP+VREF)=0.6 V`, so each frame should read1.5->2.1->2.7->3.3 V. The circuit integrates the full sensor capacitance; it does not intrinsically cancel its nominal baseline.

## Nominal50 kHz measured results

Third sample in the second frame; signed error is relative to3.3 V. This is raw output error, not baseline-subtracted sensor sensitivity.

| OTA | Switches | Third sample (V) | Error (mV) | VDD power (uW) |
| --- | --- | --- | --- | --- |
| Current two-stage OTA | ideal | 3.301600850 | +1.600850 | 177.79 |
| Current two-stage OTA | tg | 3.358334990 | +58.334990 | 177.85 |
| Telescopic + CMFB | ideal | 3.299925924 | -0.074076 | 181.79 |
| Telescopic + CMFB | tg | 3.356616600 | +56.616600 | 181.84 |
| Gain-boosted telescopic + CMFB | ideal | 3.300002980 | +0.002980 | 227.77 |
| Gain-boosted telescopic + CMFB | tg | 3.356700842 | +56.700842 | 227.80 |

Gain boosting improves ideal-switch finite-gain behavior, but the transistor-switch raw errors remain close to57 mV for both. Thus extra OTA gain alone does not correct the dominant switch-related system error in this test. The two amplifiers need not have identical switch error because input capacitance, transient input error and clock coupling differ.

## Sensor response after offline baseline subtraction

For +50 fF, expected third-sample change is36 mV. These values subtract each design's own CS=2.5 pF result from its CS=2.55 pF result at the same clock and switch configuration. This is **offline calibration**, not an implemented cancellation circuit.

| OTA | Switches | Expected change (mV) | Measured change (mV) | Gain error (%) |
| --- | --- | --- | --- | --- |
| Telescopic + CMFB | ideal | 36.000 | 35.994876 | -0.01423 |
| Telescopic + CMFB | tg | 36.000 | 36.002358 | +0.00655 |
| Gain-boosted telescopic + CMFB | ideal | 36.000 | 35.999820 | -0.00050 |
| Gain-boosted telescopic + CMFB | tg | 36.000 | 36.020290 | +0.05636 |

`sensor_sensitivity.csv` also retains +100 fF at50 kHz and +50 fF at100/200 kHz. Raw offset, calibrated sensor slope and dynamic settling are separate quantities. A large raw offset can coexist with an accurate calibrated slope. No ADC resolution or noise-limited sensitivity follows from these deterministic numbers.

## Clock and settling behavior

Clocks50/100/200 kHz were tested for all three OTAs with both switch models. At200 kHz, both cascode candidates acquire millivolt-scale ideal-switch sample errors and large remaining late-phase changes. Gain boosting does not remove the speed limit. A smaller raw transistor-switch error at200 kHz can reflect cancellation between offset and settling error, not improved operation.

`comparison.csv` gives all18 nominal tests. `samples` in the JSON records give each of the six samples, summing-node error, common-mode error and late-phase change. `tail_settling_us` is settling to within0.1% of the ideal single step (0.6 mV nominal) **of the simulated phase-end value**, not convergence to the ideal transfer. Late-phase change compares the last20 ns before phase end against0.15 period before phase end. These diagnostics do not constitute an asymptotic or PVT-qualified settling specification.

## Selected corner tests

VREF and VP stay1.5/0.3 V; CMFB reference followsVDD/2 and clock levels followVDD. Native MOS file names are retained rather than assuming modern corner labels. Temperature/supply endpoints are exploratory assumptions. Native resistor corner remains typical.

| OTA | MOS file | VDD / temp / clock | Switches | Third sample error (mV) | Sampled CM error (mV) |
| --- | --- | --- | --- | --- | --- |
| Telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 50 kHz | ideal | -0.0917 | 88.316 |
| Telescopic + CMFB | bnbp49_5v | 5.5 V / 0 C / 50 kHz | ideal | -0.0420 | 2.753 |
| Telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 50 kHz | tg | +53.1912 | 112.800 |
| Telescopic + CMFB | bnbp49_5v | 5.5 V / 0 C / 50 kHz | tg | +61.4858 | 2.519 |
| Gain-boosted telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 50 kHz | ideal | -0.6981 | 88.072 |
| Gain-boosted telescopic + CMFB | bnbp49_5v | 5.5 V / 0 C / 50 kHz | ideal | +0.0032 | 2.765 |
| Gain-boosted telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 50 kHz | tg | +52.6557 | 112.701 |
| Gain-boosted telescopic + CMFB | bnbp49_5v | 5.5 V / 0 C / 50 kHz | tg | +61.5604 | 2.532 |
| Current two-stage OTA | wnwp49_5v | 4.5 V / 85 C / 50 kHz | ideal | +1.7131 | - |
| Current two-stage OTA | bnbp49_5v | 5.5 V / 0 C / 50 kHz | ideal | +1.6120 | - |
| Current two-stage OTA | wnwp49_5v | 4.5 V / 85 C / 50 kHz | tg | +55.0211 | - |
| Current two-stage OTA | bnbp49_5v | 5.5 V / 0 C / 50 kHz | tg | +63.2266 | - |
| Telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 100 kHz | ideal | -0.1056 | 88.309 |
| Telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 100 kHz | tg | +53.1651 | 112.792 |
| Gain-boosted telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 100 kHz | ideal | -1.0682 | 87.924 |
| Gain-boosted telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 100 kHz | tg | +51.1011 | 111.850 |
| Telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 25 kHz | ideal | -0.0879 | 88.317 |
| Gain-boosted telescopic + CMFB | wnwp49_5v | 4.5 V / 85 C / 25 kHz | ideal | -0.4093 | 88.196 |

At the low-supply/hot selected corner, the gain-boosted candidate has worse ideal-switch sample error than the ordinary telescopic candidate at50/100 kHz. Both show large common-mode error, around0.09 V with ideal switches and0.11 V with transistor switches. These observations require headroom/CMFB/bias investigation before layout; high nominal DC gain does not establish better corner accuracy. Additional25 kHz ideal-switch runs help distinguish clock-dependent error from a persistent operating-point limitation.

These are selected transient stress tests, not full PVT qualification, mismatch Monte Carlo or comprehensive feedback-loop certification. A completed simulation can still have unacceptable error, common-mode shift, saturation or insufficient settling. Inspect the table and traces before assigning a pass criterion; final ASIC accuracy requirements have not been fixed.

## Numerical checks

Main runs use10 ns maximum timestep. Selected cases were repeated at2 ns:

| OTA | Switches | Clock (kHz) | 2ns vs 10ns change (uV) |
| --- | --- | --- | --- |
| Telescopic + CMFB | ideal | 50 | +0.0261 |
| Telescopic + CMFB | tg | 50 | -20.6500 |
| Gain-boosted telescopic + CMFB | ideal | 50 | +0.0200 |
| Gain-boosted telescopic + CMFB | tg | 50 | -11.8206 |
| Telescopic + CMFB | tg | 200 | -0.5677 |
| Gain-boosted telescopic + CMFB | tg | 200 | -11.6459 |

The +50 fF transistor-switch sensitivity was also repeated at2 ns for both OTAs, subtracting a matching2 ns zero-change run. See`sensitivity_timestep_check.csv`. Differences of a few or tens of microvolts in calibrated slope must be judged against this numerical sensitivity; they do not establish a fabricated accuracy ranking.

The microvolt-scale ideal-switch results should be interpreted together with timestep changes and model limitations, not as fabricated microvolt accuracy.

Total saved simulations: 66; execution failures: 0. Model hashes in`model_hashes.json` match the previously exported OTA circuits. Each run has its own deck, log, ASCII waveform and measurements JSON under`results/`.

## Design implication

The simple telescopic candidate is the stronger starting point for this SC interface: it already sharply reduces ideal-switch error relative to the current two-stage OTA, while gain boosting adds about46 uW and does not materially improve nominal speed or remove the transistor-switch error. Keep the gain-boosted version as a higher-gain option if a later accuracy budget establishes a need for it.

Before layout, verify the chosen operating range and selected corner behavior, improve the switching/readout error mechanism and check whether stable offset calibration is appropriate. CMFB sensing area and signal-dependent common-mode error also remain design work. This study does not select a tapeout-ready OTA or authorize changing the SC topology.

## Limits

- New cascode candidates are schematic-level with estimated MOS junction geometry and no routed RC/well/substrate extraction; baseline includes prior extracted routing capacitances. Bias/reference voltages are ideal. Matching, noise, PSRR, reference-generator/clock-driver power and noise are excluded. Existing SCL-HSPICE-to-ngspice ignored-parameter/noise qualification issues remain.
- The CMFB prototype uses two large1 Mohm poly resistors, source-follower sensing and MOS compensation; compact physical realization has not been demonstrated.
- CS and CF are ideal linear capacitors; this does not validate MOS caps as precision SC/SAR capacitors. Intentional internal OTA compensation remains the existing PMOS devices.
- The active load and unused-output load are assumed, and real sensor/package/ADC loading is not known. No new DRC/LVS, PEX, mismatch or noise verification was performed for these architectures.
- Power is averaged fromVDD over seven post-startup clock periods; excludes external VP/VREF/CM-reference and clock-driver power and a real current-reference generator.

## Files and reproduction

- `models/`: identical exported telescope/gain-boost circuits plus current-OTA extracted baseline; no PDK model cards redistributed.
- `tb/`: six portable nominal50 kHz decks, with relative local-model includes. From this folder run`ngspice -b -o telescopic_tg.log telescopic_tg.cir` or`gain_boosted_tg.cir`. PDK expected at`/home/berson_meshak/pdk/scl08/ngspice_models49`.
- All six exported decks were separately simulated and matched their original run data; see`export_verification.json`. PASS here confirms reproducibility of the export, not qualification against ASIC requirements.
- `scripts/simulate.py`, `checks.py`, `report.py`: regenerate the run grid and report. Raw generated decks preserve the original execution paths; regenerate them after relocating. Portable decks use relative model paths.
- `plots/sc_waveforms.png`, `clock_accuracy.png`, `complement_and_power.png`; PDF copies included.
- `nominal.json`, `checks.json`, `comparison.csv`, `sensor_sensitivity.csv`, `timestep_comparison.csv` preserve numerical results and conditions.
