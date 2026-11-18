# Pruebas de variantes de arquitectura sugeridas (basadas en S1–S4)

> Generado: 2026-11-18T00:23:28.363785Z. Validación conceptual contra salidas de simulación (no hardware). 'FAIL' = dato faltante o umbral no cumplido en modelos actuales.

## Resumen por variante

| Variante | Nombre | PASS | FAIL | Total |
|---|---|---:|---:|---:|
| V1_H3_base_2p5D | H3 2.5D base (abierta, NV) | 16 | 0 | 16 |
| V2_G3_bw_nv_2p5D | G3 2.5D BW+NV | 19 | 0 | 19 |
| V3_G2_eo_dynamic | G2 EO dinámico (sin NV PCM) | 12 | 1 | 13 |
| V4_H1_3D_partitioned | H1 3D particionado (escalado) | 16 | 0 | 16 |
| V5_H4_3D_tensor | H4 3D tensor particionado | 13 | 0 | 13 |
| V6_common_platform | Plataforma común PCIe/OpenCL heterogénea | 19 | 0 | 19 |

## V1_H3_base_2p5D — H3 2.5D base (abierta, NV)
Candidato: H3 | Perfiles: edge, ws | Layout: baseline | OV: C/D
Nota: Ruta base menor riesgo

| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |
|---|---|:---:|---:|---|---|
| S1_link | Enlace óptico factible (margen>=3dB) | PASS | 10.6 | >=3 | margen=10.6 dB, IL=10.4 dB |
| S1_thermal | Térmica nominal viable (recalibrada si aplica) | PASS | None | None | nom_ok=True, worst_ok=False |
| S1_duty | Duty peor-caso seguro > 0 para PCM (o n/a) | PASS | 0.12 | >0 si PCM | max_duty_worst=0.12 |
| S4_yield | Retención capacidad efectiva >=0.7 | PASS | 0.86 | >=0.7 | retención=0.86, yield_model=0.86 |
| S4_overhead | Overhead energía razonable (<=1.15x) | PASS | 1.061 | <=1.15 | energy_x=1.061, area+=14.0% |
| Accuracy | Exactitud proxy INT8 (CNN, closed-loop) >=0.85 | PASS | 0.9666 | >=0.85 | acc_int8=0.9666, eff_bits=4.93 |
| Reliability | Reconfig dinámica sostenible (sin throttling severo) | PASS | 1.0 | >=0.5 | duty_ach=0.08 cap=0.12 perf_factor=1.0 throttled=False |
| Fit | Ajuste perfil edge >= media | PASS | 0.796 | >=0.55 | fit=alta score=0.796 mods=3 layout=baseline |
| Fit | Ajuste perfil ws >= media | PASS | 0.776 | >=0.55 | fit=alta score=0.776 mods=7 layout=baseline |
| S3_runtime | Runtime CNN_inference_trace near-term E2E < 10ms | PASS | 2.3302 | <10ms | best=D Blobs precompilados batched e2e=2.3302ms cov=0.6375 |
| S3_runtime | Runtime MLP_classifier_trace near-term E2E < 10ms | PASS | 0.8626 | <10ms | best=D Blobs precompilados batched e2e=0.8626ms cov=0.6562 |
| Arch | NV persistente (PCM) disponible | PASS | None | None | H3 usa PCM NV para pesos/estado (M1) con control térmico por duty/layout |
| Pareto | Pareto/coste-eficiencia evaluado (edge) | PASS | None | None | pareto=True score=1.1248 tops/w=2.067 meets=True |
| Power | TOPS/W proxy (edge, TPU) > 0.1 | PASS | 0.1903 | >0.1 | tops/w=0.1903 total_w=35.596 eff_tops=6.772 |
| Pareto | Pareto/coste-eficiencia evaluado (ws) | PASS | None | None | pareto=False score=1.0844 tops/w=2.067 meets=True |
| Power | TOPS/W proxy (ws, TPU) > 0.1 | PASS | 0.1903 | >0.1 | tops/w=0.1903 total_w=83.057 eff_tops=15.803 |

## V2_G3_bw_nv_2p5D — G3 2.5D BW+NV
Candidato: G3 | Perfiles: edge, ws, dc | Layout: spread_out | OV: C/D->B/A
Nota: Mayor densidad/TOPS con NV

| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |
|---|---|:---:|---:|---|---|
| S1_link | Enlace óptico factible (margen>=3dB) | PASS | 13.9 | >=3 | margen=13.9 dB, IL=7.1 dB |
| S1_thermal | Térmica nominal viable (recalibrada si aplica) | PASS | None | None | nom_ok=True, worst_ok=False |
| S1_duty | Duty peor-caso seguro > 0 para PCM (o n/a) | PASS | 0.12 | >0 si PCM | max_duty_worst=0.12 |
| S4_yield | Retención capacidad efectiva >=0.7 | PASS | 0.89 | >=0.7 | retención=0.89, yield_model=0.89 |
| S4_overhead | Overhead energía razonable (<=1.15x) | PASS | 1.0515 | <=1.15 | energy_x=1.0515, area+=11.0% |
| Accuracy | Exactitud proxy INT8 (CNN, closed-loop) >=0.85 | PASS | 0.9765 | >=0.85 | acc_int8=0.9765, eff_bits=5.44 |
| Reliability | Reconfig dinámica sostenible (sin throttling severo) | PASS | 1.0 | >=0.5 | duty_ach=0.08 cap=0.12 perf_factor=1.0 throttled=False |
| Fit | Ajuste perfil edge >= media | PASS | 0.899 | >=0.55 | fit=alta score=0.899 mods=2 layout=compact |
| Fit | Ajuste perfil ws >= media | PASS | 0.779 | >=0.55 | fit=alta score=0.779 mods=5 layout=compact |
| Fit | Ajuste perfil dc >= media | PASS | 0.799 | >=0.55 | fit=alta score=0.799 mods=18 layout=compact |
| S3_runtime | Runtime CNN_inference_trace near-term E2E < 10ms | PASS | 2.3302 | <10ms | best=D Blobs precompilados batched e2e=2.3302ms cov=0.6375 |
| S3_runtime | Runtime MLP_classifier_trace near-term E2E < 10ms | PASS | 0.8626 | <10ms | best=D Blobs precompilados batched e2e=0.8626ms cov=0.6562 |
| Arch | Mejor densidad efectiva que H3 | PASS | None | None | G3=0.1253 vs H3=0.066 TOPS/cm² ef. |
| Pareto | Pareto/coste-eficiencia evaluado (edge) | PASS | None | None | pareto=True score=1.2207 tops/w=2.378 meets=True |
| Power | TOPS/W proxy (edge, TPU) > 0.1 | PASS | 0.2723 | >0.1 | tops/w=0.2723 total_w=24.509 eff_tops=6.675 |
| Pareto | Pareto/coste-eficiencia evaluado (ws) | PASS | None | None | pareto=True score=1.2207 tops/w=2.378 meets=True |
| Power | TOPS/W proxy (ws, TPU) > 0.1 | PASS | 0.2723 | >0.1 | tops/w=0.2723 total_w=61.273 eff_tops=16.688 |
| Pareto | Pareto/coste-eficiencia evaluado (dc) | PASS | None | None | pareto=True score=1.1873 tops/w=2.378 meets=True |
| Power | TOPS/W proxy (dc, TPU) > 0.1 | PASS | 0.2723 | >0.1 | tops/w=0.2723 total_w=220.584 eff_tops=60.075 |

## V3_G2_eo_dynamic — G2 EO dinámico (sin NV PCM)
Candidato: G2 | Perfiles: edge, ws | Layout: baseline | OV: C/D
Nota: Reconfig rápida, refresco/buffer

| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |
|---|---|:---:|---:|---|---|
| S1_link | Enlace óptico factible (margen>=3dB) | PASS | 14.3 | >=3 | margen=14.3 dB, IL=6.7 dB |
| S1_thermal | Térmica nominal viable (recalibrada si aplica) | PASS | None | None | nom_ok=True, worst_ok=True |
| S1_duty | Duty peor-caso seguro > 0 para PCM (o n/a) | PASS | 0.0 | >0 si PCM | max_duty_worst=0.0 |
| S4_yield | Datos S4 de coste disponibles | FAIL | None | required | G2 no incluido en S4 coste/overhead actual (pendiente) |
| Accuracy | Exactitud proxy INT8 (CNN, closed-loop) >=0.85 | PASS | 0.9796 | >=0.85 | acc_int8=0.9796, eff_bits=5.64 |
| Reliability | Reconfig dinámica sostenible (sin throttling severo) | PASS | 0.625 | >=0.5 | duty_ach=0.05 cap=0.05 perf_factor=0.625 throttled=True |
| Fit | Ajuste perfil edge >= media | PASS | 0.6 | >=0.55 | fit=media score=0.6 mods=None layout=baseline |
| Fit | Ajuste perfil ws >= media | PASS | 0.58 | >=0.55 | fit=media score=0.58 mods=None layout=baseline |
| S3_runtime | Runtime CNN_inference_trace near-term E2E < 10ms | PASS | 2.3302 | <10ms | best=D Blobs precompilados batched e2e=2.3302ms cov=0.6375 |
| S3_runtime | Runtime MLP_classifier_trace near-term E2E < 10ms | PASS | 0.8626 | <10ms | best=D Blobs precompilados batched e2e=0.8626ms cov=0.6562 |
| Arch | Reconfiguración rápida (clase EO) | PASS | None | None | G2: reconfig EO rápida, sin escritura PCM 300°C; requiere refresco/buffer por retención de estado rápido |
| Power | TOPS/W proxy (edge, TPU) > 0.1 | PASS | 0.3244 | >0.1 | tops/w=0.3244 total_w=23.811 eff_tops=7.723 |
| Power | TOPS/W proxy (ws, TPU) > 0.1 | PASS | 0.3244 | >0.1 | tops/w=0.3244 total_w=47.623 eff_tops=15.447 |

## V4_H1_3D_partitioned — H1 3D particionado (escalado)
Candidato: H1 | Perfiles: ws, dc | Layout: spread_out | OV: B/A+fallback
Nota: Alta capacidad, alto riesgo/controlado

| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |
|---|---|:---:|---:|---|---|
| S1_link | Enlace óptico factible (margen>=3dB) | PASS | 9.9 | >=3 | margen=9.9 dB, IL=11.1 dB |
| S1_thermal | Térmica nominal viable (recalibrada si aplica) | PASS | None | None | nom_ok=True, worst_ok=True |
| S1_duty | Duty peor-caso seguro > 0 para PCM (o n/a) | PASS | 0.12 | >0 si PCM | max_duty_worst=0.12 |
| S4_yield | Retención capacidad efectiva >=0.7 | PASS | 0.78 | >=0.7 | retención=0.78, yield_model=0.78 |
| S4_overhead | Overhead energía razonable (<=1.15x) | PASS | 1.093 | <=1.15 | energy_x=1.093, area+=22.0% |
| Accuracy | Exactitud proxy INT8 (CNN, closed-loop) >=0.85 | PASS | 0.9574 | >=0.85 | acc_int8=0.9574, eff_bits=4.58 |
| Reliability | Reconfig dinámica sostenible (sin throttling severo) | PASS | 1.0 | >=0.5 | duty_ach=0.08 cap=0.12 perf_factor=1.0 throttled=False |
| Fit | Ajuste perfil ws >= media | PASS | 0.967 | >=0.55 | fit=alta score=0.967 mods=3 layout=compact |
| Fit | Ajuste perfil dc >= media | PASS | 0.987 | >=0.55 | fit=alta score=0.987 mods=12 layout=compact |
| S3_runtime | Runtime CNN_inference_trace near-term E2E < 10ms | PASS | 2.3302 | <10ms | best=D Blobs precompilados batched e2e=2.3302ms cov=0.6375 |
| S3_runtime | Runtime MLP_classifier_trace near-term E2E < 10ms | PASS | 0.8626 | <10ms | best=D Blobs precompilados batched e2e=0.8626ms cov=0.6562 |
| Arch | Redundancia/re-mapeo reforzado para 3D | PASS | None | None | redundancia=0.22, retención=0.78 |
| Pareto | Pareto/coste-eficiencia evaluado (ws) | PASS | None | None | pareto=True score=1.1553 tops/w=2.079 meets=True |
| Power | TOPS/W proxy (ws, TPU) > 0.1 | PASS | 0.3853 | >0.1 | tops/w=0.3853 total_w=40.995 eff_tops=15.795 |
| Pareto | Pareto/coste-eficiencia evaluado (dc) | PASS | None | None | pareto=True score=1.1553 tops/w=2.079 meets=True |
| Power | TOPS/W proxy (dc, TPU) > 0.1 | PASS | 0.3853 | >0.1 | tops/w=0.3853 total_w=163.981 eff_tops=63.18 |

## V5_H4_3D_tensor — H4 3D tensor particionado
Candidato: H4 | Perfiles: dc | Layout: spread_out | OV: B/A+fallback
Nota: Techo capacidad, mayor riesgo

| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |
|---|---|:---:|---:|---|---|
| S1_link | Enlace óptico factible (margen>=3dB) | PASS | 8.6 | >=3 | margen=8.6 dB, IL=12.4 dB |
| S1_thermal | Térmica nominal viable (recalibrada si aplica) | PASS | None | None | nom_ok=True, worst_ok=True |
| S1_duty | Duty peor-caso seguro > 0 para PCM (o n/a) | PASS | 0.18 | >0 si PCM | max_duty_worst=0.18 |
| S4_yield | Retención capacidad efectiva >=0.7 | PASS | 0.7399 | >=0.7 | retención=0.7399, yield_model=0.7398 |
| S4_overhead | Overhead energía razonable (<=1.15x) | PASS | 1.109 | <=1.15 | energy_x=1.109, area+=26.0% |
| Accuracy | Exactitud proxy INT8 (CNN, closed-loop) >=0.85 | PASS | 0.9527 | >=0.85 | acc_int8=0.9527, eff_bits=4.43 |
| Reliability | Reconfig dinámica sostenible (sin throttling severo) | PASS | 1.0 | >=0.5 | duty_ach=0.08 cap=0.18 perf_factor=1.0 throttled=False |
| Fit | Ajuste perfil dc >= media | PASS | 0.982 | >=0.55 | fit=alta score=0.982 mods=11 layout=spread_out |
| S3_runtime | Runtime CNN_inference_trace near-term E2E < 10ms | PASS | 2.3302 | <10ms | best=D Blobs precompilados batched e2e=2.3302ms cov=0.6375 |
| S3_runtime | Runtime MLP_classifier_trace near-term E2E < 10ms | PASS | 0.8626 | <10ms | best=D Blobs precompilados batched e2e=0.8626ms cov=0.6562 |
| Arch | Layout spread-out recomendado para margen térmico | PASS | None | None | max_duty_worst_spread_out=0.18 |
| Pareto | Pareto/coste-eficiencia evaluado (dc) | PASS | None | None | pareto=True score=1.1308 tops/w=2.168 meets=True |
| Power | TOPS/W proxy (dc, TPU) > 0.1 | PASS | 0.4051 | >0.1 | tops/w=0.4051 total_w=150.702 eff_tops=61.042 |

## V6_common_platform — Plataforma común PCIe/OpenCL heterogénea
Candidato: H3 | Perfiles: edge, ws, dc | Layout: baseline | OV: C/D
Nota: Interfaz/modularidad común

| Categoría | Prueba | Estado | Métrica | Umbral | Detalle |
|---|---|:---:|---:|---|---|
| S1_link | Enlace óptico factible (margen>=3dB) | PASS | 10.6 | >=3 | margen=10.6 dB, IL=10.4 dB |
| S1_thermal | Térmica nominal viable (recalibrada si aplica) | PASS | None | None | nom_ok=True, worst_ok=False |
| S1_duty | Duty peor-caso seguro > 0 para PCM (o n/a) | PASS | 0.12 | >0 si PCM | max_duty_worst=0.12 |
| S4_yield | Retención capacidad efectiva >=0.7 | PASS | 0.86 | >=0.7 | retención=0.86, yield_model=0.86 |
| S4_overhead | Overhead energía razonable (<=1.15x) | PASS | 1.061 | <=1.15 | energy_x=1.061, area+=14.0% |
| Accuracy | Exactitud proxy INT8 (CNN, closed-loop) >=0.85 | PASS | 0.9666 | >=0.85 | acc_int8=0.9666, eff_bits=4.93 |
| Reliability | Reconfig dinámica sostenible (sin throttling severo) | PASS | 1.0 | >=0.5 | duty_ach=0.08 cap=0.12 perf_factor=1.0 throttled=False |
| Fit | Ajuste perfil edge >= media | PASS | 0.796 | >=0.55 | fit=alta score=0.796 mods=3 layout=baseline |
| Fit | Ajuste perfil ws >= media | PASS | 0.776 | >=0.55 | fit=alta score=0.776 mods=7 layout=baseline |
| Fit | Ajuste perfil dc >= media | PASS | 0.746 | >=0.55 | fit=media score=0.746 mods=27 layout=baseline |
| S3_runtime | Runtime CNN_inference_trace near-term E2E < 10ms | PASS | 2.3302 | <10ms | best=D Blobs precompilados batched e2e=2.3302ms cov=0.6375 |
| S3_runtime | Runtime MLP_classifier_trace near-term E2E < 10ms | PASS | 0.8626 | <10ms | best=D Blobs precompilados batched e2e=0.8626ms cov=0.6562 |
| Arch | Interfaz común y rutas OpenVINO heterogéneas definidas | PASS | None | None | Plataforma PCIe/DMA/MSI-X + ICD OpenCL común; rutas C/D iniciales con fallback, evolución a B/A |
| Pareto | Pareto/coste-eficiencia evaluado (edge) | PASS | None | None | pareto=True score=1.1248 tops/w=2.067 meets=True |
| Power | TOPS/W proxy (edge, TPU) > 0.1 | PASS | 0.1903 | >0.1 | tops/w=0.1903 total_w=35.596 eff_tops=6.772 |
| Pareto | Pareto/coste-eficiencia evaluado (ws) | PASS | None | None | pareto=False score=1.0844 tops/w=2.067 meets=True |
| Power | TOPS/W proxy (ws, TPU) > 0.1 | PASS | 0.1903 | >0.1 | tops/w=0.1903 total_w=83.057 eff_tops=15.803 |
| Pareto | Pareto/coste-eficiencia evaluado (dc) | PASS | None | None | pareto=True score=1.0631 tops/w=2.067 meets=True |
| Power | TOPS/W proxy (dc, TPU) > 0.1 | PASS | 0.1903 | >0.1 | tops/w=0.1903 total_w=320.362 eff_tops=60.953 |

## Conclusiones
- V1 (H3 2.5D) y V2 (G3 2.5D) cumplen la mayoría de pruebas funcionales/térmicas/coste en modelos actuales y son las bases recomendadas por perfil.
- V3 (G2) requiere completar S4 de coste/overhead específico, pero pasa criterios de enlace/térmico y es adecuado para reconfiguración dinámica con refresco.
- V4/V5 (3D) pasan métricas numéricas de capacidad/eficiencia tras optimización pero mantienen riesgos de integración 3D (alineación, térmica distribuida, proceso) que deben cerrarse en FEM 3D y E2–E4.
- V6 confirma la necesidad de plataforma común PCIe/OpenCL y partición heterogénea con fallback (S3).
