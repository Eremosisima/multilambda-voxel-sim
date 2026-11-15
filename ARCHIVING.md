# Archivado y publicación para sostener estado del arte (fecha pública verificable)

Este documento describe pasos prácticos para publicar este proyecto en GitHub y archivarlo (Wayback Machine y otros) como parte de una estrategia de **divulgación abierta y fechada** (publicación defensiva). **No es asesoría legal.**

## 1. Preparar el repositorio local (ya hecho en esta carpeta)
- [ ] Reemplazar metadatos de autor en `CITATION.cff`, `README.md` y manuscritos.
- [ ] Revisar licencias: código (`LICENSE`, Apache-2.0 por defecto aquí) y documentación/datos/figuras (recomendado declarar CC BY 4.0 si aplica; ajustar según tu decisión).
- [ ] Verificar que `run_simulations.py` reproduce `outputs/` y `figures/`.
- [ ] Confirmar que no se incluyen datos privados/credenciales.

## 2. Repositorio en GitHub (público)
- **Repositorio:** https://github.com/Eremosisima/multilambda-voxel-sim
1. Si el repositorio remoto ya existe y está vacío, sube este contenido desde esta carpeta:
   ```powershell
   git remote add origin https://github.com/Eremosisima/multilambda-voxel-sim.git
   git branch -M main
   git push -u origin main
   ```
   (Si `origin` ya existe: `git remote set-url origin https://github.com/Eremosisima/multilambda-voxel-sim.git`.)
2. Crea un **Release** (p. ej. `v0.1.0-preprint`) con notas que indiquen que es simulación/escenario y fecha.
3. Activa en la descripción del repo: tema, licencia, y enlace a preprint/DOI cuando exista.

## 3. Obtener DOI y sello académico (recomendado)
- **Zenodo + GitHub:** conecta tu cuenta de Zenodo con GitHub, habilita el repo y publica un Release para generar un **DOI** por versión (cita persistente y fecha).
- **OSF:** puedes crear un proyecto/registro o alojar preprints/suplementos con DOI y marca temporal.
- Conserva el DOI en `CITATION.cff` y en los manuscritos.

## 4. Archivar en Wayback Machine (Internet Archive)
Con el repositorio público accesible, usa **Save Page Now** (https://web.archive.org/save) o estos enlaces directos de guardado:
- **Repo (principal):** https://web.archive.org/save/https://github.com/Eremosisima/multilambda-voxel-sim
- **README:** https://web.archive.org/save/https://github.com/Eremosisima/multilambda-voxel-sim#readme
- **Árbol de código (main):** https://web.archive.org/save/https://github.com/Eremosisima/multilambda-voxel-sim/tree/main
- **Release v0.1.0-preprint (cuando exista):** https://web.archive.org/save/https://github.com/Eremosisima/multilambda-voxel-sim/releases/tag/v0.1.0-preprint

Tras guardar, Wayback mostrará/registrará una URL archivada con marca de tiempo en el formato:
`https://web.archive.org/web/<YYYYMMDDhhmmss>/https://github.com/Eremosisima/multilambda-voxel-sim`
(el timestamp lo asigna Wayback al momento de la captura).

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
- URL GitHub: https://github.com/Eremosisima/multilambda-voxel-sim
- URL Release vX.Y.Z: 
- DOI Zenodo: 
- URL preprint(s): 
- Capturas Wayback (web.archive.org/web/...): 
- SWHID (si aplica): 
- Fecha pública inicial: 
