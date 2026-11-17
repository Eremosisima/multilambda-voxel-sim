# IP, dominio público y Open Hardware — H3 Open WDM-PCM

## Licenciamiento y dominio público
- **Objetivo:** dedicar esta estrategia/diseño/documentación al **dominio público (CC0 1.0)** para **uso libre universal** y publicarla como **arte previo/divulgación defensiva** para dificultar apropiación registral por terceros (sin garantía absoluta). Ver `../../PUBLIC_DOMAIN_DEDICATION.md`.
- **Licencias vigentes (esta versión, hasta transición por titulares):** Hardware/diseños CERN-OHL-S v2 (`LICENSE-HARDWARE`), Código Apache-2.0 (`LICENSE`), Documentación CC BY-SA 4.0 (`LICENSE-docs`). Ver `NOTICE`.

## Objetivo de apertura
H3 se prioriza por apoyarse en **principios físicos conocidos** (interferencia de película delgada/F–P, MZI, WDM) y **elementos pasivos dieléctricos** de procesos estándar, facilitando implementación abierta y competencia.

## Copyright (expresión)
- No copiar texto, figuras, máscaras/layouts, código o datasheets de terceros sin licencia compatible. Citar fuentes externas; mantener procedencia en commits y notas.

## Patentes / FTO (no cubierto por licencias)
- El licenciamiento abierto **no otorga libertad de operación** frente a patentes vigentes. Se recomienda FTO por jurisdicción y revisión por especialista en PI antes de fabricar/comercializar.
- H3 evita en gran medida sintonía EO/RF activa (sensible en FTO) al usar G1 pasivo, pero **A1/B3** y procesos específicos pueden estar sujetos a patentes: diseñar con geometrías/materiales genéricos, documentar alternativas y sustituibilidad.
- Publicación defensiva: especificaciones habilitantes, parámetros y variantes con fecha verificable (commits/releases/DOI).

## Modularidad ante C&D
Si un bloque (p. ej. una implementación concreta de resonador o proceso) es impugnado, sustituirlo por alternativa documentada o retirar solo el material afectado en este repo, manteniendo el resto del ecosistema/candidatos activo. No realizar afirmaciones de “libre de patentes”.