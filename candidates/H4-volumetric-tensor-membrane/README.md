# H4 — Volumetric Tensor Membrane (G2/G3 + F2 + A1)

> Candidato prioritario **P1 (techo de capacidad, alto riesgo → aislar)**. Repositorio independiente: puede retirarse sin afectar otros candidatos.

## Resumen
Combina **cores de membrana apilada (G2/G3)** en 3D + etapa **difractiva/metasuperficie (F2)** para mezcla global + **A1 (PCM NV)** donde convenga. Apunta al **máximo de capacidad y throughput** (volumétrico + espacial + WDM) con mayor complejidad.

## Métricas objetivas (conceptuales, v0.8)
| Métrica | Valor |
|---|---:|
| Throughput | 10.0 TOPS/tile |
| Memoria NV efectiva | 720 MB/módulo |
| Ancho de banda | 3.5 TB/s |
| Latencia inferencia / reconfig | 8 ps / 5e-10 s |
| Coste (idx / unidad est.) | 3.00 / $12,000 |
| Factibilidad / fiabilidad | 1/5 / 0.487 |
| Overall objetivo | 0.674 |
| **Balanced eff. TOPS** | **9.49** (9.98 / 11.50 / 7.00) |
| TOPS/cm³ / MB/cm³ | 0.111 / 8.00 |
| Pareto | precio-rendimiento vs capacidad; factibilidad vs velocidad; acceso-abierto vs capacidad |
| Sensibilidad P(top5) | **0.905** (μ rank 3.12, robusto en ranking) |

## Fortalezas
- **Techo de capacidad/throughput** y mejor desempeño balanceado por escenarios; liderazgo en capacidad bruta y densidad de memoria.

## Riesgos y compromisos
- **Baja factibilidad**, alto coste y complejidad (alineación, integración difractiva+3D, control térmico/fase).
- Múltiples bloques con potencial sensibilidad FTO (EO/difractivo) → aislamiento recomendado.

## Licencias
Apache-2.0, CERN-OHL-S v2, CC BY-SA 4.0. Ver `IP_AND_OPEN_HW.md`.

## Estado
Conceptual / exploratorio de alto rendimiento. Ver `DESIGN.md`, `metrics.json`. Repo independiente para contención de riesgo.