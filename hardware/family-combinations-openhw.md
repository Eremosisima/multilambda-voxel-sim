# Combinaciones de familias (candidatos fuertes) y estrategia Open Hardware / libertad de uso

> Documento de exploración conceptual (v0.8). Propone **combinaciones entre familias A–G** para maximizar velocidad, capacidad y compacidad, indicando factibilidad, fiabilidad, dimensiones y precio relativo, junto con pautas para que los diseños se publiquen y reutilicen como **hardware libre/open hardware** minimizando riesgos de infracción de propiedad intelectual.  
> **Aviso:** información técnica y organizativa general, **no asesoría legal**. “Libre” aquí se refiere a licenciamiento abierto (p. ej. CERN-OHL-S) y a prácticas que favorecen libertad de uso; no garantiza ausencia de patentes de terceros (libertad de operación/FTO).

## 1. Criterios de selección de combinaciones

| Criterio | Qué buscamos | Por qué |
|---|---|---|
| Velocidad | Reconfiguración ps–ns (EO/índice) e inferencia por propagación/interferencia | Cómputo dinámico y baja latencia |
| Capacidad | Alta densidad de pesos/canales (TOPS, MB, TB/s), apilamiento 3D/WDM vertical | Modelos/kernels mayores en el mismo módulo |
| Dimensiones | Alta capacidad por mm²/mm³ (cores/cerdas compactas, membranas apiladas) | Más cómputo en espacio reducido |
| Fiabilidad | Retención/endurance adecuadas, estabilidad de fase/térmica, márgenes | Operación sostenida y calibrable |
| Factibilidad | Plataformas/procesos disponibles, integración por etapas | Implementable por terceros con capital |
| Precio/accesibilidad | BOM/proceso escalable, rutas sin dependencia propietaria única | Alineado con misión de acceso/competencia |
| Apertura | Basado en principios físicos y descripciones habilitantes publicables, sin copiar material propietario | Open hardware reutilizable |

## 2. Matriz de combinaciones candidatas

### H1 — “Membrane-Brush NV” (A1 + G3 + 3D cepillo)
- **Composición:** base interferométrica PCM no volátil (**A1**, MVM/pesos) + membranas apiladas de película delgada en cerda con **PCM+ajuste EO** (**G3**) + distribución volumétrica tipo cepillo (**F2/3D**).
- **Mecanismo:** cómputo/pesos persistentes por MZI/PCM; selección y ponderación espectral por interferencia de espesor $n d$ (constructiva/destructiva) en capas verticales; corrección rápida por sintonía de índice (EO).
- **Fortalezas:** muy alta **capacidad** (memoria NV + WDM vertical) y buena densidad volumétrica; velocidad de inferencia alta y reconfiguración parcial rápida (EO) con retención (PCM). Buen encaje con jerarquía M0–M3/OMCC.
- **Compromisos:** integración 3D y apilado multicapa complejos; tolerancias de espesor/fase y gestión térmica (zonas PCM). **Factibilidad** media-baja a corto plazo, alta a medio plazo por modularidad.
- **Perfil (conceptual):** velocidad media-alta, capacidad muy alta, dimensiones compactas en volumen, fiabilidad media, precio medio-alto, factibilidad media.
- **Ruta open:** especificar geometrías/parámetros genéricos (mallas MZI, apilados F–P, pila de materiales funcionales) y protocolos OMCC; evitar dependencia de IP de un único proveedor de PIC/proceso.

### H2 — “RT Membrane-WDM Core” (G2 + B3 + C1)
- **Composición:** membranas/cavidades sintonizables por índice **EO** (**G2**) + banco resonante **WDM** (**B3**) + conducción/interconexión EO rápida (**C1**) para núcleos dinámicos.
- **Mecanismo:** conmutación/ponderación por interferencia de espesor $n d$ y resonante, ambas desplazadas por EO; paralelismo espectral masivo en volumen reducido.
- **Fortalezas:** **velocidad** y **ancho de banda** muy altos, alta capacidad de cómputo/canales en espacio reducido (núcleos “core” densos), buena escalabilidad para streaming/GPU-NPU tiempo real.
- **Compromisos:** pesos mayormente volátiles (requiere recarga/buffers), consumo de drivers RF, sensibilidad térmica de resonadores. **Fiabilidad** dependiente de control térmico/fase.
- **Perfil (conceptual):** velocidad muy alta, capacidad alta (cómputo/BW) y memoria NV limitada, dimensiones compactas, fiabilidad media-alta con control, precio alto, factibilidad media-baja.
- **Ruta open:** basar en principios F–P/ring/MZI y control EO genérico; publicar calibración y mapas de control; preferir plataformas con procesos documentados.

### H3 — “Open WDM-PCM” (A1 + G1 + B3) — *candidato de mayor factibilidad abierta*
- **Composición:** pesos/compute **A1** (PCM-MZI, referencia actual) + membranas/filtros de espesor fijo **G1** para WDM vertical/filtrado pasivo + resonadores/banco **B3** donde aporte densidad.
- **Mecanismo:** elementos pasivos de película delgada (espesores fijos, sin sintonía activa compleja) proporcionan selección por interferencia constructiva/destructiva; A1 aporta pesos NV; WDM aumenta paralelismo.
- **Fortalezas:** **factibilidad y precio** relativamente mejores (muchas capas pasivas usan recubrimientos dieléctricos estándar), buena **capacidad** por WDM/apilado pasivo, retención NV, ruta incremental desde el diseño de referencia.
- **Compromisos:** reconfiguración lenta (PCM) y menor agilidad que H2; rendimiento limitado por tolerancias de fabricación pasiva.
- **Perfil (conceptual):** velocidad media (inferencia alta, reprog. lenta), capacidad media-alta, dimensiones buenas, fiabilidad media, precio bajo-medio, **factibilidad más alta**.
- **Ruta open:** prioritaria para “open hardware accesible”: materiales dieléctricos comunes (SiN/SiO₂/TiO₂, etc.), procesos de depósito conocidos, documentación completa de espesores/apilados y scripts de diseño.

### H4 — “Volumetric Tensor Membrane” (G2/G3 + F2 + A1)
- **Composición:** cores de membrana apilada **G2/G3** en cerdas 3D + etapa **difractiva/metasuperficie** (**F2**) para mezcla global + bloques **A1** para pesos NV donde convenga.
- **Mecanismo:** cómputo local espectral/por espesor en volumen + transformaciones/mixing espacial masivo por interferencia/difracción.
- **Fortalezas:** **capacidad y throughput** potencialmente muy altos (volumétrico + espacial + WDM), adecuado para GEMM/tensores grandes.
- **Compromisos:** alineación/calibración exigente, complejidad de integración y verificación; precio y riesgo técnico altos.
- **Perfil (conceptual):** velocidad alta, capacidad muy alta, dimensiones eficientes en cómputo/volumen pero sistema complejo, fiabilidad media, precio alto, factibilidad baja-media.
- **Ruta open:** modularizar (core de membrana, plano difractivo, plano A1) con interfaces publicadas para que distintos implementadores aborden subsistemas.

### H5 — “Dense Resonant Stack” (B1 + G3 + D1 selectivo)
- **Composición:** celdas resonantes de alta densidad **B1** (BIC/ring) + capas/membranas **G3** (PCM+EO) + opcional **D1** (ENZ/plasmónico) solo en hotspots de activación no lineal.
- **Mecanismo:** confinamiento resonante + selección por espesor $n d$ + no linealidad localizada donde sea necesaria (NPU).
- **Fortalezas:** **dimensiones/capacidad por área** muy buenas y eficiencia energética potencial; soporte de funciones lineales y no lineales en compacto.
- **Compromisos:** pérdidas (especialmente si hay plasmónica), sensibilidad a fabricación/térmica, madurez baja. **Fiabilidad** a validar.
- **Perfil (conceptual):** velocidad media-alta, capacidad alta en huella pequeña, fiabilidad media-baja inicial, precio medio-alto, factibilidad baja.
- **Ruta open:** aislar la parte plasmónica/ENZ como bloque opcional con alternativas dieléctricas documentadas.

## 3. Comparativa resumida de combinaciones (conceptual)

| Combo | Velocidad | Capacidad | Dimensiones (densidad) | Fiabilidad | Factibilidad | Precio rel. | Potencial open/accesible |
|---|---|---|---|---|---|---:|---|
| **H1 A1+G3+3D** | media-alta | muy alta (NV+WDM 3D) | muy alta (volumen) | media | media | 2.3 | alto (modular, principios genéricos) |
| **H2 G2+B3+C1** | muy alta | alta (BW/cómputo), NV baja | alta | media-alta* | media-baja | 2.7 | medio (plataformas EO/RF) |
| **H3 A1+G1+B3** | media | media-alta | buena | media | **alta** | **1.4** | **muy alto** (pasivo + ref A1) |
| **H4 G2/G3+F2+A1** | alta | muy alta | alta (sistema complejo) | media | baja-media | 3.0 | medio (si se modulariza) |
| **H5 B1+G3(+D1)** | media-alta | alta (área) | muy alta (área) | media-baja | baja | 2.4 | medio-bajo (ENZ/plasmónica opcional) |

\*Con control térmico/fase y calibración (OMCC). Valores orientativos, no medidos.

## 4. Estrategia para que sean Open Hardware y “libres” sin infringir

### 4.1 Licenciamiento y apertura (lo que sí controlamos)
- **Hardware/diseños:** publicar esquemáticos, máscaras/layouts (cuando existan), modelos paramétricos, BOM y documentación de fabricación bajo **CERN-OHL-S v2** (`LICENSE-HARDWARE`), de forma recíproca.
- **Código/simulaciones/RTL/firmware:** **Apache-2.0** (o equivalente permisiva/compatible elegida) con avisos `NOTICE`.
- **Documentación/datos:** **CC BY-SA 4.0** (o la indicada) para textos, figuras y datasets.
- **Práctica:** incluir fuentes editables, scripts reproducibles, parámetros y notas de procedencia; esto maximiza reutilización y competencia (objetivo de accesibilidad).

### 4.2 Evitar infracción de copyright (expresión)
- No copiar **texto, figuras, esquemáticos, código, máscaras/layouts, fotos o datasheets** de terceros sin licencia compatible; los hechos/leyes físicas y datos técnicos no son copyright, pero su **expresión** sí.
- Redactar y dibujar material propio; cuando se referencie información externa, **citar fuentes** y usar únicamente lo permitido (hechos, ideas, uso compatible).
- Verificar procedencia de aportes de colaboradores/herramientas y registrar autoría/licencias (`NOTICE`, `AI_AUTHORSHIP_NOTE.md`).

### 4.3 Reducir riesgo de patentes (invención/implementaciones) — *no garantizable sin FTO*
> El licenciamiento abierto **no elimina** patentes vigentes de terceros. Para acercarse a implementaciones “libres de restricciones” en la práctica:
- **Basarse en principios físicos y arte previo:** interferencia de película delgada/F–P, MZI, resonadores, WDM, modulación de índice y apilamiento dieléctrico son conceptos ampliamente conocidos; documentar configuraciones **genéricas** y parámetros como publicación defensiva (arte previo) con fecha verificable.
- **Evitar topologías/implementaciones específicas patentadas cuando haya alternativas:** p. ej. geometrías particulares de modulador, esquemas propietarios de control, celdas o flujos cerrados; preferir variantes de dominio público o de literatura abierta y dejar constancia de alternativas.
- **Modularidad y sustituibilidad:** diseñar interfaces para poder reemplazar un bloque (p. ej. modulador EO, tipo de resonador, material de membrana) por una implementación con mejor situación FTO.
- **FTO (freedom-to-operate) antes de fabricar/comercializar:** búsqueda de patentes en jurisdicciones objetivo y revisión por especialista en PI; especialmente relevante en EO integrado (TFLN/BTO), resonadores y arquitecturas de aceleradores.
- **No afirmar “libre de patentes”:** declarar estado conceptual, publicar como referencia abierta y recomendar FTO a implementadores.

### 4.4 Recomendación de cartera abierta
- **Corto plazo (máxima apertura/factibilidad):** **H3 (A1+G1+B3)** — predominio de elementos pasivos conocidos + referencia A1, alta documentabilidad y bajo coste relativo.
- **Medio plazo (rendimiento/capacidad):** **H1 (A1+G3+3D)** — modular, NV + capacidad volumétrica, evolucionable.
- **Alto rendimiento dinámico:** **H2 (G2+B3+C1)** — publicar diseños genéricos y calibración; sujeto a FTO en EO/RF.
- Todos los candidatos deben publicarse con especificación habilitante, datos de simulación y licencias abiertas para fortalecer arte previo y reutilización.

## 5. Trabajo siguiente
- Añadir modelos específicos por combo (TMM multicapas G, resonador WDM, enlace EO) y normalizar comparativas por mm²/mm³ y por W.
- Documentar interfaces abiertas entre bloques (óptico, eléctrico, térmico, control OMCC) para sustituibilidad.
- Completar paquete de publicación defensiva por combo (descripción habilitante, variantes, fechas/DOI) y checklist FTO para implementadores.
