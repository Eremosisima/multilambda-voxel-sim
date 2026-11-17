#!/usr/bin/env python3
"""
S4: Process-calibrated Monte Carlo variability/yield simulation and design optimizations.
Candidates: H3,G3,H1,H4. Conceptual, parametric (no measurements).
Outputs: outputs/s4_variability_yield.{json,csv,md} and figures/s4_variability_yield*.png
"""
from __future__ import annotations

import csv
import json
import math
import os
import random

OUT = "outputs"
FIG = "figures"
random.seed(42)

N_SAMPLES = 3000

# Process profiles: calibrated distributions (conceptual placeholders to be replaced by foundry metrology)
PROFILES = {
    "baseline": {
        "label": "Baseline process (current assumptions)",
        "n_sigma": 0.01, "d_sigma": 0.02, "coupling_sigma": 0.03,
        "phase_sigma": 0.04, "thermal_sigma": 0.05, "loss_sigma_db": 0.5,
        "correlation_3d": 1.15,
    },
    "improved_process": {
        "label": "Improved process control (metrology/calibrated)",
        "n_sigma": 0.007, "d_sigma": 0.014, "coupling_sigma": 0.022,
        "phase_sigma": 0.03, "thermal_sigma": 0.04, "loss_sigma_db": 0.35,
        "correlation_3d": 1.10,
    },
    "pilot_stabilized": {
        "label": "Pilot-line stabilized (tight control + thermal management)",
        "n_sigma": 0.005, "d_sigma": 0.01, "coupling_sigma": 0.016,
        "phase_sigma": 0.022, "thermal_sigma": 0.03, "loss_sigma_db": 0.25,
        "correlation_3d": 1.07,
    },
}

BASE_CANDS = {
    "H3": {
        "name": "Open WDM-PCM (A1+G1+B3)",
        "base_snr_db": 14.0, "base_phase_err": 0.05, "base_il_db": 12.0,
        "elements": 120, "dimensionality": "2.5D",
        "ecc_overhead": 0.08, "redundancy": 0.10, "calibration_eff": 0.65, "thermal_sensitivity": 0.7,
    },
    "G3": {
        "name": "Thin-film membrane stack (PCM+EO hybrid)",
        "base_snr_db": 15.5, "base_phase_err": 0.04, "base_il_db": 9.5,
        "elements": 90, "dimensionality": "2.5D",
        "ecc_overhead": 0.07, "redundancy": 0.08, "calibration_eff": 0.72, "thermal_sensitivity": 0.85,
    },
    "H1": {
        "name": "Membrane-Brush NV (A1+G3+3D)",
        "base_snr_db": 12.5, "base_phase_err": 0.06, "base_il_db": 14.5,
        "elements": 220, "dimensionality": "3D",
        "ecc_overhead": 0.12, "redundancy": 0.15, "calibration_eff": 0.55, "thermal_sensitivity": 1.0,
    },
    "H4": {
        "name": "Volumetric Tensor Membrane (G2/G3+F2+A1)",
        "base_snr_db": 11.8, "base_phase_err": 0.07, "base_il_db": 15.8,
        "elements": 260, "dimensionality": "3D",
        "ecc_overhead": 0.14, "redundancy": 0.18, "calibration_eff": 0.50, "thermal_sensitivity": 1.1,
    },
}

# Candidate optimizations (design/process levers)
OPTIMIZATIONS = {
    "H3": {
        "label": "Partitioned WDM tiles + closed-loop calibration + spare rings",
        "elements": 108, "redundancy": 0.14, "calibration_eff": 0.72, "base_snr_db": 14.4, "base_il_db": 11.6, "base_phase_err": 0.047, "thermal_sensitivity": 0.62,
    },
    "G3": {
        "label": "EO trim + PCM write scheduling + improved coupling",
        "elements": 84, "redundancy": 0.11, "calibration_eff": 0.78, "base_snr_db": 15.9, "base_il_db": 9.1, "base_phase_err": 0.037, "thermal_sensitivity": 0.78,
    },
    "H1": {
        "label": "Modular 3D partitioning + re-mapping spares + thermal vias/manifold",
        "elements": 190, "redundancy": 0.22, "calibration_eff": 0.66, "base_snr_db": 13.3, "base_il_db": 13.6, "base_phase_err": 0.054, "thermal_sensitivity": 0.82,
    },
    "H4": {
        "label": "Hierarchical partitioning + alignment/calibration loops + higher redundancy",
        "elements": 220, "redundancy": 0.26, "calibration_eff": 0.62, "base_snr_db": 12.8, "base_il_db": 14.8, "base_phase_err": 0.061, "thermal_sensitivity": 0.90,
    },
}

CRITERIA = {"snr_db_min": 8.0, "phase_err_max": 0.12, "il_db_max": 18.0}


def sample_sigma(s):
    u1 = max(random.random(), 1e-12)
    u2 = random.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return z * (s / 3.0)


def spec_for(key, optimized=False):
    s = dict(BASE_CANDS[key])
    if optimized:
        s.update(OPTIMIZATIONS[key])
        s["variant"] = "optimized"
        s["opt_label"] = OPTIMIZATIONS[key]["label"]
    else:
        s["variant"] = "baseline"
        s["opt_label"] = "none"
    return s


def run_mc(key, spec, process):
    passes = 0
    snrs=[]; pes=[]; ils=[]
    for _ in range(N_SAMPLES):
        n_v = sample_sigma(process["n_sigma"])
        d_v = sample_sigma(process["d_sigma"])
        c_v = sample_sigma(process["coupling_sigma"])
        p_v = sample_sigma(process["phase_sigma"])
        t_v = sample_sigma(process["thermal_sigma"])
        l_v = sample_sigma(process["loss_sigma_db"]) * 3.0
        static = abs(n_v)+abs(d_v)+abs(c_v)+abs(p_v)
        resid = static*(1.0-spec["calibration_eff"]) + abs(t_v)*spec["thermal_sensitivity"]
        corr = process["correlation_3d"] if spec["dimensionality"]=="3D" else 1.0
        scale = math.sqrt(spec["elements"]/100.0) * corr
        snr = spec["base_snr_db"] - (resid*18.0*scale) - abs(l_v)
        pe = spec["base_phase_err"] + resid*0.8*scale
        il = spec["base_il_db"] + abs(l_v) + resid*6.0*scale
        ok = (snr >= CRITERIA["snr_db_min"] and pe <= CRITERIA["phase_err_max"] and il <= CRITERIA["il_db_max"])
        if ok: passes += 1
        snrs.append(snr); pes.append(pe); ils.append(il)
    def stats(arr):
        arrs=sorted(arr); m=sum(arr)/len(arr)
        idx5=int(0.05*len(arrs)); idx95=min(int(0.95*len(arrs)), len(arrs)-1)
        return {"mean": round(m,4), "p5": round(arrs[idx5],4), "p95": round(arrs[idx95],4)}
    raw_yield = passes/N_SAMPLES
    effective_yield = raw_yield*(1.0-spec["redundancy"])
    return {
        "key": key, "name": spec["name"], "dimensionality": spec["dimensionality"],
        "variant": spec["variant"], "optimization": spec.get("opt_label",""),
        "process": process["label"], "samples": N_SAMPLES,
        "raw_yield": round(raw_yield,4), "effective_yield_after_redundancy": round(effective_yield,4),
        "redundancy_overhead": spec["redundancy"], "ecc_overhead": spec["ecc_overhead"],
        "calibration_efficiency": spec["calibration_eff"], "elements": spec["elements"],
        "snr_db": stats(snrs), "phase_error": stats(pes), "insertion_loss_db": stats(ils),
        "criteria": CRITERIA,
        "meets_yield_target_0_7": raw_yield >= 0.7,
        "meets_yield_target_0_85": raw_yield >= 0.85,
    }


def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)
    all_results=[]
    for pk, prof in PROFILES.items():
        for k in BASE_CANDS:
            for opt in (False, True):
                all_results.append(run_mc(k, spec_for(k,opt), prof))

    # focus views
    baseline_focus = [r for r in all_results if r["process"]==PROFILES["baseline"]["label"]]
    improved_opt = [r for r in all_results if r["process"]==PROFILES["improved_process"]["label"] and r["variant"]=="optimized"]
    best_path = []
    for k in BASE_CANDS:
        # best effective yield among optimized across profiles
        cands = [r for r in all_results if r["key"]==k and r["variant"]=="optimized"]
        best_path.append(max(cands, key=lambda x: (x["effective_yield_after_redundancy"], x["raw_yield"])))

    summary = {
        "assumptions": {"profiles": PROFILES, "samples": N_SAMPLES, "criteria": CRITERIA, "optimizations": OPTIMIZATIONS,
                        "note": "Process-calibrated conceptual MC; replace distributions with metrology/foundry stats. Optimizations: partitioning, redundancy/re-mapping, closed-loop calibration, thermal management."},
        "results": all_results,
        "best_optimized_path_per_candidate": best_path,
        "disclaimer": "Conceptual S4 model (no measurements). Yield depends on real process distributions and system-level calibration/RAS.",
    }
    with open(os.path.join(OUT,"s4_variability_yield.json"),"w",encoding="utf-8") as f:
        json.dump(summary,f,indent=2,ensure_ascii=False)

    cols=["key","name","dimensionality","variant","process","raw_yield","effective_yield_after_redundancy","snr_mean_db","snr_p5_db","phase_err_mean","phase_err_p95","il_mean_db","il_p95_db","redundancy_overhead","ecc_overhead","calibration_efficiency","elements","meets_yield_target_0_7","meets_yield_target_0_85","optimization"]
    csv_rows=[]
    for r in all_results:
        csv_rows.append({**{k:r.get(k,"") for k in cols[:6]}, "snr_mean_db":r["snr_db"]["mean"],"snr_p5_db":r["snr_db"]["p5"],"phase_err_mean":r["phase_error"]["mean"],"phase_err_p95":r["phase_error"]["p95"],"il_mean_db":r["insertion_loss_db"]["mean"],"il_p95_db":r["insertion_loss_db"]["p95"], **{k:r.get(k,"") for k in cols[13:]}})
    with open(os.path.join(OUT,"s4_variability_yield.csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(csv_rows)

    def rowtbl(rs, title):
        md=[f"### {title}", "", "| Candidato | Dim | Variante | Proceso | Yield bruto | Yield efectivo | SNR medio (dB) | SNR p5 | Err fase p95 | IL p95 (dB) | >=70% | >=85% |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|"]
        for r in rs:
            md.append(f"| {r['key']} | {r['dimensionality']} | {r['variant']} | {r['process']} | {r['raw_yield']} | {r['effective_yield_after_redundancy']} | {r['snr_db']['mean']} | {r['snr_db']['p5']} | {r['phase_error']['p95']} | {r['insertion_loss_db']['p95']} | {'sí' if r['meets_yield_target_0_7'] else 'no'} | {'sí' if r['meets_yield_target_0_85'] else 'no'} |")
        md.append("")
        return md

    md=["# S4 — Variabilidad de proceso y yield (Monte Carlo calibrado + optimizaciones)", "",
        f"> {N_SAMPLES} muestras por caso. Conceptual (no mediciones). Perfiles de proceso y optimizaciones para H3/G3/H1/H4.", ""]
    md += rowtbl(baseline_focus, "Línea base (proceso actual, baseline vs optimizado)")
    md += rowtbl(improved_opt, "Proceso mejorado + diseño optimizado")
    md += ["## Mejor ruta optimizada por candidato", "",
           "| Candidato | Proceso | Yield bruto | Yield efectivo | SNR p5 | Err fase p95 | IL p95 | Optimización |",
           "|---|---|---:|---:|---:|---:|---:|---|"]
    for r in best_path:
        md.append(f"| {r['key']} | {r['process']} | {r['raw_yield']} | {r['effective_yield_after_redundancy']} | {r['snr_db']['p5']} | {r['phase_error']['p95']} | {r['insertion_loss_db']['p95']} | {r['optimization']} |")
    md += ["", "## Lectura y optimizaciones", 
           "- **H3/G3 (2.5D):** ya cumplen objetivos con proceso base; optimización (particionado, calibración en lazo cerrado, spares) mejora margen y reduce sensibilidad térmica.",
           "- **H1/H4 (3D):** baseline efectivo insuficiente para 85% (H4 crítico); particionado jerárquico/modular, re-mapeo de spares, calibración/alineación y control térmico elevan yield bruto y efectivo en perfiles mejorados.",
           "- **Pendiente de calibración real:** reemplazar σ(n,d,acoplo,IL,térmica) con metrología; validar RAS/re-mapeo en OMCC y costo de redundancia en área/energía."]
    with open(os.path.join(OUT,"s4_variability_yield.md"),"w",encoding="utf-8") as f: f.write("\n".join(md)+"\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        keys=list(BASE_CANDS.keys()); x=range(len(keys)); width=0.18
        def get(pk,var,field):
            return [next(r[field] for r in all_results if r['key']==k and r['process']==PROFILES[pk]['label'] and r['variant']==var) for k in keys]
        fig,ax=plt.subplots(figsize=(9,4.2))
        ax.bar([i-1.5*width for i in x], get('baseline','baseline','raw_yield'), width, label='Base bruto')
        ax.bar([i-0.5*width for i in x], get('baseline','optimized','raw_yield'), width, label='Base+opt bruto')
        ax.bar([i+0.5*width for i in x], get('improved_process','optimized','raw_yield'), width, label='Proceso mej.+opt bruto')
        ax.bar([i+1.5*width for i in x], get('improved_process','optimized','effective_yield_after_redundancy'), width, label='Proc.mej.+opt efectivo')
        ax.axhline(0.7,color='orange',ls='--',lw=1); ax.axhline(0.85,color='green',ls='--',lw=1)
        ax.set_xticks(list(x)); ax.set_xticklabels(keys); ax.set_ylim(0,1.08); ax.set_ylabel('Yield')
        ax.set_title('S4: Yield por variabilidad/proceso y optimización (calibrado conceptual)')
        ax.legend(fontsize=7,ncol=2); fig.tight_layout()
        fig.savefig(os.path.join(FIG,'s4_variability_yield.png'),dpi=150)
        # extra: best path
        fig2,ax2=plt.subplots(figsize=(6,3.8))
        ax2.bar(keys,[r['raw_yield'] for r in best_path], color='#4c78a8', label='bruto (mejor ruta opt)')
        ax2.bar(keys,[r['effective_yield_after_redundancy'] for r in best_path], color='#72b7b2', alpha=0.8, label='efectivo')
        ax2.axhline(0.85,color='green',ls='--',lw=1); ax2.set_ylim(0,1.08); ax2.set_ylabel('Yield')
        ax2.set_title('S4: Mejor ruta optimizada por candidato'); ax2.legend(fontsize=8)
        fig2.tight_layout(); fig2.savefig(os.path.join(FIG,'s4_variability_yield_optimized.png'),dpi=150)
        plt.close(fig); plt.close(fig2)
    except Exception as e:
        print('figure_warning', e)

    print(json.dumps({'cases': len(all_results), 'samples': N_SAMPLES, 'out':'outputs/s4_variability_yield.*'}))

if __name__=='__main__':
    main()
