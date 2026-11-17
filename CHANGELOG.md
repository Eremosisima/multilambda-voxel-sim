# Changelog

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
