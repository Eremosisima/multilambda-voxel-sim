# Estrategia de repositorios por candidato (modularización y aislamiento de riesgo)

> Propósito: dar **atención prioritaria** a los candidatos mejor posicionados y, cuando sea conveniente, mantener **un repositorio independiente por candidato**. Así, si un proyecto enfrenta un requerimiento de cese y desista (C&D) u otro bloqueo, **solo ese repositorio/candidato se retira o pausa** y los demás continúan activos.  
> **Aviso:** organización técnica/estratégica general, **no asesoría legal**. Consultar con especialista en PI para acciones ante C&D, FTO y jurisdicciones aplicables.

## 1. Candidatos priorizados (atención especial)

Selección basada en el reanálisis objetivo (`outputs/objective_combo_analysis.md`, 19 variantes, escenarios + sensibilidad ±30%):

| Prioridad | Candidato | Directorio local (repo independiente) | Justificación objetiva (resumen) | Perfil de riesgo/aislamiento |
|---|---|---|---|---|
| **P1 – Abierto/factible (corto plazo)** | **H3 Open WDM-PCM (A1+G1+B3)** | `candidates/H3-open-wdm-pcm/` | Mejor acceso abierto/factibilidad-precio (obj_open_access 0.906, feas 0.6, $3.6k, NV, balanced 3.47). Pasivos dieléctricos + ref A1: menor dependencia de bloques EO/RF sensibles. | **Más conveniente separar/avanzar primero**: superficie FTO típicamente menor (principios/pasivos conocidos) y alto valor de continuidad. |
| **P1 – Líder overall/velocidad-capacidad** | **G2 Thin-film membrane stack (EO-tuned)** | `candidates/G2-membrane-eo-fast/` | Top overall (0.712), robusto P(top5)=0.985, alta velocidad/BW y densidad (balanced 5.42, 0.183 TOPS/cm³, 6.4 MB/cm³). | Depende de sintonía EO/plataformas (p. ej. TFLN/BTO) → **aislar** por posible sensibilidad FTO en EO. |
| **P1 – Equilibrio NV/velocidad** | **G3 Thin-film membrane stack (PCM+EO hybrid)** | `candidates/G3-membrane-pcm-eo/` | Overall 0.676, P(top5)=0.915, buena capacidad NV y densidad (8.0 MB/cm³, balanced 5.25). | Combina PCM+EO; modularidad permite sustituir bloque EO/PCM → separar. |
| **P1 – Escalado volumétrico NV** | **H1 Membrane-Brush NV (A1+G3+3D)** | `candidates/H1-membrane-brush-nv/` | Overall 0.679, P(top5)=0.93, alta capacidad volumétrica NV (640 MB, balanced 8.17, Pareto capacidad/precio-rend). | Complejidad 3D e integración → separar por riesgo técnico y de implementación. |
| **P1 – Techo de capacidad** | **H4 Volumetric Tensor Membrane** | `candidates/H4-volumetric-tensor-membrane/` | Máxima capacidad/throughput (10 TOPS, 720 MB, balanced 9.49, Pareto capacidad) pero coste/factibilidad bajos. | Alto riesgo técnico/FTO por bloques (EO/difractivo) → **aislar**; continuidad independiente del resto. |

> Referencias: G2/G3/H1/H4 resultan robustos (P(top5)≥0.905) en sensibilidad ±30%; H3 lidera acceso abierto/factibilidad. H2 (RT Membrane-WDM) queda como candidato de alto rendimiento dependiente de control térmico/fase y NV externa (puede separarse en una fase siguiente si se decide profundizar).

## 2. Principios de separación (para que un C&D no afecte a los demás)

- **Independencia de repositorio y historial:** cada candidato en su propio repo Git (nombre, README, issues, releases y trail de publicación/DOI independientes).
- **Documentación y diseño autocontenidos:** cada repo incluye solo la especificación, parámetros, scripts y datos relevantes a ese candidato (evitar acoplamiento innecesario).
- **Licencias completas por repo:** incluir `LICENSE` (Apache-2.0, código), `LICENSE-HARDWARE` (CERN-OHL-S v2), `LICENSE-docs` (CC BY-SA 4.0), `NOTICE` y nota de autoría/procedencia.
- **Modularidad de bloques sensibles:** declarar interfaces y alternativas sustituibles (p. ej. modulador EO, resonador, capa ENZ/difractiva, material de membrana) para poder retirar/sustituir un bloque sin tumbar el resto del ecosistema.
- **Publicación defensiva y procedencia:** mantener descripciones habilitantes, supuestos y fechas/commits propios; no copiar material de terceros.
- **Sin admisiones ni afirmaciones absolutas:** no declarar “libre de patentes”; documentar estado conceptual y recomendar FTO antes de fabricar/comercializar.
- **Procedimiento ante posible C&D:** pausar/retirar/ajustar **solo** el repo afectado (o el bloque identificado), preservando evidencia de procedencia y notificando la separación; los demás repos permanecen publicados según su propio estado.

## 3. Contenido mínimo de cada repo candidato

- `README.md` (alcance, métricas objetivas, fortalezas/riesgos, estado conceptual, cómo contribuir/usar).
- `DESIGN.md` (diseño enfocado, composición de familias/bloques, interfaces y alternativas sustituibles).
- `IP_AND_OPEN_HW.md` (licencias, copyright vs patentes/FTO, ruta open y notas de modularidad ante retiro de bloques).
- Licencias/`NOTICE`/autoría, `data/` o extractos de métricas, y (cuando aplique) scripts/modelos específicos del candidato.
- Historial Git propio y versionado independiente.

## 4. Publicación (pasos sugeridos por candidato)

Para cada carpeta en `candidates/<nombre>/`:
1. Revisar/ajustar contenido y confirmar procedencia.
2. Crear un repositorio vacío en la forja elegida (p. ej. GitHub) con nombre específico del candidato.
3. `git init` (si no existe), `git add -A`, commit inicial, añadir remoto y `git push`.
4. (Opcional) archivar release/DOI independiente para publicación defensiva.

> Este directorio `candidates/` en el monorepo sirve como *staging* local; cada subdirectorio está pensado para publicarse como repositorio autónomo.

## 5. Estado

- Estructura local creada para: **H3, G2, G3, H1, H4** (atención prioritaria). Ver `candidates/README.md`.
- El monorepo principal sigue siendo la referencia integrada y comparativa (`outputs/`, `hardware/`, simulaciones). La separación no elimina contenido del monorepo; habilita continuidad independiente por candidato.