#!/usr/bin/env python3
"""P2 modeling: reliability, variability, endurance, retention and read noise.

Conceptual/data-backed estimates for OPGPU memory/compute elements (M0-M3).
Outputs under outputs/ and figures/. Assumptions documented in summary JSON/report.
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
class ReliabilityParams:
    levels: int = 32
    phase_range_rad: float = 8.513  # from P1
    read_noise_sigma_rad: float = 0.06  # effective phase noise (shot+thermal+drift, conceptual)
    drift_sigma_rad_per_s: float = 1e-5
    sample_count: int = 20000
    # endurance (cycles to 20% contrast loss, conceptual/literature-informed ranges)
    m1_sb2s3_cycles: float = 1e6
    m2_vo2_cycles: float = 1e7
    m0_spiropyran_cycles: float = 1e4
    m0_azobenzene_cycles: float = 1e5
    # retention (characteristic times, s, conceptual)
    m1_retention_s: float = 1e8
    m2_hold_s: float = 1e-2  # volatile latch/hold scale (requires refresh/bias in practice)
    spiropyran_retention_s: float = 1e5
    azobenzene_retention_s: float = 1e4
    # temperature
    temp_c: float = 45.0


def level_error_rates(p: ReliabilityParams) -> Dict:
    rng = np.random.default_rng(7)
    step = p.phase_range_rad / (p.levels - 1)
    levels = np.arange(p.levels)
    true_phi = levels * step
    # sample each level equally
    samples_per = p.sample_count // p.levels
    true_idx = np.repeat(levels, samples_per)
    phi = true_phi[true_idx] + rng.normal(0.0, p.read_noise_sigma_rad, size=true_idx.size)
    # nearest-level decision
    decided = np.clip(np.rint(phi / step), 0, p.levels - 1).astype(int)
    ser = float(np.mean(decided != true_idx))
    # symbol error within +/-1 level (soft metric)
    within1 = float(np.mean(np.abs(decided - true_idx) <= 1))
    # SNR-like metric: step^2/(12*sigma^2) in amplitude-equivalent terms
    snr_step_db = 20 * math.log10((step / (math.sqrt(12) * max(p.read_noise_sigma_rad, 1e-12))) + 1e-12)
    # effective bits (capacity proxy)
    if ser <= 0 or ser >= 1:
        eff_bits = 0.0 if ser >= 1 else math.log2(p.levels)
    else:
        eff_bits = max(0.0, math.log2(p.levels) * (1 - ser))
    # noise sweep
    sweep = []
    for sigma in [0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.15]:
        ph = true_phi[true_idx] + rng.normal(0.0, sigma, size=true_idx.size)
        dec = np.clip(np.rint(ph / step), 0, p.levels - 1).astype(int)
        s = float(np.mean(dec != true_idx))
        sweep.append({"sigma_rad": sigma, "ser": round(s, 6), "snr_step_db": round(20*math.log10((step/(math.sqrt(12)*sigma))+1e-12),3)})
    return {
        "step_rad": step,
        "ser": round(ser, 6),
        "within1_rate": round(within1, 6),
        "snr_step_db": round(snr_step_db, 3),
        "effective_bits_proxy": round(eff_bits, 4),
        "noise_sweep": sweep,
    }


def endurance_curve(cycles_max: float, knee: float, points: int = 12) -> List[Dict]:
    # Contrast retention model: R(c)=1/(1+(c/knee)^p), p~1-1.5
    p = 1.2
    xs = np.logspace(0, math.log10(max(cycles_max * 5, 10)), points)
    rows = []
    for c in xs:
        r = 1.0 / (1.0 + (c / max(knee, 1.0)) ** p)
        rows.append({"cycles": float(c), "contrast_retention": round(float(r), 6)})
    return rows


def retention_curve(tau_s: float, temp_c: float, points: int = 10) -> List[Dict]:
    # Simple exponential-like retention with mild temperature acceleration proxy
    accel = math.exp(max(temp_c - 25.0, 0.0) / 40.0)
    tau_eff = tau_s / accel
    tmax = max(tau_s * 5, 1.0)
    ts = np.logspace(-3, math.log10(tmax), points)
    rows = []
    for t in ts:
        if tau_eff == float('inf'):
            r = 1.0
        else:
            r = math.exp(-t / max(tau_eff, 1e-12))
        rows.append({"time_s": float(t), "retention_fraction": round(float(min(max(r, 0.0), 1.0)), 6)})
    return rows


def build_endurance_retention(p: ReliabilityParams) -> Dict:
    end = {
        "M1_Sb2S3": endurance_curve(p.m1_sb2s3_cycles * 5, p.m1_sb2s3_cycles),
        "M2_VO2": endurance_curve(p.m2_vo2_cycles * 5, p.m2_vo2_cycles),
        "M0_Spiropyran": endurance_curve(p.m0_spiropyran_cycles * 5, p.m0_spiropyran_cycles),
        "M0_Azobenzene": endurance_curve(p.m0_azobenzene_cycles * 5, p.m0_azobenzene_cycles),
    }
    ret = {
        "M1_Sb2S3": retention_curve(p.m1_retention_s, p.temp_c),
        "M2_VO2_volatile": retention_curve(p.m2_hold_s, p.temp_c),
        "M0_Spiropyran": retention_curve(p.spiropyran_retention_s, p.temp_c),
        "M0_Azobenzene": retention_curve(p.azobenzene_retention_s, p.temp_c),
    }
    return {"endurance": end, "retention": ret}


def write_outputs(p: ReliabilityParams, noise: Dict, er: Dict) -> None:
    with open(os.path.join(OUT_DIR, "reliability_noise_sweep.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(noise["noise_sweep"][0].keys()))
        w.writeheader()
        w.writerows(noise["noise_sweep"])
    # flatten endurance/retention samples
    with open(os.path.join(OUT_DIR, "reliability_endurance_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["component", "cycles", "contrast_retention"])
        for comp, rows in er["endurance"].items():
            for r in rows:
                w.writerow([comp, r["cycles"], r["contrast_retention"]])
    with open(os.path.join(OUT_DIR, "reliability_retention_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["component", "time_s", "retention_fraction"])
        for comp, rows in er["retention"].items():
            for r in rows:
                w.writerow([comp, r["time_s"], r["retention_fraction"]])

    summary = {
        "params": asdict(p),
        "noise": noise,
        "endurance_knee_cycles": {
            "M1_Sb2S3": p.m1_sb2s3_cycles, "M2_VO2": p.m2_vo2_cycles,
            "M0_Spiropyran": p.m0_spiropyran_cycles, "M0_Azobenzene": p.m0_azobenzene_cycles,
        },
        "retention_tau_s": {
            "M1_Sb2S3": p.m1_retention_s, "M2_VO2_volatile": p.m2_hold_s,
            "M0_Spiropyran": p.spiropyran_retention_s, "M0_Azobenzene": p.azobenzene_retention_s,
        },
        "assumptions": [
            "Noise model: Gaussian phase/readout noise mapped to nearest-level decisions over P1 phase range/levels.",
            "Endurance/retention use parametric curves (contrast knee, exponential/accelerated retention) informed by reported trends; not device-measured.",
            "M2 (VO2) treated as volatile/hold element requiring refresh/bias in sustained operation.",
            "Photochromic materials (azobenzene/spiropyran) modeled for lower-frequency config/trim roles with fatigue considerations."
        ],
        "reference_context": [
            "Sb2S3 multilevel/endurance trends (e.g. Nat. Commun. 2023 10.1038/s41467-023-39180-3)",
            "VO2 photonic memory endurance (npj Nanophotonics 2024 10.1038/s44310-024-00038-1)",
            "Nanostructured PCM endurance/loss improvements (arXiv 2604.08637)",
            "Photonic memory/cycling reviews (e.g. MRS Bulletin/Science Bulletin PCM photonics literature)"
        ]
    }
    with open(os.path.join(OUT_DIR, "reliability_p2_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    lines = [
        "# P2 Modeling Report: Reliability (Noise, Endurance, Retention)",
        "",
        f"- Levels: {p.levels}, phase range: {p.phase_range_rad} rad, step: {noise['step_rad']:.6f} rad",
        f"- Read noise sigma: {p.read_noise_sigma_rad} rad -> SER {noise['ser']:.6f}, within±1 {noise['within1_rate']:.6f}, SNR_step {noise['snr_step_db']:.2f} dB, effective bits (proxy) {noise['effective_bits_proxy']:.3f}",
        "",
        "## Endurance knee cycles (conceptual)",
        f"- M1 Sb2S3: {p.m1_sb2s3_cycles:.2e}, M2 VO2: {p.m2_vo2_cycles:.2e}, M0 Spiropyran: {p.m0_spiropyran_cycles:.2e}, M0 Azobenzene: {p.m0_azobenzene_cycles:.2e}",
        "",
        "## Retention characteristic (s, conceptual)",
        f"- M1 Sb2S3: {p.m1_retention_s:.2e}, M2 VO2 volatile hold: {p.m2_hold_s:.2e}, M0 Spiropyran: {p.spiropyran_retention_s:.2e}, M0 Azobenzene: {p.azobenzene_retention_s:.2e}",
        "",
        "## Assumptions",
    ] + [f"- {a}" for a in summary["assumptions"]] + ["", "## Reference context"] + [f"- {r}" for r in summary["reference_context"]]
    with open(os.path.join(OUT_DIR, "reliability_p2_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def plot_outputs(noise: Dict, er: Dict) -> None:
    if plt is None:
        return
    sw = noise["noise_sweep"]
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot([x["sigma_rad"] for x in sw], [x["ser"] for x in sw], marker='o')
    ax.set_xlabel("Read noise sigma (rad)")
    ax.set_ylabel("Symbol error rate (SER)")
    ax.set_title("Multilevel SER vs read noise (P2)")
    ax.set_yscale('log')
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "reliability_ser_vs_noise.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    for comp, rows in er["endurance"].items():
        ax.plot([r["cycles"] for r in rows], [r["contrast_retention"] for r in rows], marker='.', label=comp)
    ax.set_xscale('log')
    ax.set_xlabel("Cycles")
    ax.set_ylabel("Contrast retention")
    ax.set_title("Endurance (conceptual)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "reliability_endurance.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    for comp, rows in er["retention"].items():
        ax.plot([r["time_s"] for r in rows], [r["retention_fraction"] for r in rows], marker='.', label=comp)
    ax.set_xscale('log')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Retention fraction")
    ax.set_title("Retention (conceptual)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "reliability_retention.png"), dpi=150)
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    p = ReliabilityParams()
    noise = level_error_rates(p)
    er = build_endurance_retention(p)
    write_outputs(p, noise, er)
    plot_outputs(noise, er)
    print(json.dumps({"ser": noise["ser"], "effective_bits_proxy": noise["effective_bits_proxy"], "snr_step_db": noise["snr_step_db"]}, indent=2))


if __name__ == "__main__":
    main()
