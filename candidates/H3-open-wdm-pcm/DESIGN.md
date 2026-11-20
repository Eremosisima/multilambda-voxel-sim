# H3 Open WDM-PCM — Diseño enfocado (conceptual)

## Composición
- **A1 (Interferometric PCM, ref):** mallas MZI/crossbar con pesos en PCM polymérico (diaryleténico/spiropirano, NV; programación óptica/térmica, calibración), control VO₂/Espiropirano; MAC por interferencia coherente y detección balanceada.
- **G1 (Membranas pasivas de espesor fijo):** apilados dieléctricos/FPG (alternativas abiertas: Zeonex/Topas, PMMA/PS); portes selectivos por interferencia por espesor d.
- **B3 (Resonant WDM bank):** anillos/microresonadores para paralelismo espectral donde aporte densidad.

## Principio de operación
1. Pesos persistentes y MVM lineal en A1 ($y = W x$ por interferencia en MZI).
2. G1 multiplexa/selecciona canales $\lambda$ por espesor óptico $n d$ (capas pasivas), aumentando capacidad y paralelismo en volumen reducido sin electrónica de sintonía rápida.
3. B3 complementa con suma/selección resonante WDM; OMCC gestiona direccionamiento, DMA/prefetch y RAS sobre M0–M3.

## Jerarquía de memoria (mapeo)
- L3/RAM NV: M1 PCM polymérico (diaryleténico/spiropirano, pesos/tensores). L2/L1: M2 VO₂ + buffers/rings; L1 retardos M3. Ver `../optical-memory-hierarchy-l1l2l3.md` en monorepo.

## Parámetros de referencia (objetivo conceptual)
- 3.5 TOPS/tile, 160 MB/módulo, 1.6 TB/s, 18 ps inferencia, reconfig PCM 2e-5 s, 4 bits/celda, coste idx 1.4, feas 3/5.

## Interfaces y alternativas sustituibles
- **Malla A1:** sustituible por variantes A2/A3 según FTO/rendimiento.
- **G1 pasivo:** materiales dieléctricos (SiN/SiO₂/TiO₂/HfO₂, etc.) y procesos de depósito estándar; sustituibles por disponibilidad.
- **B3:** rings o filtros alternativos; posible operar con G1+A1 si se simplifica.
- Control: OMCC/protocolo de pulsos documentado; interfaz PCIe/OpenCL (conceptual).

## Plan de validación sugerido
1. TMM de apilados G1 (R/T vs $n,d,\lambda$, tolerancias). 2. Modelo MZI-PCM (P1–P3). 3. Integración de banco WDM y presupuesto de pérdidas. 4. Prototipo de celda pasiva + celda PCM. 5. FTO por bloque antes de fabricar.