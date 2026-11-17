# Changelog

## [v0.8.0-research] - Combinaciones de familias y estrategia Open Hardware/FTO (2026-11-17)
### Added
- `hardware/family-combinations-openhw.md`: combinaciones candidatas **H1–H5** entre familias A–G (Membrane-Brush NV, RT Membrane-WDM, Open WDM-PCM, Volumetric Tensor Membrane, Dense Resonant Stack) con perfiles de precio/factibilidad/velocidad/fiabilidad/dimensiones/capacidad y estrategia para publicación **open hardware/libre** minimizando riesgos de infracción (copyright, patentes/FTO, licencias, publicación defensiva).
- `hardware/optical-memory-hierarchy-l1l2l3.md`: análisis de jerarquía **RAM/L3/L2/L1/registros** en OPGPU, aclaración de “capacitor óptico” y mapeo de cavidades resonantes, micro-anillos y membranas F–P (retención temporal de luz) junto a PCM/VO₂/fotoquímicos (memoria de estado) y gestión OMCC.
- `hardware/min-dimensions-analysis.md` y `model_min_dimensions.py`: dimensiones teóricas mínimas por propuesta (A1, B3, G1–G3, H3, H1, H4) considerando confinamiento/interferencia ($\lambda/2n$, $\lambda/4n$, longitud de fase), comportamiento luz-compuesto y **handicap por fallos** (guardband de rendimiento, alineación, redundancia/spares, guardas de crosstalk térmico/óptico, ECC), con salidas `outputs/min_dimensions.*`.
- `hardware/manufacturable-dimensions-and-ai-accelerators.md`, `model_manufacturable_dimensions.py`: dimensiones **fabricables** con control térmico factible y estimaciones de módulo OPGPU, más comparación de escala con **NPU/TPU/GPU** actuales para IA avanzada (`outputs/manufacturable_dimensions.*`, `outputs/ai_module_size_estimates.csv`).
- `hardware/current-strategies-schematics-and-instructions.md`: esquemáticos e instrucciones integradores de estrategias actuales (A–G, H1–H5, priorización H3/G2/G3/H1/H4), dimensiones fabricables/térmica, jerarquía M0–M3/OMCC e interfaces modulares para aislamiento C&D.
- `hardware/pcie-bridge-opencl-openvino.md`: diseño de **electrónica de compatibilización PCIe** (EP/DMA/BAR/CSRs, cadena E/O-O/E, potencia/SI-PI/térmica), stack de software (KMD/ICD/compilador) y camino de compatibilidad **OpenCL** y **OpenVINO** (plugin nativo, vía backend OpenCL, heterogéneo/fallback).
- `PUBLIC_DOMAIN_DEDICATION.md`: documento para poner las obras originales a disposición de todo el mundo en **dominio público** (vía **CC0 1.0**, en la medida permitida por la ley), con revisión de situación actual de licencias, limitaciones (patentes/FTO, marcas, terceros, moral rights), ajustes necesarios y checklist de transición (monorepo y `candidates/`).
- `model_families_development.py`: extensión a **19 variantes** incluyendo H1–H5; salidas regeneradas `outputs/families_dev_comparison.{md,csv,json}` y `figures/families_dev_{axes,speed_cost,reliability_feasibility,capacity_speed}.png`.
- `objective_combo_analysis.py`: reanálisis objetivo de combinaciones/variantes (métricas derivadas por mm²/cm³ y $/k$, simulación de escenarios de throughput: inferencia estática, reconfiguración dinámica, limitado por memoria/BW, sensibilidad Monte Carlo ±30% y frentes de Pareto) con salidas `outputs/objective_combo_analysis.*` y `figures/objective_*`.
- `CANDIDATE_REPOS_STRATEGY.md` y `candidates/` (H3, G2, G3, H1, H4): repositorios/candidatos independientes priorizados (staging) para aislamiento ante C&D.
### Changed
- `hardware/families-and-variants.md`, `hardware/opencl-compatibility.md`, `hardware/schematics-deep-dive.md`, `hardware/open-photonic-gpu-v1-schematic-pcie.md` y `README.md`: actualizados a estrategias actuales (v0.8) con referencias cruzadas (PCIe/OpenCL/OpenVINO, fabricabilidad/térmica, M0–M3/OMCC, modularidad). `README.md` referencia la propuesta de dedicación a dominio público.

## [v0.7.1-research] - Comparación de desarrollo de familias (precio, factibilidad, velocidad, fiabilidad, dimensiones, capacidad) (2026-11-17)
### Added
- `model_families_development.py`: comparación conceptual extendida de variantes (A–G, 14) por **precio**, **factibilidad**, **velocidad**, **fiabilidad**, **dimensiones** y **capacidad** (cómputo TOPS, memoria/pesos efectiva y ancho de banda), con rankings y recomendaciones por prioridad.
- **Familia G (membranas apiladas de película delgada / Fabry–Pérot):** interferencia constructiva/destructiva por espesor óptico $n d$ y $\lambda$ (análoga a agua jabonosa/experimento de Young) aplicada a cores/cerdas para alta densidad volumétrica y WDM vertical; variantes **G2** (sintonía EO rápida) y **G3** (híbrida PCM+EO) incluidas en la comparación.
- Salidas regeneradas: `outputs/families_dev_comparison.{md,csv,json}` y `figures/families_dev_{axes,speed_cost,reliability_feasibility,capacity_speed}.png`.
### Changed
- `hardware/families-and-variants.md`: eje de **capacidad**, familia/variantes **G** y **OPGPU-Membrane**, sección de comparación cuantitativa de desarrollo y referencia a salidas `families_dev_*`.
- `README.md`: referencia a `model_families_development.py` y comparativas multi-eje de familias.

## [v0.7.0-research] - Familias y variantes ópticas rápidas (2026-11-17)
### Added
- `hardware/families-and-variants.md`: familias A–F (interferométrica, resonante/BIC, electro-óptica, plasmónica/ENZ, todo-óptica no lineal, difractiva) y variantes de referencia, con énfasis en respuesta rápida e interferencia aditiva/destructiva.
- `model_families_comparison.py`: comparación conceptual (latencia, reconfiguración, energía, IL, no volatilidad, madurez) con salidas `outputs/families_comparison.*` y `figures/families_*`.

## [v0.6.0-mission] - Reencuadre de misión y adopción abierta (2026-11-17)
### Added
- `MISSION_AND_ADOPTION.md`: objetivo orientado a que terceros con capacidad/capital implementen y fabriquen a partir de las propuestas y datos abiertos, promoviendo competencia y accesibilidad mediante licenciamiento abierto (sin fijación de precios por licencia).
### Changed
- `README.md`: actualizado para reflejar el enfoque de diseño de referencia abierto y enlace a la estrategia de adopción.

## [v0.5.4-research] - Variabilidad P3, modo 4b/5b y refresco M2 (2026-11-17)
### Added
- `hardware/p3-modeling-data.md` y `model_variability_p3.py`: modelado de variabilidad espacial, comparación de modos 4b/5b y política de refresco M2 (VO₂) con salidas `outputs/p3_*` y `figures/p3_*`.
- Configuración de sistema `*-OMCC-P3-4b` en `simulate_opgpu_system.py` (modo robusto 4b, refresco M2, RAS) con resultados comparativos actualizados en `outputs/opgpu_system_*`.

## [v0.5.3-research] - Fiabilidad P2 y perfil sistema RAS (2026-11-17)
### Added
- `hardware/p2-modeling-data.md` y `model_reliability_p2.py`: modelado de fiabilidad (ruido de lectura/SER/bits efectivos, endurance y retención por material M0–M3) con salidas `outputs/reliability_*` y `figures/reliability_*`.
- Configuración de sistema `*-OMCC-P2-RAS` en `simulate_opgpu_system.py` (mayor verificación/arbitraje, margen de fiabilidad) con resultados comparativos actualizados en `outputs/opgpu_system_*`.

## [v0.5.2-research] - Integración P1 en simulación de sistema (2026-11-17)
### Added
- Integración de parámetros P1-calibrados (PCM multinivel/IL/energía, márgenes térmicos y serialización de escritura) en `simulate_opgpu_system.py`, con configuraciones comparativas `*-OMCC-P1` y resultados actualizados en `outputs/opgpu_system_*` y `figures/opgpu_system_*`.
- Perfil de desempeño/energía bajo operación térmicamente consciente (OMCC + persistencia M1 + calibración PCM), usado como respaldo de dimensionamiento.

## [v0.5.1-research] - Modelado P1 con datos de respaldo (2026-11-17)
### Added
- `hardware/p1-modeling-data.md`: resultados y análisis del modelado P1 (PCM Sb₂S₃ multinivel segmentado/tapered y térmica transitoria/diafonía 68 °C/300 °C en arreglo cepillo).
- `model_pcm_multilevel.py`: modelo de celda PCM multinivel (fase, IL, niveles 5-bit, supuestos) con salidas `outputs/pcm_multilevel_*` y `figures/pcm_multilevel_*`.
- `model_thermal_brush.py`: modelo térmico transitorio radial/axial (picos, margen VO₂, barrido de pitch) con salidas `outputs/thermal_brush_*` y `figures/thermal_brush_*`.

## [v0.5.0-hardware] - Coprocesador OMCC, RAM óptica compartida e investigación de mejoras (2026-11-17)
### Added
- `hardware/coprocessor-and-improvements.md`: diseño conceptual del coprocesador **OMCC** (Optical Memory & Control Coprocessor) con acceso directo/compartido a RAM óptica (M0–M3), funciones de gestión de memoria, DMA/prefetch, planificación térmica, calibración y RAS.
- Investigación en profundidad de mejoras: multinivel y nanoestructuración/segmentación de PCM (Sb₂S₃ y variantes), endurance/conmutación VO₂, optimización espectral/WDM, calibración en lazo cerrado, mitigación de cuellos de botella y hoja de ruta priorizada con referencias.
- Extensión de `simulate_opgpu_system.py` (v0.5) para modelar OMCC (solapamiento DMA/cómputo, persistencia de pesos en M1, arbitraje/verificación, impacto en colas) con resultados actualizados en `outputs/opgpu_system_*` y figuras.

## [v0.4.0-hardware] - OpenCL, NPU/TPU y simulación de sistema (2026-11-16)
### Added
- `hardware/opencl-compatibility.md`: modelo de compatibilidad OpenCL (dispositivo/compute units/colas/eventos), mapeo de memoria a jerarquía óptica (M0–M3), espacios BAR/MMIO y flujo de comandos PCIe→microsecuenciador→plano fotónico→O/E.
- `hardware/schematics-deep-dive.md`: esquemáticos detallados de sistema, borde PCIe/transductor (E/O, O/E, DMA, command processor), compute tile, cerda/vóxel del cepillo extruido y pipeline temporal.
- `hardware/npu-tpu-extensions.md`: extensiones de arquitectura para modos NPU (inferencia, activaciones VO₂, pesos estacionarios) y TPU-like (GEMM/matmul sistólico óptico, tiling y acumulación).
- `simulate_opgpu_system.py`: simulación de sistema (PCIe/colas OpenCL, ejecución óptica por tiles, modos GPU/NPU/TPU) con salidas `outputs/opgpu_system_*` y figuras `figures/opgpu_system_*`.

## [v0.3.0-hardware] - hardware integration (2026-11-16)
### Added
- Concepto de hardware abierto **OPGPU v0.3** integrado al repositorio: arquitectura mayoritariamente óptica con memoria óptica integrada, acoplamiento a host por PCIe (transducción E/O–O/E) y topología 3D "cepillo extruido" (canales por cerda, reflexión a 45°, vóxeles direccionables).
- Documentación de diseño en `hardware/open-photonic-gpu-v1.md` y `hardware/open-photonic-gpu-v1-schematic-pcie.md` (incluye revisión de procedencia/IP y guía de publicación open hardware).
- Licenciamiento explícito para hardware: `LICENSE-HARDWARE` (CERN-OHL-S v2) y `LICENSE-docs` (CC BY-SA 4.0) para documentación de hardware, manteniendo Apache 2.0 para el código de simulación.

## [0.1.0-preprint] - 2026-11-15
### Added
- Modelo lineal de voxel fotónico multiplexado y matriz de respuesta 4x4 con decodificación por inversión.
- Simulaciones MZI (Δφ por nivel), barridos de ruido/robustez y robustez extendida con error de calibración.
- Análisis de sensibilidad paramétrica (L, Γ, escala de Δn, crosstalk) y presupuesto simplificado de SNR (shot + deriva termo-óptica).
- Modelos de crosstalk térmico/óptico vs separación de capas.
- Escenarios de energía/CO2 con supuestos explícitos (comparación ilustrativa).
- Salidas reproducibles en `outputs/` y figuras en `figures/`.
- Borradores/documentación: `ARTICLE1_SKELETON.md`, estrategia multirrevista, guía legal/defensiva informativa, archivado, notas de riesgo y nota de autoría por IA.
- Estructura de borradores independientes en `articles/A-E` (ES).

### Notes
- Paquete de simulación/escenario; no contiene resultados experimentales ni afirmaciones de desempeño medido.
- Parámetros de materiales y referencias energéticas deben sustituirse/citarse con fuentes primarias antes de envío a revistas.

## Historial de diseño OPGPU (previo a la integración en este repositorio)
### v0.3
- Revisión de procedencia/IP, acoplamiento PCIe, arquitectura "cepillo extruido" (45°), estimación de escalabilidad de vóxeles y guía de publicación.

### v0.2
- Arquitectura orientada a cómputo y memoria predominantemente ópticos (Sb2S3, VO2, azobenceno, espiropirano).

### v0.1
- Propuesta conceptual inicial y roles de materiales.
