# S4 — Variabilidad de proceso y yield (Monte Carlo, conceptual)

> 2000 muestras por candidato. No son mediciones; calibrar con metrología/proceso y estadísticas de dispositivos.

## Resultados

| Candidato | Dim. | Yield bruto | Yield efectivo (tras redundancia) | SNR medio (dB) | SNR p5 (dB) | Error fase medio | Error fase p95 | IL medio (dB) | IL p95 (dB) | >=70% | >=85% |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|
| H3 | 2.5D | 1.0 | 0.9 | 13.2269 | 12.5855 | 0.0662 | 0.0789 | 12.5296 | 13.1204 | sí | sí |
| G3 | 2.5D | 1.0 | 0.92 | 14.777 | 14.1382 | 0.0542 | 0.067 | 10.0099 | 10.5995 | sí | sí |
| H1 | 3D | 0.9305 | 0.7909 | 11.3124 | 10.4899 | 0.0949 | 0.1234 | 15.1641 | 15.7599 | sí | sí |
| H4 | 3D | 0.7015 | 0.5752 | 10.4575 | 9.5515 | 0.1119 | 0.1471 | 16.5135 | 17.1531 | sí | no |

## Lectura
- H3/G3 (2.5D) muestran mejor robustez relativa bajo supuestos de calibración y menor correlación 3D; H1/H4 (3D) requieren mayor redundancia/calibración y control de proceso.
- El yield efectivo descuenta overhead de redundancia; ECC y calibración en OMCC son necesarios para acercarse a objetivos de prototipo.
## Acciones
- Obtener distribuciones reales (σ de n, d, acoplo, pérdida, térmica) por proceso/fundición.
- Optimizar particionado modular para contener fallos y permitir reparación/re-mapeo (OMCC).
- Endurecer calibración en lazo cerrado y pruebas de RAS en S4→E2.
