# OPGPU — Análisis de riesgos, estado del arte y mitigaciones por estrategia

> **Fecha:** 2026-11-19
> **Alcance:** trabajo conceptual/simulado (S1–S4). No son mediciones, ni BOM, ni FTO, ni garantía de rendimiento/fabricación. Las estimaciones numéricas provienen de los modelos del repositorio `open-photonic-gpu` (commit `499b613`, rama `main`).
> **Autores/titulares referenciados:** eremosisima; Contreras, Francisco Javier (sujeto a confirmación de consentimiento/CC0).

---

## 0. Resumen comparativo de riesgo

**Actualización 2026-11-19 (v0.9-disaggregated):** arquitectura revisada a "transceptor PCIe + módulo fotónico remoto por fibra con refrigeración líquida". Esto resuelve el riesgo térmico como limitante principal y relaja el factor forma.

| Candidato | Dimensión | Viabilidad actual (S4) | Yield efectivo (mejor ruta) | Riesgo global estimado | Probabilidad de éxito E2E (conceptual, 0–1) | Prioridad recomendada |
|---|---|---:|---:|:---:|:---:|---:|
| **H3** Open WDM-PCM | 2.5D | 0.676 | 0.86 | **Moderado-bajo** | **0.70–0.85** ↑ | **P1 (base)** |
| **G3** Membrana PCM+EO | 2.5D | 0.630 | 0.89 | **Moderado** | **0.60–0.75** ↑ | P1 (balance) |
| **G2** Membrana EO | 2.5D | 0.656 | 0.90 | **Moderado** | **0.55–0.70** ↑ | P1 (velocidad) |
| **H1** Brush NV 3D | 3D | 0.531 | 0.78 | **Alto** | **0.35–0.55** ↑ | P1 tras validar 2.5D |
| **H4** Tensor volumétrico 3D | 3D | 0.484 | 0.74 | **Muy alto** | **0.25–0.45** ↑ | P1 tras H1 |

*Probabilidades orientativas (conceptuales): combinan yield modelado, viabilidad de integración, madurez de plataforma, riesgo térmico, alineación 3D, FTO y dependencia de proceso. Las probabilidades aumentaron ~10–15% con arquitectura disaggregated (térmica resuelta, factor forma relajado). No son predicciones estadísticas.*

---

## 1. H3 — Open WDM-PCM (A1+G1+B3, 2.5D)

**Perfil:** ruta base de menor riesgo. Pasivos dieléctricos + referencia A1, NV, menor dependencia EO/RF sensible, acceso abierto.

**Cambio con arquitectura disaggregated:** el módulo fotónico H3 ahora reside en un módulo remoto con refrigeración líquida (cold plate o inmersión). Esto resuelve el riesgo térmico como limitante principal: duty-cycle PCM factible sube de ~0.12 a **0.5–1.0** (escritura continua sin violar margen VO2). Yield mejora (chip más grande o múltiples chips pequeños interconectados ópticamente). Acoplamiento fibra-chip con lentes/GRIN permite margen ±5 µm (IL 0.5–1.5 dB vs 2–5 dB en tarjeta PCIe).

### Principales riesgos
| # | Riesgo | Categoría | Impacto | Prob. | Mitigación | Estado del arte |
|---|---|---|---:|---:|---|---|
| 1 | **Térmica: escrituras PCM (~300 °C) afectan anillos/VO2 vecinos** | Térmica | **Bajo** (resuelto) | Baja | **Refrigeración líquida en módulo remoto** (cold plate/Fluorinert), duty-cycle 0.5–1.0 factible, secuenciado OMCC opcional. | Térmica era el limitante principal en tarjeta integrada. Con refrigeración líquida, el margen VO2 se mantiene incluso con escritura PCM continua. |
| 2 | **Deriva térmica de resonadores (anillos/WDM)** | Óptica/fase | Medio | Media | Calibración en lazo cerrado (A/B); diseño robusto a dn/dT (~80 pm/K). | Sintonía térmica de anillos es conocida; estabilización activa usada en PICs comerciales, pero consume potencia. |
| 3 | **Endurance PCM (ciclos hasta degradación)** | Fiabilidad | Medio | Baja-Media | Weight-stationary (baja fracción de reescritura); wear-leveling/re-mapeo OMCC. | PCM fotónica reporta ~10⁶ ciclos (modelo usado); suficiente para inferencia, limitada para entrenamiento continuo. |
| 4 | **IL acumulado y pérdida de enlace** | Óptica | Medio | Baja | MZIs + bancos WDM; IL modelado ~10.4 dB con margen de enlace ≥10.6 dB (S1). | PIs con IL ≤10 dB son factibles; el margen se reduce con cruces y longitud. |
| 5 | **Variabilidad de proceso (n, d, acoplamientos)** | Fabricación | Medio | Media | Monte Carlo + ECC + spares (S4: yield efectivo 0.86 con optimización). | 2.5D con procesos SiPh estándar (foundry abierta) es maduro; variabilidad de PCM es el factor dominante. |
| 6 | **FTO / patentes de terceros (PCM fotónica, WDM banks)** | Legal/IP | Medio | Media | Divulgación defensiva (TDCommons, Zenodo, GitHub), arquitectura abierta, uso de referencias públicas (A1, B3). | Existe IP activa en PCM fotónica y resonadores; la apertura + prior art reduce riesgo pero no lo elimina. |
| 7 | **Escalado a WS/DC (más módulos)** | Sistema | Bajo | Baja | Plataforma común PCIe/DMA + colas OMCC (S3). | Escalado multi-chip con PCIe/Gen4 es conocido; latencia E2E modelada 0.16–12 ms por carga. |

**Atenuación de señales (riesgo óptico):**
- IL total ruta: **~10.4 dB** (modelo S1). Principal fuente: cruces, acoplamientos, propagación.
- ER objetivo: **≥10 dB** para BER ≤1e-9 con láser ≥8 dBm (S1 sensitivity).
- SNR medio modelado: **~13.2 dB** (p5: 12.6 dB); calibración en lazo cerrado recupera margen.
- Pérdida dominante en peor caso: térmica cruzada entre celdas PCM y anillos vecinos.

---

## 2. G3 — Membrana PCM+EO híbrida (2.5D)

**Perfil:** equilibrio NV + ajuste rápido. Co-integración PCM (NV) + EO (trim/reconfig rápida).

### Principales riesgos
| # | Riesgo | Categoría | Impacto | Prob. | Mitigación | Estado del arte |
|---|---|---|---:|---:|---|---|
| 1 | **Co-integración térmica PCM/EO (aislamiento local)** | Térmica/fabricación | Alto | Media-Alta | Trenches locales, duty-cycled writes, secuenciado OMCC; aislamiento entre zonas PCM y EO. | Membranas híbridas PCM+EO son emergentes; co-integración monolítica reportada en prototipos, pero térmica PCM sigue siendo limitante. |
| 2 | **Degradación cruzada PCM→EO (estrés térmico en materiales EO)** | Fiabilidad | Alto | Media | Secuenciado estricto, buffers térmicos, caracterización de deriva post-escritura. | Materiales EO (p. ej. LiNbO3 thin-film, polímeros) son sensibles a 300 °C; compatibilidad depende de stack. |
| 3 | **IL mayor que H3 (rutas híbridas más complejas)** | Óptica | Medio | Media | Diseño de acopladores optimizado; IL modelado ~7.1 dB (mejor que H3 en ruta directa). | Membranas delgadas reducen longitud efectiva; acoplamientos fibra-chip siguen siendo reto en PICs. |
| 4 | **Repetibilidad multinivel PCM** | Fiabilidad | Medio | Media | Calibración en lazo cerrado, niveles cuantizados, ECC. | Multinivel PCM fotónica reportada experimentalmente (4–5 bits/celda en demostradores); repetibilidad a largo plazo aún en estudio. |
| 5 | **Yield de proceso (variabilidad híbrida)** | Fabricación | Medio | Media | Optimización (EO trim + scheduling PCM + improved coupling): yield efectivo 0.89 (S4). | Procesos híbridos (SiPh + PCM + EO) requieren más pasos y metrología; yield típico menor que SiPh puro. |
| 6 | **FTO / IP en EO thin-film (LiNbO3, BaTiO3, polímeros)** | Legal/IP | Medio | Media | Uso de plataformas abiertas (A1/G1) + divulgación defensiva. | LiNbO3 thin-film tiene IP activa; polímeros EO y BaTiO3 tienen menos restricciones pero madurez variable. |
| 7 | **Dependencia de drivers EO/RF** | Sistema | Bajo-Medio | Media | Plataforma común; drivers discretos o integrados según volumen. | Drivers EO de alta velocidad son comerciales pero costosos; integración monolítica es investigación activa. |

**Atenuación de señales:**
- IL total ruta: **~7.1 dB** (mejor que H3).
- ER objetivo: **≥10 dB**, láser ≥4 dBm (S1).
- SNR medio modelado: **~14.8 dB** (p5: 14.1 dB); mejor margen que H3.
- Principal pérdida: acoplamiento híbrido y cruces PCM↔EO.

---

## 3. G2 — Membrana EO sintonizada (2.5D)

**Perfil:** máxima velocidad de reconfiguración (EO, ps–ns). Sin escritura PCM 300 °C. Capacidad NV limitada.

### Principales riesgos
| # | Riesgo | Categoría | Impacto | Prob. | Mitigación | Estado del arte |
|---|---|---|---:|---:|---|---|
| 1 | **Persistencia NV limitada (volatilidad EO)** | Memoria | Alto | Alta | Refresco M2 (VO2), buffer externo, weight-stationary con reload periódico. | EO es intrínsecamente volátil; persistencia depende de arquitectura de refresco. |
| 2 | **Dependencia de plataforma/driver EO** | Sistema/Fabricación | Alto | Media | Plataforma común; drivers comerciales o discretos; aislamiento modular. | LiNbO3 thin-film, polímeros EO, BaTiO3: madurez y coste variables. |
| 3 | **Consumo de drivers EO/RF a alta velocidad** | Energía | Medio | Media | Diseño de bajo consumo, duty-cycle, batching. | Drivers EO de alta velocidad consumen significativo; optimización activa en PICs. |
| 4 | **Estabilidad de resonadores bajo sintonía EO** | Óptica | Medio | Media | EO trim + resonator stabilization + spare channels (S4); yield efectivo 0.90. | Sintonía EO de resonadores es bien estudiada; deriva por envejecimiento/temperatura requiere calibración. |
| 5 | **IL y acoplamiento en membranas EO** | Óptica | Medio | Baja-Media | Diseño de acopladores; IL modelado ~6.7 dB (mejor entre candidatos). | Membranas EO delgadas tienen acoplamiento eficiente en demostradores; escalado industrial en progreso. |
| 6 | **FTO / IP en LiNbO3 thin-film y drivers EO** | Legal/IP | Medio | Media | Plataformas alternativas (polímeros EO) + divulgación defensiva. | IP activa en LiNbO3 thin-film (procesos patentados); polímeros EO tienen menos restricciones. |
| 7 | **Sensibilidad a ruido de fase/jitter en alta velocidad** | Óptica/sistema | Medio | Media | Diseño de margen, calibración, ECC. | Ruido de fase en moduladores EO de alta velocidad es conocido; mitigación con diseño y calibración. |

**Atenuación de señales:**
- IL total ruta: **~6.7 dB** (mejor entre candidatos 2.5D).
- ER objetivo: **≥10 dB**, láser ≥4 dBm (S1).
- SNR medio modelado: **~13.5–14 dB** (depende de configuración EO).
- Principal ventaja: sin pérdida térmica PCM; principal debilidad: volatilidad.

---

## 4. H1 — Membrane-Brush NV 3D (A1+G3+3D)

**Perfil:** alta capacidad volumétrica NV. Mayor riesgo por integración 3D, alineación, térmica y yield.

### Principales riesgos
| # | Riesgo | Categoría | Impacto | Prob. | Mitigación | Estado del arte |
|---|---|---|---:|---:|---|---|
| 1 | **Integración 3D (alineación interplano, yield por plano)** | Fabricación | Muy alto | Alta | Modular 3D partitioning + re-mapping spares + thermal vias/manifold; proceso mejorado (metrología/calibrada). | 3D photonic integration es investigación activa; demostradores limitados, yield y alineación son retos principales. |
| 2 | **Extracción de calor 3D (manifold, secuenciado estricto)** | Térmica | Muy alto | Alta | Strict OMCC sequencing + vertical/lateral isolation + manifold cooling; duty ≤0.12 en peor caso (S1). | Disipación 3D es limitante conocida en electrónica y fotónica; manifold cooling es solución emergente. |
| 3 | **IL acumulado por planos (cruces, vías, longitud)** | Óptica | Alto | Alta | Diseño de rutas cortas, acopladores eficientes; IL modelado ~11.1 dB. | IL en 3D crece con planos; demostradores reportan 10–15 dB en stacks simples. |
| 4 | **Yield efectivo bajo en baseline (0.796)** | Fabricación | Alto | Alta | Proceso mejorado + optimización: yield efectivo 0.78 (S4, aún bajo vs 2.5D). | Yield en 3D fotónica es típicamente menor que 2.5D; requiere control de proceso estricto. |
| 5 | **Crosstalk térmico/óptico entre planos** | Térmica/óptica | Alto | Media-Alta | Aislamiento vertical/lateral, secuenciado, layout spread-out. | Crosstalk 3D es reportado en literatura; mitigación con diseño y espaciado. |
| 6 | **FTO / IP en integración 3D fotónica** | Legal/IP | Medio | Media | Divulgación defensiva, uso de referencias abiertas. | 3D integration tiene IP activa en empaquetado y procesos; menos en arquitecturas específicas. |
| 7 | **Empaquetado y termomecánica (CTE, estrés)** | Fabricación | Medio | Media | Diseño de CTE匹配, buffers, caracterización. | Empaquetado 3D fotónico es reto industrial; soluciones en progreso. |

**Atenuación de señales:**
- IL total ruta: **~11.1 dB** (mayor que 2.5D).
- ER objetivo: **≥10 dB**, láser ≥8 dBm (S1).
- SNR medio modelado: **~11.3 dB** (p5: 10.5 dB); menor margen que 2.5D.
- Principal pérdida: cruces interplano y longitud acumulada.

---

## 5. H4 — Volumetric Tensor Membrane (G2/G3+F2+A1, 3D)

**Perfil:** techo de capacidad/throughput. Mayor riesgo y sensibilidad de proceso. Integración muy exigente.

### Principales riesgos
| # | Riesgo | Categoría | Impacto | Prob. | Mitigación | Estado del arte |
|---|---|---|---:|---:|---|---|
| 1 | **Integración 3D compleja (híbrida: G2/G3+F2+A1)** | Fabricación | Muy alto | Muy alta | Hierarchical partitioning + alignment/calibration loops + higher redundancy; pilot-line stabilized. | Integración híbrida 3D (EO+PCM+diffractiva) no tiene demostradores maduros; es exploratoria. |
| 2 | **Térmica distribuida y activa (múltiples fuentes)** | Térmica | Muy alto | Muy alta | Aggressive sequencing + high-capacity spreading/manifold + active stabilization; duty ≤0.18 spread-out (S1). | Disipación en stacks híbridos es limitante crítico; active stabilization consume potencia. |
| 3 | **IL muy alto (rutas complejas, difractiva)** | Óptica | Muy alto | Alta | Diseño optimizado; IL modelado ~12.4 dB (mayor entre candidatos). | IL en sistemas difractivos 3D es alto; eficiencia de funciones difractivas depende de fabricación. |
| 4 | **Yield efectivo muy bajo en baseline (0.592)** | Fabricación | Muy alto | Muy alta | Pilot-line stabilized + optimización: yield efectivo 0.74 (S4, aún bajo). | Yield en 3D híbrido es típicamente muy bajo; requiere control de proceso de vanguardia. |
| 5 | **Alineación/calibración multi-eje** | Fabricación/sistema | Alto | Alta | Calibration loops + metrología; redundancia (26% área). | Alineación sub-micrométrica en 3D es reto; metrología avanzada necesaria. |
| 6 | **Sensibilidad a variabilidad de proceso** | Fabricación | Alto | Alta | Proceso pilot-line stabilized; redundancia, ECC, re-mapeo. | Variabilidad en procesos híbridos 3D es alta; control estadístico necesario. |
| 7 | **FTO / IP en difractiva 3D y metasuperficies** | Legal/IP | Medio-Alto | Media | Divulgación defensiva, uso de referencias abiertas. | Metasuperficies/diffractiva tienen IP activa; arquitecturas específicas pueden tener restricciones. |
| 8 | **H4 no alcanza umbral BER en barrido láser/ER (modelo)** | Óptica/sistema | Alto | Media | Requiere mayor ER, láser más potente, calibración fina; validación con mediciones. | Modelo S1 indica H4 no alcanza BER ≤1e-9 en barrido nominal; requiere optimización. |

**Atenuación de señales:**
- IL total ruta: **~12.4 dB** (mayor entre candidatos).
- ER objetivo: **≥10 dB**, pero **H4 no alcanza umbral BER ≤1e-9** en barrido nominal (S1 sensitivity); requiere ER mayor, láser ≥10 dBm o calibración avanzada.
- SNR medio modelado: **~10.5 dB** (p5: 9.6 dB); menor margen.
- Principal pérdida: rutas complejas, difractiva, cruces 3D.

---

## 6. Riesgos transversales (todas las estrategias)

| # | Riesgo transversal | Categoría | Impacto | Prob. | Mitigación global |
|---|---|---|---:|---:|---|
| T1 | **Sin validación experimental (S1–S4 son simulaciones)** | Metodológico | Alto | 1.0 | Transición E1–E4 con metrología; recalibración de modelos. |
| T2 | **Dependencia de proceso/foundry no definida** | Fabricación | Alto | Alta | Definir proceso objetivo (SiPh abierto, foundry comercial); caracterización E1. |
| T3 | **FTO no garantizado (patentes de terceros)** | Legal/IP | Alto | Media | Divulgación defensiva (TDCommons, Zenodo, GitHub), prior art, búsqueda FTO específica antes de fabricación. |
| T4 | **Sin BOM/coste real (estimaciones conceptuales)** | Económico | Medio | Alta | Definir BOM, volumen, cadena de suministro; cotización con foundries/fabricantes. |
| T5 | **Sin certificación/compliance (laser safety, EMC, etc.)** | Regulatorio | Medio | Media | Evaluación de riesgos, EPP, compliance normativo en laboratorio/fabricación. |
| T6 | **CC0 no efectiva aún (pendiente consentimiento titulares)** | Legal/IP | Medio | Media | Confirmar consentimiento, ejecutar `PUBLIC_DOMAIN_DEDICATION.md`. |
| T7 | **Sin FEM 3D transitorio / FDTD / RTL real** | Técnico | Medio | Alta | Herramientas externas; validación con simuladores comerciales/académicos. |
| T8 | **Escalado de sistema (colas, batching, partición OpenVINO)** | Sistema | Medio | Media | S3 modelado; validación con trazas reales de kernels (GEMM/conv/attention). |

---

## 7. Recomendaciones de priorización

1. **H3 (base):** menor riesgo global, mayor viabilidad, acceso abierto. Iniciar E1 con H3 para cerrar S1–S4 con datos medidos.
2. **G3/G2 (balance/velocidad):** madurar en paralelo con H3; aislamiento modular de dependencias EO/RF.
3. **H1/H4 (capacidad 3D):** solo tras validar 2.5D (H3/G3) y madurar térmica 3D, yield y empaquetado.
4. **Divulgación defensiva:** mantener TDCommons/Zenodo/GitHub actualizados para fortalecer prior art.
5. **Búsqueda FTO específica:** antes de cualquier inversión en fabricación, realizar búsqueda de patentes por candidato/región.

---

## 8. Notas metodológicas

- **Probabilidades de éxito:** estimaciones conceptuales basadas en yield modelado, viabilidad de integración, madurez de plataforma y riesgo térmico/óptico. No son predicciones estadísticas; sirven como guía de priorización.
- **Atenuación de señales:** valores de IL, SNR, ER provienen de modelos S1 (enlace/térmica) y S4 (variabilidad/yield). Requieren recalibración con mediciones E1.
- **Estado del arte:** referencias generales (Wuttig et al., 2017; Feldmann et al., 2019; literatura SiPh/PCM/EO). No es revisión sistemática.
- **FTO:** la divulgación defensiva crea prior art pero no garantiza libertad de operación. Búsqueda de patentes específica es necesaria antes de fabricación/comercialización.

---

*Documento conceptual; no constituye asesoría legal, ni diseño listo para fabricación, ni garantía de rendimiento/FTO.*
