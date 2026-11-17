# DivulgaciÃ³n defensiva / arte previo â€” Estrategia H1: Membrane-Brush NV (A1 + G3 + 3D cepillo)

- **Candidato:** H1 â€” Membrane-Brush NV (prioridad P1: escalado volumÃ©trico/capacidad NV)
- **VersiÃ³n/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: 2026-11-17  | Commit: cd58339/302cb2f/ba1cf7c (main) | Release: https://github.com/Eremosisima/multilambda-voxel-sim/releases/tag/v0.8.0-research | Zenodo DOI: pendiente (archivado tras releases) | ip.com ID: [PENDIENTE]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/H1-membrane-brush-nv/`, `hardware/`)
- **DedicaciÃ³n:** dominio pÃºblico (CC0 1.0, objetivo) + divulgaciÃ³n defensiva/arte previo. Sin garantÃ­a, sin FTO.

## 1. Resumen tÃ©cnico
Arquitectura **3D tipo cepillo** que apila capas/canales combinando **MZI-PCM no volÃ¡til (A1)** con **membranas PCM+EO (G3, interferencia por $n\cdot d$)**. Orientada a alta capacidad NV y throughput mediante integraciÃ³n volumÃ©trica y modularidad por bloques.

## 2. EsquemÃ¡tico e implementaciÃ³n (habilitante)
```text
             (secciÃ³n/apilado 3D "cepillo")
       â”Œâ”€ plano membrana G3 (canales Fâ€“P, nÂ·d, PCM+EO) â”€â”
Î»/WDM â”€â”¼â”€ plano MZI-PCM A1 (pesos NV, fase)             â”œâ”€ ... N planos â”€ vÃ­as/guÃ­as verticales â”€ combinador â”€ O/E
       â””â”€ plano(s) adicionales + distribuciÃ³n de control/tÃ©rmica â”˜
OMCC: direccionamiento por plano/vÃ³xel, arbitraje M0â€“M3, calibraciÃ³n y RAS.
```

## 3. ParÃ¡metros/variantes (orientativos, simulados)
- MÃ©tricas conceptuales (v0.8): throughput ~9.0 TOPS/tile, NV ~640 MB/mÃ³dulo, BW ~2.6 TB/s, factibilidad 2/5, alta densidad volumÃ©trica.
- Variantes: nÃºmero de planos, pitch, relaciÃ³n A1/G3, esquema de reparto Ã³ptico (broadcast/guÃ­as), particiÃ³n tÃ©rmica entre planos, spares por redundancia.

## 4. Instrucciones operativas
1. DiseÃ±ar particiÃ³n tÃ©rmica y guardas de crosstalk entre planos (crÃ­tico para PCM).
2. Calibrar por plano/celda (fase, niveles PCM, respuesta EO) y mantener mapas en OMCC.
3. Secuenciar escrituras NV y distribuir carga para cumplir ventanas tÃ©rmicas (S1).
4. Evaluar yield/alineaciÃ³n 3D (S4) antes de escalar el apilado.

## 5. DeclaraciÃ³n defensiva
DivulgaciÃ³n habilitante como **arte previo** con intenciÃ³n de **dominio pÃºblico (CC0 1.0)** para uso/fabricaciÃ³n libre universal. Conceptual/simulado, sin garantÃ­a ni FTO.

