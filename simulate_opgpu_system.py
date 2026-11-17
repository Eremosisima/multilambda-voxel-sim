#!/usr/bin/env python3
"""System-level simulation for OPGPU v0.5+ (OpenCL-oriented optical GPU/NPU/TPU + OMCC).

Models conceptually: PCIe command/transfer flow, optical tile execution (MVM/MAC),
memory hierarchy behavior (M0-M3), OMCC coprocessor effects (DMA/compute overlap,
optical RAM arbitration, weight persistence and verification), and P1-calibrated
PCM/thermal parameters (multilevel Sb2S3 cell IL/energy, thermal scheduling margins).
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
    # OMCC coprocessor (optical RAM access/management)
    omcc_enabled: bool = False
    prefetch_overlap: float = 0.0      # fraction of input/weight transfer overlapped with compute (0-1)
    output_overlap: float = 0.0        # fraction of output transfer overlapped with compute (0-1)
    omcc_arbitration_ns: float = 0.0   # per-dispatch optical RAM arbitration/scheduling overhead
    omcc_verify_overhead: float = 0.0   # multiplicative overhead on programming for read-verify/RAS (e.g. 0.1 = +10%)
    m1_persistent: bool = False        # weights persist in M1 across invocations when they fit
    omcc_queue_overhead_ms: float = 0.0  # added queue/dispatch efficiency effect (modeled in queue sim)
    # P1-calibrated PCM/thermal (from model_pcm_multilevel.py, model_thermal_brush.py)
    pcm_bits: int = 5                  # multilevel cell resolution
    pcm_il_db_avg: float = 0.12        # average insertion loss per PCM cell/segment (est.)
    pcm_step_energy_pj: float = 0.0031 # estimated energy per level step (conceptual)
    thermal_margin_c: float = 41.6     # estimated margin to VO2 threshold during Sb2S3 program
    thermal_write_serialization: float = 1.0  # >1 adds scheduling/serialization overhead for thermal safety
    pcm_calibrated: bool = False
    # P3 variability/refresh policy
    m2_refresh_overhead: float = 0.0   # fraction overhead for VO2 volatile refresh (background)


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
    # P1-calibrated optical loss/capacity effects (small, conceptual)
    if cfg.pcm_calibrated:
        il_penalty = max(0.0, (cfg.pcm_il_db_avg - 0.12)) * 0.03
        base *= max(0.9, 1.0 - il_penalty)
        # density/utilization tradeoff by bit mode (4b more robust, 5b denser)
        if cfg.pcm_bits <= 4:
            base *= 0.985
        else:
            base *= min(1.03, 1.0 + 0.005 * max(cfg.pcm_bits - 4, 0))
    # P2 reliability margin: stronger RAS/verification can reduce effective throughput slightly
    if cfg.omcc_verify_overhead >= 0.2:
        base *= 0.985
    # P3 M2 refresh background overhead
    if cfg.m2_refresh_overhead > 0:
        base *= max(0.9, 1.0 - cfg.m2_refresh_overhead)
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

    weights_fit_m1 = wl.weight_bytes <= cfg.m1_weight_gb * 1024**3
    # Transfers: weights programmed/loaded once per reuse epoch (amortized by reuse)
    weight_transfer_bytes = wl.weight_bytes / max(wl.weight_reuse, 1.0)
    persistent_hit = cfg.omcc_enabled and cfg.m1_persistent and weights_fit_m1 and wl.weight_reuse >= 4
    if persistent_hit:
        # Steady-state: weights already resident in optical RAM (M1), only small management traffic
        weight_transfer_bytes = min(weight_transfer_bytes, 4096.0)
    program_reuse = max(wl.weight_reuse, 1.0) * (8.0 if persistent_hit else 1.0)

    in_ns = simulate_transfer(wl.bytes_in, bw, cfg.cmd_latency_ns + cfg.eo_oe_latency_ns)
    out_ns = simulate_transfer(wl.bytes_out, bw, cfg.cmd_latency_ns + cfg.eo_oe_latency_ns)
    wt_transfer_ns = simulate_transfer(weight_transfer_bytes, bw, cfg.cmd_latency_ns)
    # programming/setup latency for M1 (amortized), thermally scheduled when calibrated
    program_factor = (1.0 + cfg.omcc_verify_overhead) if cfg.omcc_enabled else 1.0
    blocks = max(wl.weight_bytes / (1024 * 64), 1.0)
    program_ns = (blocks * cfg.sb2s3_program_us * 1000.0 * cfg.thermal_write_serialization * program_factor) / program_reuse
    wt_ns = wt_transfer_ns + (0.0 if persistent_hit else program_ns * 0.1)  # transfer-dominated; residual setup

    compute_ns = (wl.ops / (achieved_tops * 1e12)) * 1e9 if achieved_tops > 0 else float('inf')
    # control/switching overhead + OMCC arbitration
    control_ns = cfg.cmd_latency_ns + (wl.ops / max(cfg.macs_per_tile_per_cycle * cfg.tiles, 1)) * cfg.vo2_switch_ns
    arbitration_ns = cfg.omcc_arbitration_ns if cfg.omcc_enabled else 0.0
    compute_phase_ns = compute_ns + control_ns + arbitration_ns

    # OMCC prefetch/double-buffering: overlap eligible transfers with compute
    in_ov = cfg.prefetch_overlap if cfg.omcc_enabled else 0.0
    wt_ov = cfg.prefetch_overlap if (cfg.omcc_enabled and not persistent_hit) else (0.95 if persistent_hit else 0.0)
    out_ov = cfg.output_overlap if cfg.omcc_enabled else 0.0
    exposed_in_ns = in_ns * max(0.0, 1.0 - in_ov)
    exposed_wt_ns = wt_ns * max(0.0, 1.0 - wt_ov)
    exposed_out_ns = out_ns * max(0.0, 1.0 - out_ov)
    total_ns = max(compute_phase_ns, exposed_in_ns + exposed_wt_ns) + exposed_out_ns

    # Energy (very simplified)
    e_compute_pj = wl.ops/2.0 * cfg.energy_pj_per_mac  # per MAC
    e_pcie_pj = (wl.bytes_in + wl.bytes_out + weight_transfer_bytes) * cfg.energy_pj_per_byte_pcie
    if cfg.pcm_calibrated:
        weight_elements = wl.weight_bytes / 2.0  # assume 16-bit equiv element
        e_program_pj = weight_elements * cfg.pcm_bits * cfg.pcm_step_energy_pj * program_factor / program_reuse
    else:
        e_program_pj = (wl.weight_bytes / (1024*1024)) * cfg.energy_nj_per_m1_program * 1000.0 * program_factor / program_reuse
    omcc_mgmt_pj = (wl.bytes_in + wl.bytes_out) * 0.2 if cfg.omcc_enabled else 0.0
    total_energy_uj = (e_compute_pj + e_pcie_pj + e_program_pj + omcc_mgmt_pj) / 1e6

    latency_ms = total_ns / 1e6

    return {
        "config": cfg.name,
        "mode": cfg.mode,
        "omcc": cfg.omcc_enabled,
        "pcm_calibrated": cfg.pcm_calibrated,
        "workload": wl.name,
        "peak_tops": round(peak, 3),
        "utilization": round(eff, 3),
        "achieved_tops_model": round(achieved_tops, 3),
        "runtime_tops_effective": round((wl.ops/1e12)/(total_ns/1e9) if total_ns>0 else 0, 3),
        "latency_ms": round(latency_ms, 6),
        "pcie_gbps_eff": round(bw, 3),
        "energy_uj": round(total_energy_uj, 3),
        "bottleneck": bottleneck(exposed_in_ns, exposed_out_ns, exposed_wt_ns, compute_phase_ns, arbitration_ns),
        "m1_persistent_hit": persistent_hit,
        "pcm_bits": cfg.pcm_bits,
        "thermal_margin_c": cfg.thermal_margin_c,
    }


def bottleneck(in_ns, out_ns, wt_ns, compute_ns, arbitration_ns) -> str:
    parts = {
        "input_transfer": in_ns,
        "output_transfer": out_ns,
        "weight_transfer": wt_ns,
        "optical_compute": compute_ns,
        "omcc_arbitration": arbitration_ns,
    }
    return max(parts, key=parts.get)


def opencl_queue_sim(events: int = 32, omcc_enabled: bool = False) -> Dict:
    # Simple discrete-event approximation of queued kernel launches
    rng = np.random.default_rng(42)
    submit = np.sort(rng.uniform(0, 5.0, size=events))  # ms
    if omcc_enabled:
        service = rng.uniform(0.18, 1.0, size=events)  # ms (better overlap/scheduling)
        dispatch_overhead = 0.02
    else:
        service = rng.uniform(0.2, 1.2, size=events)  # ms
        dispatch_overhead = 0.05
    start = np.zeros(events)
    finish = np.zeros(events)
    for i in range(events):
        ready = submit[i] if i == 0 else max(submit[i], finish[i-1])
        start[i] = ready + dispatch_overhead  # dispatch/doorbell/OMCC scheduling overhead
        finish[i] = start[i] + service[i]
    queue_latency = start - submit
    turnaround = finish - submit
    return {
        "events": events,
        "omcc_enabled": omcc_enabled,
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
        label = r["mode"] + ("+OMCC" if r.get("omcc") else "")
        by_mode.setdefault(label, []).append(r["runtime_tops_effective"])
    summary = {
        "best_latency_case": best,
        "avg_runtime_tops_by_mode": {m: round(statistics.mean(v), 3) for m, v in by_mode.items()},
        "queue": queue,
        "notes": [
            "Conceptual system model v0.5+ (not wave-optics/signoff).",
            "Optical compute assumes effective MAC rates, WDM, and mode-dependent utilization.",
            "Memory hierarchy mapped as M0 Espiropirano, M1 Sb2S3, M2 VO2, M3 Azobenceno/delay.",
            "PCIe/OpenCL flow modeled as descriptor DMA + doorbell + microsequencer + O/E completion.",
            "OMCC models DMA/compute overlap, optical RAM arbitration, M1 weight persistence, and verify/RAS overhead.",
            "P1-calibrated configs use PCM multilevel/IL and thermal scheduling parameters from model_pcm_multilevel.py and model_thermal_brush.py.",
        ],
    }
    with open(os.path.join(OUT_DIR, "opgpu_system_sim_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # markdown report
    q_base = queue.get("baseline", queue)
    q_omcc = queue.get("omcc", queue)
    lines = [
        "# OPGPU v0.5+ System Simulation Report (OMCC + P1-calibrated PCM/thermal)",
        "",
        "## Configurations",
    ]
    for c in configs:
        omcc = "on" if getattr(c, "omcc_enabled", False) else "off"
        p1 = "on" if getattr(c, "pcm_calibrated", False) else "off"
        extra = f", PCM {getattr(c,'pcm_bits',5)}b IL {getattr(c,'pcm_il_db_avg',0.12):.3f}dB margin {getattr(c,'thermal_margin_c',0):.1f}C" if p1=="on" else ""
        lines.append(f"- **{c.name} ({c.mode}, OMCC {omcc}, P1 {p1}{extra})**: peak {peak_tops(c):.2f} TOPS, PCIe {pcie_bandwidth_gbps(c):.2f} GB/s eff, tiles {c.tiles}, WDM {c.wdm_channels}, M1 {c.m1_weight_gb} GB, M2 {c.m2_buffer_mb} MB")
    lines += ["", "## OpenCL queue model",
              f"- baseline: avg queue {q_base['avg_queue_ms']:.3f} ms, p95 {q_base['p95_queue_ms']:.3f} ms, avg turnaround {q_base['avg_turnaround_ms']:.3f} ms, makespan {q_base['makespan_ms']:.3f} ms",
              f"- OMCC: avg queue {q_omcc['avg_queue_ms']:.3f} ms, p95 {q_omcc['p95_queue_ms']:.3f} ms, avg turnaround {q_omcc['avg_turnaround_ms']:.3f} ms, makespan {q_omcc['makespan_ms']:.3f} ms",
              "", "## Workload results"]
    for r in results:
        lines.append(f"- {r['config']}/{r['workload']}: latency {r['latency_ms']:.4f} ms, util {r['utilization']}, runtime TOPS {r['runtime_tops_effective']}, energy {r['energy_uj']} uJ, bottleneck {r['bottleneck']}, M1_persist {r.get('m1_persistent_hit', False)}")
    lines += ["", "## Interpretation",
              "- OMCC overlap/prefetch and M1 weight persistence reduce exposed transfer/programming overhead, improving effective TOPS and latency on reuse-heavy workloads.",
              "- P1-calibrated configs incorporate PCM multilevel/IL and thermal scheduling margins (from P1 modeling), showing the performance/energy envelope under thermally-aware operation.",
              "- Low-intensity or non-persistent cases remain limited by transfers/control; arbitration/verification add small overheads but enable RAS and correctness."]
    with open(os.path.join(OUT_DIR, "opgpu_system_sim_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def plot_results(results: List[Dict]) -> None:
    if plt is None:
        return
    # latency by workload grouped by config
    workloads = sorted({r["workload"] for r in results})
    configs = sorted({r["config"] for r in results})
    x = np.arange(len(workloads))
    width = 0.8 / max(len(configs), 1)
    fig, ax = plt.subplots(figsize=(12, 5))
    for i, cfg in enumerate(configs):
        vals = [next(r["latency_ms"] for r in results if r["config"]==cfg and r["workload"]==wl) for wl in workloads]
        ax.bar(x + i*width, vals, width, label=cfg)
    ax.set_xticks(x + width * (len(configs)-1) / 2)
    ax.set_xticklabels(workloads, rotation=20)
    ax.set_ylabel("Latency (ms)")
    ax.set_title("OPGPU v0.5 simulated latency by mode/workload (OMCC vs baseline)")
    ax.legend(fontsize=8)
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
        SystemConfig(name="OPGPU-NPU64-OMCC", mode="NPU", tiles=64, macs_per_tile_per_cycle=4096, wdm_channels=8, energy_pj_per_mac=0.58,
                     omcc_enabled=True, prefetch_overlap=0.7, output_overlap=0.5, omcc_arbitration_ns=35.0, omcc_verify_overhead=0.08, m1_persistent=True),
        SystemConfig(name="OPGPU-TPU128-OMCC", mode="TPU", tiles=128, macs_per_tile_per_cycle=8192, wdm_channels=8, energy_pj_per_mac=0.48,
                     omcc_enabled=True, prefetch_overlap=0.75, output_overlap=0.55, omcc_arbitration_ns=40.0, omcc_verify_overhead=0.08, m1_persistent=True),
        SystemConfig(name="OPGPU-NPU64-OMCC-P1", mode="NPU", tiles=64, macs_per_tile_per_cycle=4096, wdm_channels=8, energy_pj_per_mac=0.57,
                     omcc_enabled=True, prefetch_overlap=0.72, output_overlap=0.52, omcc_arbitration_ns=38.0, omcc_verify_overhead=0.10, m1_persistent=True,
                     pcm_calibrated=True, pcm_bits=5, pcm_il_db_avg=0.123, pcm_step_energy_pj=0.0031, thermal_margin_c=41.6, thermal_write_serialization=1.15),
        SystemConfig(name="OPGPU-TPU128-OMCC-P1", mode="TPU", tiles=128, macs_per_tile_per_cycle=8192, wdm_channels=8, energy_pj_per_mac=0.47,
                     omcc_enabled=True, prefetch_overlap=0.76, output_overlap=0.56, omcc_arbitration_ns=42.0, omcc_verify_overhead=0.10, m1_persistent=True,
                     pcm_calibrated=True, pcm_bits=5, pcm_il_db_avg=0.123, pcm_step_energy_pj=0.0031, thermal_margin_c=41.6, thermal_write_serialization=1.15),
        SystemConfig(name="OPGPU-TPU128-OMCC-P2-RAS", mode="TPU", tiles=128, macs_per_tile_per_cycle=8192, wdm_channels=8, energy_pj_per_mac=0.475,
                     omcc_enabled=True, prefetch_overlap=0.74, output_overlap=0.54, omcc_arbitration_ns=48.0, omcc_verify_overhead=0.22, m1_persistent=True,
                     pcm_calibrated=True, pcm_bits=5, pcm_il_db_avg=0.123, pcm_step_energy_pj=0.0031, thermal_margin_c=41.6, thermal_write_serialization=1.18),
        SystemConfig(name="OPGPU-TPU128-OMCC-P3-4b", mode="TPU", tiles=128, macs_per_tile_per_cycle=8192, wdm_channels=8, energy_pj_per_mac=0.472,
                     omcc_enabled=True, prefetch_overlap=0.74, output_overlap=0.54, omcc_arbitration_ns=46.0, omcc_verify_overhead=0.18, m1_persistent=True,
                     pcm_calibrated=True, pcm_bits=4, pcm_il_db_avg=0.123, pcm_step_energy_pj=0.0031, thermal_margin_c=41.6, thermal_write_serialization=1.12, m2_refresh_overhead=0.002),
    ]
    workloads = example_workloads()
    results = []
    for cfg in configs:
        for wl in workloads:
            results.append(simulate_workload(cfg, wl))
    queue = {
        "baseline": opencl_queue_sim(omcc_enabled=False),
        "omcc": opencl_queue_sim(omcc_enabled=True),
    }
    write_outputs(configs, results, queue)
    plot_results(results)
    print(json.dumps({"configs": len(configs), "results": len(results), "out": OUT_DIR, "fig": FIG_DIR}, indent=2))


if __name__ == "__main__":
    main()
