"""Linear superposition model and readout matrix inversion.

Model: Δn_total(λ_r,j) contribution from material i is approximated as
    Δn_i = c_i * Δn_i,max
and measured phase/readout signals are linear in state vector c (within design regime).

For simulation we define a 4x4 response matrix A where
    y = A c + e
with c_i in [0,1] (discrete levels), y the measured differential phase (radians)
at each read wavelength/channel, and e measurement noise.
"""
from __future__ import annotations

import numpy as np
from compounds import COMPOUNDS, LEVELS_PER_MATERIAL, level_fractions


def refractive_index_change(c: np.ndarray) -> np.ndarray:
    """Total per-material index change Δn_i = c_i * Δn_i,max for state vector c."""
    c = np.asarray(c, dtype=float)
    dn_max = np.array([m.delta_n_max for m in COMPOUNDS], dtype=float)
    return c * dn_max


def total_delta_n(c: np.ndarray) -> float:
    """Scalar sum model Δn_total = Σ c_i * Δn_i,max (effective single-voxel aggregate)."""
    return float(np.sum(refractive_index_change(c)))


def ideal_response_matrix(L_um: float = 100.0, confinement: float = 0.35, crosstalk_db: float = -30.0) -> np.ndarray:
    """Build 4x4 matrix A mapping material states to phase readouts.

    Diagonal terms: Δφ_i = (2π/λ_i) * Γ * Δn_i,max * L for unit state.
    Off-diagonal terms: residual spectral/field crosstalk modeled as a small fraction.
    This is a simulation model; experimental calibration would replace A.
    """
    n = len(COMPOUNDS)
    A = np.zeros((n, n), dtype=float)
    L_m = L_um * 1e-6
    x = 10 ** (crosstalk_db / 20.0)  # amplitude-like coupling fraction for simulation
    for j, m_read in enumerate(COMPOUNDS):
        lam = m_read.read_nm * 1e-9
        for i, m_mat in enumerate(COMPOUNDS):
            dphi = (2 * np.pi / lam) * confinement * m_mat.delta_n_max * L_m
            if i == j:
                A[j, i] = dphi
            else:
                # mild wavelength-dependent leakage; stronger if read/write bands closer (simplified)
                sep = abs(m_read.read_nm - COMPOUNDS[i].read_nm)
                sep_factor = np.exp(-sep / 300.0)
                A[j, i] = dphi * x * (0.5 + 0.5 * sep_factor)
    return A


def forward_readout(c: np.ndarray, A: np.ndarray, noise_sigma_rad: float = 0.0, rng=None) -> np.ndarray:
    rng = np.random.default_rng(rng)
    y = A @ np.asarray(c, dtype=float)
    if noise_sigma_rad > 0:
        y = y + rng.normal(0.0, noise_sigma_rad, size=y.shape)
    return y


def invert_readout(y: np.ndarray, A: np.ndarray) -> np.ndarray:
    """Estimate continuous state vector c from readout y by solving A c = y."""
    return np.linalg.solve(A, y)


def quantize_levels(c_hat: np.ndarray, levels: int = LEVELS_PER_MATERIAL) -> np.ndarray:
    fr = level_fractions(levels)
    idx = np.clip(np.rint(c_hat * (levels - 1)), 0, levels - 1).astype(int)
    return fr[idx], idx


def enumerate_states(levels: int = LEVELS_PER_MATERIAL):
    fr = level_fractions(levels)
    import itertools

    for combo in itertools.product(range(levels), repeat=len(COMPOUNDS)):
        c = np.array([fr[k] for k in combo], dtype=float)
        yield combo, c
