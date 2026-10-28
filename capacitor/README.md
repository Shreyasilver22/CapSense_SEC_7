# Reusable SCL08 capacitor library

Standalone experimental metal-overlap capacitor library for SCL CP8D 800 nm. It provides editable two-pin/three-pin xschem symbols, generated GDS layouts, explicit-substrate SPICE models, examples, and verification tools. No OTA circuit is included; OTA integration belongs separately under OTA/design_2.

Start with **START_HERE.md**. **CATALOG.md** maps target values to achieved values and GDS files.

## How the symbol works

- `scl08_cap2.sym`: two signal pins, TOP/BOT. A SPICE wrapper connects substrate to global node 0. This is convenient in the attached SC integrator, OTA compensation network and basic CDAC examples when the actual substrate is grounded.
- `scl08_cap3.sym`: TOP/BOT/SUB, for explicit substrate wiring. Recommended when integrating blocks or studying substrate effects.
- Both have an editable `value` attribute. The symbol shows the target value and the extracted mutual capacitance for the PREPARED variant.
- Both retain plate-to-substrate capacitance. A two-pin drawing does not turn the physical device into an ideal floating two-terminal capacitor.
- The value selects a generated subcircuit alias, not a freely scalable ideal C element. Change to any already-prepared token and simulate immediately; prepare a new token before simulation. Unsupported values fail rather than produce an ideal fallback.

Allowed value tokens are positive concrete SPICE numbers using suffix f,p,n,u,m, e.g. 2.5p, 7.5p, 3p, 11.384f. Use the shown spellings for prepared variants. Alternate numerical spellings (e.g. 2.50p) require a prepared alias even if they represent the same number. Brace expressions, design-variable expressions, and trailing F are not supported by the layout request parser. Symbol names and concrete values must occur at the schematic's top level for automatic scanning; prepare hierarchical child schematics separately or use --value.

A project-authored converter reads documented raw Magic `.ext` node-to-substrate and explicit coupling records. It preserves three capacitors in every model. Native PDK extraction compatibility remains unresolved; see limitations below.

## The 2.5 pF and 7.5 pF pair

The first unit's raw extraction gives 11.384 fF mutual capacitance. This release uses 220 and 660 units for nominal values 2.50448 pF and 7.51344 pF. They have an exact nominal 3:1 mutual-capacitance ratio in this extracted model and equal +0.1792% absolute target error. We intentionally used 660 units rather than independent nearest rounding to 659 for 7.5p. This is a ratio-oriented unit-count choice, not a claim of statistical matching, common-centroid placement, or 10-bit accuracy.

Array footprints and both substrate capacitances are substantial. Inspect CATALOG.md and results/catalog.csv before adopting them. Corresponding layout files are `layouts/requested_2p5p.gds` and `layouts/requested_7p5p.gds`. Internal GDS cell names use unit counts (scl08_cap_n220 and scl08_cap_n660); each alias file contains that named cell. Reuse the identified cells rather than duplicating/relabeling geometry ambiguously.

For other requirements, edit requests.json explicitly. Remove a units override to use nearest-unit rounding. Limits are 1 to 4096 units; out-of-range requests are rejected, not clipped. Small requested values below one-unit capability are therefore not representable. The requested value is not a guaranteed manufacturing tolerance.

## Mapping onto the attached SC integrator

In the supplied figure, C_FB sits between the OTA inverting-input summing node (to the right of the phase-2 switch) and V_SIG/OTA output, with the reset switch in parallel. That remains true regardless of the capacitor symbol's drawing style.

A starting wiring option for an illustrative 2.5p feedback capacitor:

```spice
.include "/absolute/path/to/this_library/models/generated_caps.lib.spice"
XCFB SUM VOUT 0 scl08_cap_2.5p
* Or the identical substrate-grounded two-pin wrapper:
* XCFB SUM VOUT scl08_cap_gnd_2.5p
```

Use ONE instance, not both. TOP -> SUM, BOT -> VOUT, SUB -> substrate ground (normally 0). TOP has smaller substrate loading than BOT in these extractions, so this is a reasonable starting orientation for the high-impedance summing node, but both orientations need system simulation. BOT parasitics load the OTA output. SUM parasitics reduce the feedback factor and affect settling. Switching-node parasitics may transfer additional charge depending on the clock sequence. No claim of parasitic insensitivity is made.

`examples/sc_feedback_fragment.sch` is a wiring fragment, not a complete integrator simulation. It verifies those three pin-to-net assignments and leaves the OTA, reset switch and phase switches to the SC designer. The 2.5p role is illustrative; neither requested value's role is finalized. Do not connect substrate to VREF merely because VREF is the OTA common-mode reference.

The dashed Sensor block in the figure is an external, pressure-dependent Cs0 + deltaCs if that is the physical sensor architecture. A nominal 7.5 pF sensor should remain a variable sensor model during simulation and the actual sensor at the chip interface. The on-chip 7.5p cell is available as a fixed capacitor if the final architecture needs one; it cannot sense pressure by itself.

A rail/common-mode/clock plan must be chosen before simulating the complete figure. Its charge step depends on sensor excitation, VREF, capacitor ratios, reset interval and output headroom. Selecting the two capacitances alone does not establish a working SC readout.

## OTA compensation

The same symbol can be placed between the OTA's first-stage output n2 and final output. An initial mapping is TOP -> n2, BOT -> out, SUB -> substrate ground; compare orientation effects as needed. The prepared 3p target has an extracted mutual value around 3.00538 pF, plus separate loading at both OTA nodes.

This is NOT equivalent to replacing our old ideal 3 pF Cc by another ideal 3 pF. Compensation affects pole locations, zeros, loop stability and settling; bandwidth is not set by Cc alone. Both stage-node parasitics and the actual layout must be included when OTA work resumes. No OTA transistor sizing, compensation value or previous performance report is updated by this library release.

## SAR ADC use

A capacitive SAR DAC uses matched unit-capacitor groups with architecture-dependent weights; it does not automatically need the SC block's 2.5 and 7.5 pF values. Noise, matching, reference settling, switching strategy and required resolution determine the unit and array choices.

Prepared illustrative weights are 1/2/4/8 units, requested as 11.384f/22.768f/45.536f/91.072f. `examples/cdac_four_weights.cir` connects TOP plates to a common DAC node and BOT plates to ideal step sources, with SUB grounded. It demonstrates charge sharing and the effect of TOP substrate parasitics. It is NOT a complete 4-bit SAR converter or a final CDAC: no comparator, SAR logic, sampling switch sequence, dummy LSB, common-centroid/dummy layout, mismatch, noise, extracted resistance or reference driver is included.

The example's plateaus are checked against charge conservation including substrate loading. Passing that check does not establish INL/DNL, ENOB or ADC timing. Separate GDS variants demonstrate unit weighting but are not a matching-qualified array floorplan.

Primary architectural reference: Analog Devices, Understanding SAR ADCs: https://www.analog.com/en/resources/technical-articles/successive-approximation-registers-sar-and-flash-adcs.html

## Setup inside another xschem project

Add equivalent lines to the project's own xschemrc, retaining that project's other library paths and netlist directory:

```tcl
set cap_lib "/absolute/path/to/capacitor"
append XSCHEM_LIBRARY_PATH ":$cap_lib/symbols"
source [file join $cap_lib scripts symbol_helpers.tcl]
```

Place `scl08_cap2.sym` or `scl08_cap3.sym`; select it and press q to edit value. Add one SPICE model include using an absolute path:

```spice
.include "/absolute/path/to/capacitor/models/generated_caps.lib.spice"
```

Do not use demo-relative includes unchanged when copying the symbol into an unrelated project. For new values, prepare the actual schematic being edited. Restart xschem or source models/catalog.tcl and redraw to refresh extracted-value labels after a terminal rebuild. Headless tests verified native xschem netlisting and the displayed extracted-value strings in native SVG export; interactive GUI clicks remain untested.

Two-pin wrappers always connect substrate to SPICE 0, not an arbitrarily named VSS at a nonzero voltage. Use the three-pin symbol for nonzero or independently modeled substrate nodes. A two-pin cell still needs a real grounded substrate in the chip; no additional metal plate or external chip pin is implied.

## Generation workflow

From this library directory:

```bash
python3 scripts/prepare.py --schematic "/path/to/SC_readout.sch" \
  --pdk-root "/path/to/scl_cp8d"
```

Set SCL08_CAP_PDK_ROOT to your authorized scl_cp8d directory before launching xschem when regeneration is needed. Prepared model simulation does not require the PDK.

The xschem demo also provides **Save + generate layouts/models for edited values**. That launcher saves the open schematic and runs the same backend asynchronously, then reloads the display catalog. It uses SCL08_CAP_PDK_ROOT from the environment. The user must have an authorized compatible local PDK. Another machine must update that path. The GUI pipeline is provided but not interactively tested; its scanning/generation backend was tested with a newly requested 4p value, including DRC, model generation, xschem netlisting and ngspice simulation.

For an individual value: `python3 scripts/prepare.py --value 4p --pdk-root "/path/to/scl_cp8d"`.

For a full rebuild:

```bash
python3 scripts/build.py --pdk-root "/path/to/scl_cp8d"
python3 scripts/symbols.py
python3 scripts/examples.py
python3 scripts/verify.py
python3 scripts/report.py
```

verify.py includes the recorded end-to-end 4p fixture in results/prepare_workflow. If reproducing from a source-only copy, create that fixture with scripts/make_prepare_fixture.py and run prepare.py on it before verify.py. NumPy and Matplotlib are Python dependencies. KLayout must provide embedded Python/pya; generate.py runs inside KLayout. ngspice, xschem and Magic are external tools. scripts/common.py contains unit quantization and concrete-value validation. Editing requests.json changes requests; editing a symbol without preparing a new alias cannot create a physical layout.

Generator geometry: 20 x 20 um overlap units, 40 x 28 um pitch, two independent connected metal networks, no plate-shorting vias. Partial final rows allow arbitrary integer unit counts. It verifies each metal network's connectivity and total mutual-overlap area before GDS output. Full arrays are extracted as flat layouts, with intra-array routing included. This is a project-authored generator, not a native foundry KLayout PCell, and it is not registered as a GUI PCell.

## Files and validation

- symbols/: two generic editable symbols.
- layouts/: independently importable count-based and requested-value GDS aliases.
- models/generated_caps.lib.spice: count-based three-terminal cores, value aliases, and two-pin substrate-grounded wrappers.
- results/catalog.csv/json: target/achieved values, unit counts, footprint, parasitics and DRC status.
- results/<cell>/: DRC reports, raw .ext, native export, Magic layout and logs.
- results/verification.json: actual model-current, nominal ratio, charge-sharing and symbol/workflow checks.
- examples/value_demo.sch: runnable 2.5p/7.5p/3p demonstration with embedded waveform graph.
- examples/sc_feedback_fragment.sch: SC feedback pin mapping.
- examples/cdac_four_weights.cir and two_pin_demo.cir: runnable usage examples.
- plots/: symbol preview and capacitance/area/charge-sharing figures.

Every generated physical cell was run through the supplied KLayout DRC deck with zero reported markers. Both plates' substrate-current paths and plate-to-plate transfer were numerically checked. Native two-pin and three-pin symbols netlisted and simulated; the two-pin wrapper retains the extra TOP substrate load. The ratio-oriented pair has 3.0 nominal mutual-C ratio. CDAC plateau voltages agree with the supplied lumped network's charge conservation. These are bounded implementation checks, not physical-model qualification.

## Unresolved limitations

Installed Magic 8.3.105 is older than the technology header's 8.3.579 requirement. Native ext2spice export omits BOT-to-substrate capacitance present in raw .ext; the project converter explicitly retains the raw node and coupling terms. This discrepancy has NOT been reconciled in a supported tool flow. No fabricated capacitance measurements, validated voltage coefficients/ratings, mismatch/noise/PVT models or conductor-resistance extraction are supplied. Models assume frequency-independent lumped capacitors; AC/model tests cannot establish real wideband physical behavior.

The stock PDK LVS deck has no dedicated capacitor-device recognition. DRC does not prove formal capacitor LVS, electrical accuracy, custom-cell acceptance, or final-chip connectivity. No bypass or foundry-sign-off claim is made. Upgrade/reconcile extraction, agree capacitor/LVS treatment with the fabrication flow and validate final-chip surroundings before fabrication. Extra routing, nearby metal, substrate contacts and guard rings change the extracted network. The requested capacitance is plate-to-plate mutual C, not total loading seen from either terminal to ground.

Authored code/layouts/symbols are reusable under LICENSE; foundry files are not bundled, and foundry-derived data remain subject to the applicable PDK terms. This directory contains capacitor work only; no foundry technology/rule/model decks or OTA circuits are bundled.

## Repository quick start

From the repository root (Linux/WSL):

```bash
cd capacitor
xschem --rcfile xschemrc examples/value_demo.sch
```

For new values and regenerated layouts, first set the local authorized PDK path:

```bash
export SCL08_CAP_PDK_ROOT="/your/path/to/scl_cp8d"
python3 scripts/prepare.py --value 5p --pdk-root "$SCL08_CAP_PDK_ROOT"
```

Prepared 2.5p/7.5p/3p/4p/6p/8p/10p and 1/2/4/8-unit CDAC examples are listed in CATALOG.md. Full layouts correspond to explicit mutual-capacitance models plus substrate loading; requested capacitance is not a guaranteed manufacturing tolerance. The 6/8/10p files are standalone capacitor variants only.

The original fixed-size v1 experiment is superseded by this value-driven source and its preserved extraction-format limitation. No duplicate legacy release or unrelated OTA results are included. Generated plots/catalog/DRC and raw extraction evidence are committed; bulky transient raw files and logs are reproducible and ignored.

## Layout-optimized capacitor variants

See [layout_optimization_v1](layout_optimization_v1/README.md) for the baseline/compact/slotted comparison, prepared near3/4/8pF layouts, explicit-substrate models, editable style/value symbols and reproducible checks.

The highlighted slotted 4p candidate has about 3.99574pF mutual capacitance, 0.615322pF TOP-substrate and 4.80970pF BOT-substrate capacitance, with a 0.159475mm2 bounding footprint. These are provisional extraction estimates: the old-Magic compatibility discrepancy and absence of formal capacitor LVS remain documented. The parent library's existing model/symbol names are preserved. No OTA files are changed by this addition.
