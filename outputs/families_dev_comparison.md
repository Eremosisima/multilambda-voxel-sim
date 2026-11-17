# Family Development Comparison (Price, Feasibility, Speed, Reliability, Dimensions, Capacity)

> Conceptual estimates for implementers. Not measured data, not pricing quotes.

## Summary table

| Key | Variant | Inf (ps) | Reconf (s) | TOPS/tile | Mem (MB) | BW (TB/s) | Endurance | Stab | Feas | Tile mm² | Vol cm³ | Cost idx | Unit $ (est) | $/TOPS (est) | Rel idx | Spd idx | Cap idx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | Interferometric PCM (Ref) | 10 | 2e-05 | 2.0 | 64 | 0.8 | 1e+06 | 3/5 | 3/5 | 25 | 45 | 1.00 | 2500 | 1250 | 0.425 | 0.31 | 0.199 |
| A2 | Interferometric PCM+EO hybrid | 10 | 1e-09 | 2.5 | 56 | 1.0 | 1e+06 | 3/5 | 2/5 | 28 | 50 | 1.45 | 3800 | 1520 | 0.425 | 0.375 | 0.232 |
| A3 | Coherent I/Q | 12 | 2e-05 | 3.0 | 72 | 1.2 | 1e+06 | 2/5 | 2/5 | 30 | 50 | 1.60 | 4200 | 1400 | 0.325 | 0.301 | 0.282 |
| B1 | Resonant BIC/PCM | 40 | 5e-06 | 1.8 | 96 | 0.6 | 5e+05 | 3/5 | 2/5 | 12 | 30 | 1.20 | 3200 | 1778 | 0.406 | 0.257 | 0.201 |
| B3 | Resonant WDM bank | 30 | 1e-06 | 4.0 | 128 | 2.5 | 5e+06 | 3/5 | 3/5 | 18 | 35 | 1.30 | 3500 | 875 | 0.469 | 0.273 | 0.431 |
| C1 | Electro-optic Pockels (RT) | 5 | 5e-12 | 3.5 | 8 | 3.0 | 1e+12 | 4/5 | 2/5 | 35 | 40 | 2.10 | 6500 | 1857 | 0.9 | 0.589 | 0.337 |
| C2 | EO nonvolatile/ferroelectric | 8 | 1e-09 | 3.0 | 32 | 2.0 | 1e+09 | 4/5 | 1/5 | 30 | 40 | 1.90 | 7000 | 2333 | 0.713 | 0.388 | 0.284 |
| D1 | Plasmonic/ENZ hybrid | 1 | 1e-06 | 1.2 | 24 | 0.5 | 1e+05 | 2/5 | 1/5 | 8 | 20 | 1.70 | 5000 | 4167 | 0.263 | 0.571 | 0.11 |
| E1 | All-optical nonlinear (Kerr/2D) | 0.5 | 1e-12 | 1.0 | 12 | 1.5 | 1e+10 | 2/5 | 1/5 | 15 | 25 | 1.80 | 5500 | 5500 | 0.575 | 1.215 | 0.127 |
| F1 | Diffractive/metasurface | 20 | 1e-06 | 5.0 | 80 | 1.8 | 1e+07 | 3/5 | 2/5 | 20 | 60 | 1.50 | 4500 | 900 | 0.487 | 0.289 | 0.435 |
| A1-3D | OPGPU-Ref 3D Brush (A1) | 15 | 2e-05 | 8.0 | 512 | 2.0 | 1e+06 | 3/5 | 2/5 | 900 | 120 | 2.40 | 9000 | 1125 | 0.425 | 0.29 | 0.925 |
| C1-B | RT EO + WDM resonant | 5 | 5e-12 | 6.0 | 48 | 4.0 | 1e+10 | 3/5 | 1/5 | 40 | 45 | 2.60 | 8500 | 1417 | 0.675 | 0.589 | 0.558 |

## Rankings (best → worst)

- **price_low_cost:** A1, B1, B3, A2, F1, A3, D1, E1, C2, C1, A1-3D, C1-B
- **feasibility:** A1, B3, A2, A3, B1, C1, F1, A1-3D, C2, D1, E1, C1-B
- **speed:** E1, C1, C1-B, D1, C2, A2, A1, A3, A1-3D, F1, B3, B1
- **reliability:** C1, C2, C1-B, E1, F1, B3, A1, A2, A1-3D, B1, A3, D1
- **compactness:** D1, B1, E1, B3, F1, A1, A2, A3, C2, C1, C1-B, A1-3D
- **capacity:** A1-3D, C1-B, F1, B3, C1, C2, A3, A2, B1, A1, E1, D1
- **capacity_compute:** A1-3D, C1-B, F1, B3, C1, A3, C2, A2, A1, B1, D1, E1
- **capacity_memory:** A1-3D, B3, B1, F1, A3, A1, A2, C1-B, C2, D1, E1, C1

## Recommended by priority

- **lowest_price_accessible:** A1, B1, B3, A2, F1
- **highest_feasibility:** A1, B3, A2, A3, B1
- **highest_speed:** E1, C1, C1-B, D1, C2
- **highest_reliability:** C1, C2, C1-B, E1, F1
- **smallest_footprint:** D1, B1, E1, B3, F1
- **highest_capacity:** A1-3D, C1-B, F1, B3, C1

## Notes

- All values are conceptual, order-of-magnitude estimates for open-hardware comparison; not quotes or measured data.
- Price/cost depends strongly on volume, yield, packaging, laser/detector sourcing, and process node.
- Reliability index combines endurance (log) and stability score; real lifetime requires qualification.
- Dimensions compare module/tile scale; 3D brush trades area for volumetric density.
- Capacity combines compute throughput (TOPS/tile), effective optical memory/storage (MB/module) and memory bandwidth (TB/s), normalized within this set.
- Feasibility reflects availability of platforms/processes and integration complexity for implementers.
