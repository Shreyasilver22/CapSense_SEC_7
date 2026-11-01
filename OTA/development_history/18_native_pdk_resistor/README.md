# 18_native_pdk_resistor: Native SCL08 RPP resistor validation

Development order: **18**. Date / ordering evidence: **31 October, after resistor screening 2026**.

Native resistor, physical cell, symbol, topology image and validation.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/architecture_study_20261031/pdk_resistor_validation/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Native SCL08 resistor validation for OTA compensation

The OTA now has a trial implementation using the local SCL08 **P-poly resistor RPP subcircuit**, directly included from ngspice_models49/res/{typ,best,worst}/ppr without rewriting its resistance or temperature model. This replaces the previous ideal 16 kohm element. No proprietary model cards or rule decks are copied into this result folder.

## Device choice and native model coverage

Five native resistor types were inspected: N-poly RPN, P-poly RPP, N-diffusion RDIFFN, P-diffusion RDIFFP and N-well RNW. P-poly was selected as a first candidate because its supplied temperature coefficient is lower than N-poly/N-well and it avoids introducing an explicit diffusion/well junction as its resistive body. This does not establish it as optimal for every area/noise requirement.

The supplied RPP is a two-terminal subcircuit with R=Rsheet*L/W, typical sheet 28 ohm/square and TC1=1.049e-3 /degree C. Best/worst sheet values are 24/32 ohm/square. Native models do not supply terminal capacitance, a voltage coefficient, excess/flicker resistor noise coefficients, contact resistance or distributed terminal geometry. Therefore native-model replacement alone cannot validate those effects. Ngspice successfully parses the original HSPICE-style subcircuit; no translation of the resistor card was needed.

Standalone 1 V tests measured approximately 62.5 uA, confirming the 16 kohm resistance. The reusable symbol testbench was actually netlisted by xschem and simulated with ngspice, giving 62.4999 uA.

## Physical resistor cell

Ten series resistor bodies, each W=2.4 um, L=137.143 um, nominal 1600.0017 ohm, give 16000.0167 ohm total body resistance. The GDS has actual poly, P-type implant/reversal masks, resistor markers, resistor terminal markers, contacts and M1 connections. Its two ports are A and B. Adjacent rows alternate direction through M1 links; resistor bodies are straight sections, not electrically shorted folds.

- Local original SCL KLayout DRC deck: zero reported markers.
- Local original SCL KLayout LVS deck: resistor-cell network matches an independent sheet-resistance-derived reference (native RPP primitive representation).
- Deliberate 20 kohm reference: fails LVS as expected.

These checks apply to the standalone resistor cell, not an integrated OTA-plus-resistor macro. Existing OTA DRC/LVS does not validate adding this resistor. The complete six-capacitor/series-resistor OTA layout still needs integration and extraction.

## Parasitic estimates, explicitly not full PEX

The supplied Magic coefficients and actual drawn area/perimeter were used to estimate unshielded capacitance: poly approximately 0.46305 pF total and M1 approximately 0.01359 pF, total about **0.47664 pF**. Each segment's poly capacitance is split equally onto its two terminals; M1 capacitance is distributed equally over the eleven series-network nodes. Ground reference is VSS/substrate. This model does not resolve shielding, mutual coupling, bends, contact fringing or actual field capacitance; it is a geometry-based screening estimate, not a native parasitic extraction result. Core routing capacitances remain the prior v3 extraction and are not updated for new routing.

An additional sensitivity variant estimates terminal resistance from 1.8 um poly extension at each end, 28 ohm/square, plus the local technology's 5 ohm poly-contact coefficient: 21+5=26 ohm per end, 20 ends -> **520 ohm** in addition to the 16.00 kohm body. Thus estimated port resistance is 16.52 kohm at nominal temperature. Those added ideal elements are separate geometry/contact estimates, not supplied RPP subcircuit parameters or a calibrated extraction.

## Actual OTA simulation results

All cases use six equivalent MOS compensation units and Iref=3.5 uA, supply=5 V. Nominal point CL=5 pF and input DC=2.5 V. Minimum PM spans 1/5/10 pF and 1.5/2.5/3.5 V. Settling is the worst rising/falling 2 V follower step into 10 pF, to 0.1% about actual final output, not total ADC accuracy.

| Model case | UGF (MHz) | Minimum checked PM (degrees) | 2 V settling at 10 pF (us) |
|---|---:|---:|---:|
| Ideal 16k baseline, 27 C | 1.412 | 69.71 | 1.962 |
| Native typical RPP only, 27 C | 1.412 | 69.71 | 1.962 |
| Typical RPP + estimated C, 27 C | 1.404 | 67.60 | 2.007 |
| Typical RPP + estimated C and terminal R, 27 C | 1.410 | 68.08 | 2.002 |
| Best resistor model + estimated C, MOS nominal, 27 C | 1.381 | 65.46 | 2.022 |
| Worst resistor model + estimated C, MOS nominal, 27 C | 1.432 | 69.68 | 1.987 |
| Typical RPP + estimated C, all devices at 0 C | 1.524 | 68.26 | 1.966 |
| Typical RPP + estimated C, all devices at 85 C | 1.206 | 66.52 | 2.083 |

Resistor best/worst do not mean better/worse amplifier response: the compensation zero moves with resistance. These are resistor-corner checks with nominal MOS process, not full MOS PVT. Corner and temperature checks are separate, not all combinations. Core gain remains about 87.57 dB and nominal VDD power 176.84 uW at 27 C. A 1 ns timestep repeat of the terminal-R/C variant gives about 2.00051 us versus 2.00196 us at 5 ns. At 4 V input and CL=5 pF, the same variant has only **41.79 degrees PM**: the high-voltage stability issue remains unresolved.

The core used in these trials retains the documented what-if capacitor-count scaling (nine extracted branches scaled to six equivalent units), so it is not a newly extracted six-unit OTA layout. Updated integrated routing/gate capacitance and physical resistor realization are still required.

## Noise checks

Native RPP standalone thermal noise at 27 C is 16.2855 nV/sqrt(Hz), agreeing with sqrt(4*k*T*16k). The prior ideal SPICE resistor already includes thermal noise, so replacing it with an equal-resistance RPP subcircuit does not add a new thermal-noise mechanism. The native resistor card does not model excess/flicker noise; absence of those coefficients is not proof of negligible physical excess noise.

Actual ngspice follower noise integrations from 1 Hz to 1 MHz:

| Case | Output RMS (mV) | Input-referred RMS (mV) |
|---|---:|---:|
| Ideal 16k | 3.13636 | 3.15586 |
| Native typical RPP | 3.13636 | 3.15586 |
| RPP + estimated C | 3.14072 | 3.15961 |

These relatively large full-OTA numbers are raw local-model outputs, not a validated noise budget. The known MOS/HSPICE translation warnings and unqualified transistor-noise behavior remain. No claim of low noise, ADC resolution, SNR, excess-noise completeness or silicon agreement is made. The standalone resistor thermal check is narrower than the full-OTA noise qualification.

## Files and reuse

- models/scl08_rpp_16k.spice: reusable two-terminal wrapper containing ten native RPP subcircuit instances; includes the user's local typical PDK model. Intrinsic resistor model only, without estimated C/R.
- symbols/scl08_rpp_16k.sym: new project-local xschem wrapper symbol, not an official PDK symbol. Include models/scl08_rpp_16k.spice in the parent design. Its value is fixed by the wrapper/body geometry; editing display text does not resize it.
- tb/resistor_symbol.sch and .spice: native xschem symbol testbench actually netlisted and simulated.
- layout/rpp_16k.gds and reference.cdl: standalone physical cell and LVS reference.
- verification/drc.lyrdb and lvs.lvsdb plus logs: checks; negative_lvs reports intentional failure.
- tb/pdk_typ_C.cir and pdk_typ_RC_est.cir: portable relative-model OTA large-step benches; run from tb with ngspice -b.
- models/npdk_*.spice: full OTA trial netlists using actual PDK subcircuits; estimated parasitic additions are named separately.
- summary.csv/json, terminal_R_summary.json and final_summary.json: numerical results. ac/transients files hold original runs; terminal_R_AC/transients files hold the extra sensitivity case; fine/final_stress files hold repeat and high-bias checks.
- noise_summary.json and results/noise_*: raw full-OTA noise results; results/resistor_thermal.dat and resistor_noise.log: standalone thermal check.
- plots/pdk_resistor_comparison.png/pdf: comparison figures.
- scripts/: generation and reproduction. Requires local SCL PDK, KLayout, xschem, ngspice and numpy/matplotlib. Raw full-run decks retain staging paths; scripts regenerate them in the current project location. The supplied portable benches use relative trial-model paths. The simulator still references proprietary PDK files locally; these are not copied or published.

No source PDK files, system packages or SC design were changed. No GitHub publication was performed. The remaining practical task is integrating the resistor cell with the OTA layout, re-extracting all relevant capacitances/resistances using a validated flow, and checking noise/PVT with qualified models.
