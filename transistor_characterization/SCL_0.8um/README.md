# SCL 0.8um CMOS Transistor Characterization

This directory contains preliminary Ngspice and Python work for characterizing NMOS and PMOS devices in the SCL CP8D 0.8um process. The objective is to generate repeatable plots and parameter tables that can support transistor sizing for a two-stage OTA.

## Directory structure

- `notebooks/` - Python notebooks for NMOS and PMOS analysis.
- `netlists/` - Simulation instructions and sweep scripts.
- `data/nmos/` - NMOS simulation data.
- `data/pmos/` - PMOS simulation data.
- `results/` - Generated figures and tables.
- `RESULTS_STATUS.md` - Current status and limitations of the results.

## Characterization scope

- NMOS transfer characteristics at fixed VDS.
- NMOS output characteristics at fixed VGS.
- PMOS transfer characteristics at fixed VSD.
- PMOS output characteristics at fixed VSG.
- Numerical estimates of gm, gm/ID, gds, ro, and intrinsic gain where supported by the data.

## Requirements

- Python 3
- JupyterLab or Jupyter Notebook
- NumPy, pandas, and Matplotlib
- Ngspice for regenerating simulation data
- Authorized local access to the SCL CP8D 0.8um model library

Install the Python dependencies:

```bash
python -m pip install numpy pandas matplotlib jupyterlab
```

## Workflow

1. Run the simulation sweeps using the supplied instructions and your locally installed SCL model library.
2. Place generated raw data in the appropriate `data/nmos/` or `data/pmos/` directory.
3. Run the corresponding notebook.
4. Save generated figures and CSV tables under `results/`.
5. Verify sweep ordering, units, derivative calculations, and bias-point pairing before using extracted parameters for circuit design.

## Important limitations

These results are preliminary. The current Ngspice version reports that some HSPICE-specific model parameters are ignored. This may affect model accuracy and extracted parameters. Validate model compatibility and numerical results before using them for OTA sizing.

Do not commit foundry model files or redistribute simulation data unless the applicable licence permits it.