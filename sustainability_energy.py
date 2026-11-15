"""Scenario-based energy and CO2 estimates for photonic inference vs conventional GPUs.

All numbers are transparent assumptions for Article 1 discussion; not measured device claims.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np


def scenario_inputs():
    return {
        "reference": {
            "accelerator_name": "High-power AI accelerator (illustrative reference scenario)",
            "gpu_power_w": 700.0,
            "hours_per_year": 24 * 365,
            "datacenter_gpus": 10000,
            "cooling_overhead_factor": 2.0,  # IT + cooling
            "grid_kgco2_per_kwh": 0.4,       # global-average-like scenario; vary by region
            "tops_per_w_reported_ref": 0.5,   # illustrative inference efficiency placeholder
            "notes": "Reference values are scenario placeholders for comparison only; replace with cited public/vendor sources in manuscript. No endorsement or affiliation implied.",
        },
        "proposed_photonic": {
            "tops_per_w_scenario": [1.0, 5.0, 10.0],
            "weight_static_power_w": 0.0,     # non-volatile weights assumption
            "read_laser_mw_per_channel": 2.0,
            "channels": 4,
            "detector_and_tia_mw_per_channel": 5.0,
            "control_electronics_w": 2.0,
            "optical_throughput_tops_equiv": 0.1,  # small demonstrator scenario
            "notes": "Photonic numbers are architecture-level scenarios, not fabricated-device measurements.",
        },
    }


def annual_energy_kwh(power_w: float, hours_per_year: float, units: int = 1, overhead: float = 1.0) -> float:
    return power_w * hours_per_year * units * overhead / 1000.0


def co2_tons(energy_kwh: float, kgco2_per_kwh: float) -> float:
    return energy_kwh * kgco2_per_kwh / 1000.0


def compute_scenarios():
    inp = scenario_inputs()
    ref = inp["reference"]
    phot = inp["proposed_photonic"]

    ref_gpu_kwh = annual_energy_kwh(ref["gpu_power_w"], ref["hours_per_year"], 1, 1.0)
    ref_dc_kwh = annual_energy_kwh(ref["gpu_power_w"], ref["hours_per_year"], ref["datacenter_gpus"], ref["cooling_overhead_factor"])
    ref_dc_co2 = co2_tons(ref_dc_kwh, ref["grid_kgco2_per_kwh"])

    # Demonstrator optical power budget (static/read path, excluding high-speed DAC/ADC in full system)
    optical_read_w = phot["read_laser_mw_per_channel"] * phot["channels"] / 1000.0
    detector_w = phot["detector_and_tia_mw_per_channel"] * phot["channels"] / 1000.0
    demo_static_w = optical_read_w + detector_w + phot["control_electronics_w"] + phot["weight_static_power_w"]
    demo_tops_w = phot["optical_throughput_tops_equiv"] / demo_static_w if demo_static_w > 0 else None

    rows = []
    for tops_w in phot["tops_per_w_scenario"]:
        improvement = tops_w / ref["tops_per_w_reported_ref"]
        scaled_dc_kwh = ref_dc_kwh / improvement  # same delivered inference work assumption
        scaled_dc_co2 = co2_tons(scaled_dc_kwh, ref["grid_kgco2_per_kwh"])
        rows.append({
            "scenario_photonic_tops_per_w": tops_w,
            "relative_efficiency_vs_ref": improvement,
            "ref_datacenter_kwh_per_year": ref_dc_kwh,
            "scenario_datacenter_kwh_per_year": scaled_dc_kwh,
            "ref_datacenter_tco2_per_year": ref_dc_co2,
            "scenario_datacenter_tco2_per_year": scaled_dc_co2,
            "avoided_tco2_per_year": ref_dc_co2 - scaled_dc_co2,
            "avoided_percent": (1 - 1/improvement) * 100,
        })

    return {
        "inputs": inp,
        "reference_derived": {
            "single_gpu_kwh_per_year_no_cooling": ref_gpu_kwh,
            "single_gpu_tco2_per_year_no_cooling": co2_tons(ref_gpu_kwh, ref["grid_kgco2_per_kwh"]),
            "datacenter_kwh_per_year_with_cooling": ref_dc_kwh,
            "datacenter_tco2_per_year_with_cooling": ref_dc_co2,
        },
        "demonstrator_power_budget": {
            "optical_read_w": optical_read_w,
            "detectors_and_tia_w": detector_w,
            "control_electronics_w": phot["control_electronics_w"],
            "total_estimated_w": demo_static_w,
            "throughput_tops_equiv_assumed": phot["optical_throughput_tops_equiv"],
            "implied_tops_per_w_demo_budget": demo_tops_w,
            "note": "Excludes full-system ADC/DAC, memory movement, host, and packaging; include in final system model.",
        },
        "datacenter_scenarios_same_work": rows,
        "disclaimer": "Scenario analysis only. Real savings depend on achieved TOPS/W, utilization, workload, PUE, fabrication impacts, and grid mix.",
    }


def main(out_dir: Path):
    data = compute_scenarios()
    (out_dir / "sustainability_scenarios.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    # CSV summary
    rows = data["datacenter_scenarios_same_work"]
    import csv
    with (out_dir / "sustainability_scenarios.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return data


if __name__ == "__main__":
    main(Path(__file__).resolve().parent / "outputs")
