# Presupuesto de potencia/energía por perfil y modo (proxy, conceptual)

> Estimación aproximada (no mediciones). Dinámico ~ TOPS·pJ/MAC·utilización + fijos (PCIe/control, E/O-O/E, láser, refrigeración, OMCC) con overheads S4.

## Resumen (TPU, utilización objetivo)

| Candidato | Perfil | Módulos | Potencia total (W) | TOPS efectivos | TOPS/W | pJ/MAC ef. |
|---|---|---:|---:|---:|---:|---:|
| H3 | edge | 3 | 35.596 | 6.772 | 0.1903 | 0.6048 |
| H3 | ws | 7 | 83.057 | 15.803 | 0.1903 | 0.6048 |
| H3 | dc | 27 | 320.362 | 60.953 | 0.1903 | 0.6048 |
| G3 | edge | 2 | 24.509 | 6.675 | 0.2723 | 0.5258 |
| G3 | ws | 5 | 61.273 | 16.688 | 0.2723 | 0.5258 |
| G3 | dc | 18 | 220.584 | 60.075 | 0.2723 | 0.5258 |
| G2 | edge | 2 | 23.706 | 7.399 | 0.3121 | 0.3657 |
| G2 | ws | 5 | 59.266 | 18.499 | 0.3121 | 0.3657 |
| G2 | dc | 17 | 201.504 | 62.896 | 0.3121 | 0.3657 |
| H1 | edge | 2 | 27.33 | 10.53 | 0.3853 | 0.6012 |
| H1 | ws | 3 | 40.995 | 15.795 | 0.3853 | 0.6012 |
| H1 | dc | 12 | 163.981 | 63.18 | 0.3853 | 0.6012 |
| H4 | edge | 2 | 27.4 | 11.098 | 0.4051 | 0.5767 |
| H4 | ws | 3 | 41.1 | 16.648 | 0.4051 | 0.5767 |
| H4 | dc | 11 | 150.702 | 61.042 | 0.4051 | 0.5767 |

## Lectura
- G2/G3 muestran mejor TOPS/W proxy por menor pJ/MAC base; H3 mantiene buen balance con mayor apertura/NV; H1/H4 pagan overheads de escala/redundancia.
- Los fijos (E/O-O/E, láser, control, refrigeración) dominan en configuraciones pequeñas (edge) y deben medirse; el dinámico escala con utilización/modos.
- Usar para comparar tendencias relativas, no para especificación de producto.
