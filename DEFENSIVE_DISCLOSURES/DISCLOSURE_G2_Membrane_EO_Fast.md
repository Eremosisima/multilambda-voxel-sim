# Divulgación defensiva / arte previo — Estrategia G2: Thin-film Membrane Stack (EO-tuned), Fast Core

- **Candidato:** G2 — Membranas/cavidades F–P apiladas con sintonía electro-óptica (prioridad P1: velocidad/BW)
- **Versión/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: ____  | Commit/DOI/ID: [ ]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/G2-membrane-eo-fast/`, `hardware/`)
- **Dedicación:** dominio público (CC0 1.0, objetivo) + divulgación defensiva/arte previo. Sin garantía, sin FTO.

## 1. Resumen técnico
Núcleo rápido basado en **pilas de membranas/cavidades de película delgada (Fabry–Pérot)** cuya respuesta espectral se ajusta por **variación de índice electro-óptico (EO)**. El cómputo/selección de canal usa **interferencia constructiva/destructiva determinada por espesor óptico $n\cdot d$ y longitud de onda $\lambda$**, habilitando reconfiguración ps–ns, alto ancho de banda y alta densidad.

## 2. Esquemático e implementación (habilitante)
```text
Entrada óptica (λ/WDM) → acoplador/guía → [pila F–P: capas dieléctricas de espesor d, índice n(V)]
      n(V) modulable por campo EO (driver) → condición de resonancia/transmisión por canal (n·d, λ)
→ salida combinada → O/E (PD/TIA) / retroalimentación de control.
Control: drivers EO por canal/celda, bias térmico, calibración de fase/espectro.
```

## 3. Parámetros/variantes (orientativos, simulados)
- Diseño por $n\cdot d$ y Q de cavidad; sintonía EO (Δn por tensión/campo) para conmutación/reconfiguración rápida.
- Métricas conceptuales (v0.8): throughput ~5.5 TOPS/tile, BW ~3.2 TB/s, reconfig ~10 ps, latencia inferencia baja, factibilidad 2/5, overall top entre candidatos (simulado).
- Variantes: número de capas/cavidades, materiales EO, partición WDM, integración 2D/3D, arquitectura de driver (bloque sustituible por FTO/modularidad).

## 4. Instrucciones operativas
1. Definir apilado (d_i,n_i) y mapa canal↔λ.
2. Calibrar respuesta EO (tensión↔Δn↔desplazamiento espectral) y estabilidad térmica.
3. Operar con control de potencia/temperatura; desacoplar módulo EO para reemplazo si hay restricciones.
4. Validar presupuestos de enlace (S1) y E2E/colas (S3).

## 5. Declaración defensiva
Divulgación habilitante como **arte previo** con intención de **dominio público (CC0 1.0)** para uso/fabricación libre universal. Conceptual/simulado, sin garantía ni FTO.
