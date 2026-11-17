# S4 — Coste de redundancia/re-mapeo (área, energía, latencia, capacidad efectiva)

> Modelo conceptual (no mediciones). Cuantifica overhead de optimizaciones S4 (spares, ECC, calibración, re-mapeo OMCC).

## Resumen

| Candidato | Redundancia | ECC | Área total (cm²) | TOPS base→efectivo | Mem base→efectiva (MB) | Retención TOPS | Retención Mem | Overhead energía | Overhead latencia | TOPS/cm² efectivo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| H3 | 0.14 | 0.08 | 45.6 | 3.5→3.01 | 160→137.6 | 0.86 | 0.86 | 1.061 | 1.044 | 0.066 |
| G3 | 0.11 | 0.07 | 35.52 | 5.0→4.45 | 256→227.84 | 0.89 | 0.89 | 1.0515 | 1.041 | 0.1253 |
| H1 | 0.22 | 0.12 | 122.0 | 9.0→7.02 | 640→499.2 | 0.78 | 0.78 | 1.093 | 1.056 | 0.0575 |
| H4 | 0.26 | 0.14 | 113.4 | 10.0→7.399 | 720→532.734 | 0.7399 | 0.7399 | 1.109 | 1.062 | 0.0652 |

## Detalle por candidato

### H3 — Open WDM-PCM (A1+G1+B3)
- Optimización: Partitioned WDM tiles + closed-loop calibration + spare rings (proceso: Baseline process (current assumptions))
- Yield: bruto 1.0, efectivo modelo 0.86, fracción utilizable (con re-mapeo) 1.0, defecto recuperado 0.0
- Área: 40.0 → 45.6 cm² (+14.0% spares)
- Capacidad: TOPS 3.5→3.01 (retención 0.86), Mem 160→137.6 MB (retención 0.86), BW 1.376 TB/s
- Overheads: energía ×1.061, latencia ×1.044 (ECC/control) + calibración ×1.014
- Densidad efectiva: 0.066 TOPS/cm², 3.0175 MB/cm²

### G3 — Thin-film membrane stack (PCM+EO hybrid)
- Optimización: EO trim + PCM write scheduling + improved coupling (proceso: Baseline process (current assumptions))
- Yield: bruto 1.0, efectivo modelo 0.89, fracción utilizable (con re-mapeo) 1.0, defecto recuperado 0.0
- Área: 32.0 → 35.52 cm² (+11.0% spares)
- Capacidad: TOPS 5.0→4.45 (retención 0.89), Mem 256→227.84 MB (retención 0.89), BW 2.492 TB/s
- Overheads: energía ×1.0515, latencia ×1.041 (ECC/control) + calibración ×1.011
- Densidad efectiva: 0.1253 TOPS/cm², 6.4144 MB/cm²

### H1 — Membrane-Brush NV (A1+G3+3D)
- Optimización: Modular 3D partitioning + re-mapping spares + thermal vias/manifold (proceso: Improved process control (metrology/calibrated))
- Yield: bruto 1.0, efectivo modelo 0.78, fracción utilizable (con re-mapeo) 1.0, defecto recuperado 0.0
- Área: 100.0 → 122.0 cm² (+22.0% spares)
- Capacidad: TOPS 9.0→7.02 (retención 0.78), Mem 640→499.2 MB (retención 0.78), BW 2.028 TB/s
- Overheads: energía ×1.093, latencia ×1.056 (ECC/control) + calibración ×1.017
- Densidad efectiva: 0.0575 TOPS/cm², 4.0918 MB/cm²

### H4 — Volumetric Tensor Membrane (G2/G3+F2+A1)
- Optimización: Hierarchical partitioning + alignment/calibration loops + higher redundancy (proceso: Pilot-line stabilized (tight control + thermal management))
- Yield: bruto 0.9997, efectivo modelo 0.7398, fracción utilizable (con re-mapeo) 0.9999, defecto recuperado 0.0002
- Área: 90.0 → 113.4 cm² (+26.0% spares)
- Capacidad: TOPS 10.0→7.399 (retención 0.7399), Mem 720→532.734 MB (retención 0.7399), BW 2.59 TB/s
- Overheads: energía ×1.109, latencia ×1.062 (ECC/control) + calibración ×1.019
- Densidad efectiva: 0.0652 TOPS/cm², 4.6978 MB/cm²

## Conclusiones
- H3/G3 logran alta retención con overhead moderado (10–14% área, energía ×1.06–1.07).
- H1/H4 requieren mayor redundancia (22–26%) para asegurar yield bruto en 3D; retención neta ~73–78% TOPS/mem pero con mejora drástica de usabilidad vs baseline no optimizado.
- Re-mapeo OMCC es clave para convertir spares en capacidad utilizable; el coste real debe medirse en prototipos (área/ruteo, energía ECC, latencia de control).
