#!/usr/bin/env python3
"""
Theoretical minimum dimensions per proposal, considering light-compound behavior
and a failure handicap (yield/redundancy/tolerance/thermal-crosstalk margins).

Conceptual, first-order estimates (not fabrication-ready). Outputs in outputs/.
"""
from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import List, Dict

OUT_DIR = "outputs"

# --- Optical/material assumptions (project references) ---
LAMBDA_SIGNAL_NM = 1550.0  # NIR signal (conceptual)
LAMBDA_CONTROLS_NM = {"sb2s3": 650.0, "vo2": 800.0, "azo_trans": 365.0, "azo_cis": 450.0, "spiro_closed": 365.0, "spiro_open": 520.0}

# Refractive indices (project specs / typical thin-film dielectrics)
N = {
    "sb2s3_a": 2.70, "sb2s3_c": 3.30,
    "vo2_i": 2.50, "vo2_m": 2.00,
    "azo_trans": 1.56, "azo_cis": 1.54,
    "spiro_closed": 1.54, "spiro_open": 1.60,
    "SiN": 2.00, "SiO2": 1.45, "TiO2": 2.45, "TFLN": 2.20,
}

# Thermal thresholds (C) and P1-derived spacing guidance
T_PCM_WRITE_C = 300.0
T_VO2_THRESHOLD_C = 68.0
PITCH_THERMAL_SAFE_UM = 10.0   # P1 nominal with margin
PITCH_THERMAL_MIN_UM = 6.0     # P1 sweep lower bound (reduced margin)
ZSEP_AXIAL_UM = 8.0

# Failure handicap factors (multipliers/overheads, conceptual)
HANDICAP = {
    "yield_guardband": 1.20,        # linewidth/pitch margin for fabrication tolerance
    "alignment_margin": 1.15,       # 3D/layer alignment overhead
    "redundancy_spares": 1.15,      # spare cells/rows/blocks for defects
    "thermal_crosstalk_guard": 1.10,# extra spacing when hot materials co-located
    "optical_crosstalk_guard": 1.10,
    "ecc_overhead": 1.05,           # logical overhead for reliability
}

def nm_to_um(x): return x / 1000.0

def quarter_wave_um(lambda_nm, n):
    return nm_to_um(lambda_nm / (4.0 * n))

def confinement_limit_um(lambda_nm, n_eff):
    # diffraction/mode confinement scale ~ lambda/(2*n_eff)
    return nm_to_um(lambda_nm / (2.0 * n_eff))

def mzi_active_length_um(lambda_nm, gamma_dn_eff, phase_rad=2*math.pi):
    # L = phase * lambda / (2*pi*dn_eff)
    dn = max(gamma_dn_eff, 1e-6)
    return nm_to_um(phase_rad * lambda_nm / (2.0 * math.pi * dn))

def combined_handicap(*keys):
    h = 1.0
    for k in keys:
        h *= HANDICAP[k]
    return h

@dataclass
class ProposalDims:
    key: str
    name: str
    composition: str
    signal_lambda_nm: float
    min_feature_nm: float
    min_lateral_pitch_um: float
    min_active_length_um: float
    min_layer_thickness_nm: float
    min_vertical_pitch_um: float
    min_cell_area_um2: float
    min_cell_volume_um3: float
    failure_handicap_factor: float
    effective_min_cell_area_um2: float
    effective_min_cell_volume_um3: float
    limiting_factors: str
    material_light_behavior: str
    assumptions: str

def proposals() -> List[ProposalDims]:
    lam = LAMBDA_SIGNAL_NM
    out = []

    # --- A1: Interferometric PCM (MZI + Sb2S3/VO2) ---
    # dn_eff ~ Gamma*(nc-na)=0.35*0.6=0.21, L_2pi ~ 3.7um; P1 used 10um cell
    dn_a1 = 0.35 * (N["sb2s3_c"] - N["sb2s3_a"])  # 0.21
    l_mzi = max(mzi_active_length_um(lam, dn_a1), 10.0)  # P1 baseline 10um
    feat_a1 = confinement_limit_um(lam, N["SiN"]) * 1000  # nm, ~387nm
    # thermal dominates: PCM 300C near VO2 68C -> use P1 safe pitch
    pitch_lat = PITCH_THERMAL_SAFE_UM
    vert = ZSEP_AXIAL_UM + 2.0  # axial separation + layer
    h_a1 = combined_handicap("yield_guardband","redundancy_spares","thermal_crosstalk_guard","optical_crosstalk_guard","ecc_overhead")
    area = pitch_lat * (l_mzi + 4.0)  # include splitters/margins
    vol = area * vert
    out.append(ProposalDims(
        "A1","Interferometric PCM (Ref)","MZI + Sb2S3/VO2/azo/spiro (SiN)",
        lam, round(feat_a1,1), round(pitch_lat*h_a1,2), round(l_mzi,2),
        round(quarter_wave_um(lam,N["SiN"])*1000,1), round(vert,2),
        round(area,2), round(vol,3), round(h_a1,3),
        round(area*h_a1,2), round(vol*h_a1,3),
        "Thermal crosstalk (300C Sb2S3 vs 68C VO2), MZI arm length for 2pi, waveguide coupling",
        "Sb2S3 dn=0.6 (amorph/cryst) gives phase shift but needs thermal isolation; VO2 fast volatile switch low threshold; azo/spiro small dn for trim/config; SiN low loss NIR",
        "lambda_s=1550nm, Gamma=0.35, P1 thermal pitch>=10um (safe), axial sep 8um, passive margins for splitters"
    ))

    # --- B3: Resonant WDM bank (microrings) ---
    # bend-limited radius: SiN ring R~10-15um practical, Si ~5um; use SiPh-like 8um
    R_ring = 8.0
    pitch_b = 2*R_ring + 3.0  # ring + bus gaps
    l_b = 2*R_ring + 6.0
    feat_b = confinement_limit_um(lam, 2.4) * 1000  # high contrast ~323nm
    h_b = combined_handicap("yield_guardband","redundancy_spares","optical_crosstalk_guard","ecc_overhead")
    area_b = pitch_b * l_b
    vol_b = area_b * 3.0
    out.append(ProposalDims(
        "B3","Resonant WDM bank (microrings)","SiPh/SiN microrings + tuning",
        lam, round(feat_b,1), round(pitch_b,2), round(l_b,2),
        round(quarter_wave_um(lam,2.0)*1000,1), 3.0,
        round(area_b,2), round(vol_b,3), round(h_b,3),
        round(area_b*h_b,2), round(vol_b*h_b,3),
        "Bend loss/radius, resonator-to-bus coupling gap, thermal sensitivity of resonance",
        "High-Q resonance concentrates field (strong lambda selectivity) but narrow linewidth increases sensitivity to dn, temperature and fabrication; WDM multiplies capacity per bus",
        "R_min~8um (conservative SiPh), coupling gaps ~200-300nm feasible but guarded, vertical stack modest"
    ))

    # --- G1: Passive thin-film membrane stack (fixed thickness WDM) ---
    t_qw_sin = quarter_wave_um(lam, N["SiN"])
    t_qw_sio = quarter_wave_um(lam, N["SiO2"])
    n_layers = 16  # representative WDM/filter stack
    t_stack_um = n_layers * (t_qw_sin + t_qw_sio) / 2.0
    # lateral pixel limited by diffraction/coupling and alignment
    lat_g = max(2.0, confinement_limit_um(lam, N["SiN"]) * 4)
    h_g1 = combined_handicap("yield_guardband","redundancy_spares","alignment_margin","optical_crosstalk_guard","ecc_overhead")
    area_g = lat_g * lat_g
    vol_g = area_g * t_stack_um
    out.append(ProposalDims(
        "G1","Thin-film membrane stack (passive WDM)","Dielectric multilayer (SiN/SiO2/TiO2), fixed d",
        lam, round(confinement_limit_um(lam,N["TiO2"])*1000,1), round(lat_g,2), round(lat_g,2),
        round(t_qw_sin*1000,1), round(t_stack_um,3),
        round(area_g,2), round(vol_g,4), round(h_g1,3),
        round(area_g*h_g1,2), round(vol_g*h_g1,4),
        "Layer thickness tolerance (nm-scale), interface loss/roughness, lateral coupling/alignment",
        "Interference constructive/destructive set by n*d: quarter-wave layers give strong spectral selectivity; SiN/SiO2/TiO2 low loss in NIR, no thermal switching crosstalk",
        f"~{n_layers} alternating layers, t_qw(SiN)~{t_qw_sin*1000:.0f}nm t_qw(SiO2)~{t_qw_sio*1000:.0f}nm, lateral pixel >=2um"
    ))

    # --- G2: EO-tuned membrane/F-P stack ---
    # similar stack but needs EO layer/electrodes -> larger lateral and vertical
    lat_g2 = max(3.0, lat_g * 1.2)
    t_stack_g2 = t_stack_um + 1.0  # EO cladding/electrode spacing proxy
    h_g2 = combined_handicap("yield_guardband","redundancy_spares","alignment_margin","thermal_crosstalk_guard","ecc_overhead")
    area_g2 = lat_g2 * lat_g2
    vol_g2 = area_g2 * t_stack_g2
    out.append(ProposalDims(
        "G2","Thin-film membrane/F-P stack (EO-tuned)","Multilayer dielectric + EO (e.g. TFLN/BTO)",
        lam, round(confinement_limit_um(lam,N["TFLN"])*1000,1), round(lat_g2,2), round(lat_g2,2),
        round(quarter_wave_um(lam,N["TFLN"])*1000,1), round(t_stack_g2,3),
        round(area_g2,2), round(vol_g2,4), round(h_g2,3),
        round(area_g2*h_g2,2), round(vol_g2*h_g2,4),
        "EO overlap and electrode spacing, nm thickness control, thermal drift of resonance, optical loss",
        "EO (Pockels) shifts n -> shifts resonance/phase condition fast without moving mass; dielectric stack provides high density WDM; heating from drivers managed by spacing",
        "Adds EO layer and field margins over G1; fast reconfig but more interfaces"
    ))

    # --- G3: PCM+EO hybrid membrane stack ---
    lat_g3 = max(3.0, lat_g * 1.15)
    # include thin PCM layer per selected cells
    t_stack_g3 = t_stack_um + 0.5
    h_g3 = combined_handicap("yield_guardband","redundancy_spares","alignment_margin","thermal_crosstalk_guard","optical_crosstalk_guard","ecc_overhead")
    area_g3 = lat_g3 * lat_g3
    vol_g3 = area_g3 * t_stack_g3
    out.append(ProposalDims(
        "G3","Thin-film membrane stack (PCM+EO hybrid)","Multilayer + Sb2S3 PCM + EO tuning",
        lam, round(confinement_limit_um(lam,N["sb2s3_a"])*1000,1), round(lat_g3,2), round(lat_g3,2),
        round(quarter_wave_um(lam,N["sb2s3_a"])*1000,1), round(t_stack_g3,3),
        round(area_g3,2), round(vol_g3,4), round(h_g3,3),
        round(area_g3*h_g3,2), round(vol_g3*h_g3,4),
        "PCM crystallization volume/thermal isolation, EO electrode spacing, multilayer tolerance",
        "Sb2S3 provides large dn NV state (n*d step) for persistent spectral weight; EO gives fast fine trim; thermal 300C write requires local confinement/guarding even in thin layers",
        "Hybrid NV+fast; PCM thermal guard increases effective spacing vs G1/G2"
    ))

    # --- H3: Open WDM-PCM (A1 + G1 + B3) modular ---
    # area dominated by A1 thermal pitch and ring/bus routing; G1 vertical
    pitch_h3 = max(PITCH_THERMAL_SAFE_UM, 8.0)
    l_h3 = l_mzi + R_ring + 6.0
    t_h3 = t_stack_um + 4.0  # stacked passive + waveguide layers
    h_h3 = combined_handicap("yield_guardband","redundancy_spares","alignment_margin","thermal_crosstalk_guard","optical_crosstalk_guard","ecc_overhead")
    area_h3 = pitch_h3 * l_h3
    vol_h3 = area_h3 * t_h3
    out.append(ProposalDims(
        "H3","Open WDM-PCM (A1+G1+B3)","MZI-PCM + passive membranes + microrings (modular)",
        lam, round(feat_a1,1), round(pitch_h3,2), round(l_h3,2),
        round(t_qw_sin*1000,1), round(t_h3,3),
        round(area_h3,2), round(vol_h3,3), round(h_h3,3),
        round(area_h3*h_h3,2), round(vol_h3*h_h3,3),
        "PCM thermal isolation, ring bend/coupling, multilayer alignment, cumulative loss budget",
        "Combines A1 large dn NV weights, G1 passive n*d spectral selectivity (no tuning loss), B3 resonant WDM; mostly standard dielectrics + established PIC elements",
        "Modular tile; lateral set by thermal-safe PCM pitch and ring routing; vertical by passive stack + PIC layers"
    ))

    # --- H1: Membrane-Brush NV (A1 + G3 + 3D brush) ---
    # 3D bristle: lateral pitch thermal-safe, vertical stacking of voxels/membranes
    pitch_h1 = PITCH_THERMAL_SAFE_UM
    bristle_len = 60.0  # um, multiple vertical segments/voxels
    vox_layers = 8
    vert_h1 = vox_layers * (t_stack_g3 + ZSEP_AXIAL_UM/2.0)
    h_h1 = combined_handicap("yield_guardband","redundancy_spares","alignment_margin","thermal_crosstalk_guard","optical_crosstalk_guard","ecc_overhead")
    area_h1 = pitch_h1 * pitch_h1  # bristle cross-section footprint
    vol_h1 = area_h1 * vert_h1
    out.append(ProposalDims(
        "H1","Membrane-Brush NV (A1+G3+3D)","MZI-PCM + PCM/EO membranes in 3D bristle",
        lam, round(feat_a1,1), round(pitch_h1,2), round(bristle_len,2),
        round(quarter_wave_um(lam,N["sb2s3_a"])*1000,1), round(vert_h1,3),
        round(area_h1,2), round(vol_h1,3), round(h_h1,3),
        round(area_h1*h_h1,2), round(vol_h1*h_h1,3),
        "3D alignment, vertical thermal isolation between 300C segments, interlayer coupling, yield compounding in 3D",
        "3D stacking multiplies capacity/volume: PCM NV states per voxel + membrane n*d spectral channels; light guided/reflected (45°) along bristle; thermal isolation critical axially/laterally",
        "Footprint per bristle set by thermal pitch; height by voxel count*segment separation; 3D yield/alignment handicap applied"
    ))

    # --- H4: Volumetric Tensor Membrane (G2/G3 + F2 + A1) ---
    pitch_h4 = 8.0
    h_h4 = combined_handicap("yield_guardband","redundancy_spares","alignment_margin","thermal_crosstalk_guard","optical_crosstalk_guard","ecc_overhead") * 1.05
    area_h4 = pitch_h4 * pitch_h4
    vert_h4 = 10 * (t_stack_g2 + 2.0)  # more layers + diffractive spacing
    vol_h4 = area_h4 * vert_h4
    out.append(ProposalDims(
        "H4","Volumetric Tensor Membrane (G2/G3+F2+A1)","Membrane cores 3D + diffractive/meta + PCM NV",
        lam, round(confinement_limit_um(lam,N["TFLN"])*1000,1), round(pitch_h4,2), round(40.0,2),
        round(quarter_wave_um(lam,N["TFLN"])*1000,1), round(vert_h4,3),
        round(area_h4,2), round(vol_h4,3), round(h_h4,3),
        round(area_h4*h_h4,2), round(vol_h4*h_h4,3),
        "Diffractive alignment and phase uniformity, multi-layer registration, compounded 3D yield, thermal management",
        "EO-tuned and PCM-assisted n*d membranes for local tensor ops + diffractive/global interference mixing; highest functional density but tight phase/alignment tolerances",
        "Aggressive stacking and diffractive sections; highest handicap due to compounded tolerances/yield in complex 3D"
    ))

    return out

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    props = proposals()
    rows = [asdict(p) for p in props]

    csv_path = os.path.join(OUT_DIR, "min_dimensions.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = {
        "assumptions": {
            "lambda_signal_nm": LAMBDA_SIGNAL_NM,
            "indices": N,
            "thermal": {"T_pcm_write_C": T_PCM_WRITE_C, "T_vo2_threshold_C": T_VO2_THRESHOLD_C, "pitch_thermal_safe_um": PITCH_THERMAL_SAFE_UM, "zsep_axial_um": ZSEP_AXIAL_UM},
            "handicap_factors": HANDICAP,
        },
        "notes": [
            "Theoretical minimums are first-order estimates from confinement (lambda/2n), quarter-wave thickness (lambda/4n), phase-shift length, bend/resonator scale, and P1 thermal crosstalk spacing.",
            "Effective dimensions multiply geometric minimums by a failure handicap (yield guardband, alignment, redundancy/spares, crosstalk guards, ECC/logical overhead).",
            "Material light behavior: Sb2S3 large dn (0.6) enables compact phase/NV states but requires 300C isolation; VO2 low-threshold volatile switching; azo/spiro small dn for trim; dielectrics (SiN/SiO2/TiO2) low-loss NIR for membranes; EO shifts n rapidly for fast tuning.",
            "Not fabrication-ready; requires FDTD/FEM, thermal 3D, process-specific DRC, and experimental calibration."
        ],
        "proposals": rows,
    }
    with open(os.path.join(OUT_DIR, "min_dimensions.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Markdown report
    lines = [
        "# Dimensiones teóricas mínimas por propuesta (con handicap por fallos)",
        "",
        "> Estimaciones conceptuales de primer orden (no listas para fabricación). Consideran confinamiento óptico, interacción luz-compuesto y márgenes por fallos/tolerancias.",
        "",
        "## Supuestos clave",
        f"- Señal: λ={LAMBDA_SIGNAL_NM} nm (NIR). Controles: 365/450/520/650/800 nm.",
        "- Índices: Sb2S3 2.70/3.30, VO2 2.50/2.00, azo 1.56/1.54, espiropirano 1.54/1.60, SiN 2.00, SiO2 1.45, TiO2 2.45, TFLN 2.20.",
        f"- Térmica (P1): escritura Sb2S3 ~300°C vs umbral VO2 68°C → pitch lateral seguro ~{PITCH_THERMAL_SAFE_UM} µm, separación axial ~{ZSEP_AXIAL_UM} µm.",
        f"- Handicap por fallos (multiplicativo): {HANDICAP}.",
        "",
        "## Tabla comparativa",
        "",
        "| Propuesta | Composición | Feature mín (nm) | Pitch lat mín (µm) | Long. activa mín (µm) | Capa mín (nm) | Pitch vert mín (µm) | Área celda (µm²) | Vol celda (µm³) | Handicap | Área efect. (µm²) | Vol efect. (µm³) | Limitantes |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for p in props:
        lines.append(
            f"| {p.key} | {p.composition} | {p.min_feature_nm} | {p.min_lateral_pitch_um} | {p.min_active_length_um} | "
            f"{p.min_layer_thickness_nm} | {p.min_vertical_pitch_um} | {p.min_cell_area_um2} | {p.min_cell_volume_um3} | "
            f"{p.failure_handicap_factor} | {p.effective_min_cell_area_um2} | {p.effective_min_cell_volume_um3} | {p.limiting_factors} |"
        )
    lines += ["", "## Comportamiento luz-compuesto (resumen por propuesta)", ""]
    for p in props:
        lines.append(f"### {p.key} — {p.name}")
        lines.append(f"- **Interacción:** {p.material_light_behavior}")
        lines.append(f"- **Supuestos:** {p.assumptions}")
        lines.append(f"- **Handicap efectivo:** ×{p.failure_handicap_factor} → área {p.effective_min_cell_area_um2} µm², volumen {p.effective_min_cell_volume_um3} µm³ por celda/elemento mínimo.")
        lines.append("")
    lines += [
        "## Notas",
        "- *Mínimo teórico* ≠ mínimo fabricable: litografía, rugosidad, pérdidas, uniformidad y rendimiento fijan límites mayores según proceso.",
        "- Donde domina la térmica (PCM 300°C cerca de VO₂ 68°C), el pitch no baja de ~6–10 µm sin aislamiento avanzado (consistente con P1).",
        "- En membranas G1/G2/G3, el espesor por capa puede ser sub-µm (λ/4n), pero el volumen efectivo crece por apilado, alineación y redundancia.",
        "- Las propuestas 3D (H1/H4) reducen huella por función al apilar, pero el handicap aumenta por yield/alineación compuesta.",
    ]
    with open(os.path.join(OUT_DIR, "min_dimensions.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(json.dumps({"proposals": len(props), "out": csv_path}))

if __name__ == "__main__":
    main()
