# 10_physical_layout_v1: First MOS-compensated OTA physical layout

Development order: **10**. Date / ordering evidence: **Before compact layout v2 2026**.

Local DRC/LVS pass; historical initial layout.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_2/mos_only_compensation/physical_layout_v1/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA design_2 — MOS-only compensation: initial physical layout

This is a routed first-pass SCL08 layout of the existing tuned OTA with six parallel PMOS capacitor units. It was actually checked with the locally supplied, unmodified SCL KLayout DRC and LVS decks using KLayout 0.28.16.

- DRC: **0 reported markers**.
- LVS: **netlists match** against `schematic/reference.cdl`, independently resolved from the simulated OTA parameters.
- Negative controls: changing the capacitor gate to VDD, or changing the output PMOS width from 112 to 100 um, each produces an LVS mismatch.

These results establish local-deck geometry and connectivity checks, not foundry signoff or post-layout analog performance.

## Files

- `layout/ota_design2_mos.gds`: primary verified layout, top cell `ota_design2_mos`.
- `verification/magic_import_diagnostic/`: **unverified diagnostic conversion only; do not use as the verified layout**. Magic 8.3.688 import/re-export altered well/implant polygons (see magic_roundtrip.json). The authoritative deliverable is the original GDS opened directly in KLayout.
- `schematic/reference.cdl`: authoritative resolved six-port schematic reference.
- `schematic/ota_design2_mos.cdl`: explicitly fingered equivalent reference.
- `verification/drc.lyrdb`, `lvs.lvsdb`: open in KLayout's marker/LVS browsers.
- `verification/extracted.cir`: connectivity/device extraction from the GDS. Its pin order is printed in its SUBCKT line; do not assume it matches the original schematic order.
- `verification/summary.json`, logs and negative-control reports: evidence of checks.
- `plots/layout_preview.png` / `.pdf`: views generated from actual GDS geometry.
- `scripts/generate.py`, `verify.py`: reproduce the GDS and verification. Run `klayout -b -r scripts/generate.py`, then `python3 scripts/verify.py` from this directory. Local PDK paths are recorded in verify.py; proprietary rule files are referenced, not copied.

## Implemented devices and connections

M1/M2: W/L=7.5/2.4 um. M3/M4: 10/3.2 um. M5/M8: 20/3.2 um. M6: eight parallel 14/3.2 um fingers, total W=112 um. M7: eight parallel 20/3.2 um fingers, total W=160 um. MCAP: six parallel PMOS devices, each W/L=20/10 um (total W=120 um). Thus the layout contains 28 physical MOS devices, reduced to nine equivalent device groups by extraction.

MCAP gate connects to first-stage node N2; source/drain/body connect to OUT. Each capacitor unit has an isolated N-well with an explicit N+ well tap connected to OUT. The other PMOS wells connect to VDD. NMOS devices have explicit substrate taps to VSS. N-well reversal geometry follows the supplied DRC deck. Only six external GDS labels are used: INP, INN, OUT, VDD, VSS, IREF. Internal routes are not exported as extra labeled ports.

## Physical limitations and next design steps

This first layout uses a simple single-row floorplan and orthogonal two-metal routing. Extent is approximately 1090.8 x 148.5 um, bounding-box area 0.1620 mm2. This is a connectivity demonstrator, not an area-optimized or precision-matched analog floorplan. The differential pair/current mirrors are not common-centroid arrays; no dummy-device or guard-ring optimization has been performed. Contact arrays and current-density/electromigration checks also remain to be developed.

The earlier 2.48 pF capacitance, 1.20 MHz bandwidth and 70.8-degree phase margin are **schematic-model results**, not measurements of this layout. Routing and the OUT-connected wells introduce parasitic capacitance/resistance. No RC extraction, post-layout stability/settling simulation, PVT, mismatch, antenna/reliability or foundry signoff was completed here. In particular, do not assume this deliberately spread-out routing preserves the schematic bandwidth. The MOS-only design's high-output-voltage stability limitation remains.

The available Magic technology has an empty DRC section; Magic DRC is therefore not presented as verification. The local `netgen` executable is a mesh generator, so LVS was performed with the supplied KLayout LVS deck. The deck's native MOS W/L comparison tolerance is 3%; neither tolerance nor any rule was relaxed for this layout.

## Magic interoperability finding

The tested Magic import/re-export does not preserve all original well/implant masks: XOR areas differ on GDS layers 1, 5 and 6. This is why the native Magic file is quarantined with diagnostic results, not offered as a verified equivalent. DRC/LVS PASS applies to `layout/ota_design2_mos.gds` only. No claim is made that the diagnostic Magic conversion passes. The GDS remains editable directly in KLayout.
