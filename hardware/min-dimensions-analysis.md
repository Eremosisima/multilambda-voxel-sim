# Dimensiones teóricas mínimas por propuesta (con handicap por fallos)

> Estimaciones conceptuales de primer orden (no listas para fabricación). Consideran confinamiento óptico, interacción luz-compuesto y márgenes por fallos/tolerancias.  
> **Dominio público (objetivo declarado):** uso libre para todo el mundo; publicado como **arte previo/divulgación defensiva** (ver `../PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta).

## Supuestos clave
- Señal: λ=1550.0 nm (NIR). Controles: 365/450/520/650/800 nm.
- Índices: Sb2S3 2.70/3.30, VO2 2.50/2.00, azo 1.56/1.54, espiropirano 1.54/1.60, SiN 2.00, SiO2 1.45, TiO2 2.45, TFLN 2.20.
- Térmica (P1): escritura Sb2S3 ~300°C vs umbral VO2 68°C → pitch lateral seguro ~10.0 µm, separación axial ~8.0 µm.
- Handicap por fallos (multiplicativo): {'yield_guardband': 1.2, 'alignment_margin': 1.15, 'redundancy_spares': 1.15, 'thermal_crosstalk_guard': 1.1, 'optical_crosstalk_guard': 1.1, 'ecc_overhead': 1.05}.

## Tabla comparativa

| Propuesta | Composición | Feature mín (nm) | Pitch lat mín (µm) | Long. activa mín (µm) | Capa mín (nm) | Pitch vert mín (µm) | Área celda (µm²) | Vol celda (µm³) | Handicap | Área efect. (µm²) | Vol efect. (µm³) | Limitantes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A1 | MZI + Sb2S3/VO2/azo/spiro (SiN) | 387.5 | 17.53 | 10.0 | 193.8 | 10.0 | 140.0 | 1400.0 | 1.753 | 245.46 | 2454.606 | Thermal crosstalk (300C Sb2S3 vs 68C VO2), MZI arm length for 2pi, waveguide coupling |
| B3 | SiPh/SiN microrings + tuning | 322.9 | 19.0 | 22.0 | 193.8 | 3.0 | 418.0 | 1254.0 | 1.594 | 666.25 | 1998.751 | Bend loss/radius, resonator-to-bus coupling gap, thermal sensitivity of resonance |
| G1 | Dielectric multilayer (SiN/SiO2/TiO2), fixed d | 316.3 | 2.0 | 2.0 | 193.8 | 3.688 | 4.0 | 14.7517 | 1.833 | 7.33 | 27.0397 | Layer thickness tolerance (nm-scale), interface loss/roughness, lateral coupling/alignment |
| G2 | Multilayer dielectric + EO (e.g. TFLN/BTO) | 352.3 | 3.0 | 3.0 | 176.1 | 4.688 | 9.0 | 42.1914 | 1.833 | 16.5 | 77.3362 | EO overlap and electrode spacing, nm thickness control, thermal drift of resonance, optical loss |
| G3 | Multilayer + Sb2S3 PCM + EO tuning | 287.0 | 3.0 | 3.0 | 143.5 | 4.188 | 9.0 | 37.6914 | 2.016 | 18.15 | 75.9965 | PCM crystallization volume/thermal isolation, EO electrode spacing, multilayer tolerance |
| H3 | MZI-PCM + passive membranes + microrings (modular) | 387.5 | 10.0 | 24.0 | 193.8 | 7.688 | 240.0 | 1845.103 | 2.016 | 483.91 | 3720.252 | PCM thermal isolation, ring bend/coupling, multilayer alignment, cumulative loss budget |
| H1 | MZI-PCM + PCM/EO membranes in 3D bristle | 387.5 | 10.0 | 60.0 | 143.5 | 65.503 | 100.0 | 6550.345 | 2.016 | 201.63 | 13207.352 | 3D alignment, vertical thermal isolation between 300C segments, interlayer coupling, yield compounding in 3D |
| H4 | Membrane cores 3D + diffractive/meta + PCM NV | 352.3 | 8.0 | 40.0 | 176.1 | 66.879 | 64.0 | 4280.276 | 2.117 | 135.49 | 9061.762 | Diffractive alignment and phase uniformity, multi-layer registration, compounded 3D yield, thermal management |

## Comportamiento luz-compuesto (resumen por propuesta)

### A1 — Interferometric PCM (Ref)
- **Interacción:** Sb2S3 dn=0.6 (amorph/cryst) gives phase shift but needs thermal isolation; VO2 fast volatile switch low threshold; azo/spiro small dn for trim/config; SiN low loss NIR
- **Supuestos:** lambda_s=1550nm, Gamma=0.35, P1 thermal pitch>=10um (safe), axial sep 8um, passive margins for splitters
- **Handicap efectivo:** ×1.753 → área 245.46 µm², volumen 2454.606 µm³ por celda/elemento mínimo.

### B3 — Resonant WDM bank (microrings)
- **Interacción:** High-Q resonance concentrates field (strong lambda selectivity) but narrow linewidth increases sensitivity to dn, temperature and fabrication; WDM multiplies capacity per bus
- **Supuestos:** R_min~8um (conservative SiPh), coupling gaps ~200-300nm feasible but guarded, vertical stack modest
- **Handicap efectivo:** ×1.594 → área 666.25 µm², volumen 1998.751 µm³ por celda/elemento mínimo.

### G1 — Thin-film membrane stack (passive WDM)
- **Interacción:** Interference constructive/destructive set by n*d: quarter-wave layers give strong spectral selectivity; SiN/SiO2/TiO2 low loss in NIR, no thermal switching crosstalk
- **Supuestos:** ~16 alternating layers, t_qw(SiN)~194nm t_qw(SiO2)~267nm, lateral pixel >=2um
- **Handicap efectivo:** ×1.833 → área 7.33 µm², volumen 27.0397 µm³ por celda/elemento mínimo.

### G2 — Thin-film membrane/F-P stack (EO-tuned)
- **Interacción:** EO (Pockels) shifts n -> shifts resonance/phase condition fast without moving mass; dielectric stack provides high density WDM; heating from drivers managed by spacing
- **Supuestos:** Adds EO layer and field margins over G1; fast reconfig but more interfaces
- **Handicap efectivo:** ×1.833 → área 16.5 µm², volumen 77.3362 µm³ por celda/elemento mínimo.

### G3 — Thin-film membrane stack (PCM+EO hybrid)
- **Interacción:** Sb2S3 provides large dn NV state (n*d step) for persistent spectral weight; EO gives fast fine trim; thermal 300C write requires local confinement/guarding even in thin layers
- **Supuestos:** Hybrid NV+fast; PCM thermal guard increases effective spacing vs G1/G2
- **Handicap efectivo:** ×2.016 → área 18.15 µm², volumen 75.9965 µm³ por celda/elemento mínimo.

### H3 — Open WDM-PCM (A1+G1+B3)
- **Interacción:** Combines A1 large dn NV weights, G1 passive n*d spectral selectivity (no tuning loss), B3 resonant WDM; mostly standard dielectrics + established PIC elements
- **Supuestos:** Modular tile; lateral set by thermal-safe PCM pitch and ring routing; vertical by passive stack + PIC layers
- **Handicap efectivo:** ×2.016 → área 483.91 µm², volumen 3720.252 µm³ por celda/elemento mínimo.

### H1 — Membrane-Brush NV (A1+G3+3D)
- **Interacción:** 3D stacking multiplies capacity/volume: PCM NV states per voxel + membrane n*d spectral channels; light guided/reflected (45°) along bristle; thermal isolation critical axially/laterally
- **Supuestos:** Footprint per bristle set by thermal pitch; height by voxel count*segment separation; 3D yield/alignment handicap applied
- **Handicap efectivo:** ×2.016 → área 201.63 µm², volumen 13207.352 µm³ por celda/elemento mínimo.

### H4 — Volumetric Tensor Membrane (G2/G3+F2+A1)
- **Interacción:** EO-tuned and PCM-assisted n*d membranes for local tensor ops + diffractive/global interference mixing; highest functional density but tight phase/alignment tolerances
- **Supuestos:** Aggressive stacking and diffractive sections; highest handicap due to compounded tolerances/yield in complex 3D
- **Handicap efectivo:** ×2.117 → área 135.49 µm², volumen 9061.762 µm³ por celda/elemento mínimo.

## Notas
- *Mínimo teórico* ≠ mínimo fabricable: litografía, rugosidad, pérdidas, uniformidad y rendimiento fijan límites mayores según proceso.
- Donde domina la térmica (PCM 300°C cerca de VO₂ 68°C), el pitch no baja de ~6–10 µm sin aislamiento avanzado (consistente con P1).
- En membranas G1/G2/G3, el espesor por capa puede ser sub-µm (λ/4n), pero el volumen efectivo crece por apilado, alineación y redundancia.
- Las propuestas 3D (H1/H4) reducen huella por función al apilar, pero el handicap aumenta por yield/alineación compuesta.
