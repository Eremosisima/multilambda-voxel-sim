#!/usr/bin/env python3
"""
Manufacturable minimum dimensions for OPGPU proposals, accounting for
photonic foundry constraints and feasible thermal control, plus AI-accelerator
reference sizing context.

Conceptual estimates (not fabrication-ready). Outputs in outputs/.
"""
from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import List

OUT_DIR = "outputs"

# Foundry/process assumptions (SiPh/SiN, 193nm DUV class, BEOL PCM integration)
FOUNDRY = {
    "min_feature_practical_nm": 150,      # critical feature practical
    "waveguide_width_nm": 500,            # SiN/SOI single-mode class
    "min_gap_nm": 200,
    "heater_length_um": 50,               # compact slow-light/doped heater class
    "heater_width_um": 6,                 # heater + contacts lateral keepout
    "thermal_isolation_trench_um": 3,     # trench/void for local PCM isolation
    "electrode_via_keepout_um": 5,        # per-side access margin in complex cells
    "layer_registration_um": 0.5,         # per-layer alignment budget
    "min_bend_radius_sin_um": 15,         # conservative SiN
    "min_bend_radius_siph_um": 8,
}

# Thermal control feasibility (local PCM 300C, keep VO2 <68C, ambient/heat-spreader)
THERMAL = {
    "pcm_cell_pitch_fab_um": 20,          # lateral with isolation + heater routing
    "vo2_safe_clearance_um": 10,
    "axial_sep_fab_um": 12,
    "heat_spreader_overhead": 1.25,       # area/volume factor for spreading
    "cooling_interface_overhead": 1.40,   # module-level (TIM, spreader, cold plate path)
}

# Manufacturing/packaging overheads
MFG = {
    "yield_packaging_factor": 1.30,       # redundancy + routing + scribe/IO keepout
    "io_edge_keepout_mm": 1.0,
    "module_packaging_factor": 1.50,      # optics/fiber, drivers, control, enclosure share
}


@dataclass
class FabDims:
    key: str
    name: str
    fab_min_feature_nm: int
    fab_lateral_pitch_um: float
    fab_active_length_um: float
    fab_layer_thickness_nm: float
    fab_vertical_pitch_um: float
    fab_cell_area_um2: float
    fab_cell_volume_um3: float
    thermal_control_elements: str
    fab_notes: str


def compute() -> List[FabDims]:
    f = FOUNDRY; t = THERMAL; m = MFG
    rows = []

    # A1: MZI PCM - dominated by heater routing and thermal isolation
    pitch = max(t["pcm_cell_pitch_fab_um"], 20)
    length = 10 + f["heater_length_um"]*0.6 + f["electrode_via_keepout_um"]  # phase section + heater/control
    layer = 194
    vert = t["axial_sep_fab_um"] + 4
    area = pitch * length
    vol = area * vert
    rows.append(FabDims("A1","Interferometric PCM (Ref)", f["min_feature_practical_nm"], pitch, length, layer, vert,
                        round(area,2), round(vol,2),
                        "Doped/PIN micro-heaters for Sb2S3, isolation trenches, heat spreader, local sensing; pulsed write scheduling (OMCC)",
                        "Thermal isolation and heater contacts dominate; 300C local write feasible with trenches+spreading while keeping VO2 <68C"))

    # B3: rings + heaters/tuners
    R = f["min_bend_radius_siph_um"]
    pitch = (2*R + 6) + f["heater_width_um"]
    length = (2*R + 8) + f["heater_length_um"]*0.4
    vert = 6
    area = pitch*length
    vol = area*vert
    rows.append(FabDims("B3","Resonant WDM bank (microrings)", f["min_feature_practical_nm"], pitch, length, layer, vert,
                        round(area,2), round(vol,2),
                        "Thermo-optic or EO tuning, temperature stabilization (TEC/substrate), resonance locking",
                        "Bend radius and tuner/heater footprint dominate; stabilization needed for Q/thermal drift"))

    # G1: passive membranes
    n_layers = 16
    t_stack = n_layers*(194+267)/2000.0  # um approx avg
    pitch = 5.0 + f["layer_registration_um"]*4
    length = pitch
    vert = t_stack + 2.0
    area = pitch*length
    vol = area*vert
    rows.append(FabDims("G1","Thin-film membrane stack (passive WDM)", f["min_feature_practical_nm"], pitch, length, 194, round(vert,3),
                        round(area,2), round(vol,3),
                        "No active heating of stack; package-level thermal stabilization only",
                        "Thickness control nm-scale feasible by deposition; lateral set by registration/coupling apertures"))

    # G2: EO membranes
    pitch = 6.0 + f["electrode_via_keepout_um"]
    length = 6.0 + f["heater_length_um"]*0.2
    vert = t_stack + 3.0
    area = pitch*length
    vol = area*vert
    rows.append(FabDims("G2","Thin-film membrane/F-P stack (EO-tuned)", f["min_feature_practical_nm"], pitch, length, 176, round(vert,3),
                        round(area,2), round(vol,3),
                        "Electrode/RF routing thermal load managed by spreading; package stabilization",
                        "EO electrodes and registration dominate; fast tuning but added interfaces"))

    # G3: PCM+EO membranes
    pitch = 8.0 + f["electrode_via_keepout_um"]
    length = 8.0 + f["heater_length_um"]*0.3
    vert = t_stack + 3.5
    area = pitch*length
    vol = area*vert
    rows.append(FabDims("G3","Thin-film membrane stack (PCM+EO hybrid)", f["min_feature_practical_nm"], pitch, length, 144, round(vert,3),
                        round(area,2), round(vol,3),
                        "Localized micro-heaters for PCM layers, isolation trenches, spreading; EO thermal budget",
                        "PCM write heat requires isolation even in thin layers; co-integration increases keepout"))

    # H3: A1+G1+B3 modular
    pitch = max(t["pcm_cell_pitch_fab_um"], 22)
    length = 10 + (2*R+8) + f["heater_length_um"]*0.8 + f["electrode_via_keepout_um"]
    vert = t_stack + t["axial_sep_fab_um"] + 4
    area = pitch*length
    vol = area*vert
    rows.append(FabDims("H3","Open WDM-PCM (A1+G1+B3)", f["min_feature_practical_nm"], pitch, length, 194, round(vert,3),
                        round(area,2), round(vol,2),
                        "PCM micro-heaters + ring tuning + package TEC/spreader; OMCC thermal scheduling",
                        "Most practical advanced hybrid: combines PCM thermal needs with passive stack and ring control"))

    # H1: 3D brush
    pitch = max(t["pcm_cell_pitch_fab_um"], 22)
    bristle_h = 8*(t["axial_sep_fab_um"]+t_stack*0.5)
    area = pitch*pitch
    vol = area*bristle_h
    rows.append(FabDims("H1","Membrane-Brush NV (A1+G3+3D)", f["min_feature_practical_nm"], pitch, pitch, 144, round(bristle_h,3),
                        round(area,2), round(vol,2),
                        "Segmented heaters per voxel, vertical/lateral isolation, integrated heat spreader/manifold; strict sequencing",
                        "3D manufacturable only with advanced packaging/thermal vias or microfluidics; yield and heat removal dominate"))

    # H4: volumetric tensor
    pitch = max(t["pcm_cell_pitch_fab_um"], 20)
    bristle_h = 10*(t["axial_sep_fab_um"]*0.8 + t_stack*0.6)
    area = pitch*pitch
    vol = area*bristle_h
    rows.append(FabDims("H4","Volumetric Tensor Membrane (G2/G3+F2+A1)", f["min_feature_practical_nm"], pitch, pitch, 176, round(bristle_h,3),
                        round(area,2), round(vol,2),
                        "Distributed heaters/EO drivers, high-capacity heat spreading/cooling, active stabilization",
                        "Highest integration/thermal burden; requires aggressive 3D packaging and cooling to be feasible"))

    return rows


def module_estimates(fab: List[FabDims]):
    # Rough module sizing for "decent advanced AI" targets (conceptual, OPGPU)
    # Assume reference densities from objective analysis scaled pessimistically for manufacturable overhead
    targets = [
        {"class":"Edge AI NPU-like","target_tops":50, "target_mem_gb":8, "form":"module/card"},
        {"class":"Workstation/GPU-like","target_tops":300, "target_mem_gb":48, "form":"PCIe card / accelerator module"},
        {"class":"Datacenter TPU/GPU-like (per accelerator)","target_tops":800, "target_mem_gb":96, "form":"OAM/SXM-class module"},
    ]
    # per-proposal rough effective density (TOPS/cm2 and GB/cm3 module-equivalent, very conservative fab)
    density = {
        "A1": (0.5, 0.02), "B3": (0.8, 0.04), "G1": (0.6, 0.03), "G2": (1.2, 0.03),
        "G3": (1.1, 0.06), "H3": (0.9, 0.05), "H1": (1.5, 0.12), "H4": (1.8, 0.14),
    }
    est = []
    for r in fab:
        d_tops_cm2, d_gb_cm3 = density.get(r.key,(0.5,0.03))
        for t in targets:
            area_cm2 = (t["target_tops"]/d_tops_cm2) * MFG["yield_packaging_factor"]
            vol_cm3 = (t["target_mem_gb"]/d_gb_cm3) * MFG["yield_packaging_factor"] * THERMAL["cooling_interface_overhead"]
            side_cm = (area_cm2**0.5)
            est.append({
                "proposal": r.key,
                "class": t["class"],
                "target_tops": t["target_tops"],
                "target_mem_gb": t["target_mem_gb"],
                "est_active_area_cm2": round(area_cm2,1),
                "est_module_volume_cm3": round(vol_cm3,1),
                "est_footprint_cm": f"~{round(side_cm,1)} x {round(side_cm,1)} (2D equiv.)",
                "form_factor_note": t["form"],
            })
    return est


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    fab = compute()
    est = module_estimates(fab)
    with open(os.path.join(OUT_DIR,"manufacturable_dimensions.csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(asdict(fab[0]).keys()))
        w.writeheader(); [w.writerow(asdict(r)) for r in fab]
    with open(os.path.join(OUT_DIR,"ai_module_size_estimates.csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(est[0].keys()))
        w.writeheader(); w.writerows(est)
    out = {"foundry_assumptions":FOUNDRY, "thermal_assumptions":THERMAL, "mfg_assumptions":MFG,
           "proposals":[asdict(r) for r in fab], "ai_module_estimates": est,
           "disclaimer":"Conceptual manufacturable estimates for open-hardware reference; not validated designs."}
    with open(os.path.join(OUT_DIR,"manufacturable_dimensions.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,indent=2)
    print(json.dumps({"proposals":len(fab),"estimates":len(est)}))

if __name__ == "__main__":
    main()
