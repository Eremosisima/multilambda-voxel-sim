# Co-optimización duty ↔ throughput ↔ endurance por perfil (conceptual)

> Integra límites de duty térmico (S1), objetivos de perfil (S2) y restricciones de escritura/endurance. Modelo simplificado.

## Puntos recomendados por candidato/perfil

| Candidato | Perfil | Patrón recomendado | Duty alcanzable | Factor perf. | Endurance 5y OK | Score | Recomendación |
|---|---|---|---:|---:|:---:|---:|---|
| H3 | edge | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H3 | ws | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H3 | dc | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| G3 | edge | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| G3 | ws | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| G3 | dc | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| G2 | edge | inference_static | 0.001 | 1.0 | sí | 1.0 | ok |
| G2 | ws | inference_static | 0.001 | 1.0 | sí | 1.0 | ok |
| G2 | dc | inference_static | 0.001 | 1.0 | sí | 1.0 | ok |
| H1 | edge | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H1 | ws | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H1 | dc | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H4 | edge | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H4 | ws | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |
| H4 | dc | inference_static | 0.001 | 1.0 | no | 0.79 | redesign/wear-level |

## Lectura
- Patrones **inference_static/periodic_update** son los más compatibles con PCM (H3/G3/H1/H4) bajo límites térmicos y endurance; **adaptive/continuous_learning** requieren throttling, particionado térmico o mayor wear-leveling.
- G2 favorece reconfiguración frecuente pero necesita refresco/buffer por retención; H4 ofrece mayor cap de duty peor-caso entre PCM en este modelo.
- Diseñar para operación weight-stationary y minimizar escrituras en hot-cells (OMCC wear-leveling/re-mapeo).
