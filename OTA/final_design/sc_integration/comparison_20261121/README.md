# SCB10H switched-capacitor readout and OTA integration

## Recommendation

Use the telescopic OTA with CMFB for this fabrication run. The retuned gain-boosted schematic performs comparably in the complete SC bench. Its first-pass layout misses the sampling window when the extracted OTA capacitances are included.

## Matched test

- Murata SCB10H-B012FB as CP and a 10 pF reference as CN. The pressure sweep uses Murata's nominal capacitance equation from document 82 1251 00 C and spans 30–120 kPa absolute. Separate endpoint tests apply the four tabulated capacitance tolerances. Sensor package stray capacitance is represented by illustrative pad and board loads. The PVT sweep changes the electronics corner with the nominal sensor curve held fixed.
- One 10 kHz source, the project's transistor-level timing and trim circuitry, TX discharge to ground, buffered RX precharge at 2.5 V, and 121 SCL08 PMOS feedback units per side (W=20 µm, L=10 µm per unit). The existing reference buffer and bias fanout are transistor-level. The master 2.5 V and booster 1.70 V and VDD−1.20 V references model external sources.
- Per branch, the bench has 5 pF load at the live OTA output, 10 pF hold capacitance, and 7 pF and 100 MΩ at the board input. The heavy-load screen uses 22 pF at the board input. Input pad loading is 2 pF on each TX and RX pad, rising to 4 pF in the heavy-load screen. The board loads are assumptions.
- The sampled voltage is the held differential at the output pins, measured at 81 µs or 0.2 µs after the track clock falls if that is later. Settling is checked against the live differential median from 87–89 µs. The band is ±0.1% of that value with a ±100 µV floor, evaluated through 150 ns before the falling track-clock midpoint. The three trim codes are selected for their corners. Most runs cover the first cycle. A finer two-cycle run and a four-cycle/alternate-solver diagnostic check the nominal result.
- Typical is SCL08 TNTP at 5 V and 27 °C. Cold is WNWP with the best resistor model at 4.5 V and 0 °C. Hot is BNWP with the worst resistor model at 5.5 V and 85 °C.

## Electrical results

| Metric | Telescopic schematic | Gain-boosted schematic | Telescopic extracted C | Gain-boosted extracted C |
|---|---:|---:|---:|---:|
| Nominal held differential at 100 kPa | 41.845 mV | 41.849 mV | 42.042 mV | 11.108 mV |
| Nominal held common-mode at 100 kPa | 2.498 V | 2.498 V | 2.498 V | 4.866 V |
| Pressure/ASIC-corner points settled | 18/18 | 18/18 | 18/18 | 0/18 |
| Minimum margin before track ends across those points | 6.86 µs | 6.97 µs | 6.81 µs | Outside settling band |
| Nominal OTA supply power at 100 kPa | 280 µW | 273 µW | 280 µW | 266 µW |
| Nominal modeled readout supply power at 100 kPa | 3.015 mW | 3.009 mW | 3.015 mW | 2.998 mW |

The extracted telescopic output ranges from −187.51 to +146.11 mV across 30–120 kPa, corresponding to 3.71 mV/kPa averaged across the range. The minimum settling margin is 5.38 µs in the selected heavy-load tests. A nominal pressure lookup applied at the selected ASIC corners gives a worst-case 2.47 kPa residual over the sampled points. The lookup uses the same simulated sensor capacitance curve at all temperatures, and this number represents electronics drift within the simulation.

An illustrative direct ADC test attaches a discharged 5 pF acquisition capacitor to each held output for 1 µs through 100 Ω. At nominal 100 kPa, the extracted telescopic's differential falls from 42.02 mV at the pins before acquisition to 32.49 mV on the ADC capacitors. Use a high-impedance board buffer, or use the actual ADC input model to qualify a direct connection.

## Layout and diagnostic results

| Locally checked OTA macro | Bounding size | Bounding area | SCL08 KLayout DRC markers | LVS |
|---|---|---:|---:|---|
| Telescopic | 1.058 × 1.226 mm | 1.297 mm² | 0 | Match |
| Retuned gain-boosted, first pass | 1.327 × 2.029 mm | 2.693 mm² | 0 | Match |

These are the measured bounding areas of the implemented OTA macros. The gain-boosted layout uses two nominal 1 MΩ poly resistors for common-mode sensing. The telescopic uses two nominal 200 kΩ resistors. The engineering extraction reports 54.72 pF versus 10.64 pF summed across the resistor midpoint capacitances to ground. Excluding only those components from the gain-boosted model restores 2.498 V held common-mode, 41.84 mV differential, and 7.83 µs margin at 100 kPa. The unmodified extracted gain-boosted model still misses the timing band after four cycles and in a separate Gear run. The capacitance removal is an isolation test.

The extraction reuses the project's Magic engineering treatment for the poly resistor layer. Magic reported 20 terminal-connection warnings on the gain-boosted extraction, and KLayout LVS of the repaired extracted topology passed. The same SCL08 rule decks were used for both OTA macro checks. The area and electrical conclusions apply to these layouts and this extraction model. Full integrated layout and RC extraction including pads and ESD, selected ADC qualification, clocked noise, mismatch, and measured sensor and assembly variation remain open.

## Files and commands

- integration_comparison.png and integration_comparison.pdf contain the pressure, timing, common-mode, and area plots.
- pressure_summary.csv and all_results.csv contain the pressure summary and the sweep data. sensor_endpoints.csv and direct_adc.csv contain the interface checks.
- benches/ contains ngspice decks, logs and raw output. models/ contains the OTA and SC support netlists. The decks use the installed SCL08 model paths.
- boosted_layout/layout/ota_boosted_layout.gds contains the new OTA macro. boosted_layout/verification/ and telescopic_layout_check/ contain the DRC/LVS records.

Run from this directory in WSL with the project fixtures, local SCL08 PDK, and ngspice available.

    python3 compare.py nominal
    python3 compare.py pvt
    python3 compare.py stress
    python3 compare.py fine
    python3 check_layout.py
    python3 extract_boosted.py
    python3 pex_diag.py
    python3 interface_checks.py
    python3 report.py

The supplied extracted gain-boosted model lets the four simulator sweeps run immediately. Run the layout and extraction scripts first when regenerating that model from the source netlist.



## Repository setup

Use the installed SCL08 PDK in the standard home-directory location or set
the SCL08_MODELS environment variable to its ngspice_models49 directory.
The earlier clock and bias fixtures are in the adjacent validation_20261113
folder. The [current editable schematic](../integrated_sc_ota) has its own
setup command. The files here include the engineering capacitance extraction
and local DRC/LVS reports for both OTA macros.
