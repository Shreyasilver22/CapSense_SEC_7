# 06_further_capacitor_analysis: Further capacitor / OTA analysis

Development order: **6**. Date / ordering evidence: **After initial metal-cap study 2026**.

Historical compensation exploration; inspect the included report and measurements.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/further_capacitor_analysis/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Further capacitor exploration: OTA application check

This is a separately saved nominal comparison of six modern-extracted capacitor finalists in the unchanged tuned SCL800 eight-MOS OTA. The capacitor sweep/layouts/models are in ../../../capacitors/layout_optimization_v2. No shared library, earlier OTA design or GitHub files were modified.

## Outcome with one consistent modern capacitor flow

The modern-extracted reference gives about747kHz UGF,70.65deg nominal phase margin,64.69deg minimum checked phase margin and0.974us small-step settling. The balanced candidate (24um strips,1.5um slots,3um spines,0.5um top-plate inset) gives about748kHz,70.95deg,65.02deg and0.944us respectively. Large-step settling is effectively unchanged at about3.7us and slightly slower for the balanced candidate in this metric. No overall speedup or global optimum is claimed.

A1ns timestep repeat gives worst small-step settling0.9705us reference versus0.9415us balanced, and large-step settling3.7122us versus3.7192us. Compare RESULTS.md for all finalists and results/fine_timestep_check.json for both step polarities. Existing old-extractor numbers must NOT be mixed into this comparison.

The balanced candidate model is cap2_w24_g1p5_r3_i0p5, with Cmut3.99868pF, Ctop-sub0.183479pF and Cbot-sub4.50102pF. TOP=n2, BOT=out and SUB=vss. This is a capacitor-only geometry change; no transistor resizing or current retuning was performed. The six-pin interface remains that of the same eight-MOS core/bias network: inp,inn,out,vdd,vss,iref. IREF2.5uA,5V,27C.

## Tests

54AC runs span CL1/5/10pF x follower DC input1.5/2.5/3.5V for six finalists.36base transients cover100mV and2V follower steps at the three loads. AC uses a1e12H DC-feedback inductor and1e12F AC-ground capacitor; it estimates follower return ratio, not a full SC-phase loop injection. AC150points/decade from1Hz to1GHz. reltol1e-5,vntol1e-8,abstol1e-12,numdgt12. Transient maximum timestep5ns,duration90us,40us plateaus,10ns input edges. Four selected1ns repeats check numerical repeatability.

Settling is the last exit from0.1% of the step amplitude around actual final output, measured from input edge start. It excludes static error to ideal input. The roughly-0.206mV small-step static error remains; compensation geometry does not fix it. No claim of total small-step100uV accuracy is made.

The balanced AC/small/large portable SPICE benches were simulated and AC data agree with the sweep. This further exploration did not generate a new native OTA schematic; the unchanged core is represented by hand-authored SPICE benches. Capacitor-only native symbols were netlisted and simulated in the companion project.

## Use

spice/models.inc points at the local authorized SCL transistor deck; the deck itself is not copied. Run from tb/:

```bash
ngspice -b -o ../results/balanced_ac.log balanced_ac.cir
ngspice -b -o ../results/balanced_small.log balanced_small.cir
ngspice -b -o ../results/balanced_large.log balanced_large.cir
```

For another machine update spice/models.inc to its authorized model path. models/cap_layouts.lib.spice is a frozen modern capacitor snapshot. Re-run the sweep with:

```bash
python3 scripts/analyze.py --cap-project /path/to/layout_optimization_v2/ota_shortlist \
 --mos-model /path/to/tntp49_5v
```

The companion capacitor report.py --ota-project /path/to/this/folder regenerates the plots/tables. scripts/fine_check.py and package_selected.py refer to this installed project's companion capacitor folder for the selected geometry. Fine checks and direct bench simulations do not require Magic because they use frozen extracted models.

## Limits

Modern Magic8.3.688 meets the capacitor technology header's minimum requirement, and native/raw all-three-capacitor values agree for the36final cells. This fixes the observed native substrate-export discrepancy in this new flow; it does NOT validate real physical capacitance, detailed3D edge fields or manufacturing acceptance. Earlier published capacitor models remain unchanged and need regeneration before precision work relies on them.

Transistor HSPICE-parameter compatibility warnings remain. No PVT, mismatch, noise, real reference generator, voltage-dependent capacitor/loss/leakage, substrate disturbance, full SC switching, ADC kickback, startup or final-layout OTA wiring extraction was performed. Routing-resistance proxies were not included in the capacitor/OTA models. No final-chip or formal capacitor LVS/sign-off claim is made. The large-step result still exceeds the illustrative2.45us SC amplification window, which remains an unfrozen scenario.

legacy_8p3p105 contains historical old-model evidence only; its waveforms and summary must not be treated as current modern-extractor results. No online publication was performed.
