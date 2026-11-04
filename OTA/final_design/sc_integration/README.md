# Shreyas SC circuit + telescopic OTA / CMFB — 1 November 2026

**A working nominal integration was actually simulated with the existing extracted-capacitance SCL08 OTA and explicit native-model transmission gates. It uses one shared fully differential OTA, an early RX-transfer phase and controlled switch-gate edges. It is not a direct two-op-amp substitution, an exact reproduction of the missing original switch cell, or a physical full-SC signoff.**

## Connection and changes

The repository schematic contains two single-ended behavioral amplifiers. Two copies of our telescopic OTA, each using only OUTP and letting its own CMFB control an auxiliary OUTM, give approximately **202.809 mV** instead of the two-amplifier ideal375 mV in the original-timing trial. That connection requires one active output near3.8125 V and its auxiliary output near1.1875 V at 5 V; it exceeds the prior high-gain swing envelope and is not the preferred integration.

The preferred testbench retains CP7 pF, CN5 pF, CF40 pF per branch, 5 V supply, 2.5 V reference, 10 kHz clock, phi1 sample/reset switches, sensor excitation and two feedback networks. It replaces the two amplifier blocks with one OTA:

| OTA pin | Connection |
|---|---|
| INP | SUM_N |
| INN | SUM_P |
| OUTP | OUT_P |
| OUTM | OUT_N |
| VDD / VSS | 5 V / 0 V nominal |
| IREF | Ideal3.5 uA current from VDD |
| VCM | 2.5 V output-common-mode reference |
| VBN | 3.0 V ideal external bias |
| VBP | VDD minus2.2 V |

This polarity gives negative differential feedback in both reset and transfer. **The OTA inputs are not tied to the2.5 V reference.** Their common mode follows charge conservation, about1.52 V during nominal transfer and2.5 V during reset. Input/output common mode must not be conflated.

## Why the original switching is inaccurate

With original simultaneous TX-discharge / RX-transfer controls, the one-OTA native-switch trial produces **164.386 mV**, versus326.087 mV ideal for the shared interface. RX_P briefly reaches **-0.817 V** and RX_N **-0.767 V**. Explicit body-diode probes in `selected_checks.json` record several pC flowing through the P-branch RX-connected NMOS body junctions around the switching edge. The capacitor loses signal charge; waiting longer does not restore it.

Advancing RX transfer by1 us largely removes this rectification at the nominal5 pF load, but 10 ns gate edges still have loading sensitivity (zero external load has a large error) and numerical convergence failures. The 49-case fast-edge trial completed **36/49**; failures are retained and are not called physical instability proofs.

The final prototype uses **a separate phiT RX-transfer control starting45 us, before phi2 TX-discharge starting46 us, and1 us rise/fall ramps on all switch controls**. Pulse widths are adjusted so the phase endpoints and100 us period are retained. Phi1 begins falling41 us, finishes42 us; phiT rises45–46 us; phi2 rises46–47 us; both transfer controls finish falling91 us. Phi1 returns100–101 us. These are deliberate timing/driver changes from the uploaded10 ns edges, not an unchanged-clock claim. Real clock buffers, slew control, skew, complementary-gate timing and their power have not been implemented.

## Correct ideal transfer for the shared OTA

For ideal switches/capacitors, equal summing-node voltages VX, and VOP+VON=2VCM:

`(CF+CP)*VX-CF*VOP = -CP*VDD`

`(CF+CN)*VX-CF*VON = -CN*VDD`

Therefore:

`VX = [2*CF*VCM-(CP+CN)*VDD]/[2*CF+CP+CN]`

`VOP-VON = 2*(CP-CN)*(VDD+VCM)/[2*CF+CP+CN]`

For CP7 pF, CN5 pF, CF40 pF, VDD5 V, VCM2.5 V, the ideal input CM is1.521739 V and differential output **326.086957 mV**. Ideal outputs are2.663043 V and2.336957 V. The former two-independent-amplifier ideal375 mV assumes both inputs stay at2.5 V and is a different transfer. The reconstructed behavioral controls agree with their respective equations; their success does not establish realistic OTA or switch behavior.

## Actual final nominal result

500 us / five cycles, native typical MOS/RPP,27 C, 5 pF explicit load per output, estimated switch junction geometry, ideal linear sensor/feedback capacitors:

| Quantity | Measured |
|---|---:|
| OUT_P at480 us | 2.66148567 V |
| OUT_N at480 us | 2.33519215 V |
| Differential output | 326.293520 mV |
| Ideal shared-interface output | 326.086957 mV |
| Raw differential error | 0.206563 mV |
| Output CM | 2.49833891 V |
| Input CM during transfer | 1.52007125 V |
| Differential tail settling, 0.1% of ideal differential step | 6.493 us |
| Modeled average VDD-rail power | 239.639 uW |

Settling is the last exit from a band about the measured89 us end-of-transfer output, measured from the46 us start of TX switching. It excludes static conversion error, clock jitter and noise. The phase lasts approximately45 us; the1 us gate ramps are included. Fine5 ns versus20 ns maximum-timestep sampled differential difference is **0.1900 uV**. These are nominal tests, not final ADC accuracy or maximum-clock specifications. VDD-rail power excludes ideal-clock source energy and practical clock/bias/reference generation overhead.

**Large switching glitches remain.** In the full nominal waveform, output CM briefly spans **1.2458 to 2.5954 V** and input CM **0.4764 to 2.5018 V**. Thus2.5 V output CM and1.52 V transfer input CM describe settled plateaus, not every instant. The OTA can temporarily leave its high-gain operating region and then recover. The ADC must sample late in phi2 (the tests sample80 us,34 us after TX switching begins), never assume these waveforms are glitch-free. Faster CMFB, controlled precharge and an implemented driver deserve further work if the system cannot tolerate these excursions. The plots deliberately retain the complete excursions.

Equal6/6 pF sensors give raw differential offset **0.283950 mV**. CP7->7.05 pF gives **7.969190 mV** change versus **7.970621 mV** analytical. This demonstrates incremental response in the modeled circuit; no physical baseline-calibration circuit, mismatch Monte Carlo or sampled-noise validation was added.

## Process / voltage / temperature and loading checks

Final gate-ramp version: five native MOS cards,4.5/5/5.5 V and0/27/85 C, typical RPP, CL5 pF gives45 SC transient cases. Four extra native best/worst-RPP cases use selected MOS/V/T corners and CL10 pF. Reference and output CM target remain fixed2.5 V. Clock and TX drive amplitudes follow VDD. Each stress case covers two cycles; the nominal circuit covers five. Selected load0/10 pF, equal/swapped sensors and +50 fF tests are separate.

- Completed: **49/49**; numerical failures: **0**.
- Largest sampled absolute differential error versus each corner's ideal transfer: **2.045392 mV**.
- Largest sampled output-CM error: **1.932950 mV**.
- Largest75-to89 us differential change: **0.161152 mV**.
- Largest completed-case0.1% dynamic settling: **16.561 us**.

These are measured bounds over these finite tests, not an unconditional pass or a finalized ASIC error budget. Inspect `final_corners.json`, `corner_checks.csv` and the corner plots for individual cases. Failures, if present, remain unresolved. The preceding fast-edge grid is separately labeled and is not mixed into final-version performance. Failed100-ohm abrupt/smooth ideal-switch diagnostics are retained; the actual final evidence uses native MOS switches. Do not convert numerical failure into a physical stability claim.

The worst raw-error corner was separately repeated with5 ns maximum timestep: sampled differential difference **3.0743 uV**, fine-run error **-2.048466 mV**. Its roughly2.05 mV error and residual late-phase drift persist with the finer timestep. The result does not meet a provisional0.1% differential-accuracy target across all tested conditions; no such target has been finalized for the ASIC.

## Files and reuse

- `designs/sc_cmfb.sch`: visible Xschem SC network with10 TG symbols, four capacitors and one extracted OTA symbol. No behavioral amplifier remains in this final schematic.
- `symbols/scl08_tg.sym`, `models/scl08_tg.spice`: explicit switch reconstruction. N W10/L0.8 um; P W20/L0.8 um, bodies0/VDD. Junction areas assume4.5 um source/drain extension and are estimates, not extracted switch layout.
- `symbols/ota_cm2p5.sym`, `../models/ota_cm2p5_C.spice`: unchanged previous OTA macro with built-in CMFB. Its extracted transistor/routing network is reused; only the SC system and clock controls are new.
- `tb/sc_cmfb.cir`: portable flat native-switch bench. Run from `tb` with `ngspice -b sc_cmfb.cir`.
- `tb/xschem_support.inc`: editable CP/CN/CF, load, clock/bias sources and simulation controls for the visible schematic. The selected default is10 kHz, CP7 pF, CN5 pF, CF40 pF, CL5 pF, phiT1 us early, gate edges1 us.
- `open_xschem.sh`: launch from this directory. Xschem netlist output goes to `tb`; the actual exported schematic was simulated for500 us and compared against the flat bench. `verification/views.json` checks switch/OTA pin mappings and sampled voltages.
- `tb/sc_cmfb.raw`: generated by the exported Xschem simulation. In ngspice: `load sc_cmfb.raw`, then `plot v(outp) v(outn)` or `plot v(outp)-v(outn)`; `plot v(phi1) v(phit) v(phi2)` shows the controls. The bench uses `quit` for batch runs; load its raw file in an interactive session afterward.
- `plots/`: PNG/PDF integration, timing and corner figures. `selected.json`, `summary.json` and per-run records retain exact settings.

## Scope and remaining work

The repo was read at commit327c0a9; original SCA upload1266134. Its TG and behavioral symbols are missing, so this is an explicit reconstruction of the visible labeled network, not a byte-identical original netlist reproduction. The behavioral model text was available and retained for controls. The original upload is available in the repository SCA directory.

Only the OTA uses the existing adapted C-extraction model. Full wire/contact/well/substrate RC, quantitative noise, mismatch, actual clock/reference circuits and reliability remain unqualified. **Both40 pF feedback capacitors remain ideal linear elements**; MOS compensation inside the OTA does not implement these precision capacitors. There is no full SC physical layout or new system DRC/LVS. Existing OTA DRC/LVS apply to its unchanged macro only. The SAR ADC has not been connected. The shared-OTA transfer and clock/driver changes must be reflected in the system model before treating this as the final ASIC front end.
