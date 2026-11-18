# Estado de avance máximo (simulación/I+D con recursos disponibles)

> **Fecha:** 2026-11-18 (conceptual, basado en repo `main`).  
> **Alcance:** máximo avance posible en simulación/análisis/modelado con los datos, scripts y referencias públicas disponibles en este entorno (sin mediciones, sin FEM/FDTD/RTL externo, sin laboratorio).  
> **Objetivo del proyecto:** OPGPU de dominio público/arte previo (defensivo) para uso libre, con ruta S1–S4 (simulación) y E1–E4 (experimentos).

## 1. Qué se tiene (consolidado)

- **Estrategias/candidatos y diseño:** A–G, H1–H5, priorizados H3/G2/G3/H1/H4 (módulos en `candidates/`), esquemáticos/instrucciones v0.8, jerarquía M0–M3/OMCC, PCIe/OpenCL/OpenVINO, dimensiones fabricables, roadmap S1–S4/E1–E4.
- **Dominio público/arte previo:** intención CC0 1.0, avisos aplicados, divulgaciones defensivas (`DEFENSIVE_DISCLOSURES/`), plan de publicación/archivado (Zenodo/ip.com/Wayback). **Pendiente legal/acción externa:** ejecución CC0 por titulares, DOIs/IDs y envíos.
- **Versionado:** tags y releases publicados (Zenodo vinculado; DOIs por confirmar).

## 2. Simulaciones y cálculos completados (S1–S4 y extensiones)

| Bloque | Modelos/artefactos | Resultado clave (conceptual) |
|---|---|---|
| **S1 Enlace + térmica** | `model_s1_link_thermal.py`, `outputs/s1_*`, `outputs/s1_layout_duty.*`, `figures/s1_*` | Márgenes de enlace positivos; térmica PCM viable en nominal con secuenciado/aislamiento/enfriamiento; duty peor-caso seguro ~0.12 (H3/G3/H1), ~0.18 (H4 spread_out) en barrido layout/duty. FEM 3D transitorio pendiente (externo). |
| **S2 Perfiles sistema** | `model_s2_system_profiles.py`, `simulate_opgpu_system.py`, `outputs/s2_system_profiles.*`, `outputs/opgpu_system_*` | Edge/ws/dc con M0–M3/OMCC+P1; cumplimiento de objetivos por perfil condicionado a partición/colas reales (S3/E3). |
| **S3 PCIe/colas/OpenVINO** | `model_s3_pcie_openvino.py`, `model_s3_runtime_traces.py`, `model_openvino_realistic_traces.py`, `outputs/s3_*`, `outputs/openvino_realistic_traces.*` | E2E Gen4x8 ~0.16–12 ms por carga; contención mitigable con colas/batching/coalescing/DMA; partición A–D: CNN/MLP favorables en C/D, Transformer más fallback. Políticas de memoria (pesos residentes/tiling/pipeline) reducen copias/E2E. Validación con trazas IR/RTL reales pendiente. |
| **S4 Variabilidad, yield y coste** | `model_s4_variability_yield.py`, `model_s4_cost_overhead.py`, `outputs/s4_*` | H3/G3 robustos 2.5D; H1/H4 requieren particionado/redundancia/control de proceso. Capacidad efectiva con overhead: H3 3.01 TOPS (0.86), G2 4.93 (0.897), G3 4.45 (0.89), H1 7.02 (0.78), H4 7.40 (0.74). Calibración con metrología pendiente. |
| **Precisión analógica/quantización** | `model_accuracy_quantization.py`, `outputs/accuracy_quantization.*` | INT8 + calibración en lazo cerrado: proxy ~0.95–0.98 (CNN) según candidato; H1/H4 más sensibles a varianza de fase/IL. Validar con mediciones E/O-O/E y accuracy real. |
| **Deriva térmica/estabilidad** | `model_thermal_drift_stability.py`, `outputs/thermal_drift_stability.*` | Control en lazo cerrado necesario; H3 estabilizable en modelo simplificado, G3 parcial, H1/H4 exigen mayor aislamiento/control eficiente (potencia de control alta en modelo → optimizar actuadores). Calibrar con respuesta medida. |
| **Sensibilidad láser/E-O/BER** | `model_laser_eo_ber_sensitivity.py`, `outputs/laser_eo_ber_sensitivity.*` | Ventanas operativas dependen de IL/ER/sesgo; H4 más exigente (no alcanza umbral en barrido). Requiere medición RIN/PD/linealidad/BER. |
| **Endurance/duty y co-optimización** | `model_reliability_endurance_duty.py`, `model_duty_throughput_endurance.py`, `outputs/reliability_endurance_duty.*`, `outputs/duty_throughput_endurance.*` | Con mapeo **weight-stationary** y baja fracción de reescritura, inferencia/actualizaciones periódicas compatibles en modelo (PCM); aprendizaje continuo agresivo exige wear-leveling/limitación de rewrites. Validar con ciclado/retención medidos. |
| **Potencia/energía y Pareto** | `model_power_energy.py`, `model_pareto_multio bjective.py` (corregido: `pareto_multiobjective`), `outputs/power_energy_budget.*`, `outputs/pareto_multiobjective.*` | Tendencias TOPS/W y costo-eficiencia por perfil (proxies); G3/G2 eficientes, H3 balanceado/abierto, 3D con overheads. No es BOM ni medición. |
| **Envolvente integrada y variantes** | `model_architecture_envelope.py`, `test_architecture_variants.py`, `outputs/architecture_*` | V1 H3 base (16/0), V2 G3 (19/0), V3 G2 (16/0, con S4 coste incluido), V4 H1 (16/0), V5 H4 (13/0), V6 plataforma común (19/0) — pruebas conceptuales contra umbrales de simulación; 3D mantiene riesgos de integración. |
| **Referencias obtenidas** | `data/reference_params_supplement.json` | Parámetros públicos de referencia (Sb₂S₃, deriva ~80 pm/K, ENOB, mixes de grafos) para suplir entradas faltantes. |

## 3. Recomendaciones de arquitectura (máximo soporte por cálculos actuales)

1. **Base (menor riesgo, abierta): H3 2.5D (A1+G1+B3)** — edge/ws, NV PCM, duty PCM controlado (≤~0.12 peor caso seguro, layout/secuenciado OMCC), operación weight-stationary, OpenVINO C/D inicial.
2. **Rendimiento/BW con NV: G3 2.5D (PCM+EO)** — mejor densidad/coste-eficiencia efectiva; co-gestión térmica PCM+EO y evolución B/A.
3. **Reconfiguración dinámica rápida: G2 (EO)** — sin escritura PCM 300 °C, alta eficiencia/retención efectiva; requiere refresco/buffer por persistencia limitada y plataforma EO.
4. **Capacidad 3D gradual (alto riesgo): H1/H4** — solo tras validación 2.5D/E2–E4; particionado, redundancia/re-mapeo, manifold/térmica y control de proceso/alineación.
5. **Plataforma común (V6):** PCIe/DMA/MSI-X + ICD OpenCL, tiles modulares/aislables, colas/batching/coalescing, partición heterogénea con fallback; memoria con pesos residentes/NV donde aplique.
6. **Condiciones habilitantes:** OMCC (scheduling térmico, wear-leveling, re-mapeo), calibración en lazo cerrado, co-optimización redundancia–área–energía–latencia, y políticas de actualización para endurance.

## 4. Lo que no se puede cerrar con recursos actuales (bloqueos reales)

- **FEM térmico 3D transitorio / FDTD-EM / trazas RTL-FPGA-driver reales / metrología de proceso / mediciones E1–E4:** requieren herramientas, equipamiento o datos externos.
- **CC0 legal efectiva, DOIs/IDs Zenodo/ip.com, archivado:** requieren acción de titulares y gestión manual/externa.
- **Garantías:** no hay garantía de rendimiento, FTO, fabricabilidad, certificación ni contra intentos de registro/precios abusivos (mitigación vía arte previo/divulgación abierta).

## 5. Artefactos de referencia rápida

- Roadmap y estado: `FEASIBILITY_SIMULATION_ROADMAP.md`, `CHANGELOG.md`
- Índice: `open-photonic-gpu/README.md`
- Resultados integrados: `outputs/architecture_operating_envelope.*`, `outputs/architecture_variant_tests.*`
- Parámetros de referencia: `data/reference_params_supplement.json`
- Publicación defensiva: `DEFENSIVE_DISCLOSURES/`, `PUBLISHING_ALL_VERSIONS_PLAN.md`

*Documento de síntesis conceptual; no constituye diseño listo para fabricación/certificación ni asesoría legal.*