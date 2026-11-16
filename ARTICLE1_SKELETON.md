# Borrador de esqueleto — Artículo 1 (teórico + simulaciones)

> **Estado:** borrador generado a partir de simulaciones del repositorio. Los valores numéricos marcados como *asunción de simulación* deben sustituirse por valores citados de literatura o mediciones experimentales antes de envío.

## Título tentativo
**Wavelength-multiplexed optical memory in a single voxel using orthogonal photoswitches and phase readout: theoretical model and simulation**

## Abstract (borrador)
Proponemos una arquitectura de memoria óptica multibit por voxel basada en la superposición lineal de cambios de índice de refracción inducidos por cuatro fotoswitches ortogonales en longitud de onda, con lectura interferométrica por fase. Modelamos el estado del voxel como un vector `c ∈ [0,1]^4` con `Δn_i = c_i Δn_i,max` y `Δn_total = Σ c_i Δn_i,max`, y definimos una matriz de respuesta `A` 4×4 que mapea estados a lecturas de fase, permitiendo decodificación por inversión/calibración. Mediante simulaciones en Python mostramos: (i) 4 niveles discretos por material (8 bits/voxel) con pasos de fase del orden de ~2.6–3.0 rad por nivel bajo supuestos de diseño (L=100 µm, Γ=0.35), (ii) decodificación ideal del 100% de los 256 estados en el régimen lineal sin ruido y análisis de robustez frente a ruido y error de calibración, y (iii) estimaciones de primer orden de crosstalk térmico/óptico que sugieren espaciamiento de capas ≥ ~4 µm en el escenario simulado. Incluimos una discusión de sostenibilidad con escenarios de eficiencia energética para inferencia y una declaración ética de acceso abierto (publicación defensiva).

## 1. Introducción
- Contexto: consumo energético de IA/datacenters y necesidad de computación/memoria más eficiente.
- Motivación: fotónica, no volatilidad de pesos, multiplexado espectral para densidad.
- Contribución: modelo lineal, matriz de lectura, simulación MZI, crosstalk, tabla de compuestos candidata.
- Alcance: trabajo teórico/simulado (sin datos experimentales propios).

## 2. Modelo
### 2.1 Superposición lineal
- `Δn_i = c_i · Δn_i,max`, `c_i ∈ {0, 1/(L-1), ..., 1}` para `L=4` niveles.
- `Δn_total = Σ_i c_i · Δn_i,max` (agregado efectivo) y respuesta por canal de lectura.
- Limitaciones del régimen lineal: saturación, dependencia espectral real de `Δn(λ)`, efectos térmicos.

### 2.2 Matriz de respuesta y decodificación
- Lectura diferencial: `y = A c + e`, con `A_{ji} ≈ (2π/λ_{r,j}) Γ Δn_i,max L` (diagonal dominante) + términos de fuga.
- Inversión: `ĉ = A⁻¹ y`, cuantización al nivel discreto más cercano.
- Calibración experimental propuesta para obtener `A` real.

## 3. Materiales candidatos (simulación)
Usar tabla generada en `outputs/compounds.csv`.

| Material | Escritura (nm) | Borrado (nm) | Lectura (nm) | Δn_max (asim.) | t1/2 térmica (s) |
|---|---:|---:|---:|---:|---:|
| DTE (M1) | 313 | 530 | 1550 | +0.060 | 1e7 |
| Azobenceno (M2) | 365 | 450 | 1310 | -0.050 | 1e5 |
| Espiropirano (M3) | 405 | 590 | 980 | +0.040 | 5e4 |
| DASA (M4) | 660 | 700 | 850 | -0.030 | 2e4 |

*Nota: valores de simulación; reemplazar por datos citados/medidos.*

## 4. Simulación MZI y capacidad
- Parámetros: `L=100 µm`, `Γ=0.35`, 4 canales de lectura.
- Resultado: 8 bits/voxel, `cond(A)=1.196`, 256/256 estados decodificados sin ruido.
- Figuras: `figures/mzi_phase_per_level.png`, matriz `outputs/response_matrix_A.csv`.
- Análisis de ruido: `figures/noise_robustness.png`, `outputs/noise_sweep.csv`.
- Robustez extendida (calibración + ruido): `outputs/robustness_calibration_sweep.csv`.

## 5. Crosstalk térmico y óptico
- Modelo térmico: difusión 1D efectiva, umbral `ΔT=5 K` → distancia mínima ~4.11 µm (escenario).
- Modelo óptico: aislamiento espectral/geométrico fenomenológico.
- Figuras: `figures/thermal_crosstalk.png`, `figures/optical_crosstalk.png`.
- Recomendación de diseño inicial: separación de capas ≥ ~4–5 µm con margen (a validar).

## 6. Discusión de sostenibilidad y eficiencia (escenarios)
- Escenario de referencia y escalamiento por eficiencia (TOPS/W): `outputs/sustainability_scenarios.csv/.json`.
- Argumento cualitativo: no volatilidad de pesos (cero potencia de retención de estado) y mayor densidad por voxel pueden reducir movimiento de datos y número de dispositivos para una misma tarea; cuantificación final requiere prototipo/sistema completo.
- Incluir supuestos explícitos: utilización, PUE, mix de red, overhead de ADC/DAC/control/host, impacto de fabricación.

## 7. Ética, acceso abierto y publicación defensiva (borrador)
> Este trabajo se publica con el objetivo de promover investigación abierta en computación/memoria fotónica eficiente. Los autores prevén liberar el código de simulación, procedimientos y (en etapas posteriores) diseños de hardware bajo licencias abiertas (p. ej. CERN-OHL-S para hardware, Apache 2.0/MIT para software, CC BY para documentación), con versiones orientadas a bajo costo para fines educativos cuando sea técnicamente viable. Este manuscrito se plantea como publicación defensiva para mantener la arquitectura y el método descritos en el dominio público del arte previo, sin intención declarada de exclusión mediante patentes sobre los resultados aquí presentados. Se reportan supuestos y limitaciones para evitar sobreinterpretación de escenarios no medidos.

## 8. Limitaciones y trabajo futuro
- Validación espectral real y ortogonalidad de 4 compuestos.
- Medición de `Δn(λ)`, linealidad, fatiga, velocidad y estabilidad térmica.
- Calibración experimental de `A`, ruido real de fuente/detector, deriva térmica.
- Simulación electromagnética 3D (Meep/Lumerical/COMSOL) y prototipo.
- Modelo energético de sistema completo.

## Disponibilidad
- Código de simulación y salidas: carpeta `articulo1_memoria_fotonica_sim/`.
- Reproducibilidad: ejecutar `py -3 run_simulations.py`.

## Referencias (a completar)
- Irie et al. (diarylethenes, Δn/estabilidad) — completar cita.
- Hecht/Bandara et al. (azobenzenos) — completar cita.
- Klajn et al. (spiropiranos) — completar cita.
- Read de Alaniz et al. / trabajos DASA — completar cita.
- Reportes de consumo de GPUs/datacenters y huella de carbono — completar cita.
- Trabajos de memoria/computación fotónica y MZI weight banks — completar cita.
