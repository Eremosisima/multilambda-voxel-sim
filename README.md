# Open Photonic Voxel Memory & OPGPU (multilambda-voxel-sim)

Repositorio de **hardware abierto** (diseños de referencia, simulaciones y datos) para **memoria/cómputo fotónico voxelizado multiplexado por longitud de onda**. El proyecto está orientado a que **terceros con capacidad técnica y capital** puedan tomar estas propuestas y experimentos para implementar, fabricar y escalar la tecnología; al ser abierto (CERN-OHL-S v2, Apache-2.0, CC BY-SA), busca habilitar competencia, transparencia y **accesibilidad económica** (ver [`MISSION_AND_ADOPTION.md`](MISSION_AND_ADOPTION.md)).

Integra:

- **Paquete de simulaciones teóricas** (memoria óptica en un voxel: fotoswitches ortogonales, lectura por fase/MZI, robustez/SNR, crosstalk y escenarios de energía/CO₂).
- **Diseño de referencia OPGPU** (acelerador predominantemente óptico con memoria óptica integrada, acoplamiento PCIe/OpenCL, modos GPU/NPU/TPU, coprocesador OMCC y arquitectura 3D tipo "cepillo extruido"), con modelado P1–P3.

> **Estado:** simulación/escenario y borradores conceptuales de referencia. No representa mediciones de un dispositivo fabricado ni un diseño listo para fabricación/certificación. Pensado para adopción e implementación por terceros.

## 1. Simulaciones (paquete reproducible)

Paquete reproducible para una memoria óptica multiplexada por longitud de onda en un único voxel (fotoswitches ortogonales + lectura por fase). Incluye modelo lineal, matriz de respuesta 4x4, análisis MZI, robustez/sensibilidad, presupuesto de SNR, crosstalk térmico/óptico y escenarios de energía/CO₂.

- `compounds.py`: tabla de compuestos candidatos y parámetros (λ escritura/borrado/lectura, Δn_max, vida media térmica).
- `model.py`: modelo `delta_n_i = c_i * delta_n_i,max`, matriz `A` e inversión/decodificación.
- `mzi_sim.py`: Δφ por nivel, barrido de ruido y distinguibilidad (4 niveles/material, 8 bits/voxel).
- `robustness_extended.py`, `sensitivity.py`, `snr_budget.py`, `crosstalk.py`, `sustainability_energy.py`: análisis de robustez, sensibilidad, SNR, crosstalk y sostenibilidad.
- `run_simulations.py`: ejecuta todo y genera tablas/figuras/reporte.
- `ARTICLE1_SKELETON.md`, `PUBLICATION_STRATEGY_MULTIJOURNAL.md`, `LEGAL_REVIEW_AND_DEFENSIVE_PUBLICATION.md`, `ARCHIVING.md`: borradores y guías de publicación/archivo.
- `articles/`: borradores independientes A–E (ES).

### Requisitos y ejecución
- Python 3.10+
- `numpy`, `matplotlib`

```bash
python run_simulations.py
```

### Salidas reproducibles
- `outputs/*.csv`, `outputs/*.json`: parámetros, matrices, fases, ruido/robustez, sensibilidad, SNR, crosstalk, escenarios.
- `outputs/report.md`: resumen consolidado.
- `figures/*.png`: gráficas para manuscritos.

## 2. Diseño de hardware abierto (OPGPU v0.8, conceptual)

Concepto de acelerador **predominantemente óptico** (cómputo, enrutamiento y memoria en el dominio fotónico) con acoplamiento a host por PCIe (transducción E/O–O/E en el borde) y matriz 3D tipo **"cepillo extruido"**.

- [`FEASIBILITY_SIMULATION_ROADMAP.md`](FEASIBILITY_SIMULATION_ROADMAP.md): hoja de ruta para **hacer posible el objetivo** — **simulaciones primero** (S1–S4: presupuestos óptico/térmico/enlace, rendimiento M0–M3/OMCC, PCIe/OpenCL/OpenVINO, fiabilidad/yield) y **experimentos después** (E1–E4), con scorecard de viabilidad por candidato priorizado (H3, G2, G3, H1, H4) y secuencia recomendada. Reproducible con `model_feasibility_roadmap.py` (`outputs/feasibility_roadmap.*`, `figures/feasibility_scorecard_*`).

- [`hardware/open-photonic-gpu-v1.md`](hardware/open-photonic-gpu-v1.md): arquitectura v0.2 (núcleo MVM óptico y jerarquía de memoria óptica).
- [`hardware/open-photonic-gpu-v1-schematic-pcie.md`](hardware/open-photonic-gpu-v1-schematic-pcie.md): esquemático v0.3 (revisión de IP, acoplamiento PCIe, cerdas/canales con reflexión a 45°, direccionamiento de vóxeles, escalabilidad y guía de publicación).
- [`hardware/opencl-compatibility.md`](hardware/opencl-compatibility.md): mapeo de modelo OpenCL (plataforma/dispositivo, colas, memoria global/local/private↔M0-M3, ejecución) y protocolo de comunicación PCIe/command processor/transductor.
- [`hardware/schematics-deep-dive.md`](hardware/schematics-deep-dive.md): esquemáticos detallados (sistema, borde PCIe/E-O-O-E, compute tile, cerda/vóxel, mapa de señales y pipeline).
- [`hardware/npu-tpu-extensions.md`](hardware/npu-tpu-extensions.md): extensiones de modo **NPU** (inferencia, activaciones, pesos estacionarios) y **TPU-like** (arreglo tensorial/sistólico óptico, GEMM/matmul).
- [`hardware/coprocessor-and-improvements.md`](hardware/coprocessor-and-improvements.md): coprocesador **OMCC** con acceso directo/compartido a RAM óptica (M0–M3) y hoja de investigación de mejoras (multinivel/segmentación PCM, endurance VO₂, WDM, calibración, RAS, priorización).
- [`hardware/pcie-bridge-opencl-openvino.md`](hardware/pcie-bridge-opencl-openvino.md): **electrónica de compatibilización PCIe** (EP/DMA/BAR/CSRs, cadena E/O-O/E, potencia/SI-PI/térmica), stack de software (KMD/ICD/compilador) y camino de compatibilidad **OpenCL** y **OpenVINO** (plugin nativo, vía OpenCL, heterogéneo/fallback).
- [`hardware/current-strategies-schematics-and-instructions.md`](hardware/current-strategies-schematics-and-instructions.md): esquemáticos e instrucciones integradores de estrategias actuales (A–G, H1–H5, priorización H3/G2/G3/H1/H4), control térmico fabricable, M0–M3/OMCC e interfaces modulares/C&D.
- [`hardware/p1-modeling-data.md`](hardware/p1-modeling-data.md): modelado P1 con datos de respaldo (celda PCM Sb₂S₃ multinivel segmentada/tapered y térmica transitoria/diafonía 300 °C vs 68 °C del arreglo cepillo).
- [`hardware/p2-modeling-data.md`](hardware/p2-modeling-data.md): modelado P2 de fiabilidad (ruido/precisión efectiva, endurance y retención por material, perfil sistema P2-RAS).
- [`hardware/p3-modeling-data.md`](hardware/p3-modeling-data.md): modelado P3 (variabilidad espacial, selección de modo 4b/5b, refresco M2 y perfil robusto).
- [`hardware/families-and-variants.md`](hardware/families-and-variants.md): familias y variantes de arquitectura (A–G, incl. membranas de película delgada/F–P) con uso de interferencia aditiva/destructiva, rutas de mayor velocidad y comparación de desarrollo.
- [`hardware/family-combinations-openhw.md`](hardware/family-combinations-openhw.md): combinaciones candidatas entre familias (H1–H5), perfil multi-eje y estrategia de Open Hardware/libertad de uso sin infracción (copyright/patentes, FTO).
- [`hardware/optical-memory-hierarchy-l1l2l3.md`](hardware/optical-memory-hierarchy-l1l2l3.md): análisis de jerarquía **RAM/L3/L2/L1/registros** en OPGPU, mapeo a M0–M3/OMCC y uso de “capacitores ópticos”/cavidades, anillos y membranas F–P como buffers o memoria de estado.
- [`hardware/min-dimensions-analysis.md`](hardware/min-dimensions-analysis.md): dimensiones teóricas mínimas por propuesta (A1, B3, G1–G3, H3, H1, H4) considerando confinamiento/interferencia, comportamiento luz-compuesto y handicap por fallos (rendimiento, alineación, redundancia, crosstalk térmico/óptico, ECC).
- [`hardware/manufacturable-dimensions-and-ai-accelerators.md`](hardware/manufacturable-dimensions-and-ai-accelerators.md): dimensiones mínimas fabricables con control térmico factible y comparación de escala con NPU/TPU/GPU actuales para IA avanzada.

**Modelado reproducible:** `model_pcm_multilevel.py`, `model_thermal_brush.py`, `model_reliability_p2.py`, `model_variability_p3.py`, `model_families_comparison.py` y `model_families_development.py` generan datos/figuras en `outputs/` y `figures/` (incl. comparativas de familias por precio, factibilidad, velocidad, fiabilidad, dimensiones y capacidad en `outputs/families_dev_*`). La simulación de sistema `simulate_opgpu_system.py` integra parámetros P1–P3 en configuraciones comparativas. `objective_combo_analysis.py` realiza un reanálisis objetivo de combinaciones (métricas derivadas, escenarios estático/dinámico/memoria-limitado y sensibilidad ±30%) en `outputs/objective_combo_analysis.*` y `figures/objective_*`. `model_min_dimensions.py` estima dimensiones teóricas mínimas con handicap por fallos en `outputs/min_dimensions.*`.

**Materiales funcionales (concepto OPGPU):** Sb₂S₃ (pesos/memoria no volátil, 650 nm / 300 °C), VO₂ (conmutación/buffers volátiles, 800 nm / 68 °C), Azobenceno (ajuste de fase/retardo, 365/450 nm), Espiropirano (configuración/máscaras, 365/520 nm).

**Simulación de sistema (v0.5):** `simulate_opgpu_system.py` modela el flujo OpenCL/PCIe, ejecución óptica por tiles, modos GPU/NPU/TPU y efectos del coprocesador OMCC (solapamiento DMA/cómputo, persistencia de pesos en M1, arbitraje/verificación y colas), generando resultados en `outputs/opgpu_system_*` y figuras en `figures/opgpu_system_*`.

```bash
python simulate_opgpu_system.py
```

**Avisos:** implica fuentes láser (UV/visible/NIR) y procesos térmicos localizados (hasta ~300 °C en Sb₂S₃); requiere validación de seguridad, térmica y cumplimiento (PCIe/OpenCL son nominativos; la conformidad requiere implementación y pruebas formales).

## Misión, adopción y licencias

- **Misión y estrategia:** [`MISSION_AND_ADOPTION.md`](MISSION_AND_ADOPTION.md) (habilitar implementación por terceros, apertura para competencia y accesibilidad; las licencias no fijan precios por sí mismas).
- **Dominio público (propuesta/ajustes):** [`PUBLIC_DOMAIN_DEDICATION.md`](PUBLIC_DOMAIN_DEDICATION.md) — documento para poner las obras originales a disposición de todo el mundo en **dominio público** (vía **CC0 1.0**, en la medida permitida por la ley), con revisión de ajustes necesarios, limitaciones (patentes/FTO, marcas, terceros, derechos morales) y checklist de transición.
- **Régimen actual (vigente en esta versión):**
  - **Código fuente (simulaciones, scripts):** Apache License 2.0 (ver [`LICENSE`](LICENSE)).
  - **Diseño/documentación de hardware (`hardware/`):** CERN-OHL-S v2 (ver [`LICENSE-HARDWARE`](LICENSE-HARDWARE)).
  - **Documentación general y manuscritos:** salvo indicación en contrario, se recomienda/usa CC BY 4.0 o la licencia indicada en cada subdirectorio/archivo; la documentación de hardware específica se publica bajo CERN-OHL-S v2 (o CC BY-SA 4.0 donde se indique, p. ej. [`LICENSE-docs`](LICENSE-docs)).
- Ver [`NOTICE`](NOTICE) y [`AI_AUTHORSHIP_NOTE.md`](AI_AUTHORSHIP_NOTE.md) para atribución y procedencia.

## Aviso

Las simulaciones, escenarios y diseños conceptuales no deben interpretarse como promesas de desempeño medido ni como asesoría legal/de propiedad intelectual. Cita fuentes primarias para parámetros de materiales y consumo energético cuando prepares envíos a revistas o implementaciones.
