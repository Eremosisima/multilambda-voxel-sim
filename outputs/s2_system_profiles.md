# S2 — Perfiles de sistema (edge / workstation / datacenter)

> Modelo funcional/conceptual S2 (no mediciones). Extiende `simulate_opgpu_system.py` con envolventes edge/ws/dc, colas OMCC y parámetros M0–M3/OMCC+P1.

## Resumen por perfil

| Perfil | Batch | Objetivo lat (ms) | Objetivo TOPS | TOPS medio NPU | TOPS medio TPU | Lat media NPU (ms) | Lat media TPU (ms) | Pass lat NPU | Pass TOPS NPU | Pass TOPS TPU | Cola p95 (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| edge | 1 | 10 | 8 | 23.535 | 23.546 | 0.0557 | 0.0557 | 1.0 | 1.0 | 1.0 | 30.2626 |
| ws | 4 | 20 | 20 | 51.022 | 68.824 | 0.0938 | 0.0872 | 1.0 | 1.0 | 1.0 | 30.2626 |
| dc | 8 | 50 | 80 | 117.256 | 163.26 | 0.079 | 0.0721 | 1.0 | 0.75 | 0.75 | 30.2626 |

## Lectura
- **Edge:** limitado por PCIe x8, tiles y restricciones térmicas; adecuado a inferencia con cargas de intensidad media/alta si se amortizan pesos (persistencia M1/OMCC).
- **Workstation:** balance latencia/throughput con batching moderado; ruta preferente para demo OpenCL/OpenVINO heterogénea (C/D→B).
- **Datacenter:** mayor techo de TOPS efectivos con Gen5/tiles/WDM y batching, sujeto a partición y a que cuellos de transferencia sean solapables.
- Brechas frente a objetivos deben cerrarse con S3 (colas/DMA reales, partición de grafo, cuantización/calibración) y validación E3.

## Artefactos
- `outputs/s2_system_profiles.json`, `outputs/s2_system_profiles.csv`, `figures/s2_system_profiles.png`
