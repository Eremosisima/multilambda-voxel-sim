# Optimización multiobjetivo Pareto (costo/TOPS/W/retención/área, conceptual)

> Selección por perfil usando capacidad efectiva y overheads S4 + proxy de coste/potencia. No es BOM ni medición de energía.

## Resultados

| Candidato | Perfil | Módulos | TOPS total | Mem total (MB) | Área (cm²) | Coste idx | Potencia (W proxy) | TOPS/W | Retención | Cumple | Pareto | Score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|---:|
| H3 | edge | 3 | 9.03 | 412.8 | 136.8 | 4.2 | 4.37 | 2.067 | 0.86 | sí | sí | 1.1248 |
| H3 | ws | 7 | 21.07 | 963.2 | 319.2 | 9.8 | 10.19 | 2.067 | 0.86 | sí | no | 1.0844 |
| H3 | dc | 27 | 81.27 | 3715.2 | 1231.2 | 37.8 | 39.32 | 2.067 | 0.86 | sí | sí | 1.0631 |
| G3 | edge | 2 | 8.9 | 455.68 | 71.04 | 2.6 | 3.74 | 2.378 | 0.89 | sí | sí | 1.2207 |
| G3 | ws | 5 | 22.25 | 1139.2 | 177.6 | 6.5 | 9.36 | 2.378 | 0.89 | sí | sí | 1.2207 |
| G3 | dc | 18 | 80.1 | 4101.12 | 639.36 | 23.4 | 33.69 | 2.378 | 0.89 | sí | sí | 1.1873 |
| H1 | edge | 2 | 14.04 | 998.4 | 244.0 | 4.0 | 6.75 | 2.079 | 0.78 | sí | sí | 1.3659 |
| H1 | ws | 3 | 21.06 | 1497.6 | 366.0 | 6.0 | 10.13 | 2.079 | 0.78 | sí | sí | 1.1553 |
| H1 | dc | 12 | 84.24 | 5990.4 | 1464.0 | 24.0 | 40.51 | 2.079 | 0.78 | sí | sí | 1.1553 |
| H4 | edge | 2 | 14.798 | 1065.47 | 226.8 | 4.6 | 6.83 | 2.168 | 0.7399 | sí | sí | 1.3805 |
| H4 | ws | 3 | 22.197 | 1598.2 | 340.2 | 6.9 | 10.24 | 2.168 | 0.7399 | sí | no | 1.1585 |
| H4 | dc | 11 | 81.389 | 5860.07 | 1247.4 | 25.3 | 37.55 | 2.168 | 0.7399 | sí | sí | 1.1308 |

## Recomendación por perfil (trade-off)
- **Edge:** G3/H3 destacan por eficiencia y retención con pocos módulos; H1/H4 viables en capacidad pero con mayor coste/área/complejidad 3D.
- **WS:** G3 ofrece buen balance TOPS/W/coste; H3 base abierta de menor riesgo.
- **DC:** G3 escala en módulos con mejor coste-eficiencia que 3D en este proxy; H1/H4 reducen conteo de módulos pero requieren madurez 3D y mayor área/coste.
