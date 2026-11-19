# Checklist de envío (ip.com y Zenodo) — listo para ejecutar

Fecha preparación: 2026-11-17 · Actualización: 2026-11-19 (commit `5c4a1f8`, main) · Versión base disclosures: v0.8.0-research (tag `v0.8.0-research`)

## Estado
- [x] Esquemáticos e instrucciones completos y enlazados (`hardware/current-strategies-schematics-and-instructions.md`, `hardware/schematics-deep-dive.md`, `hardware/pcie-bridge-opencl-openvino.md`, candidatos).
- [x] Todas las estrategias A–G y H1–H5 documentadas; priorizadas H3,G2,G3,H1,H4 con divulgaciones individuales.
- [x] Borradores habilitantes listos (autores/IDs de referencia pre-rellenados, revisión final pendiente): `DISCLOSURE_CONSOLIDADA_v0.8.md`, `DISCLOSURE_H3_Open_WDM-PCM.md`, `DISCLOSURE_G2_Membrane_EO_Fast.md`, `DISCLOSURE_G3_Membrane_PCM_EO.md`, `DISCLOSURE_H1_Membrane_Brush_NV.md`, `DISCLOSURE_H4_Volumetric_Tensor_Membrane.md`.
- [x] Conflictos de terceros saneados en paquetes (PhotochemCAD excluido; referencias externas).
- [x] Todas las versiones tageadas y releases publicados: https://github.com/Eremosisima/multilambda-voxel-sim/releases
- [~] Zenodo: Concept DOI `10.5281/zenodo.24323250`; DOI versión publicado: `10.5281/zenodo.24374387` (v0.3.0-hardware, 2026-11-19, con disclaimer). **Pendiente:** confirmar ingesta/DOIs del resto de versiones (v0.1→v0.8) y registrar en `PUBLISHING_ALL_VERSIONS_PLAN.md`/`ARCHIVING.md`.
- [~] Autores/titulares pre-rellenados en disclosures: `eremosisima; Contreras, Francisco Javier`. **Pendiente:** confirmar afiliación/ORCID y **consentimiento explícito de dedicación CC0/dominio público** por todos los titulares.
- [ ] Enviar a ip.com y registrar IDs/fechas/comprobantes.
- [ ] Archivar URLs/DOIs en Wayback.

## ip.com (divulgación defensiva, por estrategia + consolidada)
Para cada envío: pegar el contenido del archivo de divulgación, adjuntar/referenciar esquemáticos e instrucciones del repo/release, declarar **dominio público (CC0, intención) + arte previo**, y confirmar que no incluye material de terceros no autorizado.
1. **Consolidada v0.8:** `DISCLOSURE_CONSOLIDADA_v0.8.md` (todas las estrategias y esquemáticos).
2. **H3:** `DISCLOSURE_H3_Open_WDM-PCM.md`
3. **G2:** `DISCLOSURE_G2_Membrane_EO_Fast.md`
4. **G3:** `DISCLOSURE_G3_Membrane_PCM_EO.md`
5. **H1:** `DISCLOSURE_H1_Membrane_Brush_NV.md`
6. **H4:** `DISCLOSURE_H4_Volumetric_Tensor_Membrane.md`

Registrar aquí (completar tras envío):

| Paquete | ID ip.com | Fecha | Evidencia/URL |
|---|---|---|---|
| Consolidada v0.8 | [ ] | [ ] | [ ] |
| H3 (Open WDM-PCM) | [ ] | [ ] | [ ] |
| G2 (Membrane EO Fast) | [ ] | [ ] | [ ] |
| G3 (Membrane PCM+EO) | [ ] | [ ] | [ ] |
| H1 (Membrane Brush NV) | [ ] | [ ] | [ ] |
| H4 (Volumetric Tensor Membrane) | [ ] | [ ] | [ ] |

## Zenodo
- Releases creados (v0.1→v0.8): verificar ingesta automática. Si falta alguno, subir snapshot del tag.
- Conocidos: Concept DOI `10.5281/zenodo.24323250`; DOI versión `10.5281/zenodo.24374387` (v0.3.0-hardware, 2026-11-19, incluye `DISCLAIMER_PUBLIC_DOMAIN_ZENODO.md`, autores eremosisima y Francisco Javier Contreras).
- Metadatos: `CITATION.cff`, `.zenodo.json`. Licencia: estado vigente; cambiar a `cc0-1.0` tras dedicación efectiva por titulares.
- Registrar Concept DOI y DOIs por versión en `PUBLISHING_ALL_VERSIONS_PLAN.md` y `ARCHIVING.md`.

## Dominio público (ejecución legal, no demorable)
- Obtener consentimiento de titulares y aplicar checklist `PUBLIC_DOMAIN_DEDICATION.md` (texto CC0, actualizar LICENSE*/NOTICE/metadatos/repo). Publicar release de dedicación.
