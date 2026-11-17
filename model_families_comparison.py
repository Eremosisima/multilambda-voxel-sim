#!/usr/bin/env python3
"""Comparative conceptual model for OPGPU optical families/variants.

Estimates response/reconfig times, energy scales, interference capability, and fit.
Outputs under outputs/ and figures/.
"""
from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import List

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

OUT_DIR = "outputs"
FIG_DIR = "figures"


@dataclass
class Family:
    key: str
    name: str
    inference_latency_ps: float      # propagation/modulation limited (order)
    reconfig_time_s: float           # weight/program update time
    energy_per_op_pj: float          # conceptual MAC/op or switch event
    il_db: float                     # typical element/path loss (conceptual)
    nonvolatile: str                 # yes/partial/no
    interference_native: str         # strong/medium/limited
    maturity: str                    # low/medium/high
    best_for: str


def families() -> List[Family]:
    return [
        Family("A1", "Interferometric PCM (ref)", 10, 2e-5, 0.8, 1.0, "yes", "strong", "medium", "Persistent weights, MVM inference"),
        Family("A2", "Interferometric PCM+EO hybrid", 10, 1e-9, 0.9, 1.2, "partial", "strong", "medium", "Fast correction + persistent base"),
        Family("B1", "Resonant BIC/PCM", 50, 5e-6, 0.4, 0.8, "yes", "strong", "medium", "Dense low-energy cells, WDM"),
        Family("C1", "Electro-optic Pockels mesh", 5, 5e-12, 1.5, 1.5, "no", "strong", "medium", "High-rate streaming/dynamic kernels"),
        Family("C2", "EO nonvolatile/ferroelectric", 8, 1e-9, 1.0, 1.3, "partial", "strong", "low", "Fast reconfigurable weights"),
        Family("D1", "Plasmonic/ENZ hybrid", 1, 1e-6, 0.6, 3.0, "depends", "medium", "low", "Compact nonlinear/activation hotspots"),
        Family("E1", "All-optical nonlinear (Kerr/2D)", 0.5, 1e-12, 2.0, 2.5, "no", "medium", "low", "Ultrafast gating/activation"),
        Family("F1", "Diffractive/metasurface", 20, 1e-6, 0.5, 1.5, "depends", "strong", "low", "Massive spatial parallelism"),
    ]


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)
    fams = families()
    rows = [asdict(f) for f in fams]
    for r in rows:
        r["inference_throughput_gops_equiv"] = round(1e3 / r["inference_latency_ps"], 3)  # very rough proxy
        r["reconfig_time_s"] = f"{r['reconfig_time_s']:.1e}"
    # write normalized numeric for plotting from originals
    with open(os.path.join(OUT_DIR, "families_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # numeric summary
    summary = {
        "families": [asdict(f) for f in fams],
        "notes": [
            "Conceptual order-of-magnitude estimates for comparison only; not measured device data.",
            "Inference latency refers to signal propagation/modulation scale; system latency also includes I/O, memory and detection.",
            "Interference-native capability indicates suitability for additive/destructive (coherent) operations.",
            "Reconfiguration time ranges from EO/optical (fast) to PCM thermal programming (slow)."
        ],
        "recommended_path": [
            "A1 as open reference baseline (persistent weights, MVM).",
            "A2/B1 for efficiency/density with interference-native compute.",
            "C1/C2 for fast reload/streaming; D1/E1 for nonlinear/activation blocks; F1 for spatial parallelism."
        ]
    }
    with open(os.path.join(OUT_DIR, "families_comparison.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = [
        "# Families Comparison (Conceptual)",
        "",
        "| Key | Family | Inference (ps) | Reconfig (s) | Energy/op (pJ) | IL (dB) | NV | Interference | Maturity |",
        "|---|---|---:|---:|---:|---:|---|---|---|",
    ]
    for f in fams:
        md.append(f"| {f.key} | {f.name} | {f.inference_latency_ps} | {f.reconfig_time_s:.1e} | {f.energy_per_op_pj} | {f.il_db} | {f.nonvolatile} | {f.interference_native} | {f.maturity} |")
    md += ["", "## Notes"] + [f"- {n}" for n in summary["notes"]] + ["", "## Recommended incremental path"] + [f"- {p}" for p in summary["recommended_path"]]
    with open(os.path.join(OUT_DIR, "families_comparison.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    if plt is not None:
        keys = [f.key for f in fams]
        inf = [f.inference_latency_ps for f in fams]
        recon = [f.reconfig_time_s for f in fams]
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(keys, inf)
        ax.set_yscale('log')
        ax.set_ylabel('Inference/modulation scale (ps, log)')
        ax.set_title('Inference/modulation latency by family (conceptual)')
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, 'families_inference_latency.png'), dpi=150)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(keys, recon)
        ax.set_yscale('log')
        ax.set_ylabel('Reconfiguration time (s, log)')
        ax.set_title('Weight reconfiguration time by family (conceptual)')
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, 'families_reconfig_time.png'), dpi=150)
        plt.close(fig)

        e = [f.energy_per_op_pj for f in fams]
        il = [f.il_db for f in fams]
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        ax.scatter(e, il)
        for f in fams:
            ax.annotate(f.key, (f.energy_per_op_pj, f.il_db))
        ax.set_xlabel('Energy/op (pJ, conceptual)')
        ax.set_ylabel('IL (dB, conceptual)')
        ax.set_title('Energy vs insertion loss by family')
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, 'families_energy_il.png'), dpi=150)
        plt.close(fig)

    print(json.dumps({"families": len(fams), "out": OUT_DIR}, indent=2))


if __name__ == "__main__":
    main()
