# S3 — Simulación funcional de runtime sobre trazas (partición/fallback, colas, copias)

> Conceptual (sin trazas reales de driver/RTL). Extiende S3 con secuencias de operadores, partición por ruta A–D y scheduling por colas/batching/DMA.

## Resumen (mejores configs por traza)

| Traza | Horizonte | Mejor ruta | Cola | Cobertura offload | Fallback (ms) | E2E (ms) |
|---|---|---|---|---:|---:|---:|
| CNN_inference_trace | near_term | D Blobs precompilados | batched | 0.6375 | 1.0445 | 2.3302 |
| CNN_inference_trace | target | A Plugin nativo (maduro objetivo) | batched | 0.8075 | 0.4263 | 2.0863 |
| MLP_classifier_trace | near_term | D Blobs precompilados | batched | 0.6562 | 0.3713 | 0.8626 |
| MLP_classifier_trace | target | A Plugin nativo (maduro objetivo) | batched | 0.8313 | 0.1144 | 0.7564 |
| Transformer_block_trace | near_term | D Blobs precompilados | batched | 0.5 | 2.4503 | 3.9446 |
| Transformer_block_trace | target | A Plugin nativo (maduro objetivo) | batched | 0.6333 | 1.8647 | 3.7297 |

## Lectura
- CNN/MLP logran menor E2E y mayor cobertura efectiva en C/D (corto plazo) y mejor aún en A/B; Transformer mantiene mayor fracción en fallback (softmax/norm/attention) y se beneficia de batching/pipelining.
- Colas profundas + batching + coalescing reducen espera relativa; el coste H2D/D2H y fallback dominan cuando la partición es incompleta.
- Validar con grafos OpenVINO reales y trazas FPGA/driver para latencias y contención reales.
