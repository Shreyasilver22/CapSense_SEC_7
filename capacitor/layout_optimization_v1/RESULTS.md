# Matched-capacitance layout comparison

All values are experimental raw-.ext estimates. Useful capacitances match each baseline within 0.13%; unchanged extraction deck/conditions. No physical matching or tolerance claim.

| Target | Layout | Mutual C (pF) | TOP-sub (pF) | BOT-sub (pF) | Area (mm2) | M1 route R proxy (ohm) |
|---|---|---:|---:|---:|---:|---:|
| 3p | baseline | 3.00538 | 1.85155 | 5.51627 | 0.29808 | 13.25 |
| 3p | compact | 3.00457 | 1.60050 | 5.08205 | 0.19892 | 14.37 |
| 3p | slotted | 3.00539 | 0.46890 | 3.62743 | 0.12032 | 6.67 |
| 4p | baseline | 3.99578 | 2.44696 | 7.32176 | 0.39437 | 15.30 |
| 4p | compact | 3.99098 | 2.11585 | 6.74161 | 0.26265 | 16.58 |
| 4p | slotted | 3.99574 | 0.61532 | 4.80970 | 0.15948 | 7.55 |
| 8p | baseline | 8.00295 | 4.90149 | 14.62060 | 0.79891 | 21.95 |
| 8p | compact | 8.00463 | 4.24063 | 13.48970 | 0.52995 | 23.77 |
| 8p | slotted | 8.00291 | 1.21003 | 9.59705 | 0.31829 | 11.19 |

For the same ~4 pF mutual capacitance, slotted versus baseline reductions:

- TOP substrate loading: 74.85%
- BOT substrate loading: 34.31%
- Footprint: 59.56%

The routing-resistance column is a geometry/sheet-resistance proxy, not PEX. It excludes broad-plate distributed resistance, coupling, contacts, vias and frequency effects. It was not included in the OTA model. Compact routing is narrower and has a slightly larger proxy than the baseline despite smaller area.

Slotted geometry uses corresponding 20 um wide strips separated by 2 um slots, connected by separate 3 um side spines, rather than individual routed tiles. The lower metal signal plate shields much of the upper plate from substrate in the extraction model; no extra grounded shield or process layer is added. Less terminal/bus metal and fewer plate edges also contribute. The old extractor and simplified capacitance coefficients limit confidence in absolute and relative numbers; independent supported extraction is still required.
