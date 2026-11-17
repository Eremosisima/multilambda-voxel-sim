# Hoja de ruta de viabilidad — simulación primero, experimentos después

> **Objetivo:** hacer posible el objetivo OPGPU de forma abierta y reproducible: **primero con simulaciones** (cerrar presupuestos físicos y de sistema), **después con experimentos** (validar parámetros, integrar y escalar).  
> **Estado:** plan de referencia conceptual (v0.8). Basado en outputs/simulaciones del repositorio; **no son mediciones ni diseños listos para fabricación/certificación**.  
> **Modelo reproducible:** `py -3 model_feasibility_roadmap.py` → `outputs/feasibility_roadmap.*`, `figures/feasibility_scorecard_{axes,overall}.png`.

## 1. Priorización (estrategia actual)

| Prioridad | Candidato | Rol | Fortalezas clave | Principal reto |
|---|---|---|---|---|
| **P1 (ruta base)** | **H3** Open WDM-PCM (A1+G1+B3) | Abierto/factible | Pasivos dieléctricos + ref A1, NV, menor dependencia EO/RF sensible, mejor acceso abierto | Térmica en escrituras PCM y estabilización de anillos |
| **P1** | **G2** Membrana EO-sintonizada | Velocidad/BW | Reconfiguración rápida, alta densidad/BW | Capacidad NV limitada, dependencia plataforma/driver EO |
| **P1** | **G3** Membrana PCM+EO híbrida | NV + ajuste rápido | Equilibrio memoria NV y sintonía rápida, buena densidad | Calor localizado PCM (300 °C) con co-integración EO |
| **P1** | **H1** Membrane-Brush NV 3D (A1+G3+3D) | Capacidad volumétrica NV | Alta capacidad/huella por función en 3D | Alineación/yield 3D y extracción de calor (secuenciado, spreader/manifold) |
| **P1** | **H4** Tensor volumétrico (G2/G3+F2+A1) | Techo de capacidad | Máximo throughput/capacidad potencial | Integración/térmica/alineación muy exigentes y sensibilidad FTO |

> Mantener modularidad e interfaces comunes (óptica/eléctrica/térmica/control OMCC) y aislamiento por candidato/bloque (ver `CANDIDATE_REPOS_STRATEGY.md`, `candidates/`).

## 2. Scorecard de viabilidad (consolidado, heurístico 0–1)

Fuente: `outputs/feasibility_roadmap_scorecard.csv`, `outputs/feasibility_roadmap.json` (consolida `objective_combo_analysis.json`, `manufacturable_dimensions.json`, contexto P1–P3/sistema).

| Candidato | Scorecard | Óptica | Memoria M0–M3 | Térmica/control | Fabricabilidad | Yield/empaque/3D | PCIe/OpenCL/OpenVINO | Coste/acceso | Riesgo FTO/mod. | TOPS bal. | Mem (MB) | BW (TB/s) | Huella edge |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **H3** Open WDM-PCM | **0.676** | 0.65 | 0.70 | 0.60 | 0.65 | 0.75 | 0.55 | 0.80 | 0.80 | 3.47 | 160 | 1.6 | ~8.5×8.5 cm |
| **G2** Membrana EO | **0.656** | 0.75 | 0.45 | 0.75 | 0.70 | 0.80 | 0.55 | 0.55 | 0.55 | 5.42 | 192 | 3.2 | ~7.4×7.4 cm |
| **G3** Membrana PCM+EO | **0.630** | 0.72 | 0.75 | 0.55 | 0.60 | 0.70 | 0.55 | 0.55 | 0.60 | 5.25 | 256 | 2.8 | ~7.7×7.7 cm |
| **H1** Membrane-Brush NV 3D | **0.531** | 0.70 | 0.85 | 0.45 | 0.40 | 0.35 | 0.50 | 0.45 | 0.55 | 8.17 | 640 | 2.6 | ~6.6×6.6 cm |
| **H4** Tensor volumétrico 3D | **0.484** | 0.78 | 0.85 | 0.35 | 0.35 | 0.30 | 0.45 | 0.35 | 0.40 | 9.49 | 720 | 3.5 | ~6.0×6.0 cm |

Figuras: `figures/feasibility_scorecard_axes.png`, `figures/feasibility_scorecard_overall.png`.

**Lectura:** H3 ofrece la mejor viabilidad integrada (acceso/coste, modularidad, 2.5D) como base de cierre de riesgos; G2/G3 aportan rendimiento/memoria con retos de EO/térmica PCM; H1/H4 maximizan capacidad/compacidad potencial pero requieren madurar térmica 3D, yield y empaquetado.

## 3. Fase A — Simulaciones (hacer posible el objetivo)

Condición habilitante transversal: **control térmico factible** (PCM ~300 °C local, VO₂ < 68 °C, spreading/TEC/trincheras y secuenciado OMCC) coherente con dimensiones fabricables.

| ID | Hito de simulación | Candidatos | Qué cerrar (salidas) | Criterio de salida | Scripts/modelos base |
|---|---|---|---|---|---|
| **S1** | Presupuestos óptico/térmico/enlace | H3,G2,G3,H1,H4 | IL/pérdidas, fase/SNR por ruta (G1/G2/G3/A1/B3), potencia láser/detectores, térmica 3D transitoria (300 °C/68 °C, EO/rings), márgenes vs fabricable | Márgenes positivos nominal/peor-caso; pitch/aislamiento coherentes | `model_min_dimensions.py`, `model_manufacturable_dimensions.py`, `model_pcm_multilevel.py`, `model_thermal_brush.py`, `spectral_beer_lambert.py`, `snr_budget.py`, `mzi_sim.py`, `crosstalk.py` |
| **S2** | Rendimiento sistema y memoria M0–M3/OMCC | H3 (base), G2/G3, H1/H4 | TOPS efectivos, utilización, BW, latencia E2E, persistencia de pesos, refresco M2, scheduling térmico/arbitraje por perfil GPU/NPU/TPU-OpenCL | Objetivos edge/ws/dc cumplidos o brechas cuantificadas | `simulate_opgpu_system.py`, `model_reliability_p2.py`, `model_variability_p3.py` |
| **S3** | Electrónica/software (PCIe/OpenCL/OpenVINO) | Plataforma común + módulos | Latencia/BW borde (PCIe/DMA/MSI-X, colas), coste microsecuencias, partición/cobertura de ops, cuantización/calibración y precisión analógica; ruta OpenVINO (heterogénea/plugin) | Ruta OpenCL Nivel 1→2 y demo OpenVINO (C/D) viable en simulación funcional | `simulate_opgpu_system.py`, modelos de colas/BW; diseño `hardware/pcie-bridge-opencl-openvino.md` |
| **S4** | Fiabilidad, variabilidad y yield | H3,G2,G3 (2.5D), H1,H4 (3D) | Monte Carlo de proceso (n,d,acoplos,fase,térmica), deriva, endurance/retención, ECC/RAS, redundancia; yield funcional vs overhead | Yield modelado aceptable para prototipo de laboratorio y ruta de mejora | `sensitivity.py`, `robustness_extended.py`, `scaling_robustness.py`, `model_reliability_p2.py`, `model_variability_p3.py`, `model_feasibility_roadmap.py` |

**Extensiones de simulación recomendadas (próximas iteraciones):** FDTD/EM de membranas MZI/ring (parámetros n·d, acoplo), FEM térmico 3D por candidato (peores casos de co-ubicación y duty cycle), modelo de enlace E/O-O/E con ruido y cuantización, y simulador funcional de runtime/ICD+plugin OpenVINO sobre trazas de kernels (GEMM/conv/atención).

## 4. Fase B — Experimentos (después de cerrar simulaciones)

| ID | Experimento | Candidatos | Mediciones/salidas | Criterio de salida |
|---|---|---|---|---|
| **E1** | Celdas y materiales (PoC) | G1→B3/A1→G2/G3 | n, Δn, IL, ER, velocidad, energía, ciclos, retención, dependencia térmica | Parámetros medidos dentro de rangos de S1–S4 o modelo recalibrado |
| **E2** | Integración 2.5D y control térmico | H3, G3 | Mapas térmicos medidos, estabilidad, eye/SNR, consumo, repetibilidad; secuenciado OMCC | Operación estable bajo perfiles de escritura/reconfiguración |
| **E3** | Borde electrónico y enlace de sistema | Plataforma común | Bring-up PCIe/DMA/MSI-X (FPGA), cadena E/O-O/E, latencia E2E, kernel GEMM/conv, demo OpenVINO heterogénea | Ejecución E2E correcta con telemetría y exactitud reportada |
| **E4** | Módulo integrado y escalado 3D | H3/G3 → H1/H4 | TOPS/W, capacidad, estabilidad a largo plazo, yield, empaquetado/térmica | Viabilidad demostrada para clase objetivo (edge/ws) con datos reproducibles |

## 5. Secuencia recomendada

1. **H3** como vía de menor riesgo para cerrar **S1–S4** y **E1–E3** (pasivos + referencia A1, 2.5D, control térmico acotado).  
2. **G3/G2** en paralelo para madurar NV+ajuste y ruta EO de alta velocidad (dependencias EO/RF aisladas modularmente).  
3. **H1/H4** tras validar térmica 3D, yield y empaquetado (térmica 3D y alineación como precondición de **E4**).  
4. Mantener interfaces comunes y repos/candidatos modulares para que bloqueos/C&D afecten solo al bloque/candidato implicado.

## 6. Artefactos y referencias

- **Roadmap (reproducible):** `model_feasibility_roadmap.py`, `outputs/feasibility_roadmap.{md,json}`, `outputs/feasibility_roadmap_scorecard.csv`, `figures/feasibility_scorecard_{axes,overall}.png`
- **Comparativas y dimensiones:** `outputs/objective_combo_analysis.*`, `outputs/families_dev_comparison.*`, `outputs/min_dimensions.*`, `outputs/manufacturable_dimensions.*`, `outputs/ai_module_size_estimates.csv`
- **Sistema y fiabilidad:** `outputs/opgpu_system_*`, `outputs/pcm_multilevel_*`, `outputs/thermal_brush_*`, `outputs/reliability_*`, `outputs/p3_*`
- **Diseño/estrategia:** `hardware/current-strategies-schematics-and-instructions.md`, `hardware/pcie-bridge-opencl-openvino.md`, `hardware/manufacturable-dimensions-and-ai-accelerators.md`, `hardware/optical-memory-hierarchy-l1l2l3.md`, `CANDIDATE_REPOS_STRATEGY.md`
- **Dominio público (propuesta):** `PUBLIC_DOMAIN_DEDICATION.md`

*Documento conceptual de planificación; requiere recalibración con resultados de simulación y experimentación. No constituye asesoría legal ni garantiza FTO/rendimiento.*