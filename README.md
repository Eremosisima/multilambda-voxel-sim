# Open Photonic Voxel Memory & OPGPU (multilambda-voxel-sim)

Repositorio abierto del proyecto de **memoria/cómputo fotónico voxelizado multiplexado por longitud de onda**. Integra:

- **Paquete de simulaciones teóricas** (memoria óptica en un voxel: fotoswitches ortogonales, lectura por fase/MZI, robustez/SNR, crosstalk y escenarios de energía/CO₂).
- **Concepto de hardware abierto OPGPU v0.3** (acelerador predominantemente óptico con memoria óptica integrada, acoplamiento PCIe y arquitectura 3D tipo "cepillo extruido").

> **Estado:** simulación/escenario y borradores conceptuales de hardware. No representa mediciones de un dispositivo fabricado ni un diseño listo para fabricación/certificación.

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

## 2. Diseño de hardware abierto (OPGPU v0.4, conceptual)

Concepto de acelerador **predominantemente óptico** (cómputo, enrutamiento y memoria en el dominio fotónico) con acoplamiento a host por PCIe (transducción E/O–O/E en el borde) y matriz 3D tipo **"cepillo extruido"**.

- [`hardware/open-photonic-gpu-v1.md`](hardware/open-photonic-gpu-v1.md): arquitectura v0.2 (núcleo MVM óptico y jerarquía de memoria óptica).
- [`hardware/open-photonic-gpu-v1-schematic-pcie.md`](hardware/open-photonic-gpu-v1-schematic-pcie.md): esquemático v0.3 (revisión de IP, acoplamiento PCIe, cerdas/canales con reflexión a 45°, direccionamiento de vóxeles, escalabilidad y guía de publicación).
- [`hardware/opencl-compatibility.md`](hardware/opencl-compatibility.md): mapeo de modelo OpenCL (plataforma/dispositivo, colas, memoria global/local/private↔M0-M3, ejecución) y protocolo de comunicación PCIe/command processor/transductor.
- [`hardware/schematics-deep-dive.md`](hardware/schematics-deep-dive.md): esquemáticos detallados (sistema, borde PCIe/E-O-O-E, compute tile, cerda/vóxel, mapa de señales y pipeline).
- [`hardware/npu-tpu-extensions.md`](hardware/npu-tpu-extensions.md): extensiones de modo **NPU** (inferencia, activaciones, pesos estacionarios) y **TPU-like** (arreglo tensorial/sistólico óptico, GEMM/matmul).

**Materiales funcionales (concepto OPGPU):** Sb₂S₃ (pesos/memoria no volátil, 650 nm / 300 °C), VO₂ (conmutación/buffers volátiles, 800 nm / 68 °C), Azobenceno (ajuste de fase/retardo, 365/450 nm), Espiropirano (configuración/máscaras, 365/520 nm).

**Simulación de sistema (v0.4):** `simulate_opgpu_system.py` modela el flujo OpenCL/PCIe, ejecución óptica por tiles y modos GPU/NPU/TPU, generando resultados en `outputs/opgpu_system_*` y figuras en `figures/opgpu_system_*`.

```bash
python simulate_opgpu_system.py
```

**Avisos:** implica fuentes láser (UV/visible/NIR) y procesos térmicos localizados (hasta ~300 °C en Sb₂S₃); requiere validación de seguridad, térmica y cumplimiento (PCIe/OpenCL son nominativos; la conformidad requiere implementación y pruebas formales).

## Licencias

- **Código fuente (simulaciones, scripts):** Apache License 2.0 (ver [`LICENSE`](LICENSE)).
- **Diseño/documentación de hardware (`hardware/`):** CERN-OHL-S v2 (ver [`LICENSE-HARDWARE`](LICENSE-HARDWARE)).
- **Documentación general y manuscritos:** salvo indicación en contrario, se recomienda/usa CC BY 4.0 o la licencia indicada en cada subdirectorio/archivo; la documentación de hardware específica se publica bajo CERN-OHL-S v2 (o CC BY-SA 4.0 donde se indique, p. ej. [`LICENSE-docs`](LICENSE-docs)).
- Ver [`NOTICE`](NOTICE) y [`AI_AUTHORSHIP_NOTE.md`](AI_AUTHORSHIP_NOTE.md) para atribución y procedencia.

## Aviso

Las simulaciones, escenarios y diseños conceptuales no deben interpretarse como promesas de desempeño medido ni como asesoría legal/de propiedad intelectual. Cita fuentes primarias para parámetros de materiales y consumo energético cuando prepares envíos a revistas o implementaciones.
