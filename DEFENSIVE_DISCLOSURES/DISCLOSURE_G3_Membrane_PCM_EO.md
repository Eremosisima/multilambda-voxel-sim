# Divulgación defensiva / arte previo — Estrategia G3: Thin-film Membrane Stack (PCM + EO hybrid)

- **Candidato:** G3 — Membranas F–P apiladas con estado base PCM + ajuste EO (prioridad P1: equilibrio NV + velocidad)
- **Versión/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: ____  | Commit/DOI/ID: [ ]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/G3-membrane-pcm-eo/`, `hardware/`)
- **Dedicación:** dominio público (CC0 1.0, objetivo) + divulgación defensiva/arte previo. Sin garantía, sin FTO.

## 1. Resumen técnico
Pila de **membranas/cavidades de película delgada** donde la interferencia por $n\cdot d$ define la función óptica: **PCM** aporta retención no volátil (estado/peso base) y **EO** aporta ajuste/reconfiguración rápida de índice. Ofrece alta densidad volumétrica con equilibrio entre capacidad NV y velocidad.

## 2. Esquemático e implementación (habilitante)
```text
Entrada (λ/WDM) → pila F–P multicapa
  - capa/volumen PCM (n_pcm conmutado por pulsos térmicos/ópticos, NV)
  - capa/elemento EO (Δn rápido por campo)
→ respuesta espectral/fase programable por (n·d, λ) → salida → O/E.
Secuenciación: programar base PCM (infrecuente) + modular EO (frecuente).
```

## 3. Parámetros/variantes (orientativos, simulados)
- Métricas conceptuales (v0.8): throughput ~5.0 TOPS/tile, NV ~256 MB/módulo, BW ~2.8 TB/s, reconfig ~0.5 ns (vía EO), factibilidad 2/5.
- Variantes: fracción PCM vs EO, número de cavidades, WDM, perfiles de pulso PCM, aislamiento térmico y redundancia.

## 4. Instrucciones operativas
1. Particionar estado persistente (PCM) y ajuste dinámico (EO).
2. Calibrar niveles PCM y respuesta EO; aplicar refresco/calibración según deriva.
3. Secuenciar escrituras PCM para minimizar crosstalk térmico con planos adyacentes.
4. Validar con S1/S2/S4 (márgenes, rendimiento, variabilidad/yield).

## 5. Declaración defensiva
Divulgación habilitante como **arte previo** con intención de **dominio público (CC0 1.0)** para uso/fabricación libre universal. Conceptual/simulado, sin garantía ni FTO.
