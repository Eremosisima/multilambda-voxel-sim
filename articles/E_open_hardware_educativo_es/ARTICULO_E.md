# Artículo E (borrador, ES): Especificación abierta de un demostrador educativo de bajo costo para conceptos de memoria óptica y lectura por fase

**Tipo:** especificación conceptual / recurso educativo abierto (sin prototipo certificado).  
**Contribución propia:** arquitectura modular documentada, criterios de bajo costo y reproducibilidad, y lineamientos de licenciamiento abierto para fines educativos y de investigación.

## Resumen
Se propone una especificación abierta de alto nivel para un demostrador educativo orientado a ilustrar conceptos de codificación de estado, lectura por fase y procesamiento de señales en sistemas ópticos/mixtos, priorizando componentes accesibles, documentación clara y seguridad. La especificación distingue entre un perfil educativo (baja complejidad/costo) y un perfil de investigación (mayores requisitos), sin afirmar desempeño equivalente a equipos industriales ni resultados experimentales no verificados. Se incluyen recomendaciones de licencias abiertas, materiales didácticos y prácticas de reproducibilidad.

## 1. Objetivos y alcance
- Facilitar aprendizaje y replicación de conceptos (modelo, calibración, ruido, lectura) con enfoque abierto.
- No sustituye diseños certificados ni pretende aplicaciones críticas de seguridad.

## 2. Arquitectura conceptual (modular)
- **Módulo óptico:** fuente(s), camino interferométrico/guía equivalente, medio de modulación conceptual; énfasis en medición de fase/intensidad según montaje.
- **Módulo de detección y control:** sensores/fotodetectores, adquisición, control de bajo costo (microcontrolador/FPGA educativa según caso).
- **Módulo de software:** scripts de adquisición, calibración, decodificación y visualización (reutilizar/adapter `../../model.py` y herramientas del repo).
- **Documentación:** lista de materiales orientativa por rangos de costo, montaje, riesgos y calibración.

## 3. Consideraciones de bajo costo y accesibilidad
- Preferir componentes ampliamente disponibles y documentación en español.
- Definir versión mínima viable para aula/laboratorio docente y ruta de escalamiento opcional.
- Incluir alternativas cuando un componente no esté disponible localmente.

## 4. Seguridad, ética y cumplimiento
- Seguridad láser/eléctrica según normas locales; uso solo en entornos adecuados y con supervisión cuando corresponda.
- Transparencia: etiquetar como demostrador educativo; no realizar claims de desempeño industrial.
- Respeto de licencias de software/hardware de terceros y atribución adecuada.

## 5. Licenciamiento y apertura
- Software: Apache-2.0/MIT u otra licencia abierta compatible.
- Documentación y materiales didácticos: CC BY 4.0 (recomendado) u opción elegida.
- Diseños de hardware (si se publican): CERN-OHL v2 (variante según objetivos) con documentación de fabricación.

## 6. Evaluación educativa (propuesta)
- Rúbricas de aprendizaje: comprensión del modelo, calibración, análisis de error/SNR y documentación de experimentos.
- Fomentar reporte de limitaciones y resultados negativos.

## 7. Limitaciones
- Especificación conceptual sujeta a validación práctica, disponibilidad de componentes y revisión de seguridad.

## Disponibilidad
- Recursos de simulación base: `../../` (ver `../../README.md`, `../../ARCHIVING.md`). Adaptar y versionar materiales antes de publicación.