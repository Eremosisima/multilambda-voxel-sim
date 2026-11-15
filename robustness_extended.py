"""Extended robustness: calibration/gain error and noise thresholds."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import numpy as np

from compounds import COMPOUNDS, LEVELS_PER_MATERIAL, level_fractions
from model import ideal_response_matrix, forward_readout, invert_readout, quantize_levels


def test_with_calibration_error(A_true: np.ndarray, rel_error: float, noise_sigma_rad: float, trials: int = 500, seed: int = 1):
    rng = np.random.default_rng(seed)
    fr = level_fractions(LEVELS_PER_MATERIAL)
    levels = LEVELS_PER_MATERIAL
    # decoder uses perturbed estimate of A (calibration/fabrication mismatch)
    perturb = rng.normal(0.0, rel_error, size=A_true.shape)
    A_est = A_true * (1.0 + perturb)
    total = 0
    correct = 0
    sym_err = 0
    for _ in range(trials):
        idx_true = rng.integers(0, levels, size=len(COMPOUNDS))
        c = fr[idx_true]
        y = forward_readout(c, A_true, noise_sigma_rad=noise_sigma_rad, rng=rng)
        c_hat = invert_readout(y, A_est)
        _, idx_hat = quantize_levels(c_hat, levels)
        total += 1
        sym_err += int(np.sum(idx_hat != idx_true))
        if np.all(idx_hat == idx_true):
            correct += 1
    return {
        "calibration_rel_error_std": rel_error,
        "noise_sigma_rad": noise_sigma_rad,
        "word_accuracy": correct / total,
        "symbol_error_rate": sym_err / (total * len(COMPOUNDS)),
        "trials": total,
    }


def sweep():
    A = ideal_response_matrix(L_um=100.0, confinement=0.35)
    rows = []
    for rel in [0.0, 0.01, 0.02, 0.05, 0.1]:
        for sigma in [0.001, 0.01, 0.03, 0.1]:
            rows.append(test_with_calibration_error(A, rel, sigma, trials=400, seed=7))
    return rows


def main(out_dir: Path):
    rows = sweep()
    with (out_dir / "robustness_calibration_sweep.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # summary thresholds (word accuracy >= 0.99)
    ok = [r for r in rows if r["word_accuracy"] >= 0.99]
    summary = {
        "rows": len(rows),
        "high_accuracy_points_word_acc_ge_0_99": ok,
        "note": "Model-level robustness; real systems also need drift, nonlinearity, saturation and detector noise models.",
    }
    (out_dir / "robustness_calibration_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return rows, summary


if __name__ == "__main__":
    main(Path(__file__).resolve().parent / "outputs")
