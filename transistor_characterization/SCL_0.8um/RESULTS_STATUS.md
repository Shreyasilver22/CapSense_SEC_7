# Results status

The notebooks are organized analysis templates based on the uploaded notebooks and the PMOS sweeps discussed in the project chat. Raw `.dat` files were not included in this package, so plots/tables are generated when the notebooks are run with the corresponding local simulation files.

Known caveats:
- Ngspice 42 reports ignored HSPICE-specific model parameters.
- Numerical derivatives need validation.
- Check each `wrdata` file's columns and sweep ordering before relying on derived values.
- Do not publish restricted PDK models or raw model-derived datasets without permission.
