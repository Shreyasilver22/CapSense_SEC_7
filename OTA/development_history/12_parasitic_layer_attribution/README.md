# 12_parasitic_layer_attribution: Poly / metal parasitic attribution

Development order: **12**. Date / ordering evidence: **After compact layout v2 2026**.

Analysis of extracted capacitance by layer; not a new OTA topology.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/physical_layout_v2/layer_breakdown/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# Compact OTA parasitic attribution

The modeled routing capacitance is primarily metal, not polysilicon, in the current compact OTA. Poly nevertheless has substantially greater sheet resistance and is the intentional electrode of the MOS compensation capacitor.

## Measured extraction breakdown

| Node ground capacitance | Poly (fF) | Metal 1 (fF) | Metal 2 (fF) | Total (fF) |
|---|---:|---:|---:|---:|
| N2, sensitive first-stage node | 57.24 | 104.22 | 54.35 | 215.81 |
| OUT | 0 | 136.07 | 84.48 | 220.55 |

At N2, these shares are approximately 26.5%, 48.3% and 25.2%. At OUT, the model reports 61.7% M1 and 38.3% M2. This does not imply the physical output has no diffusion/well capacitance: junction effects are separate and well-junction extraction is missing.

N2-to-OUT routing coupling is additionally 10.82 fF: approximately 7.60 fF M2/M1, 2.37 fF M1/poly, 0.82 fF M1/active and 0.034 fF M2/poly. Coupling is stored once per node pair; its effect depends on the signals' relative motion. It must not be indiscriminately added to ground capacitance as effective loading. The intentional approximately 2.48 pF MOS compensation capacitance is supplied by the transistor model and is excluded from these routing terms.

## How it was checked

Nine extraction runs use the same verified v2 GDS, geometry and established extraction-only marker-import adaptation. One uses all capacitance rules; eight individually retain only a source category of capacitance coefficients, setting the other capacitance coefficients to zero in temporary private technology copies. Geometry and resistance coefficients do not change. Source PDK files are untouched and no proprietary cards/decks are copied into this result folder.

The sum of the eight isolated categories reproduces every reported baseline node-ground and coupling term within 0.0006 fF. This is linear coefficient attribution, not a field-solver validation. Both isolated and baseline extraction logs retain the known tied-source/drain capacitor warnings. The previous topology-LVS validation applies to the unchanged electrical geometry; no new physical layout revision was made.

Files: breakdown.csv/json contain all node and coupling terms; runs/ contains raw extraction evidence; plots/layer_breakdown.png/pdf is the comparison figure. scripts/analyze.py regenerates the experiments against the local physical_layout_v2 GDS. scripts/report.py makes the chart and nominal AC sensitivity experiments. Requires the local PDK, Magic 8.3.688 currently in /tmp/magic_cap_validate, ngspice and Python plotting packages. The temporary Magic tool may need rebuilding after cleanup.

## Gate resistance: estimate, not qualified R extraction

The local deck specifies poly sheet resistance 22 ohm/square, versus 0.05 ohm/square for M1 and 0.03 ohm/square for M2. For equal geometry, poly is approximately 440 times as resistive as M1. Contact and via resistances are separate.

For one compensation unit W=20 um and L=10 um, the poly path along the gate width is approximately 22*(20/10)=44 ohms from contacted edge to far edge. A uniformly loaded gate driven at one end has approximate low-frequency distributed gate resistance R/3, or 14.7 ohms/unit, about 2.44 ohms for six equivalent units in parallel. This simplified estimate excludes the gate extension, contact resistance and metal feed network. It is not a resistance extracted from the full layout. The broad output PMOS gates, each W=28 um/L=3.2 um, similarly give about 192.5 ohms far-end path per finger before extension/contact effects. Gate resistance deserves attention even when poly is not the largest routing-capacitance contributor.

## Nominal AC sensitivity simulations

Conditions: 5 V, 27 C, ideal 2.5 uA reference, 5 pF load and 2.5 V follower bias. Artificially removing a rule category is a sensitivity experiment, not a realizable layout change or predicted optimization result.

| Removed ground-capacitance category, across all nodes | UGF (MHz) | Phase margin (degrees) |
|---|---:|---:|
| None | 1.09134 | 65.31 |
| Poly | 1.09385 | 65.76 |
| Metal 1 | 1.09848 | 66.65 |
| Metal 2 | 1.09545 | 66.00 |

Even complete removal of poly ground capacitance gives a modest nominal change. Therefore focus next on shortening sensitive M1/M2 routes and unnecessary overlaps, while retaining short poly extensions and considering additional gate contacts/fingers. This does not resolve the known 10 pF and high-output-voltage phase-margin failures by itself.

## Limits

These are exploratory local-deck estimates. Intrinsic MOS capacitances and modeled diffusion junction capacitances are not included in the layer table; well/substrate junction capacitance and diode behavior remain unqualified. The full-RC extractor still reports substrate errors, so this report does not claim validated resistance-network PEX, a complete parasitic budget, PVT qualification or foundry signoff. Material rankings can change when missing well terms and actual SC loading are included.
