# Open Photonic Voxel Memory — Simulaciones (paquete abierto)

Paquete reproducible de **simulaciones teóricas** para una memoria óptica multiplexada por longitud de onda en un único voxel (fotoswitches ortogonales + lectura por fase). Incluye modelo lineal, matriz de respuesta 4x4, análisis MZI, robustez/sensibilidad, presupuesto de SNR, crosstalk térmico/óptico y escenarios de energía/CO2.

> **Estado:** trabajo de simulación/escenario. Los parámetros numéricos son supuestos inspirados en literatura salvo que se citen explícitamente en manuscritos derivados. No representa mediciones de un dispositivo fabricado.

## Contenido principal

- `compounds.py`: tabla de 4 compuestos candidatos y parámetros (lambda escritura/borrado/lectura, delta_n_max, vida media térmica).
- `model.py`: modelo `delta_n_i = c_i * delta_n_i,max`, matriz `A` (lectura por fase) e inversión/decodificación.
- `mzi_sim.py`: delta_phi por nivel, barrido de ruido y distinguibilidad (4 niveles/material, 8 bits/voxel).
- `robustness_extended.py`: robustez frente a error de calibración y ruido.
- `sensitivity.py`: sensibilidad paramétrica (L, Gamma, escala de delta_n, crosstalk, ruido).
- `snr_budget.py`: presupuesto simplificado de ruido de fase (shot + deriva termo-óptica).
- `crosstalk.py`: estimaciones de crosstalk térmico y óptico vs separación de capas.
- `sustainability_energy.py`: escenarios energéticos/CO2 (mismo trabajo útil, supuestos explícitos).
- `run_simulations.py`: ejecuta todo y genera tablas/figuras/reporte.
- `ARTICLE1_SKELETON.md`: borrador de esqueleto del Artículo 1.
- `PUBLICATION_STRATEGY_MULTIJOURNAL.md`: descomposición en artículos independientes (incluye opciones en español).
- `LEGAL_REVIEW_AND_DEFENSIVE_PUBLICATION.md`: guía informativa de publicación defensiva/archivo (no asesoría legal).
- `ARCHIVING.md`: pasos para GitHub, DOI (Zenodo), Wayback Machine y preservación.

## Requisitos y ejecución

- Python 3.10+
- `numpy`, `matplotlib`

```bash
python run_simulations.py
```

## Salidas reproducibles

- `outputs/*.csv`, `outputs/*.json`: parámetros, matriz A, fases, ruido/robustez, sensibilidad, SNR, crosstalk, escenarios de sostenibilidad.
- `outputs/report.md`: resumen consolidado.
- `figures/*.png`: gráficas para manuscritos.

## Publicación abierta y estado del arte

Este repositorio está pensado para facilitar **divulgación fechada y verificable** (preprints, releases con DOI, archivado web). Ver `ARCHIVING.md` y `LEGAL_REVIEW_AND_DEFENSIVE_PUBLICATION.md`. Para una estrategia de múltiples manuscritos independientes (varios en español), ver `PUBLICATION_STRATEGY_MULTIJOURNAL.md`.

## Licencias

- **Código fuente:** Apache License 2.0 (ver `LICENSE`).
- **Documentación, manuscritos en borrador, figuras y datos generados:** salvo indicación en contrario, se recomienda publicarlos bajo **CC BY 4.0** para maximizar reutilización con atribución. Ajusta y declara la licencia final antes del release público según tu elección y políticas de las revistas/repositorios.

## Aviso

Las simulaciones y escenarios no deben interpretarse como promesas de desempeño medido ni como asesoría legal/de propiedad intelectual. Cita fuentes primarias para parámetros de materiales y consumo energético cuando prepares envíos a revistas.
