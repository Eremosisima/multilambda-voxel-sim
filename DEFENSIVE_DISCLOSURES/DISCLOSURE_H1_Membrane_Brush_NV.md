# Divulgación defensiva / arte previo — Estrategia H1: Membrane-Brush NV (A1 + G3 + 3D cepillo)

- **Candidato:** H1 — Membrane-Brush NV (prioridad P1: escalado volumétrico/capacidad NV)
- **Versión/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: ____  | Commit/DOI/ID: [ ]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/H1-membrane-brush-nv/`, `hardware/`)
- **Dedicación:** dominio público (CC0 1.0, objetivo) + divulgación defensiva/arte previo. Sin garantía, sin FTO.

## 1. Resumen técnico
Arquitectura **3D tipo cepillo** que apila capas/canales combinando **MZI-PCM no volátil (A1)** con **membranas PCM+EO (G3, interferencia por $n\cdot d$)**. Orientada a alta capacidad NV y throughput mediante integración volumétrica y modularidad por bloques.

## 2. Esquemático e implementación (habilitante)
```text
             (sección/apilado 3D "cepillo")
       ┌─ plano membrana G3 (canales F–P, n·d, PCM+EO) ─┐
λ/WDM ─┼─ plano MZI-PCM A1 (pesos NV, fase)             ├─ ... N planos ─ vías/guías verticales ─ combinador ─ O/E
       └─ plano(s) adicionales + distribución de control/térmica ┘
OMCC: direccionamiento por plano/vóxel, arbitraje M0–M3, calibración y RAS.
```

## 3. Parámetros/variantes (orientativos, simulados)
- Métricas conceptuales (v0.8): throughput ~9.0 TOPS/tile, NV ~640 MB/módulo, BW ~2.6 TB/s, factibilidad 2/5, alta densidad volumétrica.
- Variantes: número de planos, pitch, relación A1/G3, esquema de reparto óptico (broadcast/guías), partición térmica entre planos, spares por redundancia.

## 4. Instrucciones operativas
1. Diseñar partición térmica y guardas de crosstalk entre planos (crítico para PCM).
2. Calibrar por plano/celda (fase, niveles PCM, respuesta EO) y mantener mapas en OMCC.
3. Secuenciar escrituras NV y distribuir carga para cumplir ventanas térmicas (S1).
4. Evaluar yield/alineación 3D (S4) antes de escalar el apilado.

## 5. Declaración defensiva
Divulgación habilitante como **arte previo** con intención de **dominio público (CC0 1.0)** para uso/fabricación libre universal. Conceptual/simulado, sin garantía ni FTO.
