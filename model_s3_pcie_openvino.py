#!/usr/bin/env python3
"""
S3: PCIe bridge end-to-end latency/bandwidth, queue contention, and OpenVINO compatibility/partition model.
Conceptual functional model (no hardware measurements).
Outputs: outputs/s3_pcie_openvino.{json,md}, outputs/s3_pcie_latency.csv, outputs/s3_queue_contention.csv,
         outputs/s3_openvino_partition.csv, figures/s3_pcie_latency_gen4x8.png, figures/s3_queue_openvino.png
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
        {"id": "A", "name": "Plugin OpenVINO nativo", "maturity": "medio plazo", "operator_coverage_target": "alto (subgrafos MatMul/Conv/FC y fusiones objetivo)", "precision_path": "INT8/FP16 calibrado + verificación de exactitud analógica", "dependency": "runtime/driver estable y compilador de microprogramas", "performance": "mejor (control directo, tiling/fusión)", "effort": "alto", "recommended_phase": "S3→E3 evolución"},
        {"id": "B", "name": "Vía backend OpenCL de OpenVINO (ICD OPGPU)", "maturity": "condicionada", "operator_coverage_target": "media (lo que genere el plugin OpenCL y soporte el compilador OPGPU)", "precision_path": "formatos soportados por ICD + calibración", "dependency": "ICD OpenCL Nivel 2 suficientemente compatible", "performance": "media", "effort": "medio", "recommended_phase": "tras S3 Nivel 1→2"},
        {"id": "C", "name": "Heterogéneo (OPGPU + CPU/GPU fallback)", "maturity": "corto plazo", "operator_coverage_target": "parcial en OPGPU, resto fallback", "precision_path": "mixta; validar partición y acumulación", "dependency": "runtime y particionado de grafo", "performance": "dependiente de partición", "effort": "medio", "recommended_phase": "S3 demostración inicial"},
        {"id": "D", "name": "Blobs/redes precompiladas", "maturity": "corto plazo", "operator_coverage_target": "topologías fijas soportadas", "precision_path": "calibración por modelo", "dependency": "toolchain de compilación offline", "performance": "buena en casos fijos", "effort": "bajo-medio", "recommended_phase": "S3/E3 demos"},
    ],
    "operator_support_initial": [
        {"op": "MatMul/GEMM", "priority": "P0", "status": "objetivo directo (núcleo óptico)", "route": "A/B/C/D", "opgpu_offloadable": 1.0},
        {"op": "Convolution", "priority": "P0", "status": "vía im2col+GEMM/tiling", "route": "A/B/C/D", "opgpu_offloadable": 0.95},
        {"op": "FullyConnected", "priority": "P0", "status": "GEMM", "route": "A/B/C/D", "opgpu_offloadable": 1.0},
        {"op": "Add/Mul (eltwise)", "priority": "P1", "status": "posible en dominio óptico/mixto", "route": "A/B/C", "opgpu_offloadable": 0.7},
        {"op": "Activation (ReLU/GELU approx)", "priority": "P1", "status": "aprox. óptica/LUT o borde/host", "route": "A/C", "opgpu_offloadable": 0.5},
        {"op": "Softmax/LayerNorm", "priority": "P1", "status": "preferente fallback o bloque mixto", "route": "C (A futuro)", "opgpu_offloadable": 0.2},
        {"op": "Attention (compuesto)", "priority": "P2", "status": "descomposición (MatMul+softmax+eltwise)", "route": "C/A", "opgpu_offloadable": 0.6},
        {"op": "Quantize/Dequantize", "priority": "P1", "status": "en frontera E/O-O/E y runtime", "route": "A/B/C/D", "opgpu_offloadable": 0.8},
    ],
    "notes": "La precisión analógica/ruido/deriva exige cuantización calibrada y reporting de exactitud (no bit-exact)."
}

# Representative OpenVINO graph mixes for partition/coverage simulation
GRAPH_MIXES = [
    {"graph": "CNN_inference", "ops": {"MatMul/GEMM": 0.10, "Convolution": 0.55, "FullyConnected": 0.10, "Add/Mul (eltwise)": 0.10, "Activation (ReLU/GELU approx)": 0.10, "Quantize/Dequantize": 0.05}},
    {"graph": "Transformer_encoder_block", "ops": {"MatMul/GEMM": 0.45, "FullyConnected": 0.10, "Add/Mul (eltwise)": 0.10, "Activation (ReLU/GELU approx)": 0.05, "Softmax/LayerNorm": 0.15, "Attention (compuesto)": 0.10, "Quantize/Dequantize": 0.05}},
    {"graph": "MLP_classifier", "ops": {"MatMul/GEMM": 0.20, "FullyConnected": 0.55, "Add/Mul (eltwise)": 0.10, "Activation (ReLU/GELU approx)": 0.10, "Quantize/Dequantize": 0.05}},
]


def bw_gbps(lanes, gt_s, eff):
    return lanes * gt_s * eff / 8.0


def transfer_us(kb, gbps):
    if gbps <= 0:
        return float("inf")
    bits = kb * 1024 * 8
    return (bits / (gbps * 1e9)) * 1e6


def model_latency():
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
            overlap = 0.3 * min(t_h2d + t_d2h, compute) if w["batch_ops"] > 1 or w["compute_units"] > 5e7 else 0.0
            total = fixed + t_h2d + compute + t_d2h - overlap
            rows.append({
                "pcie": label, "pcie_gbps_eff": round(g, 2), "workload": w["name"],
                "h2d_kb": w["h2d_kb"], "d2h_kb": w["d2h_kb"], "compute_units": w["compute_units"],
                "t_h2d_us": round(t_h2d, 3), "t_compute_us": round(compute, 3), "t_d2h_us": round(t_d2h, 3),
                "t_fixed_us": round(fixed, 3), "overlap_us": round(overlap, 3),
                "t_total_us": round(total, 3), "t_total_ms": round(total / 1000.0, 4),
            })
    return rows


def model_queue_contention():
    # Queue/DMA contention scenarios (conceptual): depth, batch, MSI-X coalescing/doorbell pressure
    scenarios = [
        {"name": "single_stream", "queue_depth": 1, "concurrency": 1, "msix_coalesce": 1, "dma_channels": 1},
        {"name": "pipelined_stream", "queue_depth": 8, "concurrency": 2, "msix_coalesce": 2, "dma_channels": 2},
        {"name": "batched_inference", "queue_depth": 16, "concurrency": 4, "msix_coalesce": 4, "dma_channels": 2},
        {"name": "multi_tenant", "queue_depth": 32, "concurrency": 8, "msix_coalesce": 4, "dma_channels": 4},
    ]
    # base per-request service from Gen4 x8 representative workloads
    base_service_ms = {
        "GEMM_small": 0.156, "GEMM_large": 12.244, "Conv_tile": 2.986, "Attention_block_proxy": 7.125, "Batched_inference_8": 4.510
    }
    rows = []
    for s in scenarios:
        for w, base in base_service_ms.items():
            util = min(0.98, 0.35 + 0.08*s["concurrency"] + (0.04 if w in ("GEMM_large","Attention_block_proxy") else 0.02))
            # contention inflates effective service and adds queueing; batching/coalescing helps
            contention = 1.0 + 0.18*max(0, s["concurrency"]-s["dma_channels"]) + 0.06*math.log2(max(1,s["queue_depth"]))
            mitigation = 1.0 - (0.05*math.log2(max(1,s["msix_coalesce"])) + 0.04*math.log2(max(1,s["dma_channels"])) + (0.03 if s["queue_depth"]>=8 else 0.0))
            eff_service = base * max(0.75, contention*max(0.7, mitigation))
            # M/M/1-like approximation scaled (conceptual)
            q_wait = 0.0 if util >= 0.999 else eff_service * (util/(1.0-util)) * (0.4 + 0.1*s["concurrency"])
            # pipelining overlap benefit for deeper queues
            overlap_gain = 0.12 if s["queue_depth"]>=8 else 0.0
            e2e = max(eff_service, eff_service + q_wait*(1.0-overlap_gain))
            rows.append({
                "scenario": s["name"], "workload": w, "queue_depth": s["queue_depth"], "concurrency": s["concurrency"],
                "dma_channels": s["dma_channels"], "msix_coalesce": s["msix_coalesce"],
                "utilization_est": round(util,3), "eff_service_ms": round(eff_service,4),
                "queue_wait_ms": round(q_wait,4), "e2e_ms_est": round(e2e,4),
                "throughput_rel": round((1.0/e2e)/(1.0/base),4)
            })
    return rows


def model_openvino_partition():
    off = {o["op"]: o["opgpu_offloadable"] for o in OPENVINO["operator_support_initial"]}
    routes = {
        "A_native": {"label": "A Plugin nativo (maduro objetivo)", "impl_factor": 0.95, "fallback_penalty": 1.15},
        "B_opencl": {"label": "B Backend OpenCL/ICD", "impl_factor": 0.80, "fallback_penalty": 1.20},
        "C_hetero": {"label": "C Heterogéneo OPGPU+fallback", "impl_factor": 0.70, "fallback_penalty": 1.35},
        "D_compiled": {"label": "D Blobs precompilados", "impl_factor": 0.75, "fallback_penalty": 1.10},
    }
    rows=[]
    for g in GRAPH_MIXES:
        for rid, r in routes.items():
            covered = 0.0
            for op, frac in g["ops"].items():
                covered += frac * off.get(op, 0.0) * r["impl_factor"]
            covered = min(1.0, covered)
            fallback = 1.0 - covered
            # performance proxy relative to ideal full offload (1.0)
            perf_rel = covered * 1.0 + fallback * (1.0 / r["fallback_penalty"])
            accuracy_risk = "bajo-medio" if covered>0.75 else ("medio" if covered>0.5 else "medio-alto")
            rows.append({
                "graph": g["graph"], "route": rid, "route_label": r["label"],
                "offload_coverage": round(covered,4), "fallback_fraction": round(fallback,4),
                "perf_proxy_rel": round(perf_rel,4), "accuracy_risk": accuracy_risk,
                "recommended": (rid in ("C_hetero","D_compiled") and covered>=0.45) or (rid in ("A_native","B_opencl") and covered>=0.65)
            })
    return rows


def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)
    lat_rows = model_latency()
    q_rows = model_queue_contention()
    part_rows = model_openvino_partition()

    summary = {
        "assumptions": {
            "pcie": [{"label": p[0], "lanes": p[1], "gt_s": p[2], "eff": p[3], "gbps_eff": round(bw_gbps(*p[1:]), 2)} for p in PCIE],
            "stages_us": STAGES_US,
            "overlap_model": "partial overlap for batched/large compute workloads",
            "queue_model": "utilization/contention approximation with DMA/MSI-X/coalescing and pipelining factors (conceptual)",
        },
        "latency_results": lat_rows,
        "queue_contention_results": q_rows,
        "openvino_partition_results": part_rows,
        "openvino": OPENVINO,
        "disclaimer": "Conceptual S3 model for planning; validate with RTL/FPGA bring-up, driver traces, and real kernel graphs.",
    }
    with open(os.path.join(OUT, "s3_pcie_openvino.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    def write_csv(name, rows):
        with open(os.path.join(OUT,name),"w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    write_csv("s3_pcie_latency.csv", lat_rows)
    write_csv("s3_queue_contention.csv", q_rows)
    write_csv("s3_openvino_partition.csv", part_rows)

    md = ["# S3 — PCIe/E2E, colas/DMA y compatibilidad/partición OpenVINO (conceptual)", "",
          "> Modelo funcional para planificación S3. No son mediciones; validar con bring-up FPGA, trazas de driver y grafos reales.", "",
          "## Latencia E2E estimada (µs)", "",
          "| PCIe | Carga | H2D (µs) | Cómputo (µs) | D2H (µs) | Fijo (µs) | Solape (µs) | Total (µs) | Total (ms) |",
          "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in lat_rows:
        md.append(f"| {r['pcie']} | {r['workload']} | {r['t_h2d_us']} | {r['t_compute_us']} | {r['t_d2h_us']} | {r['t_fixed_us']} | {r['overlap_us']} | {r['t_total_us']} | {r['t_total_ms']} |")

    md += ["", "## Contención de colas/DMA (Gen4 x8, conceptual)", "",
           "| Escenario | Carga | Prof. cola | Concurrencia | DMA | MSI-X | Utiliz. | Servicio eff (ms) | Espera cola (ms) | E2E est. (ms) | Throughput rel. |",
           "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in q_rows:
        md.append(f"| {r['scenario']} | {r['workload']} | {r['queue_depth']} | {r['concurrency']} | {r['dma_channels']} | {r['msix_coalesce']} | {r['utilization_est']} | {r['eff_service_ms']} | {r['queue_wait_ms']} | {r['e2e_ms_est']} | {r['throughput_rel']} |")

    md += ["", "## Partición/cobertura OpenVINO (grafos representativos)", "",
           "| Grafo | Ruta | Cobertura offload | Fallback | Rend. relativo (proxy) | Riesgo exactitud | Recomendado (S3) |",
           "|---|---|---:|---:|---:|---|:---:|"]
    for r in part_rows:
        md.append(f"| {r['graph']} | {r['route_label']} | {r['offload_coverage']} | {r['fallback_fraction']} | {r['perf_proxy_rel']} | {r['accuracy_risk']} | {'sí' if r['recommended'] else 'no'} |")

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

    md += ["", "## Recomendaciones S3",
           "- **Corto plazo:** rutas C/D para demo funcional (GEMM/Conv/MLP, CNN con fallback) con cuantización/calibración y reporte de exactitud.",
           "- **Evolución:** ruta B (ICD OpenCL maduro) y luego A (plugin nativo) para mayor cobertura/fusión y menor fallback en transformer/attention.",
           "- **Colas/DMA:** usar colas profundas + batching + coalescing MSI-X y múltiples canales DMA para sostener throughput; validar contención real en FPGA/driver.",
           "- Definir particionado de grafo y métricas de exactitud vs referencia por operador/subgrafo."]
    with open(os.path.join(OUT, "s3_pcie_openvino.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        subset = [r for r in lat_rows if r["pcie"] == "Gen4 x8"]
        names = [r["workload"] for r in subset]; totals = [r["t_total_ms"] for r in subset]
        fig, ax = plt.subplots(1,2,figsize=(11,4))
        ax[0].bar(names, totals, color="#72b7b2")
        ax[0].set_ylabel("Latencia E2E (ms)"); ax[0].set_title("S3: Latencia E2E (Gen4 x8)"); ax[0].tick_params(axis='x', rotation=20)
        # partition coverage for CNN vs Transformer
        graphs = [g['graph'] for g in GRAPH_MIXES]; routes = ['C_hetero','D_compiled','B_opencl','A_native']
        x=range(len(graphs)); w=0.18
        for i,rid in enumerate(routes):
            vals=[next(r['offload_coverage'] for r in part_rows if r['graph']==g and r['route']==rid) for g in graphs]
            ax[1].bar([xi+i*w for xi in x], vals, w, label=rid)
        ax[1].set_xticks([xi+1.5*w for xi in x]); ax[1].set_xticklabels(graphs, rotation=15); ax[1].set_ylim(0,1.05)
        ax[1].set_ylabel('Cobertura offload'); ax[1].set_title('S3: Cobertura OpenVINO por ruta/grafo'); ax[1].legend(fontsize=7)
        fig.tight_layout(); fig.savefig(os.path.join(FIG,'s3_queue_openvino.png'), dpi=150); plt.close(fig)
        # keep original name too
        fig2, ax2 = plt.subplots(figsize=(8,3.8))
        ax2.bar(names, totals, color="#72b7b2"); ax2.set_ylabel('Latencia E2E (ms)'); ax2.set_title('S3: Latencia E2E estimada (PCIe Gen4 x8)')
        ax2.tick_params(axis='x', rotation=20); fig2.tight_layout(); fig2.savefig(os.path.join(FIG,'s3_pcie_latency_gen4x8.png'), dpi=150); plt.close(fig2)
    except Exception as e:
        print("figure_warning:", e)

    print(json.dumps({"lat_rows": len(lat_rows), "queue_rows": len(q_rows), "partition_rows": len(part_rows), "out": "outputs/s3_pcie_openvino.*"}))

if __name__ == "__main__":
    main()
