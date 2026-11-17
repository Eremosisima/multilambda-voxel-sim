# Objective Review: Family Combinations (Comparative Analysis & Simulations)

> Re-analysis of `families_dev_comparison.json` with derived metrics, scenario simulations, and sensitivity. Conceptual/order-of-magnitude only (not measured).

## 1. Key derived metrics (focus variants)

| Key | Variant | TOPS/mm² | TOPS/cm³ | MB/cm³ | TOPS/k$ | MB/k$ | Eff TOPS static | Eff TOPS dynamic | Eff TOPS mem-bound | Balanced | Obj overall |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| G2 | Thin-film membrane stack (EO-tuned) | 0.305556 | 0.183333 | 6.4 | 0.887097 | 30.967742 | 5.4951 | 5.5 | 5.2525 | 5.4159 | 0.712 |
| H1 | Membrane-Brush NV (A1+G3+3D) | 0.012857 | 0.09 | 6.4 | 0.918367 | 65.306122 | 8.968 | 10.35 | 5.2 | 8.1727 | 0.6787 |
| G3 | Thin-film membrane stack (PCM+EO hybrid) | 0.25 | 0.15625 | 8.0 | 0.862069 | 44.137931 | 4.994 | 5.75 | 5.0 | 5.248 | 0.6759 |
| H4 | Volumetric Tensor Membrane (G2/G3+F2+A1) | 0.02 | 0.111111 | 8.0 | 0.833333 | 60.0 | 9.9762 | 11.5 | 7.0 | 9.4921 | 0.6741 |
| B3 | Resonant WDM bank | 0.222222 | 0.114286 | 3.657143 | 1.142857 | 36.571429 | 3.965 | 4.5954 | 3.64 | 4.0668 | 0.6055 |
| A1-3D | OPGPU-Ref 3D Brush (A1) | 0.008889 | 0.066667 | 4.266667 | 0.888889 | 56.888889 | 7.9645 | 9.016 | 4.0 | 6.9935 | 0.5772 |
| H3 | Open WDM-PCM (A1+G1+B3) | 0.159091 | 0.0875 | 4.0 | 0.972222 | 44.444444 | 3.4814 | 3.9445 | 2.984 | 3.47 | 0.5739 |
| H2 | RT Membrane-WDM Core (G2+B3+C1) | 0.233333 | 0.184211 | 2.526316 | 0.76087 | 10.434783 | 6.9937 | 7.0 | 6.2125 | 6.7354 | 0.5736 |
| C1 | Electro-optic Pockels (RT) | 0.1 | 0.0875 | 0.2 | 0.538462 | 1.230769 | 3.4948 | 2.975 | 2.8897 | 3.1198 | 0.4723 |
| H5 | Dense Resonant Stack (B1+G3+D1) | 0.285714 | 0.142857 | 5.0 | 0.512821 | 17.948718 | 3.9928 | 4.6 | 2.5716 | 3.7215 | 0.4538 |
| A1 | Interferometric PCM (Ref) | 0.08 | 0.044444 | 1.422222 | 0.8 | 25.6 | 1.9941 | 1.96 | 1.384 | 1.7794 | 0.44 |

## 2. Internal consistency checks (baseline)

No major $/TOPS inconsistencies detected by this check.

## 3. Objective rankings (all variants)

- **overall:** G2, H1, G3, H4, B3, A1-3D, H3, H2, C1-B, C1 ...
- **speed:** H4, H2, H1, E1, C1-B, G2, A1-3D, G3, C1, H5 ...
- **capacity:** H4, G3, H1, G2, H2, A1-3D, H5, B3, C1-B, H3 ...
- **density_dims:** G3, G2, H4, H5, H2, H1, B3, H3, A1-3D, C1-B ...
- **reliability:** C1, G2, H2, C2, C1-B, E1, F1, G3, H1, H4 ...
- **feasibility:** A1, B3, H3, A2, A3, B1, C1, F1, A1-3D, G2 ...
- **price_perf:** H1, A1-3D, H4, B3, H3, G3, G2, F1, A1, B1 ...
- **open_access:** B3, H3, A1, H1, A1-3D, G3, G2, F1, B1, A3 ...
- **balanced_eff_tops:** H4, H1, A1-3D, H2, C1-B, G2, G3, F1, B3, H5 ...

## 4. Pareto fronts (non-dominated)

- **price_perf_vs_capacity:** H1, H4
- **feasibility_vs_speed:** B3, H1, H4
- **open_access_vs_capacity:** B3, G3, H1, H4

## 5. Sensitivity (rank stability, +/-30%, 200 trials)

| Key | mean rank | std | min | max | P(top5) |
|---|---:|---:|---:|---:|---:|
| A1 | 12.71 | 2.148 | 8 | 17 | 0.0 |
| B3 | 5.935 | 1.769 | 1 | 12 | 0.395 |
| G2 | 2.105 | 1.27 | 1 | 7 | 0.985 |
| G3 | 3.055 | 1.689 | 1 | 10 | 0.915 |
| H1 | 2.98 | 1.52 | 1 | 8 | 0.93 |
| H2 | 6.075 | 1.442 | 2 | 9 | 0.38 |
| H3 | 7.005 | 1.88 | 1 | 12 | 0.21 |
| H4 | 3.12 | 1.602 | 1 | 8 | 0.905 |
| H5 | 11.49 | 1.643 | 8 | 16 | 0.0 |
| C1 | 10.39 | 1.532 | 6 | 15 | 0.0 |
| A1-3D | 6.345 | 1.675 | 2 | 11 | 0.28 |

## 6. Objective review of combinations (H1–H5)

- **H1 Membrane-Brush NV:** highest capacity/density-by-volume in baseline (MB/cm³=6.4, TOPS/cm³=0.09) and strong overall (0.6787), but low areal compactness and high cost/complexity; dynamic efficiency benefits from NV weights but reconfig is not ultra-fast. Risk: 3D integration, thermal/phase tolerances.
- **H2 RT Membrane-WDM Core:** top speed/BW profile (BW=4.5 TB/s, balanced eff=6.7354) and good volumetric density, but **low NV memory** (MB/cm³=2.526316) and lowest feasibility/cost profile among H combos; best for streaming/dynamic kernels, weak as standalone weight store.
- **H3 Open WDM-PCM:** strongest open-access/feasibility-price proxy (obj_open_access=0.9062, feasibility=0.6, unit $3600); moderate speed (slow PCM reconfig) but decent memory density (MB/cm³=4.0) and NV. Most robust near-term candidate under open/practical constraints.
- **H4 Volumetric Tensor Membrane:** maximum raw capacity/throughput (TOPS=10.0, MB=720, cap_idx=0.967) yet highest cost/risk and low feasibility; efficiency advantage is scenario-dependent and integration/alignment dominate realizability.
- **H5 Dense Resonant Stack:** good areal/volumetric compute density but limited by reliability/stability (rel_idx=0.369, stability=2) and high losses (ENZ/plasmonic optional block); remains exploratory.

## 7. Conclusions (objective)

- **Best balanced candidate today (open/feasible): H3** — highest feasibility and best price-perf/open-access among hybrids, NV and incremental from A1.
- **Best dynamic/high-speed compact core: H2/G2** — strong in static/dynamic/bandwidth scenarios, but require external/NV weight strategy (pair with M1/A1 or H3) and thermal/phase control.
- **Best capacity scaling (if integration solved): H1/H4** — volumetric leaders; H4 highest ceiling, H1 more modular NV path. Both carry high cost and integration risk.
- **Baseline A1 remains the reference** for low cost/risk and openness; volumetric 3D (A1-3D) helps capacity but area/packaging trade-offs are significant.
- **Model caveats:** inputs are conceptual; $/TOPS fields show some baseline inconsistencies (section 2); power/thermal/system-loss models are not yet coupled — next step is physics-linked models (TMM for G, ring/F-P loss-Q, thermal) and per-mm²/mm³/W normalization.
