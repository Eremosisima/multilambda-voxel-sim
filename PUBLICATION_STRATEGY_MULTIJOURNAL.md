# Estrategia de publicación en múltiples artículos y revistas (acceso abierto, varias en español)

Objetivo: descomponer el trabajo en **contribuciones independientes** (métodos, datos y narrativa distintos) publicables en diferentes revistas/plataformas de acceso abierto —incluyendo opciones en español— para ampliar difusión, arte previo y resiliencia ante conflictos de interés externos. Cada pieza debe ser científicamente autónoma y cumplir políticas editoriales.

> **Nota:** Las revistas y condiciones (APC, alcance, idioma, indexación) cambian. Verificar siempre en DOAJ, SciELO, Redalyc, Latindex y en la web oficial de cada revista antes de enviar.

## Paquetes de artículo propuestos (independientes)

### Artículo A (ES) — Modelo matemático y decodificación por inversión de matriz
- **Foco:** formulación `y = A c + e`, condicionamiento de `A`, cuantización multinivel, capacidad (bits/voxel) en función de niveles/canales, sensibilidad numérica y requisitos de calibración. Sin depender de un dispositivo fabricado ni de un set propietario de compuestos.
- **Evidencia:** derivaciones, simulaciones numéricas paramétricas (sensibilidad), figuras de condición/margen/error.
- **Posibles destinos (verificar):** revistas OA en español de matemática aplicada/ingeniería/física teórica o educación superior en SciELO/Redalyc/DOAJ (p. ej. categorías de modelado, procesamiento de señales, ingeniería). Alternativa: preprint en español + repositorio con DOI.
- **Idioma:** español (con abstract en inglés).

### Artículo B (ES/EN) — Simulación interferométrica y presupuesto de lectura por fase
- **Foco:** relación `Δφ = (2π/λ) Γ Δn L`, diseño paramétrico de MZI/canales, márgenes de cuantización, presupuesto de ruido (shot/deriva térmica, etc.) y robustez frente a crosstalk/calibración. Parametrizado (no atado a una marca/química específica).
- **Evidencia:** `outputs/mzi_*`, `outputs/sensitivity_*`, `outputs/snr_budget.*`, figuras.
- **Posibles destinos (verificar):** revistas OA de óptica/fotónica/instrumentación o ingeniería eléctrica/electrónica (SciELO/DOAJ; algunas aceptan español/inglés/portugués). Preprint técnico en inglés para visibilidad internacional.
- **Idioma:** español o inglés según revista.

### Artículo C (ES) — Criterios de ortogonalidad espectral y estabilidad para conmutadores fotoactivos (marco de selección)
- **Foco:** metodología y criterios para seleccionar conjuntos de conmutadores (ventanas λ de escritura/borrado/lectura, Δn, vida media, fatiga, compatibilidad de matriz) y matriz de decisión; puede presentarse como estudio metodológico/revisión sistemática acotada con datos de literatura **debidamente citados**.
- **Evidencia:** tabla comparativa basada en fuentes publicadas, criterios de ortogonalidad/crosstalk espectral, discusión de incertidumbre. (Evitar presentar valores no citados como hechos.)
- **Posibles destinos (verificar):** revistas OA en español de química/fotoquímica/ciencia de materiales/ingeniería de materiales (SciELO/Redalyc).
- **Idioma:** español.

### Artículo D (ES) — Escenarios de eficiencia energética y huella para inferencia con memoria no volátil (análisis de escenarios)
- **Foco:** modelo de cálculo kWh/CO₂, sensibilidad a TOPS/W, PUE, mix eléctrico y utilización; discusión de no volatilidad (retención sin potencia) como supuesto a validar a nivel sistema. **No** atribuir ahorros medidos sin prototipo.
- **Evidencia:** `outputs/sustainability_scenarios.*`, supuestos explícitos, rangos.
- **Posibles destinos (verificar):** revistas OA en español de energía, sostenibilidad, tecnología y sociedad, ingeniería ambiental/industrial (SciELO/Redalyc/DOAJ).
- **Idioma:** español.

### Artículo E (ES/EN) — Especificación abierta y educativa de un demostrador de bajo costo (diseño conceptual reproducible)
- **Foco:** arquitectura abierta, lista de componentes de bajo costo (rangos), modularidad pro/educativa, documentación y licencias abiertas, consideraciones de seguridad y reproducibilidad. Sin revelar ni requerir fabricación propietaria.
- **Evidencia:** esquemas conceptuales, BOM orientativa, guía de replicación y gobernanza open-source/hardware.
- **Posibles destinos (verificar):** journals de open hardware/educación en ingeniería (DOAJ) y/o revistas iberoamericanas de innovación educativa/tecnología abierta.
- **Idioma:** español e inglés (versiones o complementos según lo permita la política).

## Plataformas transversales (preprints/repositorios con fecha y DOI)
- **Preprints:** arXiv (EN) y/o repositorios regionales/institucionales en español cuando existan; también OSF Preprints.
- **Archivo con DOI:** Zenodo (código, datos, figuras, versiones de manuscrito) para fijar arte previo con identificador persistente.
- **Índices para buscar revistas OA:** DOAJ, SciELO, Redalyc, Latindex Catálogo 2.0; filtrar por idioma español, APC = 0 si se busca "libre de cargos", y área temática.

## Secuenciación sugerida (minimiza solapamiento)
1. Publicar código/datos + nota técnica en repositorio con DOI (base común reproducible).
2. Enviar Art. A y B (núcleo modelo/simulación) como preprints separados con énfasis distinto.
3. Enviar Art. D (sostenibilidad) a revista ES de energía/sostenibilidad (audiencia distinta).
4. Preparar Art. C con citas de literatura reales (trabajo bibliográfico) y enviarlo a revista ES de materiales/química.
5. Art. E como especificación abierta/educativa en venue de open hardware/educación.

## Reglas para evitar problemas editoriales
- No reciclar texto/figuras sustanciales entre manuscritos; cada uno con su contribución y conjunto de resultados.
- Declarar relación entre trabajos solo si la revista lo requiere (p. ej. "trabajo complementario") y ser transparente con editores.
- No fragmentar artificialmente resultados mínimos: cada artículo debe responder una pregunta clara y valiosa por sí mismo.
- Mantener trazabilidad: mismos parámetros base versionados, pero análisis y objetivos distintos por artículo.
