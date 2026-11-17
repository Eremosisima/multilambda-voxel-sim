# Plan de publicación de todas las versiones (dominio público, sin conflictos) — Zenodo + ip.com

> Objetivo: publicar **todas las estrategias, esquemáticos, instrucciones, diseños, código y datos originales** del proyecto en **dominio público (uso libre universal)** y como **divulgación defensiva/arte previo**, de forma fechada y habilitante, para maximizar utilidad a la humanidad y dificultar apropiación registral/monopolización de lo divulgado (sin garantía absoluta, no asesoría legal).

## 0. Principio y precedentes (enfoque a seguir)

Enfoque alineado con prácticas históricas de protección del bien común frente a apropiación abusiva:
- **Divulgación defensiva / arte previo:** publicar descripciones habilitantes, públicas y fechadas para que lo divulgado no sea patentable por terceros (p.ej. publicaciones técnicas, defensive disclosures). 
- **Dominio público / CC0:** renuncia de copyright en la medida permitida por la ley para permitir uso, estudio, fabricación y mejora por cualquiera sin condiciones (inspirado en la tradición de poner conocimiento esencial al servicio público, p.ej. renuncias/público abierto de invenciones y datos). 
- **Acceso verificable y preservado:** versiones inmutables, identificadores persistentes (DOI) y archivado independiente.

Límites: ni la publicación ni CC0 garantizan impedir todo intento de patente/registro, ni otorgan libertad de operación (FTO) frente a patentes de terceros, ni controlan precios por sí solos; sí permiten que cualquiera fabrique/use lo divulgado y fortalecen la oposición basada en arte previo.

## 1. Auditoría de conflictos de derechos (obligatoria antes de cada paquete)

| Elemento | Estado | Acción |
|---|---|---|
| Especificaciones, esquemáticos textuales, instrucciones, diseños, código y resultados/figuras generados por el proyecto (`hardware/*`, `candidates/*`, scripts, `outputs/*`, `figures/*`, docs raíz) | Declarados originales/procedencia documentada (`NOTICE`, commits) | Confirmar consentimiento de **todos los titulares** para dedicar a CC0/publicar; mantener procedencia |
| `data/spectra/photochemcad/*` (antes: datos descargados de PhotochemCAD) | **Terceros** — riesgo de redistribución | **Excluidos del repo/paquetes** (se conservan solo referencias y enlaces en `data/spectra/photochemcad/README.md` y `DATA_SEARCH_DOSSIER.md`). No incluir datos de terceros sin derechos claros |
| Licencias actuales (Apache-2.0, CERN-OHL-S v2, CC BY-SA 4.0) | Vigentes hasta transición | Ejecutar checklist de `PUBLIC_DOMAIN_DEDICATION.md` para pasar a CC0 1.0 cuando los titulares lo autoricen |
| Metadatos (`CITATION.cff`, `.zenodo.json`) | Requieren autores/versiones/licencia correctos por release | Actualizar por versión; no marcar CC0 si el paquete incluye material no dedicable |

**Regla:** un paquete es “sin conflictos” solo si contiene obra original propia (o con permiso explícito compatible) y excluye terceros no autorizados.

## 2. Inventario de versiones a publicar (todas las posibles)

| Hito (CHANGELOG) | Commit/tag | GitHub Release / tag a crear | Contenido principal |
|---|---|---|---|
| v0.1.0-preprint | `v0.1.0-preprint` (e84016d) | ya existe | Paquete inicial de simulación voxel |
| v0.3.0-hardware | `v0.3.0-hardware` (ec464aa) | ya existe | OPGPU v0.3 hardware |
| v0.4.0-hardware | `v0.4.0-hardware` (d4040fb) | ya existe | OpenCL, NPU/TPU, esquemas, sim. sistema |
| v0.5.0-hardware | `v0.5.0-hardware` (4f06017) | ya existe | OMCC, RAM óptica compartida |
| v0.5.1-research | ea3f930 | `v0.5.1-research` | Modelado P1 PCM/térmica |
| v0.5.2-research | 0b724aa | `v0.5.2-research` | Integración P1 en sim. sistema |
| v0.5.3-research | b8c3cbb | `v0.5.3-research` | Fiabilidad P2, RAS |
| v0.5.4-research | 800a1ee | `v0.5.4-research` | Variabilidad P3, modo 4b/5b, refresco M2 |
| v0.6.0-mission | 1675866 | `v0.6.0-mission` | Misión/adopción abierta |
| v0.7.0-research | b9753cf | `v0.7.0-research` | Familias/variantes ópticas rápidas |
| v0.7.1-research | 6666153 | `v0.7.1-research` | Eje capacidad en comparación |
| v0.8.0-research | ed4b8fe (y sucesores conflict-free) | `v0.8.0-research` | H1–H5, esquemáticos/instrucciones, PCIe/OpenCL/OpenVINO, manufacturabilidad, roadmap, S1/S3/S4, PD intent |

Publicar además, cuando aporte, **paquetes por estrategia** (H3, G2, G3, H1, H4) como divulgaciones independientes.

## 3. Zenodo — publicación y archivo (DOI por versión + Concept DOI)

**Preparación por versión:**
- Crear tag anotado y GitHub Release para cada hito.
- Ajustar `.zenodo.json`/`CITATION.cff` al snapshot (versión, fecha, autores/titulares, descripción, keywords, `related_identifiers`).
- Licencia: usar la licencia real del snapshot; cambiar a `cc0-1.0` solo tras dedicación efectiva de todo el contenido incluido. Declarar “defensive publication/prior art, conceptual/simulation”.
- Verificar contenido del snapshot: incluir `hardware/*`, `candidates/*`, código, `outputs/*`, `figures/*`, docs; **excluir** terceros no autorizados.

**Publicación:**
- Habilitar repo en Zenodo, generar releases (integración GitHub) o subir snapshots manualmente.
- Obtener **DOI de versión** y **Concept DOI**; citar versiones específicas.
- Registrar DOIs/URLs en `README.md`, `CITATION.cff`/`ARCHIVING.md`.

## 4. ip.com — divulgación defensiva / arte previo

**Objetivo:** disclosures habilitantes, fechadas y buscables como arte previo (visibles en contextos de examen, según servicio).

**Paquetes recomendados:**
- Disclosure **consolidada v0.8** (todas las estrategias A–G, H1–H5, esquemáticos, instrucciones, M0–M3/OMCC, PCIe/OpenCL/OpenVINO, térmica/manufacturable, simulaciones/limitaciones, intención PD).
- Disclosures **por estrategia** (H3, G2, G3, H1, H4) para aislamiento y cobertura específica.
- (Opcional) disclosures por hitos anteriores relevantes.

**Contenido mínimo (enabling):** problema, principio físico, arquitectura y esquemáticos, parámetros/rangos, variantes, instrucciones de implementación/operación conceptual, resultados/limitaciones (simulados), y declaración de uso libre/dominio público + arte previo. Sin material de terceros no autorizado. Validar coste/vouchers, formato, adjuntos e idioma con el proveedor.

## 5. Ejecución (checklist operativa)

- [ ] Confirmar titulares/autores y consentimiento para CC0/publicación.
- [ ] Sanear terceros (PhotochemCAD excluido; revisar resto) y verificar procedencia.
- [ ] Aplicar transición CC0 (textos legales y metadatos) cuando proceda (`PUBLIC_DOMAIN_DEDICATION.md`).
- [ ] Crear tags anotados y releases para v0.5.1–v0.8.0 (+ los ya existentes).
- [ ] Añadir/ajustar `.zenodo.json` y `CITATION.cff` por versión; actualizar `CHANGELOG.md`.
- [ ] Publicar cada versión en Zenodo y registrar DOIs.
- [ ] Preparar y enviar disclosures en ip.com; registrar IDs/fechas.
- [ ] Archivar en Wayback las URLs/DOIs y actualizar `ARCHIVING.md`/README.
- [ ] Mantener avisos: conceptual/simulado, sin garantía, sin FTO, marcas nominativas.

## 6. Registro de publicación (completar al ejecutar)

| Versión/paquete | Fecha | Zenodo DOI (versión) | Concept DOI | ip.com ID/fecha | Wayback | Notas |
|---|---|---|---|---|---|---|
| v0.1.0-preprint |  |  |  |  |  |  |
| v0.3.0-hardware |  |  |  |  |  |  |
| v0.4.0-hardware |  |  |  |  |  |  |
| v0.5.0-hardware |  |  |  |  |  |  |
| v0.5.1-research |  |  |  |  |  |  |
| v0.5.2-research |  |  |  |  |  |  |
| v0.5.3-research |  |  |  |  |  |  |
| v0.5.4-research |  |  |  |  |  |  |
| v0.6.0-mission |  |  |  |  |  |  |
| v0.7.0-research |  |  |  |  |  |  |
| v0.7.1-research |  |  |  |  |  |  |
| v0.8.0-research |  |  |  |  |  |  |
| Estrategia H3 |  |  |  |  |  |  |
| Estrategia G2 |  |  |  |  |  |  |
| Estrategia G3 |  |  |  |  |  |  |
| Estrategia H1 |  |  |  |  |  |  |
| Estrategia H4 |  |  |  |  |  |  |
