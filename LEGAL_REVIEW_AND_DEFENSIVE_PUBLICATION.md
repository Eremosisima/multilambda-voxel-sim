# Revisión legal informativa y estrategia de publicación defensiva (no es asesoría legal)

> **Aviso importante:** Este documento es una guía informativa general para apoyar la discusión del proyecto. **No constituye asesoría legal, de propiedad intelectual ni de patentes.** Las leyes, criterios de patentabilidad, plazos y efectos varían por país y por jurisdicción. Antes de tomar decisiones (publicar, licenciar, divulgar detalles habilitantes, firmar acuerdos o renunciar a derechos), consulta a un **abogado/a de propiedad intelectual** calificado en las jurisdicciones relevantes.

## 1. Objetivo declarado
- Maximizar el **acceso abierto**, la reproducibilidad y el beneficio público/sostenible.
- Reducir el riesgo de que un tercero restrinja el uso mediante patentes sobre ideas ya divulgadas, mediante **publicación defensiva** (divulgación habilitante que pase a ser arte previo).
- Separar contribuciones en publicaciones independientes para que el conocimiento quede documentado en múltiples contextos (idiomas, revistas, comunidades), dificultando bloqueos por estrategias de una sola entidad.

## 2. Publicación defensiva (principios prácticos)
- **Divulgación habilitante y fechada:** publica una descripción suficientemente clara (problema, modelo, ecuaciones, parámetros, supuestos, variantes, resultados y limitaciones) en un medio con **fecha verificable**.
- **Canales con sello de tiempo y preservación:** preprints (p. ej. arXiv u otros repositorios abiertos), repositorios con DOI (Zenodo, OSF, repositorios institucionales), y revistas de acceso abierto. Conserva hashes/commits y evidencia de autoría.
- **Cobertura amplia de variantes:** dentro de lo ético y responsable, describe alternativas razonables (materiales candidatos, geometrías, rangos de parámetros, métodos de lectura/calibración) para fortalecer el valor como arte previo.
- **Coherencia:** no mezcles afirmaciones experimentales no realizadas con resultados simulados; etiqueta supuestos y escenarios.

## 3. Licenciamiento abierto (recomendaciones habituales, a validar)
- **Texto, figuras y manuscritos:** CC BY 4.0 (o la que exija la revista, verificando compatibilidad con tus objetivos).
- **Software de simulación:** Apache-2.0 o MIT (permisivas) o GPL según preferencia; incluye aviso de licencia y copyright.
- **Hardware/diseños (etapas futuras):** CERN-OHL-S v2 (strongly reciprocal) u otras variantes CERN-OHL según estrategia; documenta claramente qué archivos cubre.
- **Datos:** CC BY 4.0 o CC0 cuando proceda.
- Verifica compatibilidad entre licencias y las políticas de cada revista/repositorio.

## 4. Descomposición en artículos "no relacionados" (estrategia de desacoplamiento)
Para reducir el riesgo de que un solo paquete sea objetado/bloqueado por conflictos de interés externos y para ampliar el arte previo, separa en contribuciones con **objeto, método y evidencia distintos**:
- **A. Modelo matemático y decodificación:** álgebra lineal de la matriz de respuesta, condicionamiento, inversión, capacidad de niveles/bits, sensibilidad numérica (sin claims de dispositivo fabricado).
- **B. Simulación fotónica/interferométrica:** Δφ, márgenes de fase, presupuestos de SNR, sensibilidad a L/Γ/Δn (independiente de la tabla específica de compuestos si se parametriza).
- **C. Criterios de selección espectral/materiales (revisión/criterios):** ortogonalidad λ, estabilidad, Δn, compatibilidad, metodología de evaluación (compilación y criterios, no invención de un compuesto concreto).
- **D. Sostenibilidad y escenarios energético-ambientales:** modelo de escenarios kWh/CO₂, supuestos de sistema, marcos de evaluación para inferencia eficiente (independiente de la implementación física detallada).
- **E. Marco abierto/educativo y accesibilidad:** especificación de diseño de bajo costo, reproducibilidad, documentación abierta, gobernanza comunitaria.

**Buenas prácticas:** cada artículo debe tener **novedad propia, datos/figuras propios y redacción propia**; citar entre ellos solo cuando corresponda (o tratarlos como trabajos independientes si así se decide editorialmente) y evitar reutilización sustancial de texto/figuras (auto-plagio). Declara siempre que son estudios de simulación/escenario cuando aplique.

## 5. Consideraciones de riesgo y cumplimiento
- **No promesas de desempeño:** evitar afirmaciones no respaldadas (p. ej. TOPS/W medidos, ahorros garantizados) sin evidencia de sistema/prototipo.
- **Seguridad y doble uso:** este trabajo se presenta como memoria/lectura óptica y eficiencia; evita divulgar instrucciones para usos dañinos. (No aplica como riesgo principal aquí, pero es buena práctica general.)
- **Colaboraciones y acuerdos:** si trabajas con laboratorios, universidades o empresas, revisa cesión de derechos, confidencialidad y publicaciones antes de divulgar.
- **Patentes existentes:** una publicación defensiva puede ayudar contra patentes futuras sobre lo divulgado, pero **no elimina** el riesgo de patentes ya concedidas/solicitadas por terceros; considera una búsqueda de estado del arte (FTO/patent landscape) con apoyo profesional si planeas implementación/comercialización.

## 6. Checklist antes de publicar
- [ ] Supuestos, parámetros y limitaciones claramente etiquetados.
- [ ] Código y datos con licencia y README de reproducción.
- [ ] Fechado/DOI/preprint y archivo de versión enviada.
- [ ] Revisión de texto para evitar claims no soportados.
- [ ] Revisión de coautorías, afiliaciones y agradecimientos.
- [ ] Validación de políticas de la revista (acceso abierto, licencias, APC, idioma).
- [ ] **Consulta con abogado/a PI** para estrategia específica (especialmente si hay interés en patentar algo distinto o en operar en mercados regulados).

## 7. Nota sobre "blindaje" frente a empresas
Ninguna estrategia garantiza que no existan intentos de bloqueo (litigio, patentes previas, presión comercial). La combinación de **divulgación temprana, abierta, verificable y distribuida** + licencias abiertas + documentación habilitante es una de las formas más sólidas de favorecer el acceso público y el arte previo, pero debe complementarse con asesoría legal profesional según el caso.
