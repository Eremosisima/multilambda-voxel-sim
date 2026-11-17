# Family Development Comparison (Price, Feasibility, Speed, Reliability, Dimensions, Capacity)

> Conceptual estimates for implementers. Not measured data, not pricing quotes.

## Summary table

| Key | Variant | Inf (ps) | Reconf (s) | TOPS/tile | Mem (MB) | BW (TB/s) | Endurance | Stab | Feas | Tile mm² | Vol cm³ | Cost idx | Unit $ (est) | $/TOPS (est) | Rel idx | Spd idx | Cap idx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | Interferometric PCM (Ref) | 10 | 2e-05 | 2.0 | 64 | 0.8 | 1e+06 | 3/5 | 3/5 | 25 | 45 | 1.00 | 2500 | 1250 | 0.425 | 0.31 | 0.158 |
| A2 | Interferometric PCM+EO hybrid | 10 | 1e-09 | 2.5 | 56 | 1.0 | 1e+06 | 3/5 | 2/5 | 28 | 50 | 1.45 | 3800 | 1520 | 0.425 | 0.375 | 0.186 |
| A3 | Coherent I/Q | 12 | 2e-05 | 3.0 | 72 | 1.2 | 1e+06 | 2/5 | 2/5 | 30 | 50 | 1.60 | 4200 | 1400 | 0.325 | 0.301 | 0.225 |
| B1 | Resonant BIC/PCM | 40 | 5e-06 | 1.8 | 96 | 0.6 | 5e+05 | 3/5 | 2/5 | 12 | 30 | 1.20 | 3200 | 1778 | 0.406 | 0.257 | 0.157 |
| B3 | Resonant WDM bank | 30 | 1e-06 | 4.0 | 128 | 2.5 | 5e+06 | 3/5 | 3/5 | 18 | 35 | 1.30 | 3500 | 875 | 0.469 | 0.273 | 0.346 |
| C1 | Electro-optic Pockels (RT) | 5 | 5e-12 | 3.5 | 8 | 3.0 | 1e+12 | 4/5 | 2/5 | 35 | 40 | 2.10 | 6500 | 1857 | 0.9 | 0.589 | 0.279 |
| C2 | EO nonvolatile/ferroelectric | 8 | 1e-09 | 3.0 | 32 | 2.0 | 1e+09 | 4/5 | 1/5 | 30 | 40 | 1.90 | 7000 | 2333 | 0.713 | 0.388 | 0.232 |
| D1 | Plasmonic/ENZ hybrid | 1 | 1e-06 | 1.2 | 24 | 0.5 | 1e+05 | 2/5 | 1/5 | 8 | 20 | 1.70 | 5000 | 4167 | 0.263 | 0.571 | 0.088 |
| E1 | All-optical nonlinear (Kerr/2D) | 0.5 | 1e-12 | 1.0 | 12 | 1.5 | 1e+10 | 2/5 | 1/5 | 15 | 25 | 1.80 | 5500 | 5500 | 0.575 | 1.215 | 0.106 |
| F1 | Diffractive/metasurface | 20 | 1e-06 | 5.0 | 80 | 1.8 | 1e+07 | 3/5 | 2/5 | 20 | 60 | 1.50 | 4500 | 900 | 0.487 | 0.289 | 0.349 |
| A1-3D | OPGPU-Ref 3D Brush (A1) | 15 | 2e-05 | 8.0 | 512 | 2.0 | 1e+06 | 3/5 | 2/5 | 900 | 120 | 2.40 | 9000 | 1125 | 0.425 | 0.29 | 0.715 |
| C1-B | RT EO + WDM resonant | 5 | 5e-12 | 6.0 | 48 | 4.0 | 1e+10 | 3/5 | 1/5 | 40 | 45 | 2.60 | 8500 | 1417 | 0.675 | 0.589 | 0.457 |
| G2 | Thin-film membrane stack (EO-tuned) | 3 | 1e-11 | 5.5 | 192 | 3.2 | 1e+11 | 3/5 | 2/5 | 18 | 30 | 1.85 | 6200 | 1127 | 0.738 | 0.588 | 0.475 |
| G3 | Thin-film membrane stack (PCM+EO hybrid) | 4 | 5e-10 | 5.0 | 256 | 2.8 | 1e+07 | 3/5 | 2/5 | 20 | 32 | 1.75 | 5800 | 1160 | 0.487 | 0.447 | 0.468 |
| H1 | Membrane-Brush NV (A1+G3+3D) | 12 | 1e-09 | 9.0 | 640 | 2.6 | 1e+07 | 3/5 | 2/5 | 700 | 100 | 2.30 | 9800 | 1089 | 0.487 | 0.365 | 0.848 |
| H2 | RT Membrane-WDM Core (G2+B3+C1) | 3 | 1e-11 | 7.0 | 96 | 4.5 | 1e+11 | 3/5 | 1/5 | 30 | 38 | 2.70 | 9200 | 1314 | 0.738 | 0.588 | 0.547 |
| H3 | Open WDM-PCM (A1+G1+B3) | 18 | 2e-05 | 3.5 | 160 | 1.6 | 1e+06 | 3/5 | 3/5 | 22 | 40 | 1.40 | 3600 | 1029 | 0.425 | 0.282 | 0.306 |
| H4 | Volumetric Tensor Membrane (G2/G3+F2+A1) | 8 | 5e-10 | 10.0 | 720 | 3.5 | 1e+07 | 3/5 | 1/5 | 500 | 90 | 3.00 | 12000 | 1200 | 0.487 | 0.398 | 0.967 |
| H5 | Dense Resonant Stack (B1+G3+D1) | 6 | 5e-10 | 4.0 | 140 | 1.4 | 5e+06 | 2/5 | 1/5 | 14 | 28 | 2.40 | 7800 | 1950 | 0.369 | 0.416 | 0.315 |

## Rankings (best → worst)

- **price_low_cost:** A1, B1, B3, H3, A2, F1, A3, D1, G3, E1, G2, C2, C1, H1, A1-3D, H5, C1-B, H2, H4
- **feasibility:** A1, B3, H3, A2, A3, B1, C1, F1, A1-3D, G2, G3, H1, C2, D1, E1, C1-B, H2, H4, H5
- **speed:** E1, C1, C1-B, G2, H2, D1, G3, H5, H4, C2, A2, H1, A1, A3, A1-3D, F1, H3, B3, B1
- **reliability:** C1, G2, H2, C2, C1-B, E1, F1, G3, H1, H4, B3, A1, A2, A1-3D, H3, B1, H5, A3, D1
- **compactness:** D1, B1, H5, E1, B3, G2, F1, G3, H3, A1, A2, A3, C2, H2, C1, C1-B, H4, H1, A1-3D
- **capacity:** H4, H1, A1-3D, H2, G2, G3, C1-B, F1, B3, H5, H3, C1, C2, A3, A2, A1, B1, E1, D1
- **capacity_compute:** H4, H1, A1-3D, H2, C1-B, G2, F1, G3, B3, H5, C1, H3, A3, C2, A2, A1, B1, D1, E1
- **capacity_memory:** H4, H1, A1-3D, G3, G2, H3, H5, B3, B1, H2, F1, A3, A1, A2, C1-B, C2, D1, E1, C1

## Recommended by priority

- **lowest_price_accessible:** A1, B1, B3, H3, A2
- **highest_feasibility:** A1, B3, H3, A2, A3
- **highest_speed:** E1, C1, C1-B, G2, H2
- **highest_reliability:** C1, G2, H2, C2, C1-B
- **smallest_footprint:** D1, B1, H5, E1, B3
- **highest_capacity:** H4, H1, A1-3D, H2, G2

## Notes

- All values are conceptual, order-of-magnitude estimates for open-hardware comparison; not quotes or measured data.
- Price/cost depends strongly on volume, yield, packaging, laser/detector sourcing, and process node.
- Reliability index combines endurance (log) and stability score; real lifetime requires qualification.
- Dimensions compare module/tile scale; 3D brush trades area for volumetric density.
- Capacity combines compute throughput (TOPS/tile), effective optical memory/storage (MB/module) and memory bandwidth (TB/s), normalized within this set.
- Feasibility reflects availability of platforms/processes and integration complexity for implementers.
