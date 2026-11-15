"""Physical phase-noise/SNR budget estimates for MZI readout (order-of-magnitude)."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import numpy as np

from mzi_sim import phase_per_level


def shot_noise_phase_sigma(optical_power_w: float, wavelength_m: float, bandwidth_hz: float, quantum_eff: float = 0.8):
    """Approximate shot-noise-limited phase sensitivity for an interferometric readout.
    sigma_phi ~ 1/sqrt(N_ph) at quadrature, N_ph = eta*P/(h*f*B) photons in measurement.
    This is a simplified estimate (ignores fringe visibility, excess noise, balanced detection details).
    """
    h = 6.62607015e-34
    c = 299792458.0
    f = c / wavelength_m
    n_ph = quantum_eff * optical_power_w / (h * f * bandwidth_hz) if bandwidth_hz > 0 else float("inf")
    sigma = 1.0 / math.sqrt(n_ph) if n_ph > 0 else float("inf")
    return sigma, n_ph


def thermal_phase_drift_sigma(L_m: float, dn_dT: float = 1e-5, dT_rms_k: float = 0.01, wavelength_m: float = 1550e-9, confinement: float = 0.35):
    """Order-of-magnitude thermo-optic phase fluctuation: dphi = (2pi/lambda)*Gamma*(dn/dT)*dT*L."""
    return (2 * math.pi / wavelength_m) * confinement * dn_dT * dT_rms_k * L_m


def budget_table():
    rows_mzi, _ = phase_per_level(L_um=100.0, confinement=0.35)
    bw_cases = [1e3, 1e6, 1e9]  # Hz (slow readout to fast)
    p_cases = [1e-6, 10e-6, 100e-6, 1e-3]  # W
    rows = []
    for r in rows_mzi:
        lam = r["read_nm"] * 1e-9
        step = abs(r["delta_phi_per_level_rad"])
        for P in p_cases:
            for B in bw_cases:
                sigma_shot, nph = shot_noise_phase_sigma(P, lam, B)
                sigma_th = thermal_phase_drift_sigma(100e-6, wavelength_m=lam)
                sigma_total = math.sqrt(sigma_shot**2 + sigma_th**2)
                snr = step / sigma_total if sigma_total > 0 else float("inf")
                margin = (step / 2.0) / sigma_total if sigma_total > 0 else float("inf")  # half-step margin
                rows.append({
                    "material": r["material"],
                    "read_nm": r["read_nm"],
                    "phase_step_rad": step,
                    "optical_power_w": P,
                    "bandwidth_hz": B,
                    "sigma_shot_rad": sigma_shot,
                    "sigma_thermal_rad": sigma_th,
                    "sigma_total_rad": sigma_total,
                    "snr_step_over_sigma": snr,
                    "half_step_margin_sigma": margin,
                    "photons_per_measurement_est": nph,
                })
    return rows


def main(out_dir: Path):
    rows = budget_table()
    with (out_dir / "snr_budget.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # summarize feasible points (e.g. margin >= 3 sigma on half-step)
    feasible = [r for r in rows if r["half_step_margin_sigma"] >= 3.0]
    summary = {
        "total_points": len(rows),
        "feasible_half_step_margin_ge_3sigma": len(feasible),
        "example_feasible": feasible[:10],
        "assumptions": "Simplified shot-noise + thermo-optic drift model; excludes RIN, detector NEP, visibility loss, 1/f, and control noise.",
    }
    (out_dir / "snr_budget_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    main(Path(__file__).resolve().parent / "outputs")
