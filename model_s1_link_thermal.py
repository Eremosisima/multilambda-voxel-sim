#!/usr/bin/env python3
"""
S1: Optical link budget and thermal-operating margin simulation per prioritized candidate.
Conceptual, parametric (no measurements). Uses manufacturable assumptions from repo.
"""
from __future__ import annotations

import csv
import json
import math
import os

OUT = "outputs"
FIG = "figures"

# Nominal element losses (dB) and penalties - conceptual ranges
ELEMENT_DB = {
    "fiber_chip_coupling": 1.5,
    "wg_propagation_db_cm": 1.5,
    "mzi_passive": 0.8,
    "pcm_element": 0.6,
    "vo2_switch": 0.5,
    "ring_drop": 1.0,
    "ring_through": 0.2,
    "membrane_stack_passive": 0.8,  # per functional stack (multi-layer)
    "membrane_eo": 1.0,
    "membrane_pcm_eo": 1.2,
    "splitter_combiner": 0.5,
    "crossing": 0.1,
    "detector_coupling": 0.5,
    "margin_packaging": 1.0,
}

LASER = {"source_dbm": 10.0, "per_channel_dbm": 3.0}  # conceptual
DETECTOR = {"min_signal_dbm": -18.0, "sensitivity_dbm": -22.0}  # conceptual

# Thermal assumptions (C)
THERMAL = {
    "ambient_c": 45.0,
    "vo2_limit_c": 68.0,
    "pcm_write_peak_c": 300.0,
    "ring_tune_load_c": 20.0,
    "eo_driver_load_c": 15.0,
    "spreader_delta_c": 15.0,
    "tec_capacity_c": 25.0,
    "isolation_nominal_c": 230.0,  # drop from 300C hotspot to neighbor region (with trenches/spreading)
    "isolation_worst_c": 180.0,
    "omcc_duty_factor_nom": 0.15,
    "omcc_duty_factor_worst": 0.35,
}

CANDIDATES = {
    "H3": {
        "name": "Open WDM-PCM (A1+G1+B3)",
        "path": [
            ("fiber_chip_coupling", 1),
            ("wg_propagation_db_cm", 0.5),
            ("membrane_stack_passive", 1),
            ("splitter_combiner", 1),
            ("ring_drop", 2),
            ("ring_through", 1),
            ("mzi_passive", 1),
            ("pcm_element", 1),
            ("vo2_switch", 1),
            ("splitter_combiner", 1),
            ("wg_propagation_db_cm", 0.5),
            ("detector_coupling", 1),
            ("margin_packaging", 1),
        ],
        "thermal_sources": {"pcm_write": 300.0, "ring_tune": 20.0},
        "notes": "Thermal dominated by PCM writes near rings/VO2; relies on trenches, spreading, TEC and OMCC sequencing."
    },
    "G2": {
        "name": "Thin-film membrane/F-P stack (EO-tuned)",
        "path": [
            ("fiber_chip_coupling", 1),
            ("wg_propagation_db_cm", 0.4),
            ("membrane_eo", 2),
            ("splitter_combiner", 1),
            ("wg_propagation_db_cm", 0.4),
            ("detector_coupling", 1),
            ("margin_packaging", 1),
        ],
        "thermal_sources": {"eo_driver": 15.0, "ring_tune": 0.0},
        "notes": "No 300C PCM write; thermal load mainly EO/RF drivers and stabilization, manageable with spreading."
    },
    "G3": {
        "name": "Thin-film membrane stack (PCM+EO hybrid)",
        "path": [
            ("fiber_chip_coupling", 1),
            ("wg_propagation_db_cm", 0.4),
            ("membrane_pcm_eo", 2),
            ("splitter_combiner", 1),
            ("wg_propagation_db_cm", 0.4),
            ("detector_coupling", 1),
            ("margin_packaging", 1),
        ],
        "thermal_sources": {"pcm_write": 300.0, "eo_driver": 12.0},
        "notes": "Localized PCM write heat co-integrated with EO; requires isolation/trenches and duty-cycled writes."
    },
    "H1": {
        "name": "Membrane-Brush NV (A1+G3+3D)",
        "path": [
            ("fiber_chip_coupling", 1),
            ("wg_propagation_db_cm", 0.8),
            ("membrane_pcm_eo", 2),
            ("mzi_passive", 1),
            ("pcm_element", 1),
            ("vo2_switch", 1),
            ("crossing", 4),
            ("splitter_combiner", 2),
            ("wg_propagation_db_cm", 0.8),
            ("detector_coupling", 1),
            ("margin_packaging", 1),
        ],
        "thermal_sources": {"pcm_write": 300.0, "eo_driver": 12.0, "ring_tune": 10.0},
        "notes": "3D stacking increases path/crossings and thermal density; segmented heaters, vertical/lateral isolation and strict sequencing required."
    },
    "H4": {
        "name": "Volumetric Tensor Membrane (G2/G3+F2+A1)",
        "path": [
            ("fiber_chip_coupling", 1),
            ("wg_propagation_db_cm", 1.0),
            ("membrane_eo", 1),
            ("membrane_pcm_eo", 2),
            ("crossing", 6),
            ("splitter_combiner", 2),
            ("mzi_passive", 1),
            ("pcm_element", 1),
            ("wg_propagation_db_cm", 1.0),
            ("detector_coupling", 1),
            ("margin_packaging", 1),
        ],
        "thermal_sources": {"pcm_write": 300.0, "eo_driver": 18.0, "ring_tune": 10.0},
        "notes": "Highest optical path complexity and distributed thermal load; needs high-capacity spreading/cooling and active stabilization."
    },
}


def path_loss_db(path):
    total = 0.0
    detail = []
    for elem, count in path:
        if elem == "wg_propagation_db_cm":
            loss = ELEMENT_DB[elem] * count
        else:
            loss = ELEMENT_DB[elem] * count
        total += loss
        detail.append({"element": elem, "count": count, "loss_db": round(loss, 3)})
    return round(total, 3), detail


def thermal_eval(srcs):
    amb = THERMAL["ambient_c"]
    # local peak during write (at actuator)
    local_peak = amb + max(srcs.values()) if srcs else amb
    # neighbor temperature estimate: ambient + (peak-ambient - isolation)*duty + background
    def neighbor(isolation, duty, bg):
        coupled = max(local_peak - isolation, 0.0) * duty
        return amb + THERMAL["spreader_delta_c"] * 0.3 + bg + coupled
    nom_bg = srcs.get("ring_tune", 0) * 0.2 + srcs.get("eo_driver", 0) * 0.15
    worst_bg = nom_bg * 1.4
    t_nom = neighbor(THERMAL["isolation_nominal_c"], THERMAL["omcc_duty_factor_nom"], nom_bg)
    t_worst = neighbor(THERMAL["isolation_worst_c"], THERMAL["omcc_duty_factor_worst"], worst_bg)
    margin_nom = THERMAL["vo2_limit_c"] - t_nom
    margin_worst = THERMAL["vo2_limit_c"] - t_worst
    return {
        "local_peak_c": round(local_peak, 2),
        "neighbor_nominal_c": round(t_nom, 2),
        "neighbor_worst_c": round(t_worst, 2),
        "vo2_limit_c": THERMAL["vo2_limit_c"],
        "margin_nominal_c": round(margin_nom, 2),
        "margin_worst_c": round(margin_worst, 2),
        "thermal_feasible_nominal": margin_nom >= 0,
        "thermal_feasible_worst_case": margin_worst >= 0,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    rows = []
    for k, c in CANDIDATES.items():
        il, detail = path_loss_db(c["path"])
        rx = round(LASER["per_channel_dbm"] - il, 3)
        snr_margin = round(rx - DETECTOR["min_signal_dbm"], 3)
        sens_margin = round(rx - DETECTOR["sensitivity_dbm"], 3)
        th = thermal_eval(c["thermal_sources"])
        rows.append({
            "key": k,
            "name": c["name"],
            "insertion_loss_db": il,
            "laser_per_ch_dbm": LASER["per_channel_dbm"],
            "rx_signal_dbm": rx,
            "detector_min_dbm": DETECTOR["min_signal_dbm"],
            "link_margin_db": snr_margin,
            "sensitivity_margin_db": sens_margin,
            "link_feasible": snr_margin >= 3.0,
            **th,
            "notes": c["notes"],
            "path_detail": detail,
        })

    summary = {
        "assumptions": {
            "elements_db": ELEMENT_DB,
            "laser": LASER,
            "detector": DETECTOR,
            "thermal": THERMAL,
            "criteria": "link feasible if margin >= 3 dB above min detector signal; thermal feasible if neighbor < 68C (VO2) in nominal/worst duty-cycle cases",
        },
        "candidates": rows,
        "disclaimer": "Conceptual parametric S1 model; replace with measured IL/n/k, calibrated thermal FEM and detector noise for design decisions.",
    }
    with open(os.path.join(OUT, "s1_link_thermal.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    csv_rows = [{kk: vv for kk, vv in r.items() if kk != "path_detail"} for r in rows]
    with open(os.path.join(OUT, "s1_link_thermal.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)

    # Markdown
    md = ["# S1 — Presupuesto de enlace óptico y márgenes térmicos (conceptual)", "",
          "> Modelo paramétrico S1. No son mediciones; requiere calibración con IL/FEM/ruido medidos.", "",
          "## Resumen por candidato", "",
          "| Candidato | IL (dB) | Rx (dBm) | Margen enlace (dB) | Margen sens. (dB) | Enlace ok (>=3dB) | Vecino nominal (C) | Margen VO2 nom (C) | Vecino peor caso (C) | Margen VO2 peor (C) | Térmica nominal | Térmica peor caso |",
          "|---|---:|---:|---:|---:|:---:|---:|---:|---:|---:|:---:|:---:|"]
    for r in rows:
        md.append(f"| {r['key']} | {r['insertion_loss_db']} | {r['rx_signal_dbm']} | {r['link_margin_db']} | {r['sensitivity_margin_db']} | {'sí' if r['link_feasible'] else 'no'} | {r['neighbor_nominal_c']} | {r['margin_nominal_c']} | {r['neighbor_worst_c']} | {r['margin_worst_c']} | {'sí' if r['thermal_feasible_nominal'] else 'no'} | {'sí' if r['thermal_feasible_worst_case'] else 'no'} |")
    md += ["", "## Notas", ""]
    for r in rows:
        md.append(f"- **{r['key']}**: {r['notes']}")
    md += ["", "## Recomendaciones S1", "- Refinar IL con datos de proceso (acoplos, propagación, rings/membranas/MZI) y presupuesto de ruido del receptor.",
           "- Ejecutar FEM térmico 3D transitorio con layout real (trench, pitch, duty cycle OMCC) para validar márgenes VO2 y estabilidad de resonancias.",
           "- Para H1/H4, co-optimizar ruta óptica (cruces/longitud) y distribución térmica (manifold/secuenciado) antes de E2/E4."]
    with open(os.path.join(OUT, "s1_link_thermal.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        keys = [r["key"] for r in rows]
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].bar(keys, [r["link_margin_db"] for r in rows], color="#4c78a8")
        axes[0].axhline(3.0, color="red", ls="--", lw=1, label="umbral 3 dB")
        axes[0].set_title("Margen de enlace óptico (dB)")
        axes[0].set_ylabel("dB")
        axes[0].legend()
        axes[1].bar(keys, [r["margin_nominal_c"] for r in rows], color="#54a24b", label="nominal")
        axes[1].bar(keys, [r["margin_worst_c"] for r in rows], color="#e45756", alpha=0.6, label="peor caso")
        axes[1].axhline(0.0, color="black", ls="--", lw=1)
        axes[1].set_title("Margen térmico vs VO2 68C (°C)")
        axes[1].set_ylabel("°C")
        axes[1].legend()
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "s1_link_thermal_margins.png"), dpi=150)
        plt.close(fig)
    except Exception as e:
        print("figure_warning:", e)

    print(json.dumps({"candidates": len(rows), "out": "outputs/s1_link_thermal.*"}))


if __name__ == "__main__":
    main()
