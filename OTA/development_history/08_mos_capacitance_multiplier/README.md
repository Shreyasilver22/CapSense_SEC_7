# 08_mos_capacitance_multiplier: MOS capacitor and capacitance-multiplier feasibility

Development order: **8**. Date / ordering evidence: **Before MOS-only selection 2026**.

Feasibility experiment, not a qualified active precision capacitor.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_cap_multiplier_feasibility/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Simple MOS-capacitor and capacitance-multiplier feasibility test

Unchanged tuned SCL800 eight-MOS OTA with5V supply,27C,2.5uA ideal reference current and5pF external load. This is a pre-layout concept comparison, not a new finalized OTA design or physical multiplier implementation. Earlier capacitor/OTA projects and GitHub files are unchanged.

## Cases

1. Ideal4pF compensation capacitor.
2. Ideal4.12549932pF, matched to the MOS model's capacitance at the tested DC point.
3. Modern-extracted refined metal capacitor, near4pF including both substrate parasitics.
4. Full MOS capacitor: ten parallel PMOS devices, each W20um,L10um, with gate connected to n2 and source/drain/body tied to out.
5. Small MOS capacitor: two identical PMOS devices without multiplication.
6. Small MOS capacitor plus an IDEAL behavioral5x current multiplier.

Full MOS gate-area proxy=10*20*10=2000um2; small MOS gate-area proxy=400um2. These are gate areas, not complete layout areas. Well spacing/taps, source/drain access, routing and the eventual active multiplier's area are excluded. No physical MOS-capacitor layout was generated.

## MOS connection and multiplier

The PMOS isolated N-well is assumed tied to the output along with its source and drain. Its gate connects to n2 through a0V current-sensing source:

```spice
VSENSE n2 gc 0
MCAP out gc out out P W=20u L=10u M=2
BMULT n2 out I={4*i(VSENSE)}
```

The B source supplies four additional copies of the small MOS gate current. Total terminal current is therefore5times the sensed gate current. Its terminals are n2/out, so it multiplies the MOS's floating two-terminal apparent capacitance. It does not create a second Miller factor from the OTA's overall gain. The OTA's original Miller-compensation mechanism remains present.

This behavioral source has unlimited bandwidth, no noise, no explicit supply draw/headroom limit and no added poles/delay/saturation. A hardware current mirror/amplifier implementation would not have those ideal properties. Identical response to a five-times-larger MOS is a deliberate consistency check, not proof of a realizable free-area/power improvement.

The PMOS body connection assumes an isolated, properly contacted N-well. Its N-well/substrate capacitance, resistance and diode behavior are not included in this MOS-only model test. Ordinary gate/source/drain/body connectivity must not be copied into a layout with an incorrectly biased well. No NMOS body was tied to a moving signal node. During the tested large step, full MOS gate-body voltage stays about+0.183to+2.198V, while output stays within roughly1.49to3.50V.

## Results and interpretation

See RESULTS.md and plots/mos_multiplier_comparison.png/.pdf. Full MOS and ideal5x small-MOS cases produce ~740.5kHz UGF,76.86-degree phase margin and3.99us worst2V-step dynamic settling. The small MOS alone reaches only46.80degrees phase margin. MOS-only cases have less modeled substrate loading than the metal case because N-well/layout parasitics were omitted; this is NOT evidence that a fabricated MOS capacitor is already better.

The41-point C-V characterization sweeps gate/body voltage-2.5to+2.5V with source/drain/body at2.5V, using1kHzto1MHz AC. The full MOS model is flat near4.1255pF over the tested OTA's positive gate-body range, but varies strongly outside that range (down to~0.852pF in this sweep). The ideal matched-capacitor control reproduces the full MOS AC response at this bias. This supports MOS-alone compensation as a candidate to characterize before adding an active multiplier; it does not establish SC/SAR precision suitability across arbitrary terminal voltages.

The multiplier preserves the underlying MOS C(V) dependence; it does not make a nonlinear capacitor linear. Quiescent OTA supply power is~175uW in these cases, but the ideal multiplier has NO supply model, so this is not total hardware power for a multiplier implementation. No noise comparison or precision ADC/SC qualification is claimed.

## Simulation details

Six nominal AC cases and twelve nominal follower transients. AC150points/decade from1Hzto1GHz at a follower DC point of2.5V, using1e12H DC feedback and1e12F AC ground fixture. Small step2.5->2.6V; large step1.5->3.5V. Pulse edges10ns,40us plateaus,90us total duration,5ns max timestep. reltol1e-5,vntol1e-8,abstol1e-12,numdgt12.

Settling is the last exit from0.1% of step amplitude around actual final output, worst polarity. It excludes static tracking error to the ideal input. Gate-body voltage and output extrema are recorded. No load/supply/temperature/process/mismatch/startup sweep was performed. Existing ngspice warnings about ignored HSPICE parameters, including PMOS capacitance entries, remain; C-V/dynamic results need model compatibility validation before precision use.

## Run and inspect

Readable core variants are in models/. The ideal multiplier is one explicit B source, clearly marked in mos_small_ideal_5x.inc. All original inputs/logs/numeric waveforms are in results/<case>/. The private SCL transistor deck is referenced locally and is not bundled.

From tb/:

```bash
ngspice -b -o ../results/multiplier.log mos_small_ideal_5x_ac.cir
ngspice -b -o ../results/multiplier_step.log mos_small_ideal_5x_large.cir
```

spice/models.inc points to the user's authorized local tntp49_5v deck; update it for another machine. scripts/run.py reproduces the complete comparison and C-V characterization from the earlier local tuned-core source; scripts/report.py verifies equivalence, creates portable benches and plots. The core and metal-model snapshots are included for inspection. No native xschem schematic or transistor-level multiplier amplifier was created in this simple experiment.

A practical next comparison should first characterize a layout-realizable MOS Cc including well parasitics; only then design an active multiplier with explicit power, noise, bandwidth, swing and stability limits if needed. The present test is encouraging for MOS Cc alone and only demonstrates the ideal multiplier concept. No public upload was performed.
