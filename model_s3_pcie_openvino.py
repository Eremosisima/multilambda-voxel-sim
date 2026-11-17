#!/usr/bin/env python3
"""
S3: PCIe bridge end-to-end latency/bandwidth and OpenVINO compatibility path model.
Conceptual functional model (no hardware measurements).
"""
from __future__ import annotations

import csv
import json
import math
import os

OUT = "outputs"
FIG = "figures"

# PCIe configs: (label, lanes, gen_gt_s, eff_factor)
PCIE = [
    ("Gen3 x8", 8, 8.0, 0.80),
    ("Gen4 x8", 8, 16.0, 0.82),
    ("Gen4 x16", 16, 16.0, 0.83),
    ("Gen5 x16", 16, 32.0, 0.84),
]

# Pipeline stage latencies in microseconds (conceptual)
STAGES_US = {
    "doorbell_mmio": 0.6,
    "descriptor_fetch_dma": 1.2,
    "command_parse_schedule": 0.8,
    "microseq_setup": 1.5,
    "eo_conversion_tx": 0.4,
    "optical_compute_1k_mac_equiv": 0.05,  # scales with work
    "oe_conversion_rx": 0.5,
    "completion_dma_msi": 1.0,
}

# Workloads (approx activation/weight/result bytes and compute units, conceptual)
WORKLOADS = [
    {"name": "GEMM_small", "h2d_kb": 64, "d2h_kb": 16, "compute_units": 2e6, "batch_ops": 1},
    {"name": "GEMM_large", "h2d_kb": 4096, "d2h_kb": 1024, "compute_units": 2e8, "batch_ops": 1},
    {"name": "Conv_tile", "h2d_kb": 512, "d2h_kb": 256, "compute_units": 5e7, "batch_ops": 1},
    {"name": "Attention_block_proxy", "h2d_kb": 2048, "d2h_kb": 512, "compute_units": 1.2e8, "batch_ops": 1},
    {"name": "Batched_inference_8", "h2d_kb": 1024, "d2h_kb": 128, "compute_units": 8e7, "batch_ops": 8},
]

OPENVINO = {
    "routes": [
        {
            "id": "A",
            "name": "Plugin OpenVINO nativo",
            "maturity": "medio plazo",
            "operator_coverage_target": "alto (subgrafos MatMul/Conv/FC y fusiones objetivo)",
            "precision_path": "INT8/FP16 calibrado + verificación de exactitud analógica",
            "dependency": "runtime/driver estable y compilador de microprogramas",
            "performance": "mejor (control directo, tiling/fusión)",
            "effort": "alto",
            "recommended_phase": "S3→E3 evolución"
        },
        {
            "id": "B",
            "name": "Vía backend OpenCL de OpenVINO (ICD OPGPU)",
            "maturity": "condicionada",
            "operator_coverage_target": "media (lo que genere el plugin OpenCL y soporte el compilador OPGPU)",
            "precision_path": "formatos soportados por ICD + calibración",
            "dependency": "ICD OpenCL Nivel 2 suficientemente compatible",
            "performance": "media",
            "effort": "medio",
            "recommended_phase": "tras S3 Nivel 1→2"
        },
        {
            "id": "C",
            "name": "Heterogéneo (OPGPU + CPU/GPU fallback)",
            "maturity": "corto plazo",
            "operator_coverage_target": "parcial en OPGPU, resto fallback",
            "precision_path": "mixta; validar partición y acumulación",
            "dependency": "runtime y particionado de grafo",
            "performance": "dependiente de partición",
            "effort": "medio",
            "recommended_phase": "S3 demostración inicial"
        },
        {
            "id": "D",
            "name": "Blobs/redes precompiladas",
            "maturity": "corto plazo",
            "operator_coverage_target": "topologías fijas soportadas",
            "precision_path": "calibración por modelo",
            "dependency": "toolchain de compilación offline",
            "performance": "buena en casos fijos",
            "effort": "bajo-medio",
            "recommended_phase": "S3/E3 demos"
        },
    ],
    "operator_support_initial": [
        {"op": "MatMul/GEMM", "priority": "P0", "status": "objetivo directo (núcleo óptico)", "route": "A/B/C/D"},
        {"op": "Convolution", "priority": "P0", "status": "vía im2col+GEMM/tiling", "route": "A/B/C/D"},
        {"op": "FullyConnected", "priority": "P0", "status": "GEMM", "route": "A/B/C/D"},
        {"op": "Add/Mul (eltwise)", "priority": "P1", "status": "posible en dominio óptico/mixto", "route": "A/B/C"},
        {"op": "Activation (ReLU/GELU approx)", "priority": "P1", "status": "aprox. óptica/LUT o borde/host", "route": "A/C"},
        {"op": "Softmax/LayerNorm", "priority": "P1", "status": "preferente fallback o bloque mixto", "route": "C (A futuro)"},
        {"op": "Attention (compuesto)", "priority": "P2", "status": "descomposición (MatMul+softmax+eltwise)", "route": "C/A"},
        {"op": "Quantize/Dequantize", "priority": "P1", "status": "en frontera E/O-O/E y runtime", "route": "A/B/C/D"},
    ],
    "notes": "La precisión analógica/ruido/deriva exige cuantización calibrada y reporting de exactitud (no bit-exact)."
}


def bw_gbps(lanes, gt_s, eff):
    # GT/s * lanes * eff / 8 (approx for 128b/130b-like efficiency)
    return lanes * gt_s * eff / 8.0


def transfer_us(kb, gbps):
    if gbps <= 0:
        return float("inf")
    bits = kb * 1024 * 8
    return (bits / (gbps * 1e9)) * 1e6


def model():
    rows = []
    for pcie in PCIE:
        label, lanes, gt, eff = pcie
        g = bw_gbps(lanes, gt, eff)
        for w in WORKLOADS:
            t_h2d = transfer_us(w["h2d_kb"], g)
            t_d2h = transfer_us(w["d2h_kb"], g)
            fixed = (STAGES_US["doorbell_mmio"] + STAGES_US["descriptor_fetch_dma"] +
                     STAGES_US["command_parse_schedule"] + STAGES_US["microseq_setup"] +
                     STAGES_US["eo_conversion_tx"] + STAGES_US["oe_conversion_rx"] +
                     STAGES_US["completion_dma_msi"])
            compute = (w["compute_units"] / 1000.0) * STAGES_US["optical_compute_1k_mac_equiv"]
            # simple overlap: DMA can overlap partially with compute for batched/streamed cases
            overlap = 0.3 * min(t_h2d + t_d2h, compute) if w["batch_ops"] > 1 or w["compute_units"] > 5e7 else 0.0
            total = fixed + t_h2d + compute + t_d2h - overlap
            rows.append({
                "pcie": label,
                "pcie_gbps_eff": round(g, 2),
                "workload": w["name"],
                "h2d_kb": w["h2d_kb"],
                "d2h_kb": w["d2h_kb"],
                "compute_units": w["compute_units"],
                "t_h2d_us": round(t_h2d, 3),
                "t_compute_us": round(compute, 3),
                "t_d2h_us": round(t_d2h, 3),
                "t_fixed_us": round(fixed, 3),
                "overlap_us": round(overlap, 3),
                "t_total_us": round(total, 3),
                "t_total_ms": round(total / 1000.0, 4),
            })
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    rows = model()
    summary = {
        "assumptions": {
            "pcie": [{"label": p[0], "lanes": p[1], "gt_s": p[2], "eff": p[3], "gbps_eff": round(bw_gbps(*p[1:]), 2)} for p in PCIE],
            "stages_us": STAGES_US,
            "overlap_model": "simple partial overlap for batched/large compute workloads",
        },
        "latency_results": rows,
        "openvino": OPENVINO,
        "disclaimer": "Conceptual S3 model for planning; validate with RTL/FPGA bring-up, driver traces, and real kernel graphs.",
    }
    with open(os.path.join(OUT, "s3_pcie_openvino.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT, "s3_pcie_latency.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    md = ["# S3 — PCIe/E2E latencia y ruta de compatibilidad OpenVINO (conceptual)", "",
          "> Modelo funcional para planificación S3. No son mediciones; validar con bring-up FPGA, trazas de driver y grafos reales.", "",
          "## Latencia E2E estimada (µs)", "",
          "| PCIe | Carga | H2D (µs) | Cómputo (µs) | D2H (µs) | Fijo (µs) | Solape (µs) | Total (µs) | Total (ms) |",
          "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        md.append(f"| {r['pcie']} | {r['workload']} | {r['t_h2d_us']} | {r['t_compute_us']} | {r['t_d2h_us']} | {r['t_fixed_us']} | {r['overlap_us']} | {r['t_total_us']} | {r['t_total_ms']} |")
    md += ["", "## Rutas de compatibilidad OpenVINO", "",
           "| Ruta | Madurez | Cobertura objetivo | Precisión | Dependencia | Rendimiento | Fase |",
           "|---|---|---|---|---|---|---|"]
    for r in OPENVINO["routes"]:
        md.append(f"| {r['id']} {r['name']} | {r['maturity']} | {r['operator_coverage_target']} | {r['precision_path']} | {r['dependency']} | {r['performance']} | {r['recommended_phase']} |")
    md += ["", "## Cobertura inicial de operadores (objetivo)", "",
           "| Operador | Prioridad | Estado | Rutas |",
           "|---|---|---|---|"]
    for op in OPENVINO["operator_support_initial"]:
        md.append(f"| {op['op']} | {op['priority']} | {op['status']} | {op['route']} |")
    md += ["", "## Recomendaciones S3", "- Priorizar ruta **C/D** para demo funcional temprana (GEMM/Conv) y evolucionar a **B/A** según madurez de ICD/compilador.",
           "- Modelar colas reales (doorbells, MSI-X, batching) y contención DMA en `simulate_opgpu_system.py` para perfiles edge/ws/dc.",
           "- Definir flujo de cuantización/calibración y métricas de exactitud vs referencia para cargas OpenVINO."]
    with open(os.path.join(OUT, "s3_pcie_openvino.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # Plot Gen4 x8 totals per workload
        subset = [r for r in rows if r["pcie"] == "Gen4 x8"]
        names = [r["workload"] for r in subset]
        totals = [r["t_total_ms"] for r in subset]
        fig, ax = plt.subplots(figsize=(8, 3.8))
        ax.bar(names, totals, color="#72b7b2")
        ax.set_ylabel("Latencia E2E (ms)")
        ax.set_title("S3: Latencia E2E estimada (PCIe Gen4 x8)")
        ax.tick_params(axis='x', rotation=20)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "s3_pcie_latency_gen4x8.png"), dpi=150)
        plt.close(fig)
    except Exception as e:
        print("figure_warning:", e)

    print(json.dumps({"rows": len(rows), "pcie_configs": len(PCIE), "workloads": len(WORKLOADS), "out": "outputs/s3_pcie_openvino.*"}))


if __name__ == "__main__":
    main()
