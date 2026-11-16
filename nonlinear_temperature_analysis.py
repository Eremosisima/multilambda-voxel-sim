"""Analysis of linear-model validity: nonlinear response and temperature dependence.

This is a physics-informed simulation study (not experimental proof). It compares
linear assumptions against plausible nonlinear/saturation and temperature effects.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from compounds import COMPOUNDS, level_fractions
from model import ideal_response_matrix, forward_readout, invert_readout, quantize_levels


def linear_response(c, dn_max):
    return c * dn_max


def saturating_response(c, dn_max, k=2.0):
    """Monotonic saturating response: reaches ~dn_max as c->1 with curvature.
    Normalized so that f(0)=0 and f(1)=dn_max.
    """
    c = np.asarray(c, dtype=float)
    denom = 1.0 - math.exp(-k)
    return dn_max * (1.0 - np.exp(-k * c)) / denom


def logistic_response(c, dn_max, steepness=6.0, midpoint=0.5):
    """Sigmoidal/nonlinear conversion curve, normalized to [0,dn_max] on c in [0,1]."""
    c = np.asarray(c, dtype=float)
    def g(x):
        return 1.0 / (1.0 + np.exp(-steepness * (x - midpoint)))
    g0, g1 = g(0.0), g(1.0)
    return dn_max * (g(c) - g0) / (g1 - g0)


def effective_A_from_nonlinear(A_linear, c, response_fn, **kwargs):
    """Build effective readout for nonlinear material response.

    Assumes phase contribution of material i scales with its effective dn(c_i)
    relative to dn_max, while matrix structure/crosstalk shape stays same as first-order.
    y = A_linear @ w(c), where w_i = response_i(c_i)/dn_max_i in [0,1].
    """
    c = np.asarray(c, dtype=float)
    dn_max = np.array([m.delta_n_max for m in COMPOUNDS], dtype=float)
    eff = np.array([response_fn(ci, dni, **kwargs) for ci, dni in zip(c, dn_max)], dtype=float)
    w = np.divide(eff, dn_max, out=np.zeros_like(eff), where=np.abs(dn_max) > 1e-15)
    return A_linear @ w, w, eff


def compare_linear_nonlinear(out_dir: Path):
    A = ideal_response_matrix(L_um=100.0, confinement=0.35)
    fr = level_fractions(4)
    rng = np.random.default_rng(7)
    models = {
        "linear": (linear_response, {}),
        "saturating_k2": (saturating_response, {"k": 2.0}),
        "logistic_s6": (logistic_response, {"steepness": 6.0, "midpoint": 0.5}),
    }
    rows = []
    trials = 400
    for name, (fn, kw) in models.items():
        correct = 0
        sym_err = 0
        se = 0.0
        for _ in range(trials):
            idx_true = rng.integers(0, 4, size=len(COMPOUNDS))
            c = fr[idx_true]
            y, w, eff = effective_A_from_nonlinear(A, c, fn, **kw)
            # decoder assumes calibrated LINEAR model (common practical risk)
            c_hat = invert_readout(y, A)
            _, idx_hat = quantize_levels(c_hat, 4)
            correct += int(np.all(idx_hat == idx_true))
            sym_err += int(np.sum(idx_hat != idx_true))
            se += float(np.sum((c_hat - c) ** 2))
        rows.append({
            "response_model": name,
            "decoder_assumption": "linear",
            "word_accuracy": correct / trials,
            "symbol_error_rate": sym_err / (trials * len(COMPOUNDS)),
            "mse_state_estimate": se / trials,
            "trials": trials,
        })

    # if decoder calibrated to nonlinear mapping (oracle linearization in state domain)
    for name, (fn, kw) in [("saturating_k2", (saturating_response, {"k": 2.0})), ("logistic_s6", (logistic_response, {"steepness": 6.0, "midpoint": 0.5}))]:
        correct = 0
        sym_err = 0
        se = 0.0
        for _ in range(trials):
            idx_true = rng.integers(0, 4, size=len(COMPOUNDS))
            c = fr[idx_true]
            y, w, eff = effective_A_from_nonlinear(A, c, fn, **kw)
            # oracle: knows effective weights w(c) relation but must infer c from y via linear A -> gets w, then invert monotonic map numerically
            w_hat = invert_readout(y, A)
            # invert response per material by search over c in [0,1]
            c_hat = []
            dn_max = np.array([m.delta_n_max for m in COMPOUNDS], dtype=float)
            grid = np.linspace(0, 1, 2001)
            for i in range(len(COMPOUNDS)):
                target = w_hat[i] * dn_max[i]
                resp = fn(grid, dn_max[i], **kw)
                j = int(np.argmin(np.abs(resp - target)))
                c_hat.append(grid[j])
            c_hat = np.array(c_hat)
            _, idx_hat = quantize_levels(c_hat, 4)
            correct += int(np.all(idx_hat == idx_true))
            sym_err += int(np.sum(idx_hat != idx_true))
            se += float(np.sum((c_hat - c) ** 2))
        rows.append({
            "response_model": name,
            "decoder_assumption": "calibrated_nonlinear_inverse",
            "word_accuracy": correct / trials,
            "symbol_error_rate": sym_err / (trials * len(COMPOUNDS)),
            "mse_state_estimate": se / trials,
            "trials": trials,
        })

    # plot response curves
    cgrid = np.linspace(0, 1, 200)
    plt.figure(figsize=(7, 4))
    plt.plot(cgrid, linear_response(cgrid, 1.0), label="lineal")
    plt.plot(cgrid, saturating_response(cgrid, 1.0, k=2.0), label="saturante (k=2)")
    plt.plot(cgrid, logistic_response(cgrid, 1.0, steepness=6.0), label="logística (s=6)")
    plt.xlabel("Estado normalizado c")
    plt.ylabel("Respuesta efectiva normalizada Δn_eff/Δn_max")
    plt.title("Modelos de respuesta lineal vs no lineal (ilustrativos)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir.parent / "figures" / "nonlinear_response_curves.png", dpi=160)
    plt.close()

    with (out_dir / "nonlinear_model_comparison.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


def temperature_analysis(out_dir: Path):
    """Assess temperature dependence: thermo-optic phase drift and retention (Arrhenius)."""
    rows = []
    # 1) Thermo-optic drift contribution vs temperature change
    L_m = 100e-6
    Gamma = 0.35
    dn_dT = 1e-5  # 1/K, order-of-magnitude for polymer/integrated stacks (assumption)
    for dT in [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]:
        for m in COMPOUNDS:
            lam = m.read_nm * 1e-9
            dphi = (2 * math.pi / lam) * Gamma * dn_dT * dT * L_m
            step = abs((2 * math.pi / lam) * Gamma * m.delta_n_max * L_m / 3.0)
            rows.append({
                "analysis": "thermo_optic_drift",
                "material": m.key,
                "read_nm": m.read_nm,
                "deltaT_K": dT,
                "phase_drift_rad": abs(dphi),
                "phase_step_rad": step,
                "drift_over_step": abs(dphi) / step if step else None,
            })

    # 2) Retention under temperature (Arrhenius): k(T)=k_ref*exp(-Ea/R*(1/T-1/Tref)), t1/2=ln2/k
    R = 8.314462618
    Ea = 80000.0  # J/mol illustrative activation energy for thermal back-reaction
    Tref = 293.15
    retention_rows = []
    for dT in [0, 10, 20, 40, 60]:
        T = Tref + dT
        factor = math.exp(-Ea / R * (1.0 / T - 1.0 / Tref))  # rate multiplier vs ref
        for m in COMPOUNDS:
            t_half_ref = m.thermal_half_life_s
            k_ref = math.log(2) / max(t_half_ref, 1e-30)
            kT = k_ref * factor
            t_half_T = math.log(2) / kT if kT > 0 else float("inf")
            retention_rows.append({
                "analysis": "thermal_retention_arrhenius",
                "material": m.key,
                "deltaT_above_ref_K": dT,
                "temperature_K": T,
                "t_half_ref_s": t_half_ref,
                "t_half_at_T_s": t_half_T,
                "rate_multiplier_vs_ref": factor,
                "Ea_J_per_mol_assumed": Ea,
            })

    # 3) Required temperature stability for given drift budget (fraction of half-step)
    budget_frac = 0.1  # 10% of half-step margin
    stab_rows = []
    for m in COMPOUNDS:
        lam = m.read_nm * 1e-9
        step = abs((2 * math.pi / lam) * Gamma * m.delta_n_max * L_m / 3.0)
        half_margin = step / 2.0
        budget = budget_frac * half_margin
        sens = (2 * math.pi / lam) * Gamma * dn_dT * L_m  # rad/K
        dT_max = budget / sens if sens else float("inf")
        stab_rows.append({
            "material": m.key,
            "read_nm": m.read_nm,
            "phase_step_rad": step,
            "half_step_margin_rad": half_margin,
            "drift_budget_rad": budget,
            "phase_sensitivity_rad_per_K": sens,
            "max_deltaT_for_budget_K": dT_max,
            "budget_fraction_of_half_step": budget_frac,
        })

    with (out_dir / "temperature_thermo_optic.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with (out_dir / "temperature_retention_arrhenius.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(retention_rows[0].keys()))
        w.writeheader(); w.writerows(retention_rows)
    with (out_dir / "temperature_stability_budget.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(stab_rows[0].keys()))
        w.writeheader(); w.writerows(stab_rows)

    # plot drift over step
    mats = [m.key for m in COMPOUNDS]
    dTs = [0.1, 0.5, 1.0, 5.0, 10.0]
    plt.figure(figsize=(7,4))
    for m in COMPOUNDS:
        vals = [r["drift_over_step"] for r in rows if r["analysis"]=="thermo_optic_drift" and r["material"]==m.key and r["deltaT_K"] in dTs]
        plt.plot(dTs, vals, marker="o", label=f"{m.key} ({m.read_nm} nm)")
    plt.axhline(0.1, color="r", linestyle="--", alpha=0.6, label="10% del paso (ref)")
    plt.xlabel("ΔT (K)")
    plt.ylabel("|deriva de fase| / paso de nivel")
    plt.title("Deriva termo-óptica relativa vs cambio de temperatura (modelo)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir.parent / "figures" / "thermo_optic_drift.png", dpi=160)
    plt.close()

    # plot retention
    plt.figure(figsize=(7,4))
    dTs_r = [0,10,20,40,60]
    for m in COMPOUNDS:
        vals = [r["t_half_at_T_s"] for r in retention_rows if r["material"]==m.key]
        plt.semilogy(dTs_r, vals, marker="o", label=m.key)
    plt.xlabel("ΔT sobre referencia (K)")
    plt.ylabel("Vida media t1/2 (s)")
    plt.title("Retención térmica (Arrhenius, Ea asumida)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir.parent / "figures" / "thermal_retention_arrhenius.png", dpi=160)
    plt.close()

    summary = {
        "thermo_optic_model": {"dn_dT_per_K": dn_dT, "L_um": 100.0, "confinement": 0.35, "note": "Order-of-magnitude; real dn/dT depends on material/stack."},
        "arrhenius_model": {"Ea_J_per_mol": Ea, "T_ref_K": Tref, "note": "Illustrative Ea; actual kinetics material-specific."},
        "stability_budget_fraction_of_half_step": budget_frac,
        "max_deltaT_for_budget_K_by_material": {r["material"]: r["max_deltaT_for_budget_K"] for r in stab_rows},
        "worst_case_max_deltaT_for_budget_K": min(r["max_deltaT_for_budget_K"] for r in stab_rows),
    }
    return rows, retention_rows, stab_rows, summary


def main(out_dir: Path):
    nl_rows = compare_linear_nonlinear(out_dir)
    to_rows, ret_rows, stab_rows, t_summary = temperature_analysis(out_dir)
    report = {
        "linear_model_assessment": {
            "conclusion": "Linear model is a valid first-order approximation in a limited regime, but nonlinear/saturation response and calibration are likely required for accurate multi-level operation.",
            "evidence": nl_rows,
            "recommendation": "Characterize dn_eff vs control/state experimentally; use calibrated inverse mapping or nonlinear model in decoder if response is not linear.",
        },
        "temperature_assessment": {
            "conclusion": "Temperature must be considered: thermo-optic drift can consume phase margin, and thermal back-reaction (retention) is strongly temperature-dependent.",
            "stability_budget": t_summary,
            "recommendation": "Include thermal management/stabilization and temperature-aware calibration; measure dn/dT, Ea and kinetics per material.",
        },
    }
    (out_dir / "nonlinear_temperature_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (out_dir / "nonlinear_temperature_report.md").open("w", encoding="utf-8") as f:
        f.write("# Análisis: validez del modelo lineal y dependencia de temperatura\n\n")
        f.write("## 1. ¿Funciona el modelo lineal o se requiere no linealidad?\n\n")
        f.write("**Conclusión:** el modelo lineal es una aproximación de primer orden útil, pero **no debe asumirse universalmente**. En materiales fotosensibles reales es plausible encontrar saturación/no linealidad en la relación control/estado → Δn efectivo, además de histéresis, fatiga o dependencia espectral.\n\n")
        f.write("Comparación (decodificador asumiendo linealidad vs respuesta efectiva no lineal ilustrativa):\n\n")
        f.write("| Respuesta efectiva | Supuesto del decodificador | Exactitud palabra | SER | MSE estado |\n|---|---|---:|---:|---:|\n")
        for r in nl_rows:
            f.write(f"| {r['response_model']} | {r['decoder_assumption']} | {r['word_accuracy']:.3f} | {r['symbol_error_rate']:.3f} | {r['mse_state_estimate']:.4f} |\n")
        f.write("\nImplicación: si la respuesta real es no lineal y el decodificador usa el modelo lineal sin calibración, aparecen errores de cuantización/decodificación. Con **calibración e inversa no lineal** (mapeo caracterizado) se puede recuperar desempeño en la medida en que la respuesta sea monotónica y estable.\n\n")
        f.write("**Recomendación:** medir/ajustar `Δn_eff(c, λ, T, historial)`; usar LUT o modelo inverso calibrado por canal/material; verificar linealidad por rangos de operación.\n\n")
        f.write("## 2. ¿Hay que considerar la temperatura?\n\n")
        f.write("**Conclusión: sí.** La temperatura afecta al menos (i) la **fase leída** vía efecto termo-óptico (deriva) y (ii) la **retención/estado** vía cinética térmica (back-reaction).\n\n")
        f.write(f"- Deriva termo-óptica (modelo, dn/dT={t_summary['thermo_optic_model']['dn_dT_per_K']}/K, L=100 µm, Γ=0.35): para mantener deriva ≤ {t_summary['stability_budget_fraction_of_half_step']*100:.0f}% del medio paso, el peor caso entre canales requiere estabilidad aproximada mejor que **{t_summary['worst_case_max_deltaT_for_budget_K']:.2f} K** (ver `temperature_stability_budget.csv`).\n")
        f.write("- Retención (Arrhenius ilustrativo, Ea asumida): la vida media disminuye rápidamente al aumentar T; los valores reales dependen del material/matriz y deben medirse (ver `temperature_retention_arrhenius.csv`, `figures/thermal_retention_arrhenius.png`).\n\n")
        f.write("**Recomendación:** control/estabilización térmica o compensación en lectura; calibración dependiente de temperatura; caracterización de dn/dT y cinética (Ea, tasas) por compuesto.\n\n")
        f.write("## Artefactos\n- `outputs/nonlinear_model_comparison.csv`\n- `outputs/temperature_thermo_optic.csv`, `outputs/temperature_retention_arrhenius.csv`, `outputs/temperature_stability_budget.csv`\n- `outputs/nonlinear_temperature_summary.json`\n- `figures/nonlinear_response_curves.png`, `figures/thermo_optic_drift.png`, `figures/thermal_retention_arrhenius.png`\n")
    return report
