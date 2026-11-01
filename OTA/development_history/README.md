# OTA development history

All OTA development studies available locally through 1 November 2026, arranged by development sequence. Numbering is a navigation aid, not an assertion that every entry is a distinct topology. Supporting models and rejected trials are included. Where exact creation dates are unavailable, relative order is stated explicitly.

## Start here

- [Current telescopic OTA / CMFB revision 2](../current_telescopic_cmfb_v2/): browseable schematic, symbol, GDS, models, benches, plots and verification records.
- [Latest verified two-stage candidate](20_two_stage_stability_recovery/): different topology and bias range; not interchangeable without checking the system.
- Existing `OTA/design_1` and `OTA/design_2` are preserved as previously published.

## Chronological index

| Order | Development date / sequence | Study | Status |
|---|---|---|---|
| 01 | Initial work, before 28 October | [Original seven-transistor two-stage OTA](01_original_two_stage/) | Historical voltage-bias baseline; characterization, schematic and original results. |
| 02 | Before 28 October | [Behavioral SC / OTA / SAR model](02_behavioral_system_model/) | Supporting system model; not a transistor-level PDK simulation. |
| 03 | 28 October | [Current-reference bias and channel-length sweep](03_current_reference_bias/) | Ideal current reference plus diode-connected mirror; length/current/compensation tradeoffs. |
| 04 | 28 October | [Independent stage and device-group tuning](04_independent_stage_tuning/) | Selected high-gain compromise plus faster and lower-power alternatives. |
| 05 | 28 October | [Extracted metal-capacitor compensation](05_extracted_metal_compensation/) | Parasitic and plate-orientation study; capacitor library itself remains in the existing capacitor directory. |
| 06 | After initial metal-cap study | [Further capacitor / OTA analysis](06_further_capacitor_analysis/) | Historical compensation exploration; inspect the included report and measurements. |
| 07 | Before MOS-only selection | [Capacitor layout / OTA parasitic comparison](07_capacitor_layout_optimization/) | Historical layout-capacitance tradeoffs; does not qualify precision SC capacitors. |
| 08 | Before MOS-only selection | [MOS capacitor and capacitance-multiplier feasibility](08_mos_capacitance_multiplier/) | Feasibility experiment, not a qualified active precision capacitor. |
| 09 | Before first physical OTA layout | [MOS-only compensation selection](09_mos_only_compensation/) | Six PMOS gate-capacitor units selected in the original schematic-level experiment. |
| 10 | Before compact layout v2 | [First MOS-compensated OTA physical layout](10_physical_layout_v1/) | Local DRC/LVS pass; historical initial layout. |
| 11 | Before 30 October retuning | [Compact symmetric layout and extraction](11_physical_layout_v2/) | Compact ABBA arrangement, local DRC/LVS and exploratory extraction. |
| 12 | After compact layout v2 | [Poly / metal parasitic attribution](12_parasitic_layer_attribution/) | Analysis of extracted capacitance by layer; not a new OTA topology. |
| 13 | 30 October | [Extracted MOS-compensation retuning](13_extracted_compensation_retuning/) | Capacitor-count and reference-current tradeoffs on the compact extracted model. |
| 14 | 30 October | [Current versus MOS-capacitor optimization](14_current_cap_optimization/) | Nine units / 3.5 uA balanced candidate under provisional screening limits. |
| 15 | 30 October development sequence | [Physical nine-unit MOS-capacitor revision](15_physical_layout_v3/) | Actual schematic and GDS update; corrected physical finger geometry. |
| 16 | 30 October | [SC integrator test with layout-v3 OTA](16_sc_integrator_validation/) | Assumed CS=2.5 pF, CF=7.5 pF, VREF=1.5 V; these are not the newly uploaded SCA values. |
| 17 | 31 October | [Series-resistor / MOS compensation study](17_series_resistor_compensation/) | Six units plus 16 kohm ideal resistor screening; later physically implemented separately. |
| 18 | 31 October, after resistor screening | [Native SCL08 RPP resistor validation](18_native_pdk_resistor/) | Native resistor, physical cell, symbol, topology image and validation. |
| 19 | 31 October | [Integrated OTA / RPP extraction and PVT](19_integrated_resistor_pvt/) | Six-unit / 16 kohm layout passes local DRC/LVS but fails the assumed full stability envelope. |
| 20 | 31 October | [Two-stage stability recovery](20_two_stage_stability_recovery/) | 12 MOS-cap units, 28 kohm RPP, widened output PMOS; minimum main-grid PM 62.22 degrees; slower settling. |
| 21 | 31 October | [Alternative OTA architecture comparison](21_architecture_comparison/) | Basic fully differential, telescopic, folded, gain-boosted telescopic and class-AB prototypes versus the two-stage baseline. |
| 22 | 31 October | [Telescopic / gain-boosted OTA SC comparison](22_telescopic_sc_comparison/) | Both candidates tested in the previously assumed SC circuit; gain boosting provides little sampled benefit in that benchmark. |
| 23 | 1 November, first telescopic layout | [First telescopic layout: extracted CMFB failure](23_first_telescopic_layout_failed/) | Historical failed candidate: local DRC/LVS pass, but resistor parasitics destabilize CMFB. Do not use as the current design. |
| 24 | 1 November, after extracted failure | [Telescopic OTA with corrected CMFB](24_telescopic_cmfb_revision_2/) | Current verified telescopic prototype: local DRC/LVS pass, 1442 successful AC checks, minimum CMFB PM 63.75 degrees. C-extraction only, not full signoff. |
| 25 | 1 November, after CMFB revision 2 | [MOS active-resistor feasibility](25_active_resistor_feasibility/) | Direct NMOS / complementary substitutions simulated; corner failures prevent replacing the verified poly network. No active-resistor layout. |

## Using the packages

Each numbered entry provides an original report, `project.zip`, and selected plot previews. Download the required ZIP files and extract all into one directory, preserving their paths. Extracting all packages reconstructs `ota_design_1/`, `ota_design_2/` and `architecture_exploration_20261031/` as neighboring folders. This preserves study dependencies without duplicating nested revisions in every package. Scripts may still contain historical absolute paths: configure local PDK includes before running. The standalone current prototype above is also available without ZIP extraction.

All available design sources, test decks, custom model wrappers, GDS/layout sources, scripts, CSV/JSON measurements, plots and DRC/LVS records are retained in their owning package. Dense `.dat`/`.raw` waveforms are omitted to avoid uploading gigabytes of regenerable sweep output. The [manifest](manifest.json) lists every included source file with SHA-256, package hashes and all omissions. Runtime environments, caches, dependency binaries and duplicate archives are excluded. Native proprietary PDK model cards are not included; local SCL08 installation is required.

## Interpret results correctly

Historical READMEs are snapshots. Statements such as "not yet simulated", "not pushed", or "no layout" apply to that study at that point; later entries record subsequent work. Rejected candidates remain available as evidence, with their failed status explicit. A DRC/LVS pass establishes local rule/connectivity checks, not analog performance or foundry signoff. Performance used adapted capacitance extraction; full interconnect/substrate RC and quantitative noise qualification remain unresolved. MOS compensation does not establish a precision SC/SAR capacitor replacement.

The newly uploaded `SCA/sc_diff_tb.sch` uses different assumptions (10 kHz, 40 pF feedback, 2.5 V reference, two behavioral amplifiers). The OTA SC tests archived here used the earlier assumed circuit; they have **not** validated the new SCA design. Its missing symbols and unexpected differential result still need resolution.

This publication packages existing results. No new circuit simulations or DRC/LVS checks are claimed by the upload.
