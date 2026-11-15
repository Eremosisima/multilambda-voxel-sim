# Archivado y publicación para sostener estado del arte (fecha pública verificable)

Este documento describe pasos prácticos para publicar este proyecto en GitHub y archivarlo (Wayback Machine y otros) como parte de una estrategia de **divulgación abierta y fechada** (publicación defensiva). **No es asesoría legal.**

## 1. Preparar el repositorio local (ya hecho en esta carpeta)
- [ ] Reemplazar metadatos de autor en `CITATION.cff`, `README.md` y manuscritos.
- [ ] Revisar licencias: código (`LICENSE`, Apache-2.0 por defecto aquí) y documentación/datos/figuras (recomendado declarar CC BY 4.0 si aplica; ajustar según tu decisión).
- [ ] Verificar que `run_simulations.py` reproduce `outputs/` y `figures/`.
- [ ] Confirmar que no se incluyen datos privados/credenciales.

## 2. Crear repositorio en GitHub (público)
1. En GitHub: **New repository** (público). Nombre sugerido: `open-photonic-voxel-sim` (o el que prefieras). No inicializar con README si vas a subir este contenido.
2. En tu máquina, desde esta carpeta:
   ```powershell
   git init
   git add .
   git commit -m "Initial public simulation package: model, MZI, crosstalk, sensitivity, SNR, energy scenarios, drafts"
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/<tu-repo>.git
   git push -u origin main
   ```
3. Crea un **Release** (p. ej. `v0.1.0-preprint`) con notas que indiquen que es simulación/escenario y fecha.
4. Activa en la descripción del repo: tema, licencia, y enlace a preprint/DOI cuando exista.

## 3. Obtener DOI y sello académico (recomendado)
- **Zenodo + GitHub:** conecta tu cuenta de Zenodo con GitHub, habilita el repo y publica un Release para generar un **DOI** por versión (cita persistente y fecha).
- **OSF:** puedes crear un proyecto/registro o alojar preprints/suplementos con DOI y marca temporal.
- Conserva el DOI en `CITATION.cff` y en los manuscritos.

## 4. Archivar en Wayback Machine (Internet Archive)
- **Snapshot manual:** visita https://web.archive.org/save e ingresa la URL pública del repositorio GitHub, la página del release y (si aplica) la página del DOI/preprint.
- **Verificación:** guarda los enlaces `web.archive.org/web/...` como evidencia de captura.
- Repite snapshots cuando publiques versiones importantes (nuevos releases, preprints, correcciones).
- Nota: Wayback archiva páginas web públicas; para preservar **código y datasets** de forma robusta complementa con Zenodo/Software Heritage.

## 5. Otros archivos de preservación (opcional pero útil)
- **Software Heritage:** puede archivar repositorios públicos de código fuente (https://archive.softwareheritage.org/). Solicita/activa el archivado del repo y conserva el identificador SWHID si se genera.
- **Repositorios institucionales:** si tienes afiliación, deposita una copia con metadatos y fecha.
- **archive.today / perma.cc:** capturas adicionales de páginas clave (no reemplazan DOI/archivo de código).

## 6. Buenas prácticas para "estado del arte"
- Publica una descripción **habilitante** (modelo, ecuaciones, parámetros, supuestos, limitaciones, variantes) — no solo marketing.
- Etiqueta claramente: *simulación/escenario* vs *medición experimental*.
- Mantén historial de versiones (tags/releases) y changelog.
- Si derivas artículos (A–E de `PUBLICATION_STRATEGY_MULTIJOURNAL.md`), enlaza cada preprint/publicación al release/DOI correspondiente.

## 7. Registro de evidencias (rellenar)
- URL GitHub: 
- URL Release vX.Y.Z: 
- DOI Zenodo: 
- URL preprint(s): 
- Capturas Wayback: 
- SWHID (si aplica): 
- Fecha pública inicial: 
