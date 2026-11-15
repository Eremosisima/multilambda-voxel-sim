# Simulation report (Article 1 draft support)

- Materials: 4; levels/material: 4; capacity: 8 bits/voxel
- MZI matrix condition number: 1.1962
- Noiseless full-state decode accuracy: 100.0% (256 states)
- Phase step per level (rad): M1=2.8376, M2=-2.7979, M3=2.9920, M4=-2.5872
- Recommended layer spacing (model): >= 4.11 µm
- Thermal diffusion length (estimate): 1.09 µm
- Robustness sweep points: 20 (see outputs/robustness_calibration_sweep.csv)
- Sensitivity: design 60 pts, crosstalk/noise 30 pts (outputs/sensitivity_*.csv)
- SNR budget points: 48, feasible (half-step margin >=3*sigma): 48 (outputs/snr_budget.csv)
- Sustainability scenario (same-work, best case 10.0 TOPS/W vs ref): avoided ~46603 tCO2/year out of 49056 tCO2/year (assumptions in outputs/sustainability_scenarios.json)

Key artifacts: outputs/*.csv, outputs/*.json, figures/*.png, ARTICLE1_SKELETON.md
Note: parameters are literature-inspired simulation assumptions; replace with cited/measured values for publication. Energy/CO2 results are scenarios, not measured device claims.