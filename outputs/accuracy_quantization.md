# Precisión analógica y cuantización (proxy, conceptual)

> Combina márgenes S1 (enlace/IL) y estadísticas S4 (SNR, error de fase, IL) con ruido de cuantización para estimar exactitud relativa y bits efectivos. No son resultados de inferencia real.

## Puntos recomendados (calibración en lazo cerrado, CNN)

| Candidato | Acc. proxy INT8 | Acc. proxy INT6 | Bits efectivos (INT8) |
|---|---:|---:|---:|
| H3 | 0.9666 | 0.9643 | 4.93 |
| G3 | 0.9765 | 0.9733 | 5.44 |
| H1 | 0.9574 | 0.9556 | 4.58 |
| H4 | 0.9527 | 0.951 | 4.43 |
| G2 | 0.9796 | 0.976 | 5.64 |

## Lectura
- INT8 con calibración en lazo cerrado ofrece el mejor compromiso para H3/G3; INT6 es viable con mayor sensibilidad en cargas mixtas/Transformer.
- H1/H4 requieren mejor control de fase/IL y calibración para sostener bits efectivos altos debido a mayor varianza (S4).
- Calibrar con mediciones E/O-O/E, ruido de fotodetección/ADC/DAC y exactitud de inferencia por modelo.
