#!/usr/bin/env python3
"""P3 modeling: spatial variability, 4/5-bit mode selection, and M2 (VO2) refresh policy.

Builds on P1/P2 data to estimate robust operating modes and system overheads.
Outputs under outputs/ and figures/.
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


def ensure_dirs() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


@dataclass
class P3Params:
    phase_range_rad: float = 8.513
    read_noise_sigma_rad: float = 0.06
    spatial_sigma_rad: float = 0.03  # cell-to-cell variability (phase), conceptual
    drift_sigma_rad: float = 0.01    # slow drift/calibration residual
    samples_per_level: int = 800
    m2_hold_s: float = 0.01          # from P2 (VO2 volatile hold)
    m2_refresh_energy_pj: float = 0.5  # per cell refresh, conceptual
    m2_cells_active: int = 1_000_000   # active volatile cells in working set (example)
    ser_target_5b: float = 0.01
    ser_target_4b: float = 0.001


def eval_mode(levels: int, p: P3Params) -> Dict:
    rng = np.random.default_rng(11 if levels == 32 else 17)
    step = p.phase_range_rad / (levels - 1)
    idx = np.arange(levels)
    phi_nom = idx * step
    total_sigma = math.sqrt(p.read_noise_sigma_rad**2 + p.spatial_sigma_rad**2 + p.drift_sigma_rad**2)
    true_idx = np.repeat(idx, p.samples_per_level)
    offsets = rng.normal(0.0, p.spatial_sigma_rad, size=levels)  # fixed spatial per cell/level proxy
    phi = phi_nom[true_idx] + offsets[true_idx] + rng.normal(0.0, math.sqrt(p.read_noise_sigma_rad**2 + p.drift_sigma_rad**2), size=true_idx.size)
    decided = np.clip(np.rint(phi / step), 0, levels - 1).astype(int)
    ser = float(np.mean(decided != true_idx))
    within1 = float(np.mean(np.abs(decided - true_idx) <= 1))
    snr_db = 20 * math.log10((step / (math.sqrt(12) * max(total_sigma, 1e-12))) + 1e-12)
    eff_bits = max(0.0, math.log2(levels) - (-math.log2(max(1-ser, 1e-12))) * 0.15)  # conservative proxy
    return {
        "levels": levels,
        "bits_nominal": int(math.log2(levels)),
        "step_rad": round(step, 6),
        "total_sigma_rad": round(total_sigma, 6),
        "snr_step_db": round(snr_db, 3),
        "ser": round(ser, 6),
        "within1_rate": round(within1, 6),
        "effective_bits_proxy": round(min(eff_bits, math.log2(levels)), 4),
    }


def m2_refresh_policy(p: P3Params) -> Dict:
    # Refresh rate to maintain volatile state; overhead as fraction of a 1ms window example
    refresh_rate_hz = 1.0 / max(p.m2_hold_s, 1e-6)
    window_s = 1e-3
    refreshes_per_window = refresh_rate_hz * window_s
    # assume OMCC pipelines refresh in background with partial overlap
    overhead_fraction = min(0.25, refreshes_per_window * 0.02)  # 2% slot per refresh batch (conceptual)
    energy_per_window_uj = (p.m2_cells_active * p.m2_refresh_energy_pj * refreshes_per_window) / 1e6
    return {
        "m2_hold_s": p.m2_hold_s,
        "refresh_rate_hz": round(refresh_rate_hz, 3),
        "refreshes_per_1ms_window": round(refreshes_per_window, 3),
        "overhead_fraction_est": round(overhead_fraction, 4),
        "energy_per_1ms_window_uj_est": round(energy_per_window_uj, 4),
        "active_cells_example": p.m2_cells_active,
        "policy": "OMCC-scheduled background refresh with batched VO2 hold/restore; prioritize compute windows"
    }


def variability_sweep(p: P3Params) -> List[Dict]:
    rows = []
    for spat in [0.0, 0.02, 0.03, 0.04, 0.06]:
        pp = P3Params(**{**asdict(p), "spatial_sigma_rad": spat})
        r5 = eval_mode(32, pp)
        r4 = eval_mode(16, pp)
        rows.append({
            "spatial_sigma_rad": spat,
            "ser_5b": r5["ser"],
            "ser_4b": r4["ser"],
            "eff_bits_5b": r5["effective_bits_proxy"],
            "eff_bits_4b": r4["effective_bits_proxy"],
        })
    return rows


def write_outputs(p: P3Params, r4: Dict, r5: Dict, refresh: Dict, sweep: List[Dict]) -> None:
    with open(os.path.join(OUT_DIR, "p3_mode_comparison.json"), "w", encoding="utf-8") as f:
        json.dump({"params": asdict(p), "mode_4b": r4, "mode_5b": r5, "m2_refresh": refresh}, f, indent=2)
    with open(os.path.join(OUT_DIR, "p3_variability_sweep.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sweep[0].keys()))
        w.writeheader()
        w.writerows(sweep)

    # Recommendation
    rec = "5b" if r5["ser"] <= p.ser_target_5b else ("4b" if r4["ser"] <= p.ser_target_4b else "4b+ECC/calibration")
    summary = {
        "params": asdict(p),
        "mode_4b": r4,
        "mode_5b": r5,
        "m2_refresh": refresh,
        "variability_sweep": sweep,
        "recommendation": {
            "mode": rec,
            "rationale": "Select highest density meeting SER target under combined read noise, spatial variability, and drift; fall back to 4b or ECC with tighter calibration.",
            "m2_policy": "Background batched refresh scheduled by OMCC; account overhead in sustained pipelines."
        },
        "assumptions": [
            "Spatial variability modeled as per-cell Gaussian phase offset plus read/drift noise.",
            "Effective-bits proxy is conservative (not channel capacity).",
            "M2 refresh modeled as periodic hold maintenance for VO2 volatile state; rates/energy are conceptual.",
            "Targets: SER <= 1% (5b) or <= 0.1% (4b) as design goals."
        ]
    }
    with open(os.path.join(OUT_DIR, "p3_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    lines = [
        "# P3 Modeling Report: Variability, 4/5-bit Modes, and M2 Refresh",
        "",
        f"- Combined sigma (5b/4b context): read {p.read_noise_sigma_rad}, spatial {p.spatial_sigma_rad}, drift {p.drift_sigma_rad} rad",
        f"- 5b: step {r5['step_rad']:.6f} rad, SNR {r5['snr_step_db']:.2f} dB, SER {r5['ser']:.6f}, eff bits {r5['effective_bits_proxy']:.3f}",
        f"- 4b: step {r4['step_rad']:.6f} rad, SNR {r4['snr_step_db']:.2f} dB, SER {r4['ser']:.6f}, eff bits {r4['effective_bits_proxy']:.3f}",
        f"- Recommendation: **{rec}**",
        "",
        "## M2 (VO2) refresh policy (conceptual)",
        f"- Hold {refresh['m2_hold_s']} s, rate {refresh['refresh_rate_hz']} Hz, overhead ~{refresh['overhead_fraction_est']*100:.2f}% per 1ms window, energy ~{refresh['energy_per_1ms_window_uj_est']:.3f} uJ/window (example {refresh['active_cells_example']} cells)",
        f"- Policy: {refresh['policy']}",
        "",
        "## Assumptions",
    ] + [f"- {a}" for a in summary["assumptions"]]
    with open(os.path.join(OUT_DIR, "p3_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    if plt is not None:
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot([x["spatial_sigma_rad"] for x in sweep], [x["ser_5b"] for x in sweep], marker='o', label='5b SER')
        ax.plot([x["spatial_sigma_rad"] for x in sweep], [x["ser_4b"] for x in sweep], marker='o', label='4b SER')
        ax.axhline(p.ser_target_5b, color='tab:blue', ls='--', alpha=0.5, label='5b target')
        ax.axhline(p.ser_target_4b, color='tab:orange', ls='--', alpha=0.5, label='4b target')
        ax.set_xlabel('Spatial sigma (rad)')
        ax.set_ylabel('SER')
        ax.set_yscale('log')
        ax.set_title('SER vs spatial variability (P3)')
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, "p3_variability_ser.png"), dpi=150)
        plt.close(fig)


def main() -> None:
    ensure_dirs()
    p = P3Params()
    r4 = eval_mode(16, p)
    r5 = eval_mode(32, p)
    refresh = m2_refresh_policy(p)
    sweep = variability_sweep(p)
    write_outputs(p, r4, r5, refresh, sweep)
    print(json.dumps({"rec": "5b" if r5["ser"]<=p.ser_target_5b else "4b", "ser5": r5["ser"], "ser4": r4["ser"], "refresh_overhead": refresh["overhead_fraction_est"]}, indent=2))


if __name__ == "__main__":
    main()
