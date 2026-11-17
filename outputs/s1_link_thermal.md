# S1 — Presupuesto de enlace óptico y márgenes térmicos (conceptual)

> Modelo paramétrico S1. No son mediciones; requiere calibración con IL/FEM/ruido medidos.

## Resumen por candidato

| Candidato | IL (dB) | Rx (dBm) | Margen enlace (dB) | Margen sens. (dB) | Enlace ok (>=3dB) | Vecino nominal (C) | Margen VO2 nom (C) | Vecino peor caso (C) | Margen VO2 peor (C) | Térmica nominal | Térmica peor caso |
|---|---:|---:|---:|---:|:---:|---:|---:|---:|---:|:---:|:---:|
| H3 | 10.4 | -7.4 | 10.6 | 14.6 | sí | 70.75 | -2.75 | 117.47 | -49.47 | no | no |
| G2 | 6.7 | -3.7 | 14.3 | 18.3 | sí | 51.75 | 16.25 | 52.65 | 15.35 | sí | sí |
| G3 | 7.1 | -4.1 | 13.9 | 17.9 | sí | 68.55 | -0.55 | 114.39 | -46.39 | no | no |
| H1 | 11.1 | -8.1 | 9.9 | 13.9 | sí | 70.55 | -2.55 | 117.19 | -49.19 | no | no |
| H4 | 12.4 | -9.4 | 8.6 | 12.6 | sí | 71.45 | -3.45 | 118.45 | -50.45 | no | no |

## Recalibración térmica (secuenciado/enfriamiento, PCM candidatos)

| Candidato | Escenario | Vecino nom (C) | Margen nom (C) | Vecino peor (C) | Margen peor (C) | Nom | Peor |
|---|---|---:|---:|---:|---:|:---:|:---:|
| H3 | OMCC-sequenced writes + trench/spreader + TEC assist | 54.0 | 14.0 | 74.82 | -6.82 | sí | no |
| G3 | Duty-cycled PCM writes + isolation + TEC assist | 51.8 | 16.2 | 71.74 | -3.74 | sí | no |
| H1 | Strict OMCC sequencing + vertical/lateral isolation + manifold cooling | 49.32 | 18.68 | 65.43 | 2.57 | sí | sí |
| H4 | Aggressive sequencing + high-capacity spreading/manifold + active stabilization | 46.85 | 21.15 | 60.83 | 7.17 | sí | sí |

## Notas

- **H3**: Thermal dominated by PCM writes near rings/VO2; relies on trenches, spreading, TEC and OMCC sequencing.
- **G2**: No 300C PCM write; thermal load mainly EO/RF drivers and stabilization, manageable with spreading.
- **G3**: Localized PCM write heat co-integrated with EO; requires isolation/trenches and duty-cycled writes.
- **H1**: 3D stacking increases path/crossings and thermal density; segmented heaters, vertical/lateral isolation and strict sequencing required.
- **H4**: Highest optical path complexity and distributed thermal load; needs high-capacity spreading/cooling and active stabilization.

## Barrido layout/duty transitorio (conceptual, candidatos PCM)

| Candidato | Layout | Duty | Vecino nom (°C) | Margen nom (°C) | Vecino peor (°C) | Margen peor (°C) | Nom | Peor |
|---|---|---:|---:|---:|---:|---:|:---:|:---:|
| H3 | compact | 0.03 | 49.54 | 18.46 | 52.76 | 15.24 | sí | sí |
| H3 | compact | 0.05 | 51.91 | 16.09 | 56.2 | 11.8 | sí | sí |
| H3 | compact | 0.08 | 55.45 | 12.55 | 61.36 | 6.64 | sí | sí |
| H3 | compact | 0.12 | 60.18 | 7.82 | 68.24 | -0.24 | sí | no |
| H3 | compact | 0.18 | 67.27 | 0.73 | 78.57 | -10.57 | sí | no |
| H3 | baseline | 0.03 | 49.0 | 19.0 | 52.14 | 15.86 | sí | sí |
| H3 | baseline | 0.05 | 51.0 | 17.0 | 55.16 | 12.84 | sí | sí |
| H3 | baseline | 0.08 | 54.0 | 14.0 | 59.7 | 8.3 | sí | sí |
| H3 | baseline | 0.12 | 58.0 | 10.0 | 65.74 | 2.26 | sí | sí |
| H3 | baseline | 0.18 | 64.0 | 4.0 | 74.82 | -6.82 | sí | no |
| H3 | spread_out | 0.03 | 48.58 | 19.42 | 51.75 | 16.25 | sí | sí |
| H3 | spread_out | 0.05 | 50.3 | 17.7 | 54.52 | 13.48 | sí | sí |
| H3 | spread_out | 0.08 | 52.88 | 15.12 | 58.67 | 9.33 | sí | sí |
| H3 | spread_out | 0.12 | 56.32 | 11.68 | 64.21 | 3.79 | sí | sí |
| H3 | spread_out | 0.18 | 61.48 | 6.52 | 72.51 | -4.51 | sí | no |
| G3 | compact | 0.03 | 47.34 | 20.66 | 49.68 | 18.32 | sí | sí |
| G3 | compact | 0.05 | 49.71 | 18.29 | 53.12 | 14.88 | sí | sí |
| G3 | compact | 0.08 | 53.25 | 14.75 | 58.28 | 9.72 | sí | sí |
| G3 | compact | 0.12 | 57.98 | 10.02 | 65.16 | 2.84 | sí | sí |
| G3 | compact | 0.18 | 65.07 | 2.93 | 75.49 | -7.49 | sí | no |
| G3 | baseline | 0.03 | 46.8 | 21.2 | 49.06 | 18.94 | sí | sí |
| G3 | baseline | 0.05 | 48.8 | 19.2 | 52.08 | 15.92 | sí | sí |
| G3 | baseline | 0.08 | 51.8 | 16.2 | 56.62 | 11.38 | sí | sí |
| G3 | baseline | 0.12 | 55.8 | 12.2 | 62.66 | 5.34 | sí | sí |
| G3 | baseline | 0.18 | 61.8 | 6.2 | 71.74 | -3.74 | sí | no |
| G3 | spread_out | 0.03 | 46.38 | 21.62 | 48.67 | 19.33 | sí | sí |
| G3 | spread_out | 0.05 | 48.1 | 19.9 | 51.44 | 16.56 | sí | sí |
| G3 | spread_out | 0.08 | 50.68 | 17.32 | 55.59 | 12.41 | sí | sí |
| G3 | spread_out | 0.12 | 54.12 | 13.88 | 61.13 | 6.87 | sí | sí |
| G3 | spread_out | 0.18 | 59.28 | 8.72 | 69.43 | -1.43 | sí | no |
| H1 | compact | 0.03 | 46.96 | 21.04 | 50.03 | 17.97 | sí | sí |
| H1 | compact | 0.05 | 49.26 | 18.74 | 53.37 | 14.63 | sí | sí |
| H1 | compact | 0.08 | 52.72 | 15.28 | 58.38 | 9.62 | sí | sí |
| H1 | compact | 0.12 | 57.33 | 10.67 | 65.06 | 2.94 | sí | sí |
| H1 | compact | 0.18 | 64.24 | 3.76 | 75.08 | -7.08 | sí | no |
| H1 | baseline | 0.03 | 46.41 | 21.59 | 49.39 | 18.61 | sí | sí |
| H1 | baseline | 0.05 | 48.35 | 19.65 | 52.31 | 15.69 | sí | sí |
| H1 | baseline | 0.08 | 51.26 | 16.74 | 56.68 | 11.32 | sí | sí |
| H1 | baseline | 0.12 | 55.14 | 12.86 | 62.52 | 5.48 | sí | sí |
| H1 | baseline | 0.18 | 60.96 | 7.04 | 71.26 | -3.26 | sí | no |
| H1 | spread_out | 0.03 | 45.99 | 22.01 | 49.01 | 18.99 | sí | sí |
| H1 | spread_out | 0.05 | 47.65 | 20.35 | 51.67 | 16.33 | sí | sí |
| H1 | spread_out | 0.08 | 50.13 | 17.87 | 55.65 | 12.35 | sí | sí |
| H1 | spread_out | 0.12 | 53.45 | 14.55 | 60.97 | 7.03 | sí | sí |
| H1 | spread_out | 0.18 | 58.42 | 9.58 | 68.95 | -0.95 | sí | no |
| H4 | compact | 0.03 | 45.5 | 22.5 | 48.84 | 19.16 | sí | sí |
| H4 | compact | 0.05 | 47.76 | 20.24 | 52.08 | 15.92 | sí | sí |
| H4 | compact | 0.08 | 51.16 | 16.84 | 56.93 | 11.07 | sí | sí |
| H4 | compact | 0.12 | 55.7 | 12.3 | 63.41 | 4.59 | sí | sí |
| H4 | compact | 0.18 | 62.49 | 5.51 | 73.13 | -5.13 | sí | no |
| H4 | baseline | 0.03 | 44.95 | 23.05 | 48.19 | 19.81 | sí | sí |
| H4 | baseline | 0.05 | 46.85 | 21.15 | 51.0 | 17.0 | sí | sí |
| H4 | baseline | 0.08 | 49.7 | 18.3 | 55.21 | 12.79 | sí | sí |
| H4 | baseline | 0.12 | 53.5 | 14.5 | 60.83 | 7.17 | sí | sí |
| H4 | baseline | 0.18 | 59.2 | 8.8 | 69.25 | -1.25 | sí | no |
| H4 | spread_out | 0.03 | 44.53 | 23.47 | 47.8 | 20.2 | sí | sí |
| H4 | spread_out | 0.05 | 46.14 | 21.86 | 50.35 | 17.65 | sí | sí |
| H4 | spread_out | 0.08 | 48.57 | 19.43 | 54.18 | 13.82 | sí | sí |
| H4 | spread_out | 0.12 | 51.8 | 16.2 | 59.28 | 8.72 | sí | sí |
| H4 | spread_out | 0.18 | 56.65 | 11.35 | 66.92 | 1.08 | sí | sí |

### Duty máximo factible por layout (margen VO2 ≥ 0 °C)

| Candidato | Layout | Max duty nominal | Max duty peor caso |
|---|---|---:|---:|
| G3 | compact | 0.18 | 0.12 |
| G3 | baseline | 0.18 | 0.12 |
| G3 | spread_out | 0.25 | 0.12 |
| H1 | compact | 0.18 | 0.12 |
| H1 | baseline | 0.25 | 0.12 |
| H1 | spread_out | 0.25 | 0.12 |
| H3 | compact | 0.18 | 0.08 |
| H3 | baseline | 0.18 | 0.12 |
| H3 | spread_out | 0.25 | 0.12 |
| H4 | compact | 0.18 | 0.12 |
| H4 | baseline | 0.25 | 0.12 |
| H4 | spread_out | 0.25 | 0.18 |

## Recomendaciones S1
- Refinar IL con datos de proceso (acoplos, propagación, rings/membranas/MZI) y presupuesto de ruido del receptor.
- Ejecutar FEM térmico 3D transitorio con layout real (trench, pitch, duty cycle OMCC) para validar márgenes VO2 y estabilidad de resonancias; usar barrido layout/duty como guía de secuenciado.
- Para H1/H4, co-optimizar ruta óptica (cruces/longitud) y distribución térmica (manifold/secuenciado, layouts spread-out) antes de E2/E4.
- Aplicar escenarios recalibrados y validar duty cycle efectivo y densidad de escritura por layout en S2/E2.
