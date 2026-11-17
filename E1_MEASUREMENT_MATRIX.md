# E1 — Matriz de parámetros medibles y preparación experimental

> **Objetivo:** definir qué medir por familia/candidato para recalibrar modelos S1–S4 y habilitar transición simulación→experimento (roadmap E1–E4). Conceptual/preparatorio (no sustituye protocolos de laboratorio ni seguridad).

## 1. Parámetros medibles comunes (por dispositivo/celda/módulo)

| Dominio | Parámetro | Símbolo/unidad | Método/instrumentación típica | Condiciones a barrer | Alimenta modelo |
|---|---|---|---|---|---|
| Óptico/pasivo | Pérdida de inserción | IL (dB) | OSA, medidor de potencia, swept-lambda | λ (C/L band), polarización, temperatura | S1 enlace, `spectral_beer_lambert.py` |
| Óptico/pasivo | Relación de extinción / contraste | ER (dB) | OSA/potencia en estados ON/OFF | λ, potencia, estado | S1/S4, `snr_budget.py` |
| Óptico/actuación | Cambio de índice/efectivo | Δn, Δn_eff | Interferometría, espectro de resonancia/F–P | nivel/estado, T, voltaje/campo | A1/G2/G3, `mzi_sim.py`, `model_pcm_multilevel.py` |
| Óptico/fase | Desplazamiento de fase | Δφ (rad) | MZI/balanced detection, reconstrucción | nivel PCM, λ, T | P1/P3, S1 |
| Resonancia | Q, FSR, λ_res | — | Swept laser + detector, OSA | T, tuning, potencia | B3/G1/G2/G3 |
| Memoria PCM | Niveles distinguibles, retención | niveles, tiempo (s) | Escritura/lectura cíclica, deriva temporal | pulsos, T, tiempo | P1/P2/S4, `model_pcm_multilevel.py` |
| Memoria PCM | Energía/ciclo de escritura | E (pJ–nJ) | Medición eléctrica/óptica de pulso | amplitud, ancho, tasa | S2, térmica |
| Conmutación | Tiempo de conmutación | t (ps–µs según tecnología) | Pump-probe, osciloscopio rápido | estado, T | G2/G3/VO₂ |
| Térmica | Mapa de temperatura / transitorio | T(x,y,z,t) (°C) | Termografía IR, sensores integrados | duty cycle, potencia, secuencia OMCC | S1, `model_thermal_brush.py` |
| Crosstalk | Óptico/térmico entre celdas | dB, °C | Medición vecino ON/OFF, barrido pitch | pitch, patrón de activación | S1/S4 |
| Ruido/detección | SNR, ruido equivalente | dB, NEP | Balanced PD, ESA/tiempo | potencia, BW, λ | S1/S3, `snr_budget.py` |
| Endurance/fatiga | Ciclos hasta degradación | N ciclos, ΔIL/ΔER | Ciclado automatizado | régimen, T | P2/S4, `model_reliability_p2.py` |

## 2. Matriz por candidato priorizado

| Candidato | Elementos críticos a medir | Parámetros prioritarios (E1) | Objetivo/referencia de modelo (conceptual) | Riesgo principal a cerrar |
|---|---|---|---|---|
| **H3 (A1+G1+B3)** | Celdas MZI-PCM Sb₂S₃, filtros/membranas G1 pasivas, anillos WDM, integración 2.5D | Δn_eff/Δφ por nivel PCM, IL de ruta, ER, retención PCM, deriva térmica de anillo, crosstalk térmico (duty OMCC), ciclos | IL ruta ~10.4 dB (modelo S1), margen térmico nominal viable con secuenciado; 4–5 bits/celda objetivo | Margen térmico peor-caso y estabilidad de resonancias bajo escritura PCM |
| **G2 (membrana EO)** | Cavidades F–P apiladas, sintonía EO, drivers | Δn(V), desplazamiento espectral, IL, ER, velocidad de reconfiguración, consumo EO, deriva térmica | Reconfig ps–ns, BW alto, IL ruta ~6.7 dB; sin escritura PCM 300°C | Dependencia EO, pérdida/acoplo y estabilidad térmica/RF |
| **G3 (PCM+EO)** | Membrana híbrida (estado PCM + trim EO), aislamiento | Δφ/Δn por estado PCM y EO, IL, velocidad EO, energía/retención PCM, crosstalk térmico localizado | IL ~7.1 dB, equilibrio NV+ajuste; viabilidad térmica nominal con duty-cycle | Co-integración térmica PCM/EO y repetibilidad multinivel |
| **H1 (A1+G3+3D)** | Apilado 3D, guías verticales, celdas PCM y membranas por plano | IL por plano/vía, alineación/acoplo interplano, Δφ, mapa térmico 3D, crosstalk, yield por plano | IL ~11.1 dB, capacidad NV alta; factibilidad térmica con secuenciado/manifold (nominal y peor-caso modelados) | Yield/alineación 3D y extracción de calor |
| **H4 (G2/G3+F2+A1)** | Membranas 3D, etapa difractiva F2, PCM local | Eficiencia/función difractiva, IL total, uniformidad de fase, alineación 3D, térmica distribuida, yield | IL ~12.4 dB, techo de capacidad; alta sensibilidad a proceso | Integración/alineación 3D, pérdidas acumuladas y variabilidad |

## 3. Condiciones de prueba y barridos recomendados (E1→E2)

- **Óptico:** λ en banda operativa (y márgenes), potencia de entrada (régimen lineal), polarización, acoplamiento fibra-chip/guía.
- **Térmico:** temperatura ambiente/controlada, duty cycle de escritura (OMCC), secuencias de pulsos, estado estacionario vs transitorio.
- **Eléctrico/EO:** voltaje/campo, ancho de pulso, repetición, consumo.
- **Fiabilidad:** ciclado (endurance PCM/EO), retención a distintos T, deriva temporal, calibración en lazo cerrado.
- **Variabilidad:** muestreo por lote/wafer/posición, repetibilidad celda-a-celda (alimentar σ de S4).

## 4. Criterios de salida E1 (para recalibrar y pasar a E2)
- Parámetros medidos (IL, Δn/Δφ, ER, tiempos, energía, retención, T transitoria) dentro de rangos usados en S1–S4 **o** modelo actualizado con valores medidos y márgenes recalculados.
- Identificación de limitante dominante por candidato (térmico, pérdida, variabilidad, alineación) y plan de mitigación validado en simulación.
- Datos trazables (condiciones, incertidumbre) almacenados en `outputs/`/`data/` con procedencia para cierre de arte previo y reproducibilidad.

## 5. Mapeo medición → recalibración de modelos
- **S1 (`model_s1_link_thermal.py`):** IL por elemento, acoplos, mapas T(t), aislamiento efectivo → márgenes de enlace y VO₂.
- **S2 (`model_s2_system_profiles.py`, `simulate_opgpu_system.py`):** latencias reales, throughput, overhead de control/ECC, eficiencia E/O-O/E.
- **S3 (`model_s3_pcie_openvino.py`):** tiempos de cola/DMA, jitter, BW efectivo, coste de partición/fallback.
- **S4 (`model_s4_variability_yield.py`, `model_s4_cost_overhead.py`):** σ(n,d,acoplo,IL,térmica), tasas de fallo, eficacia de re-mapeo/calibración → yield y coste real.
- **P1–P3:** niveles PCM, ruido/precisión, retención/endurance, refresco M2.

## 6. Seguridad y cumplimiento (recordatorio)
Láseres (UV/visible/NIR), alta temperatura localizada (PCM ~300 °C), y alta tensión/RF en EO requieren controles de seguridad, EPP, y cumplimiento normativo en laboratorio/fabricación. No realizar experimentos sin evaluación de riesgos.
