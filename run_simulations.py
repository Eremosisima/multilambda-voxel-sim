"""Run all Article 1 simulations and save tables/figures."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from compounds import COMPOUNDS, LEVELS_PER_MATERIAL, BITS_PER_VOXEL, compound_table_rows
from model import ideal_response_matrix, enumerate_states, forward_readout, invert_readout, quantize_levels
from mzi_sim import phase_per_level, sweep_noise
from crosstalk import thermal_crosstalk, optical_crosstalk, min_distance_for_threshold
from robustness_extended import main as robustness_main
from sustainability_energy import main as sustainability_main
from sensitivity import main as sensitivity_main
from snr_budget import main as snr_budget_main
from scaling_robustness import main as scaling_robustness_main

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
FIG = ROOT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)


def save_csv(path: Path, rows, fieldnames=None):
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def simulate_compounds():
    rows = compound_table_rows()
    save_csv(OUT / "compounds.csv", rows)
    lines = [
        f"Compounds: {len(COMPOUNDS)}",
        f"Levels per material: {LEVELS_PER_MATERIAL}",
        f"Bits per voxel: {BITS_PER_VOXEL}",
        "",
    ]
    for r in rows:
        lines.append(
            f"- {r['key']} {r['compound']}: write={r['lambda_write_nm']} nm, "
            f"erase={r['lambda_erase_nm']} nm, read={r['lambda_read_nm']} nm, "
            f"Δn_max={r['delta_n_max']}, t1/2={r['thermal_half_life_s']} s"
        )
    (OUT / "compounds_summary.txt").write_text("\n".join(lines), encoding="utf-8")
    return rows


def simulate_mzi():
    rows, A = phase_per_level(L_um=100.0, confinement=0.35)
    save_csv(OUT / "mzi_phase_levels.csv", rows)
    np.savetxt(OUT / "response_matrix_A.csv", A, delimiter=",")
    cond = float(np.linalg.cond(A))

    noise_rows = sweep_noise(A)
    save_csv(OUT / "noise_sweep.csv", noise_rows)

    # Ideal decode check over all 256 states with no noise
    ok = 0
    total = 0
    for combo, c in enumerate_states():
        y = forward_readout(c, A, noise_sigma_rad=0.0)
        c_hat = invert_readout(y, A)
        _, idx_hat = quantize_levels(c_hat)
        if np.array_equal(np.array(combo), idx_hat):
            ok += 1
        total += 1

    summary = {
        "L_um": 100.0,
        "confinement": 0.35,
        "matrix_condition_number": cond,
        "all_states_noiseless_decode_accuracy": ok / total,
        "total_states": total,
    }
    (OUT / "mzi_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Plot: phase per level
    labels = [r["material"] for r in rows]
    vals = [abs(r["delta_phi_per_level_rad"]) for r in rows]
    plt.figure(figsize=(7, 4))
    bars = plt.bar(labels, vals, color=["#4C72B0", "#55A868", "#C44E52", "#8172B3"])
    plt.ylabel("|Δφ| per level (rad)")
    plt.title("MZI phase step per material level (L=100 µm, Γ=0.35)")
    for b, v in zip(bars, vals):
        plt.text(b.get_x() + b.get_width()/2, v, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    plt.savefig(FIG / "mzi_phase_per_level.png", dpi=160)
    plt.close()

    # Plot: noise sweep
    sig = [r["noise_sigma_rad"] for r in noise_rows]
    acc = [r["word_accuracy"] for r in noise_rows]
    ser = [r["symbol_error_rate"] for r in noise_rows]
    plt.figure(figsize=(7, 4))
    plt.semilogx(sig, acc, marker="o", label="Word accuracy (8-bit voxel)")
    plt.semilogx(sig, ser, marker="s", label="Symbol error rate")
    plt.xlabel("Phase noise σ (rad)")
    plt.ylabel("Rate")
    plt.ylim(-0.05, 1.05)
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.title("Decode robustness vs phase noise")
    plt.tight_layout()
    plt.savefig(FIG / "noise_robustness.png", dpi=160)
    plt.close()

    return rows, noise_rows, summary


def simulate_crosstalk():
    thermal_rows, Ld = thermal_crosstalk()
    optical_rows = optical_crosstalk()
    save_csv(OUT / "thermal_crosstalk.csv", thermal_rows)
    save_csv(OUT / "optical_crosstalk.csv", optical_rows)

    d_th = min_distance_for_threshold(thermal_rows, "distance_um")
    d_op = min_distance_for_threshold(optical_rows, "distance_um")
    summary = {
        "thermal_diffusion_length_um": Ld,
        "thermal_threshold_K": thermal_rows[0]["threshold_K"] if thermal_rows else None,
        "min_distance_thermal_um": d_th,
        "optical_threshold_fraction": optical_rows[0]["threshold_fraction"] if optical_rows else None,
        "min_distance_optical_um": d_op,
        "recommended_layer_spacing_um": max([d for d in [d_th, d_op] if d is not None] + [0.0]),
    }
    (OUT / "crosstalk_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Thermal plot
    d = [r["distance_um"] for r in thermal_rows]
    t = [r["deltaT_K"] for r in thermal_rows]
    thr = thermal_rows[0]["threshold_K"]
    plt.figure(figsize=(7, 4))
    plt.plot(d, t, label="Estimated ΔT in adjacent layer")
    plt.axhline(thr, color="r", linestyle="--", label=f"Threshold {thr} K")
    if d_th is not None:
        plt.axvline(d_th, color="g", linestyle=":", label=f"Min distance ~{d_th:.2f} µm")
    plt.xlabel("Layer separation (µm)")
    plt.ylabel("Temperature rise ΔT (K)")
    plt.title("Thermal crosstalk vs layer separation")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "thermal_crosstalk.png", dpi=160)
    plt.close()

    # Optical plot
    d = [r["distance_um"] for r in optical_rows]
    p = [r["parasitic_fraction"] for r in optical_rows]
    thrp = optical_rows[0]["threshold_fraction"]
    plt.figure(figsize=(7, 4))
    plt.semilogy(d, np.maximum(p, 1e-12), label="Parasitic excitation fraction")
    plt.axhline(thrp, color="r", linestyle="--", label=f"Threshold {thrp:.0%}")
    if d_op is not None:
        plt.axvline(d_op, color="g", linestyle=":", label=f"Min distance ~{d_op:.2f} µm")
    plt.xlabel("Layer separation (µm)")
    plt.ylabel("Parasitic fraction")
    plt.title("Optical crosstalk vs layer separation")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "optical_crosstalk.png", dpi=160)
    plt.close()

    return summary


def main():
    simulate_compounds()
    mzi_rows, noise_rows, mzi_summary = simulate_mzi()
    xt_summary = simulate_crosstalk()
    robustness_rows, robustness_summary = robustness_main(OUT)
    sens_summary = sensitivity_main(OUT)
    snr_summary = snr_budget_main(OUT)
    scaling_summary = scaling_robustness_main(OUT)
    sust = sustainability_main(OUT)

    ref_co2 = sust["reference_derived"]["datacenter_tco2_per_year_with_cooling"]
    best = max(sust["datacenter_scenarios_same_work"], key=lambda r: r["relative_efficiency_vs_ref"])
    report = [
        "# Simulation report (Article 1 draft support)",
        "",
        f"- Materials: {len(COMPOUNDS)}; levels/material: {LEVELS_PER_MATERIAL}; capacity: {BITS_PER_VOXEL} bits/voxel",
        f"- MZI matrix condition number: {mzi_summary['matrix_condition_number']:.4f}",
        f"- Noiseless full-state decode accuracy: {mzi_summary['all_states_noiseless_decode_accuracy']*100:.1f}% ({mzi_summary['total_states']} states)",
        "- Phase step per level (rad): " + ", ".join(f"{r['material']}={r['delta_phi_per_level_rad']:.4f}" for r in mzi_rows),
        f"- Recommended layer spacing (model): >= {xt_summary['recommended_layer_spacing_um']:.2f} µm",
        f"- Thermal diffusion length (estimate): {xt_summary['thermal_diffusion_length_um']:.2f} µm",
        f"- Robustness sweep points: {len(robustness_rows)} (see outputs/robustness_calibration_sweep.csv)",
        f"- Sensitivity: design {sens_summary['design_points']} pts, crosstalk/noise {sens_summary['crosstalk_noise_points']} pts (outputs/sensitivity_*.csv)",
        f"- SNR budget points: {snr_summary['total_points']}, feasible (half-step margin >=3*sigma): {snr_summary['feasible_half_step_margin_ge_3sigma']} (outputs/snr_budget.csv)",
        f"- Monte Carlo robustness (400 samples): mean word acc={scaling_summary['monte_carlo']['mean_word_accuracy']:.3f}, p05={scaling_summary['monte_carlo']['p05_word_accuracy']:.3f} (outputs/scaling_robustness_summary.json)",
        f"- Sustainability scenario (same-work, best case {best['scenario_photonic_tops_per_w']} TOPS/W vs ref): avoided ~{best['avoided_tco2_per_year']:.0f} tCO2/year out of {ref_co2:.0f} tCO2/year (assumptions in outputs/sustainability_scenarios.json)",
        "",
        "Key artifacts: outputs/*.csv, outputs/*.json, figures/*.png, ARTICLE1_SKELETON.md",
        "Note: parameters are literature-inspired simulation assumptions; replace with cited/measured values for publication. Energy/CO2 results are scenarios, not measured device claims.",
    ]
    (OUT / "report.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
