# 01_original_two_stage: Original seven-transistor two-stage OTA

Development order: **1**. Date / ordering evidence: **Initial work, before 28 October 2026**.

Historical voltage-bias baseline; characterization, schematic and original results.

Download [project.zip](project.zip) and extract it into the same working directory as the other history packages. The archive preserves original project-relative paths under `ota_design_1/`, so neighboring studies and scripts can share their original dependencies. Dense `.dat` / `.raw` waveforms and tool environments are omitted; measurement tables, plots, simulation decks/logs, models and physical verification files are retained. See the parent manifest and README for scope.

---

## Original report (historical snapshot)

# OTA design 1 — SCL 0.8 um

All design work is stored inside this project directory.

- designs/: xschem transistor schematic and symbol, SPICE core, PDK include
- tb/: xschem follower testbench and SPICE AC/DC/transient/reference testbenches
- plots/: PNG and PDF simulation plots
- results/: generated netlist, logs, numerical data, and raw waveform
- scripts/: plotting code
- reference_tables/: copied characterization tables
- exports/: schematic SVG and shareable project archive
- DESIGN_REPORT.md: original design results and limitations

## Open in xschem

From this project directory:

```sh
xschem --rcfile xschemrc tb/ota_follower_tb.sch
xschem --rcfile xschemrc designs/ota_scl08.sch
```

The project xschemrc adds designs/ and tb/ to the symbol search path, and puts generated netlists in results/. Keep it with the project. It is portable across project locations, but the standard xschem library path may need changing on another installation.

## Run SPICE tests

```sh
cd tb
ngspice -b -o ../results/reference.log reference.cir
ngspice -b -o ../results/open_loop.log open_loop.cir
ngspice -b -o ../results/follower.log follower.cir
cd ..
python3 scripts/plot_results.py
```

SPICE testbenches must run with tb/ as the working directory. Their includes point to designs/ and their waveform outputs to results/. Logs should use the paths above. Plotting code finds the project root automatically.

## Use in a switched-capacitor circuit

Place designs/ota_scl08.sym using the project configuration. Connect inp, inn, out, vdd (5 V), vss (0 V), and external vbn (0.95 V above vss). The 5 pF Miller capacitor is internal. The demo output load is external. Copy the demo MODELS block to your top-level testbench. No separate ota7.inc include is needed when using the hierarchical xschem symbol.

The PDK remains at /home/berson_meshak/pdk/scl08/ngspice_models49/mos/tntp49_5v and is not bundled. On another machine update designs/models.inc and the MODELS block in tb/ota_follower_tb.sch. Generated netlists include local absolute paths and should be regenerated there.

## Verification after reorganization

All three SPICE tests were rerun in this layout. The xschem testbench was netlisted again and the generated netlist simulated: output_high=2.610739 V and output_low=2.511864 V, reproducing the original results. Plots were regenerated from these runs. HSPICE compatibility warnings and all limitations in DESIGN_REPORT.md still apply.

The original generated ota_scl08 workspace folder was removed only after these checks passed. Synced sources, existing user schematics, and PDK files were not changed.
