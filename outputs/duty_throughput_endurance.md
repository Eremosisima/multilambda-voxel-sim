# Co-optimización duty ↔ throughput ↔ endurance por perfil (conceptual, weight-stationary)

> Integra límites de duty térmico (S1), objetivos (S2) y endurance con fracción de celdas reescritas por evento (mapeo weight-stationary). Modelo simplificado.

## Puntos recomendados por candidato/perfil

| Candidato | Perfil | Patrón recomendado | Duty alcanzable | Fracción reescrita | Factor perf. | Endurance 5y OK | Score | Recomendación |
|---|---|---|---:|---:|---:|:---:|---:|---|
| H3 | edge | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H3 | ws | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H3 | dc | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| G3 | edge | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| G3 | ws | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| G3 | dc | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| G2 | edge | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| G2 | ws | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| G2 | dc | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H1 | edge | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H1 | ws | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H1 | dc | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H4 | edge | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H4 | ws | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |
| H4 | dc | weight_stationary_inference | 0.0001 | 0.0005 | 1.0 | sí | 1.0 | ok |

## Resumen por patrón (ejemplos)

| Candidato | Perfil | Patrón | Duty | Rewrites 5y | Margen vida | Endurance OK |
|---|---|---|---:|---:|---:|:---:|
| H3 | ws | weight_stationary_inference | 0.0001 | 78.84 | 634195.8397 | sí |
| H3 | ws | periodic_update | 0.02 | 31540000.0 | 1.5855 | sí |
| H3 | ws | continuous_learning | 0.12 | 23650000000.0 | 0.0021 | no |
| G3 | ws | weight_stationary_inference | 0.0001 | 78.84 | 634195.8397 | sí |
| G3 | ws | periodic_update | 0.02 | 31540000.0 | 1.5855 | sí |
| G3 | ws | continuous_learning | 0.12 | 23650000000.0 | 0.0021 | no |
| G2 | ws | weight_stationary_inference | 0.0001 | 78.84 | 6341958396752.916 | sí |
| G2 | ws | periodic_update | 0.02 | 31540000.0 | 15854895.9919 | sí |
| G2 | ws | continuous_learning | 0.2 | 39420000000.0 | 12683.9168 | sí |
| H1 | ws | weight_stationary_inference | 0.0001 | 78.84 | 317097.9198 | sí |
| H1 | ws | periodic_update | 0.02 | 31540000.0 | 0.7927 | no |
| H1 | ws | continuous_learning | 0.12 | 23650000000.0 | 0.0011 | no |
| H4 | ws | weight_stationary_inference | 0.0001 | 78.84 | 317097.9198 | sí |
| H4 | ws | periodic_update | 0.02 | 31540000.0 | 0.7927 | no |
| H4 | ws | continuous_learning | 0.18 | 35480000000.0 | 0.0007 | no |

## Lectura
- Con mapeo **weight-stationary** (baja fracción de reescritura), inferencia y actualizaciones periódicas son compatibles con endurance PCM en este modelo; cargas de aprendizaje continuo/adaptativas agresivas requieren wear-leveling, particionado térmico y/o reducción de rewrites.
- G2 favorece reconfiguración frecuente (alta endurance EO) pero necesita refresco/buffer por retención; candidatos PCM exigen minimizar escrituras en hot-cells (OMCC).
- Validar con estadísticas reales de ciclado/retención y patrones de actualización de pesos por aplicación.
