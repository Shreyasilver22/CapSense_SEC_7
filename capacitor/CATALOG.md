# Prepared capacitor values and layouts

EXPERIMENTAL extraction estimates, not silicon measurements. TOP/BOT are plate ports; SUB is the substrate reference.

| Requested | Units | Extracted mutual C | Error | GDS footprint | Layout |
|---|---:|---:|---:|---|---|
| 2.5p | 220 | 2.50448 pF | +0.1792% | 512 x 484 um | layouts/requested_2p5p.gds |
| 7.5p | 660 | 7.51344 pF | +0.1792% | 872 x 848 um | layouts/requested_7p5p.gds |
| 3p | 264 | 3.00538 pF | +0.1793% | 552 x 540 um | layouts/requested_3p.gds |
| 11.384f | 1 | 0.011384 pF | -0.0000% | 32 x 20 um | layouts/requested_11p384f.gds |
| 22.768f | 2 | 0.022768 pF | -0.0000% | 72 x 36 um | layouts/requested_22p768f.gds |
| 45.536f | 4 | 0.045536 pF | -0.0000% | 72 x 64 um | layouts/requested_45p536f.gds |
| 91.072f | 8 | 0.091072 pF | -0.0000% | 112 x 92 um | layouts/requested_91p072f.gds |
| 4p | 351 | 3.99578 pF | -0.1055% | 632 x 624 um | layouts/requested_4p.gds |
| 6p | 527 | 5.99937 pF | -0.0105% | 792 x 764 um | layouts/requested_6p.gds |
| 8p | 703 | 8.00295 pF | +0.0369% | 912 x 876 um | layouts/requested_8p.gds |
| 10p | 878 | 9.99515 pF | -0.0485% | 992 x 1016 um | layouts/requested_10p.gds |

The requested 2.5p/7.5p pair uses 220/660 units for a nominal exact 3:1 mutual-capacitance ratio. This is not statistical matching qualification. Nearest independent rounding would use 659 units for 7.5p; the shipped pair intentionally prioritizes the nominal ratio. The larger target is +0.1792% above its requested value, like the smaller one.

Substrate capacitances and verification are in results/catalog.csv and verification.json. Footprint includes intra-array routing, excludes guard rings and chip surroundings. No common-centroid/dummy layout, conductor-resistance extraction, mismatch or PVT qualification is claimed.
