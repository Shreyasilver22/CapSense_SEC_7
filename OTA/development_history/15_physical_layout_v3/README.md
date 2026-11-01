# 15_physical_layout_v3: Physical nine-unit MOS-capacitor revision

Development order: **15**. Date / ordering evidence: **30 October development sequence 2026**.

Actual schematic and GDS update; corrected physical finger geometry.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/physical_layout_v3/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA design_2 — physical layout v3: nine MOS compensation units, 3.5 uA Iref

This revision implements the balanced current/capacitor study candidate in an actual updated schematic and GDS layout, then reruns local physical verification and exploratory parasitic extraction. All prior revisions remain separate.

## Changes and physical verification

- Native xschem schematic: nine parallel PMOS gate-capacitor units, each W/L=20/10 um; gate=N2, source/drain/body=OUT. Native testbench reference is an ideal 3.5 uA current source from VDD to IREF.
- Physical layout: nine isolated, OUT-tapped N-wells for compensation, ABBA input/mirror sequences and the existing four-row routing plan. Thirty-one physical MOS devices. Extent 462.5 x 243.9 um, bounding area 0.11280 mm2 (v2 was 0.08880 mm2 with six units). This is an initial analog macro, without completed dummy/guard-ring/current-density optimization.
- DRC: zero markers using the original, unmodified local SCL CP8D KLayout deck.
- LVS: matches both independent resolved and fingered schematic references. Deliberate gate and size errors fail LVS as expected.
- Native xschem core/testbench were netlisted; capacitor multiplicity and bias checked; native testbench actually simulated.
- C-extracted transistor topology matches GDS in a separate KLayout LVS run. Contracting extracted wire resistors also matches GDS. These tests validate topology, not numerical extraction coefficients.

The schematic now explicitly uses physical unit W and parallel multiplicities: M1/M2 3.75/2.4 um each m=2, M3/M4 5/3.2 um each m=2, M6 28/3.2 um m=4, M7 20/3.2 um m=8. M5/M8 remain 20/3.2 um m=1. Total W/L values match the original design, but BSIM narrow-width effects can differ between one wide transistor and many fingers. Earlier aggregate-width schematics were not electrically identical to the physical fingers in this model. The corrected fingered schematic and physical layout are now consistent in unit geometry. The primary C-extracted comparison already used the physical fingers.

## Simulation results

Supply 5 V, 27 C, ideal Iref 3.5 uA. Nominal: CL=5 pF, follower DC=2.5 V. Minimum PM covers all nine combinations of CL=1/5/10 pF and DC=1.5/2.5/3.5 V. Four model variants were checked across these nine points plus a 4 V stress point. Each variant had 100 mV and 2 V follower transients at all three loads. Final schematic results use the explicit physical finger geometry. A separate 1 ns repeat checks the new C model at 10 pF.

| Variant | Gain (dB) | Nominal UGF (MHz) | Nominal PM (deg) | Minimum PM (deg) | Nominal supply power (uW) | 2 V settling at 10 pF (us) |
|---|---:|---:|---:|---:|---:|---:|
| schematic | 87.57 | 0.947 | 73.41 | 65.77 | 176.84 | 2.703 |
| previous_sizing | 87.57 | 0.937 | 71.25 | 63.51 | 176.84 | 2.805 |
| new_C_extracted | 87.57 | 0.936 | 71.04 | 63.26 | 176.84 | 2.815 |
| new_RC_diagnostic | 87.58 | 0.936 | 70.99 | 63.21 | 176.52 | 2.791 |

New C-model large-step settling at maximum step 1 ns: 2.81221 us. The 5 ns result is approximately 2.8147 us; the difference is about 0.0025 us. Settling is worst rising/falling time into a 0.1% band about actual final output, not total ideal SC/ADC accuracy. The original prediction was 2.8048 us; the new geometry gives about 2.81 us, so it remains close to the sizing estimate. The extra array routing reduces minimum PM slightly, from 63.51 to 63.26 degrees.

At the separate 4 V DC stress point the new C-extracted model gives PM about 46.80 degrees. High-output-voltage operation remains unresolved and cannot be treated as meeting the 60-degree target. These are sparse nominal load/bias checks, not a continuous operating-envelope guarantee.

## Extraction status and tool rebuild

The prior temporary Magic binary had been cleared. Magic 8.3.688 was rebuilt from the pinned official source tag under /tmp/magic_ota_tool. Tk development headers were downloaded and unpacked under /tmp; no system packages or PDK sources were modified. Build settings: --with-interpreter=tcl --without-tk --without-x --without-opengl --without-cairo --disable-readline --disable-threads; generated build flags include the local Tk headers and -ltk8.6. Tool/source archive hashes are in verification/tool_build.json. The binary is temporary and may require rebuilding again after cleanup.

The same documented extraction-only marker-import filter is applied to prevent raw reversal/implant marker paint from overwriting electrical wells/active. No bulk connections are manually changed in SPICE. Original PDK files and physical DRC/LVS decks remain unmodified. The nine shorted-source/drain capacitor warnings remain in C extraction. The RC run emits substrate-tile and missing-substrate-connection errors: **RC results are diagnostic only**. Well-junction capacitance/diode behavior and distributed well/substrate networks are not qualified. The new extraction produces 124 wire resistors and 156 capacitor elements in its diagnostic RC output; this count does not establish completeness.

No claims of foundry signoff, reliable full-RC PEX, PVT/mismatch/noise qualification or SC-system settling are made. The reference generator itself is ideal. The next work is resolving well-aware extraction and testing the real SC timing/load, with the 4 V stability issue kept explicit.

## Files and opening

- designs/ota_mos_only.sch and .sym: updated native xschem cell; tb/ota_mos_only_tb.sch: updated native testbench. Start xschem from this project root to load xschemrc.
- layout/ota_design2_mos.gds: authoritative editable layout; open directly in KLayout. No native Magic layout is represented as a verified equivalent.
- schematic/reference.cdl, fingered_reference.cdl: independent reference views; schematic/ota_design2_mos.cdl: physical instance list.
- verification/drc.lyrdb, lvs.lvsdb, fingered.lvsdb, C_topology.lvsdb and RC_topology.lvsdb plus text logs: verification evidence.
- verification/final_summary.json: consolidated results. verification/prior_simulation_summary.json retains the earlier aggregate-width schematic simulation for audit; its schematic row is superseded by the fingered schematic.
- pex/ota_C_only.spice: new exploratory C model; pex/ota_extracted.spice: new diagnostic RC model. pex/import_filter.json and logs document the adaptation and errors.
- simulations/: actual native simulation decks, data, logs, CSV and summary.json. Raw decks reference staging paths; regenerate with scripts/analyze.py after moving.
- tb/extracted_large_10p.cir: portable relative-include C-extracted large-step testbench. Run from tb using ngspice -b extracted_large_10p.cir.
- plots/layout_preview.png/pdf and new_extraction.png/pdf: actual GDS preview and comparison plots.
- scripts/: generation, checking, extraction and analysis. Reproduce generation/DRC/LVS with KLayout generate.py and Python verify.py; extract.py --cap-only then extract.py uses local PDK and temporary Magic; prepare_pex.py and check_extraction.py validate connectivity. analyze.py regenerates simulations. Fine timestep deck is stored separately. Proprietary transistor model/deck files are referenced locally, not copied.
