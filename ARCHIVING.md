# Archivado y publicación defensiva (todas las versiones, Zenodo + ip.com)

Pasos para publicar y archivar el proyecto de forma **abierta, fechada y verificable** (divulgación defensiva / arte previo) en dominio público (objetivo CC0 1.0) y sin conflictos de derechos. **No es asesoría legal.**

Referencia principal: `PUBLISHING_ALL_VERSIONS_PLAN.md` (inventario, paquetes, checklist y registro de DOIs/IDs).

## 1. Preparación (conflicto-free)
- [ ] Confirmar **titulares/autores** y consentimiento para dedicación CC0/publicación; completar `CITATION.cff` y `.zenodo.json` por versión.
- [ ] Excluir material de terceros no autorizado (p.ej. datos PhotochemCAD ya excluidos; revisar `data/`, figuras, adjuntos).
- [ ] Ejecutar transición CC0 cuando proceda (`PUBLIC_DOMAIN_DEDICATION.md`) o declarar licencia vigente correcta del snapshot.
- [ ] Verificar reproducibilidad (`run_simulations.py`, `simulate_opgpu_system.py`, etc.) y coherencia de esquemáticos/instrucciones (`hardware/`, `candidates/`, `DEFENSIVE_DISCLOSURES/`).

## 2. GitHub: tags y releases (todas las versiones)

Repositorio: https://github.com/Eremosisima/multilambda-voxel-sim (rama `main`).

| Versión | Tag | Commit | Release |
|---|---|---|---|
| v0.1.0-preprint | v0.1.0-preprint | e84016d | crear/publicar |
| v0.3.0-hardware | v0.3.0-hardware | ec464aa | crear/publicar |
| v0.4.0-hardware | v0.4.0-hardware | d4040fb | crear/publicar |
| v0.5.0-hardware | v0.5.0-hardware | 4f06017 | crear/publicar |
| v0.5.1-research | v0.5.1-research | ea3f930 | crear/publicar |
| v0.5.2-research | v0.5.2-research | 0b724aa | crear/publicar |
| v0.5.3-research | v0.5.3-research | b8c3cbb | crear/publicar |
| v0.5.4-research | v0.5.4-research | 800a1ee | crear/publicar |
| v0.6.0-mission | v0.6.0-mission | 1675866 | crear/publicar |
| v0.7.0-research | v0.7.0-research | b9753cf | crear/publicar |
| v0.7.1-research | v0.7.1-research | 6666153 | crear/publicar |
| v0.8.0-research | v0.8.0-research | ed4b8fe | crear/publicar |

Para cada release: notas con alcance, estado (conceptual/simulado), licencia/PD intent, y enlace a esquemáticos/disclosures.

## 3. Zenodo (DOI por versión + Concept DOI)
- Conectar Zenodo con GitHub y habilitar el repositorio.
- Publicar un **Release por cada tag** para archivar todas las versiones (o subir snapshots manualmente).
- Verificar metadatos (`.zenodo.json`/CITATION), licencia del snapshot y exclusión de terceros.
- (Opcional) registros separados por estrategia H3/G2/G3/H1/H4 usando `DEFENSIVE_DISCLOSURES/`.
- Guardar **Concept DOI** y **DOI de cada versión** en la tabla de registro.

## 4. ip.com (divulgación defensiva / arte previo)
- Preparar disclosures habilitantes sin conflictos (ver `DEFENSIVE_DISCLOSURES/`): consolidada v0.8 y por estrategia (H3,G2,G3,H1,H4), y por hitos si se desea.
- Incluir: esquemáticos, parámetros/rangos, variantes, instrucciones, resultados/limitaciones y declaración de dominio público/arte previo.
- Publicar con cuenta/vouchers según servicio y registrar **ID, fecha y comprobante** por disclosure.

## 5. Wayback y preservación adicional
- Archivar (Save Page Now): repo, README, árbol `main`, cada release, y páginas de DOIs/disclosures.
  - https://web.archive.org/save/https://github.com/Eremosisima/multilambda-voxel-sim
- Repetir tras cada publicación relevante. Complementar con **Software Heritage** (SWHID) si aplica.

## 6. Registro de evidencias (rellenar)

Ver tabla completa en `PUBLISHING_ALL_VERSIONS_PLAN.md` §6. Resumen:
- URL GitHub: https://github.com/Eremosisima/multilambda-voxel-sim
- Concept DOI Zenodo: [ ]
- DOIs por versión (v0.1→v0.8): [ ]
- IDs/fechas ip.com (consolidado, H3,G2,G3,H1,H4): [ ]
- Capturas Wayback (web.archive.org/web/...): [ ]
- SWHID: [ ]
- Fecha pública inicial de esta ronda: [ ]
