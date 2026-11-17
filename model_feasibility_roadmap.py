#!/usr/bin/env python3
"""
Feasibility roadmap model: consolidates existing simulation/analysis outputs
(objective combo, manufacturable dims, system P1-P3 context) into a
simulation-first plan to make prioritized OPGPU candidates feasible.

Conceptual, reproducible from repo outputs. Not a fabrication-ready design.
"""
from __future__ import annotations

import csv
import json
import math
import os
from datetime import datetime, timezone

OUT = "outputs"
FIG = "figures"

PRIORITY = ["H3", "G2", "G3", "H1", "H4"]

# Target envelopes (conceptual) for "make feasible"
TARGETS = {
    "edge": {"tops": 50, "mem_gb": 8, "bw_tbps": 1.0, "power_w": 75, "form": "module/card"},
    "workstation": {"tops": 300, "mem_gb": 48, "bw_tbps": 4.0, "power_w": 300, "form": "PCIe accelerator"},
    "datacenter": {"tops": 800, "mem_gb": 96, "bw_tbps": 8.0, "power_w": 600, "form": "OAM/SXM-class"},
}

# Feasibility axes (0-1, higher = more feasible/mature now), conceptual scoring
# derived/adjusted from repo analyses and known integration burdens
AXES = {
    "H3": {
        "optical_compute": 0.65, "memory_hierarchy": 0.70, "thermal_control": 0.60,
        "manufacturability": 0.65, "yield_packaging_3d": 0.75, "pcie_opencl_openvino": 0.55,
        "cost_access": 0.80, "risk_fto_modularity": 0.80,
        "notes": "Most practical/open path (A1+G1+B3, passive dielectrics + ref A1). Thermal for PCM writes and ring stabilization dominate; 2.5D integration feasible."
    },
    "G2": {
        "optical_compute": 0.75, "memory_hierarchy": 0.45, "thermal_control": 0.75,
        "manufacturability": 0.70, "yield_packaging_3d": 0.80, "pcie_opencl_openvino": 0.55,
        "cost_access": 0.55, "risk_fto_modularity": 0.55,
        "notes": "High speed/BW via EO-tuned membranes; volatile/low NV capacity, EO platform dependence and driver/RF thermal load need management."
    },
    "G3": {
        "optical_compute": 0.72, "memory_hierarchy": 0.75, "thermal_control": 0.55,
        "manufacturability": 0.60, "yield_packaging_3d": 0.70, "pcie_opencl_openvino": 0.55,
        "cost_access": 0.55, "risk_fto_modularity": 0.60,
        "notes": "Balanced NV+fast trim (PCM+EO). Localized PCM write heat (300C) with EO co-integration is the main constraint; good memory density."
    },
    "H1": {
        "optical_compute": 0.70, "memory_hierarchy": 0.85, "thermal_control": 0.45,
        "manufacturability": 0.40, "yield_packaging_3d": 0.35, "pcie_opencl_openvino": 0.50,
        "cost_access": 0.45, "risk_fto_modularity": 0.55,
        "notes": "High NV volumetric capacity (3D brush). Feasibility gated by 3D alignment/yield and heat extraction (segmented heaters, spreader/manifold, sequencing)."
    },
    "H4": {
        "optical_compute": 0.78, "memory_hierarchy": 0.85, "thermal_control": 0.35,
        "manufacturability": 0.35, "yield_packaging_3d": 0.30, "pcie_opencl_openvino": 0.45,
        "cost_access": 0.35, "risk_fto_modularity": 0.40,
        "notes": "Max capacity/throughput potential (tensor volumetric). Highest integration/thermal/alignment burden and FTO sensitivity; requires aggressive 3D packaging/cooling."
    },
}

AXIS_W = {
    "optical_compute": 0.15, "memory_hierarchy": 0.12, "thermal_control": 0.18,
    "manufacturability": 0.15, "yield_packaging_3d": 0.12, "pcie_opencl_openvino": 0.10,
    "cost_access": 0.08, "risk_fto_modularity": 0.10,
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)

    obj = load_json(os.path.join(OUT, "objective_combo_analysis.json"))
    mfg = load_json(os.path.join(OUT, "manufacturable_dimensions.json"))

    variants = {v["key"]: v for v in obj["variants"]}
    fab = {p["key"]: p for p in mfg["proposals"]}
    mod = {}
    for e in mfg["ai_module_estimates"]:
        mod.setdefault(e["proposal"], {})[e["class"]] = e

    rows = []
    for k in PRIORITY:
        v = variants.get(k, {})
        f = fab.get(k, {})
        ax = AXES[k]
        score = sum(ax[a] * AXIS_W[a] for a in AXIS_W)
        # pick edge/workstation module estimates if present
        edge = mod.get(k, {}).get("Edge AI NPU-like", {})
        ws = mod.get(k, {}).get("Workstation/GPU-like", {})
        dc = mod.get(k, {}).get("Datacenter TPU/GPU-like (per accelerator)", {})
        rows.append({
            "key": k,
            "name": v.get("name", k),
            "overall_rank": obj["rankings_objective"]["overall"].index(k) + 1 if k in obj["rankings_objective"]["overall"] else None,
            "open_access_rank": obj["rankings_objective"]["open_access"].index(k) + 1 if k in obj["rankings_objective"]["open_access"] else None,
            "feasibility_rank": obj["rankings_objective"]["feasibility"].index(k) + 1 if k in obj["rankings_objective"]["feasibility"] else None,
            "obj_overall": v.get("obj_overall"),
            "obj_feasibility": v.get("obj_feasibility"),
            "balanced_eff_tops": v.get("balanced_eff_tops"),
            "throughput_tops_tile": v.get("throughput_tops_tile"),
            "memory_capacity_mb_module": v.get("memory_capacity_mb_module"),
            "memory_bandwidth_tbps": v.get("memory_bandwidth_tbps"),
            "fab_cell_area_um2": f.get("fab_cell_area_um2"),
            "fab_cell_volume_um3": f.get("fab_cell_volume_um3"),
            "fab_vertical_pitch_um": f.get("fab_vertical_pitch_um"),
            "thermal_control_elements": f.get("thermal_control_elements"),
            "module_edge_footprint_cm": edge.get("est_footprint_cm"),
            "module_edge_volume_cm3": edge.get("est_module_volume_cm3"),
            "module_ws_footprint_cm": ws.get("est_footprint_cm"),
            "module_ws_volume_cm3": ws.get("est_module_volume_cm3"),
            "module_dc_footprint_cm": dc.get("est_footprint_cm"),
            "module_dc_volume_cm3": dc.get("est_module_volume_cm3"),
            "feasibility_scorecard_0_1": round(score, 4),
            **{f"axis_{a}": ax[a] for a in AXIS_W},
            "notes": ax["notes"],
        })

    # Simulation milestones and experiment mapping
    milestones = [
        {
            "id": "S1", "phase": "Simulación (ahora)", "title": "Presupuestos óptico/térmico/enlace por candidato",
            "description": "Modelo de pérdidas/IL, fase y SNR por ruta (G1/G2/G3/A1/B3), presupuesto de potencia láser/detectores, mapa térmico 3D transitorio (escritura PCM 300C, VO2 <68C, drivers EO/rings), y márgenes vs dimensiones fabricables.",
            "candidates": "H3,G2,G3,H1,H4",
            "outputs": "tablas de margen (dB, °C), sensibilidades, puntos de operación seguros",
            "exit_criteria": "Márgenes positivos en casos nominal y peor-caso paramétrico; pitch/aislamiento coherentes con fabricable"
        },
        {
            "id": "S2", "phase": "Simulación (ahora)", "title": "Rendimiento sistema y memoria (M0-M3/OMCC)",
            "description": "Extender simulate_opgpu_system y modelos de jerarquía: throughput efectivo bajo colas DMA/PCIe, latencia E2E, persistencia de pesos, refresco M2, políticas de scheduling térmico y arbitraje OMCC por perfil (GPU/NPU/TPU, OpenCL).",
            "candidates": "H3 (base), G2/G3, H1/H4",
            "outputs": "TOPS efectivos, utilización, BW, contención térmica, escenarios edge/ws/dc",
            "exit_criteria": "Cumplimiento de objetivos de clase (edge/ws/dc) dentro de incertidumbre modelada o brechas cuantificadas"
        },
        {
            "id": "S3", "phase": "Simulación (ahora)", "title": "Compatibilidad electrónica y software (PCIe/OpenCL/OpenVINO)",
            "description": "Modelar latencia/ancho de banda del borde (PCIe/DMA/MSI-X, colas), coste de microsecuencias y partición de kernels; definir cobertura de operadores y cuantización/calibración para precisión analógica (ruta OpenVINO heterogénea/plugin).",
            "candidates": "Plataforma común + módulos",
            "outputs": "presupuesto de latencia E2E, mapa de ops soportadas/fallback, requisitos de ICD/plugin",
            "exit_criteria": "Ruta Nivel 1→2 OpenCL y demo OpenVINO (C/D) viable en simulación funcional"
        },
        {
            "id": "S4", "phase": "Simulación (ahora)", "title": "Fiabilidad, variabilidad y yield",
            "description": "Monte Carlo de variaciones de proceso (n, d, acoplos, fase, térmica), deriva, endurance/retención, ECC/RAS y redundancia; estimar rendimiento funcional vs overhead (handicap fabricable).",
            "candidates": "H3,G2,G3 (2.5D) y H1,H4 (3D)",
            "outputs": "distribuciones de rendimiento, tasas de fallo, políticas de calibración/RAS",
            "exit_criteria": "Yield modelado aceptable para prototipo de laboratorio y ruta de mejora definida"
        },
        {
            "id": "E1", "phase": "Experimentos (posterior)", "title": "Celdas y materiales (prueba de concepto)",
            "description": "Caracterizar elementos unitarios: membranas λ/4n (G1), sintonía EO (G2), conmutación/escritura PCM y retención (A1/G3), anillos WDM (B3), pérdidas y estabilidad térmica.",
            "candidates": "G1→B3/A1→G2/G3",
            "outputs": "n, Δn, IL, ER, velocidad, energía, ciclos, retención, dependencia térmica",
            "exit_criteria": "Parámetros medidos dentro de rangos usados en S1-S4 o modelo actualizado"
        },
        {
            "id": "E2", "phase": "Experimentos (posterior)", "title": "Integración 2.5D y control térmico",
            "description": "Prototipo de submódulo (p. ej. H3 o G3) con actuadores térmicos/EO, sensado y secuenciado OMCC; validar aislamiento 300C/68C, calibración y RAS básico.",
            "candidates": "H3, G3",
            "outputs": "mapas térmicos medidos, estabilidad, eye/SNR, consumo, repetibilidad",
            "exit_criteria": "Operación estable bajo perfiles de escritura/reconfiguración definidos"
        },
        {
            "id": "E3", "phase": "Experimentos (posterior)", "title": "Borde electrónico y enlace de sistema",
            "description": "Bring-up PCIe/DMA/MSI-X en FPGA, cadena E/O-O/E, latencia E2E y demo de kernel (GEMM/conv) con runtime; prueba de ruta OpenVINO heterogénea.",
            "candidates": "Plataforma común",
            "outputs": "link up, throughput/latencia medidos, exactitud funcional vs referencia",
            "exit_criteria": "Ejecución end-to-end correcta con telemetría y métricas reportadas"
        },
        {
            "id": "E4", "phase": "Experimentos (posterior)", "title": "Módulo integrado y escalado 3D",
            "description": "Integración de candidato seleccionado (H3/G3 y, si procede, H1/H4) en módulo con empaquetado/térmica; evaluación de rendimiento, densidad y fiabilidad a escala.",
            "candidates": "H3/G3 → H1/H4",
            "outputs": "TOPS/W, capacidad, estabilidad a largo plazo, yield",
            "exit_criteria": "Demostración de viabilidad para clase objetivo (edge/ws) con datos reproducibles"
        },
    ]

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "goal": "Hacer posible el objetivo OPGPU: primero con simulaciones, luego experimentos",
        "priority_order": PRIORITY,
        "targets": TARGETS,
        "scorecard_axes_weights": AXIS_W,
        "candidates": rows,
        "milestones": milestones,
        "assumptions": [
            "Consolidación conceptual basada en outputs existentes (objective, manufacturable, P1-P3, sistema); no mediciones ni diseño listo para fabricación.",
            "Puntajes de ejes (0-1) son heurísticos y deben recalibrarse con resultados de simulación/experimentos.",
            "El control térmico factible (PCM ~300C, VO2 <68C, spreading/TEC, secuenciado OMCC) es condición habilitante.",
            "Compatibilidad OpenCL/OpenVINO depende de madurez de runtime/compilador/ICD y de precisión analógica; PCIe/OpenCL/OpenVINO nominativos.",
        ],
    }

    # JSON
    with open(os.path.join(OUT, "feasibility_roadmap.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # CSV scorecard
    csv_path = os.path.join(OUT, "feasibility_roadmap_scorecard.csv")
    if rows:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    # Markdown
    md = []
    md.append("# Hoja de ruta de viabilidad (simulación primero, luego experimentos)")
    md.append("")
    md.append(f"> Generado: {summary['generated_at']} (UTC). Consolidación conceptual basada en outputs del repositorio; no mediciones.")
    md.append("")
    md.append("## 1. Prioridad y objetivo")
    md.append("")
    md.append("Candidatos priorizados (estrategia actual): **H3** (abierto/factible), **G2** (velocidad/BW), **G3** (NV+ajuste equilibrado), **H1** (NV volumétrico), **H4** (techo de capacidad).")
    md.append("Objetivo: alcanzar viabilidad demostrable por clase (edge/workstation/datacenter) mediante simulaciones que cierren presupuestos físicos y de sistema, y derivar experimentos específicos.")
    md.append("")
    md.append("## 2. Scorecard de viabilidad (0–1, heurístico)")
    md.append("")
    headers = ["Candidato","Nombre","Scorecard","Óptica/cómputo","Memoria M0-M3","Térmica/control","Fabricabilidad","Yield/empaque/3D","PCIe/OpenCL/OpenVINO","Coste/acceso","Riesgo FTO/mod.","TOPS bal.","Mem (MB)","BW (TB/s)","Área celda (µm²)","Huella edge","Huella ws"]
    md.append("| " + " | ".join(headers) + " |")
    md.append("|" + "|".join(["---"]*len(headers)) + "|")
    for r in rows:
        md.append("| {key} | {name} | {sc:.3f} | {oc} | {mh} | {th} | {mf} | {yp} | {sw} | {ca} | {rf} | {bt} | {mem} | {bw} | {ca2} | {fe} | {fw} |".format(
            key=r["key"], name=r["name"], sc=r["feasibility_scorecard_0_1"],
            oc=r["axis_optical_compute"], mh=r["axis_memory_hierarchy"], th=r["axis_thermal_control"],
            mf=r["axis_manufacturability"], yp=r["axis_yield_packaging_3d"], sw=r["axis_pcie_opencl_openvino"],
            ca=r["axis_cost_access"], rf=r["axis_risk_fto_modularity"],
            bt=r["balanced_eff_tops"], mem=r["memory_capacity_mb_module"], bw=r["memory_bandwidth_tbps"],
            ca2=r["fab_cell_area_um2"], fe=r["module_edge_footprint_cm"], fw=r["module_ws_footprint_cm"],
        ))
    md.append("")
    md.append("## 3. Hitos de simulación (primero) y experimentos (después)")
    md.append("")
    for m in milestones:
        md.append(f"### {m['id']} — {m['title']} ({m['phase']})")
        md.append(f"- **Candidatos:** {m['candidates']}")
        md.append(f"- **Descripción:** {m['description']}")
        md.append(f"- **Salidas:** {m['outputs']}")
        md.append(f"- **Criterio de salida:** {m['exit_criteria']}")
        md.append("")
    md.append("## 4. Recomendación de secuencia")
    md.append("")
    md.append("1. **H3** como vía de menor riesgo para cerrar S1–S4 y E1–E3 (pasivos + ref A1, control térmico acotado).")
    md.append("2. **G3/G2** en paralelo para madurar memoria NV+ajuste y ruta EO de alta velocidad (dependencias EO/RF aisladas modularmente).")
    md.append("3. **H1/H4** tras validar térmica 3D, yield y empaquetado (simulación térmica 3D y de alineación como precondición de E4).")
    md.append("4. Mantener interfaz común (óptica/eléctrica/térmica/OMCC) y repos/candidatos modulares para aislar bloqueos.")
    md.append("")
    md.append("## 5. Supuestos y limitaciones")
    md.append("")
    for a in summary["assumptions"]:
        md.append(f"- {a}")
    md.append("")
    with open(os.path.join(OUT, "feasibility_roadmap.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    # Simple figure: scorecard bars (matplotlib)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        axes_keys = list(AXIS_W.keys())
        labels = ["opt", "mem", "therm", "mfg", "yield/3D", "PCIe/SW", "cost", "FTO/mod"]
        x = np.arange(len(axes_keys))
        width = 0.15
        fig, ax = plt.subplots(figsize=(10, 4.5))
        for i, r in enumerate(rows):
            vals = [r[f"axis_{a}"] for a in axes_keys]
            ax.bar(x + (i - 2) * width, vals, width, label=r["key"])
        ax.set_ylabel("Score (0-1, heurístico)")
        ax.set_title("Feasibility scorecard por eje (candidatos priorizados)")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        ax.legend(ncol=5, fontsize=8)
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "feasibility_scorecard_axes.png"), dpi=150)
        plt.close(fig)

        # overall scorecard
        fig, ax = plt.subplots(figsize=(6, 3.5))
        keys = [r["key"] for r in rows]
        vals = [r["feasibility_scorecard_0_1"] for r in rows]
        ax.bar(keys, vals, color=["#4c78a8", "#f58518", "#54a24b", "#e45756", "#72b7b2"])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Scorecard ponderado (0-1)")
        ax.set_title("Viabilidad integrada (simulación/realización)")
        for i, v in enumerate(vals):
            ax.text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=9)
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "feasibility_scorecard_overall.png"), dpi=150)
        plt.close(fig)
    except Exception as e:
        print("figure_warning:", e)

    print(json.dumps({"candidates": len(rows), "milestones": len(milestones), "out": "outputs/feasibility_roadmap.*"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
