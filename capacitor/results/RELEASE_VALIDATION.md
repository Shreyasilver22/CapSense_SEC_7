# Release validation

Validated before upload on 28 October 2026.

- 11 prepared value aliases: 2.5p, 7.5p, 3p, 4p, 6p, 8p, 10p and 11.384f/22.768f/45.536f/91.072f.
- All physical variants regenerated; supplied KLayout DRC reports contain zero markers.
- Both metal networks connected; overlap area checked against unit count.
- Plate-transfer and both substrate-current checks passed for every value.
- Two-pin and three-pin xschem symbols netlisted and simulated.
- Native SVG display checked for requested/extracted values.
- Nominal 7.5p-to-2.5p mutual-capacitance ratio = 3.
- Four-weight charge-sharing example passed its expected plateau checks; it is not a SAR ADC.
- 4p schematic-driven layout/model preparation workflow was previously exercised end to end; fixture/model/layout are included and simulation rechecked in the standalone package.

Magic 8.3.105 is below the PDK header's required 8.3.579. The native exporter omits one substrate capacitor; explicit raw-.ext evaluation models retain the documented node/coupling terms. This incompatibility is unresolved. No formal capacitor LVS, matching, PVT, voltage-rating or silicon qualification is claimed.

No OTA circuit, foundry model card, technology file, rule deck, environment, credential or notebook is included. Scripts use the recipient's local authorized PDK for regeneration. Prepared lumped-model examples run without a PDK. Large waveform/raw files and machine-specific logs are ignored and reproducible.
