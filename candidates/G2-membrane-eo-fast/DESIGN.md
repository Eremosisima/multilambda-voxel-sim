# G2 Thin-film Membrane Stack (EO-tuned) — Diseño enfocado

## Principio
Membranas/cavidades F–P apiladas con espesor óptico $n d$ sintonizable por índice electro-óptico: $\delta \approx \frac{4\pi n(E) d \cos\theta}{\lambda} + \phi_r$. La conmutación/ponderación se realiza por condiciones de **interferencia constructiva/destructiva** por capa y longitud de onda (WDM vertical).

## Composición
- Multicapa dieléctrica (p. ej. SiN/SiO₂/TiO₂) + material/estructura EO (TFLN/BTO u otras plataformas) para control de $n$.
- Integración en cerdas/cores del arreglo 3D (cepillo) para alta densidad por mm³.
- Acoplo a guías/buses WDM y detección diferencial/balanceada cuando aplique.

## Parámetros de referencia
- 5.5 TOPS/tile, 192 MB, 3.2 TB/s, 3 ps inferencia, 1e-11 s reconfig, 2 bits/celda efectivos, coste idx 1.85, feas 2/5.

## Rol en jerarquía
- L1/L2: buffers/cómputo rápido por retención resonante y sintonía EO. L3: capacidad NV limitada → combinar con M1 PCM (A1/H3) para pesos estacionarios.

## Interfaces sustituibles
- Plataforma EO sustituible (TFLN, BTO, polímeros EO, etc.) según disponibilidad/FTO. Materiales dieléctricos estándar para apilado pasivo base. Interfaz de control/calibración OMCC documentada.

## Validación sugerida
1. TMM de multicapas (R/T, IL, tolerancias ±nm, sensibilidad térmica/angular). 2. Modelo Δn(E) y velocidad/energía. 3. Presupuesto de enlace WDM y densidad MB/TOPS por cm³. 4. Prototipo de cavidad sintonizable.