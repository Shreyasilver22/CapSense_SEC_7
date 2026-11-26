# CapSense integrated AFE bench

## Editing capacitor values in Xschem

Open `schematic/capsense_integrated_tb.sch` (or a 40/50/60 pF variant). Select the visible **CAP_VALUES** block beside the analog circuit, press **Q**, edit the `.param` values, and save. CS controls both CSP and CSN. CP and CN control the sensor capacitors. CFB_W, CFB_L and CFB_M control both PMOS feedback banks. Values use SPICE units: `10p`, `20u`, `202.7u`.

You can also select CSP/CSN and press Q to replace `value={CS}` with a literal value, or select MCFP/MCFN and edit W, L and M directly. Keep both branches matched for a symmetric design. The feedback symbol now shows the PMOS connection and emits the MOS card directly; there is no hidden capacitor subcircuit to edit. Source, drain and body remain tied to the summing node, and the gate to the output.

After changing values, regenerate the netlist with Xschem's Netlist button, then run the simulation as usual. An already-open ngspice session retains its previous circuit until the regenerated netlist is loaded or the simulator is restarted. These are design/simulation settings, not silicon-programmable capacitor banks.

Current defaults preserve the completed sweep geometry. All four schematics were netlisted, and a small-signal check confirms the direct PMOS cards match the previous devices at the default dimensions. See `simulation/cap_controls_check/verification.json` and `electrical_equivalence.json`. This check does not repeat the full AFE sweep.

The completed study under `cfb_sweep/` is an archived dataset. Its replay script reads its frozen circuit snapshot; later schematic edits do not change those old results. Use the current Xschem schematic for new component values.

Open `./open_xschem.sh`, or open `schematic/capsense_integrated_tb.sch`. Run `python3 run_simulation.py` to compile the original RTL with the verified private Icarus compiler, regenerate the netlist and run ngspice. Standard Xschem symbols and the installed SCL models remain external dependencies. Root configuration and PDK files were not edited.

## Earlier integrated-bench verification

`simulation/verification_final/host_final.log`: 795 us, completed without simulation errors before the current feedback-capacitor grid study. This earlier run does not verify every new capacitor/sensor combination. `verification.json` checks full duration, finite saved signals and all seven output rails. All phase/complement/sample_valid outputs span 0–5 V. Requested TX/RX, OTA input/output, common-mode and differential data are saved as exp1_*.dat. integrated.raw contains complete saved vectors. No graphs were generated. This confirms simulation execution, not analog accuracy or fabrication readiness.

## Circuit changes

The twelve SC-network switches now use your Transmission_v1_26 TG, not the previous reconstructed 10u/20u model. Original source: /home/shreyas/Desktop/Sec_7/designs/tg/Transmission_v1_26.sch. Its copied schematic/symbol are under symbols/. MOS sizes are NMOS 2.5u, PMOS 4.5u, L=.8u. `simulation/user_tg.spice` preserves the original transistor connections, W/L and evaluates its PDK nf=1 area/perimeter/resistance expressions numerically; the source PDK templates otherwise emitted unresolved @nf/@W expressions.

Five ideal input-CM correction switches are replaced with the same TG plus a 2-transistor complement inverter. This changes their effective on-resistance relative to the old ideal 10/3000/100000-ohm switch models; the CM loop must therefore be revalidated. Behavioral sensing/integration sources remain as in the existing input-CM correction design. It is not yet a wholly transistor-level ASIC implementation.

The Verilog MOD-100 phase generator uses the repaired project-private runtime under Phase_Generator_Testbench. Its six phase outputs drive only the intended TG control nets, with all seven outputs preserved. Explicit clock/reset voltage sources feed digital simulation bridges. These bridges are simulation interfaces, not physical ASIC cells. The private runtime aliases under /tmp are recreated automatically by the schematic control block before every run, including after reboot.

The external sample/hold/ADC fixture and its legacy auxiliary clock instance have been removed from this AFE-only bench. Original fixture text is archived in simulation/removed_external_adc_fixture.spice.txt, and all pre-edit project files are backed up under before_tg_counter_update/. Therefore the external loading differs from the earlier full ADC-load fixture. Explicit CLP/CLN=5p loads, OTA/CMFB, bias circuit, sensor configuration CP=11.79p/CN=10p and series sampling capacitors remain. Unused clock definitions remain in clock.spice, but no legacy clock instance drives the AFE.

## Numerical assumptions and next verification

The successful bench uses KLU, first-order Gear, xtrtol=2 and 80 ns maximum step. Phase DAC ramps are 1 us at 0–5 V. These are simulation settings, not implemented clock buffers. A timestep/integration-order accuracy check and actual transistor-level digital driver loading remain necessary before sensitivity/signoff claims. Counter synthesis work is separate; this bench runs behavioral RTL via Icarus.

No original RTL, external source schematic, original TG design, system tool or PDK was modified. Use this project opener so Xschem writes netlists to simulation/ and picks up the local .spiceinit. Paths target the requested installed project directory.

## Visible TG hierarchy correction

All twelve SC switches are now explicit six-pin Transmission_v1_26_h/v hierarchical symbols, not switch-blade primitive wrappers. Descending opens copied transistor schematics containing your original NMOS and PMOS. The h/v variants only change pin placement on the top-level drawing. Each pin connection and transistor parameter matches the electrically tested model; see simulation/hierarchical_tg_verification.txt. Original TG sources remain unchanged.

## PMOS feedback-capacitor sweep

The feedback capacitors use five parallel PMOS fingers, each W = 20 µm. Only L changes:

| Nominal CFB | L per finger | Total gate area |
| --- | --- | --- |
| 40 pF | 202.7 µm | 20,270 µm² |
| 50 pF | 253.375 µm | 25,337.5 µm² |
| 60 pF | 304.05 µm | 30,405 µm² |

Open `schematic/capsense_cfb_40pf.sch`, `capsense_cfb_50pf.sch` or `capsense_cfb_60pf.sch`. CP, CN, CS and the feedback dimensions are parameters in CAP_VALUES. The 40 pF nominal bench defaults to 795 µs; the 50/60 pF benches default to 1595 µs via SIM_STOP. Low sensor-capacitance cases may need more cycles; the batch checks this separately.

`cfb_sweep/progress.json` tracks the 23 × 23 × 3 study: CP and CN each range from 1 to 12 pF in 0.5 pF steps. `cfb_sweep/FINISHED.json` exists only after all 1,587 cases have been processed and analysis has completed. See `cfb_sweep/study_notes.txt` for geometry, measurement definitions, phase replay/live comparisons and convergence criteria. The batch replays recorded outputs of the original RTL to reduce simulation time; the Xschem variants retain live co-simulation.

The reported sensitivities are in mV/pF. Pressure sensitivity requires the sensor's capacitance-versus-pressure calibration. Numerical completion and small cycle-to-cycle drift do not prove useful sensitivity: selected low-capacitance cases exhibit premature sensor charging through the TG model when internal nodes rise above the 5 V supply. Those results are retained in the study.

## Completed sweep results

All 1,587 combinations completed: 529 per feedback-capacitor geometry, no failed or drift-flagged cases. Maximum final-cycle change was 0.9785 mV under the 1 mV drift criterion. This is a numerical criterion, not an absolute accuracy guarantee. Final grid completeness, finite values, original RTL equality and model hashes are checked in `cfb_sweep/final_verification.json`.

At CP = CN = 10 pF, partial sensitivity to CP with CN fixed is 46.7434, 37.4052 and 31.1701 mV/pF for nominal CFB = 40, 50 and 60 pF. Input and output common modes are near 2.5 V. Use `cfb_sweep/measurements.dat` or `measurements.json` for all requested voltages and derivatives, `feedback_comparison.png` for comparison curves, and `cfb_40/50/60_measurements.png` for the six measurement maps. Details and limitations are in `cfb_sweep/RESULTS.txt` and `study_notes.txt`.

The low-capacitance response collapse remains a design issue. Selected internal-node and TG-off tests show charge loss when boosted nodes exceed the supply. All cases are retained; completion does not establish useful sensitivity over the entire 1–12 pF range.
