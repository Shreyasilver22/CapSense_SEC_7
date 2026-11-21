# Sensor capacitance sweep from 7 to 12 pF

This study uses the released differential 10 kHz SC circuit and final telescopic OTA with extracted capacitance. Each sensor branch is swept independently in 1 pF steps, giving 36 combinations. Nominal conditions are 5 V, 27 °C, typical SCL08 MOS and RPP models, 40 pF feedback capacitors, 5 pF load per output, and a 2.5 V output common-mode reference. The RX transfer starts 1 µs before TX discharge. The sample is at 80 µs into the fifth clock cycle. The CSV also includes the differential change from 80 to 88 µs.

Ideal charge balance gives Vdiff = 2(CP − CN)(VDD + VCM)/(2CF + CP + CN). Increasing both branch capacitors together increases their total and lowers the ideal input common-mode. Changing only one branch changes both the differential signal and its conversion factor.

The sensor-only noise estimate uses positive and negative charge perturbations after sampling and before transfer. The simulated voltage gains from each perturbation to the sample are weighted by independent kT/C variance. These results cover the two sensor capacitors. Total sampled noise also depends on OTA and reset noise, switching, and noise folding.

Run `python3 sweep.py` and `python3 plot.py` from this directory with the same dependencies as the parent validation. The fine timestep CSV uses 5 ns instead of the nominal 20 ns for the two largest differential signals and the largest total capacitance.

## Nominal findings

All 36 combinations completed. At the sample, output common-mode spans 2.49487 to 2.50015 V and input common-mode spans 0.78163 to 1.38292 V. The 12/7 pF and 7/12 pF pairs produce +756.379 mV and −755.513 mV, respectively. The maximum absolute deviation from ideal charge balance is 7.182 mV at 11/12 pF. The change in differential output between the 80 µs and 88 µs samples is under 0.22 µV across the grid.

For equal branches, the sampled differential output rises from 0.324 mV at 7/7 pF to 0.678 mV at 12/12 pF. During switching, the input common-mode drops below ground in 28 cases. The minimum is −0.552 V at 12/12 pF, where the output common-mode reaches 0.681 V before recovering. The results establish nominal recovery at the testbench's sampling instant. The 7–12 pF extension has no process, supply, temperature, physical clock driver, or ADC loading sweep.
