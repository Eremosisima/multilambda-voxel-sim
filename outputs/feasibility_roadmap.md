# Hoja de ruta de viabilidad (simulación primero, luego experimentos)

> Generado: 2026-11-17T18:01:02.630704+00:00 (UTC). Consolidación conceptual basada en outputs del repositorio; no mediciones.

## 1. Prioridad y objetivo

Candidatos priorizados (estrategia actual): **H3** (abierto/factible), **G2** (velocidad/BW), **G3** (NV+ajuste equilibrado), **H1** (NV volumétrico), **H4** (techo de capacidad).
Objetivo: alcanzar viabilidad demostrable por clase (edge/workstation/datacenter) mediante simulaciones que cierren presupuestos físicos y de sistema, y derivar experimentos específicos.

## 2. Scorecard de viabilidad (0–1, heurístico)

| Candidato | Nombre | Scorecard | Óptica/cómputo | Memoria M0-M3 | Térmica/control | Fabricabilidad | Yield/empaque/3D | PCIe/OpenCL/OpenVINO | Coste/acceso | Riesgo FTO/mod. | TOPS bal. | Mem (MB) | BW (TB/s) | Área celda (µm²) | Huella edge | Huella ws |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H3 | Open WDM-PCM (A1+G1+B3) | 0.676 | 0.65 | 0.7 | 0.6 | 0.65 | 0.75 | 0.55 | 0.8 | 0.8 | 3.47 | 160 | 1.6 | 1738.0 | ~8.5 x 8.5 (2D equiv.) | ~20.8 x 20.8 (2D equiv.) |
| G2 | Thin-film membrane stack (EO-tuned) | 0.656 | 0.75 | 0.45 | 0.75 | 0.7 | 0.8 | 0.55 | 0.55 | 0.55 | 5.4159 | 192 | 3.2 | 176.0 | ~7.4 x 7.4 (2D equiv.) | ~18.0 x 18.0 (2D equiv.) |
| G3 | Thin-film membrane stack (PCM+EO hybrid) | 0.630 | 0.72 | 0.75 | 0.55 | 0.6 | 0.7 | 0.55 | 0.55 | 0.6 | 5.248 | 256 | 2.8 | 299.0 | ~7.7 x 7.7 (2D equiv.) | ~18.8 x 18.8 (2D equiv.) |
| H1 | Membrane-Brush NV (A1+G3+3D) | 0.531 | 0.7 | 0.85 | 0.45 | 0.4 | 0.35 | 0.5 | 0.45 | 0.55 | 8.1727 | 640 | 2.6 | 484 | ~6.6 x 6.6 (2D equiv.) | ~16.1 x 16.1 (2D equiv.) |
| H4 | Volumetric Tensor Membrane (G2/G3+F2+A1) | 0.483 | 0.78 | 0.85 | 0.35 | 0.35 | 0.3 | 0.45 | 0.35 | 0.4 | 9.4921 | 720 | 3.5 | 400 | ~6.0 x 6.0 (2D equiv.) | ~14.7 x 14.7 (2D equiv.) |

## 3. Hitos de simulación (primero) y experimentos (después)

### S1 — Presupuestos óptico/térmico/enlace por candidato (Simulación (ahora))
- **Candidatos:** H3,G2,G3,H1,H4
- **Descripción:** Modelo de pérdidas/IL, fase y SNR por ruta (G1/G2/G3/A1/B3), presupuesto de potencia láser/detectores, mapa térmico 3D transitorio (escritura PCM 300C, VO2 <68C, drivers EO/rings), y márgenes vs dimensiones fabricables.
- **Salidas:** tablas de margen (dB, °C), sensibilidades, puntos de operación seguros
- **Criterio de salida:** Márgenes positivos en casos nominal y peor-caso paramétrico; pitch/aislamiento coherentes con fabricable

### S2 — Rendimiento sistema y memoria (M0-M3/OMCC) (Simulación (ahora))
- **Candidatos:** H3 (base), G2/G3, H1/H4
- **Descripción:** Extender simulate_opgpu_system y modelos de jerarquía: throughput efectivo bajo colas DMA/PCIe, latencia E2E, persistencia de pesos, refresco M2, políticas de scheduling térmico y arbitraje OMCC por perfil (GPU/NPU/TPU, OpenCL).
- **Salidas:** TOPS efectivos, utilización, BW, contención térmica, escenarios edge/ws/dc
- **Criterio de salida:** Cumplimiento de objetivos de clase (edge/ws/dc) dentro de incertidumbre modelada o brechas cuantificadas

### S3 — Compatibilidad electrónica y software (PCIe/OpenCL/OpenVINO) (Simulación (ahora))
- **Candidatos:** Plataforma común + módulos
- **Descripción:** Modelar latencia/ancho de banda del borde (PCIe/DMA/MSI-X, colas), coste de microsecuencias y partición de kernels; definir cobertura de operadores y cuantización/calibración para precisión analógica (ruta OpenVINO heterogénea/plugin).
- **Salidas:** presupuesto de latencia E2E, mapa de ops soportadas/fallback, requisitos de ICD/plugin
- **Criterio de salida:** Ruta Nivel 1→2 OpenCL y demo OpenVINO (C/D) viable en simulación funcional

### S4 — Fiabilidad, variabilidad y yield (Simulación (ahora))
- **Candidatos:** H3,G2,G3 (2.5D) y H1,H4 (3D)
- **Descripción:** Monte Carlo de variaciones de proceso (n, d, acoplos, fase, térmica), deriva, endurance/retención, ECC/RAS y redundancia; estimar rendimiento funcional vs overhead (handicap fabricable).
- **Salidas:** distribuciones de rendimiento, tasas de fallo, políticas de calibración/RAS
- **Criterio de salida:** Yield modelado aceptable para prototipo de laboratorio y ruta de mejora definida

### E1 — Celdas y materiales (prueba de concepto) (Experimentos (posterior))
- **Candidatos:** G1→B3/A1→G2/G3
- **Descripción:** Caracterizar elementos unitarios: membranas λ/4n (G1), sintonía EO (G2), conmutación/escritura PCM y retención (A1/G3), anillos WDM (B3), pérdidas y estabilidad térmica.
- **Salidas:** n, Δn, IL, ER, velocidad, energía, ciclos, retención, dependencia térmica
- **Criterio de salida:** Parámetros medidos dentro de rangos usados en S1-S4 o modelo actualizado

### E2 — Integración 2.5D y control térmico (Experimentos (posterior))
- **Candidatos:** H3, G3
- **Descripción:** Prototipo de submódulo (p. ej. H3 o G3) con actuadores térmicos/EO, sensado y secuenciado OMCC; validar aislamiento 300C/68C, calibración y RAS básico.
- **Salidas:** mapas térmicos medidos, estabilidad, eye/SNR, consumo, repetibilidad
- **Criterio de salida:** Operación estable bajo perfiles de escritura/reconfiguración definidos

### E3 — Borde electrónico y enlace de sistema (Experimentos (posterior))
- **Candidatos:** Plataforma común
- **Descripción:** Bring-up PCIe/DMA/MSI-X en FPGA, cadena E/O-O/E, latencia E2E y demo de kernel (GEMM/conv) con runtime; prueba de ruta OpenVINO heterogénea.
- **Salidas:** link up, throughput/latencia medidos, exactitud funcional vs referencia
- **Criterio de salida:** Ejecución end-to-end correcta con telemetría y métricas reportadas

### E4 — Módulo integrado y escalado 3D (Experimentos (posterior))
- **Candidatos:** H3/G3 → H1/H4
- **Descripción:** Integración de candidato seleccionado (H3/G3 y, si procede, H1/H4) en módulo con empaquetado/térmica; evaluación de rendimiento, densidad y fiabilidad a escala.
- **Salidas:** TOPS/W, capacidad, estabilidad a largo plazo, yield
- **Criterio de salida:** Demostración de viabilidad para clase objetivo (edge/ws) con datos reproducibles

## 4. Recomendación de secuencia

1. **H3** como vía de menor riesgo para cerrar S1–S4 y E1–E3 (pasivos + ref A1, control térmico acotado).
2. **G3/G2** en paralelo para madurar memoria NV+ajuste y ruta EO de alta velocidad (dependencias EO/RF aisladas modularmente).
3. **H1/H4** tras validar térmica 3D, yield y empaquetado (simulación térmica 3D y de alineación como precondición de E4).
4. Mantener interfaz común (óptica/eléctrica/térmica/OMCC) y repos/candidatos modulares para aislar bloqueos.

## 5. Supuestos y limitaciones

- Consolidación conceptual basada en outputs existentes (objective, manufacturable, P1-P3, sistema); no mediciones ni diseño listo para fabricación.
- Puntajes de ejes (0-1) son heurísticos y deben recalibrarse con resultados de simulación/experimentos.
- El control térmico factible (PCM ~300C, VO2 <68C, spreading/TEC, secuenciado OMCC) es condición habilitante.
- Compatibilidad OpenCL/OpenVINO depende de madurez de runtime/compilador/ICD y de precisión analógica; PCIe/OpenCL/OpenVINO nominativos.
