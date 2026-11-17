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


def thermal_eval(srcs, isolation_nom=None, isolation_worst=None, duty_nom=None, duty_worst=None,
                 spreader_eff=0.3, tec_delta=0.0, bg_scale_nom=1.0, bg_scale_worst=1.4,
                 layout_factor_nom=1.0, layout_factor_worst=1.0, transient_rise_nom=1.0, transient_rise_worst=1.08):
    amb = THERMAL["ambient_c"]
    iso_n = (THERMAL["isolation_nominal_c"] if isolation_nom is None else isolation_nom) * layout_factor_nom
    iso_w = (THERMAL["isolation_worst_c"] if isolation_worst is None else isolation_worst) * layout_factor_worst
    d_n = THERMAL["omcc_duty_factor_nom"] if duty_nom is None else duty_nom
    d_w = THERMAL["omcc_duty_factor_worst"] if duty_worst is None else duty_worst
    # local peak during write (at actuator)
    local_peak = amb + max(srcs.values()) if srcs else amb
    # neighbor temperature estimate: ambient + (peak-ambient - isolation)*duty*transient + background
    def neighbor(isolation, duty, bg, transient):
        coupled = max(local_peak - isolation, 0.0) * duty * transient
        return amb + THERMAL["spreader_delta_c"] * spreader_eff + bg + coupled - tec_delta
    nom_bg = (srcs.get("ring_tune", 0) * 0.2 + srcs.get("eo_driver", 0) * 0.15) * bg_scale_nom
    worst_bg = (srcs.get("ring_tune", 0) * 0.2 + srcs.get("eo_driver", 0) * 0.15) * bg_scale_worst
    t_nom = neighbor(iso_n, d_n, nom_bg, transient_rise_nom)
    t_worst = neighbor(iso_w, d_w, worst_bg, transient_rise_worst)
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
        "effective_isolation_nom_c": round(iso_n, 2),
        "effective_isolation_worst_c": round(iso_w, 2),
        "duty_nom": d_n, "duty_worst": d_w,
        "layout_factor_nom": layout_factor_nom, "layout_factor_worst": layout_factor_worst,
    }


def layout_duty_sweep(key, c, rc=None):
    # conceptual layout/duty-aware transient sweep for PCM candidates
    if "pcm_write" not in c["thermal_sources"]:
        return []
    layouts = [
        ("compact", 0.94, 0.92, 1.03, 1.10),
        ("baseline", 1.00, 1.00, 1.00, 1.08),
        ("spread_out", 1.05, 1.04, 0.98, 1.05),
    ]
    duties = [0.03, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35]
    base = rc or {}
    rows = []
    for lname, lf_n, lf_w, tr_n, tr_w in layouts:
        for d in duties:
            ev = thermal_eval(
                c["thermal_sources"],
                isolation_nom=base.get("isolation_nominal_c"),
                isolation_worst=base.get("isolation_worst_c"),
                duty_nom=d, duty_worst=d,
                spreader_eff=base.get("spreader_eff", 0.3),
                tec_delta=base.get("tec_delta", 0.0),
                layout_factor_nom=lf_n, layout_factor_worst=lf_w,
                transient_rise_nom=tr_n, transient_rise_worst=tr_w,
            )
            rows.append({
                "candidate": key, "scenario": base.get("label", "default"),
                "layout": lname, "duty_cycle": d,
                "neighbor_nominal_c": ev["neighbor_nominal_c"],
                "margin_nominal_c": ev["margin_nominal_c"],
                "neighbor_worst_c": ev["neighbor_worst_c"],
                "margin_worst_c": ev["margin_worst_c"],
                "feasible_nominal": ev["thermal_feasible_nominal"],
                "feasible_worst_case": ev["thermal_feasible_worst_case"],
                "effective_isolation_nom_c": ev["effective_isolation_nom_c"],
                "effective_isolation_worst_c": ev["effective_isolation_worst_c"],
            })
    return rows

# S1 recalibrated scenarios (sequencing/cooling/isolation) for PCM candidates
RECALIBRATED = {
    "H3": {"isolation_nominal_c": 245, "isolation_worst_c": 205, "duty_nom": 0.08, "duty_worst": 0.18, "spreader_eff": 0.2, "tec_delta": 6.0, "label": "OMCC-sequenced writes + trench/spreader + TEC assist"},
    "G3": {"isolation_nominal_c": 245, "isolation_worst_c": 205, "duty_nom": 0.08, "duty_worst": 0.18, "spreader_eff": 0.2, "tec_delta": 6.0, "label": "Duty-cycled PCM writes + isolation + TEC assist"},
    "H1": {"isolation_nominal_c": 248, "isolation_worst_c": 210, "duty_nom": 0.06, "duty_worst": 0.14, "spreader_eff": 0.18, "tec_delta": 8.0, "label": "Strict OMCC sequencing + vertical/lateral isolation + manifold cooling"},
    "H4": {"isolation_nominal_c": 250, "isolation_worst_c": 215, "duty_nom": 0.05, "duty_worst": 0.12, "spreader_eff": 0.16, "tec_delta": 10.0, "label": "Aggressive sequencing + high-capacity spreading/manifold + active stabilization"},
}


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    rows = []
    sweep_rows = []
    for k, c in CANDIDATES.items():
        il, detail = path_loss_db(c["path"])
        rx = round(LASER["per_channel_dbm"] - il, 3)
        snr_margin = round(rx - DETECTOR["min_signal_dbm"], 3)
        sens_margin = round(rx - DETECTOR["sensitivity_dbm"], 3)
        th = thermal_eval(c["thermal_sources"])
        recal = None
        rc = RECALIBRATED.get(k)
        if rc:
            recal = thermal_eval(
                c["thermal_sources"],
                isolation_nom=rc.get("isolation_nominal_c"),
                isolation_worst=rc.get("isolation_worst_c"),
                duty_nom=rc.get("duty_nom"),
                duty_worst=rc.get("duty_worst"),
                spreader_eff=rc.get("spreader_eff", 0.3),
                tec_delta=rc.get("tec_delta", 0.0),
            )
            recal["scenario"] = rc["label"]
        # layout/duty-aware transient sweep (conceptual) for PCM candidates
        sweep_rows.extend(layout_duty_sweep(k, c, rc if rc else None))
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
            "recalibrated": recal,
        })

    summary = {
        "assumptions": {
            "elements_db": ELEMENT_DB,
            "laser": LASER,
            "detector": DETECTOR,
            "thermal": THERMAL,
            "criteria": "link feasible if margin >= 3 dB above min detector signal; thermal feasible if neighbor < 68C (VO2) in nominal/worst duty-cycle cases",
            "recalibrated_scenarios": RECALIBRATED,
            "layout_duty_sweep": "layout_factor and transient_rise factors with duty sweep for PCM candidates (conceptual, not FEM)",
        },
        "candidates": rows,
        "layout_duty_sweep_rows": sweep_rows,
        "disclaimer": "Conceptual parametric S1 model; replace with measured IL/n/k, calibrated thermal FEM and detector noise for design decisions.",
    }
    with open(os.path.join(OUT, "s1_link_thermal.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    if sweep_rows:
        with open(os.path.join(OUT, "s1_layout_duty.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(sweep_rows[0].keys()))
            w.writeheader(); w.writerows(sweep_rows)

    csv_rows = []
    for r in rows:
        base = {kk: vv for kk, vv in r.items() if kk not in ("path_detail","recalibrated")}
        if r.get("recalibrated"):
            base["recal_scenario"] = r["recalibrated"].get("scenario")
            base["recal_neighbor_nominal_c"] = r["recalibrated"].get("neighbor_nominal_c")
            base["recal_margin_nominal_c"] = r["recalibrated"].get("margin_nominal_c")
            base["recal_neighbor_worst_c"] = r["recalibrated"].get("neighbor_worst_c")
            base["recal_margin_worst_c"] = r["recalibrated"].get("margin_worst_c")
            base["recal_feasible_nominal"] = r["recalibrated"].get("thermal_feasible_nominal")
            base["recal_feasible_worst"] = r["recalibrated"].get("thermal_feasible_worst_case")
        csv_rows.append(base)
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
    md += ["", "## Recalibración térmica (secuenciado/enfriamiento, PCM candidatos)", "",
          "| Candidato | Escenario | Vecino nom (C) | Margen nom (C) | Vecino peor (C) | Margen peor (C) | Nom | Peor |",
          "|---|---|---:|---:|---:|---:|:---:|:---:|"]
    for r in rows:
        if r.get("recalibrated"):
            rc = r["recalibrated"]
            md.append(f"| {r['key']} | {rc['scenario']} | {rc['neighbor_nominal_c']} | {rc['margin_nominal_c']} | {rc['neighbor_worst_c']} | {rc['margin_worst_c']} | {'sí' if rc['thermal_feasible_nominal'] else 'no'} | {'sí' if rc['thermal_feasible_worst_case'] else 'no'} |")
    md += ["", "## Notas", ""]
    for r in rows:
        md.append(f"- **{r['key']}**: {r['notes']}")
    # layout/duty-aware transient sweep summary (PCM candidates)
    if sweep_rows:
        md += ["", "## Barrido layout/duty transitorio (conceptual, candidatos PCM)", "",
               "| Candidato | Layout | Duty | Vecino nom (°C) | Margen nom (°C) | Vecino peor (°C) | Margen peor (°C) | Nom | Peor |",
               "|---|---|---:|---:|---:|---:|---:|:---:|:---:|"]
        # show selected duty points
        show_duties = {0.03, 0.05, 0.08, 0.12, 0.18}
        for sr in sweep_rows:
            if sr["duty_cycle"] in show_duties and sr["layout"] in ("compact","baseline","spread_out"):
                md.append(f"| {sr['candidate']} | {sr['layout']} | {sr['duty_cycle']} | {sr['neighbor_nominal_c']} | {sr['margin_nominal_c']} | {sr['neighbor_worst_c']} | {sr['margin_worst_c']} | {'sí' if sr['feasible_nominal'] else 'no'} | {'sí' if sr['feasible_worst_case'] else 'no'} |")
        # max feasible duty summary
        md += ["", "### Duty máximo factible por layout (margen VO2 ≥ 0 °C)", "",
               "| Candidato | Layout | Max duty nominal | Max duty peor caso |",
               "|---|---|---:|---:|"]
        for k in sorted({r['candidate'] for r in sweep_rows}):
            for layout in ("compact","baseline","spread_out"):
                sub = [r for r in sweep_rows if r['candidate']==k and r['layout']==layout]
                dn = max([r['duty_cycle'] for r in sub if r['feasible_nominal']] or [0.0])
                dw = max([r['duty_cycle'] for r in sub if r['feasible_worst_case']] or [0.0])
                md.append(f"| {k} | {layout} | {dn} | {dw} |")
        # separate sweep report
        smd = ["# S1 — Barrido layout/duty-aware transitorio (conceptual)", "",
               "> Aproximación paramétrica (aislamiento efectivo, duty OMCC, factor transitorio por layout). No sustituye FEM 3D transitorio.", "",
               "| Candidato | Layout | Duty | Vecino nom (°C) | Margen nom (°C) | Vecino peor (°C) | Margen peor (°C) | Nom | Peor |",
               "|---|---|---:|---:|---:|---:|---:|:---:|:---:|"]
        for sr in sweep_rows:
            smd.append(f"| {sr['candidate']} | {sr['layout']} | {sr['duty_cycle']} | {sr['neighbor_nominal_c']} | {sr['margin_nominal_c']} | {sr['neighbor_worst_c']} | {sr['margin_worst_c']} | {'sí' if sr['feasible_nominal'] else 'no'} | {'sí' if sr['feasible_worst_case'] else 'no'} |")
        with open(os.path.join(OUT, "s1_layout_duty.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(smd) + "\n")

    md += ["", "## Recomendaciones S1", "- Refinar IL con datos de proceso (acoplos, propagación, rings/membranas/MZI) y presupuesto de ruido del receptor.",
           "- Ejecutar FEM térmico 3D transitorio con layout real (trench, pitch, duty cycle OMCC) para validar márgenes VO2 y estabilidad de resonancias; usar barrido layout/duty como guía de secuenciado.",
           "- Para H1/H4, co-optimizar ruta óptica (cruces/longitud) y distribución térmica (manifold/secuenciado, layouts spread-out) antes de E2/E4.",
           "- Aplicar escenarios recalibrados y validar duty cycle efectivo y densidad de escritura por layout en S2/E2."]

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
        if sweep_rows:
            fig2, axes2 = plt.subplots(1, 2, figsize=(10, 4), sharey=False)
            for cand, ax in zip(["H3","G3","H1","H4"], [axes2[0], axes2[0], axes2[1], axes2[1]]):
                pass
            # simpler: one subplot per 2 cands? do H3/G3 and H1/H4
            for ax, cands in zip(axes2, [["H3","G3"], ["H1","H4"]]):
                for cand in cands:
                    sub = [r for r in sweep_rows if r['candidate']==cand and r['layout']=='baseline']
                    sub = sorted(sub, key=lambda x: x['duty_cycle'])
                    ax.plot([r['duty_cycle'] for r in sub], [r['margin_nominal_c'] for r in sub], marker='o', label=f"{cand} nom")
                    ax.plot([r['duty_cycle'] for r in sub], [r['margin_worst_c'] for r in sub], marker='x', ls='--', label=f"{cand} peor")
                ax.axhline(0.0, color='black', ls='--', lw=1)
                ax.set_xlabel('Duty cycle (OMCC)'); ax.set_ylabel('Margen VO2 (°C)')
                ax.set_title('Layout baseline: margen vs duty ' + ('(H3,G3)' if cands[0]=='H3' else '(H1,H4)'))
                ax.legend(fontsize=7)
            fig2.tight_layout()
            fig2.savefig(os.path.join(FIG, "s1_layout_duty.png"), dpi=150)
            plt.close(fig2)
    except Exception as e:
        print("figure_warning:", e)

    print(json.dumps({"candidates": len(rows), "out": "outputs/s1_link_thermal.*"}))


if __name__ == "__main__":
    main()
