# Changelog

## [v0.8.1-research] - I+D: avance simulaciones S1/S2 (2026-11-17)
### Added
- `model_s2_system_profiles.py` y salidas `outputs/s2_system_profiles.{md,csv,json}`, `figures/s2_system_profiles.png`: perfiles de rendimiento S2 (edge/workstation/datacenter) para modos GPU/NPU/TPU con M0-M3/OMCC+P1, colas, batching y cumplimiento de objetivos.
### Changed
- `model_s1_link_thermal.py` y `outputs/s1_link_thermal.*`: recalibración térmica paramétrica para candidatos PCM (H3,G3,H1,H4) mediante secuenciado OMCC, aislamiento, spreading/TEC/manifold (márgenes nominales viables; peores casos mejorados, FEM 3D aún requerido para cierre).
- `FEASIBILITY_SIMULATION_ROADMAP.md`: referencias actualizadas a artefactos S1/S2.

## [v0.8.0-research] - Combinaciones de familias y estrategia Open Hardware/FTO (2026-11-17)
### Added
- `hardware/family-combinations-openhw.md`: combinaciones candidatas **H1â€“H5** entre familias Aâ€“G (Membrane-Brush NV, RT Membrane-WDM, Open WDM-PCM, Volumetric Tensor Membrane, Dense Resonant Stack) con perfiles de precio/factibilidad/velocidad/fiabilidad/dimensiones/capacidad y estrategia para publicaciÃ³n **open hardware/libre** minimizando riesgos de infracciÃ³n (copyright, patentes/FTO, licencias, publicaciÃ³n defensiva).
- `hardware/optical-memory-hierarchy-l1l2l3.md`: anÃ¡lisis de jerarquÃ­a **RAM/L3/L2/L1/registros** en OPGPU, aclaraciÃ³n de â€œcapacitor Ã³pticoâ€ y mapeo de cavidades resonantes, micro-anillos y membranas Fâ€“P (retenciÃ³n temporal de luz) junto a PCM/VOâ‚‚/fotoquÃ­micos (memoria de estado) y gestiÃ³n OMCC.
- `hardware/min-dimensions-analysis.md` y `model_min_dimensions.py`: dimensiones teÃ³ricas mÃ­nimas por propuesta (A1, B3, G1â€“G3, H3, H1, H4) considerando confinamiento/interferencia ($\lambda/2n$, $\lambda/4n$, longitud de fase), comportamiento luz-compuesto y **handicap por fallos** (guardband de rendimiento, alineaciÃ³n, redundancia/spares, guardas de crosstalk tÃ©rmico/Ã³ptico, ECC), con salidas `outputs/min_dimensions.*`.
- `hardware/manufacturable-dimensions-and-ai-accelerators.md`, `model_manufacturable_dimensions.py`: dimensiones **fabricables** con control tÃ©rmico factible y estimaciones de mÃ³dulo OPGPU, mÃ¡s comparaciÃ³n de escala con **NPU/TPU/GPU** actuales para IA avanzada (`outputs/manufacturable_dimensions.*`, `outputs/ai_module_size_estimates.csv`).
- `hardware/current-strategies-schematics-and-instructions.md`: esquemÃ¡ticos e instrucciones integradores de estrategias actuales (Aâ€“G, H1â€“H5, priorizaciÃ³n H3/G2/G3/H1/H4), dimensiones fabricables/tÃ©rmica, jerarquÃ­a M0â€“M3/OMCC e interfaces modulares para aislamiento C&D.
- `hardware/pcie-bridge-opencl-openvino.md`: diseÃ±o de **electrÃ³nica de compatibilizaciÃ³n PCIe** (EP/DMA/BAR/CSRs, cadena E/O-O/E, potencia/SI-PI/tÃ©rmica), stack de software (KMD/ICD/compilador) y camino de compatibilidad **OpenCL** y **OpenVINO** (plugin nativo, vÃ­a backend OpenCL, heterogÃ©neo/fallback).
- `PUBLIC_DOMAIN_DEDICATION.md`: documento para poner las obras originales a disposiciÃ³n de todo el mundo en **dominio pÃºblico** (vÃ­a **CC0 1.0**, en la medida permitida por la ley), con revisiÃ³n de situaciÃ³n actual de licencias, limitaciones (patentes/FTO, marcas, terceros, moral rights), ajustes necesarios y checklist de transiciÃ³n (monorepo y `candidates/`).
- `FEASIBILITY_SIMULATION_ROADMAP.md` y `model_feasibility_roadmap.py`: hoja de ruta de viabilidad **simulaciÃ³n primero (S1â€“S4) y experimentos despuÃ©s (E1â€“E4)** para candidatos priorizados (H3,G2,G3,H1,H4), con scorecard consolidado (Ã³ptica, memoria M0â€“M3, tÃ©rmica/control, fabricabilidad, yield/3D, PCIe/OpenCL/OpenVINO, coste/acceso, FTO/modularidad), secuencia recomendada y salidas `outputs/feasibility_roadmap.*` y `figures/feasibility_scorecard_{axes,overall}.png`.
- Simulaciones de avance S1/S3/S4: `model_s1_link_thermal.py` (`outputs/s1_link_thermal.*`, `figures/s1_link_thermal_margins.png`), `model_s3_pcie_openvino.py` (`outputs/s3_pcie_openvino.*`, `outputs/s3_pcie_latency.csv`, `figures/s3_pcie_latency_gen4x8.png`), `model_s4_variability_yield.py` (`outputs/s4_variability_yield.*`, `figures/s4_variability_yield.png`).
- `model_families_development.py`: extensiÃ³n a **19 variantes** incluyendo H1â€“H5; salidas regeneradas `outputs/families_dev_comparison.{md,csv,json}` y `figures/families_dev_{axes,speed_cost,reliability_feasibility,capacity_speed}.png`.
- `objective_combo_analysis.py`: reanÃ¡lisis objetivo de combinaciones/variantes (mÃ©tricas derivadas por mmÂ²/cmÂ³ y $/k$, simulaciÃ³n de escenarios de throughput: inferencia estÃ¡tica, reconfiguraciÃ³n dinÃ¡mica, limitado por memoria/BW, sensibilidad Monte Carlo Â±30% y frentes de Pareto) con salidas `outputs/objective_combo_analysis.*` y `figures/objective_*`.
- `CANDIDATE_REPOS_STRATEGY.md` y `candidates/` (H3, G2, G3, H1, H4): repositorios/candidatos independientes priorizados (staging) para aislamiento ante C&D.
### Changed
- `hardware/*` (familias Aâ€“G, combinaciones H1â€“H5, esquemÃ¡ticos e instrucciones, jerarquÃ­a M0â€“M3/OMCC, P1â€“P3, OpenCL/PCIe-OpenVINO, dimensiones/viabilidad) y `README.md`: actualizados a estrategias actuales (v0.8) y marcados con **objetivo de dominio pÃºblico (CC0 1.0) y divulgaciÃ³n defensiva/arte previo** (uso libre universal; dificultar apropiaciÃ³n registral por terceros, sin garantÃ­a absoluta), manteniendo aviso de licencias vigentes y transiciÃ³n segÃºn `PUBLIC_DOMAIN_DEDICATION.md`.
- `candidates/H3,G2,G3,H1,H4` (README, IP_AND_OPEN_HW, NOTICE): todas las estrategias/candidatos priorizados subidos y marcados con objetivo de dominio pÃºblico (CC0 1.0) y publicaciÃ³n defensiva para uso libre universal.

## [v0.7.1-research] - ComparaciÃ³n de desarrollo de familias (precio, factibilidad, velocidad, fiabilidad, dimensiones, capacidad) (2026-11-17)
### Added
- `model_families_development.py`: comparaciÃ³n conceptual extendida de variantes (Aâ€“G, 14) por **precio**, **factibilidad**, **velocidad**, **fiabilidad**, **dimensiones** y **capacidad** (cÃ³mputo TOPS, memoria/pesos efectiva y ancho de banda), con rankings y recomendaciones por prioridad.
- **Familia G (membranas apiladas de pelÃ­cula delgada / Fabryâ€“PÃ©rot):** interferencia constructiva/destructiva por espesor Ã³ptico $n d$ y $\lambda$ (anÃ¡loga a agua jabonosa/experimento de Young) aplicada a cores/cerdas para alta densidad volumÃ©trica y WDM vertical; variantes **G2** (sintonÃ­a EO rÃ¡pida) y **G3** (hÃ­brida PCM+EO) incluidas en la comparaciÃ³n.
- Salidas regeneradas: `outputs/families_dev_comparison.{md,csv,json}` y `figures/families_dev_{axes,speed_cost,reliability_feasibility,capacity_speed}.png`.
### Changed
- `hardware/families-and-variants.md`: eje de **capacidad**, familia/variantes **G** y **OPGPU-Membrane**, secciÃ³n de comparaciÃ³n cuantitativa de desarrollo y referencia a salidas `families_dev_*`.
- `README.md`: referencia a `model_families_development.py` y comparativas multi-eje de familias.

## [v0.7.0-research] - Familias y variantes Ã³pticas rÃ¡pidas (2026-11-17)
### Added
- `hardware/families-and-variants.md`: familias Aâ€“F (interferomÃ©trica, resonante/BIC, electro-Ã³ptica, plasmÃ³nica/ENZ, todo-Ã³ptica no lineal, difractiva) y variantes de referencia, con Ã©nfasis en respuesta rÃ¡pida e interferencia aditiva/destructiva.
- `model_families_comparison.py`: comparaciÃ³n conceptual (latencia, reconfiguraciÃ³n, energÃ­a, IL, no volatilidad, madurez) con salidas `outputs/families_comparison.*` y `figures/families_*`.

## [v0.6.0-mission] - Reencuadre de misiÃ³n y adopciÃ³n abierta (2026-11-17)
### Added
- `MISSION_AND_ADOPTION.md`: objetivo orientado a que terceros con capacidad/capital implementen y fabriquen a partir de las propuestas y datos abiertos, promoviendo competencia y accesibilidad mediante licenciamiento abierto (sin fijaciÃ³n de precios por licencia).
### Changed
- `README.md`: actualizado para reflejar el enfoque de diseÃ±o de referencia abierto y enlace a la estrategia de adopciÃ³n.

## [v0.5.4-research] - Variabilidad P3, modo 4b/5b y refresco M2 (2026-11-17)
### Added
- `hardware/p3-modeling-data.md` y `model_variability_p3.py`: modelado de variabilidad espacial, comparaciÃ³n de modos 4b/5b y polÃ­tica de refresco M2 (VOâ‚‚) con salidas `outputs/p3_*` y `figures/p3_*`.
- ConfiguraciÃ³n de sistema `*-OMCC-P3-4b` en `simulate_opgpu_system.py` (modo robusto 4b, refresco M2, RAS) con resultados comparativos actualizados en `outputs/opgpu_system_*`.

## [v0.5.3-research] - Fiabilidad P2 y perfil sistema RAS (2026-11-17)
### Added
- `hardware/p2-modeling-data.md` y `model_reliability_p2.py`: modelado de fiabilidad (ruido de lectura/SER/bits efectivos, endurance y retenciÃ³n por material M0â€“M3) con salidas `outputs/reliability_*` y `figures/reliability_*`.
- ConfiguraciÃ³n de sistema `*-OMCC-P2-RAS` en `simulate_opgpu_system.py` (mayor verificaciÃ³n/arbitraje, margen de fiabilidad) con resultados comparativos actualizados en `outputs/opgpu_system_*`.

## [v0.5.2-research] - IntegraciÃ³n P1 en simulaciÃ³n de sistema (2026-11-17)
### Added
- IntegraciÃ³n de parÃ¡metros P1-calibrados (PCM multinivel/IL/energÃ­a, mÃ¡rgenes tÃ©rmicos y serializaciÃ³n de escritura) en `simulate_opgpu_system.py`, con configuraciones comparativas `*-OMCC-P1` y resultados actualizados en `outputs/opgpu_system_*` y `figures/opgpu_system_*`.
- Perfil de desempeÃ±o/energÃ­a bajo operaciÃ³n tÃ©rmicamente consciente (OMCC + persistencia M1 + calibraciÃ³n PCM), usado como respaldo de dimensionamiento.

## [v0.5.1-research] - Modelado P1 con datos de respaldo (2026-11-17)
### Added
- `hardware/p1-modeling-data.md`: resultados y anÃ¡lisis del modelado P1 (PCM Sbâ‚‚Sâ‚ƒ multinivel segmentado/tapered y tÃ©rmica transitoria/diafonÃ­a 68 Â°C/300 Â°C en arreglo cepillo).
- `model_pcm_multilevel.py`: modelo de celda PCM multinivel (fase, IL, niveles 5-bit, supuestos) con salidas `outputs/pcm_multilevel_*` y `figures/pcm_multilevel_*`.
- `model_thermal_brush.py`: modelo tÃ©rmico transitorio radial/axial (picos, margen VOâ‚‚, barrido de pitch) con salidas `outputs/thermal_brush_*` y `figures/thermal_brush_*`.

## [v0.5.0-hardware] - Coprocesador OMCC, RAM Ã³ptica compartida e investigaciÃ³n de mejoras (2026-11-17)
### Added
- `hardware/coprocessor-and-improvements.md`: diseÃ±o conceptual del coprocesador **OMCC** (Optical Memory & Control Coprocessor) con acceso directo/compartido a RAM Ã³ptica (M0â€“M3), funciones de gestiÃ³n de memoria, DMA/prefetch, planificaciÃ³n tÃ©rmica, calibraciÃ³n y RAS.
- InvestigaciÃ³n en profundidad de mejoras: multinivel y nanoestructuraciÃ³n/segmentaciÃ³n de PCM (Sbâ‚‚Sâ‚ƒ y variantes), endurance/conmutaciÃ³n VOâ‚‚, optimizaciÃ³n espectral/WDM, calibraciÃ³n en lazo cerrado, mitigaciÃ³n de cuellos de botella y hoja de ruta priorizada con referencias.
- ExtensiÃ³n de `simulate_opgpu_system.py` (v0.5) para modelar OMCC (solapamiento DMA/cÃ³mputo, persistencia de pesos en M1, arbitraje/verificaciÃ³n, impacto en colas) con resultados actualizados en `outputs/opgpu_system_*` y figuras.

## [v0.4.0-hardware] - OpenCL, NPU/TPU y simulaciÃ³n de sistema (2026-11-16)
### Added
- `hardware/opencl-compatibility.md`: modelo de compatibilidad OpenCL (dispositivo/compute units/colas/eventos), mapeo de memoria a jerarquÃ­a Ã³ptica (M0â€“M3), espacios BAR/MMIO y flujo de comandos PCIeâ†’microsecuenciadorâ†’plano fotÃ³nicoâ†’O/E.
- `hardware/schematics-deep-dive.md`: esquemÃ¡ticos detallados de sistema, borde PCIe/transductor (E/O, O/E, DMA, command processor), compute tile, cerda/vÃ³xel del cepillo extruido y pipeline temporal.
- `hardware/npu-tpu-extensions.md`: extensiones de arquitectura para modos NPU (inferencia, activaciones VOâ‚‚, pesos estacionarios) y TPU-like (GEMM/matmul sistÃ³lico Ã³ptico, tiling y acumulaciÃ³n).
- `simulate_opgpu_system.py`: simulaciÃ³n de sistema (PCIe/colas OpenCL, ejecuciÃ³n Ã³ptica por tiles, modos GPU/NPU/TPU) con salidas `outputs/opgpu_system_*` y figuras `figures/opgpu_system_*`.

## [v0.3.0-hardware] - hardware integration (2026-11-16)
### Added
- Concepto de hardware abierto **OPGPU v0.3** integrado al repositorio: arquitectura mayoritariamente Ã³ptica con memoria Ã³ptica integrada, acoplamiento a host por PCIe (transducciÃ³n E/Oâ€“O/E) y topologÃ­a 3D "cepillo extruido" (canales por cerda, reflexiÃ³n a 45Â°, vÃ³xeles direccionables).
- DocumentaciÃ³n de diseÃ±o en `hardware/open-photonic-gpu-v1.md` y `hardware/open-photonic-gpu-v1-schematic-pcie.md` (incluye revisiÃ³n de procedencia/IP y guÃ­a de publicaciÃ³n open hardware).
- Licenciamiento explÃ­cito para hardware: `LICENSE-HARDWARE` (CERN-OHL-S v2) y `LICENSE-docs` (CC BY-SA 4.0) para documentaciÃ³n de hardware, manteniendo Apache 2.0 para el cÃ³digo de simulaciÃ³n.

## [0.1.0-preprint] - 2026-11-15
### Added
- Modelo lineal de voxel fotÃ³nico multiplexado y matriz de respuesta 4x4 con decodificaciÃ³n por inversiÃ³n.
- Simulaciones MZI (Î”Ï† por nivel), barridos de ruido/robustez y robustez extendida con error de calibraciÃ³n.
- AnÃ¡lisis de sensibilidad paramÃ©trica (L, Î“, escala de Î”n, crosstalk) y presupuesto simplificado de SNR (shot + deriva termo-Ã³ptica).
- Modelos de crosstalk tÃ©rmico/Ã³ptico vs separaciÃ³n de capas.
- Escenarios de energÃ­a/CO2 con supuestos explÃ­citos (comparaciÃ³n ilustrativa).
- Salidas reproducibles en `outputs/` y figuras en `figures/`.
- Borradores/documentaciÃ³n: `ARTICLE1_SKELETON.md`, estrategia multirrevista, guÃ­a legal/defensiva informativa, archivado, notas de riesgo y nota de autorÃ­a por IA.
- Estructura de borradores independientes en `articles/A-E` (ES).

### Notes
- Paquete de simulaciÃ³n/escenario; no contiene resultados experimentales ni afirmaciones de desempeÃ±o medido.
- ParÃ¡metros de materiales y referencias energÃ©ticas deben sustituirse/citarse con fuentes primarias antes de envÃ­o a revistas.

## Historial de diseÃ±o OPGPU (previo a la integraciÃ³n en este repositorio)
### v0.3
- RevisiÃ³n de procedencia/IP, acoplamiento PCIe, arquitectura "cepillo extruido" (45Â°), estimaciÃ³n de escalabilidad de vÃ³xeles y guÃ­a de publicaciÃ³n.

### v0.2
- Arquitectura orientada a cÃ³mputo y memoria predominantemente Ã³pticos (Sb2S3, VO2, azobenceno, espiropirano).

### v0.1
- Propuesta conceptual inicial y roles de materiales.

