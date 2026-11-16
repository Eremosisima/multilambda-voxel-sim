"""MZI phase-shift, noise, and level-distinguishability simulations."""
from __future__ import annotations

import numpy as np
from compounds import COMPOUNDS, LEVELS_PER_MATERIAL, level_fractions
from model import ideal_response_matrix, forward_readout, invert_readout, quantize_levels


def phase_per_level(L_um: float = 100.0, confinement: float = 0.35):
    """Return Δφ per discrete level step for each material at its read channel."""
    A = ideal_response_matrix(L_um=L_um, confinement=confinement)
    fr = level_fractions(LEVELS_PER_MATERIAL)
    step = fr[1] - fr[0] if len(fr) > 1 else 1.0
    # diagonal-dominant phase step in own channel
    per_level = np.diag(A) * step
    rows = []
    for i, m in enumerate(COMPOUNDS):
        rows.append(
            {
                "material": m.key,
                "name": m.name,
                "read_nm": m.read_nm,
                "delta_phi_full_rad": float(np.diag(A)[i]),
                "delta_phi_per_level_rad": float(per_level[i]),
                "delta_phi_per_level_deg": float(np.degrees(per_level[i])),
            }
        )
    return rows, A


def noise_sigma_from_snr(phase_step_rad: float, snr: float) -> float:
    """Approximate phase noise sigma such that SNR = phase_step / sigma."""
    if snr <= 0:
        return float("inf")
    return abs(phase_step_rad) / snr


def distinguishability_test(A: np.ndarray, noise_sigma_rad: float, trials: int = 400, rng_seed: int = 0):
    """Monte Carlo: probability of correctly decoding all 4 material states at once."""
    rng = np.random.default_rng(rng_seed)
    fr = level_fractions(LEVELS_PER_MATERIAL)
    levels = LEVELS_PER_MATERIAL
    total = 0
    correct = 0
    symbol_errors = 0
    # sample random states (full enumeration is 256 states; sample for speed but include edges)
    for _ in range(trials):
        idx_true = rng.integers(0, levels, size=len(COMPOUNDS))
        c = fr[idx_true]
        y = forward_readout(c, A, noise_sigma_rad=noise_sigma_rad, rng=rng)
        c_hat = invert_readout(y, A)
        _, idx_hat = quantize_levels(c_hat, levels)
        total += 1
        symbol_errors += int(np.sum(idx_hat != idx_true))
        if np.all(idx_hat == idx_true):
            correct += 1
    return {
        "noise_sigma_rad": noise_sigma_rad,
        "word_accuracy": correct / total if total else 0.0,
        "symbol_error_rate": symbol_errors / (total * len(COMPOUNDS)) if total else 0.0,
        "trials": total,
    }


def sweep_noise(A: np.ndarray):
    sigmas = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
    return [distinguishability_test(A, s, trials=600, rng_seed=42) for s in sigmas]
