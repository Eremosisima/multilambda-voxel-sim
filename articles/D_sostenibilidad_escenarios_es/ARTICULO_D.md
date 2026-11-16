# Artículo D (borrador, ES): Escenarios de consumo energético y huella de CO2 en inferencia de IA con memoria no volátil — análisis paramétrico

**Tipo:** análisis de escenarios (modelado), sin mediciones de sistema.  
**Contribución propia:** modelo transparente de cálculo kWh/CO2 y sensibilidad a eficiencia (TOPS/W), PUE/factor de enfriamiento, utilización y mix eléctrico, separado de afirmaciones de desempeño de hardware específico.

## Resumen
Se presenta un marco de escenarios para estimar consumo anual de energía y emisiones asociadas a infraestructura de inferencia, comparando un caso de referencia ilustrativo con escenarios alternativos de mayor eficiencia computacional. El modelo explicita supuestos (potencia, horas, número de unidades, sobrecarga de enfriamiento, intensidad de carbono de la red) y reporta resultados como rangos condicionales. Se discute el posible impacto cualitativo de mecanismos de retención de estado sin potencia (no volatilidad) a nivel de arquitectura, señalando que su beneficio neto depende de la implementación completa del sistema.

## 1. Introducción
- Contexto: crecimiento del consumo energético asociado a cómputo para IA y necesidad de métricas comparables.
- Alcance: escenarios; no se atribuyen mediciones ni ahorros garantizados a una tecnología específica.

## 2. Metodología de cálculo
- Energía: `E = P · t · N · f_overhead`.
- Emisiones: `CO2 = E · I_grid` (con `I_grid` variable por región/tiempo).
- Escalamiento por eficiencia: para igual trabajo útil, `E_alt = E_ref / (η_alt/η_ref)` (supuesto de proporcionalidad, a discutir).
- Código/datos: `../../sustainability_energy.py`, `../../outputs/sustainability_scenarios.*`.

## 3. Escenarios y resultados (ilustrativos)
- Referencia ilustrativa: 700 W/unidad, 8760 h/año, 10,000 unidades, sobrecarga ×2, 0.4 kgCO2/kWh → 122.64 GWh/año, 49.056 ktCO2/año.
- Escenarios de eficiencia relativa 2×/10×/20×: reducciones del 50%/90%/95% bajo el supuesto de mismo trabajo útil.
- Presupuesto parcial de lectura (demostrador simulado): potencia estimada de subsistemas de lectura/control en orden de vatios bajos en el ejemplo, con eficiencia sistema-a-nivel dependiente de ADC/DAC, host y movimiento de datos (no incluida).

## 4. Discusión
- Sensibilidad a PUE, utilización real, perfil temporal, mix eléctrico y límites termodinámicos/prácticos.
- Impactos de ciclo de vida (fabricación, agua, e-waste) quedan fuera del modelo actual y deben tratarse en estudios específicos con datos.

## 5. Limitaciones
- Modelo simplificado; resultados no extrapolables sin validación de sistema y fuentes citadas para parámetros de referencia.

## 6. Conclusiones
- Los escenarios cuantifican órdenes de magnitud condicionales y sirven para comparar supuestos de eficiencia, no para certificar desempeño de una implementación concreta.

## Disponibilidad y declaraciones
- Ver `../../README.md`, `../../CITATION.cff`. Incluir citas a fuentes públicas para cifras de referencia en la versión para envío.
