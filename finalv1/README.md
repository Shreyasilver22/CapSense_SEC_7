# CapSense finalv1

Selected GDS: `layout/CapSense_ASIC_ROUTED.gds`.
Main functional schematic: `schematic/capsense_current_tb.sch`.
Controller hierarchy: `schematic/controller/`.
RTL: `rtl/capsense_phase_gen.v`.

## Verified

Selected whole-chip SCL DRC: zero violations. LVS: match. Supplemental core via-overlap checks: pass. Original analog topology retained; digital mapping formally equivalent to RTL (21 checks proven). Native transistor counter load tests passed nominal, 4.5 V/85 C slow, and 5.5 V/-20 C fast cases, with all seven outputs correct. These load tests exclude routing RC and complete analog dynamics.

## Important scope

This is an engineering handoff, NOT tapeout signoff. The functional Xschem bench retains its previously validated digital model; the selected GDS uses a newer formally equivalent mapping. `models/selected_gds_counter.cdl` and `layout/chip_reference.cdl` are the exact selected-layout electrical references. The schematic is not a full-chip extracted/pad-level simulation bench.

## Remaining

Settled pre/post sensitivity and reset recovery; full analog PVT and sampled noise; complete pad/ESD and routing-RC qualification; loaded routed clocks and combined dynamic supply verification; CM_X reliability; final silicon-ID/top-name and submission checks. Local model audits found ignored HSPICE parameters, including pad capacitance. Do not treat earlier startup results as settled sensitivity or switching ripple as device noise.

## Opening and dependencies

Open the main schematic from its `schematic/` directory using your SCL-configured Xschem environment. Internal project references were made relative. Installed Xschem symbols and SCL PDK/model paths remain external dependencies and must be configured for the collaborator's machine. The installed PDK is not bundled. No clean-machine Xschem/netlisting validation of this handoff has been performed.

See `verification/` for recorded evidence. Keep source schematics and RTL unchanged while developing isolated copies. Do not publish third-party SCL models/library material until their redistribution terms are checked; bundled model files require your review before pushing.
