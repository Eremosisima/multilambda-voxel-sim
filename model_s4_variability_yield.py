#!/usr/bin/env python3
"""
S4: Monte Carlo process-variability and yield simulation for prioritized candidates.
Focus on H3 and G3 (2.5D, nearer-term) with comparative notes for H1/H4 (3D).
Conceptual, parametric (no measurements).
"""
from __future__ import annotations

import csv
import json
import math
import os
import random

OUT = "outputs"
FIG = "figures"
random.seed(42)

N_SAMPLES = 2000

# Nominal parameters and relative 3-sigma process variations (conceptual)
PROCESS = {
    "n_sigma": 0.01,       # refractive index
    "d_sigma": 0.02,       # thickness/geometry
    "coupling_sigma": 0.03,
    "phase_sigma": 0.04,   # rad-equivalent fractional
    "thermal_sigma": 0.05,
    "loss_sigma_db": 0.5,  # dB extra
}

CANDS = {
    "H3": {
        "name": "Open WDM-PCM (A1+G1+B3)",
        "base_snr_db": 14.0,
        "base_phase_err": 0.05,
        "base_il_db": 12.0,
        "elements": 120,
        "dimensionality": "2.5D",
        "ecc_overhead": 0.08,
        "redundancy": 0.10,
        "calibration_eff": 0.65,  # fraction of static error correctable
        "thermal_sensitivity": 0.7,
    },
    "G3": {
        "name": "Thin-film membrane stack (PCM+EO hybrid)",
        "base_snr_db": 15.5,
        "base_phase_err": 0.04,
        "base_il_db": 9.5,
        "elements": 90,
        "dimensionality": "2.5D",
        "ecc_overhead": 0.07,
        "redundancy": 0.08,
        "calibration_eff": 0.72,
        "thermal_sensitivity": 0.85,
    },
    "H1": {
        "name": "Membrane-Brush NV (A1+G3+3D)",
        "base_snr_db": 12.5,
        "base_phase_err": 0.06,
        "base_il_db": 14.5,
        "elements": 220,
        "dimensionality": "3D",
        "ecc_overhead": 0.12,
        "redundancy": 0.15,
        "calibration_eff": 0.55,
        "thermal_sensitivity": 1.0,
    },
    "H4": {
        "name": "Volumetric Tensor Membrane (G2/G3+F2+A1)",
        "base_snr_db": 11.8,
        "base_phase_err": 0.07,
        "base_il_db": 15.8,
        "elements": 260,
        "dimensionality": "3D",
        "ecc_overhead": 0.14,
        "redundancy": 0.18,
        "calibration_eff": 0.50,
        "thermal_sensitivity": 1.1,
    },
}

# Pass criteria (conceptual)
CRITERIA = {"snr_db_min": 8.0, "phase_err_max": 0.12, "il_db_max": 18.0}


def sample_sigma(s):
    # normal approx via Box-Muller, scaled so 3*sigma ~ s
    u1 = max(random.random(), 1e-12)
    u2 = random.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return z * (s / 3.0)


def run_mc(key, spec):
    passes = 0
    snrs = []
    pes = []
    ils = []
    for _ in range(N_SAMPLES):
        n_v = sample_sigma(PROCESS["n_sigma"])
        d_v = sample_sigma(PROCESS["d_sigma"])
        c_v = sample_sigma(PROCESS["coupling_sigma"])
        p_v = sample_sigma(PROCESS["phase_sigma"])
        t_v = sample_sigma(PROCESS["thermal_sigma"])
        l_v = sample_sigma(PROCESS["loss_sigma_db"]) * 3.0  # already sigma-like
        # aggregate static errors, partially calibratable
        static = abs(n_v) + abs(d_v) + abs(c_v) + abs(p_v)
        resid = static * (1.0 - spec["calibration_eff"]) + abs(t_v) * spec["thermal_sensitivity"]
        # element count amplifies variability (sqrt for uncorrelated, plus correlation term)
        scale = math.sqrt(spec["elements"] / 100.0) * (1.15 if spec["dimensionality"] == "3D" else 1.0)
        snr = spec["base_snr_db"] - (resid * 18.0 * scale) - abs(l_v)
        pe = spec["base_phase_err"] + resid * 0.8 * scale
        il = spec["base_il_db"] + abs(l_v) + resid * 6.0 * scale
        ok = (snr >= CRITERIA["snr_db_min"] and pe <= CRITERIA["phase_err_max"] and il <= CRITERIA["il_db_max"])
        if ok:
            passes += 1
        snrs.append(snr); pes.append(pe); ils.append(il)

    def stats(arr):
        arrs = sorted(arr)
        m = sum(arr) / len(arr)
        idx5 = int(0.05 * len(arrs)); idx95 = int(0.95 * len(arrs)) - 1
        return {"mean": round(m, 4), "p5": round(arrs[idx5], 4), "p95": round(arrs[idx95], 4)}

    raw_yield = passes / N_SAMPLES
    effective_yield = raw_yield * (1.0 - spec["redundancy"])  # overhead cost proxy
    return {
        "key": key,
        "name": spec["name"],
        "dimensionality": spec["dimensionality"],
        "samples": N_SAMPLES,
        "raw_yield": round(raw_yield, 4),
        "effective_yield_after_redundancy": round(effective_yield, 4),
        "redundancy_overhead": spec["redundancy"],
        "ecc_overhead": spec["ecc_overhead"],
        "calibration_efficiency": spec["calibration_eff"],
        "snr_db": stats(snrs),
        "phase_error": stats(pes),
        "insertion_loss_db": stats(ils),
        "criteria": CRITERIA,
        "meets_yield_target_0_7": raw_yield >= 0.7,
        "meets_yield_target_0_85": raw_yield >= 0.85,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    results = [run_mc(k, v) for k, v in CANDS.items()]

    summary = {
        "assumptions": {
            "process_3sigma": PROCESS,
            "samples": N_SAMPLES,
            "criteria": CRITERIA,
            "note": "Static errors partially correctable by calibration; 3D candidates modeled with higher element count/correlation and lower calibration efficiency."
        },
        "results": results,
        "disclaimer": "Conceptual Monte Carlo S4 model; calibrate distributions with foundry/process metrology and measured device statistics.",
    }
    with open(os.path.join(OUT, "s4_variability_yield.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    csv_rows = []
    for r in results:
        csv_rows.append({
            "key": r["key"], "name": r["name"], "dimensionality": r["dimensionality"],
            "raw_yield": r["raw_yield"], "effective_yield_after_redundancy": r["effective_yield_after_redundancy"],
            "snr_mean_db": r["snr_db"]["mean"], "snr_p5_db": r["snr_db"]["p5"],
            "phase_err_mean": r["phase_error"]["mean"], "phase_err_p95": r["phase_error"]["p95"],
            "il_mean_db": r["insertion_loss_db"]["mean"], "il_p95_db": r["insertion_loss_db"]["p95"],
            "redundancy_overhead": r["redundancy_overhead"], "ecc_overhead": r["ecc_overhead"],
            "meets_yield_target_0_7": r["meets_yield_target_0_7"], "meets_yield_target_0_85": r["meets_yield_target_0_85"],
        })
    with open(os.path.join(OUT, "s4_variability_yield.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)

    md = ["# S4 — Variabilidad de proceso y yield (Monte Carlo, conceptual)", "",
          f"> {N_SAMPLES} muestras por candidato. No son mediciones; calibrar con metrología/proceso y estadísticas de dispositivos.", "",
          "## Resultados", "",
          "| Candidato | Dim. | Yield bruto | Yield efectivo (tras redundancia) | SNR medio (dB) | SNR p5 (dB) | Error fase medio | Error fase p95 | IL medio (dB) | IL p95 (dB) | >=70% | >=85% |",
          "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|"]
    for r in results:
        md.append(f"| {r['key']} | {r['dimensionality']} | {r['raw_yield']} | {r['effective_yield_after_redundancy']} | {r['snr_db']['mean']} | {r['snr_db']['p5']} | {r['phase_error']['mean']} | {r['phase_error']['p95']} | {r['insertion_loss_db']['mean']} | {r['insertion_loss_db']['p95']} | {'sí' if r['meets_yield_target_0_7'] else 'no'} | {'sí' if r['meets_yield_target_0_85'] else 'no'} |")
    md += ["", "## Lectura", "- H3/G3 (2.5D) muestran mejor robustez relativa bajo supuestos de calibración y menor correlación 3D; H1/H4 (3D) requieren mayor redundancia/calibración y control de proceso.",
           "- El yield efectivo descuenta overhead de redundancia; ECC y calibración en OMCC son necesarios para acercarse a objetivos de prototipo.",
           "## Acciones", "- Obtener distribuciones reales (σ de n, d, acoplo, pérdida, térmica) por proceso/fundición.", "- Optimizar particionado modular para contener fallos y permitir reparación/re-mapeo (OMCC).", "- Endurecer calibración en lazo cerrado y pruebas de RAS en S4→E2."]
    with open(os.path.join(OUT, "s4_variability_yield.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        keys = [r["key"] for r in results]
        fig, ax = plt.subplots(figsize=(7, 4))
        raw = [r["raw_yield"] for r in results]
        eff = [r["effective_yield_after_redundancy"] for r in results]
        x = range(len(keys))
        ax.bar([i - 0.15 for i in x], raw, width=0.3, label="Yield bruto")
        ax.bar([i + 0.15 for i in x], eff, width=0.3, label="Yield efectivo (tras redundancia)")
        ax.axhline(0.7, color="orange", ls="--", lw=1, label="objetivo 70%")
        ax.axhline(0.85, color="green", ls="--", lw=1, label="objetivo 85%")
        ax.set_xticks(list(x)); ax.set_xticklabels(keys)
        ax.set_ylim(0, 1.05); ax.set_ylabel("Yield")
        ax.set_title("S4: Yield simulado por variabilidad de proceso")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "s4_variability_yield.png"), dpi=150)
        plt.close(fig)
    except Exception as e:
        print("figure_warning:", e)

    print(json.dumps({"candidates": len(results), "samples": N_SAMPLES, "out": "outputs/s4_variability_yield.*"}))


if __name__ == "__main__":
    main()
