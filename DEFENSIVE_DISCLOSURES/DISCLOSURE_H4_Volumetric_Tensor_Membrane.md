# Divulgación defensiva / arte previo — Estrategia H4: Volumetric Tensor Membrane (G2/G3 + F2 + A1)

- **Candidato:** H4 — Volumetric Tensor Membrane (prioridad P1: techo de capacidad/throughput; alto riesgo, aislar)
- **Versión/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: ____  | Commit/DOI/ID: [ ]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/H4-volumetric-tensor-membrane/`, `hardware/`)
- **Dedicación:** dominio público (CC0 1.0, objetivo) + divulgación defensiva/arte previo. Sin garantía, sin FTO.

## 1. Resumen técnico
Combinación de **núcleos de membrana apilada 3D (G2/G3, interferencia por $n\cdot d$)** + **etapa difractiva/metasuperficie (F2) para mezcla/transformación espacial global** + **celdas PCM no volátiles (A1)** donde convenga. Apunta al máximo de capacidad/throughput (volumétrico + espacial + WDM) con mayor complejidad e integración.

## 2. Esquemático e implementación (habilitante)
```text
Entrada (λ/WDM, distribución) 
  → apilado 3D de membranas/cavidades (G2 EO rápido y/o G3 PCM+EO, por planos/canales)
  → etapa F2 difractiva/metasuperficie (mezcla/tensorización espacial, pesos/patrones programados o fijos según variante)
  → celdas A1 PCM (estado NV/ponderación local donde aplique)
  → O/E (PD/TIA) → buffers/host.
Control: drivers EO, escritura PCM, alineación 3D, OMCC (M0–M3, RAS).
```

## 3. Parámetros/variantes (orientativos, simulados)
- Métricas conceptuales (v0.8): throughput ~10.0 TOPS/tile (techo), NV ~720 MB/módulo, BW ~3.5 TB/s, factibilidad 1/5 (alto riesgo), coste relativo alto.
- Variantes: proporción G2/G3, función F2 (fija vs reconfigurable), reparto de PCM, número de planos, topología de interconexión y empaquetado 3D.

## 4. Instrucciones operativas y riesgos
1. **Aislar** como candidato independiente (no bloquear otros si hay C&D/bloqueo).
2. Control estricto de alineación 3D, pérdidas, diafonía y térmica; validar yield (S4).
3. Calibración por etapa (membranas, F2, PCM) y partición de modos GPU/NPU/TPU por bloque.
4. Tratar estimaciones como techo conceptual sujeto a validación S1–S4 y experimentos E1–E4.

## 5. Declaración defensiva
Divulgación habilitante como **arte previo** con intención de **dominio público (CC0 1.0)** para uso/fabricación libre universal. Conceptual/simulado, alto riesgo, sin garantía ni FTO.
