# Editable SCL08 capacitors: quick start

Use `scl08_cap2.sym` for a conventional two-pin appearance with substrate tied to SPICE ground internally. Use `scl08_cap3.sym` when substrate wiring must be explicit. Both include the same extracted substrate parasitics.

## Open and change a value

From this directory:

```bash
xschem --rcfile xschemrc examples/value_demo.sch
```

1. Select a capacitor and press **q**.
2. Set `value=2.5p`, `value=7.5p` or `value=3p`. These values are already prepared.
3. The symbol displays both Target and Extracted plate-to-plate capacitance.
4. Ctrl-click **Run simulation + plot** in the demo.
5. The matching GDS file is listed in CATALOG.md.

For a NEW value, such as `4p`, Ctrl-click **Save + generate layouts/models for edited values**, wait for completion, then netlist/simulate. This saves the schematic before scanning top-level capacitor instances. The button uses SCL08_CAP_PDK_ROOT; set SCL08_CAP_PDK_ROOT before launching xschem on another computer. Results and errors go to results/prepare_gui.log. GUI clicks have not been exercised in the headless environment; the same prepare backend was tested end to end.

The equivalent terminal command is:

```bash
python3 scripts/prepare.py --schematic "/path/to/your_circuit.sch" \
  --pdk-root "/path/to/scl_cp8d"
```

Or request a value directly:

```bash
python3 scripts/prepare.py --value 4p --pdk-root "/path/to/scl_cp8d"
```

`4p` is also included because this workflow was tested. A value without a prepared model produces an unknown-subcircuit simulation error; it never silently substitutes an ideal capacitor. New values require layout/model generation. This is a value-driven generator, not an automatically stretching foundry PCell.

## Bring it into Shreyas's project

Add this library's symbols directory to XSCHEM_LIBRARY_PATH, source scripts/symbol_helpers.tcl for the extracted-value display, and add an absolute-path SPICE include to models/generated_caps.lib.spice. Use the same library copy for simulation and layout. See README.md for the exact setup.

In the attached SC figure, the feedback capacitor's two signal terminals go to the OTA inverting-input summing node and OTA output. SUB goes to substrate ground, not VREF. The two-pin symbol already makes that substrate connection to SPICE 0. `examples/sc_feedback_fragment.sch` shows explicit wiring with 2.5p as an illustration; the 2.5/7.5 pF roles are NOT frozen.

If the 7.5 pF quantity is the physical external sensor, retain the sensor and its variation model. Do not replace the real pressure-dependent sensor with a fixed on-chip capacitor.

## Status

Prepared models/layouts are experimental. Old installed Magic 8.3.105 is below the PDK-required 8.3.579; native export omits one substrate capacitor, so explicit raw-.ext evaluation models are retained. They require reconciliation in a supported flow before fabrication. DRC/model/symbol checks passed; no formal capacitor LVS, matching, noise, voltage-rating or silicon qualification is claimed.
