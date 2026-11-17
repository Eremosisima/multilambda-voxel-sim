# S1 — Presupuesto de enlace óptico y márgenes térmicos (conceptual)

> Modelo paramétrico S1. No son mediciones; requiere calibración con IL/FEM/ruido medidos.

## Resumen por candidato

| Candidato | IL (dB) | Rx (dBm) | Margen enlace (dB) | Margen sens. (dB) | Enlace ok (>=3dB) | Vecino nominal (C) | Margen VO2 nom (C) | Vecino peor caso (C) | Margen VO2 peor (C) | Térmica nominal | Térmica peor caso |
|---|---:|---:|---:|---:|:---:|---:|---:|---:|---:|:---:|:---:|
| H3 | 10.4 | -7.4 | 10.6 | 14.6 | sí | 70.75 | -2.75 | 112.85 | -44.85 | no | no |
| G2 | 6.7 | -3.7 | 14.3 | 18.3 | sí | 51.75 | 16.25 | 52.65 | 15.35 | sí | sí |
| G3 | 7.1 | -4.1 | 13.9 | 17.9 | sí | 68.55 | -0.55 | 109.77 | -41.77 | no | no |
| H1 | 11.1 | -8.1 | 9.9 | 13.9 | sí | 70.55 | -2.55 | 112.57 | -44.57 | no | no |
| H4 | 12.4 | -9.4 | 8.6 | 12.6 | sí | 71.45 | -3.45 | 113.83 | -45.83 | no | no |

## Recalibración térmica (secuenciado/enfriamiento, PCM candidatos)

| Candidato | Escenario | Vecino nom (C) | Margen nom (C) | Vecino peor (C) | Margen peor (C) | Nom | Peor |
|---|---|---:|---:|---:|---:|:---:|:---:|
| H3 | OMCC-sequenced writes + trench/spreader + TEC assist | 54.0 | 14.0 | 72.8 | -4.8 | sí | no |
| G3 | Duty-cycled PCM writes + isolation + TEC assist | 51.8 | 16.2 | 69.72 | -1.72 | sí | no |
| H1 | Strict OMCC sequencing + vertical/lateral isolation + manifold cooling | 49.32 | 18.68 | 63.92 | 4.08 | sí | sí |
| H4 | Aggressive sequencing + high-capacity spreading/manifold + active stabilization | 46.85 | 21.15 | 59.58 | 8.42 | sí | sí |

## Notas

- **H3**: Thermal dominated by PCM writes near rings/VO2; relies on trenches, spreading, TEC and OMCC sequencing.
- **G2**: No 300C PCM write; thermal load mainly EO/RF drivers and stabilization, manageable with spreading.
- **G3**: Localized PCM write heat co-integrated with EO; requires isolation/trenches and duty-cycled writes.
- **H1**: 3D stacking increases path/crossings and thermal density; segmented heaters, vertical/lateral isolation and strict sequencing required.
- **H4**: Highest optical path complexity and distributed thermal load; needs high-capacity spreading/cooling and active stabilization.

## Recomendaciones S1
- Refinar IL con datos de proceso (acoplos, propagación, rings/membranas/MZI) y presupuesto de ruido del receptor.
- Ejecutar FEM térmico 3D transitorio con layout real (trench, pitch, duty cycle OMCC) para validar márgenes VO2 y estabilidad de resonancias.
- Para H1/H4, co-optimizar ruta óptica (cruces/longitud) y distribución térmica (manifold/secuenciado) antes de E2/E4.
- Aplicar escenarios recalibrados (secuenciado OMCC, aislamiento, spreading/TEC/manifold) y validar duty cycle efectivo en S2/E2.
