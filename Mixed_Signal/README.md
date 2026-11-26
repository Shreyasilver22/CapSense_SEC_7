# CapSense mixed-signal readout

SCL CP8D 0.8 µm capacitive-sensor readout: switched-capacitor network, user-designed transmission gates, telescopic OTA/CMFB, and the Verilog MOD-100 phase generator. This folder adds the mixed-signal development work without replacing the repository's earlier analog designs.

## Start here

- `Phase_Generator_Testbench/rtl/capsense_phase_gen.v`: unchanged RTL.
- `Phase_Generator_Testbench/schematic/phase_generator_tb.sch`: standalone clock-generator bench.
- `Integrated_Design/schematic/capsense_integrated_tb.sch`: integrated bench with ideal CS and PMOS CFB.
- `Integrated_Design/schematic/capsense_integrated_pmos_cs_tb.sch`: separate variant with PMOS CS and CFB.
- `Integrated_Design/schematic/capsense_cfb_40pf.sch`, `50pf.sch`, `60pf.sch`: feedback-size comparisons (full filenames use the `capsense_cfb_` prefix).
- `Integrated_Design/scripts/`: pressure/sensor experiment scripts.
- `Integrated_Design/cfb_sweep/`: archived 1,587-case measurements, plots and analysis sources.

The schematics and symbols are source files you can edit in Xschem. Select the visible **CAP_VALUES** block and press **Q** to change CP/CN, CS or PMOS W/L/M. In the PMOS-CS version use CS_W, CS_L and CS_M. Five parallel W=20 µm devices with L=50.675 µm target approximately 10 pF; capacitance depends on bias. The root project files are archival sources; configure an ignored working copy before running.

## Local setup

Requires Linux, Python 3, Xschem, ngspice with XSPICE/d_cosim, an Icarus runtime supporting libvvp, and a separately installed SCL CP8D PDK. The original machine used ngspice 45.2 and system Icarus 12.0 plus the pinned project-private runtime described below. Installed tool versions alone do not prove that co-simulation is functional.

From this `Mixed_Signal` directory:

```bash
python3 configure_local.py --pdk-root /your/path/to/open_pdks/scl_cp8d
```

This creates `work/Phase_Generator_Testbench/` and `work/Integrated_Design/`, replaces original absolute paths there, and gives co-simulation unique temporary aliases. It leaves tracked source files and the installed PDK unchanged. If a saved schematic omitted a shared CS/CFB default, the helper inserts it into that schematic's visible CAP_VALUES block and records it in ignored `local_setup.json`.

If you already have the verified private runtime, supply its directory with `--runtime /path/to/Phase_Generator_Testbench/runtime`. On the original workstation that path is `/home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench/runtime`.

Otherwise obtain and build Icarus locally:

```bash
cd work/Phase_Generator_Testbench
mkdir -p runtime-src
git clone https://github.com/steveicarus/iverilog.git runtime-src/iverilog
git -C runtime-src/iverilog checkout 24acba16baba765484df7b3f29c8fa931c10e6ec
sh build_local_runtime.sh
sh build_adapter.sh
python3 run_testbench.py
```

Build prerequisites: a C/C++ compiler, make, autoconf, gperf, bison and flex. `build_adapter.sh` also needs ngspice headers including `ngspice/cosim.h` matching the installed simulator. It defaults to `/usr/share/ngspice/scripts/src`; set `NGSPICE_HEADERS` to the appropriate include root if different. The small ngspice adapter sources and their license are retained under `adapter/`; complete downloaded tool source trees and compiled binaries are excluded.

After the standalone bench passes:

```bash
cd ../Integrated_Design
./open_xschem.sh
```

Open the PMOS-CS schematic separately from Xschem if desired. Regenerate the netlist after changing values. The main bench can also run with `python3 run_simulation.py`. Open the configured files under `work/`, rather than the archived originals. Historical reference schematics may retain dependencies from earlier analog projects; the primary entry points are the standalone bench and the five `capsense_*` benches listed above.

For plotting/analysis, install `requirements.txt` in your own Python environment. No Python environment or package installation is bundled. The archived sweep uses its frozen circuit snapshot and recorded RTL phase sequence; editing a current schematic does not change the archived study.

## What has been verified

- Standalone original RTL and live ngspice–Icarus co-simulation: all seven outputs, actual RTL port ordering, 0/5 V simulation interface. Original-machine reports are under `Phase_Generator_Testbench/reports/`.
- The integrated analog switches use the user's NMOS W=2.5 µm / PMOS W=4.5 µm, L=0.8 µm TG geometry.
- The completed CFB study covers CP and CN independently from 1 to 12 pF in 0.5 pF steps, for CFB labels 40/50/60 pF: 1,587 cases. All completed and met a 1 mV cycle-to-cycle drift criterion; this is not an absolute accuracy bound.
- Near CP=CN=10 pF, CP sensitivity at fixed CN was 46.74/37.41/31.17 mV/pF for CFB 40/50/60 pF.
- The later PMOS-CS variant was netlisted and its PMOS C–V was checked. The full AFE transient and sensitivity grid have NOT been rerun for that variant. Archived grid results use ideal CS, not the new PMOS CS.

Reports describe historical runs on the original workstation. A relocated checkout must be tested locally; archived PASS reports are not new-machine test results.

## Known limitations

Simulation ADC/DAC bridges connect RTL logic to electrical nodes; they are not physical converter blocks in the ASIC. The visible bench retains live RTL co-simulation. The archived large sweep replays recorded original RTL phases, compared against live runs in selected pilots. PMOS capacitors are nonlinear. Low sensor capacitances show premature charge loss when internal nodes boost above the supply. Behavioral input-CM sensing and ideal supplies/interfaces remain. This is a nominal prelayout study, not a complete transistor-level ASIC signoff.

## What is intentionally excluded

PDK installations/model cards/cell libraries, multi-gigabyte per-case waveforms, compiled runtimes, downloaded third-party source trees, caches and superseded backups. The selected measurement dataset and summary plots are kept for review and regeneration. All original local files remain available on the workstation. See `SOURCE_MANIFEST.json` for source snapshot hashes and `THIRD_PARTY_NOTICES.txt` for dependencies and upstream notices.

## Packaging check (26 November 2026)

The configured working copy generated netlists for all six primary schematics. The standalone bench also passed a fresh 305 µs live co-simulation check for all seven outputs using the existing original-workstation private runtime. A fresh runtime rebuild and relocated full AFE transient were not run. See `PORTABILITY_CHECK.json`.
