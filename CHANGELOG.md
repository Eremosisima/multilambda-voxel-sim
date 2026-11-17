# Changelog

## [v0.5.0-hardware] - Coprocesador OMCC, RAM óptica compartida e investigación de mejoras (2026-11-17)
### Added
- `hardware/coprocessor-and-improvements.md`: diseño conceptual del coprocesador **OMCC** (Optical Memory & Control Coprocessor) con acceso directo/compartido a RAM óptica (M0–M3), funciones de gestión de memoria, DMA/prefetch, planificación térmica, calibración y RAS.
- Investigación en profundidad de mejoras: multinivel y nanoestructuración/segmentación de PCM (Sb₂S₃ y variantes), endurance/conmutación VO₂, optimización espectral/WDM, calibración en lazo cerrado, mitigación de cuellos de botella y hoja de ruta priorizada con referencias.

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
