# H3 — Open WDM-PCM (A1 + G1 + B3)

> Candidato prioritario **P1 (abierto/factible, corto plazo)** del programa Open Photonic GPU. Repositorio independiente para aislamiento: si este proyecto requiere retiro (p. ej. C&D), los demás candidatos continúan.

## Resumen
Combinación de **pesos/cómputo PCM-MZI (A1, referencia)** + **membranas/filtros de película delgada de espesor fijo (G1, pasivos)** + **banco resonante/WDM (B3)**. Usa interferencia constructiva/destructiva por espesor óptico $n d$ en elementos pasivos y cómputo interferométrico coherente para lograr **buena capacidad NV con la mayor factibilidad y menor coste relativo** entre los híbridos.

## Métricas objetivas (conceptuales, `objective_combo_analysis`, v0.8)
| Métrica | Valor |
|---|---:|
| Throughput | 3.5 TOPS/tile |
| Memoria NV efectiva | 160 MB/módulo |
| Ancho de banda | 1.6 TB/s |
| Latencia inferencia / reconfig | 18 ps / 2e-5 s (PCM, lenta) |
| Coste (idx / unidad est.) | 1.40 / $3,600 |
| Factibilidad / fiabilidad | 3/5 / 0.425 |
| Overall objetivo | 0.574 |
| **Acceso abierto (fact+precio)** | **0.906** (líder entre híbridos) |
| TOPS/cm³ / MB/cm³ | 0.088 / 4.00 |
| Eff. estático / dinámico / mem-bound / balanced | 3.48 / 3.94 / 2.98 / 3.47 TOPS |
| Sensibilidad P(top5) | 0.21 (μ rank 7.01) — penaliza velocidad, pero destaca en factibilidad/precio |

## Fortalezas
- **Máxima factibilidad y perfil abierto/accesible:** predominio de elementos pasivos dieléctricos estándar (SiN/SiO₂/TiO₂, etc.) + diseño de referencia A1.
- **Memoria no volátil y ruta incremental** desde la arquitectura base; buena capacidad por WDM/apilado pasivo.
- **Menor superficie de dependencia** en bloques EO/RF propietarios frente a alternativas de alta velocidad.

## Riesgos y compromisos
- Reconfiguración lenta (PCM) y menor agilidad dinámica; rendimiento sujeto a tolerancias de fabricación pasiva.
- Resultados **conceptuales/simulados**, no medidos ni listos para fabricación.

## Composición y bloques sustituibles
- A1: malla MZI + pesos Sb₂S₃ (NV). B3: resonadores/rings WDM. G1: membranas/filtros de espesor fijo (interferencia por $n d$).
- Interfaces modulares (óptico/térmico/control OMCC) permiten sustituir resonadores o materiales de capa.

## Licencias
- Código: Apache-2.0 (`LICENSE`)
- Hardware/diseños: CERN-OHL-S v2 (`LICENSE-HARDWARE`)
- Documentación: CC BY-SA 4.0 (`LICENSE-docs`)
- Ver `NOTICE`, `AI_AUTHORSHIP_NOTE.md`, `IP_AND_OPEN_HW.md`.

## Estado
**Conceptual / investigación abierta.** No es un producto ni un diseño validado. Ver `DESIGN.md` y `metrics.json`.