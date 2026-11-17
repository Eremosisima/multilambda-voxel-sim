# G2 — Thin-film Membrane Stack (EO-tuned), Fast Core

> Candidato prioritario **P1 (líder overall / velocidad-BW)**. Repositorio independiente para aislamiento ante C&D u otros bloqueos.

## Resumen
Apilado de **membranas/cavidades de película delgada (Fabry–Pérot)** con sintonía por **índice electro-óptico (EO)**. El cómputo y la selección de canales se basan en **interferencia constructiva/destructiva por espesor óptico $n d$ y $\lambda$**, permitiendo núcleos compactos con alta velocidad, alto ancho de banda y buena densidad volumétrica.

## Métricas objetivas (conceptuales, v0.8)
| Métrica | Valor |
|---|---:|
| Throughput | 5.5 TOPS/tile |
| Memoria efectiva | 192 MB/módulo (baja NV) |
| Ancho de banda | 3.2 TB/s |
| Latencia inferencia / reconfig | 3 ps / 1e-11 s |
| Coste (idx / unidad est.) | 1.85 / $6,200 |
| Factibilidad / fiabilidad | 2/5 / 0.738 |
| **Overall objetivo** | **0.712 (top)** |
| Balanced eff. TOPS | 5.42 (estático 5.50 / dinámico 5.50 / mem-bound 5.25) |
| TOPS/cm³ / MB/cm³ | 0.183 / 6.40 |
| Sensibilidad P(top5) | **0.985** (μ rank 2.11, muy robusto) |

## Fortalezas
- **Líder overall robusto**: excelente equilibrio velocidad-capacidad-densidad en escenarios estático, dinámico y limitado por memoria.
- **Reconfiguración ultrarrápida** (EO) y alta densidad volumétrica por apilado vertical/WDM en core.
- Ideal para núcleos de cómputo dinámico/streaming compactos.

## Riesgos y compromisos
- **Memoria NV limitada**: requiere estrategia de pesos persistentes externa (emparejar con M1/A1/H3).
- Dependencia de plataformas EO (p. ej. TFLN/BTO) y control térmico/fase → **relevante para FTO y aislamiento**.
- Factibilidad media-baja; conceptual/no validado.

## Licencias
Apache-2.0 (código), CERN-OHL-S v2 (hardware), CC BY-SA 4.0 (docs). Ver `NOTICE`, `IP_AND_OPEN_HW.md`.

## Estado
Conceptual / investigación abierta. Ver `DESIGN.md`, `metrics.json`. Repo independiente para retiro aislado si fuera necesario.