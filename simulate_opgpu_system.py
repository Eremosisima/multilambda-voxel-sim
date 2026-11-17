#!/usr/bin/env python3
"""System-level simulation for OPGPU v0.4 (OpenCL-oriented optical GPU/NPU/TPU).

Models conceptually: PCIe command/transfer flow, optical tile execution (MVM/MAC),
memory hierarchy behavior (M0-M3), and mode-dependent metrics (GPU/NPU/TPU).
Outputs JSON/CSV/Markdown and simple figures under outputs/ and figures/.

This is a functional/performance *model*, not a wave-optics or signoff circuit sim.
"""
from __future__ import annotations

import csv
import json
import math
import os
import statistics
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None

OUT_DIR = "outputs"
FIG_DIR = "figures"


@dataclass
class SystemConfig:
    name: str
    mode: str  # GPU, NPU, TPU
    pcie_lanes: int = 16
    pcie_gen_gbps_per_lane: float = 32.0  # Gen5 x16 ~64 GB/s raw per dir, model effective
    pcie_efficiency: float = 0.75
    tiles: int = 64
    macs_per_tile_per_cycle: int = 4096  # effective optical MACs per scheduling cycle
    optical_clock_ghz: float = 2.0
    wdm_channels: int = 8
    m1_weight_gb: float = 2.0  # non-volatile optical (Sb2S3) effective capacity
    m2_buffer_mb: float = 64.0  # volatile optical (VO2)
    dac_adc_bits: int = 8
    eo_oe_latency_ns: float = 45.0
    cmd_latency_ns: float = 250.0
    sb2s3_program_us: float = 20.0  # per weight-block program event (amortized)
    vo2_switch_ns: float = 2.0
    energy_pj_per_mac: float = 0.8
    energy_pj_per_byte_pcie: float = 8.0
    energy_nj_per_m1_program: float = 50.0


def ensure_dirs() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def pcie_bandwidth_gbps(cfg: SystemConfig) -> float:
    # GB/s effective (one direction), simplified
    raw = cfg.pcie_lanes * cfg.pcie_gen_gbps_per_lane / 8.0
    return raw * cfg.pcie_efficiency


def peak_tops(cfg: SystemConfig) -> float:
    macs_per_s = cfg.tiles * cfg.macs_per_tile_per_cycle * cfg.optical_clock_ghz * 1e9 * cfg.wdm_channels
    # 1 MAC ~ 2 ops
    return (2.0 * macs_per_s) / 1e12


@dataclass
class Workload:
    name: str
    ops: float  # total operations
    bytes_in: float
    bytes_out: float
    weight_bytes: float
    weight_reuse: float  # times weights reused (>=1)
    m2_working_set_bytes: float
    intensity_ops_per_byte: float


def example_workloads() -> List[Workload]:
    return [
        Workload("GEMV_4k", ops=2*4096*4096, bytes_in=4096*2, bytes_out=4096*2, weight_bytes=4096*4096*2, weight_reuse=1, m2_working_set_bytes=4096*4, intensity_ops_per_byte=2.0),
        Workload("GEMM_1024", ops=2*(1024**3), bytes_in=2*1024*1024*2, bytes_out=1024*1024*2, weight_bytes=1024*1024*2, weight_reuse=1024, m2_working_set_bytes=8*1024*1024, intensity_ops_per_byte=512.0),
        Workload("Conv_infer_batch1", ops=2*64*64*128*3*3*128, bytes_in=64*64*128, bytes_out=64*64*128, weight_bytes=128*3*3*128, weight_reuse=4096, m2_working_set_bytes=4*1024*1024, intensity_ops_per_byte=300.0),
        Workload("Attention_block", ops=2*(512**3)*2, bytes_in=3*512*512*2, bytes_out=512*512*2, weight_bytes=3*512*512*2, weight_reuse=512, m2_working_set_bytes=16*1024*1024, intensity_ops_per_byte=200.0),
    ]


def mode_efficiency(cfg: SystemConfig, wl: Workload) -> float:
    # Utilization/efficiency factor by mode-workload affinity (conceptual)
    base = 0.55
    if cfg.mode == "TPU":
        base = 0.78 if wl.intensity_ops_per_byte >= 100 else 0.45
    elif cfg.mode == "NPU":
        base = 0.72 if wl.weight_reuse >= 64 else 0.5
    elif cfg.mode == "GPU":
        base = 0.6 if wl.intensity_ops_per_byte < 100 else 0.65
    # memory fit penalty
    if wl.m2_working_set_bytes > cfg.m2_buffer_mb * 1024 * 1024:
        base *= 0.7
    if wl.weight_bytes > cfg.m1_weight_gb * 1024**3:
        base *= 0.8
    return min(max(base, 0.05), 0.95)


def simulate_transfer(bytes_total: float, bw_gbps: float, overhead_ns: float) -> float:
    if bw_gbps <= 0:
        return float('inf')
    seconds = bytes_total / (bw_gbps * 1024**3)
    return seconds * 1e9 + overhead_ns


def simulate_workload(cfg: SystemConfig, wl: Workload) -> Dict:
    bw = pcie_bandwidth_gbps(cfg)
    peak = peak_tops(cfg)
    eff = mode_efficiency(cfg, wl)
    achieved_tops = peak * eff

    # Transfers: weights programmed/loaded once per reuse epoch (amortized by reuse)
    weight_transfer_bytes = wl.weight_bytes / max(wl.weight_reuse, 1.0)
    # If weights fit in M1 non-volatile, after first load/program they stay; model first-epoch cost separately
    in_ns = simulate_transfer(wl.bytes_in, bw, cfg.cmd_latency_ns + cfg.eo_oe_latency_ns)
    out_ns = simulate_transfer(wl.bytes_out, bw, cfg.cmd_latency_ns + cfg.eo_oe_latency_ns)
    wt_ns = simulate_transfer(weight_transfer_bytes, bw, cfg.cmd_latency_ns)

    compute_ns = (wl.ops / (achieved_tops * 1e12)) * 1e9 if achieved_tops > 0 else float('inf')
    # control/switching overhead
    control_ns = cfg.cmd_latency_ns + (wl.ops / max(cfg.macs_per_tile_per_cycle * cfg.tiles, 1)) * cfg.vo2_switch_ns
    total_ns = in_ns + out_ns + wt_ns + compute_ns + control_ns

    # Energy (very simplified)
    e_compute_pj = wl.ops/2.0 * cfg.energy_pj_per_mac  # per MAC
    e_pcie_pj = (wl.bytes_in + wl.bytes_out + weight_transfer_bytes) * cfg.energy_pj_per_byte_pcie
    e_program_pj = (wl.weight_bytes / (1024*1024)) * cfg.energy_nj_per_m1_program * 1000.0 / max(wl.weight_reuse,1.0)
    total_energy_uj = (e_compute_pj + e_pcie_pj + e_program_pj) / 1e6

    latency_ms = total_ns / 1e6
    achieved_ops_per_s = wl.ops / (total_ns / 1e9) if total_ns > 0 else 0
    tops_achieved_runtime = achieved_ops_per_s * 2 / 1e12  # rough

    return {
        "config": cfg.name,
        "mode": cfg.mode,
        "workload": wl.name,
        "peak_tops": round(peak, 3),
        "utilization": round(eff, 3),
        "achieved_tops_model": round(achieved_tops, 3),
        "runtime_tops_effective": round((wl.ops/1e12)/(total_ns/1e9) if total_ns>0 else 0, 3),
        "latency_ms": round(latency_ms, 6),
        "pcie_gbps_eff": round(bw, 3),
        "energy_uj": round(total_energy_uj, 3),
        "bottleneck": bottleneck(in_ns, out_ns, wt_ns, compute_ns, control_ns),
    }


def bottleneck(in_ns, out_ns, wt_ns, compute_ns, control_ns) -> str:
    parts = {
        "input_transfer": in_ns,
        "output_transfer": out_ns,
        "weight_transfer": wt_ns,
        "optical_compute": compute_ns,
        "control": control_ns,
    }
    return max(parts, key=parts.get)


def opencl_queue_sim(events: int = 32) -> Dict:
    # Simple discrete-event approximation of queued kernel launches
    rng = np.random.default_rng(42)
    submit = np.sort(rng.uniform(0, 5.0, size=events))  # ms
    service = rng.uniform(0.2, 1.2, size=events)  # ms
    start = np.zeros(events)
    finish = np.zeros(events)
    for i in range(events):
        ready = submit[i] if i == 0 else max(submit[i], finish[i-1])
        start[i] = ready + 0.05  # dispatch/doorbell overhead
        finish[i] = start[i] + service[i]
    queue_latency = start - submit
    turnaround = finish - submit
    return {
        "events": events,
        "avg_queue_ms": float(np.mean(queue_latency)),
        "p95_queue_ms": float(np.percentile(queue_latency, 95)),
        "avg_turnaround_ms": float(np.mean(turnaround)),
        "makespan_ms": float(finish[-1] - submit[0]),
        "avg_service_ms": float(np.mean(service)),
    }


def write_outputs(configs: List[SystemConfig], results: List[Dict], queue: Dict) -> None:
    # configs
    with open(os.path.join(OUT_DIR, "opgpu_system_configs.json"), "w", encoding="utf-8") as f:
        json.dump([asdict(c) | {"peak_tops": peak_tops(c), "pcie_gbps_eff": pcie_bandwidth_gbps(c)} for c in configs], f, indent=2)
    # results csv
    keys = list(results[0].keys())
    with open(os.path.join(OUT_DIR, "opgpu_system_sim_results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(results)
    with open(os.path.join(OUT_DIR, "opgpu_opencl_queue_sim.json"), "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

    # summary
    best = min(results, key=lambda r: r["latency_ms"])
    by_mode = {}
    for r in results:
        by_mode.setdefault(r["mode"], []).append(r["runtime_tops_effective"])
    summary = {
        "best_latency_case": best,
        "avg_runtime_tops_by_mode": {m: round(statistics.mean(v), 3) for m, v in by_mode.items()},
        "queue": queue,
        "notes": [
            "Conceptual system model (not wave-optics/signoff).",
            "Optical compute assumes effective MAC rates, WDM, and mode-dependent utilization.",
            "Memory hierarchy mapped as M0 Espiropirano, M1 Sb2S3, M2 VO2, M3 Azobenceno/delay.",
            "PCIe/OpenCL flow modeled as descriptor DMA + doorbell + microsequencer + O/E completion.",
        ],
    }
    with open(os.path.join(OUT_DIR, "opgpu_system_sim_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # markdown report
    lines = [
        "# OPGPU v0.4 System Simulation Report",
        "",
        "## Configurations",
    ]
    for c in configs:
        lines.append(f"- **{c.name} ({c.mode})**: peak {peak_tops(c):.2f} TOPS, PCIe {pcie_bandwidth_gbps(c):.2f} GB/s eff, tiles {c.tiles}, WDM {c.wdm_channels}, M1 {c.m1_weight_gb} GB, M2 {c.m2_buffer_mb} MB")
    lines += ["", "## OpenCL queue model", f"- avg queue: {queue['avg_queue_ms']:.3f} ms, p95: {queue['p95_queue_ms']:.3f} ms, avg turnaround: {queue['avg_turnaround_ms']:.3f} ms, makespan: {queue['makespan_ms']:.3f} ms", "", "## Workload results"]
    for r in results:
        lines.append(f"- {r['config']}/{r['workload']}: latency {r['latency_ms']:.4f} ms, util {r['utilization']}, runtime TOPS {r['runtime_tops_effective']}, energy {r['energy_uj']} uJ, bottleneck {r['bottleneck']}")
    lines += ["", "## Interpretation", "- NPU/TPU modes benefit high weight-reuse/intensity workloads (stationary weights in M1, pipelined optical MACs).", "- Low-intensity cases are limited by PCIe/E-O-O-E and control overhead.", "- Sb2S3 programming cost is amortized when weights persist across many reuses; VO2 switching supports fast runtime control."]
    with open(os.path.join(OUT_DIR, "opgpu_system_sim_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def plot_results(results: List[Dict]) -> None:
    if plt is None:
        return
    # latency by workload grouped by config
    workloads = sorted({r["workload"] for r in results})
    configs = sorted({r["config"] for r in results})
    x = np.arange(len(workloads))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for i, cfg in enumerate(configs):
        vals = [next(r["latency_ms"] for r in results if r["config"]==cfg and r["workload"]==wl) for wl in workloads]
        ax.bar(x + i*width, vals, width, label=cfg)
    ax.set_xticks(x + width)
    ax.set_xticklabels(workloads, rotation=20)
    ax.set_ylabel("Latency (ms)")
    ax.set_title("OPGPU v0.4 simulated latency by mode and workload")
    ax.legend()
    ax.set_yscale('log')
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "opgpu_system_latency.png"), dpi=150)
    plt.close(fig)

    # tops/utilization
    fig, ax = plt.subplots(figsize=(7, 4))
    for cfg in configs:
        rs = [r for r in results if r["config"]==cfg]
        ax.scatter([r["utilization"] for r in rs], [r["runtime_tops_effective"] for r in rs], label=cfg)
    ax.set_xlabel("Utilization")
    ax.set_ylabel("Effective runtime TOPS")
    ax.set_title("Utilization vs effective TOPS")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "opgpu_system_tops.png"), dpi=150)
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    configs = [
        SystemConfig(name="OPGPU-GPU64", mode="GPU", tiles=64, macs_per_tile_per_cycle=4096, wdm_channels=8),
        SystemConfig(name="OPGPU-NPU64", mode="NPU", tiles=64, macs_per_tile_per_cycle=4096, wdm_channels=8, energy_pj_per_mac=0.6),
        SystemConfig(name="OPGPU-TPU128", mode="TPU", tiles=128, macs_per_tile_per_cycle=8192, wdm_channels=8, energy_pj_per_mac=0.5),
    ]
    workloads = example_workloads()
    results = []
    for cfg in configs:
        for wl in workloads:
            results.append(simulate_workload(cfg, wl))
    queue = opencl_queue_sim()
    write_outputs(configs, results, queue)
    plot_results(results)
    print(json.dumps({"configs": len(configs), "results": len(results), "out": OUT_DIR, "fig": FIG_DIR}, indent=2))


if __name__ == "__main__":
    main()
