# Envolvente operativa integrada y sugerencias de arquitectura (S1–S4, conceptual)

> Combina S1 (enlace/térmico, duty/layout), S2 (perfiles), S3 (colas/partición OpenVINO) y S4 (yield/coste). Planificación, no mediciones ni signoff.

## Resumen por candidato y perfil

| Candidato | Perfil | Ajuste | Score | Layout | Duty máx nom | Duty máx peor | TOPS ef. módulo | Obj. TOPS | Módulos est. | Retención | Presupuesto write/reconfig | Ruta OpenVINO |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| H3 | edge | alta | 0.796 | baseline | 0.18 | 0.12 | 3.01 | 8 | 3 | 0.86 | high | C/D (heterogéneo/compilado) |
| H3 | ws | alta | 0.776 | baseline | 0.18 | 0.12 | 3.01 | 20 | 7 | 0.86 | high | C/D inicial → B/A con madurez |
| H3 | dc | media | 0.746 | baseline | 0.18 | 0.12 | 3.01 | 80 | 27 | 0.86 | high | B/A objetivo (con fallback C en subgrafos mixtos) |
| G2 | edge | media | 0.6 | baseline | 0.0 | 0.0 | 0 | 8 | None | 0 | n/a | C/D (heterogéneo/compilado) |
| G2 | ws | media | 0.58 | baseline | 0.0 | 0.0 | 0 | 20 | None | 0 | n/a | C/D inicial → B/A con madurez |
| G2 | dc | media | 0.55 | baseline | 0.0 | 0.0 | 0 | 80 | None | 0 | n/a | B/A objetivo (con fallback C en subgrafos mixtos) |
| G3 | edge | alta | 0.899 | compact | 0.18 | 0.12 | 4.45 | 8 | 2 | 0.89 | high | C/D (heterogéneo/compilado) |
| G3 | ws | alta | 0.779 | compact | 0.18 | 0.12 | 4.45 | 20 | 5 | 0.89 | high | C/D inicial → B/A con madurez |
| G3 | dc | alta | 0.799 | compact | 0.18 | 0.12 | 4.45 | 80 | 18 | 0.89 | high | B/A objetivo (con fallback C en subgrafos mixtos) |
| H1 | edge | alta | 0.837 | compact | 0.18 | 0.12 | 7.02 | 8 | 2 | 0.78 | high | C/D (heterogéneo/compilado) |
| H1 | ws | alta | 0.967 | compact | 0.18 | 0.12 | 7.02 | 20 | 3 | 0.78 | high | C/D inicial → B/A con madurez |
| H1 | dc | alta | 0.987 | compact | 0.18 | 0.12 | 7.02 | 80 | 12 | 0.78 | high | B/A objetivo (con fallback C en subgrafos mixtos) |
| H4 | edge | alta | 0.832 | spread_out | 0.25 | 0.18 | 7.399 | 8 | 2 | 0.7399 | high | C/D (heterogéneo/compilado) |
| H4 | ws | alta | 0.932 | spread_out | 0.25 | 0.18 | 7.399 | 20 | 3 | 0.7399 | high | C/D inicial → B/A con madurez |
| H4 | dc | alta | 0.982 | spread_out | 0.25 | 0.18 | 7.399 | 80 | 11 | 0.7399 | high | B/A objetivo (con fallback C en subgrafos mixtos) |

## Cobertura OpenVINO por grafo (rutas clave, S3)

| Grafo | A (nativo, objetivo) | C (heterogéneo, corto plazo) | D (compilado, corto plazo) |
|---|---:|---:|---:|
| CNN_inference | 0.8384 | 0.6178 | 0.6619 |
| Transformer_encoder_block | 0.7363 | 0.5425 | 0.5813 |
| MLP_classifier | 0.8645 | 0.637 | 0.6825 |

## Sugerencias de arquitectura basadas en cálculos

### **Base recomendada (menor riesgo, abierta): H3 2.5D (A1+G1+B3)**
Edge/workstation: 1 módulo clase H3 (3.01 TOPS ef., 138 MB ef.) cubre objetivos S2 con margen; usar layout baseline/spread-out y OMCC con duty de escritura ≤0.12 (peor caso seguro)–0.18 (nominal) para respetar VO₂. Persistencia NV en PCM + pasivos G1 favorecen acceso abierto y estabilidad; ruta OpenVINO C/D inicial.

### **Rendimiento/BW con equilibrio NV: G3 2.5D (PCM+EO)**
Cuando se requiera mayor BW/TOPS (workstation/datacenter) con NV: G3 ofrece 4.45 TOPS ef. y mejor densidad (0.125 TOPS/cm² ef.) con overhead bajo; requiere co-gestión térmica PCM/EO y layout spread-out para headroom de duty. Evolucionar a rutas B/A.

### **Reconfiguración rápida (sin NV fuerte): G2 EO**
Para cargas dinámicas donde prima velocidad de reconfiguración sobre persistencia, usar G2 con buffers/refresco M2–M3 y partición heterogénea (fallback para estado persistente si aplica).

### **Capacidad/escalado (alto riesgo controlado): H1/H4 3D**
Para datacenter/capacidad: H1/H4 alcanzan mayor TOPS/Mem efectivos por módulo tras optimización pero exigen particionado jerárquico, layout spread-out, manifold/vías térmicas, redundancia 22–26% y re-mapeo OMCC. Introducir gradualmente sobre base 2.5D validada (E2→E4).

### **Plataforma común y software**
Mantener interfaz PCIe/DMA/MSI-X + ICD OpenCL común; particionar grafos (CNN/MLP favorables en C/D, transformer con más fallback hasta madurar A/B). Usar colas profundas, batching y coalescing para sostener throughput (S3).

### **Térmica/fiabilidad (condición habilitante)**
Secuenciado OMCC y límites de duty por layout son obligatorios en candidatos PCM; co-optimizar redundancia con retención efectiva (S4) y calibración en lazo cerrado.

## Simulaciones adicionales factibles (sin mediciones nuevas)

- **FEM térmico 3D transitorio** (herramienta externa) calibrado con layout real: cerrar márgenes VO₂/rings y densidad de escritura.
- **Modelo de ruido/E/O-O/E y cuantización** acoplado a márgenes S1: estimar exactitud efectiva vs bit-depth y potencia óptica.
- **Simulador funcional de runtime OpenCL/ICD + partición de grafos reales** (trazas): validar fallback, latencia de colas y BW efectivo (extiende S3).
- **Barrido de fiabilidad temporal/endurance** con tasas de refresco M2 y write-rate limitados por duty térmico (extiende P2/S4).
- **Optimización multiobjetivo (Pareto costo/TOPS/W/retención)** usando `objective_combo_analysis` + S4 coste para selección de configuración por perfil.

