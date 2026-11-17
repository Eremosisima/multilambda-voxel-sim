# H1 — Membrane-Brush NV (A1 + G3 + 3D cepillo)

> Candidato prioritario **P1 (escalado volumétrico NV)**. Repositorio independiente para aislamiento.

## Resumen
Combina **A1 (MZI PCM NV)** + **G3 (membranas PCM+EO, interferencia por $n d$)** en arquitectura **3D tipo cepillo**. Orientado a **alta capacidad NV y densidad volumétrica** con modularidad de bloques.

## Métricas objetivas (conceptuales, v0.8)
| Métrica | Valor |
|---|---:|
| Throughput | 9.0 TOPS/tile |
| Memoria NV efectiva | 640 MB/módulo |
| Ancho de banda | 2.6 TB/s |
| Latencia inferencia / reconfig | 12 ps / 1e-09 s |
| Coste (idx / unidad est.) | 2.30 / $9,800 |
| Factibilidad / fiabilidad | 2/5 / 0.487 |
| Overall objetivo | 0.679 |
| Balanced eff. TOPS | 8.17 (8.97 / 10.35 / 5.20) |
| TOPS/cm³ / MB/cm³ | 0.090 / 6.40 |
| Pareto | precio-rendimiento vs capacidad; factibilidad vs velocidad; acceso-abierto vs capacidad |
| Sensibilidad P(top5) | **0.93** (μ rank 2.98, robusto) |

## Fortalezas
- Alta capacidad NV y throughput efectivo en escenarios estático/dinámico; fuerte en Pareto de capacidad.
- Modular (A1/G3/3D como bloques), buen candidato de escalado si se resuelve integración.

## Riesgos y compromisos
- Integración 3D/empaquetado complejos, tolerancias térmicas/fase, coste y área de tile elevada.
- Conceptual/no validado.

## Licencias
Apache-2.0, CERN-OHL-S v2, CC BY-SA 4.0. Ver `IP_AND_OPEN_HW.md`.

## Estado
Conceptual / investigación abierta. Ver `DESIGN.md`, `metrics.json`.