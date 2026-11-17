# S3 — PCIe/E2E, colas/DMA y compatibilidad/partición OpenVINO (conceptual)

> Modelo funcional para planificación S3. No son mediciones; validar con bring-up FPGA, trazas de driver y grafos reales.

## Latencia E2E estimada (µs)

| PCIe | Carga | H2D (µs) | Cómputo (µs) | D2H (µs) | Fijo (µs) | Solape (µs) | Total (µs) | Total (ms) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Gen3 x8 | GEMM_small | 81.92 | 100.0 | 20.48 | 6.0 | 0.0 | 208.4 | 0.2084 |
| Gen3 x8 | GEMM_large | 5242.88 | 10000.0 | 1310.72 | 6.0 | 1966.08 | 14593.52 | 14.5935 |
| Gen3 x8 | Conv_tile | 655.36 | 2500.0 | 327.68 | 6.0 | 0.0 | 3489.04 | 3.489 |
| Gen3 x8 | Attention_block_proxy | 2621.44 | 6000.0 | 655.36 | 6.0 | 983.04 | 8299.76 | 8.2998 |
| Gen3 x8 | Batched_inference_8 | 1310.72 | 4000.0 | 163.84 | 6.0 | 442.368 | 5038.192 | 5.0382 |
| Gen4 x8 | GEMM_small | 39.961 | 100.0 | 9.99 | 6.0 | 0.0 | 155.951 | 0.156 |
| Gen4 x8 | GEMM_large | 2557.502 | 10000.0 | 639.376 | 6.0 | 959.063 | 12243.815 | 12.2438 |
| Gen4 x8 | Conv_tile | 319.688 | 2500.0 | 159.844 | 6.0 | 0.0 | 2985.532 | 2.9855 |
| Gen4 x8 | Attention_block_proxy | 1278.751 | 6000.0 | 319.688 | 6.0 | 479.532 | 7124.907 | 7.1249 |
| Gen4 x8 | Batched_inference_8 | 639.376 | 4000.0 | 79.922 | 6.0 | 215.789 | 4509.508 | 4.5095 |
| Gen4 x16 | GEMM_small | 19.74 | 100.0 | 4.935 | 6.0 | 0.0 | 130.675 | 0.1307 |
| Gen4 x16 | GEMM_large | 1263.345 | 10000.0 | 315.836 | 6.0 | 473.754 | 11111.427 | 11.1114 |
| Gen4 x16 | Conv_tile | 157.918 | 2500.0 | 78.959 | 6.0 | 0.0 | 2742.877 | 2.7429 |
| Gen4 x16 | Attention_block_proxy | 631.672 | 6000.0 | 157.918 | 6.0 | 236.877 | 6558.713 | 6.5587 |
| Gen4 x16 | Batched_inference_8 | 315.836 | 4000.0 | 39.48 | 6.0 | 106.595 | 4254.721 | 4.2547 |
| Gen5 x16 | GEMM_small | 9.752 | 100.0 | 2.438 | 6.0 | 0.0 | 118.19 | 0.1182 |
| Gen5 x16 | GEMM_large | 624.152 | 10000.0 | 156.038 | 6.0 | 234.057 | 10552.133 | 10.5521 |
| Gen5 x16 | Conv_tile | 78.019 | 2500.0 | 39.01 | 6.0 | 0.0 | 2623.029 | 2.623 |
| Gen5 x16 | Attention_block_proxy | 312.076 | 6000.0 | 78.019 | 6.0 | 117.029 | 6279.067 | 6.2791 |
| Gen5 x16 | Batched_inference_8 | 156.038 | 4000.0 | 19.505 | 6.0 | 52.663 | 4128.88 | 4.1289 |

## Contención de colas/DMA (Gen4 x8, conceptual)

| Escenario | Carga | Prof. cola | Concurrencia | DMA | MSI-X | Utiliz. | Servicio eff (ms) | Espera cola (ms) | E2E est. (ms) | Throughput rel. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| single_stream | GEMM_small | 1 | 1 | 1 | 1 | 0.45 | 0.156 | 0.0638 | 0.2198 | 0.7097 |
| single_stream | GEMM_large | 1 | 1 | 1 | 1 | 0.47 | 12.244 | 5.4289 | 17.6729 | 0.6928 |
| single_stream | Conv_tile | 1 | 1 | 1 | 1 | 0.45 | 2.986 | 1.2215 | 4.2075 | 0.7097 |
| single_stream | Attention_block_proxy | 1 | 1 | 1 | 1 | 0.47 | 7.125 | 3.1592 | 10.2842 | 0.6928 |
| single_stream | Batched_inference_8 | 1 | 1 | 1 | 1 | 0.45 | 4.51 | 1.845 | 6.355 | 0.7097 |
| pipelined_stream | GEMM_small | 8 | 2 | 2 | 2 | 0.53 | 0.162 | 0.1096 | 0.2584 | 0.6036 |
| pipelined_stream | GEMM_large | 8 | 2 | 2 | 2 | 0.55 | 12.7142 | 9.3237 | 20.919 | 0.5853 |
| pipelined_stream | Conv_tile | 8 | 2 | 2 | 2 | 0.53 | 3.1007 | 2.0979 | 4.9468 | 0.6036 |
| pipelined_stream | Attention_block_proxy | 8 | 2 | 2 | 2 | 0.55 | 7.3986 | 5.4256 | 12.1732 | 0.5853 |
| pipelined_stream | Batched_inference_8 | 8 | 2 | 2 | 2 | 0.53 | 4.6832 | 3.1686 | 7.4716 | 0.6036 |
| batched_inference | GEMM_small | 16 | 4 | 2 | 4 | 0.69 | 0.2072 | 0.3689 | 0.5318 | 0.2933 |
| batched_inference | GEMM_large | 16 | 4 | 2 | 4 | 0.71 | 16.26 | 31.8472 | 44.2856 | 0.2765 |
| batched_inference | Conv_tile | 16 | 4 | 2 | 4 | 0.69 | 3.9654 | 7.061 | 10.1791 | 0.2933 |
| batched_inference | Attention_block_proxy | 16 | 4 | 2 | 4 | 0.71 | 9.462 | 18.5325 | 25.7706 | 0.2765 |
| batched_inference | Batched_inference_8 | 16 | 4 | 2 | 4 | 0.69 | 5.9893 | 10.6648 | 15.3743 | 0.2933 |
| multi_tenant | GEMM_small | 32 | 8 | 4 | 4 | 0.98 | 0.2489 | 14.638 | 13.1303 | 0.0119 |
| multi_tenant | GEMM_large | 32 | 8 | 4 | 4 | 0.98 | 19.539 | 1148.8917 | 1030.5637 | 0.0119 |
| multi_tenant | Conv_tile | 32 | 8 | 4 | 4 | 0.98 | 4.7651 | 280.1855 | 251.3283 | 0.0119 |
| multi_tenant | Attention_block_proxy | 32 | 8 | 4 | 4 | 0.98 | 11.3701 | 668.5604 | 599.7032 | 0.0119 |
| multi_tenant | Batched_inference_8 | 32 | 8 | 4 | 4 | 0.98 | 7.1971 | 423.187 | 379.6016 | 0.0119 |

## Partición/cobertura OpenVINO (grafos representativos)

| Grafo | Ruta | Cobertura offload | Fallback | Rend. relativo (proxy) | Riesgo exactitud | Recomendado (S3) |
|---|---|---:|---:|---:|---|:---:|
| CNN_inference | A Plugin nativo (maduro objetivo) | 0.8384 | 0.1616 | 0.9789 | bajo-medio | sí |
| CNN_inference | B Backend OpenCL/ICD | 0.706 | 0.294 | 0.951 | medio | sí |
| CNN_inference | C Heterogéneo OPGPU+fallback | 0.6178 | 0.3822 | 0.9009 | medio | sí |
| CNN_inference | D Blobs precompilados | 0.6619 | 0.3381 | 0.9693 | medio | sí |
| Transformer_encoder_block | A Plugin nativo (maduro objetivo) | 0.7363 | 0.2637 | 0.9656 | medio | sí |
| Transformer_encoder_block | B Backend OpenCL/ICD | 0.62 | 0.38 | 0.9367 | medio | no |
| Transformer_encoder_block | C Heterogéneo OPGPU+fallback | 0.5425 | 0.4575 | 0.8814 | medio | sí |
| Transformer_encoder_block | D Blobs precompilados | 0.5813 | 0.4187 | 0.9619 | medio | sí |
| MLP_classifier | A Plugin nativo (maduro objetivo) | 0.8645 | 0.1355 | 0.9823 | bajo-medio | sí |
| MLP_classifier | B Backend OpenCL/ICD | 0.728 | 0.272 | 0.9547 | medio | sí |
| MLP_classifier | C Heterogéneo OPGPU+fallback | 0.637 | 0.363 | 0.9059 | medio | sí |
| MLP_classifier | D Blobs precompilados | 0.6825 | 0.3175 | 0.9711 | medio | sí |

## Rutas de compatibilidad OpenVINO

| Ruta | Madurez | Cobertura objetivo | Precisión | Dependencia | Rendimiento | Fase |
|---|---|---|---|---|---|---|
| A Plugin OpenVINO nativo | medio plazo | alto (subgrafos MatMul/Conv/FC y fusiones objetivo) | INT8/FP16 calibrado + verificación de exactitud analógica | runtime/driver estable y compilador de microprogramas | mejor (control directo, tiling/fusión) | S3→E3 evolución |
| B Vía backend OpenCL de OpenVINO (ICD OPGPU) | condicionada | media (lo que genere el plugin OpenCL y soporte el compilador OPGPU) | formatos soportados por ICD + calibración | ICD OpenCL Nivel 2 suficientemente compatible | media | tras S3 Nivel 1→2 |
| C Heterogéneo (OPGPU + CPU/GPU fallback) | corto plazo | parcial en OPGPU, resto fallback | mixta; validar partición y acumulación | runtime y particionado de grafo | dependiente de partición | S3 demostración inicial |
| D Blobs/redes precompiladas | corto plazo | topologías fijas soportadas | calibración por modelo | toolchain de compilación offline | buena en casos fijos | S3/E3 demos |

## Cobertura inicial de operadores (objetivo)

| Operador | Prioridad | Estado | Rutas |
|---|---|---|---|
| MatMul/GEMM | P0 | objetivo directo (núcleo óptico) | A/B/C/D |
| Convolution | P0 | vía im2col+GEMM/tiling | A/B/C/D |
| FullyConnected | P0 | GEMM | A/B/C/D |
| Add/Mul (eltwise) | P1 | posible en dominio óptico/mixto | A/B/C |
| Activation (ReLU/GELU approx) | P1 | aprox. óptica/LUT o borde/host | A/C |
| Softmax/LayerNorm | P1 | preferente fallback o bloque mixto | C (A futuro) |
| Attention (compuesto) | P2 | descomposición (MatMul+softmax+eltwise) | C/A |
| Quantize/Dequantize | P1 | en frontera E/O-O/E y runtime | A/B/C/D |

## Recomendaciones S3
- **Corto plazo:** rutas C/D para demo funcional (GEMM/Conv/MLP, CNN con fallback) con cuantización/calibración y reporte de exactitud.
- **Evolución:** ruta B (ICD OpenCL maduro) y luego A (plugin nativo) para mayor cobertura/fusión y menor fallback en transformer/attention.
- **Colas/DMA:** usar colas profundas + batching + coalescing MSI-X y múltiples canales DMA para sostener throughput; validar contención real en FPGA/driver.
- Definir particionado de grafo y métricas de exactitud vs referencia por operador/subgrafo.
