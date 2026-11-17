# S3 — PCIe/E2E latencia y ruta de compatibilidad OpenVINO (conceptual)

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
- Priorizar ruta **C/D** para demo funcional temprana (GEMM/Conv) y evolucionar a **B/A** según madurez de ICD/compilador.
- Modelar colas reales (doorbells, MSI-X, batching) y contención DMA en `simulate_opgpu_system.py` para perfiles edge/ws/dc.
- Definir flujo de cuantización/calibración y métricas de exactitud vs referencia para cargas OpenVINO.
