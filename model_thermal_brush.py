#!/usr/bin/env python3
"""P1 modeling: transient thermal/crosstalk estimate for brush-extruded array.

Lumped radial+axial thermal diffusion approximation (finite-difference in radius) to
estimate peak temperatures during Sb2S3 programming (300C target) and VO2 operation
(68C threshold) at neighboring voxels/cerdas. Conceptual, assumption-driven.

Outputs under outputs/ and figures/.
"""
from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None

OUT_DIR = "outputs"
FIG_DIR = "figures"


@dataclass
class ThermalParams:
    # geometry (um)
    pitch_um: float = 10.0
    bristle_radius_um: float = 1.5
    voxel_length_um: float = 5.0
    z_sep_um: float = 8.0  # axial separation between Sb2S3 and VO2 segments
    # thermal properties (effective medium approximations)
    k_w_mk: float = 1.4      # W/mK (SiN/polymer/oxide composite effective)
    rho_kg_m3: float = 2600.0
    cp_j_kgk: float = 700.0
    h_w_m2k: float = 2.0e4   # effective heat extraction to substrate/ambient path
    t_ambient_c: float = 25.0
    # thresholds
    t_vo2_c: float = 68.0
    t_sb2s3_c: float = 300.0
    # pulse scenarios
    sb2s3_pulse_us: float = 2.0
    sb2s3_peak_c: float = 320.0
    vo2_pulse_us: float = 0.5
    vo2_peak_c: float = 85.0
    # simulation
    r_max_um: float = 40.0
    nr: int = 80
    dt_ns: float = 5.0
    t_total_us: float = 30.0


def ensure_dirs() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def simulate_pulse(p: ThermalParams, peak_c: float, pulse_us: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Radial 1D heat equation: dT/dt = alpha*(d2T/dr2 + 1/r dT/dr) - beta*(T-Tamb) + S(t,r).
    Source applied in bristle core during pulse to reach nominal peak scale.
    """
    r_um = np.linspace(0.5, p.r_max_um, p.nr)
    r = r_um * 1e-6
    dr = r[1] - r[0]
    alpha = p.k_w_mk / (p.rho_kg_m3 * p.cp_j_kgk)
    beta = p.h_w_m2k / (p.rho_kg_m3 * p.cp_j_kgk * (p.voxel_length_um * 1e-6))  # lumped axial extraction
    dt = p.dt_ns * 1e-9
    steps = int((p.t_total_us * 1e-6) / dt)
    T = np.full(p.nr, p.t_ambient_c, dtype=float)
    times_us = np.arange(steps) * dt * 1e6

    # Source strength calibrated to approximate target peak in core (simple proportional control)
    target_rise = peak_c - p.t_ambient_c
    S0 = target_rise / max(pulse_us * 1e-6, dt) * 2.6  # heuristic scaling (tuned for nominal peak)
    core = r_um <= p.bristle_radius_um

    peak_trace = np.zeros(steps)
    neighbor_idx = np.argmin(np.abs(r_um - p.pitch_um))
    neighbor_trace = np.zeros(steps)
    far_idx = np.argmin(np.abs(r_um - 2 * p.pitch_um))
    far_trace = np.zeros(steps)

    for i in range(steps):
        t_us = times_us[i]
        S = np.zeros_like(T)
        if t_us <= pulse_us:
            S[core] = S0
        Tn = T.copy()
        # interior
        for j in range(1, p.nr - 1):
            d2 = (T[j + 1] - 2 * T[j] + T[j - 1]) / (dr * dr)
            d1 = (T[j + 1] - T[j - 1]) / (2 * dr * r[j])
            Tn[j] = T[j] + dt * (alpha * (d2 + d1) - beta * (T[j] - p.t_ambient_c) + S[j])
        # boundaries: Neumann at center-ish, Dirichlet ambient at far edge
        Tn[0] = Tn[1]
        Tn[-1] = p.t_ambient_c
        T = Tn
        peak_trace[i] = T[0]
        neighbor_trace[i] = T[neighbor_idx]
        far_trace[i] = T[far_idx]
    return times_us, r_um, np.vstack([peak_trace, neighbor_trace, far_trace])


def analyze(p: ThermalParams) -> Dict:
    t1, r, tr_sb = simulate_pulse(p, p.sb2s3_peak_c, p.sb2s3_pulse_us)
    t2, _, tr_vo = simulate_pulse(p, p.vo2_peak_c, p.vo2_pulse_us)

    sb_core_peak = float(np.max(tr_sb[0]))
    sb_neighbor_peak = float(np.max(tr_sb[1]))
    sb_far_peak = float(np.max(tr_sb[2]))
    vo_core_peak = float(np.max(tr_vo[0]))
    vo_neighbor_peak = float(np.max(tr_vo[1]))

    # axial attenuation estimate from separation (exponential decay approximation)
    axial_atten = math.exp(-p.z_sep_um / max(p.voxel_length_um, 1e-6))
    sb_at_vo2_segment = p.t_ambient_c + (sb_neighbor_peak - p.t_ambient_c) * axial_atten

    results = {
        "params": asdict(p),
        "sb2s3_core_peak_c": round(sb_core_peak, 3),
        "sb2s3_neighbor_pitch_peak_c": round(sb_neighbor_peak, 3),
        "sb2s3_far_peak_c": round(sb_far_peak, 3),
        "vo2_core_peak_c": round(vo_core_peak, 3),
        "vo2_neighbor_pitch_peak_c": round(vo_neighbor_peak, 3),
        "axial_atten_factor_est": round(axial_atten, 6),
        "sb2s3_heat_at_adjacent_vo2_segment_c_est": round(sb_at_vo2_segment, 3),
        "vo2_disturb_margin_c": round(p.t_vo2_c - sb_at_vo2_segment, 3),
        "safe_pitch_for_vo2_um_est": p.pitch_um if sb_at_vo2_segment < p.t_vo2_c else p.pitch_um * 1.5,
        "assumptions": [
            "1D radial finite-difference with lumped axial extraction; effective homogenized properties.",
            "Source calibrated heuristically to reach nominal peak in core; absolute values require FEM calibration.",
            "Axial coupling estimated via exponential attenuation over z_sep_um as first-order isolation proxy.",
            "Thresholds: VO2 68C, Sb2S3 programming ~300C (project spec)."
        ]
    }
    traces = {
        "time_us": t1.tolist(),
        "sb2s3_core_c": tr_sb[0].tolist(),
        "sb2s3_neighbor_c": tr_sb[1].tolist(),
        "sb2s3_far_c": tr_sb[2].tolist(),
        "vo2_core_c": tr_vo[0].tolist(),
        "vo2_neighbor_c": tr_vo[1].tolist(),
    }
    return results, traces


def write_outputs(results: Dict, traces: Dict) -> None:
    with open(os.path.join(OUT_DIR, "thermal_brush_summary.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(OUT_DIR, "thermal_brush_traces.csv"), "w", newline="", encoding="utf-8") as f:
        keys = list(traces.keys())
        w = csv.writer(f)
        w.writerow(keys)
        for i in range(len(traces["time_us"])):
            w.writerow([traces[k][i] for k in keys])

    # sweep pitch
    p0 = ThermalParams()
    sweep = []
    for pitch in [6, 8, 10, 12, 16, 20]:
        p = ThermalParams(pitch_um=float(pitch))
        res, _ = analyze(p)
        sweep.append({
            "pitch_um": pitch,
            "sb2s3_neighbor_pitch_peak_c": res["sb2s3_neighbor_pitch_peak_c"],
            "sb2s3_heat_at_adjacent_vo2_segment_c_est": res["sb2s3_heat_at_adjacent_vo2_segment_c_est"],
            "vo2_disturb_margin_c": res["vo2_disturb_margin_c"],
        })
    with open(os.path.join(OUT_DIR, "thermal_brush_pitch_sweep.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sweep[0].keys()))
        w.writeheader()
        w.writerows(sweep)

    lines = [
        "# P1 Modeling Report: Thermal Transient and Crosstalk (Brush Array)",
        "",
        f"- Nominal: pitch={p0.pitch_um} µm, z_sep={p0.z_sep_um} µm, Sb2S3 pulse={p0.sb2s3_pulse_us} µs (target {p0.sb2s3_peak_c}°C), VO2 pulse={p0.vo2_pulse_us} µs (target {p0.vo2_peak_c}°C)",
        f"- Sb2S3 core/neighbor/far peaks: {results['sb2s3_core_peak_c']:.2f} / {results['sb2s3_neighbor_pitch_peak_c']:.2f} / {results['sb2s3_far_peak_c']:.2f} °C",
        f"- Estimated heat at adjacent VO2 segment (axial atten.): {results['sb2s3_heat_at_adjacent_vo2_segment_c_est']:.2f} °C (VO2 threshold 68°C, margin {results['vo2_disturb_margin_c']:.2f} °C)",
        f"- VO2 core/neighbor peaks: {results['vo2_core_peak_c']:.2f} / {results['vo2_neighbor_pitch_peak_c']:.2f} °C",
        "",
        "## Assumptions",
    ] + [f"- {a}" for a in results["assumptions"]] + [
        "",
        "## Pitch sweep (see thermal_brush_pitch_sweep.csv)",
        "- Increasing pitch and z-separation reduces lateral/axial crosstalk; values guide isolation margins and scheduling.",
    ]
    with open(os.path.join(OUT_DIR, "thermal_brush_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def plot_outputs(results: Dict, traces: Dict) -> None:
    if plt is None:
        return
    t = np.array(traces["time_us"])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t, traces["sb2s3_core_c"], label="Sb2S3 core")
    ax.plot(t, traces["sb2s3_neighbor_c"], label="Neighbor @pitch")
    ax.plot(t, traces["sb2s3_far_c"], label="Far @2*pitch")
    ax.axhline(68, color='orange', ls='--', label='VO2 threshold 68C')
    ax.axhline(300, color='red', ls=':', label='Sb2S3 target 300C')
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Transient thermal response (Sb2S3 programming pulse)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "thermal_brush_sb2s3.png"), dpi=150)
    plt.close(fig)

    # pitch sweep
    try:
        with open(os.path.join(OUT_DIR, "thermal_brush_pitch_sweep.csv"), "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        pitch = [float(r["pitch_um"]) for r in rows]
        heat = [float(r["sb2s3_heat_at_adjacent_vo2_segment_c_est"]) for r in rows]
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(pitch, heat, marker='o', label='Heat at adjacent VO2 segment (est.)')
        ax.axhline(68, color='orange', ls='--', label='VO2 threshold')
        ax.set_xlabel("Pitch (µm)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Crosstalk vs pitch (P1 estimate)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, "thermal_brush_pitch_sweep.png"), dpi=150)
        plt.close(fig)
    except Exception:
        pass


def main() -> None:
    ensure_dirs()
    p = ThermalParams()
    results, traces = analyze(p)
    write_outputs(results, traces)
    # reload traces for plot if needed (already have)
    plot_outputs(results, traces)
    print(json.dumps({"sb2s3_core_peak_c": results["sb2s3_core_peak_c"], "vo2_disturb_margin_c": results["vo2_disturb_margin_c"]}, indent=2))


if __name__ == "__main__":
    main()
