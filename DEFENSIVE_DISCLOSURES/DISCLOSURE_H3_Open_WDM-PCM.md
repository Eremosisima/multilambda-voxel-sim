# DivulgaciÃ³n defensiva / arte previo â€” Estrategia H3: Open WDM-PCM (A1 + G1 + B3)

- **Candidato:** H3 â€” Open WDM-PCM (prioridad P1: abierto/factible)
- **VersiÃ³n/estado:** v0.8.0-research (conceptual/simulado), [FECHA]: 2026-11-17  | Commit: cd58339/302cb2f/ba1cf7c (main) | Release: https://github.com/Eremosisima/multilambda-voxel-sim/releases/tag/v0.8.0-research | Zenodo DOI: pendiente (archivado tras releases) | ip.com ID: [PENDIENTE]
- **Autores/titulares:** [COMPLETAR] (consentimiento CC0/DP). **Fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`candidates/H3-open-wdm-pcm/`, `hardware/`)
- **DedicaciÃ³n:** dominio pÃºblico (CC0 1.0, objetivo) + divulgaciÃ³n defensiva/arte previo. Sin garantÃ­a, sin FTO.

## 1. Resumen tÃ©cnico
CombinaciÃ³n de **pesos/cÃ³mputo PCM-MZI no volÃ¡til (A1, Sbâ‚‚Sâ‚ƒ)** + **membranas/filtros pasivos de pelÃ­cula delgada de espesor fijo (G1, interferencia por $n\cdot d$)** + **banco resonante/WDM (B3)**. Busca alta capacidad no volÃ¡til con mÃ¡xima factibilidad y menor coste relativo usando elementos pasivos dielÃ©ctricos y principios conocidos (Fâ€“P/pelÃ­cula delgada, MZI, WDM).

## 2. EsquemÃ¡tico e implementaciÃ³n (habilitante)
```text
Î»1..Î»n â”€ MUX/WDM â”€â”¬â”€ banco microrings/filtros resonantes (B3) â”€â”€â”€â”€â”€â”€â”€â”€â”
                  â””â”€ celdas MZI con fase/peso PCM Sbâ‚‚Sâ‚ƒ (A1, NV) â”€â”€â”€â”€â”¤â”€ combinador â”€ O/E (PD/TIA)
Elementos G1: lÃ¡minas/filtros pasivos de espesor fijo d, Ã­ndice n (selecciÃ³n por nÂ·d, Î»)
Control: pulsos Ã³pticos/tÃ©rmicos de escritura PCM (set/reset multinivel), sesgo/calibraciÃ³n, lectura interferomÃ©trica.
Memoria: M3 NV en PCM; M1/M0 por propagaciÃ³n/resonancia; gestiÃ³n OMCC.
```

## 3. ParÃ¡metros/variantes (orientativos, simulados)
- PCM Sbâ‚‚Sâ‚ƒ multinivel (celdas segmentadas/tapered), escritura por pulsos controlados; modos 4b/5b segÃºn ruido/variabilidad.
- Canales WDM Î»1..Î»n; filtros G1 por espesor Ã³ptico $n\cdot d$; resonadores B3 para densidad/espectro.
- MÃ©tricas conceptuales (v0.8): throughput ~3.5 TOPS/tile, NV ~160 MB/mÃ³dulo, BW ~1.6 TB/s, factibilidad relativa alta (3/5), coste relativo bajo, perfil abierto.
- Variantes: nÃºmero de canales, geometrÃ­a MZI, apilado G1, particiÃ³n tÃ©rmica, redundancia/spares.

## 4. Instrucciones operativas
1. Calibrar mapa faseâ†”nivel PCM (multinivel) y compensar deriva.
2. Cargar pesos estacionarios (inferencia NV) y usar WDM para paralelismo.
3. Secuenciar escritura PCM para limitar crosstalk tÃ©rmico; monitorizar con OMCC/RAS.
4. Verificar mÃ¡rgenes de enlace/tÃ©rmico (S1) y rendimiento sistema (S2) antes de escalar.

## 5. DeclaraciÃ³n defensiva
DivulgaciÃ³n habilitante publicada como **arte previo** para impedir registro/patente de lo descrito por terceros, y con intenciÃ³n de **dominio pÃºblico (CC0 1.0)** para uso/fabricaciÃ³n libre universal. Conceptual/simulado, sin garantÃ­a ni FTO.

