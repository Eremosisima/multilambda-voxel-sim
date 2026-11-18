# Fiabilidad/endurance bajo restricción térmica de duty (conceptual)

> Proyecta escrituras/reconfiguraciones sostenibles usando límites de duty S1 (peor caso) y parámetros de endurance/retención. No son mediciones.

## Resumen

| Candidato | Carga | Duty deseado | Límite térmico (peor) | Duty alcanzable | Throttling | Factor perf. | Endurance OK (5y, margen) | Refresh necesario |
|---|---|---:|---:|---:|:---:|---:|:---:|:---:|
| H3 | inference_static | 0.001 | 0.12 | 0.001 | no | 1.0 | no | no |
| H3 | periodic_reconfig | 0.02 | 0.12 | 0.02 | no | 1.0 | no | no |
| H3 | dynamic_adaptation | 0.08 | 0.12 | 0.08 | no | 1.0 | no | no |
| H3 | aggressive_reconfig | 0.2 | 0.12 | 0.12 | sí | 0.6 | no | no |
| G3 | inference_static | 0.001 | 0.12 | 0.001 | no | 1.0 | no | no |
| G3 | periodic_reconfig | 0.02 | 0.12 | 0.02 | no | 1.0 | no | no |
| G3 | dynamic_adaptation | 0.08 | 0.12 | 0.08 | no | 1.0 | no | no |
| G3 | aggressive_reconfig | 0.2 | 0.12 | 0.12 | sí | 0.6 | no | no |
| G2 | inference_static | 0.001 | 0.05 | 0.001 | no | 1.0 | sí | sí |
| G2 | periodic_reconfig | 0.02 | 0.05 | 0.02 | no | 1.0 | sí | sí |
| G2 | dynamic_adaptation | 0.08 | 0.05 | 0.05 | sí | 0.625 | sí | sí |
| G2 | aggressive_reconfig | 0.2 | 0.05 | 0.05 | sí | 0.25 | sí | sí |
| H1 | inference_static | 0.001 | 0.12 | 0.001 | no | 1.0 | no | no |
| H1 | periodic_reconfig | 0.02 | 0.12 | 0.02 | no | 1.0 | no | no |
| H1 | dynamic_adaptation | 0.08 | 0.12 | 0.08 | no | 1.0 | no | no |
| H1 | aggressive_reconfig | 0.2 | 0.12 | 0.12 | sí | 0.6 | no | no |
| H4 | inference_static | 0.001 | 0.18 | 0.001 | no | 1.0 | no | no |
| H4 | periodic_reconfig | 0.02 | 0.18 | 0.02 | no | 1.0 | no | no |
| H4 | dynamic_adaptation | 0.08 | 0.18 | 0.08 | no | 1.0 | no | no |
| H4 | aggressive_reconfig | 0.2 | 0.18 | 0.18 | sí | 0.9 | no | no |

## Lectura
- Cargas estáticas/periódicas son compatibles con límites térmicos PCM (H3/G3/H1/H4) y preservan endurance; adaptación dinámica agresiva puede requerir throttling o particionado/alternancia térmica.
- G2 (EO) no está limitado por escritura térmica PCM pero requiere refresco/buffer por baja retención efectiva de estado rápido; adecuado a reconfiguración frecuente.
- Integrar con OMCC (scheduling térmico, wear-leveling, re-mapeo) y validar con caracterización de ciclos/retención.
