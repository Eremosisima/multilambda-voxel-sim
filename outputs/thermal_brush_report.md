# P1 Modeling Report: Thermal Transient and Crosstalk (Brush Array)

- Nominal: pitch=10.0 µm, z_sep=8.0 µm, Sb2S3 pulse=2.0 µs (target 320.0°C), VO2 pulse=0.5 µs (target 85.0°C)
- Sb2S3 core/neighbor/far peaks: 416.67 / 31.68 / 25.26 °C
- Estimated heat at adjacent VO2 segment (axial atten.): 26.35 °C (VO2 threshold 68°C, margin 41.65 °C)
- VO2 core/neighbor peaks: 155.43 / 26.37 °C

## Assumptions
- 1D radial finite-difference with lumped axial extraction; effective homogenized properties.
- Source calibrated heuristically to reach nominal peak in core; absolute values require FEM calibration.
- Axial coupling estimated via exponential attenuation over z_sep_um as first-order isolation proxy.
- Thresholds: VO2 68C, Sb2S3 programming ~300C (project spec).

## Pitch sweep (see thermal_brush_pitch_sweep.csv)
- Increasing pitch and z-separation reduces lateral/axial crosstalk; values guide isolation margins and scheduling.
