# 11_physical_layout_v2: Compact symmetric layout and extraction

Development order: **11**. Date / ordering evidence: **Before 30 October retuning 2026**.

Compact ABBA arrangement, local DRC/LVS and exploratory extraction.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/physical_layout_v2/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA design_2: compact layout and exploratory parasitic extraction

This revision compacts the MOS-compensated OTA into four rows, preserves all schematic W/L totals, and arranges the input pair and PMOS mirror as symmetric ABBA unit sequences. Both pairs use equal-length identical unit devices. Each MOS-capacitor unit retains its isolated, tapped N-well tied to OUT. Main routes use orthogonal M1/M2, row-local buses and vertical net trunks.

## Physical verification

- KLayout 0.28.16, original local SCL CP8D DRC/LVS decks, unmodified.
- DRC: 0 markers.
- LVS: matches the independent resolved schematic reference, including six 20/10 um PMOS capacitor units.
- Negative controls: incorrect capacitor gate and incorrect output PMOS size each fail LVS.
- Import-adjusted C-extraction transistor topology matches the GDS through a separate KLayout LVS comparison.
- Contracting the extracted wire resistors also produces a transistor topology matching the GDS. This is a connectivity check, not validation of extracted R/C values.

| Geometry | Original layout v1 | Compact layout v2 |
|---|---:|---:|
| Bounding width (um) | 1090.8 | 364.1 |
| Bounding height (um) | 148.5 | 243.9 |
| Bounding area (mm2) | 0.16198 | 0.08880 |

Bounding-box area decreases about 45.2%. This includes routing and wells, not a complete guarded chip macro boundary. No claim of improved measured offset or mismatch is made: dummy devices, guard rings, contact-array optimization, routing symmetry and Monte Carlo validation remain open. Input and mirror placement now has a common geometric center within each ABBA sequence; routing parasitics are not perfectly balanced.

## Extraction finding and workaround

The unmodified Magic SCL import paints raw reversal/implant marker masks onto the same internal planes used by electrical wells/active geometry. In this test that destroys the OUT-connected well recognition: its native extracted capacitor bulk becomes VDD. That netlist is quarantined as invalid and is never used for the comparison simulations.

`scripts/extract.py` constructs a temporary, extraction-only technology copy and omits raw marker painting for nwell_rev, boron_rev, boron and CONT from the CIF input section. The original raw GDS masks still participate in all device/tap boolean derivations. Source PDK files are untouched, and DRC/LVS always use the original decks. No transistor bulk is manually rewritten in SPICE. The resulting native capacitor bulk is OUT and independent KLayout topology comparisons pass.

This import adaptation is an engineering workaround, not a foundry-qualified extraction deck. Six C-extraction warnings report tied source/drain capacitor devices with one terminal and reconnect the remainder to OUT. Independent topology comparison verifies the resulting device connections. The full resistor-network run additionally reports substrate-tile and missing-substrate-connection errors. Its output is retained and simulated as **diagnostic only**, despite matching after wire contraction. It must not be treated as validated full-RC PEX.

The technology has no qualified well/substrate junction extraction in this flow, and well resistance is disabled in its coefficients. Well junction capacitance/diode behavior and distributed substrate/well resistance remain absent. Model translation warnings from ngspice remain. These limits matter particularly for the capacitor's moving OUT-connected wells.

## Estimated parasitic reduction

Using the same import-adjusted extraction flow for both layouts, node ground-capacitance estimates are approximately:

| Node | Original v1 (fF) | Compact v2 (fF) |
|---|---:|---:|
| First-stage N2 | 458 | 216 |
| OUT | 468 | 221 |

These are extracted node-to-ground terms, not total effective loading or MOS compensation capacitance. Coupling terms are stored separately. The v2 C-only extraction reports N2 about 214.5 fF; the resistor extraction's .ext node accounting reports about 215.8 fF. Neither includes the missing well-junction contribution.

## Actual ngspice results

Conditions: 5 V, 27 C, ideal 2.5 uA reference, 5 pF explicit output load, follower bias 2.5 V. Thirty AC cases and ten transient cases were run across five model variants. Transient maximum step 2 ns; settling band is 0.1% of the applied step about actual final output, not total ideal accuracy.

| Model | Gain (dB) | UGF (MHz) | PM (degrees) | 100 mV settling (us) | 2 V settling (us) |
|---|---:|---:|---:|---:|---:|
| Original schematic | 88.77 | 1.199 | 70.80 | 0.603 | 2.349 |
| Drawn device geometry/junctions only | 89.61 | 1.111 | 68.12 | 0.687 | 2.331 |
| Compact layout + extracted C | 89.61 | 1.091 | 65.31 | 0.694 | 2.584 |
| Compact RC, diagnostic | 89.61 | 1.091 | 65.27 | 0.692 | 2.552 |
| Original layout RC, diagnostic | 89.90 | 1.173 | 64.74 | 0.818 | 2.521 |

The device-only row includes actual extracted source/drain area/perimeter and finger geometry. The original schematic omits these explicit junction dimensions, so the rows are not solely a comparison of wiring. Reduced estimated parasitics and area do not establish an overall speed improvement; large-step settling is not improved versus all variants.

For the compact capacitance-loaded model at 2.5 V bias, PM is 74.54 degrees with 1 pF and **56.39 degrees with 10 pF**. At 5 pF and 4 V bias, PM is only **39.58 degrees**. This revision does not satisfy a blanket 60-degree requirement across the load/bias envelope. Compensation/current retuning and a trustworthy well-aware extractor are next. No PVT, noise, mismatch, real current-generator, complete SC-loop or foundry signoff qualification has been completed.

## Files and use

- `layout/ota_design2_mos.gds`: authoritative verified editable GDS; open directly in KLayout. No verified native Magic layout is offered.
- `schematic/reference.cdl`: independent schematic reference; `ota_design2_mos.cdl` is its fingered equivalent.
- `verification/drc.lyrdb`, `lvs.lvsdb`, logs: primary local-deck verification.
- `verification/pex_topology.lvsdb`, `rc_topology.lvsdb`: extraction topology checks.
- `pex/ota_C_only.spice`: exploratory extracted capacitance model.
- `pex/ota_extracted.spice`: RC diagnostic model, substrate errors remain.
- `pex/*.ext`, `*.res.ext`, extraction logs and import_filter.json: extraction evidence.
- `baseline_v1/`: original verified GDS and same-flow diagnostic extraction for comparison.
- `simulations/`: runnable benches, native data, CSV measurements, summary.json and simulator logs. Includes point to their original staging paths; `scripts/analyze.py` regenerates benches with paths for its current project directory.
- `plots/layout_preview.png` and `extracted_comparison.png`, plus PDFs: layout and simulation figures.
- `scripts/`: generation, extraction, comparison and plotting scripts. Requires local SCL PDK, KLayout, ngspice, numpy/matplotlib, and Magic 8.3.688 currently at `/tmp/magic_cap_validate/bin/magic`. That temporary tool may need rebuilding; no global tool install was changed.

Reproduce: run `klayout -b -r scripts/generate.py`, `python3 scripts/verify.py`, then `python3 scripts/extract.py --cap-only` and `python3 scripts/extract.py`, `python3 scripts/prepare_pex.py`, and `python3 scripts/analyze.py`. Also regenerate the baseline using its extraction script if needed. PDK model/deck paths must exist locally. No proprietary PDK cards or rule files are redistributed in this folder.
