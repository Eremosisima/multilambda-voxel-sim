## 1. Límite físico: presupuesto de atenuación (Light Attenuation Budget)
- Pérdida polimérica (0.1–0.5 dB/cm), budget óptico 15 dB → línea máx: 150 cm (mejor, 0.1 dB/cm), 30 cm (peor, 0.5 dB/cm).
- Solución arquitectónica: pases transversales de 10–15 cm → láminas muy largas sin atenuación total. ≤ 30 cm? (25–30 cm promedio).

## 2. Sheet v1: geometría y capacidad
- Footprint: 10 × 100 cm → área 1000 cm² (1,000 cm² esperado).
- Canales paralelos: paso 0 µm → 2000 canales (2,000 esperados).
- Longitud lineal útil por canal: 68.6 cm (100 cm - curvas de pliegues ≈ 31 cm).
- Nodos por canal: 3430 (3,430 esperados) [spacing 200 µm].
- **Total de nodos ópticos por lámina: 6.86 M (≈6.86M esperados)**
- Check: 3430 nodos/canal × 2000 canales = 6.86M ≈ 6.86M (ratio 1.000).

## 3. Regímenes de rendimiento (simulación de TOPS)
- Conservador (1 λ, 100 MHz, 2 ops/nodo): **1,372 TOPS** (esperado ≈1,370) [ratio 1.001].
- Optimizado (16 λ, 1 GHz, 31.9 ops/nodo implícito): **219,000 TOPS** (esperado ≈219,000) [ratio 1.000].
- Cuello de botella real: PCIe 5.0 x16 (800 Gbps) ≈ 100–400 TOPS efectivos (especificación). La lámina procesa >> en el núcleo; el PCIe limita.

## 4. Escalabilidad de láminas en sistema (flujo hidráulico estimado)
- Escritorio (tanque 5 L): 4 láminas en paralelo (área ≈ 0.4 m²). Carga de bomba: 6.0 L/min → dentro de capacidad útil de PC pump.
- Rack 4U: 32 láminas (4 bancos × 8): área = 3.20 m² (≈3.2 m², esperado ≈ 3.2 m² ✓).
- Límite hidráulico: más allá de ~32 láminas, ΔP inter-sheet requiere bombas industriales (2× typical pump); caída de presión (f · L/D · ρ · v²/2, L≈32 cm, D≈0.5 mm, separadores 3 mm).
