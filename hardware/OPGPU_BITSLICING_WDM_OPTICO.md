# OPGPU Bit-Slicing Óptico WDM — Precisión IA con Memorias Ternarias (CC0 1.0, dominio público)

> **Versión:** 1.0 — 2026-11-19
> **Estado:** especificación conceptual. No es diseño listo para fabricación.
> **Dominio público:** arte previo defensivo (disclosure defensivo): mapeo de bits a canales WDM con ganancias calibradas y memorias ternarias (Sb₂S₃ PCM).

## 1. Objetivo

Permitir ejecutar operaciones de IA de alta precisión (INT8/FP16-like) usando memorias ópticas ternarias (MZI + PCM Sb₂S₃: estados de alta (~+), bajo (~0), sin arribo/Z), mediante descomposición de pesos en bits distribuidos por canales WDM — "bit-slicing óptico". La celda ternaria individual puede no ser precisa; la suma ponderada por canales WDM (cada bit con su ganancia calibrada β_i = 2^i·β_0) recupera pesos de IA de precisión nivelada con ADC 12 bits.

## 2. Fundamento matemático

Cálculo óptico base (MVM):

```
y = W · x
```

donde W es la matriz de pesos y x los vectores de activación. Cada entrada w_ij se descompone en bits:

```
w = Σ_k b_k · β_k        (b_k ∈ {0,1}; β_k = 2^k · β_0)
```

La celda óptica del bit k (celda ternaria MZI+PCM) suma al haz de entrada:

- b_k = 1: transmite β_k × x
- b_k = 0: no transmite (estado Z)
- (estado 1 alternativo para doble planta de bits)

El fotodetector recibe:

```
y ≈ Σ_k b_k · β_k · x
```

Recuperando w = Σ b_k·2^k: con ADC 12 bits y margen SNR ≥ 13 bits por bit.

## 3. Codificación de valores (número entero efectivo)

### 3.1 Celdas ternarias
Estados de la celda (MZI + PCM Sb₂S₃):
- **1 (alta):** transmisión calibrada T_i ≈ β_i (Referencia óptica per channel).
- **0 (bajo/absento):** sin arribo (Z).
- **Z (intermedio):** doble ausencia/estado para redundancia (diseño abierto).

### 3.2 Bit-slicing WDM
- N bits: N canales WDM λ_0..λ_{N-1} en C-band (1530–1565 nm), espaciado WDM estándar (100/200 GHz).
- Canales para bits: λ_0..λ_{N-2}; canal λ_sign para signo/ruido (design opcional).
- Ganancias calibradas: β_i = 2^i·β_0 (β_0 ≈ unidad de eficiencia del ADC).
- Señales de control: escritura óptica (650 nm, Arrhenius) + tuning térmico por OMCC para alinear β_i.

### 3.3 Ejemplo: INT8 weight
```
w = b7·128 + b6·64 + b5·32 + b4·16 + b3·8 + b2·4 + b1·2 + b0·1
```
- Celda i: MZI tile i, PCM Sb2S3, λ_i = 1530 + i·0.04 nm (200 GHz spacing)
- β_i = 2^i · β_0
- Resultado: ADC mide Σ b_i·2^i·β_0 → w.

## 4. Pseudocódigo abierto (referencia abierta, CC0 1.0)

```python
# Pseudocode — referencia abierta, public domain (CC0 1.0)
def encode_weight(w, bits=8, wdm_base=1530, wdm_sp=0.04, beta0=1.0):
    cells = []
    for i in range(bits):
        b = (w >> i) & 1
        cells.append({
            "state": b,                 # 1 = T_i, 0 = Z
            "lambda": wdm_base + i * wdm_sp,
            "gain": 2**i * beta0,
        })
    return cells

def decode_result(measurements, cells):
    total = 0
    for m, c in zip(measurements, cells):
        if c["state"] == 0:
            continue
        d = round(m / c["gain"])  # T_i medido; d ∈ {0,1}
        total += d * c["gain"]
    return total

def calibrate_cell(cell, optical_ref, temp, wdm_chan, ppm):
    # Determinar ganancia beta_i y dependencia T(T): Arrhenius
    # Ejemplo: escribir ópticamente (650 nm) + ajuste por OMCC
    # Devuelve (T_i(T), ppm_drift)
    pass
```

Pseudocódigo de la celda (mapeo MZI → estado):
```
write_state(cell, state):
    # OMCC command: set MZI bar/through via PCM programming (650 nm)
    # OMCC: telemetría de T_i por ADC; corrección por Arrhenius
    pass
```

## 5. Precisión y tolerancia

- ADC 12 bits (≥ 13 bits margen por bit más significativo).
- β_i tolerancia: ±10% de la ganancia del bit menos significativo.
- Redundancia opcional: 2 celdas por bit MSB (Z-state reusado como redundancia) → corrección de errores.
- Validación de ancho de banda: β_i distribuido 20–30% sobre valor nominal (salvaguarda).

## 6. Integración con la arquitectura OPGPU

- Celdas bit-slicing: MZI tiles (sección 4.2 de ARQUITECTURA_DISAGGREGATED.md).
- Canales WDM: β_i usa 16 λs (8–12 bits de precisión).
- Control OMCC: comandos ópticos por celda (ARQUITECTURA/TRANCEPTOR spec).
- Flujo óptico: 2 nodos suman λ_i → ADC en RX O/E.
- Compute: acción términica según Sb₂S₃ (diaryleténico/spiropirano, Δn grande).

## 7. Verificación y herramientas abiertas (estado conceptual)

- **Simulación de precisión:** pseudocódigo + modelos Monte Carlo de β_i con distribución de ruido + drift Arrhenius; estimar SNR per bit.
- **Referencia abierta:** pseudocódigo + diagramas de flujo (cómputo óptico y calibración).
- **Estado:** conceptual/simulado (S1–S4); sin prototipo físico por validar.

## 8. Licencia

**CC0 1.0 — dominio público.** Divulgación defensiva: mapeo de bits a canales WDM con ganancias calibradas (2^i·β_0) y memorias ternarias Sb₂S₃ es publicado como arte previo para dificultar patentes "alrededor" del diseño.

## 9. Referencias útiles

- Róos et al. (2015) — *Nature Photonics* 9, 725-732, DOI:10.1038/nphoton.2015.182 (memoria fotónica integrada, PCM multinivel).
- Feldmann et al. (2019) — *Nature* 569, 208-214, DOI:10.1038/s41586-019-1157-8 (pesos ópticos integrados).
- Arbabi & Goddard (2013) — *Optics Letters* 38(19), 3878-3881, DOI:10.1364/OL.38.003878 (dn/dT en SiN/SiOx).
- Meep (GPL-2.0) — EM/FDTD para guías; gdstk (BSL-1.0) — GDSII.
- Zenodo: DOI 10.5281/zenodo.24323250 (v0.3.0).
