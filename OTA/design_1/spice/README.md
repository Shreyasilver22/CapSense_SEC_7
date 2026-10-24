# SPICE files

`ota7.inc` is the seven-transistor OTA subcircuit authored for this design. `models.inc.example` documents the local foundry-model include.

The SCL CP8D model cards are not redistributed: no redistribution terms were established from the installed files. A user must obtain the PDK separately and run the model configuration script. Its output `models.inc` is ignored by Git. The root repository license must not be interpreted as licensing foundry files.

The tests expect MOS model names N and P from the nominal tntp49_5v deck. Ngspice accepts LEVEL49 as BSIM3, but ignores some HSPICE parameters, including PMOS capacitance entries. The original cards are not modified. Dynamic/noise predictions remain provisional until those differences are resolved or independently bounded.
