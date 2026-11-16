"""Scaled and uncertainty-aware robustness analysis.

Adds Monte Carlo uncertainty propagation, level-scaling, and simple array crosstalk scaling.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import numpy as np

from compounds import COMPOUNDS
from model import ideal_response_matrix, forward_readout, invert_readout, quantize_levels


def mc_uncertainty(n_samples: int = 500, seed: int = 123):
    """Propagate parameter uncertainty to margins and decode performance."""
    rng = np.random.default_rng(seed)
    rows = []
    summary = {"n_samples": n_samples, "pass_word_accuracy_ge_0_99": 0}
    min_steps = []
    conds = []
    accs = []
    for i in range(n_samples):
        L_um = rng.normal(100.0, 5.0)          # fabrication/length variation
        Gamma = rng.normal(0.35, 0.03)
        dn_scale = rng.normal(1.0, 0.10)       # material/index uncertainty
        xt_db = rng.normal(-30.0, 3.0)
        sigma = abs(rng.normal(0.01, 0.005))  # phase noise
        cal_err = abs(rng.normal(0.02, 0.01))

        L_um = float(np.clip(L_um, 50, 200))
        Gamma = float(np.clip(Gamma, 0.1, 0.6))
        dn_scale = float(np.clip(dn_scale, 0.4, 1.6))
        xt_db = float(np.clip(xt_db, -50, -15))

        A = ideal_response_matrix(L_um=L_um, confinement=Gamma, crosstalk_db=xt_db) * dn_scale
        cond = float(np.linalg.cond(A))
        step = float(np.mean(np.abs(np.diag(A)) / 3.0))

        # quick decode test
        levels = 4
        fr = np.linspace(0.0, 1.0, levels)
        perturb = rng.normal(0.0, cal_err, size=A.shape)
        A_est = A * (1.0 + perturb)
        trials = 80
        correct = 0
        for _ in range(trials):
            idx_true = rng.integers(0, levels, size=len(COMPOUNDS))
            c = fr[idx_true]
            y = forward_readout(c, A, noise_sigma_rad=sigma, rng=rng)
            try:
                c_hat = invert_readout(y, A_est)
            except np.linalg.LinAlgError:
                correct += 0
                continue
            _, idx_hat = quantize_levels(c_hat, levels)
            if np.all(idx_hat == idx_true):
                correct += 1
        acc = correct / trials
        min_steps.append(step)
        conds.append(cond)
        accs.append(acc)
        if acc >= 0.99:
            summary["pass_word_accuracy_ge_0_99"] += 1
        if i < 50:  # sample rows
            rows.append({
                "sample": i,
                "L_um": L_um, "confinement": Gamma, "delta_n_scale": dn_scale,
                "crosstalk_db": xt_db, "noise_sigma_rad": sigma, "calibration_rel_error_std": cal_err,
                "cond_A": cond, "mean_phase_step_rad": step, "word_accuracy": acc,
            })
    summary.update({
        "mean_phase_step_rad": float(np.mean(min_steps)),
        "p05_phase_step_rad": float(np.quantile(min_steps, 0.05)),
        "p95_phase_step_rad": float(np.quantile(min_steps, 0.95)),
        "mean_cond_A": float(np.mean(conds)),
        "p95_cond_A": float(np.quantile(conds, 0.95)),
        "mean_word_accuracy": float(np.mean(accs)),
        "p05_word_accuracy": float(np.quantile(accs, 0.05)),
        "pass_rate_word_accuracy_ge_0_99": summary["pass_word_accuracy_ge_0_99"] / n_samples,
    })
    return rows, summary


def level_scaling(levels_list=(2, 4, 8, 16)):
    """Evaluate margin vs number of quantization levels (same physical phase range)."""
    A = ideal_response_matrix(L_um=100.0, confinement=0.35)
    out = []
    for L in levels_list:
        step = float(np.mean(np.abs(np.diag(A)) / (L - 1)))
        half_margin = step / 2.0
        bits = int(len(COMPOUNDS) * math.log2(L))
        # approximate tolerable sigma for 3-sigma half-step margin
        sigma_3 = half_margin / 3.0 if half_margin > 0 else 0.0
        out.append({
            "levels_per_material": L,
            "bits_per_voxel": bits,
            "states_per_voxel": L ** len(COMPOUNDS),
            "mean_phase_step_rad": step,
            "half_step_margin_rad": half_margin,
            "sigma_for_3sigma_half_step_margin_rad": sigma_3,
        })
    return out


def array_crosstalk_scaling(sizes=(1, 2, 4, 8, 16), pitch_um: float = 10.0):
    """Simple nearest-neighbor aggregated crosstalk scaling for NxN voxel arrays.

    Model: effective interference term grows with number of active neighbors within coupling radius.
    This is a coarse scaling estimate, not a full EM simulation.
    """
    out = []
    coupling_radius_um = 30.0
    base_xt_db = -30.0
    base_x = 10 ** (base_xt_db / 20.0)
    for N in sizes:
        voxels = N * N
        # average neighbors in grid (4-neighborhood interior approximation)
        if N == 1:
            neighbors = 0
        elif N == 2:
            neighbors = 2
        else:
            neighbors = 4 * (1 - 1 / N)  # rough average
        spatial = math.exp(-pitch_um / coupling_radius_um)
        agg = base_x * neighbors * spatial
        agg_db = 20 * math.log10(max(agg, 1e-12))
        # crude SIR-like margin proxy
        margin_db = -agg_db
        out.append({
            "array_size": f"{N}x{N}",
            "voxels": voxels,
            "pitch_um": pitch_um,
            "avg_neighbors_model": neighbors,
            "aggregated_crosstalk_linear": agg,
            "aggregated_crosstalk_db": agg_db,
            "isolation_margin_db_proxy": margin_db,
        })
    return out


def main(out_dir: Path):
    mc_rows, mc_summary = mc_uncertainty(n_samples=400, seed=123)
    lvl_rows = level_scaling()
    arr_rows = array_crosstalk_scaling()

    with (out_dir / "mc_uncertainty_samples.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(mc_rows[0].keys()))
        w.writeheader()
        w.writerows(mc_rows)
    with (out_dir / "level_scaling.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lvl_rows[0].keys()))
        w.writeheader()
        w.writerows(lvl_rows)
    with (out_dir / "array_crosstalk_scaling.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(arr_rows[0].keys()))
        w.writeheader()
        w.writerows(arr_rows)

    summary = {
        "monte_carlo": mc_summary,
        "level_scaling": lvl_rows,
        "array_scaling": arr_rows,
        "notes": "Uncertainty propagation assumes independent Gaussian parameter perturbations; array scaling is a coarse nearest-neighbor model. Use for design trends, not final performance guarantees.",
    }
    (out_dir / "scaling_robustness_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    main(Path(__file__).resolve().parent / "outputs")
