# Artículo A (borrador, ES): Modelo matemático de memoria óptica multinivel por superposición lineal y decodificación matricial

**Tipo:** teórico/simulación numérica (sin datos experimentales).  
**Contribución propia:** formulación paramétrica `y = A c + e`, análisis de condicionamiento, capacidad discreta y sensibilidad numérica de la decodificación.

## Resumen
Se presenta un modelo matemático para un voxel de memoria óptica con `M` materiales y `L` niveles discretos por material, donde el estado se representa como `c ∈ [0,1]^M`. Bajo un régimen lineal, la respuesta de lectura se modela como `y = A c + e`, con `A ∈ R^{M×M}` dependiente de parámetros físicos efectivos. Se analiza la invertibilidad/condicionamiento de `A`, la cuantización de estados y la sensibilidad del error de decodificación frente a perturbaciones (ruido y error de calibración). Resultados de simulación reproducible ilustran capacidad de `M·log2(L)` bits/voxel y condiciones numéricas para recuperación estable.

## 1. Introducción
- Motivación general: codificación multinivel y lectura multicanal como problema de estimación lineal.
- Delimitación: no se propone un dispositivo fabricado ni se reclaman métricas experimentales.

## 2. Modelo
- Estado: `c_i ∈ {0, 1/(L-1), ..., 1}`.
- Superposición: `Δn_i = c_i · Δn_i,max` (parámetro efectivo) y lectura lineal `y = A c + e`.
- Matriz `A`: términos diagonales dominantes y términos fuera de diagonal como fuga/crosstalk efectivo.
- Decodificación: `ĉ = argmin ||Ac - y||` (en caso cuadrado, `A^{-1}y`) + cuantización al nivel más cercano.

## 3. Métodos numéricos (reproducibles)
- Enumeración/muestreo de estados, inversión lineal, cuantización.
- Métricas: exactitud de palabra, tasa de error por símbolo, número de condición `cond(A)`.
- Sensibilidad: perturbaciones relativas en `A` y ruido aditivo gaussiano en `y`.
- Código/datos: `../../model.py`, `../../sensitivity.py`, `../../outputs/sensitivity_*`, `../../outputs/response_matrix_A.csv`.

## 4. Resultados (a partir del paquete)
- Caso base (M=4, L=4): 256 estados, `cond(A)=1.196` (escenario base), decodificación ideal 100% sin ruido.
- Barridos paramétricos: 60 puntos de diseño y 30 de crosstalk/ruido muestran dependencia del margen con el paso efectivo (función de parámetros físicos equivalentes).
- Reportar tablas/figuras propias derivadas de `outputs/sensitivity_*` y análisis de condición.

## 5. Discusión y limitaciones
- Validez del régimen lineal, no linealidades/saturación, errores de modelo y necesidad de calibración experimental en sistemas reales.
- La capacidad teórica no implica viabilidad física sin validación de parámetros.

## 6. Conclusiones
- El marco matricial proporciona una base transparente para evaluar capacidad y requisitos numéricos de lectura multinivel bajo supuestos explícitos.

## Disponibilidad
- Simulaciones y datos: repositorio del proyecto (ver `../../README.md`, `../../CITATION.cff`).

## Declaraciones
- Conflictos de interés: declarar los que correspondan.
- Financiamiento: declarar si aplica.
- Uso de herramientas: describir cualquier asistencia computacional/IA según política editorial.
