# SCL08 capacitor layout optimization experiment

28 October 2026. Standalone layout-optimization experiment alongside the original capacitor library; no OTA implementation is included. Nine physical layouts compare baseline tiled, compact tiled and slotted-overlap geometries near 3/4/8 pF. Models are experimental raw-Magic-extraction estimates, not qualified silicon capacitances.

Start with RESULTS.md and plots/layout_comparison.png. Layouts are standalone GDS files in layouts/. All nine models are in models/cap_layouts.lib.spice. The 4p slotted candidate is capopt_slotted_4p, actual extracted mutual C about 3.99574 pF.

## What changed in layout

- Baseline: 20 x 20 um overlap tiles at 40 x 28 um pitch, 4 um buses, separate side extensions; reproduces earlier extracted values.
- Compact: 20 x 20 um tiles at 32 x 23 um pitch, shorter extensions and 3 um buses. This reduces routing footprint but narrower buses can increase route resistance.
- Slotted: corresponding 20 um wide metal strips separated by 2 um slots. Each metal layer has its own 3 um side spine connecting the strips; M1 spine is on the left, M2 spine on the right. Both strip networks remain electrically independent. There are NO vias between plates and NO added grounded shield. The lower signal plate covers most of the upper plate's substrate-facing area in this extraction model.

For the approximately 4 pF comparison, baseline versus slotted: TOP-to-substrate 2.44696 -> 0.615322 pF; BOT-to-substrate 7.32176 -> 4.80970 pF; footprint 0.394368 -> 0.159475 mm2. This is about 75%/34%/60% lower respectively. Useful capacitance is nearly identical, 3.99578 versus 3.99574 pF. The nominal 4p token is a convenient name, not an exact 4 pF or a manufacturing tolerance guarantee. target_F in config is the corresponding baseline extracted reference. All layout variants are within 0.13% of those references.

## Checks and model limits

Actual checks performed:

- Each metal network is one connected region; no plate-shorting via layers are drawn.
- Minimum metal widths and internal notch spacing checked geometrically.
- A conservative 25 um square erosion check rejects solid regions wider than 25 um in both axes; narrow strips/slots pass. This is a project check supplementing the deck, not a foundry interpretation/sign-off.
- Supplied KLayout DRC deck run on each GDS: zero reported markers.
- Plate-transfer current and BOTH substrate-current paths checked in ngspice for every model.
- Two-pin and three-pin style/value symbols netlisted and simulated in xschem/ngspice.

The supplied deck uses isolated spacing checks, so the explicit notch check is useful for connected slotted polygons. Other manual rules, mask grid/density/slot acceptance, final-chip connections, substrate contacts and via/contact necking need review in the actual fabrication flow. No contacts, vias, guard rings or substrate taps are included in these capacitor-only cells. A DRC pass alone does not establish their acceptance as capacitor devices. The stock LVS device deck has no dedicated capacitor recognition; no formal capacitor LVS pass is claimed.

Installed Magic remains 8.3.105, below the technology header's 8.3.579 requirement. Native export loses a substrate capacitance present in raw .ext; project-authored evaluation models preserve documented node-to-substrate and explicit coupling records. This discrepancy is unresolved. The same deck was used consistently for comparisons, but complex slot/fringe/shielding effects need confirmation with a supported/reconciled extractor and preferably an independent suitable field-solver/characterization flow. These predicted improvements are NOT evidence of measured physical performance.

No conductor-resistance PEX, dielectric loss/leakage, voltage coefficients/ratings, PVT, mismatch or statistical matching models are included. The resistance column in RESULTS.md is only a route-length/width and sheet-resistance proxy; it excludes distributed plate effects, vias and contacts and is not used by the OTA simulation. No noise or bandwidth accuracy claim follows from testing a frequency-independent lumped capacitor model.

## Reuse in xschem

From this folder:

```bash
xschem --rcfile xschemrc examples/layout_comparison.sch
```

Select a capacitor and press q. Prepared properties:

- style=baseline, compact, or slotted
- value=3p, 4p, or 8p

The symbol displays requested and extracted mutual capacitance. capopt3.sym has TOP/BOT/SUB; capopt2.sym internally grounds SUB to SPICE 0. Both retain the same plate-to-substrate parasitics. Unprepared style/value combinations do not fall back to an ideal capacitor; their model name is deliberately unresolved. This is an experiment with nine generated variants, not an arbitrary-value foundry PCell.

Add symbols/ to another project's XSCHEM_LIBRARY_PATH, source scripts/symbol_helpers.tcl in its own xschemrc, and include the absolute path to models/cap_layouts.lib.spice. Source the helper after choosing a library copy so model/display lookup uses that same version. GUI clicks were not tested headlessly, but native netlisting/simulation were.

Plain SPICE:

```spice
.include "/path/to/layout_optimization_v1/models/cap_layouts.lib.spice"
XCFB sensitive_node driven_node substrate_ground capopt_slotted_4p
* Two-pin convenience alternative, if substrate is SPICE 0:
* XCFB sensitive_node driven_node capopt_slotted_4p_gnd
```

Use one instance, not both. TOP is Metal 2; BOT is Metal 1. SUB is the substrate reference, not a third metal plate or an added external chip pin. Do not tie substrate to signal common mode simply because that node is VREF. TOP on the sensitive node is the starting orientation supported by the OTA tests; other circuits and plate orientations need their own checks.

## Layout reuse and generation

Import layouts/capopt_slotted_4p.gds (cell capopt_slotted_4p) or another named variant into KLayout. The slotted 4p cell measures 404.76 x 394 um. Active plate strips are 20 um wide with 2 um gaps and separate 3 um spines. Geometry is drawn on a 1 nm GDS database grid, with actual slotted dimensions rounded to 0.01 um; the final mask grid must be confirmed before fabrication. Metal layers are 8/0 and 10/0; pin text layers 8/7 and 10/7. Additional surrounding/connecting metal changes the model, so extract again in the final floorplan.

Rebuild using an authorized local PDK (no foundry files bundled):

```bash
python3 scripts/extract.py --pdk-root /path/to/scl_cp8d
python3 scripts/assets.py
python3 scripts/verify.py
python3 scripts/report.py
```

Requirements: Python 3 with NumPy/Matplotlib; KLayout with embedded pya; Magic, ngspice and xschem. generate.py is run inside KLayout by extract.py, not with plain python. config.json holds comparison targets, baseline unit counts and strip row counts. Slotted length is seeded from the local overlap/edge coefficient estimate and rounded; extraction determines the actual value. Unsupported geometry or disconnected networks fail checks. Adding values requires extending config and verifying rules/models; old per-unit CDAC floorplans are not automatically replaced.

Project-authored code/layouts/symbols are reusable under LICENSE; that does not relicense foundry data or derived-model rights. No foundry rule/technology/model decks are redistributed.

## OTA application comparison

A separate local OTA experiment evaluated these frozen models; the optimized-capacitor OTA update is not part of this capacitor-only publication. The unchanged tuned OTA with the slotted 4p model gives about 742 kHz UGF, 69.23-degree nominal PM and 63.09-degree minimum checked PM, with a 2 V step settling in about 3.67 us. The previous baseline 8p implementation was ~364 kHz/65.79 degrees/7.82 us. Those are nominal model-based comparisons, not physical/PVT results. Changing from baseline 8p to slotted 4p changes BOTH geometry and compensation value. RESULTS.md provides the fair same-capacitance layout comparison separately.

The 3p slotted candidate still misses the >=60-degree working margin screen at the worst tested point (~58.71 degrees), so 4p was selected among tested values. No global minimum required C or optimum is claimed. For SC/SAR ratio matching, these large continuous strip capacitors are not common-centroid/dummy matched-unit arrays; further matching/layout design is required. This publication preserves the original capacitor library and does not change OTA/design_2.

## Repository quick start

From the repository root:

```bash
cd capacitor/layout_optimization_v1
xschem --rcfile xschemrc examples/layout_comparison.sch
```

Choose style=slotted and value=4p for the highlighted candidate. The three-pin model is capopt_slotted_4p (TOP BOT SUB); the two-pin wrapper is capopt_slotted_4p_gnd (TOP BOT, substrate tied internally to SPICE 0). Prepared style/value combinations are baseline/compact/slotted x 3p/4p/8p. Full GDS layouts are in layouts/. The original value-driven library in the parent capacitor directory remains available separately; its original symbol/model names are not silently redirected.
