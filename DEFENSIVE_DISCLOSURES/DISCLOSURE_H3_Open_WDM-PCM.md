# Divulgación defensiva / arte previo — Estrategia H3: Open WDM-PCM (A1 + G1 + B3)

- **Candidato:** H3 — Open WDM-PCM (prioridad P1: abierto/factible)
- **Versión/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: ____  | Commit/DOI/ID: [ ]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/H3-open-wdm-pcm/`, `hardware/`)
- **Dedicación:** dominio público (CC0 1.0, objetivo) + divulgación defensiva/arte previo. Sin garantía, sin FTO.

## 1. Resumen técnico
Combinación de **pesos/cómputo PCM-MZI no volátil (A1, Sb₂S₃)** + **membranas/filtros pasivos de película delgada de espesor fijo (G1, interferencia por $n\cdot d$)** + **banco resonante/WDM (B3)**. Busca alta capacidad no volátil con máxima factibilidad y menor coste relativo usando elementos pasivos dieléctricos y principios conocidos (F–P/película delgada, MZI, WDM).

## 2. Esquemático e implementación (habilitante)
```text
λ1..λn ─ MUX/WDM ─┬─ banco microrings/filtros resonantes (B3) ────────┐
                  └─ celdas MZI con fase/peso PCM Sb₂S₃ (A1, NV) ────┤─ combinador ─ O/E (PD/TIA)
Elementos G1: láminas/filtros pasivos de espesor fijo d, índice n (selección por n·d, λ)
Control: pulsos ópticos/térmicos de escritura PCM (set/reset multinivel), sesgo/calibración, lectura interferométrica.
Memoria: M3 NV en PCM; M1/M0 por propagación/resonancia; gestión OMCC.
```

## 3. Parámetros/variantes (orientativos, simulados)
- PCM Sb₂S₃ multinivel (celdas segmentadas/tapered), escritura por pulsos controlados; modos 4b/5b según ruido/variabilidad.
- Canales WDM λ1..λn; filtros G1 por espesor óptico $n\cdot d$; resonadores B3 para densidad/espectro.
- Métricas conceptuales (v0.8): throughput ~3.5 TOPS/tile, NV ~160 MB/módulo, BW ~1.6 TB/s, factibilidad relativa alta (3/5), coste relativo bajo, perfil abierto.
- Variantes: número de canales, geometría MZI, apilado G1, partición térmica, redundancia/spares.

## 4. Instrucciones operativas
1. Calibrar mapa fase↔nivel PCM (multinivel) y compensar deriva.
2. Cargar pesos estacionarios (inferencia NV) y usar WDM para paralelismo.
3. Secuenciar escritura PCM para limitar crosstalk térmico; monitorizar con OMCC/RAS.
4. Verificar márgenes de enlace/térmico (S1) y rendimiento sistema (S2) antes de escalar.

## 5. Declaración defensiva
Divulgación habilitante publicada como **arte previo** para impedir registro/patente de lo descrito por terceros, y con intención de **dominio público (CC0 1.0)** para uso/fabricación libre universal. Conceptual/simulado, sin garantía ni FTO.
