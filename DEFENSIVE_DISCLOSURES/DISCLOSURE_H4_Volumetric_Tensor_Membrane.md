# DivulgaciÃ³n defensiva / arte previo â€” Estrategia H4: Volumetric Tensor Membrane (G2/G3 + F2 + A1)

- **Candidato:** H4 â€” Volumetric Tensor Membrane (prioridad P1: techo de capacidad/throughput; alto riesgo, aislar)
- **VersiÃ³n/estado:** v0.8.0-research (conceptual/simulado), [FECHA de preparación/actualización]: 2026-11-19 (base v0.8: 2026-11-17)  | Commit base v0.8: cd58339/302cb2f/ba1cf7c; actualización: 5c4a1f8 (main) | Release v0.8: https://github.com/Eremosisima/multilambda-voxel-sim/releases/tag/v0.8.0-research | Zenodo: Concept DOI: 10.5281/zenodo.24323250; DOI versión v0.3.0-hardware (publicado): 10.5281/zenodo.24374387; DOIs por versión restantes: pendientes de confirmar/registrar | ip.com ID: [PENDIENTE TRAS ENVÍO]
- **Autores/titulares:** eremosisima; Contreras, Francisco Javier (confirmar afiliación/ORCID y consentimiento explícito de dedicación CC0 por todos los titulares). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/H4-volumetric-tensor-membrane/`, `hardware/`)
- **DedicaciÃ³n:** dominio pÃºblico (CC0 1.0, objetivo) + divulgaciÃ³n defensiva/arte previo. Sin garantÃ­a, sin FTO.

## 1. Resumen tÃ©cnico
CombinaciÃ³n de **nÃºcleos de membrana apilada 3D (G2/G3, interferencia por $n\cdot d$)** + **etapa difractiva/metasuperficie (F2) para mezcla/transformaciÃ³n espacial global** + **celdas PCM no volÃ¡tiles (A1)** donde convenga. Apunta al mÃ¡ximo de capacidad/throughput (volumÃ©trico + espacial + WDM) con mayor complejidad e integraciÃ³n.

## 2. EsquemÃ¡tico e implementaciÃ³n (habilitante)
```text
Entrada (Î»/WDM, distribuciÃ³n) 
  â†’ apilado 3D de membranas/cavidades (G2 EO rÃ¡pido y/o G3 PCM+EO, por planos/canales)
  â†’ etapa F2 difractiva/metasuperficie (mezcla/tensorizaciÃ³n espacial, pesos/patrones programados o fijos segÃºn variante)
  â†’ celdas A1 PCM (estado NV/ponderaciÃ³n local donde aplique)
  â†’ O/E (PD/TIA) â†’ buffers/host.
Control: drivers EO, escritura PCM, alineaciÃ³n 3D, OMCC (M0â€“M3, RAS).
```

## 3. ParÃ¡metros/variantes (orientativos, simulados)
- MÃ©tricas conceptuales (v0.8): throughput ~10.0 TOPS/tile (techo), NV ~720 MB/mÃ³dulo, BW ~3.5 TB/s, factibilidad 1/5 (alto riesgo), coste relativo alto.
- Variantes: proporciÃ³n G2/G3, funciÃ³n F2 (fija vs reconfigurable), reparto de PCM, nÃºmero de planos, topologÃ­a de interconexiÃ³n y empaquetado 3D.

## 4. Instrucciones operativas y riesgos
1. **Aislar** como candidato independiente (no bloquear otros si hay C&D/bloqueo).
2. Control estricto de alineaciÃ³n 3D, pÃ©rdidas, diafonÃ­a y tÃ©rmica; validar yield (S4).
3. CalibraciÃ³n por etapa (membranas, F2, PCM) y particiÃ³n de modos GPU/NPU/TPU por bloque.
4. Tratar estimaciones como techo conceptual sujeto a validaciÃ³n S1â€“S4 y experimentos E1â€“E4.

## 5. DeclaraciÃ³n defensiva
DivulgaciÃ³n habilitante como **arte previo** con intenciÃ³n de **dominio pÃºblico (CC0 1.0)** para uso/fabricaciÃ³n libre universal. Conceptual/simulado, alto riesgo, sin garantÃ­a ni FTO.

