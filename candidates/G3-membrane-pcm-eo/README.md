# G3 — Thin-film Membrane Stack (PCM + EO hybrid)

> Candidato prioritario **P1 (equilibrio NV + velocidad)**. Repositorio independiente para aislamiento.

## Resumen
Membranas/cavidades apiladas de película delgada donde la interferencia por espesor óptico $n d$ define canales/pesos: **PCM** aporta retención no volátil (estado base) y **EO** permite ajuste/reconfiguración rápida de índice. Alta densidad volumétrica con equilibrio entre capacidad NV y velocidad.

## Métricas objetivas (conceptuales, v0.8)
| Métrica | Valor |
|---|---:|
| Throughput | 5.0 TOPS/tile |
| Memoria NV efectiva | 256 MB/módulo |
| Ancho de banda | 2.8 TB/s |
| Latencia inferencia / reconfig | 4 ps / 5e-10 s |
| Coste (idx / unidad est.) | 1.75 / $5,800 |
| Factibilidad / fiabilidad | 2/5 / 0.487 |
| Overall objetivo | 0.676 |
| Balanced eff. TOPS | 5.25 (4.99 / 5.75 / 5.00) |
| TOPS/cm³ / MB/cm³ | 0.156 / 8.00 |
| Sensibilidad P(top5) | **0.915** (μ rank 3.06, robusto) |

## Fortalezas
- **Equilibrio NV + velocidad** y alta densidad de memoria/volumen (8.0 MB/cm³).
- Robusto bajo sensibilidad ±30%; fuerte en escenario dinámico.
- Capa PCM y capa EO separables (sustituibilidad).

## Riesgos y compromisos
- Fiabilidad/endurance media (PCM/ciclos) y complejidad de integración de materiales; dependencia EO con implicaciones FTO.
- Conceptual/no validado.

## Licencias
Apache-2.0 (código), CERN-OHL-S v2 (hardware), CC BY-SA 4.0 (docs). Ver `IP_AND_OPEN_HW.md`.

## Estado
Conceptual / investigación abierta. Ver `DESIGN.md`, `metrics.json`.