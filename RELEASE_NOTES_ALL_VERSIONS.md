# Release notes para GitHub (todas las versiones) — Zenodo

Tags ya publicados en `origin`. En GitHub: **Releases → Draft a new release → Choose a tag** (seleccionar el tag), pegar el título y notas correspondientes, marcar como *Latest* solo `v0.8.0-research` si se desea, y **Publish release**. Con Zenodo vinculado, cada release publicado se archivará (DOI de versión + Concept DOI).

Repo: https://github.com/Eremosisima/multilambda-voxel-sim

---

## v0.8.0-research (tag: `v0.8.0-research`, commit ed4b8fe) — Latest
**Title:** v0.8.0-research — OPGPU strategies, schematics, feasibility (S1/S3/S4) and public-domain/defensive intent

**Notes:**
OPGPU conceptual/simulation release (not measured, not fabrication/certification-ready).

- **Strategies & schematics:** families A–G and combinations H1–H5 (prioritized H3, G2, G3, H1, H4) with integrated schematics/instructions (`hardware/current-strategies-schematics-and-instructions.md`, `hardware/schematics-deep-dive.md`, `hardware/pcie-bridge-opencl-openvino.md`).
- **Candidates (independent):** `candidates/H3-open-wdm-pcm`, `G2-membrane-eo-fast`, `G3-membrane-pcm-eo`, `H1-membrane-brush-nv`, `H4-volumetric-tensor-membrane`.
- **Feasibility simulations:** roadmap S1–S4/E1–E4 and models/results (`model_feasibility_roadmap.py`, `model_s1_link_thermal.py`, `model_s3_pcie_openvino.py`, `model_s4_variability_yield.py`, `outputs/*`, `figures/*`).
- **Public domain & defensive publication (intent):** `PUBLIC_DOMAIN_DEDICATION.md`, defensive disclosures in `DEFENSIVE_DISCLOSURES/`, all-versions publishing plan `PUBLISHING_ALL_VERSIONS_PLAN.md`. Current licenses remain (Apache-2.0 code, CERN-OHL-S v2 hardware, CC BY-SA 4.0 docs) pending rights-holder CC0 dedication.
- **Conflict-free packaging:** third-party redistributable spectral data excluded (see `data/spectra/photochemcad/README.md`).

No warranty, no FTO/patent guarantee. Use as open prior art/defensive disclosure of what is described.

---

## v0.7.1-research (tag: `v0.7.1-research`, commit 6666153)
**Title:** v0.7.1-research — Capacity axis in family development comparison

**Notes:**
Conceptual/simulation. Adds capacity axis to family development comparison and updates docs/outputs (`model_families_development.py`, `outputs/families_dev_*`, `figures/families_dev_*`). No measurements.

---

## v0.7.0-research (tag: `v0.7.0-research`, commit b9753cf)
**Title:** v0.7.0-research — Optical families/variants (fast response, interference)

**Notes:**
Conceptual/simulation. Adds optical families/variants (A–G, fast response, additive/destructive interference) and comparison model/docs (`hardware/families-and-variants.md`, `model_families_comparison.py`, outputs/figures). No measurements.

---

## v0.6.0-mission (tag: `v0.6.0-mission`, commit 1675866)
**Title:** v0.6.0-mission — Mission and open adoption reframing

**Notes:**
Reframes project mission for open adoption by third-party implementers (`MISSION_AND_ADOPTION.md`, README updates). Conceptual/simulation.

---

## v0.5.4-research (tag: `v0.5.4-research`, commit 800a1ee)
**Title:** v0.5.4-research — P3 variability, 4b/5b mode selection, M2 refresh

**Notes:**
Conceptual/simulation. P3 variability modeling, spatial variation, 4b/5b operating mode selection, M2 refresh policy and system profile (`model_variability_p3.py`, `hardware/p3-modeling-data.md`, `outputs/p3_*`).

---

## v0.5.3-research (tag: `v0.5.3-research`, commit b8c3cbb)
**Title:** v0.5.3-research — P2 reliability modeling and RAS system profile

**Notes:**
Conceptual/simulation. P2 reliability (noise/effective precision, endurance, retention) and RAS system profile (`model_reliability_p2.py`, `hardware/p2-modeling-data.md`, `outputs/reliability_p2_*`).

---

## v0.5.2-research (tag: `v0.5.2-research`, commit 0b724aa)
**Title:** v0.5.2-research — Integrate P1 parameters into system simulation

**Notes:**
Conceptual/simulation. Integrates P1 PCM/thermal parameters into system simulation for comparative data (`simulate_opgpu_system.py`, outputs).

---

## v0.5.1-research (tag: `v0.5.1-research`, commit ea3f930)
**Title:** v0.5.1-research — P1 modeling (PCM multilevel, thermal/crosstalk)

**Notes:**
Conceptual/simulation. P1 modeling with backing data: multilevel segmented/tapered Sb₂S₃ PCM cell and transient thermal/crosstalk (`model_pcm_multilevel.py`, `model_thermal_brush.py`, `hardware/p1-modeling-data.md`, outputs/figures).

---

## v0.5.0-hardware (tag: `v0.5.0-hardware`, commit 4f06017)
**Title:** v0.5.0-hardware — OMCC coprocessor, shared optical RAM, improvement research

**Notes:**
Conceptual hardware/research. Adds OMCC coprocessor with direct/shared access to optical RAM (M0–M3) and improvement research (`hardware/coprocessor-and-improvements.md`, system simulation updates).

---

## v0.4.0-hardware (tag: `v0.4.0-hardware`, commit ee48ebc)
**Title:** v0.4.0-hardware — OpenCL compatibility, NPU/TPU modes, deep schematics, system simulation

**Notes:**
Conceptual hardware. OpenCL mapping, NPU/TPU extensions, detailed schematics, and system simulation (`hardware/opencl-compatibility.md`, `hardware/npu-tpu-extensions.md`, `hardware/schematics-deep-dive.md`, `simulate_opgpu_system.py`).

---

## v0.3.0-hardware (tag: `v0.3.0-hardware`, commit b95641c)
**Title:** v0.3.0-hardware — OPGPU hardware integration (optical architecture, PCIe, brush-voxel)

**Notes:**
Conceptual hardware integration: predominantly optical architecture, PCIe coupling, brush-voxel 3D concept and schematics (`hardware/open-photonic-gpu-v1*.md`).

---

## v0.1.0-preprint (tag: `v0.1.0-preprint`, commit e84016d)
**Title:** v0.1.0-preprint — Initial open photonic voxel memory simulation package

**Notes:**
Initial reproducible simulation package (linear model, 4x4 readout, MZI, sensitivity, SNR, crosstalk, energy scenarios) with article drafts. Theoretical/simulation only.

---

## Nota común (todas las versiones)
- **Estado:** conceptual/simulado, no validado experimentalmente, no listo para fabricación/certificación. Sin garantía, sin FTO.
- **Dominio público / defensa:** intención de dominio público (CC0 1.0) y divulgación defensiva/arte previo (ver `PUBLIC_DOMAIN_DEDICATION.md`, `DEFENSIVE_DISCLOSURES/`, `PUBLISHING_ALL_VERSIONS_PLAN.md`); licencias vigentes del snapshot según archivos `LICENSE*` hasta transición por titulares.
- **Publicación:** con Zenodo vinculado, publicar cada release para archivar todas las versiones (DOI por versión + Concept DOI).
