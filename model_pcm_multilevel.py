#!/usr/bin/env python3
"""P1 modeling: segmented/tapered Sb2S3 multilevel PCM cell (conceptual, data-backed estimates).

Generates level/phase/transmission/energy/loss estimates and figures under outputs/ and figures/.
Assumptions are documented in outputs/pcm_multilevel_summary.json and report.
"""
from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import Dict, List

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None

OUT_DIR = "outputs"
FIG_DIR = "figures"


@dataclass
class PCMParams:
    material: str = "Sb2S3"
    n_amorphous: float = 2.70
    n_crystalline: float = 3.30
    # effective index change seen by guided mode (fraction of material dn, mode overlap dependent)
    mode_overlap: float = 0.35
    # extinction/absorption proxies (dB/cm) at read wavelength, assumed for conceptual model
    alpha_a_db_cm: float = 5.0
    alpha_c_db_cm: float = 40.0
    read_lambda_nm: float = 1550.0
    program_lambda_nm: float = 650.0
    t_write_c: float = 300.0
    t_erase_c: float = 250.0  # melt-quench/amorphization thermal reference
    cell_length_um: float = 10.0
    segments: int = 8
    taper_extra_loss_db: float = 0.05  # per tapered interface, design target
    bits_levels: int = 32  # 5-bit target


def ensure_dirs() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def level_fractions(levels: int) -> np.ndarray:
    return np.linspace(0.0, 1.0, levels)


def compute_levels(p: PCMParams) -> List[Dict]:
    f = level_fractions(p.bits_levels)
    dn_mat = p.n_crystalline - p.n_amorphous
    dneff = p.mode_overlap * dn_mat
    L_cm = p.cell_length_um * 1e-4
    lam_cm = p.read_lambda_nm * 1e-7
    rows = []
    for i, frac in enumerate(f):
        # linear mixing approximation for partial crystallization fraction
        n_eff = p.n_amorphous + dneff * frac
        delta_neff = dneff * frac
        delta_phi_rad = 2.0 * math.pi * delta_neff * L_cm / lam_cm
        alpha_db_cm = p.alpha_a_db_cm + (p.alpha_c_db_cm - p.alpha_a_db_cm) * frac
        il_db = alpha_db_cm * L_cm + p.taper_extra_loss_db * 2.0
        transmission = 10 ** (-il_db / 10.0)
        # programming energy estimate: scales with crystallized volume fraction step and thermal budget
        # normalized conceptual value (pJ) for a 10um x 0.5um x 0.03um effective heated volume
        vol_um3 = p.cell_length_um * 0.5 * 0.03
        e_write_pj = 0.8 * vol_um3 * (0.2 + 0.8 * frac)  # higher fraction -> higher cumulative energy
        e_step_pj = 0.8 * vol_um3 * (0.8 / max(p.bits_levels - 1, 1))
        rows.append({
            "level": i,
            "crystallinity_fraction": round(float(frac), 6),
            "n_eff": round(float(n_eff), 6),
            "delta_neff": round(float(delta_neff), 6),
            "delta_phi_rad": round(float(delta_phi_rad), 6),
            "delta_phi_pi": round(float(delta_phi_rad / math.pi), 6),
            "insertion_loss_db": round(float(il_db), 6),
            "transmission": round(float(transmission), 6),
            "alpha_eff_db_cm": round(float(alpha_db_cm), 6),
            "cum_program_energy_pj_est": round(float(e_write_pj), 4),
            "step_program_energy_pj_est": round(float(e_step_pj), 4),
        })
    return rows


def segmentation_analysis(p: PCMParams) -> Dict:
    # Compare monolithic vs segmented/tapered concept (loss and thermal confinement proxies)
    mono_il = (p.alpha_a_db_cm + (p.alpha_c_db_cm - p.alpha_a_db_cm) * 0.5) * (p.cell_length_um * 1e-4)
    seg_il = mono_il + p.taper_extra_loss_db * 2.0 * 0.6  # tapers mitigate scattering penalty
    return {
        "segments": p.segments,
        "monolithic_mid_il_db_est": round(mono_il, 6),
        "segmented_tapered_mid_il_db_est": round(seg_il, 6),
        "scattering_reduction_factor_est": 0.35,
        "thermal_confinement_improvement_est": 0.25,
        "rationale": "Segmentation/tapering targets lower scattering and better heat confinement; values are design targets consistent with reported PCM nanostructuring trends."
    }


def write_outputs(p: PCMParams, rows: List[Dict], seg: Dict) -> None:
    with open(os.path.join(OUT_DIR, "pcm_multilevel_levels.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    phi = np.array([r["delta_phi_rad"] for r in rows])
    il = np.array([r["insertion_loss_db"] for r in rows])
    margins = np.diff(phi)
    summary = {
        "params": asdict(p),
        "num_levels": len(rows),
        "bits": round(math.log2(len(rows)), 3),
        "phase_range_rad": round(float(phi[-1] - phi[0]), 6),
        "phase_range_pi": round(float((phi[-1] - phi[0]) / math.pi), 6),
        "min_phase_step_rad": round(float(np.min(margins)), 6),
        "mean_phase_step_rad": round(float(np.mean(margins)), 6),
        "il_min_db": round(float(np.min(il)), 6),
        "il_max_db": round(float(np.max(il)), 6),
        "segmentation": seg,
        "assumptions": [
            "Linear mixing of effective index/absorption vs crystallinity fraction (first-order).",
            "Mode overlap and loss coefficients are design-estimate placeholders to be calibrated by FDTD/FEM and measurement.",
            "Energy estimates are normalized conceptual values proportional to effective switched volume and fraction.",
            "Material indices from project spec: Sb2S3 amorphous 2.70, crystalline 3.30; read at 1550 nm conceptually."
        ],
        "references_context": [
            "Sb2S3 multilevel electrical control (Nat. Commun. 2023, 10.1038/s41467-023-39180-3)",
            "High-density/optimized PCM photonic memory (Photonics 2025, 10.3390/photonics12111130)",
            "Nanostructured/tapered PCM for low loss and endurance (arXiv 2604.08637)"
        ]
    }
    with open(os.path.join(OUT_DIR, "pcm_multilevel_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    lines = [
        "# P1 Modeling Report: Sb2S3 Segmented/Tapered Multilevel PCM Cell",
        "",
        f"- Material: {p.material}, n_a={p.n_amorphous}, n_c={p.n_crystalline}, read λ={p.read_lambda_nm} nm, L={p.cell_length_um} µm, segments={p.segments}",
        f"- Levels: {len(rows)} ({summary['bits']} bits), phase range {summary['phase_range_rad']:.4f} rad ({summary['phase_range_pi']:.3f} π)",
        f"- Mean/min phase step: {summary['mean_phase_step_rad']:.6f} / {summary['min_phase_step_rad']:.6f} rad",
        f"- Insertion loss range: {summary['il_min_db']:.4f}–{summary['il_max_db']:.4f} dB",
        f"- Segmentation (mid-state IL est.): mono {seg['monolithic_mid_il_db_est']:.4f} dB vs seg/taper {seg['segmented_tapered_mid_il_db_est']:.4f} dB",
        "",
        "## Assumptions",
    ] + [f"- {a}" for a in summary["assumptions"]] + ["", "## Reference context"] + [f"- {r}" for r in summary["references_context"]]
    with open(os.path.join(OUT_DIR, "pcm_multilevel_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def plot_outputs(rows: List[Dict]) -> None:
    if plt is None:
        return
    frac = [r["crystallinity_fraction"] for r in rows]
    phi = [r["delta_phi_rad"] for r in rows]
    il = [r["insertion_loss_db"] for r in rows]
    tr = [r["transmission"] for r in rows]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(frac, phi, marker='o', ms=3)
    ax.set_xlabel("Crystallinity fraction")
    ax.set_ylabel("Δφ (rad)")
    ax.set_title("Sb2S3 multilevel phase vs crystallinity")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "pcm_multilevel_phase.png"), dpi=150)
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(frac, il, color='tab:red', marker='o', ms=3, label='IL (dB)')
    ax1.set_xlabel("Crystallinity fraction")
    ax1.set_ylabel("Insertion loss (dB)", color='tab:red')
    ax2 = ax1.twinx()
    ax2.plot(frac, tr, color='tab:blue', marker='x', ms=3, label='T')
    ax2.set_ylabel("Transmission", color='tab:blue')
    ax1.set_title("Insertion loss and transmission vs crystallinity")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "pcm_multilevel_loss.png"), dpi=150)
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    p = PCMParams()
    rows = compute_levels(p)
    seg = segmentation_analysis(p)
    write_outputs(p, rows, seg)
    plot_outputs(rows)
    print(json.dumps({"levels": len(rows), "out": OUT_DIR}, indent=2))


if __name__ == "__main__":
    main()
