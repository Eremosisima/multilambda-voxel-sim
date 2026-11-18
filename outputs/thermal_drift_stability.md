# Deriva térmica temporal y estabilidad de resonancias (conceptual, informado por referencia)

> Sensibilidad de referencia: 80 pm/K, tuning ~0.08 nm/mW (Si ring típico). Modelo transitorio simplificado; calibrar con respuesta medida y lazo de control.

## Resumen

| Candidato | Control | Detuning medio (nm) | Detuning p95 (nm) | Potencia tuning media (mW) | Potencia tuning p95 (mW) | Fracción estable | Estable (>=95%) |
|---|---|---:|---:|---:|---:|---:|:---:|
| H3 | open_loop | 0.31997 | 0.39923 | 0.0 | 0.0 | 0.0 | no |
| H3 | static_calibration | 0.15993 | 0.19967 | 399.8224 | 499.1775 | 0.0 | no |
| H3 | closed_loop_a | 0.06261 | 0.07865 | 469.5978 | 589.8491 | 0.0 | no |
| H3 | closed_loop_b_fast | 0.02526 | 0.03169 | 315.7716 | 396.091 | 1.0 | sí |
| G3 | open_loop | 0.41227 | 0.50876 | 0.0 | 0.0 | 0.0 | no |
| G3 | static_calibration | 0.20595 | 0.25499 | 514.8671 | 637.4788 | 0.0 | no |
| G3 | closed_loop_a | 0.08164 | 0.10127 | 612.326 | 759.5415 | 0.0 | no |
| G3 | closed_loop_b_fast | 0.03262 | 0.04082 | 407.7689 | 510.1955 | 0.855 | no |
| G2 | open_loop | 0.41757 | 0.57759 | 0.0 | 0.0 | 0.0 | no |
| G2 | static_calibration | 0.21033 | 0.29209 | 525.8295 | 730.2162 | 0.0 | no |
| G2 | closed_loop_a | 0.08409 | 0.11668 | 630.7026 | 875.0874 | 0.0 | no |
| G2 | closed_loop_b_fast | 0.03365 | 0.0467 | 420.6194 | 583.8069 | 0.68 | no |
| H1 | open_loop | 0.52212 | 0.63269 | 0.0 | 0.0 | 0.0 | no |
| H1 | static_calibration | 0.26297 | 0.31815 | 657.4283 | 795.3656 | 0.0 | no |
| H1 | closed_loop_a | 0.10507 | 0.12665 | 788.0281 | 949.9086 | 0.0 | no |
| H1 | closed_loop_b_fast | 0.04203 | 0.05082 | 525.3512 | 635.2555 | 0.36 | no |
| H4 | open_loop | 0.62937 | 0.75132 | 0.0 | 0.0 | 0.0 | no |
| H4 | static_calibration | 0.31577 | 0.37885 | 789.4258 | 947.113 | 0.0 | no |
| H4 | closed_loop_a | 0.12576 | 0.14995 | 943.2361 | 1124.6267 | 0.0 | no |
| H4 | closed_loop_b_fast | 0.05028 | 0.06044 | 628.4926 | 755.5311 | 0.0 | no |

## Lectura
- Sin control en lazo cerrado, los candidatos con escritura PCM/anillos muestran mayor detuning transitorio; lazos cerrados (A/B) recuperan estabilidad a costa de potencia de control.
- G2 (sin escrituras PCM 300°C) reduce pulsos térmicos pero sigue requiriendo estabilización EO/anillos.
- H1/H4 concentran mayor carga térmica; necesitan aislamiento, secuenciado y control rápido para mantener resonancias dentro de tolerancia.
