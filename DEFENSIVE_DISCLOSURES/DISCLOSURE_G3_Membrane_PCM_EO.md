# DivulgaciÃ³n defensiva / arte previo â€” Estrategia G3: Thin-film Membrane Stack (PCM + EO hybrid)

- **Candidato:** G3 â€” Membranas Fâ€“P apiladas con estado base PCM + ajuste EO (prioridad P1: equilibrio NV + velocidad)
- **VersiÃ³n/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: 2026-11-17  | Commit: cd58339/302cb2f/ba1cf7c (main) | Release: https://github.com/Eremosisima/multilambda-voxel-sim/releases/tag/v0.8.0-research | Zenodo DOI: pendiente (archivado tras releases) | ip.com ID: [PENDIENTE]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/G3-membrane-pcm-eo/`, `hardware/`)
- **DedicaciÃ³n:** dominio pÃºblico (CC0 1.0, objetivo) + divulgaciÃ³n defensiva/arte previo. Sin garantÃ­a, sin FTO.

## 1. Resumen tÃ©cnico
Pila de **membranas/cavidades de pelÃ­cula delgada** donde la interferencia por $n\cdot d$ define la funciÃ³n Ã³ptica: **PCM** aporta retenciÃ³n no volÃ¡til (estado/peso base) y **EO** aporta ajuste/reconfiguraciÃ³n rÃ¡pida de Ã­ndice. Ofrece alta densidad volumÃ©trica con equilibrio entre capacidad NV y velocidad.

## 2. EsquemÃ¡tico e implementaciÃ³n (habilitante)
```text
Entrada (Î»/WDM) â†’ pila Fâ€“P multicapa
  - capa/volumen PCM (n_pcm conmutado por pulsos tÃ©rmicos/Ã³pticos, NV)
  - capa/elemento EO (Î”n rÃ¡pido por campo)
â†’ respuesta espectral/fase programable por (nÂ·d, Î») â†’ salida â†’ O/E.
SecuenciaciÃ³n: programar base PCM (infrecuente) + modular EO (frecuente).
```

## 3. ParÃ¡metros/variantes (orientativos, simulados)
- MÃ©tricas conceptuales (v0.8): throughput ~5.0 TOPS/tile, NV ~256 MB/mÃ³dulo, BW ~2.8 TB/s, reconfig ~0.5 ns (vÃ­a EO), factibilidad 2/5.
- Variantes: fracciÃ³n PCM vs EO, nÃºmero de cavidades, WDM, perfiles de pulso PCM, aislamiento tÃ©rmico y redundancia.

## 4. Instrucciones operativas
1. Particionar estado persistente (PCM) y ajuste dinÃ¡mico (EO).
2. Calibrar niveles PCM y respuesta EO; aplicar refresco/calibraciÃ³n segÃºn deriva.
3. Secuenciar escrituras PCM para minimizar crosstalk tÃ©rmico con planos adyacentes.
4. Validar con S1/S2/S4 (mÃ¡rgenes, rendimiento, variabilidad/yield).

## 5. DeclaraciÃ³n defensiva
DivulgaciÃ³n habilitante como **arte previo** con intenciÃ³n de **dominio pÃºblico (CC0 1.0)** para uso/fabricaciÃ³n libre universal. Conceptual/simulado, sin garantÃ­a ni FTO.

