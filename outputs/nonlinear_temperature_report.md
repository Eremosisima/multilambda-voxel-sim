# Análisis: validez del modelo lineal y dependencia de temperatura

## 1. ¿Funciona el modelo lineal o se requiere no linealidad?

**Conclusión:** el modelo lineal es una aproximación de primer orden útil, pero **no debe asumirse universalmente**. En materiales fotosensibles reales es plausible encontrar saturación/no linealidad en la relación control/estado → Δn efectivo, además de histéresis, fatiga o dependencia espectral.

Comparación (decodificador asumiendo linealidad vs respuesta efectiva no lineal ilustrativa):

| Respuesta efectiva | Supuesto del decodificador | Exactitud palabra | SER | MSE estado |
|---|---|---:|---:|---:|
| linear | linear | 1.000 | 0.000 | 0.0000 |
| saturating_k2 | linear | 0.058 | 0.512 | 0.0894 |
| logistic_s6 | linear | 1.000 | 0.000 | 0.0159 |
| saturating_k2 | calibrated_nonlinear_inverse | 1.000 | 0.000 | 0.0000 |
| logistic_s6 | calibrated_nonlinear_inverse | 1.000 | 0.000 | 0.0000 |

Implicación: si la respuesta real es no lineal y el decodificador usa el modelo lineal sin calibración, aparecen errores de cuantización/decodificación. Con **calibración e inversa no lineal** (mapeo caracterizado) se puede recuperar desempeño en la medida en que la respuesta sea monotónica y estable.

**Recomendación:** medir/ajustar `Δn_eff(c, λ, T, historial)`; usar LUT o modelo inverso calibrado por canal/material; verificar linealidad por rangos de operación.

## 2. ¿Hay que considerar la temperatura?

**Conclusión: sí.** La temperatura afecta al menos (i) la **fase leída** vía efecto termo-óptico (deriva) y (ii) la **retención/estado** vía cinética térmica (back-reaction).

- Deriva termo-óptica (modelo, dn/dT=1e-05/K, L=100 µm, Γ=0.35): para mantener deriva ≤ 10% del medio paso, el peor caso entre canales requiere estabilidad aproximada mejor que **50.00 K** (ver `temperature_stability_budget.csv`).
- Retención (Arrhenius ilustrativo, Ea asumida): la vida media disminuye rápidamente al aumentar T; los valores reales dependen del material/matriz y deben medirse (ver `temperature_retention_arrhenius.csv`, `figures/thermal_retention_arrhenius.png`).

**Recomendación:** control/estabilización térmica o compensación en lectura; calibración dependiente de temperatura; caracterización de dn/dT y cinética (Ea, tasas) por compuesto.

## Artefactos
- `outputs/nonlinear_model_comparison.csv`
- `outputs/temperature_thermo_optic.csv`, `outputs/temperature_retention_arrhenius.csv`, `outputs/temperature_stability_budget.csv`
- `outputs/nonlinear_temperature_summary.json`
- `figures/nonlinear_response_curves.png`, `figures/thermo_optic_drift.png`, `figures/thermal_retention_arrhenius.png`
