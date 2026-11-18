# Trazas OpenVINO más realistas y políticas de memoria (conceptual)

> Extiende S3 con secuencias tipo ResNet50/BERT/MLP/ViT, reutilización y políticas de colocación de memoria (host, pesos residentes, tiling, pipeline on-device).

## Mejores resultados por traza

| Traza | Horizonte | Mejor ruta | Mejor política memoria | Cobertura | Copias (ms) | E2E (ms) |
|---|---|---|---|---:|---:|---:|
| ResNet50_infer | near_term | D Blobs precompilados | full_on_device_pipeline | 0.6038 | 0.3817 | 5.1238 |
| ResNet50_infer | target | A Plugin nativo (maduro objetivo) | full_on_device_pipeline | 0.7648 | 0.381 | 4.4876 |
| BERT_base_block | near_term | D Blobs precompilados | full_on_device_pipeline | 0.5667 | 0.5206 | 6.2556 |
| BERT_base_block | target | A Plugin nativo (maduro objetivo) | full_on_device_pipeline | 0.7178 | 0.5179 | 5.7577 |
| MLP_recommender | near_term | D Blobs precompilados | full_on_device_pipeline | 0.6429 | 0.1141 | 1.6477 |
| MLP_recommender | target | A Plugin nativo (maduro objetivo) | full_on_device_pipeline | 0.8143 | 0.1135 | 1.4207 |
| ViT_patch_head | near_term | D Blobs precompilados | full_on_device_pipeline | 0.5625 | 0.4666 | 5.2244 |
| ViT_patch_head | target | A Plugin nativo (maduro objetivo) | full_on_device_pipeline | 0.7125 | 0.4666 | 4.8004 |

## Lectura
- Políticas con pesos residentes/tiling/pipeline on-device reducen copias H2D/D2H y E2E, especialmente en CNN/MLP; Transformer sigue penalizado por fallback en atención/softmax/norm.
- La memoria NV (PCM, M1/M3) favorece `device_resident_weights` y reduce tráfico PCIe; requiere gestión de coherencia y actualización térmicamente limitada.
- Calibrar con grafos IR reales, tamaños de tensores, layout DMA y mapa de memoria M0–M3/host.
