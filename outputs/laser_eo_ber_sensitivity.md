# Sensibilidad láser/E-O acoplada a BER/exactitud (proxy, conceptual)

> Barrido de potencia láser, ER y sesgo con ruido equivalente para estimar ventana operativa (BER/accuracy proxy).

## Mejores puntos operativos (umbral BER<=1e-9 y acc>=0.9)

| Candidato | Láser mín. OK (dBm) | ER (dB) | Sesgo | SNR proxy (dB) | Accuracy proxy |
|---|---:|---:|---:|---:|---:|
| H3 | 8 | 10 | 0.0 | 24.657 | 1.0 |
| G2 | 4 | 10 | 0.0 | 23.957 | 1.0 |
| G3 | 4 | 10 | 0.0 | 23.557 | 1.0 |
| H1 | 8 | 10 | 0.0 | 23.957 | 1.0 |
| H4 | None | 10 | 0.0 | 22.657 | 1.0 |

## Lectura
- Mayor IL (H1/H4) exige más potencia láser y mejor ER/sesgo para mantener margen de SNR; H3/G3/G2 operan con menor potencia relativa.
- La calibración de sesgo y ER efectivo es crítica para exactitud analógica; integrar con control en lazo cerrado y cuantización (modelo de accuracy).
- Validar con mediciones de RIN, responsividad/ruido de PD, linealidad E/O y BER/enlace real.
