# P1 — Modelado con datos de respaldo (PCM multinivel y térmica transitoria)

> Resultados generados por simulación/modelado conceptual (scripts reproducibles). **No son mediciones**; sirven como datos de respaldo iniciales para dimensionamiento y decisiones de diseño. Todos los valores dependen de las suposiciones declaradas y requieren calibración por simulación FEM/FDTD y caracterización experimental.

## 1. Celda PCM multinivel segmentada/tapered (Sb₂S₃)

**Script:** `model_pcm_multilevel.py`  
**Salidas:** `outputs/pcm_multilevel_levels.csv`, `outputs/pcm_multilevel_summary.json`, `outputs/pcm_multilevel_report.md`, `figures/pcm_multilevel_{phase,loss}.png`

### 1.1 Parámetros del modelo (base)
- Material: Sb₂S₃, $n_a=2.70$, $n_c=3.30$ (especificación del proyecto)
- Lectura: $\lambda=1550\,\text{nm}$ (conceptual), longitud de celda $L=10\,\mu\text{m}$, solapamiento modal efectivo $0.35$
- Estructura: segmentada/tapered ($8$ segmentos, penalización de taper $0.05\,\text{dB/interfaz}$ como objetivo de diseño)
- Objetivo de niveles: $32$ ($5$ bits), fracción de cristalinidad $f\in[0,1]$
- Modelo óptico: mezcla lineal de primer orden para índice/absorción efectivos, $\Delta\phi = \frac{2\pi}{\lambda}\Delta n_{eff}L$, $\Delta n_{eff}=f\cdot\Gamma\cdot(n_c-n_a)$

### 1.2 Resultados clave (generados)
| Métrica | Valor |
|---|---:|
| Niveles / bits | 32 / 5.0 |
| Rango de fase | 8.513 rad (**2.710 π**) |
| Paso de fase medio / mínimo | 0.275 rad / 0.275 rad (uniforme por discretización) |
| Pérdida de inserción (rango) | 0.105–0.140 dB |
| IL estado medio (mono vs seg/taper, est.) | 0.225 dB vs 0.285 dB (según supuestos de pérdida/dispersión del modelo) |

**Interpretación:** con los supuestos adoptados, una celda de $10\,\mu\text{m}$ y $\Gamma=0.35$ ofrece un rango de fase > $2\pi$ y 32 niveles distinguibles en fase (resolución geométrica uniforme). El rango de IL es bajo en el modelo simplificado; valores reales dependerán de $\alpha(\lambda)$, pérdidas de acoplamiento, dispersión por segmentación y calidad de película, por lo que se requiere calibración FDTD/FEM y medición.

### 1.3 Suposiciones y límites
- Mezcla lineal de índice/absorción frente a fracción cristalina (aproximación de primer orden).
- $\Gamma$, coeficientes de pérdida y energía son estimaciones de diseño a calibrar.
- La energía por paso se modela como magnitud conceptual proporcional al volumen conmutado efectivo.
- Contexto de referencia: control multinivel Sb₂S₃ (Nat. Commun. 2023, 10.1038/s41467-023-39180-3), optimización de memoria PCM fotónica (Photonics 2025, 10.3390/photonics12111130), nanoestructuración/tapering (arXiv 2604.08637).

## 2. Térmica transitoria y diafonía en arreglo "cepillo" (Sb₂S₃ 300 °C vs VO₂ 68 °C)

**Script:** `model_thermal_brush.py`  
**Salidas:** `outputs/thermal_brush_summary.json`, `outputs/thermal_brush_traces.csv`, `outputs/thermal_brush_pitch_sweep.csv`, `outputs/thermal_brush_report.md`, `figures/thermal_brush_{sb2s3.png,pitch_sweep.png}`

### 2.1 Parámetros del modelo (nominal)
- Geometría: pitch $10\,\mu\text{m}$, radio de cerda $1.5\,\mu\text{m}$, longitud de vóxel $5\,\mu\text{m}$, separación axial Sb₂S₃–VO₂ $z_{sep}=8\,\mu\text{m}$
- Medio efectivo: $k=1.4\,\text{W/mK}$, $\rho=2600\,\text{kg/m^3}$, $c_p=700\,\text{J/kgK}$, extracción equivalente $h=2\times10^4\,\text{W/m^2K}$
- Pulsos: programación Sb₂S₃ $2.0\,\mu\text{s}$ (objetivo ~320 °C), operación VO₂ $0.5\,\mu\text{s}$ (objetivo ~85 °C), $T_{amb}=25\,^\circ\text{C}$
- Umbrales: VO₂ 68 °C, Sb₂S₃ ~300 °C
- Método: difusión térmica radial 1D (diferencias finitas) + extracción axial concentrada; acoplamiento axial estimado por atenuación exponencial $e^{-z_{sep}/L_{vox}}$ (proxy de primer orden)

### 2.2 Resultados nominales (generados)
| Métrica | Valor |
|---|---:|
| Pico en núcleo (Sb₂S₃, pulso prog.) | 416.67 °C |
| Pico en cerda vecina @ pitch | 31.68 °C |
| Pico lejano @ 2·pitch | 25.18 °C |
| Calor estimado en segmento VO₂ adyacente (atenuación axial) | **26.35 °C** |
| Margen respecto a umbral VO₂ (68 °C) | **41.65 °C** |
| Pico núcleo/vecino (pulso VO₂) | 105.48 °C / 25.34 °C |
| Factor de atenuación axial (est.) | 0.2019 |

### 2.3 Barrido de pitch (crosstalk lateral/axial estimado)
| Pitch (µm) | Pico vecino (°C) | Calor en segmento VO₂ ady. (°C) | Margen a 68 °C (°C) |
|---:|---:|---:|---:|
| 6 | 44.67 | 28.97 | 39.03 |
| 8 | 35.75 | 27.17 | 40.83 |
| 10 | 31.68 | 26.35 | 41.65 |
| 12 | 29.15 | 25.84 | 42.16 |
| 16 | 26.23 | 25.25 | 42.75 |
| 20 | 25.26 | 25.05 | 42.95 |

**Interpretación:** bajo estas suposiciones, la combinación de separación lateral ($\ge 6\,\mu\text{m}$), separación axial ($8\,\mu\text{m}$) y extracción térmica mantiene el segmento VO₂ adyacente muy por debajo de 68 °C durante un pulso de programación de Sb₂S₃ que alcanza >400 °C en el núcleo. La programación de VO₂ (núcleo ~105 °C en este modelo) queda localizada con bajo impacto en vecinos.

### 2.4 Suposiciones y límites
- Modelo 1D radial con propiedades homogeneizadas y fuente calibrada heurísticamente (no sustituye FEM transitorio 3D).
- La atenuación axial es un proxy exponencial; interfaces reales, barreras y geometría 3D modificarán el acoplamiento.
- No modela explícitamente histéresis completa de VO₂ ni cinética de cambio de fase de Sb₂S₃; los umbrales se usan como criterios de seguridad.
- Requiere validación con simulación térmica 3D, medición de $k/c_p$ efectivos y caracterización pulso a pulso.

## 3. Uso de estos datos en el diseño
- **Dimensionamiento:** soportan pitch $\ge 10\,\mu\text{m}$ y $z_{sep}\ge 8\,\mu\text{m}$ como punto de partida conservador (consistente con el escenario de escalado v0.3) sujeto a validación.
- **Planificación OMCC:** refuerzan la necesidad de calendarización de pulsos, confinamiento térmico y verificación post-escritura (evitar solapamientos 300 °C/68 °C).
- **Celdas M1:** justifican explorar celdas Sb₂S₃ segmentadas/tapered multinivel ($\ge 5$ bits) con calibración en lazo cerrado para aumentar densidad efectiva ($N_m$).
- **Próximos pasos (P1/P2):** calibrar parámetros con FDTD/FEM (óptico) y FEM transitorio (térmico), incorporar variabilidad/endurance y retroalimentar `simulate_opgpu_system.py` con IL, energía y márgenes medidos/simulados de mayor fidelidad.