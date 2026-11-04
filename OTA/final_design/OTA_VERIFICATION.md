# Telescopic OTA: 2.5 V input common-mode revision, 1 November 2026

The native SCL08 BSIM3 models were actually simulated in ngspice with the previously verified CMFB-v2 extracted-capacitance network. Raising the **external NMOS cascode bias VBN from 2.4 V to 3.0 V** restores nominal gain when the **input common mode is 2.5 V**. Output CM reference remains **2.5 V** at nominal 5 V supply. Transistor sizes, reference-current setting, compensation, poly resistors, connectivity and GDS are unchanged. This is an operating-point revision, not a newly laid-out architecture.

## Nominal measured comparison

5 V, 27 C, typical native MOS/RPP, 3.5 uA ideal current reference, 5 pF explicit load on **each** output, balanced outputs. Actual output mean is approximately 2.4991 V due to finite CMFB error. Gain is at 0.01 Hz; UGF is the differential unity crossing. VBP=VDD-2.2 V.

| Configuration | Gain dB | UGF MHz | Differential PM deg | CMFB PM deg | VDD power uW |
|---|---:|---:|---:|---:|---:|
| Previous input 1.5 V | 88.44 | 1.343 | 89.30 | 70.71 | 231.96 |
| Input 2.5 V, old bias | 51.21 | 0.315 | 89.95 | 70.73 | 232.97 |
| Input 2.5 V, VBN=3 V | 87.53 | 1.366 | 89.31 | 70.74 | 233.04 |

At old VBN=2.4 V the input MOS has VDS=0.06765 V against VDSAT=0.25888 V, so it is not in the desired saturation region. At VBN=3 V its VDS=0.46278 V and VDSAT=0.17932 V. Native device operating-point diagnostics are in `headroom.json`. The external VBN bias source is ideal; no practical 3 V bias generator was implemented or qualified.

## Output swing is still restricted

The new input operating point does **not** retain the old wide output range. A separate fixed-input/fixed-output-CM screen at commanded differential output +/-1 V (approximately 2 V and 3 V outputs) falls to **58.93 dB** at its worst selected corner. This run completed numerically but is not an acceptable high-gain operating point. At +/-2 V differential with output CM tracking half-supply, some exploratory points have gain below unity and no unity crossing. Phase-margin statistics must never hide these gain/headroom failures.

The final narrower grid commands differential outputs **0 or +/-0.5 V**, giving nominal per-output endpoints **2.25 V and 2.75 V**. Both input CM and output CM references are fixed at 2.5 V, including supply variations. This range is characterized here; it is not a finalized ASIC swing requirement or proof of continuous-range bounds. If the system needs much wider swing with 2.5 V input CM, folded cascode or a different input/core arrangement should be compared rather than treating the bias change as a complete solution.

## Actual corner screening

1082 AC simulations: five native MOS cards (`tntp49_5v`, `bnbp49_5v`, `bnwp49_5v`, `wnbp49_5v`, `wnwp49_5v`), 4.5/5/5.5 V, 0/27/85 C, best/typ/worst native RPP =135 configurations. Each has differential and CMFB loop measurements at centered outputs with CL1/10 pF, and differential command +/-0.5 V with CL10 pF. Two nominal CL5 pF measurements complete the grid. These are assumed engineering conditions, not final chip requirements. Input/output CM are fixed at 2.5 V; the earlier exploratory `corner_bias_screen` instead tracks output CM=VDD/2 and is labeled separately.

- Differential: minimum gain **84.81 dB**, minimum PM **88.85 degrees**; missing unity crossings: 0.
- CMFB: minimum PM **65.73 degrees**; missing unity crossings: 0.
- Maximum AC operating-point output-CM error across the final grid: **3.147 mV**.

All crossings and failed/marginal wide-range measurements remain in JSON/CSV and per-run logs. A successful simulator exit is not itself a performance pass. The 60-degree loop screen and any gain targets remain provisional.

## Differential closed-loop transients

Ideal external differential-feedback fixture keeps the mean of the input voltages at its specified value. Command steps from -A to +A differential, so each output changes by A. Edges are 10 ns; main maximum timestep10 ns; settling is the last exit from a +/-0.1% band about each output's actual settled value, measured from the start of the edge. Static error is separate and not included in that settling band. CMFB controls the output average. This is an OTA benchmark, not the newly uploaded SCA or SAR circuit. The main comparison uses a 50 us sequence and algebraically equivalent linear controlled-voltage sources in its external feedback fixture. An initial 120 us / 2 ns batch using behavioral expressions had six runtime-limit failures; its records and logs remain in `transients_initial_120us_dt2.json` and are not counted as completed transient evidence.

| Input CM V | VBN V | CL per output pF | Step per output V | Worst 0.1% settling us | Worst static differential error mV |
|---|---|---|---|---|---|
| 1.5 | 2.4 | 5 | 0.1 | 0.836 | 0.0038 |
| 1.5 | 2.4 | 5 | 1 | 3.525 | 0.0380 |
| 1.5 | 2.4 | 10 | 0.1 | 1.228 | 0.0038 |
| 1.5 | 2.4 | 10 | 1 | 4.683 | 0.0380 |
| 2.5 | 2.4 | 5 | 0.1 | 3.544 | 0.2745 |
| 2.5 | 2.4 | 5 | 1 | 4.561 | 2.8890 |
| 2.5 | 2.4 | 10 | 0.1 | 5.174 | 0.2745 |
| 2.5 | 2.4 | 10 | 1 | 6.054 | 2.8890 |
| 2.5 | 3 | 5 | 0.1 | 0.820 | 0.0042 |
| 2.5 | 3 | 5 | 1 | 3.335 | 0.0432 |
| 2.5 | 3 | 10 | 0.1 | 1.209 | 0.0042 |
| 2.5 | 3 | 10 | 1 | 4.551 | 0.0432 |

Wide-swing transient cases may complete despite reduced endpoint gain; inspect their static error and do not use settling time alone as acceptance.

## Files and use in the original study

- `models/ota_cm2p5_C.spice`: renamed unchanged extracted macro `ota_telescopic_cm2p5`, pins **INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP**. Supply nominal5 V, VSS0, IREF3.5 uA, VCM2.5 V, VBN3.0 V, VBP2.8 V. The INP/INN mean must be established by the surrounding signal/feedback circuit; the VCM pin sets output mean only.
- `symbols/ota_cm2p5.sym`, `designs/ota_core.sch`: reusable symbol and unchanged transistor circuit with updated bias annotation.
- `designs/ota_cm2p5_ac_tb.sch`, `ota_cm2p5_transient_tb.sch`: native Xschem benches; model includes assume the local PDK location. Run Xschem from this project using `./open_xschem.sh`. The opened AC bench uses an ideal fixture to measure gain; it is not a physical feedback circuit.
- `tb/ac.cir`, `tb/transient.cir`: run from `tb` with `ngspice -b ac.cir` or `ngspice -b transient.cir`. Benches write raw files for interactive plotting; in ngspice use `load ota_cm2p5_ac.raw` then `plot db(v(od))`, or `load ota_cm2p5_transient.raw` then `plot v(op) v(om)`.
- `layout/ota_telescopic_layout.gds`: byte-identical to the verified CMFB-v2 GDS. `verification/provenance.json` records source hashes and inherited DRC/LVS results. **No new DRC/LVS is claimed**, because geometry/connectivity did not change. A new practical bias generator would need its own layout/checks.
- `verification/export.json`: Xschem symbol pin order, actual netlisting and exported ngspice AC regression.
- `bias_screen`, `corner_bias_screen`, `fixed_cm_screen`, `final_ac_grid`, `transients`: JSON/CSV measurements. `plots/` contains PNG/PDF comparisons. Scripts reproduce the study with the original adjacent CMFB-v2 project and local PDK.

## Limitations

The existing adapted capacitance extraction and native model warnings are inherited. Full wire/contact/well/substrate RC, quantitative noise, mismatch, startup/reference generation and silicon qualification remain open. MOS gate capacitors remain compensation elements; this work does not establish precision SC/SAR capacitor feasibility. The newly uploaded 10 kHz, 40 pF feedback, 2.5 V reference SCA circuit has **not** been integrated or validated here. No automatic GitHub publication is performed by this revision.

## Timestep refinement

Two selected final-bias cases were repeated at a 2 ns maximum timestep using the same 50 us sequence and linear feedback fixture. CL5 pF, 0.1 V per-output step: settling 0.82039 -> 0.81679 us. CL10 pF, 1 V per-output step: settling 4.55079 -> 4.54289 us. These selected checks do not extend the characterized PVT output range. Records: `fine_transients.json`, `verification/fine_timestep.json`, `fine_results/`.
