# Open Photonic GPU (OPGPU) / multilambda-voxel-sim

Repositorio abierto de **estrategias, esquemáticos, instrucciones, diseños, código y datos de simulación** para una arquitectura de **memoria/cómputo fotónico voxelizado** (acelerador predominantemente óptico, interfaz PCIe, modos GPU/NPU/TPU). Orientado a que cualquiera pueda **estudiar, reproducir, fabricar y mejorar** la tecnología y a servir como **divulgación defensiva / arte previo** fechada y habilitante.

> **Objetivo (dominio público y utilidad pública):** dedicar las obras originales a **dominio público (CC0 1.0, en la medida permitida por la ley)** para **uso libre universal** y dificultar apropiación registral por terceros de lo divulgado. La transición legal está **pendiente de titulares** (ver `PUBLIC_DOMAIN_DEDICATION.md`); licencias vigentes actuales: Apache-2.0 (código), CERN-OHL-S v2 (hardware), CC BY-SA 4.0 (documentación, según se indique).  
> **Estado:** conceptual/simulado. **No** son mediciones ni un diseño listo para fabricación/certificación. Sin garantía, sin libertad de operación (FTO) garantizada, sin asesoría legal. PCIe/OpenCL/OpenVINO son rutas de compatibilidad nominativas.

## Índice y orden del repositorio

| Área | Ruta | Contenido |
|---|---|---|
| **Estrategias y esquemáticos (actual)** | `hardware/current-strategies-schematics-and-instructions.md` | Esquemáticos e instrucciones integradores A–G, H1–H5, M0–M3/OMCC, modularidad/C&D |
| **Esquemáticos detallados** | `hardware/schematics-deep-dive.md`, `hardware/open-photonic-gpu-v1-schematic-pcie.md`, `hardware/open-photonic-gpu-v1.md` | Vistas de sistema, borde PCIe/E-O-O/E, tiles, cerda/vóxel, pipeline |
| **PCIe, OpenCL, OpenVINO** | `hardware/pcie-bridge-opencl-openvino.md`, `hardware/opencl-compatibility.md` | Electrónica de borde, DMA/BAR/CSRs, stack software, rutas OpenVINO |
| **Familias y combinaciones** | `hardware/families-and-variants.md`, `hardware/family-combinations-openhw.md` | Familias A–G, combinaciones H1–H5, perfiles multi-eje y open-hardware |
| **Candidatos priorizados (independientes)** | `candidates/` (H3, G2, G3, H1, H4) | Diseño, métricas, IP/PD intent, licencias y NOTICE por estrategia |
| **Memoria, dimensiones, fiabilidad** | `hardware/optical-memory-hierarchy-l1l2l3.md`, `hardware/min-dimensions-analysis.md`, `hardware/manufacturable-dimensions-and-ai-accelerators.md`, `hardware/p1-modeling-data.md`, `hardware/p2-modeling-data.md`, `hardware/p3-modeling-data.md` | M0–M3, escalado, P1–P3 |
| **Viabilidad (simulación→experimento)** | `FEASIBILITY_SIMULATION_ROADMAP.md`, `outputs/s1_*`, `outputs/s3_*`, `outputs/s4_*`, `outputs/feasibility_roadmap.*` | Hoja de ruta S1–S4/E1–E4 y resultados |
| **Divulgación defensiva (lista para publicar)** | `DEFENSIVE_DISCLOSURES/` | Borradores habilitantes: consolidado v0.8 y por estrategia (H3,G2,G3,H1,H4) |
| **Publicación de todas las versiones** | `PUBLISHING_ALL_VERSIONS_PLAN.md`, `ARCHIVING.md` | Plan Zenodo+ip.com, inventario de versiones/tags, registro de DOIs/IDs |
| **Dominio público y marco** | `PUBLIC_DOMAIN_DEDICATION.md`, `LEGAL_REVIEW_AND_DEFENSIVE_PUBLICATION.md`, `RISK_AND_COMPLIANCE_NOTES.md` | Dedicación CC0, arte previo, limitaciones (no asesoría legal) |
| **Simulaciones y datos** | `run_simulations.py`, `simulate_opgpu_system.py`, `model_*.py`, `objective_combo_analysis.py`, `outputs/`, `figures/` | Reproducibles (conceptuales) |

## Estrategias, esquemáticos e instrucciones (todas incluidas)

- **Familias base A–G:** cómputo/memoria por interferencia (MZI/PCM, resonadores/WDM, fotoquímicos, VO₂/plasmónico, mallas coherentes, difractiva/metasuperficie, membranas F–P por $n\cdot d$ en variantes pasiva/EO/PCM+EO).
- **Combinaciones H1–H5:** H1 Membrane-Brush NV (A1+G3+3D), H2 RT Membrane-WDM, H3 Open WDM-PCM (A1+G1+B3), H4 Volumetric Tensor Membrane (G2/G3+F2+A1), H5 Dense Resonant Stack.
- **Priorizadas (P1):** **H3** (abierto/factible), **G2** (velocidad/BW), **G3** (NV+velocidad), **H1** (escalado NV 3D), **H4** (techo de capacidad, alto riesgo, aislar). Detalle y esquemáticos por estrategia: `hardware/current-strategies-schematics-and-instructions.md` y `DEFENSIVE_DISCLOSURES/`.

## Candidatos independientes (aislamiento C&D)

Cada candidato en `candidates/` (H3, G2, G3, H1, H4) mantiene diseño, métricas, licencias/NOTICE y declaración de intención de dominio público/divulgación defensiva; puede publicarse o retirarse sin afectar a los demás. Ver `candidates/README.md` y `CANDIDATE_REPOS_STRATEGY.md`.

## Versiones y publicación (todas)

Tags/hitos: `v0.1.0-preprint`, `v0.3.0-hardware`, `v0.4.0-hardware`, `v0.5.0-hardware`, `v0.5.1-research`–`v0.5.4-research`, `v0.6.0-mission`, `v0.7.0-research`, `v0.7.1-research`, `v0.8.0-research`. Plan y registro de publicación en Zenodo/ip.com: `PUBLISHING_ALL_VERSIONS_PLAN.md` y `ARCHIVING.md`. Material de terceros no redistribuible excluido de paquetes (p.ej. datos PhotochemCAD: ver `data/spectra/photochemcad/README.md`).

## Reproducibilidad (simulaciones conceptuales)

- Requisitos: Python 3.10+, `numpy`, `matplotlib`.
- Ejecución base: `python run_simulations.py` · `python simulate_opgpu_system.py` · `python model_feasibility_roadmap.py` · `python model_s1_link_thermal.py` · `python model_s3_pcie_openvino.py` · `python model_s4_variability_yield.py` · `python objective_combo_analysis.py` (y demás `model_*.py`).
- Salidas: `outputs/*` y `figures/*` (no son mediciones).

## Misión, licencias y avisos

- **Misión/adopción:** `MISSION_AND_ADOPTION.md`.
- **Dominio público (propuesta):** `PUBLIC_DOMAIN_DEDICATION.md`; divulgación defensiva: `LEGAL_REVIEW_AND_DEFENSIVE_PUBLICATION.md`, `DEFENSIVE_DISCLOSURES/`.
- **Licencias vigentes:** código `LICENSE` (Apache-2.0), hardware `LICENSE-HARDWARE` (CERN-OHL-S v2), docs `LICENSE-docs` (CC BY-SA 4.0) según aplique; transición a CC0 1.0 pendiente de titulares. Atribución/procedencia: `NOTICE`, `AI_AUTHORSHIP_NOTE.md`, `CITATION.cff`.

**Avisos:** implica en concepto fuentes láser y gradientes térmicos (requiere validación de seguridad/cumplimiento). Resultados y diseños son conceptuales/simulados; no constituyen promesas de desempeño, FTO, ni asesoría legal.
