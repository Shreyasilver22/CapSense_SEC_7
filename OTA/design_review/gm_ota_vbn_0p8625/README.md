# Uploaded five-transistor OTA at VBN = 0.8625 V

The uploaded gm_ota.sch is the circuit and gm_ota.sym is its reusable symbol. Both were checked through an Xschem-generated symbol testbench and simulated with ngspice using local typical SCL08 Level 49 MOS models.

## Conditions

VDD 5 V, VSS 0 V, VBN 0.8625 V, 27 °C. SP DC input 2.5 V and explicit output capacitance 5 pF were adopted from the supplied drawing notes. The actual instances all use L = 3.2 µm. M1–M4 use W = 2.5 µm and M5 uses W = 5 µm. SP is noninverting and SENSE is inverting for output voltage.

## Results

| Quantity | Result |
|---|---:|
| Gain at follower DC bias | 44.99 dB |
| Unity-gain bandwidth | 154.54 kHz |
| Estimated differential phase margin | 89.98° |
| Open-loop −3 dB bandwidth at follower bias | 867.77 Hz |
| Supply current | 0.7864 µA |
| OTA supply power | 3.9322 µW |
| Effective sink transconductance at clamped 2.5 V output | 4.8650 µS |
| Follower output for a 2.5 V input | 2.505934 V |
| Worst 100 mV dynamic settling | 7.086 µs |
| Worst 2 V dynamic settling | 16.317 µs |
| Natural output at equal 2.5 V inputs | 3.559467 V |

Dynamic settling uses a ±0.1% step-amplitude band around the attained output. The 100 mV follower step has about 5.4–5.9 mV of static error, so it misses that band around the ideal input command. Settling relative to an attained plateau and absolute tracking error are retained as separate measurements in results/settling.csv.

All five transistors have positive modeled saturation margin at the nominal 2.5 V follower operating point. The measured tail current is approximately 0.786 µA.

## Verification and limits

The original supplied schematic and symbol were copied byte-for-byte into designs/. The expanded symbol subcircuit matches the five MOS instance connections in the standalone netlist. Independent symbol-export and benchmark AC responses agreed within about 0.01 percent. Steady transient outputs were checked at 2 ns versus 5 ns maximum timestep.

The supplied annotation says L = 0.8 µm and Cc = 5 pF, while the actual instances use L = 3.2 µm and contain no internal capacitor. The output pin IOUT is declared as an input in the supplied metadata. Ngspice uses the connected circuit regardless of that direction tag. Xschem also reports undriven-node checks for the code-based testbench sources.

The native HSPICE-style models produce ignored-parameter warnings in ngspice, including PMOS overlap-capacitance parameters. Source/drain instance areas are unspecified in the upload. Frequency and transient predictions inherit these model limits. These tests use ideal bias sources and do not establish SC-system, noise, mismatch or PVT performance.

## Files and rerun

- designs/ contains the source schematic, symbol and expanded subcircuit.
- tb/gm_ota_symbol_tb.sch is the symbol-based testbench.
- results/ contains exact benches, simulator logs, numerical waveforms, CSV tables and verification records.
- plots/ contains the frequency response, follower steps, current transfer and input-bias sweep.

Run python3 run.py followed by python3 plot.py from this folder. The scripts regenerate bench include paths for this project location and expect the local SCL08 PDK under ~/pdk/scl08. Open the symbol testbench with xschem --rcfile ./xschemrc tb/gm_ota_symbol_tb.sch.
