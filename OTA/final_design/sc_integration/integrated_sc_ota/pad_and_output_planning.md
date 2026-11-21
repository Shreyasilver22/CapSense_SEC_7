# Pad-frame and analog output planning

The installed SCL08 standard pad-frame manual enumerates these die bond-pad
counts. The package lead map depends on the selected bonding plan.

| Die | Approximate core | Signal pads | Dedicated VDD/VSS pads | Total |
|---|---|---:|---:|---:|
| 1 × 1 mm | 0.39 × 0.39 mm | 4 | 2 | 6 |
| 2 × 2 mm | 1.39 × 1.39 mm | 12 | 4 | 16 |
| 3 × 3 mm | 2.39 × 2.39 mm | 24 | 4 | 28 |
| 4 × 4 mm | 3.39 × 3.39 mm | 32 | 8 | 40 |
| 5 × 5 mm | 4.39 × 4.39 mm | 44 | 8 | 52 |

The present readout needs six signal pads with on-chip OTA bias and VP tied
to the 5 V supply: SENSP, SENSN, CLK10K, VREF, VOUTP, and VOUTN. External
clock trim adds three inputs. The 2 × 2 mm reference frame has six default
input and six default output cells, so seven inputs would require changing
one signal pad type. Keep the positions and cell types of the supply pads.
The layout and full integrated core fit remain to be checked.

The board can digitize both OTA outputs differentially or use a high-input-
impedance difference amplifier. A possible 3.3 V board interface is
VADC = 1.65 V + 10 × (VOUTP − VOUTN). The nominal corrected SC sweep maps
to approximately 0.83–2.20 V for that example. The actual ADC acquisition
load and sampling clock still require verification.

Source manual: SCL/VDG/AMDD/STD_PAD_FRAME_0.8µ/09/2026, pages 2–11.
