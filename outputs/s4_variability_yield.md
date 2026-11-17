# S4 — Variabilidad de proceso y yield (Monte Carlo calibrado + optimizaciones)

> 3000 muestras por caso. Conceptual (no mediciones). Perfiles de proceso y optimizaciones para H3/G3/H1/H4.

### Línea base (proceso actual, baseline vs optimizado)

| Candidato | Dim | Variante | Proceso | Yield bruto | Yield efectivo | SNR medio (dB) | SNR p5 | Err fase p95 | IL p95 (dB) | >=70% | >=85% |
|---|---|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|
| H3 | 2.5D | baseline | Baseline process (current assumptions) | 1.0 | 0.9 | 13.2342 | 12.5989 | 0.0789 | 13.1023 | sí | sí |
| H3 | 2.5D | optimized | Baseline process (current assumptions) | 1.0 | 0.86 | 13.6954 | 13.0756 | 0.0709 | 12.7109 | sí | sí |
| G3 | 2.5D | baseline | Baseline process (current assumptions) | 1.0 | 0.92 | 14.7759 | 14.1323 | 0.0679 | 10.608 | sí | sí |
| G3 | 2.5D | optimized | Baseline process (current assumptions) | 1.0 | 0.89 | 15.2378 | 14.621 | 0.0607 | 10.1615 | sí | sí |
| H1 | 3D | baseline | Baseline process (current assumptions) | 0.9367 | 0.7962 | 11.3244 | 10.5178 | 0.1234 | 15.7389 | sí | sí |
| H1 | 3D | optimized | Baseline process (current assumptions) | 0.9973 | 0.7779 | 12.3313 | 11.5876 | 0.1014 | 14.8107 | sí | sí |
| H4 | 3D | baseline | Baseline process (current assumptions) | 0.7217 | 0.5918 | 10.4743 | 9.593 | 0.1439 | 17.1151 | sí | no |
| H4 | 3D | optimized | Baseline process (current assumptions) | 0.967 | 0.7156 | 11.7221 | 10.953 | 0.1167 | 16.0015 | sí | sí |

### Proceso mejorado + diseño optimizado

| Candidato | Dim | Variante | Proceso | Yield bruto | Yield efectivo | SNR medio (dB) | SNR p5 | Err fase p95 | IL p95 (dB) | >=70% | >=85% |
|---|---|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|
| H3 | 2.5D | optimized | Improved process control (metrology/calibrated) | 1.0 | 0.86 | 13.8986 | 13.4396 | 0.066 | 12.3764 | sí | sí |
| G3 | 2.5D | optimized | Improved process control (metrology/calibrated) | 1.0 | 0.89 | 15.4114 | 14.9792 | 0.0552 | 9.8508 | sí | sí |
| H1 | 3D | optimized | Improved process control (metrology/calibrated) | 1.0 | 0.78 | 12.6099 | 12.091 | 0.0882 | 14.4316 | sí | sí |
| H4 | 3D | optimized | Improved process control (metrology/calibrated) | 0.9963 | 0.7373 | 12.0268 | 11.4467 | 0.1018 | 15.6782 | sí | sí |

## Mejor ruta optimizada por candidato

| Candidato | Proceso | Yield bruto | Yield efectivo | SNR p5 | Err fase p95 | IL p95 | Optimización |
|---|---|---:|---:|---:|---:|---:|---|
| H3 | Baseline process (current assumptions) | 1.0 | 0.86 | 13.0756 | 0.0709 | 12.7109 | Partitioned WDM tiles + closed-loop calibration + spare rings |
| G3 | Baseline process (current assumptions) | 1.0 | 0.89 | 14.621 | 0.0607 | 10.1615 | EO trim + PCM write scheduling + improved coupling |
| H1 | Improved process control (metrology/calibrated) | 1.0 | 0.78 | 12.091 | 0.0882 | 14.4316 | Modular 3D partitioning + re-mapping spares + thermal vias/manifold |
| H4 | Pilot-line stabilized (tight control + thermal management) | 0.9997 | 0.7398 | 11.8377 | 0.0913 | 15.4123 | Hierarchical partitioning + alignment/calibration loops + higher redundancy |

## Lectura y optimizaciones
- **H3/G3 (2.5D):** ya cumplen objetivos con proceso base; optimización (particionado, calibración en lazo cerrado, spares) mejora margen y reduce sensibilidad térmica.
- **H1/H4 (3D):** baseline efectivo insuficiente para 85% (H4 crítico); particionado jerárquico/modular, re-mapeo de spares, calibración/alineación y control térmico elevan yield bruto y efectivo en perfiles mejorados.
- **Pendiente de calibración real:** reemplazar σ(n,d,acoplo,IL,térmica) con metrología; validar RAS/re-mapeo en OMCC y costo de redundancia en área/energía.
