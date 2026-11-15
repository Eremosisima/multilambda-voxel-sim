"""Sensitivity analyses for Article 1 robustness: sweep design and model parameters."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import numpy as np

from compounds import COMPOUNDS, LEVELS_PER_MATERIAL, level_fractions
from model import ideal_response_matrix, forward_readout, invert_readout, quantize_levels


def decode_accuracy(A: np.ndarray, noise_sigma_rad: float = 0.0, calibration_rel_error_std: float = 0.0, trials: int = 500, seed: int = 0):
    rng = np.random.default_rng(seed)
    fr = level_fractions(LEVELS_PER_MATERIAL)
    levels = LEVELS_PER_MATERIAL
    perturb = rng.normal(0.0, calibration_rel_error_std, size=A.shape)
    A_est = A * (1.0 + perturb) if calibration_rel_error_std > 0 else A
    correct = 0
    sym_err = 0
    for _ in range(trials):
        idx_true = rng.integers(0, levels, size=len(COMPOUNDS))
        c = fr[idx_true]
        y = forward_readout(c, A, noise_sigma_rad=noise_sigma_rad, rng=rng)
        try:
            c_hat = invert_readout(y, A_est)
        except np.linalg.LinAlgError:
            continue
        _, idx_hat = quantize_levels(c_hat, levels)
        sym_err += int(np.sum(idx_hat != idx_true))
        if np.all(idx_hat == idx_true):
            correct += 1
    return correct / trials, sym_err / (trials * len(COMPOUNDS))


def sweep_design():
    rows = []
    for L_um in [50, 75, 100, 150, 200]:
        for gamma in [0.2, 0.35, 0.5]:
            for dn_scale in [0.25, 0.5, 1.0, 1.5]:
                A_base = ideal_response_matrix(L_um=L_um, confinement=gamma)
                # scale delta_n effect by scaling A columns proportionally via temp matrix rebuild approximation
                A = A_base * dn_scale
                cond = float(np.linalg.cond(A))
                step = float(np.mean(np.abs(np.diag(A)) / (LEVELS_PER_MATERIAL - 1)))
                wacc, ser = decode_accuracy(A, noise_sigma_rad=0.01, calibration_rel_error_std=0.02, trials=300, seed=11)
                rows.append({
                    "L_um": L_um,
                    "confinement": gamma,
                    "delta_n_scale": dn_scale,
                    "cond_A": cond,
                    "mean_phase_step_rad": step,
                    "word_accuracy_sigma0.01_cal0.02": wacc,
                    "symbol_error_rate": ser,
                })
    return rows


def sweep_crosstalk_and_noise():
    rows = []
    for xt_db in [-20, -25, -30, -40, -60]:
        A = ideal_response_matrix(L_um=100.0, confinement=0.35, crosstalk_db=xt_db)
        cond = float(np.linalg.cond(A))
        for sigma in [0.001, 0.01, 0.03, 0.1, 0.3, 1.0]:
            wacc, ser = decode_accuracy(A, noise_sigma_rad=sigma, calibration_rel_error_std=0.02, trials=400, seed=13)
            rows.append({
                "crosstalk_db": xt_db,
                "noise_sigma_rad": sigma,
                "cond_A": cond,
                "word_accuracy_cal0.02": wacc,
                "symbol_error_rate": ser,
            })
    return rows


def main(out_dir: Path):
    d = sweep_design()
    c = sweep_crosstalk_and_noise()
    for name, rows in [("sensitivity_design.csv", d), ("sensitivity_crosstalk_noise.csv", c)]:
        with (out_dir / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    summary = {
        "design_points": len(d),
        "crosstalk_noise_points": len(c),
        "min_step_among_design_rad": min(r["mean_phase_step_rad"] for r in d),
        "max_step_among_design_rad": max(r["mean_phase_step_rad"] for r in d),
        "worst_word_accuracy_design_sweep": min(r["word_accuracy_sigma0.01_cal0.02"] for r in d),
        "note": "Sensitivity to geometry/confinement/delta_n scaling and crosstalk; use to justify margins and required SNR/calibration.",
    }
    (out_dir / "sensitivity_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    main(Path(__file__).resolve().parent / "outputs")
