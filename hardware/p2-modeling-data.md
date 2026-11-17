# P2 — Modelado de fiabilidad: ruido, resistencia (endurance) y retención

> Resultados generados por simulación/modelado conceptual (script reproducible). **No son mediciones**; cuantifican márgenes y riesgos para guiar calibración, RAS (OMCC) y perfiles NPU/TPU. Requieren validación experimental.  
> **Dominio público (objetivo declarado):** uso libre para todo el mundo; publicado como **arte previo/divulgación defensiva** (ver `../PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta).

## 1. Ruido de lectura y precisión efectiva (celda multinivel, base P1)

**Script:** `model_reliability_p2.py`  
**Salidas:** `outputs/reliability_p2_summary.json`, `outputs/reliability_noise_sweep.csv`, `outputs/reliability_p2_report.md`, `figures/reliability_ser_vs_noise.png`

### 1.1 Configuración
- Niveles: 32 (5 bits), rango de fase: 8.513 rad (P1), paso: 0.2746 rad
- Ruido de lectura (fase equivalente): $\sigma = 0.06$ rad (gaussiano, conceptual: shot + térmico + deriva)
- Decisión: nivel más cercano; $2\times10^4$ muestras (Monte Carlo)

### 1.2 Resultados nominales
| Métrica | Valor |
|---|---:|
| SER (symbol error rate) | 0.0205 (2.05%) |
| Tasa dentro de ±1 nivel | 1.0000 |
| SNR de paso (proxy) | 2.42 dB |
| Bits efectivos (proxy) | 4.898 |

### 1.3 Barrido de ruido (`outputs/reliability_noise_sweep.csv`)
| $\sigma$ (rad) | SER | SNR_paso (dB) |
|---:|---:|---:|
| 0.02 | 0.0000 | 11.97 |
| 0.04 | 0.0005 | 5.95 |
| 0.06 | 0.0205 | 2.42 |
| 0.08 | 0.0864 | -0.07 |
| 0.10 | 0.1680 | -2.01 |
| 0.12 | 0.2507 | -3.59 |
| 0.15 | 0.3521 | -5.53 |

**Interpretación:** con $\sigma\le 0.04$ rad el régimen es robusto para 5 bits; a $\sigma=0.06$ rad aparecen errores mayormente de 1 nivel (±1 = 100%), lo que motiva verificación, codificación/ECC, calibración y márgenes de lectura (OMCC/RAS). La mejora de SNR (óptico, ADC, estabilidad térmica) es palanca directa para recuperar bits efectivos.

## 2. Endurance (ciclos) y retención

**Salidas:** `outputs/reliability_endurance_summary.csv`, `outputs/reliability_retention_summary.csv`, `figures/reliability_{endurance,retention}.png`

### 2.1 Endurance (rodilla conceptual, retención de contraste)
| Componente (rol) | Ciclos (rodilla) | Nota |
|---|---:|---|
| M1 Sb₂S₃ (NV, pesos/memoria) | 1.0×10⁶ | PCM no volátil; segmentación/tapering puede mejorar (tendencias reportadas) |
| M2 VO₂ (volátil, conmutación/latches) | 1.0×10⁷ | Alta ciclabildad reportada en conmutación fotónica VO₂ |
| M0 Espiropirano (config/máscara) | 1.0×10⁴ | Fotoquímico, fatiga relevante; uso de baja frecuencia |
| M0 Azobenceno (trim/calibración) | 1.0×10⁵ | Ajuste lento; limitar tasa de reconfiguración |

### 2.2 Retención (característica conceptual, @~45 °C con aceleración simple)
| Componente | $\tau$ / escala | Nota |
|---|---:|---|
| M1 Sb₂S₃ | 1.0×10⁸ s | No volátil, retención larga |
| M2 VO₂ | 1.0×10⁻² s | Volátil (*hold* corto), requiere refresco/sesgo |
| M0 Espiropirano | 1.0×10⁵ s | Biestable fotoquímico, dependiente de condiciones |
| M0 Azobenceno | 1.0×10⁴ s | Relajación térmica posible; rol de trim |

## 3. Integración en sistema (P2-RAS, simulación)

**Simulación:** `simulate_opgpu_system.py` (v0.5+, configs `*-OMCC-P2-RAS`)  
**Resultados:** `outputs/opgpu_system_sim_report.md`

Para reflejar gestión de fiabilidad (mayor verificación/lectura redundante, arbitraje y márgenes), se modeló una configuración P2-RAS (p. ej. `omcc_verify_overhead=0.22`, overhead de arbitraje incrementado, ligera penalización de utilización efectiva) sobre el perfil P1 térmicamente consciente.

| Config / carga (alto reuso, M1 persistente) | Latencia (ms) | TOPS efectivos | Energía (µJ) | Cuello |
|---|---:|---:|---:|---|
| OPGPU-TPU128-OMCC-P1 / GEMM_1024 | 0.0377 | 57.04 | 556.26 | input_transfer |
| **OPGPU-TPU128-OMCC-P2-RAS / GEMM_1024** | **0.0401** | **53.55** | **561.63** | input_transfer |
| OPGPU-TPU128-OMCC-P1 / Conv_infer_batch1 | 0.0072 | 166.67 | 292.47 | output_transfer |
| **OPGPU-TPU128-OMCC-P2-RAS / Conv_infer_batch1** | **0.0075** | **160.01** | **295.49** | output_transfer |
| OPGPU-TPU128-OMCC-P1 / Attention_block | 0.0120 | 44.68 | 143.39 | input_transfer |
| **OPGPU-TPU128-OMCC-P2-RAS / Attention_block** | **0.0128** | **41.81** | **144.73** | input_transfer |

**Interpretación:** el coste de RAS/verificación es moderado frente a la ganancia estructural de OMCC+persistence, y proporciona el margen necesario para operar cerca del régimen de ruido observado (SER/bit efectivo) y gestionar desgaste/retención.

## 4. Suposiciones y referencias
- Modelos paramétricos/conceptuales (no caracterización de dispositivo): ruido gaussiano en fase, curvas de endurance/retención con rodilla/aceleración térmica simplificada.
- **Referencias de contexto:** Sb₂S₃ multinivel/endurance (Nat. Commun. 2023, 10.1038/s41467-023-39180-3); endurance fotónica VO₂ (npj Nanophotonics 2024, 10.1038/s44310-024-00038-1); mejoras por nanoestructuración PCM (arXiv 2604.08637); literatura de memorias fotónicas PCM (p. ej. MRS Bulletin / Science Bulletin).

## 5. Acciones derivadas (P2→P3)
- Reducir $\sigma_{lectura}$ (presupuesto óptico, ADC/TIA, estabilización) para operar en región de SER baja a 5 bits; evaluar 4 bits como modo robusto.
- Política OMCC: *wear leveling* en M1, limitación de tasa de escritura en M0 fotoquímicos, refresco/gestión de *hold* en M2 (VO₂).
- Calibrar con mediciones: distribución de niveles, BER/SER real, ciclos a fallo, retención vs temperatura y deriva.