"""Thermal and optical crosstalk estimates vs layer separation.

These are simplified engineering models for Article 1 simulations:
- Thermal: 1D diffusion from a write pulse in one layer; require adjacent-layer temperature
  rise to stay below an activation/perturbation threshold.
- Optical: Beer-Lambert absorption of a write beam in neighboring layers; require parasitic
  absorption fraction below a threshold when layers are spaced/separated by buffers.
"""
from __future__ import annotations

import numpy as np


def thermal_crosstalk(
    distances_um=None,
    pulse_energy_nj: float = 2.0,
    pulse_radius_um: float = 2.0,
    layer_thickness_um: float = 0.5,
    rho: float = 1200.0,  # kg/m^3, polymer-like
    cp: float = 1400.0,   # J/kg/K
    k_th: float = 0.2,    # W/m/K
    t_eff_us: float = 10.0,
    delta_t_threshold_k: float = 5.0,
):
    """Estimate peak temperature rise in a neighboring layer after a write pulse.

    Uses a diffusion-length approximation: L_d = sqrt(alpha * t), alpha = k/(rho*cp).
    Temperature rise scales approximately as exp(-d/L_d) from source region.
    """
    if distances_um is None:
        distances_um = np.linspace(0.1, 20.0, 120)

    d_m = np.asarray(distances_um) * 1e-6
    alpha = k_th / (rho * cp)
    t_s = t_eff_us * 1e-6
    L_d = np.sqrt(alpha * t_s)

    vol = np.pi * (pulse_radius_um * 1e-6) ** 2 * (layer_thickness_um * 1e-6)
    dT0 = (pulse_energy_nj * 1e-9) / (rho * cp * max(vol, 1e-30))
    dT = dT0 * np.exp(-d_m / max(L_d, 1e-30))

    rows = []
    for dist, rise in zip(distances_um, dT):
        rows.append(
            {
                "distance_um": float(dist),
                "deltaT_K": float(rise),
                "below_threshold": bool(rise <= delta_t_threshold_k),
                "threshold_K": delta_t_threshold_k,
                "thermal_diffusion_length_um": float(L_d * 1e6),
                "source_deltaT_K_est": float(dT0),
            }
        )
    return rows, float(L_d * 1e6)


def optical_crosstalk(
    distances_um=None,
    alpha_abs_cm_inv: float = 2e4,  # absorption of active layer at neighbor's write wavelength (worst-case residual)
    isolation_factor: float = 1e-3,  # spectral/filter/isolation at non-target wavelength
    active_thickness_um: float = 0.3,
    parasitic_threshold: float = 0.01,  # 1% parasitic write fraction
):
    """Estimate parasitic optical excitation in adjacent layers.

    Model: fraction ~ isolation_factor * (1-exp(-alpha*d_layer)) * exp(-alpha_buffer*d_sep)
    Buffer assumed low-loss; separation provides geometric/spectral isolation in practice.
    Here separation penalty is modeled phenomenologically as exp(-d/3um) for confined modes.
    """
    if distances_um is None:
        distances_um = np.linspace(0.0, 20.0, 121)
    d = np.asarray(distances_um, dtype=float)
    alpha_um = alpha_abs_cm_inv * 1e-4
    absorb_in_active = 1.0 - np.exp(-alpha_um * active_thickness_um)
    confinement_leak = np.exp(-d / 3.0)
    parasitic = isolation_factor * absorb_in_active * confinement_leak
    rows = []
    for dist, frac in zip(d, parasitic):
        rows.append(
            {
                "distance_um": float(dist),
                "parasitic_fraction": float(frac),
                "below_threshold": bool(frac <= parasitic_threshold),
                "threshold_fraction": parasitic_threshold,
            }
        )
    return rows


def min_distance_for_threshold(rows, key: str, ok_key: str = "below_threshold"):
    for r in rows:
        if r[ok_key]:
            return float(r[key])
    return None
