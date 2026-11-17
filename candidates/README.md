# Repositorios candidatos (staging local)

Cada subdirectorio es un **proyecto independiente** (repo Git propio) enfocado en un candidato prioritario, listo para publicarse por separado. Objetivo: si un candidato recibe un cese y desista u otro bloqueo, **solo ese proyecto se retira** y los demás continúan.

| Candidato | Directorio | Foco | Estado |
|---|---|---|---|
| **H3 Open WDM-PCM** (A1+G1+B3) | `H3-open-wdm-pcm/` | Abierto/factible, bajo coste relativo, NV, pasivos por espesor $n d$ | P1 – prioritario |
| **G2 Membrane EO Fast** (G) | `G2-membrane-eo-fast/` | Velocidad/BW alta, interferencia $n d$ con sintonía EO, núcleo compacto | P1 – prioritario |
| **G3 Membrane PCM+EO** (G) | `G3-membrane-pcm-eo/` | Equilibrio NV + reconfiguración rápida, alta densidad | P1 – prioritario |
| **H1 Membrane-Brush NV** (A1+G3+3D) | `H1-membrane-brush-nv/` | Escalado volumétrico 3D, máxima capacidad NV modular | P1 – prioritario |
| **H4 Volumetric Tensor Membrane** | `H4-volumetric-tensor-membrane/` | Techo de capacidad/throughput, alto riesgo/integración | P1 – prioritario (aislar) |

Ver `../CANDIDATE_REPOS_STRATEGY.md` y `../outputs/objective_combo_analysis.md` para justificación y métricas. Cada carpeta incluye licencias, aviso y documentación enfocada; inicializar/publicar como repos separados según corresponda.