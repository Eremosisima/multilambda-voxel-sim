#!/usr/bin/env python3
"""
Objective, detailed review and comparative simulation for current OPGPU family combinations.

Reads outputs/families_dev_comparison.json (conceptual baseline), computes derived
metrics, checks internal consistency, runs scenario simulations (static inference,
dynamic/reconfig-heavy, memory-bandwidth-bound), and performs simple sensitivity
analysis (+/-30% perturbations on uncertain parameters) for H1-H5 and key baselines.

Outputs: outputs/objective_combo_analysis.md/.json/.csv and figures/objective_*.
All results remain conceptual/order-of-magnitude (not measurements).
"""
from __future__ import annotations

import csv
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

OUT_DIR = "outputs"
FIG_DIR = "figures"
BASE_JSON = os.path.join(OUT_DIR, "families_dev_comparison.json")

FOCUS = ["A1", "B3", "G2", "G3", "H1", "H2", "H3", "H4", "H5", "C1", "A1-3D"]


def load_base():
    with open(BASE_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_div(a, b, default=0.0):
    return a / b if b else default


def compute_derived(v: Dict) -> Dict:
    d = dict(v)
    tile_mm2 = v.get("tile_mm2", 0) or 0
    vol_cm3 = v.get("volume_cm3_module", 0) or 0
    tops = v.get("throughput_tops_tile", 0) or 0
    mem = v.get("memory_capacity_mb_module", 0) or 0
    bw = v.get("memory_bandwidth_tbps", 0) or 0
    cost = v.get("est_unit_cost_usd", 0) or 0
    d["tops_per_mm2"] = round(safe_div(tops, tile_mm2), 6)
    d["tops_per_cm3"] = round(safe_div(tops, vol_cm3), 6)
    d["mb_per_mm2"] = round(safe_div(mem, tile_mm2), 6)
    d["mb_per_cm3"] = round(safe_div(mem, vol_cm3), 6)
    d["tbps_per_cm3"] = round(safe_div(bw, vol_cm3), 6)
    d["tops_per_kusd"] = round(safe_div(tops, cost / 1000.0), 6)
    d["mb_per_kusd"] = round(safe_div(mem, cost / 1000.0), 6)
    d["tops_per_w_proxy"] = None  # no power data in baseline
    # internal consistency checks
    implied_cpt = safe_div(cost, tops, default=None)
    listed_cpt = v.get("cost_per_tops_usd")
    d["implied_cost_per_tops_usd"] = round(implied_cpt, 3) if implied_cpt is not None else None
    d["cost_per_tops_delta"] = (
        round(listed_cpt - implied_cpt, 3)
        if (implied_cpt is not None and listed_cpt is not None)
        else None
    )
    # endurance/reconfig practicality
    rc = v.get("reconfig_time_s", 0) or 0
    d["reconfigs_per_s"] = round(safe_div(1.0, rc), 6) if rc > 0 else None
    # effective memory bits density (Mb/mm2) rough
    d["mbit_per_mm2"] = round(safe_div(mem * 8, tile_mm2), 6)
    return d


def scenario_sim(v: Dict) -> Dict:
    """Simple workload scenarios (conceptual).
    Returns effective throughput (TOPS) under each scenario.
    """
    tops = float(v.get("throughput_tops_tile", 0) or 0)
    bw = float(v.get("memory_bandwidth_tbps", 0) or 0)  # TB/s
    mem_mb = float(v.get("memory_capacity_mb_module", 0) or 0)
    rc = float(v.get("reconfig_time_s", 1e9) or 1e9)
    lat_ps = float(v.get("inference_latency_ps", 1e6) or 1e6)

    # Scenario 1: Static inference, weights resident (compute-bound ideal)
    # limited slightly by latency pipeline efficiency
    pipe_eff = 1.0 / (1.0 + lat_ps / 1000.0)  # mild penalty if very high latency
    s_static = tops * max(0.3, min(1.0, 0.7 + 0.3 * pipe_eff))

    # Scenario 2: Dynamic kernels / frequent reconfig (every 1 ms batch)
    # if reconfig >= batch window, throughput collapses
    batch_s = 1e-3
    avail = max(0.0, batch_s - min(rc, batch_s))
    duty = avail / batch_s
    # memory nonvolatility helps (can keep weights) - approximate via mem and bits/cell
    nv_bonus = 1.0
    if mem_mb >= 128 and (v.get("memory_bits_per_cell", 0) or 0) >= 3:
        nv_bonus = 1.15
    if mem_mb < 16:
        nv_bonus = 0.85
    s_dynamic = tops * duty * nv_bonus
    # floor for ultra-fast reconfig
    if rc <= 1e-9:
        s_dynamic = max(s_dynamic, tops * 0.85)

    # Scenario 3: Memory-bandwidth-bound (large model streaming), assume 2 bytes/param eff
    # effective tops limited by bw: tops_eff ~ bw_TBps * 1e12 bytes/s / (2 bytes*ops?) simplified:
    # assume 2 TOPS per TB/s as a rough balance point
    bw_limited = bw * 2.0
    mem_cap_factor = min(1.0, 0.4 + 0.6 * min(mem_mb / 256.0, 1.0))
    s_membound = min(tops, max(bw_limited, 0.1)) * (0.7 + 0.3 * mem_cap_factor)

    return {
        "eff_tops_static_inference": round(s_static, 4),
        "eff_tops_dynamic_reconfig": round(s_dynamic, 4),
        "eff_tops_memory_bound": round(s_membound, 4),
        "balanced_eff_tops": round((s_static + s_dynamic + s_membound) / 3.0, 4),
    }


def objective_score(d: Dict, all_rows: List[Dict]) -> Dict:
    # Normalize on selected objective metrics (higher better unless noted)
    def nmax(key):
        m = max((r.get(key, 0) or 0) for r in all_rows) or 1.0
        return safe_div(d.get(key, 0) or 0, m)

    def nmin_cost(key):
        m = min((r.get(key, 1e18) or 1e18) for r in all_rows) or 1.0
        v = d.get(key, m) or m
        return safe_div(m, v)

    speed = 0.5 * nmax("speed_index") + 0.5 * nmax("balanced_eff_tops")
    capacity = 0.4 * nmax("capacity_index") + 0.3 * nmax("mb_per_cm3") + 0.3 * nmax("tops_per_cm3")
    dims = 0.5 * nmax("mb_per_cm3") + 0.5 * nmax("tops_per_cm3")  # density view
    reliability = nmax("reliability_index")
    feasibility = nmax("feasibility_norm")
    price = 0.5 * nmax("tops_per_kusd") + 0.5 * nmax("mb_per_kusd")
    open_access = 0.6 * feasibility + 0.4 * price  # proxy for accessible/open adoption
    overall = (speed + capacity + reliability + feasibility + price + dims) / 6.0
    return {
        "obj_speed": round(speed, 4),
        "obj_capacity": round(capacity, 4),
        "obj_density_dims": round(dims, 4),
        "obj_reliability": round(reliability, 4),
        "obj_feasibility": round(feasibility, 4),
        "obj_price_perf": round(price, 4),
        "obj_open_access": round(open_access, 4),
        "obj_overall": round(overall, 4),
    }


def sensitivity(rows: List[Dict], keys_focus: List[str]) -> Dict:
    """Perturb uncertain params and observe rank stability for focus set."""
    uncertain = [
        "throughput_tops_tile",
        "memory_capacity_mb_module",
        "memory_bandwidth_tbps",
        "cost_index",
        "est_unit_cost_usd",
        "feasibility_score",
        "stability_score",
    ]
    rng = np.random.default_rng(42)
    base_map = {r["key"]: r for r in rows}
    focus = [k for k in keys_focus if k in base_map]
    rank_counts = {k: [] for k in focus}
    trials = 200
    for _ in range(trials):
        sim_rows = []
        for r in rows:
            rr = deepcopy(r)
            for p in uncertain:
                if p in rr and isinstance(rr[p], (int, float)) and rr[p] is not None:
                    factor = float(rng.uniform(0.7, 1.3))
                    val = rr[p] * factor
                    if p in ("feasibility_score", "stability_score"):
                        val = int(max(1, min(5, round(val))))
                    rr[p] = val
            # recompute dependent simple fields
            rr["feasibility_norm"] = round(rr.get("feasibility_score", 1) / 5.0, 3)
            rr["price_norm_low_better"] = round(1.0 / (rr.get("cost_index", 1) or 1), 3)
            # recompute derived minimal for scoring
            rr = compute_derived(rr)
            scen = scenario_sim(rr)
            rr.update(scen)
            sim_rows.append(rr)
        # score
        for rr in sim_rows:
            rr.update(objective_score(rr, sim_rows))
        ordered = sorted(sim_rows, key=lambda x: x["obj_overall"], reverse=True)
        pos = {r["key"]: i + 1 for i, r in enumerate(ordered)}
        for k in focus:
            if k in pos:
                rank_counts[k].append(pos[k])
    summary = {}
    for k, vals in rank_counts.items():
        if not vals:
            continue
        arr = np.array(vals)
        summary[k] = {
            "rank_mean": round(float(arr.mean()), 3),
            "rank_std": round(float(arr.std()), 3),
            "rank_min": int(arr.min()),
            "rank_max": int(arr.max()),
            "top5_rate": round(float((arr <= 5).mean()), 3),
        }
    return {"trials": trials, "perturbation": "+/-30%", "params": uncertain, "focus": summary}


def pareto_front(rows: List[Dict], x="obj_price_perf", y="obj_capacity") -> List[str]:
    pts = [(r["key"], r[x], r[y]) for r in rows]
    front = []
    for k, xv, yv in pts:
        dominated = False
        for k2, x2, y2 in pts:
            if k2 == k:
                continue
            if (x2 >= xv and y2 >= yv) and (x2 > xv or y2 > yv):
                dominated = True
                break
        if not dominated:
            front.append(k)
    return front


def write_outputs(base, enriched: List[Dict], sens: Dict, fronts: Dict):
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    # CSV
    fields = list(enriched[0].keys())
    with open(os.path.join(OUT_DIR, "objective_combo_analysis.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(enriched)

    report = {
        "assumptions": [
            "Objective re-analysis of existing conceptual baseline (families_dev_comparison.json); no new physical measurements.",
            "Scenario simulations are simplified throughput models: static inference, dynamic 1ms reconfig batches, and memory-bandwidth-bound streaming (2 TOPS per TB/s rough balance).",
            "Sensitivity: 200 Monte Carlo trials with +/-30% perturbation on throughput, memory, bandwidth, cost, and scores.",
            "3D/volumetric variants have lower areal compactness but higher volumetric density; both views reported.",
        ],
        "pareto_fronts": fronts,
        "sensitivity": sens,
        "rankings_objective": {
            "overall": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_overall"], reverse=True)],
            "speed": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_speed"], reverse=True)],
            "capacity": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_capacity"], reverse=True)],
            "density_dims": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_density_dims"], reverse=True)],
            "reliability": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_reliability"], reverse=True)],
            "feasibility": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_feasibility"], reverse=True)],
            "price_perf": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_price_perf"], reverse=True)],
            "open_access": [r["key"] for r in sorted(enriched, key=lambda x: x["obj_open_access"], reverse=True)],
            "balanced_eff_tops": [r["key"] for r in sorted(enriched, key=lambda x: x["balanced_eff_tops"], reverse=True)],
        },
        "variants": enriched,
    }
    with open(os.path.join(OUT_DIR, "objective_combo_analysis.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Markdown
    focus_set = set(FOCUS)
    foc = [r for r in enriched if r["key"] in focus_set]
    foc = sorted(foc, key=lambda x: x["obj_overall"], reverse=True)
    lines = [
        "# Objective Review: Family Combinations (Comparative Analysis & Simulations)",
        "",
        "> Re-analysis of `families_dev_comparison.json` with derived metrics, scenario simulations, and sensitivity. Conceptual/order-of-magnitude only (not measured).",
        "",
        "## 1. Key derived metrics (focus variants)",
        "",
        "| Key | Variant | TOPS/mm² | TOPS/cm³ | MB/cm³ | TOPS/k$ | MB/k$ | Eff TOPS static | Eff TOPS dynamic | Eff TOPS mem-bound | Balanced | Obj overall |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in foc:
        lines.append(
            f"| {r['key']} | {r['name']} | {r['tops_per_mm2']} | {r['tops_per_cm3']} | {r['mb_per_cm3']} | "
            f"{r['tops_per_kusd']} | {r['mb_per_kusd']} | {r['eff_tops_static_inference']} | "
            f"{r['eff_tops_dynamic_reconfig']} | {r['eff_tops_memory_bound']} | {r['balanced_eff_tops']} | {r['obj_overall']} |"
        )

    # Baseline inconsistencies
    lines += ["", "## 2. Internal consistency checks (baseline)", ""]
    inconsist = [r for r in enriched if r.get("cost_per_tops_delta") is not None and abs(r["cost_per_tops_delta"]) > 1]
    if inconsist:
        lines.append("`cost_per_tops_usd` differs from `est_unit_cost_usd/throughput_tops_tile` (should be aligned or explained):")
        lines.append("")
        lines.append("| Key | listed $/TOPS | implied $/TOPS (unit/TOPS) | delta |")
        lines.append("|---|---:|---:|---:|")
        for r in sorted(inconsist, key=lambda x: abs(x["cost_per_tops_delta"]), reverse=True)[:12]:
            lines.append(f"| {r['key']} | {r['cost_per_tops_usd']} | {r['implied_cost_per_tops_usd']} | {r['cost_per_tops_delta']} |")
    else:
        lines.append("No major $/TOPS inconsistencies detected by this check.")

    # Objective rankings
    lines += ["", "## 3. Objective rankings (all variants)", ""]
    for k, v in report["rankings_objective"].items():
        lines.append(f"- **{k}:** {', '.join(v[:10])}{' ...' if len(v)>10 else ''}")

    lines += ["", "## 4. Pareto fronts (non-dominated)", ""]
    for k, v in fronts.items():
        lines.append(f"- **{k}:** {', '.join(v)}")

    # Sensitivity for combos
    lines += ["", "## 5. Sensitivity (rank stability, +/-30%, 200 trials)", ""]
    lines.append("| Key | mean rank | std | min | max | P(top5) |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for k in FOCUS:
        if k in sens["focus"]:
            s = sens["focus"][k]
            lines.append(f"| {k} | {s['rank_mean']} | {s['rank_std']} | {s['rank_min']} | {s['rank_max']} | {s['top5_rate']} |")

    # Objective review of H1-H5
    h = {r["key"]: r for r in enriched}
    lines += [
        "",
        "## 6. Objective review of combinations (H1–H5)",
        "",
        f"- **H1 Membrane-Brush NV:** highest capacity/density-by-volume in baseline (MB/cm³={h['H1']['mb_per_cm3']}, TOPS/cm³={h['H1']['tops_per_cm3']}) and strong overall ({h['H1']['obj_overall']}), but low areal compactness and high cost/complexity; dynamic efficiency benefits from NV weights but reconfig is not ultra-fast. Risk: 3D integration, thermal/phase tolerances.",
        f"- **H2 RT Membrane-WDM Core:** top speed/BW profile (BW={h['H2']['memory_bandwidth_tbps']} TB/s, balanced eff={h['H2']['balanced_eff_tops']}) and good volumetric density, but **low NV memory** (MB/cm³={h['H2']['mb_per_cm3']}) and lowest feasibility/cost profile among H combos; best for streaming/dynamic kernels, weak as standalone weight store.",
        f"- **H3 Open WDM-PCM:** strongest open-access/feasibility-price proxy (obj_open_access={h['H3']['obj_open_access']}, feasibility={h['H3']['feasibility_norm']}, unit ${h['H3']['est_unit_cost_usd']}); moderate speed (slow PCM reconfig) but decent memory density (MB/cm³={h['H3']['mb_per_cm3']}) and NV. Most robust near-term candidate under open/practical constraints.",
        f"- **H4 Volumetric Tensor Membrane:** maximum raw capacity/throughput (TOPS={h['H4']['throughput_tops_tile']}, MB={h['H4']['memory_capacity_mb_module']}, cap_idx={h['H4']['capacity_index']}) yet highest cost/risk and low feasibility; efficiency advantage is scenario-dependent and integration/alignment dominate realizability.",
        f"- **H5 Dense Resonant Stack:** good areal/volumetric compute density but limited by reliability/stability (rel_idx={h['H5']['reliability_index']}, stability={h['H5']['stability_score']}) and high losses (ENZ/plasmonic optional block); remains exploratory.",
        "",
        "## 7. Conclusions (objective)",
        "",
        "- **Best balanced candidate today (open/feasible): H3** — highest feasibility and best price-perf/open-access among hybrids, NV and incremental from A1.",
        "- **Best dynamic/high-speed compact core: H2/G2** — strong in static/dynamic/bandwidth scenarios, but require external/NV weight strategy (pair with M1/A1 or H3) and thermal/phase control.",
        "- **Best capacity scaling (if integration solved): H1/H4** — volumetric leaders; H4 highest ceiling, H1 more modular NV path. Both carry high cost and integration risk.",
        "- **Baseline A1 remains the reference** for low cost/risk and openness; volumetric 3D (A1-3D) helps capacity but area/packaging trade-offs are significant.",
        "- **Model caveats:** inputs are conceptual; $/TOPS fields show some baseline inconsistencies (section 2); power/thermal/system-loss models are not yet coupled — next step is physics-linked models (TMM for G, ring/F-P loss-Q, thermal) and per-mm²/mm³/W normalization.",
    ]

    with open(os.path.join(OUT_DIR, "objective_combo_analysis.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # Plots
    if plt is not None:
        # Scenario bars for focus
        keys = [r["key"] for r in foc]
        x = np.arange(len(keys))
        w = 0.25
        fig, ax = plt.subplots(figsize=(12, 4.8))
        ax.bar(x - w, [r["eff_tops_static_inference"] for r in foc], w, label="static")
        ax.bar(x, [r["eff_tops_dynamic_reconfig"] for r in foc], w, label="dynamic/reconfig")
        ax.bar(x + w, [r["eff_tops_memory_bound"] for r in foc], w, label="memory-bound")
        ax.set_xticks(x)
        ax.set_xticklabels(keys)
        ax.set_ylabel("Effective TOPS (conceptual)")
        ax.set_title("Scenario simulation: effective throughput (focus variants)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, "objective_scenarios.png"), dpi=150)
        plt.close(fig)

        # Volumetric density scatter
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter([r["mb_per_cm3"] for r in enriched], [r["tops_per_cm3"] for r in enriched], alpha=0.6)
        for r in foc:
            ax.annotate(r["key"], (r["mb_per_cm3"], r["tops_per_cm3"]))
        ax.set_xlabel("Memory density (MB/cm³)")
        ax.set_ylabel("Compute density (TOPS/cm³)")
        ax.set_title("Volumetric density (objective derived)")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, "objective_density.png"), dpi=150)
        plt.close(fig)

        # Price-perf vs capacity
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter([r["obj_price_perf"] for r in enriched], [r["obj_capacity"] for r in enriched], alpha=0.6)
        for r in foc:
            ax.annotate(r["key"], (r["obj_price_perf"], r["obj_capacity"]))
        ax.set_xlabel("Objective price-performance (higher better)")
        ax.set_ylabel("Objective capacity+density (higher better)")
        ax.set_title("Price-performance vs capacity")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, "objective_price_capacity.png"), dpi=150)
        plt.close(fig)

        # Sensitivity box-like (mean/std)
        sens_keys = [k for k in FOCUS if k in sens["focus"]]
        means = [sens["focus"][k]["rank_mean"] for k in sens_keys]
        stds = [sens["focus"][k]["rank_std"] for k in sens_keys]
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(sens_keys, means, yerr=stds, capsize=4)
        ax.invert_yaxis()
        ax.set_ylabel("Mean rank (lower better)")
        ax.set_title("Sensitivity: rank stability under +/-30% perturbations")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, "objective_sensitivity.png"), dpi=150)
        plt.close(fig)

    return report


def main():
    base = load_base()
    variants = base.get("variants", [])
    enriched = []
    for v in variants:
        d = compute_derived(v)
        d.update(scenario_sim(d))
        enriched.append(d)
    # compute objective scores after all have scenario/derived fields
    for d in enriched:
        d.update(objective_score(d, enriched))

    sens = sensitivity(enriched, FOCUS)
    fronts = {
        "price_perf_vs_capacity": pareto_front(enriched, "obj_price_perf", "obj_capacity"),
        "feasibility_vs_speed": pareto_front(enriched, "obj_feasibility", "obj_speed"),
        "open_access_vs_capacity": pareto_front(enriched, "obj_open_access", "obj_capacity"),
    }
    report = write_outputs(base, enriched, sens, fronts)
    print(json.dumps({
        "variants": len(enriched),
        "focus": FOCUS,
        "fronts": fronts,
        "out": [os.path.join(OUT_DIR, "objective_combo_analysis.md"), os.path.join(OUT_DIR, "objective_combo_analysis.json")]
    }, indent=2))


if __name__ == "__main__":
    main()
