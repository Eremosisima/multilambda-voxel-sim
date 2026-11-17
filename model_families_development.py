#!/usr/bin/env python3
"""Extended development comparison for OPGPU families/variants.

Conceptual, assumption-driven estimates comparing: price/cost, feasibility, speed,
reliability, dimensions, and capacity (compute + memory). Intended for open-hardware
implementers (not measured data).

Outputs: outputs/families_dev_* and figures/families_dev_*.
"""
from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import List, Dict

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

OUT_DIR = "outputs"
FIG_DIR = "figures"


@dataclass
class Variant:
    key: str
    family: str
    name: str
    # Speed
    inference_latency_ps: float
    reconfig_time_s: float
    throughput_tops_tile: float  # conceptual per tile/module scale
    # Reliability
    endurance_cycles: float
    stability_score: int          # 1-5 (5 best) phase/thermal/drift robustness
    lifetime_class: str
    # Dimensions
    cell_um2: float               # effective cell/element area
    tile_mm2: float
    volume_cm3_module: float      # module-scale (incl. 3D brush where applicable)
    density_gops_mm2: float       # conceptual
    # Capacity (compute + memory, conceptual)
    memory_bits_per_cell: float   # effective stored bits/weight levels per element
    memory_capacity_mb_module: float  # effective optical memory/storage per module
    memory_bandwidth_tbps: float  # effective memory/interconnect bandwidth
    # Feasibility
    feasibility_score: int        # 1-5 (5 easiest to realize with available processes)
    integration_complexity: str   # low/medium/high
    platform_examples: str
    # Price (conceptual)
    cost_index: float             # relative (1 = A1 baseline)
    est_nre_usd_k: float          # non-recurring eng/proto (very rough)
    est_unit_cost_usd: float      # at moderate volume, conceptual
    cost_per_tops_usd: float      # conceptual
    # Interference
    interference_mode: str
    notes: str


def variants() -> List[Variant]:
    # Capacity fields: memory_bits_per_cell, memory_capacity_mb_module, memory_bandwidth_tbps (conceptual)
    return [
        Variant("A1", "A", "Interferometric PCM (Ref)", 10, 2e-5, 2.0, 1e6, 3, "media",
                100, 25, 45, 80, 4.0, 64, 0.8, 3, "medium", "SiN/SiPh + Sb2S3/VO2", 1.00, 800, 2500, 1250,
                "MZI coherente + detección balanceada", "Base abierta; pesos NV; reprog. lenta; P1-P3 aplican"),
        Variant("A2", "A", "Interferometric PCM+EO hybrid", 10, 1e-9, 2.5, 1e6, 3, "media",
                120, 28, 50, 89, 4.0, 56, 1.0, 2, "high", "SiN/SiPh + PCM + EO (TFLN/BTO)", 1.45, 1400, 3800, 1520,
                "MZI coherente, ajuste EO rápido", "Pesos gruesos NV + corrección rápida; más drivers"),
        Variant("A3", "A", "Coherent I/Q", 12, 2e-5, 3.0, 1e6, 2, "media",
                140, 30, 50, 100, 5.0, 72, 1.2, 2, "high", "SiPh + PCM + coherente", 1.60, 1600, 4200, 1400,
                "Interferencia compleja I/Q", "Mayor densidad/aritmética compleja; requiere coherencia estricta"),
        Variant("B1", "B", "Resonant BIC/PCM", 40, 5e-6, 1.8, 5e5, 3, "media",
                25, 12, 30, 150, 4.0, 96, 0.6, 2, "high", "SiN + BIC + PCM", 1.20, 1200, 3200, 1778,
                "Fano/interferencia resonante", "Alta densidad/eficiencia; sensible a fab/temperatura"),
        Variant("B3", "B", "Resonant WDM bank", 30, 1e-6, 4.0, 5e6, 3, "media-alta",
                40, 18, 35, 222, 4.0, 128, 2.5, 3, "medium", "SiPh microrings + actuador", 1.30, 1100, 3500, 875,
                "Interferencia resonante + suma WDM", "Paralelismo espectral; calibración por canal"),
        Variant("C1", "C", "Electro-optic Pockels (RT)", 5, 5e-12, 3.5, 1e12, 4, "alta",
                300, 35, 40, 100, 1.0, 8, 3.0, 2, "high", "TFLN/BTO/EO polímero", 2.10, 2200, 6500, 1857,
                "MZI/ring EO (constructiva/destructiva)", "Muy rápido y reconfigurable; sin pesos NV intrínsecos (buffer)"),
        Variant("C2", "C", "EO nonvolatile/ferroelectric", 8, 1e-9, 3.0, 1e9, 4, "alta",
                200, 30, 40, 100, 2.0, 32, 2.0, 1, "high", "PZT/BTO ferroeléctrico integrado", 1.90, 2500, 7000, 2333,
                "MZI EO con retención", "Rápido + retención; madurez de integración baja-media"),
        Variant("D1", "D", "Plasmonic/ENZ hybrid", 1, 1e-6, 1.2, 1e5, 2, "baja-media",
                4, 8, 20, 150, 2.0, 24, 0.5, 1, "high", "Metal/TCO-ENZ + dieléctrico", 1.70, 1800, 5000, 4167,
                "Interferencia local/plasmónica", "Muy compacto y no lineal; pérdidas óhmicas altas; capacidad limitada"),
        Variant("E1", "E", "All-optical nonlinear (Kerr/2D)", 0.5, 1e-12, 1.0, 1e10, 2, "media",
                20, 15, 25, 67, 1.0, 12, 1.5, 1, "high", "SiN/SOI + TMD/2D", 1.80, 2000, 5500, 5500,
                "Umbral/interferencia no lineal", "Ultrarrápido; requiere potencia óptica; capacidad de estado baja"),
        Variant("F1", "F", "Diffractive/metasurface", 20, 1e-6, 5.0, 1e7, 3, "media",
                16, 20, 60, 250, 3.0, 80, 1.8, 2, "high", "Metasuperficie + actuador", 1.50, 1500, 4500, 900,
                "Suma/interferencia en campo", "Alto paralelismo espacial; alineación crítica"),
        Variant("A1-3D", "A+3D", "OPGPU-Ref 3D Brush (A1)", 15, 2e-5, 8.0, 1e6, 3, "media",
                100, 900, 120, 9, 4.0, 512, 2.0, 2, "high", "SiN 3D + PCM + cepillo", 2.40, 3000, 9000, 1125,
                "MZI + distribución 3D por cerdas", "Escala volumétrica; alta capacidad/memoria; packaging complejo"),
        Variant("C1-B", "C+B", "RT EO + WDM resonant", 5, 5e-12, 6.0, 1e10, 3, "media-alta",
                80, 40, 45, 150, 2.0, 48, 4.0, 1, "high", "TFLN + microrings", 2.60, 2800, 8500, 1417,
                "Interferencia EO + resonante/WDM", "Combina velocidad y paralelismo espectral; capacidad NV moderada"),
    ]


def score_reliability(v: Variant) -> float:
    e = math.log10(max(v.endurance_cycles, 1))
    e_n = min(max((e - 4) / 8, 0), 1)  # 1e4->0, 1e12->1
    return round((v.stability_score / 5) * 0.5 + e_n * 0.5, 3)


def score_speed(v: Variant) -> float:
    # combine fast inference and fast reconfig
    inf = 1 / (1 + math.log10(max(v.inference_latency_ps, 0.1)))
    rec = 1 / (1 + math.log10(max(v.reconfig_time_s * 1e12, 1)))  # normalize to ps
    return round(inf * 0.5 + rec * 0.5, 3)


def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def write_outputs(vars_: List[Variant]) -> List[Dict]:
    rows = []
    for v in vars_:
        d = asdict(v)
        d["reliability_index"] = score_reliability(v)
        d["speed_index"] = score_speed(v)
        d["feasibility_norm"] = round(v.feasibility_score / 5, 3)
        d["price_norm_low_better"] = round(1 / v.cost_index, 3)
        d["dimension_compactness"] = round(1 / (1 + math.log10(max(v.tile_mm2, 1))), 3)
        rows.append(d)

    # Capacity normalization (relative to max in this conceptual set)
    max_tops = max(r["throughput_tops_tile"] for r in rows) or 1.0
    max_mem = max(r["memory_capacity_mb_module"] for r in rows) or 1.0
    max_bw = max(r["memory_bandwidth_tbps"] for r in rows) or 1.0
    for r in rows:
        r["capacity_compute_norm"] = round(r["throughput_tops_tile"] / max_tops, 3)
        r["capacity_memory_norm"] = round(r["memory_capacity_mb_module"] / max_mem, 3)
        r["capacity_bandwidth_norm"] = round(r["memory_bandwidth_tbps"] / max_bw, 3)
        r["capacity_index"] = round(
            0.5 * r["capacity_compute_norm"]
            + 0.35 * r["capacity_memory_norm"]
            + 0.15 * r["capacity_bandwidth_norm"],
            3,
        )

    csv_fields = list(rows[0].keys())
    with open(os.path.join(OUT_DIR, "families_dev_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=csv_fields)
        w.writeheader()
        w.writerows(rows)

    # Rankings by axis (best first)
    def rank(key, rev=True):
        return [r["key"] for r in sorted(rows, key=lambda x: x[key], reverse=rev)]

    summary = {
        "axes": ["price", "feasibility", "speed", "reliability", "dimensions", "capacity"],
        "rankings": {
            "price_low_cost": rank("price_norm_low_better", True),
            "feasibility": rank("feasibility_norm", True),
            "speed": rank("speed_index", True),
            "reliability": rank("reliability_index", True),
            "compactness": rank("dimension_compactness", True),
            "capacity": rank("capacity_index", True),
            "capacity_compute": rank("capacity_compute_norm", True),
            "capacity_memory": rank("capacity_memory_norm", True),
        },
        "recommended_by_priority": {
            "lowest_price_accessible": rank("price_norm_low_better", True)[:5],
            "highest_feasibility": rank("feasibility_norm", True)[:5],
            "highest_speed": rank("speed_index", True)[:5],
            "highest_reliability": rank("reliability_index", True)[:5],
            "smallest_footprint": rank("dimension_compactness", True)[:5],
            "highest_capacity": rank("capacity_index", True)[:5],
        },
        "notes": [
            "All values are conceptual, order-of-magnitude estimates for open-hardware comparison; not quotes or measured data.",
            "Price/cost depends strongly on volume, yield, packaging, laser/detector sourcing, and process node.",
            "Reliability index combines endurance (log) and stability score; real lifetime requires qualification.",
            "Dimensions compare module/tile scale; 3D brush trades area for volumetric density.",
            "Capacity combines compute throughput (TOPS/tile), effective optical memory/storage (MB/module) and memory bandwidth (TB/s), normalized within this set.",
            "Feasibility reflects availability of platforms/processes and integration complexity for implementers."
        ],
        "variants": rows,
    }
    with open(os.path.join(OUT_DIR, "families_dev_comparison.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Markdown report
    lines = [
        "# Family Development Comparison (Price, Feasibility, Speed, Reliability, Dimensions, Capacity)",
        "",
        "> Conceptual estimates for implementers. Not measured data, not pricing quotes.",
        "",
        "## Summary table",
        "",
        "| Key | Variant | Inf (ps) | Reconf (s) | TOPS/tile | Mem (MB) | BW (TB/s) | Endurance | Stab | Feas | Tile mm² | Vol cm³ | Cost idx | Unit $ (est) | $/TOPS (est) | Rel idx | Spd idx | Cap idx |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        v = next(x for x in vars_ if x.key == r["key"])
        lines.append(
            f"| {r['key']} | {r['name']} | {v.inference_latency_ps} | {v.reconfig_time_s:.0e} | "
            f"{v.throughput_tops_tile} | {v.memory_capacity_mb_module} | {v.memory_bandwidth_tbps} | "
            f"{v.endurance_cycles:.0e} | {v.stability_score}/5 | {v.feasibility_score}/5 | {v.tile_mm2} | {v.volume_cm3_module} | "
            f"{v.cost_index:.2f} | {v.est_unit_cost_usd:.0f} | {v.cost_per_tops_usd:.0f} | {r['reliability_index']} | {r['speed_index']} | {r['capacity_index']} |"
        )

    lines += ["", "## Rankings (best → worst)", ""]
    for k, v in summary["rankings"].items():
        lines.append(f"- **{k}:** {', '.join(v)}")

    lines += ["", "## Recommended by priority", ""]
    for k, v in summary["recommended_by_priority"].items():
        lines.append(f"- **{k}:** {', '.join(v)}")

    lines += ["", "## Notes", ""] + [f"- {n}" for n in summary["notes"]]
    with open(os.path.join(OUT_DIR, "families_dev_comparison.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return rows


def plot(rows: List[Dict]):
    if plt is None:
        return
    keys = [r["key"] for r in rows]

    # Radar-like bar groups for normalized axes
    metrics = [
        ("price_norm_low_better", "Price (lower cost)"),
        ("feasibility_norm", "Feasibility"),
        ("speed_index", "Speed"),
        ("reliability_index", "Reliability"),
        ("dimension_compactness", "Compactness"),
        ("capacity_index", "Capacity"),
    ]
    x = np.arange(len(keys))
    width = 0.13
    fig, ax = plt.subplots(figsize=(15, 5))
    for i, (m, label) in enumerate(metrics):
        ax.bar(x + i*width, [r[m] for r in rows], width, label=label)
    ax.set_xticks(x + width*2.5)
    ax.set_xticklabels(keys, rotation=30)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Normalized score (higher better)")
    ax.set_title("OPGPU families/variants: multi-axis comparison (conceptual)")
    ax.legend(ncol=3, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "families_dev_axes.png"), dpi=150)
    plt.close(fig)

    # Speed vs cost
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter([r["speed_index"] for r in rows], [r["cost_index"] for r in rows])
    for r in rows:
        ax.annotate(r["key"], (r["speed_index"], r["cost_index"]))
    ax.set_xlabel("Speed index (higher better)")
    ax.set_ylabel("Cost index (lower better)")
    ax.set_title("Speed vs cost (conceptual)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "families_dev_speed_cost.png"), dpi=150)
    plt.close(fig)

    # Reliability vs feasibility
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter([r["feasibility_norm"] for r in rows], [r["reliability_index"] for r in rows])
    for r in rows:
        ax.annotate(r["key"], (r["feasibility_norm"], r["reliability_index"]))
    ax.set_xlabel("Feasibility (higher better)")
    ax.set_ylabel("Reliability index (higher better)")
    ax.set_title("Reliability vs feasibility (conceptual)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "families_dev_reliability_feasibility.png"), dpi=150)
    plt.close(fig)

    # Capacity vs speed
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter([r["speed_index"] for r in rows], [r["capacity_index"] for r in rows])
    for r in rows:
        ax.annotate(r["key"], (r["speed_index"], r["capacity_index"]))
    ax.set_xlabel("Speed index (higher better)")
    ax.set_ylabel("Capacity index (higher better)")
    ax.set_title("Capacity vs speed (conceptual)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "families_dev_capacity_speed.png"), dpi=150)
    plt.close(fig)


def main():
    ensure_dirs()
    vars_ = variants()
    rows = write_outputs(vars_)
    plot(rows)
    print(json.dumps({"variants": len(vars_), "out": OUT_DIR}, indent=2))


if __name__ == "__main__":
    main()
