# Artículo C (borrador, ES): Criterios de selección y ortogonalidad espectral de conmutadores fotoactivos para memoria óptica multicanal (marco metodológico)

**Tipo:** metodológico / revisión acotada basada en literatura (a completar con citas primarias).  
**Contribución propia:** marco de criterios y matriz de evaluación para seleccionar conjuntos de materiales/cromóforos candidatos según ortogonalidad, Δn efectivo, estabilidad y compatibilidad.

## Resumen
Se propone un marco metodológico para evaluar conjuntos de conmutadores fotoactivos destinados a esquemas conceptuales de almacenamiento/lectura multicanal. El marco considera: ventanas espectrales de activación y lectura, cambio de índice de refracción efectivo, estabilidad térmica, fatiga, cinética y compatibilidad de integración. Se incluye una tabla de parámetros **de trabajo para simulación** (no experimental) que debe sustituirse por valores reportados en literatura citada. El objetivo es estandarizar criterios de comparación y explicitar incertidumbres, sin reivindicar un material o conjunto específico como invención validada.

## 1. Introducción
- Importancia de ortogonalidad espectral y estabilidad para reducir crosstalk en sistemas multicanal.
- Alcance: criterios de selección y evaluación; no se presentan síntesis ni mediciones nuevas.

## 2. Criterios de evaluación
- **Ortogonalidad espectral:** separación entre bandas de escritura/borrado/lectura; solapamiento y riesgo de activación parásita.
- **Respuesta óptica:** Δn(λ) efectivo, linealidad, rango dinámico y niveles alcanzables.
- **Estabilidad y fiabilidad:** vida media térmica, foto-fatiga, repetibilidad de ciclos.
- **Integración:** compatibilidad con matriz/guía, temperatura de proceso, uniformidad.
- **Seguridad y disponibilidad:** consideraciones prácticas y de manejo según fichas y normativa aplicable (a documentar con fuentes).

## 3. Metodología propuesta
- Matriz de decisión multicriterio (pesos definidos por aplicación) y análisis de sensibilidad a incertidumbre de parámetros.
- Reglas de documentación: cada parámetro acompañado de fuente, condiciones de medición y rango de variabilidad reportado.

## 4. Conjunto ilustrativo para simulación (a reemplazar por literatura citada)
- Usar `../../outputs/compounds.csv` y `../../compounds.py` **solo como ejemplo paramétrico**. En la versión para envío: sustituir por tabla con referencias primarias por material/familia, condiciones (matriz, longitud de onda, temperatura) y valores reportados.

## 5. Discusión
- Riesgos de inferir ortogonalidad a partir de valores nominales sin espectros completos.
- Necesidad de estandarizar métricas (Δn, t1/2, ciclos) para comparabilidad.

## 6. Conclusiones
- Un marco explícito de criterios y trazabilidad a fuentes facilita comparaciones rigurosas y evita sobreinterpretación de parámetros de simulación.

## Trabajo pendiente obligatorio para envío
- Completar búsqueda bibliográfica y citas primarias; ajustar o retirar cualquier valor no respaldado.
- Declarar conflictos, financiamiento y método de revisión.
