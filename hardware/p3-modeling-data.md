# P3 — Variabilidad espacial, selección de modo 4/5 bits y refresco M2

> Modelado conceptual basado en datos P1/P2. **No son mediciones**; define políticas de operación robusta (modo de bits, calibración, refresco VO₂) y su impacto a nivel de sistema.  
> **Dominio público (objetivo declarado):** uso libre para todo el mundo; publicado como **arte previo/divulgación defensiva** (ver `../PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta).

## 1. Variabilidad espacial y selección de modo (4b vs 5b)

**Script:** `model_variability_p3.py`  
**Salidas:** `outputs/p3_summary.json`, `outputs/p3_mode_comparison.json`, `outputs/p3_variability_sweep.csv`, `outputs/p3_report.md`, `figures/p3_variability_ser.png`

### 1.1 Configuración
- Rango de fase (P1): 8.513 rad
- Ruido de lectura: $\sigma_{read}=0.06$ rad (P2)
- Variabilidad espacial (celda a celda): $\sigma_{spatial}=0.03$ rad
- Deriva/residuo de calibración: $\sigma_{drift}=0.01$ rad
- $\sigma_{total}=\sqrt{\sigma_{read}^2+\sigma_{spatial}^2+\sigma_{drift}^2}\approx 0.0678$ rad
- Objetivos SER: ≤1% (5b), ≤0.1% (4b)

### 1.2 Comparación de modos (nominal)
| Modo | Paso (rad) | SNR_paso (dB) | SER | Bits efectivos (proxy) |
|---:|---:|---:|---:|---:|
| 5 bits (32 niveles) | 0.2746 | 1.36 | 0.03828 | ~4.49 |
| 4 bits (16 niveles) | 0.5675 | 7.67 | 0.00000 | 4.00 |

**Recomendación nominal:** **4b** (cumple objetivo de robustez bajo variabilidad/noise asumidos; 5b supera el objetivo de SER sin calibración/ECC adicional).

### 1.3 Barrido de variabilidad espacial (`outputs/p3_variability_sweep.csv`)
| $\sigma_{spatial}$ (rad) | SER 5b | SER 4b | Bits ef. 5b | Bits ef. 4b |
|---:|---:|---:|---:|---:|
| 0.00 | 0.0166 | 0.00000 | 4.786 | 4.000 |
| 0.02 | 0.0226 | 0.00000 | 4.625 | 4.000 |
| 0.03 | 0.0383 | 0.00000 | 4.488 | 4.000 |
| 0.04 | 0.0686 | 0.00000 | 4.243 | 4.000 |
| 0.06 | 0.1379 | 0.00070 | 3.709 | 3.991 |

**Implicación:** a mayor variabilidad, 4b mantiene margen amplio; 5b requiere reducción de $\sigma$ (óptica/ADC/térmica) y/o calibración por celda + ECC.

## 2. Refresco de M2 (VO₂ volátil)

De P2, retención/hold característico de M2: ~0.01 s (conceptual). Política modelada (OMCC):

| Parámetro | Valor (ejemplo) |
|---|---:|
| Tasa de refresco | 100 Hz |
| Refrescos por ventana de 1 ms | 0.1 |
| Sobrecoste temporal estimado | ~0.20% |
| Energía estimada por ventana (1 ms, 10⁶ celdas activas) | ~0.05 µJ |
| Política | Refresco en segundo plano, por lotes y calendarizado por OMCC, priorizando ventanas de cómputo |

## 3. Integración en sistema (P3)

**Simulación:** `simulate_opgpu_system.py` (config `OPGPU-TPU128-OMCC-P3-4b`)  
**Resultados:** `outputs/opgpu_system_sim_report.md`

Perfil P3 (4b robusto + refresco M2 + RAS moderado, pesos persistentes en M1):

| Carga | Latencia (ms) | TOPS efectivos | Energía (µJ) | Cuello |
|---|---:|---:|---:|---|
| GEMM_1024 | 0.0401 | 53.55 | 558.41 | input_transfer |
| Conv_infer_batch1 | 0.0075 | 160.01 | 293.68 | output_transfer |
| Attention_block | 0.0128 | 41.81 | 143.92 | input_transfer |
| GEMV_4k (sin persistencia) | 0.5215 | 0.064 | 276.73 | weight_transfer |

**Lectura:** el modo 4b reduce densidad efectiva pero mejora robustez frente a variabilidad; el coste de refresco M2 es pequeño con scheduling OMCC. El rendimiento se mantiene en el mismo orden que P2-RAS para cargas de alto reuso, con mejor margen de integridad.

## 4. Suposiciones y siguientes pasos
- Variabilidad modelada como offset gaussiano por celda + ruido/deriva; el proxy de bits efectivos es conservador (no capacidad de canal).
- Tasas/energía de refresco VO₂ son conceptuales y dependen de dispositivo y sesgo térmico/óptico.
- **Siguientes pasos:** calibración por celda/tile (mapas de offset), ECC/codificación multinivel, caracterización real de retención/refresco VO₂ y selección dinámica de modo 4b/5b por perfil de SNR.