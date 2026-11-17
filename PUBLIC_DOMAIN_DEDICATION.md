# Dedicación al dominio público (propuesta) y ajustes necesarios

> **Objetivo:** poner el contenido original de este repositorio a disposición de todo el mundo en **dominio público** (en la máxima medida permitida por la ley).  
> **Estado:** documento de análisis y plan de ajustes (v0.8). **No es asesoría legal.** La dedicación efectiva requiere la decisión y acción de los/las titulares de derechos sobre las obras originales.  
> **Alcance:** monorepo `multilambda-voxel-sim` / OPGPU y, si se decide, los repos de staging en `candidates/` (cada uno independiente).

## 1. Situación actual de licenciamiento (a ajustar)

| Ámbito (actual) | Licencia declarada | Naturaleza | Ajuste para dominio público |
|---|---|---|---|
| Código (simulaciones, scripts, modelos, software) | **Apache License 2.0** (`LICENSE`) | Permisiva con condiciones (aviso, NOTICE, concesión de patente) | Sustituir/renunciar a favor de dedicación a dominio público (p. ej. **CC0 1.0**) o mantener dual-licencia si se desea; eliminar condiciones incompatibles con “sin restricciones” |
| Diseño/documentación de hardware (`hardware/`, diseños, esquemáticos, parámetros) | **CERN-OHL-S v2** (`LICENSE-HARDWARE`) | Copyleft fuerte/recíproca + concesión de patente condicionada | **Cambio sustancial:** requiere reemplazo por **CC0 1.0** (o equivalente) para renunciar a reciprocidad y, en lo posible, a restricciones de copyright; revisar implicaciones de patente |
| Documentación (textos, figuras, datos/documentos; según directorio) | **CC BY-SA 4.0** (`LICENSE-docs`, partes indicadas) / referencias a CC BY 4.0 en `README` | Atribución (BY) y, en BY-SA, compartición igual (SA) | Reemplazar por **CC0 1.0** para eliminar requisitos de atribución/SA como condición de licencia (se puede mantener atribución voluntaria como crédito) |
| Avisos/procedencia | `NOTICE`, `AI_AUTHORSHIP_NOTE.md`, cabeceras/README/CHANGELOG | Atribución, procedencia, disclaimers | Conservar como **informativos** (provenance/crédito/seguridad), pero no como condiciones de licencia de dominio público |
| Candidatos (`candidates/*`) | Copias de Apache/CERN-OHL-S/CC BY-SA + `NOTICE` por repo | Independientes, mismo esquema mixto | Aplicar los mismos ajustes en cada repo/candidato si se publican como dominio público |

**Documentos/referencias a actualizar por coherencia:** `README.md`, `CHANGELOG.md`, `MISSION_AND_ADOPTION.md`, `NOTICE`, `CANDIDATE_REPOS_STRATEGY.md`, `candidates/README.md`, y los apartados “Licencia propuesta/licencias” en `hardware/*.md` (p. ej. `current-strategies-schematics-and-instructions.md`, `open-photonic-gpu-v1-schematic-pcie.md`, `schematics-deep-dive.md`, `pcie-bridge-opencl-openvino.md`, `IP_AND_OPEN_HW.md` en candidatos), `CITATION.cff` si aplica.

## 2. Qué significa “dominio público” y herramienta recomendada

- **Dedicación a dominio público (copyright):** los titulares renuncian, en la medida máxima permitida por la ley, a los derechos de autor sobre la obra, permitiendo copiar, modificar, distribuir y usar (incluso con fines comerciales) **sin pedir permiso ni cumplir condiciones** (atribución, share-alike, avisos) como requisito de licencia.
- **Herramienta recomendada:** **Creative Commons CC0 1.0 Universal** (dedicación/waiver + licencia de respaldo “fallback” donde el waiver no sea plenamente efectivo). Es el instrumento estándar y ampliamente reconocido para código, datos, documentación y diseños.
  - Texto legal: https://creativecommons.org/publicdomain/zero/1.0/legalcode
  - Resumen: https://creativecommons.org/publicdomain/zero/1.0/
- **Limitaciones importantes (no eliminadas por CC0):**
  - **Patentes:** CC0 (según su texto) no otorga una licencia de patente afirmativa en los mismos términos que Apache-2.0/CERN-OHL-S; en la práctica, el waiver de copyright no equivale a una garantía de libertad de operación (FTO). Riesgos de patentes de terceros **persisten**.
  - **Marcas:** nombres/marcas (p. ej. PCIe, OpenCL, OpenVINO) siguen sujetos a derechos de marca; su uso nominativo debe mantenerse correcto.
  - **Garantías/responsabilidad:** la obra se ofrece “tal cual”, sin garantías (esto es compatible con dominio público/CC0).
  - **Derechos morales y leyes locales:** en algunas jurisdicciones los derechos morales no son renunciables totalmente; CC0 incluye una renuncia en la medida posible.
  - **Obras de terceros:** solo puede dedicarse lo que es obra original propia (o sobre lo que se tienen derechos suficientes). Materiales de terceros, si los hubiera, quedan excluidos.
  - **Copias ya distribuidas:** quienes recibieron copias bajo licencias anteriores (Apache-2.0, CERN-OHL-S v2, CC BY/SA) conservan los derechos otorgados por esas licencias para esas copias; la nueva dedicación aplica hacia adelante y a las copias distribuidas bajo los nuevos términos por los titulares que la adopten.

## 3. Ajustes necesarios (checklist de transición)

### 3.1 Decisión y titularidad (requisito previo)
- [ ] Confirmar que **todos los titulares de derechos** de las contribuciones originales (autores/colaboradores) consienten la dedicación a dominio público/CC0. Sin consenso, solo puede dedicarse la parte propia.
- [ ] Identificar y **excluir o relicenciar** cualquier contenido de terceros incorporado (texto, figuras, código, datos, esquemáticos, máscaras) que no sea dedicable; mantener registro de procedencia.
- [ ] Confirmar que no hay obligaciones contractuales/confidenciales incompatibles.

### 3.2 Archivos de licencia y avisos (monorepo)
- [ ] **Añadir** un archivo de dedicación, p. ej. `LICENSE` o `LICENSE-CC0` / `COPYING`, con el **texto legal completo de CC0 1.0** y una nota de dedicación que identifique la obra y a los titulares (y fecha).
- [ ] **Retirar o reemplazar** `LICENSE` (Apache-2.0, código), `LICENSE-HARDWARE` (CERN-OHL-S v2) y `LICENSE-docs` (CC BY-SA 4.0) si la intención es dominio público uniforme. (Alternativa: declarar CC0 como licencia principal y conservar las anteriores solo como referencia histórica en `CHANGELOG`/historial, dejando claro que ya no rigen las versiones nuevas — decisión de los titulares.)
- [ ] **Actualizar `NOTICE`:** pasar de “licencias X/Y/Z” a una declaración de **dominio público/CC0**, conservando procedencia, créditos (opcionales pero recomendados), disclaimers de seguridad (láser/térmica), ausencia de garantía y aclaración de no-FTO/patentes/marcas.
- [ ] **Actualizar `README.md` y `CHANGELOG.md`:** describir el nuevo régimen (dominio público vía CC0), alcance, exclusiones y fecha; registrar la entrada de cambio de licencia.
- [ ] **Actualizar `MISSION_AND_ADOPTION.md` y `CANDIDATE_REPOS_STRATEGY.md`:** alinear el objetivo (“accesibilidad/competencia”) con el hecho de que dominio público elimina condiciones de licencia (distinto de copyleft recíproco); mantener advertencias FTO/C&D.
- [ ] **Actualizar `CITATION.cff`** (si existe) para reflejar la licencia CC0 y metadatos vigentes.

### 3.3 Documentación y cabeceras en el contenido
- [ ] Revisar cabeceras y secciones “Licencia propuesta / Licencias” en `hardware/*.md`, `articles/*`, y documentos raíz: reemplazar referencias a CERN-OHL-S/Apache/CC BY-SA por **CC0 1.0 / dominio público**, manteniendo avisos técnicos y de seguridad.
- [ ] En esquemáticos y docs clave (`hardware/current-strategies-schematics-and-instructions.md`, `hardware/pcie-bridge-opencl-openvino.md`, `hardware/open-photonic-gpu-v1-schematic-pcie.md`, `hardware/schematics-deep-dive.md`, etc.) indicar: “Dedicado al dominio público (CC0 1.0) en la medida permitida por la ley; sin garantía; patentes/FTO no garantizadas”.
- [ ] (Opcional) Añadir una cabecera breve uniforme en archivos de código/fuentes: referencia a CC0 y al archivo de licencia.

### 3.4 Candidatos (`candidates/`) y modularidad
- [ ] Decidir si los candidatos de staging se publican también como dominio público: replicar en cada `candidates/<nombre>/` el nuevo `LICENSE`/CC0, `NOTICE` y actualizar `README.md`, `DESIGN.md`, `IP_AND_OPEN_HW.md`.
- [ ] Si algún candidato debe permanecer bajo otra licencia por estrategia, documentarlo explícitamente (el monorepo puede ser CC0 y un candidato distinto, siempre que el contenido sea separable y los derechos lo permitan).

### 3.5 Publicación y comunicación
- [ ] Hacer commit con mensaje explícito (p. ej. “Dedicate original work to public domain (CC0 1.0)”) y **push** a GitHub.
- [ ] Actualizar la descripción/licencia del repositorio en la forja (selector de licencia → CC0 o “public domain”, si está disponible) para que sea visible externamente.
- [ ] Archivar en Wayback Machine las páginas relevantes tras el cambio (README, archivos de licencia, hardware/).
- [ ] (Opcional) Publicar un release/DOI indicando la dedicación para trazabilidad de procedencia/fecha.

## 4. Redacción sugerida de dedicación (a adaptar por los titulares)

> *Los titulares de derechos de las obras originales contenidas en este repositorio, en la medida en que ostentan dichos derechos, dedican dichas obras al dominio público mundial mediante CC0 1.0 Universal, renunciando a todos sus derechos de autor y derechos conexos en la máxima medida permitida por la ley aplicable. La obra se proporciona “tal cual”, sin garantía de ningún tipo. Esta dedicación no constituye una licencia de patentes ni garantiza libertad de operación; no afecta derechos de marca ni derechos sobre obras de terceros. Se recomienda, de forma no obligatoria, mantener el crédito de procedencia.*

Colocar el texto legal completo de CC0 1.0 en el archivo de licencia y referenciarlo desde `README.md` y `NOTICE`.

## 5. Resumen de impacto

| Aspecto | Antes (mixto) | Después (dominio público/CC0) |
|---|---|---|
| Uso/copia/modificación/redistribución | Permitido con condiciones (atribución, SA/reciprocidad, avisos según licencia) | Permitido **sin condiciones de copyright** (en la medida posible) |
| Atribución | Requerida (Apache NOTICE/CC BY/SA) | **No requerida** por licencia (recomendada como crédito) |
| Reciprocidad (hardware/docs) | Requerida (CERN-OHL-S, CC BY-SA) | **No requerida** |
| Patentes | Concesión condicionada (Apache, CERN-OHL-S) | **Sin concesión explícita equivalente**; FTO no garantizada |
| Accesibilidad para terceros | Alta, con obligaciones | Máxima en términos de copyright |

## 6. Referencias internas y externas
- Internas: `LICENSE`, `LICENSE-HARDWARE`, `LICENSE-docs`, `NOTICE`, `README.md`, `CHANGELOG.md`, `MISSION_AND_ADOPTION.md`, `CANDIDATE_REPOS_STRATEGY.md`, `hardware/*`.
- Externas: CC0 1.0 https://creativecommons.org/publicdomain/zero/1.0/ ; guía de licencias open hardware https://ohwr.org/project/cernohl/wikis/home ; políticas de dominio público de datos/código (según jurisdicción).  

*Documento preparado para revisión por los titulares del proyecto. No constituye asesoría legal.*