"""Polynomial nonlinear model fitting with temperature influence.

Generates synthetic phase-readout data from a temperature-dependent nonlinear ground-truth
response, fits polynomial models of varying degree, tracks coefficient changes vs temperature,
and reports selection criteria (RMSE, AIC, BIC) to guide model order.
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

from compounds import COMPOUNDS


def ground_truth_response(c: np.ndarray, T_c: float, dn_max: np.ndarray) -> np.ndarray:
    """Synthetic ground truth: saturating nonlinearity + temperature-dependent amplitude and curvature.

    w_i(c,T) = g_i(T) * (1-exp(-k_i(T)*c)) / (1-exp(-k_i(T))) normalized to [0,1] at c=1
    dn_eff = dn_max * w
    Temperature effects (illustrative): amplitude degrades slightly with T, curvature changes.
    """
    c = np.asarray(c, dtype=float)
    T_ref = 25.0
    dT = T_c - T_ref
    w = np.zeros_like(c, dtype=float)
    for i in range(len(c)):
        # material-specific illustrative parameters
        k0 = 1.8 + 0.2 * i            # base curvature
        kT = k0 * (1.0 + 0.003 * dT)  # curvature drifts with T
        gT = 1.0 - 0.0015 * dT        # effective amplitude/gain vs T
        gT = float(np.clip(gT, 0.7, 1.05))
        kT = float(np.clip(kT, 0.5, 6.0))
        denom = 1.0 - math.exp(-kT)
        w[i] = gT * (1.0 - math.exp(-kT * c[i])) / denom if abs(denom) > 1e-12 else gT * c[i]
    return dn_max * w


def build_A(L_um=100.0, confinement=0.35):
    n = len(COMPOUNDS)
    A = np.zeros((n, n), dtype=float)
    L_m = L_um * 1e-6
    for j, m_read in enumerate(COMPOUNDS):
        lam = m_read.read_nm * 1e-9
        for i, m_mat in enumerate(COMPOUNDS):
            dphi = (2 * math.pi / lam) * confinement * m_mat.delta_n_max * L_m
            if i == j:
                A[j, i] = dphi
            else:
                sep = abs(m_read.read_nm - COMPOUNDS[i].read_nm)
                A[j, i] = dphi * 0.03 * np.exp(-sep / 300.0)
    return A


def generate_dataset(temps=(15, 25, 35, 50, 65), n_per_temp=300, noise_sigma=0.01, seed=0):
    rng = np.random.default_rng(seed)
    A = build_A()
    dn_max = np.array([m.delta_n_max for m in COMPOUNDS], dtype=float)
    Xc, XT, Y = [], [], []
    # include structured multi-level states plus random continuous states
    levels = np.linspace(0, 1, 4)
    for T in temps:
        for _ in range(n_per_temp):
            if rng.random() < 0.5:
                c = rng.choice(levels, size=len(COMPOUNDS))
            else:
                c = rng.uniform(0, 1, size=len(COMPOUNDS))
            dn_eff = ground_truth_response(c, T, dn_max)
            w = np.divide(dn_eff, dn_max, out=np.zeros_like(dn_eff), where=np.abs(dn_max) > 1e-15)
            y = A @ w + rng.normal(0, noise_sigma, size=len(COMPOUNDS))
            Xc.append(c.copy()); XT.append(T); Y.append(y)
    return np.array(Xc), np.array(XT), np.array(Y), A, dn_max


def fit_polynomial_per_channel(Xc, XT, Y_eff, degree: int):
    """Fit y_eff_i ≈ sum_{p=0..d} a_{i,p}(T?) - here fit per temperature separately to observe coeff change,
    and also a global model with temperature terms.

    Y_eff: estimated effective weight/phase contribution target per channel (N, M).
    Returns per-temp coeffs and global coeffs/stats.
    """
    temps = sorted(set(XT.tolist()))
    M = Y_eff.shape[1]
    per_temp = {}
    for T in temps:
        mask = XT == T
        c = Xc[mask]  # (n,M) states but we fit per material/channel using its own c_i -> y_eff_i mapping
        y = Y_eff[mask]
        coeffs = []
        for i in range(M):
            # Vandermonde in c_i: [1, c, c^2, ...]
            V = np.vstack([c[:, i] ** p for p in range(degree + 1)]).T
            a, *_ = np.linalg.lstsq(V, y[:, i], rcond=None)
            coeffs.append(a)
        per_temp[float(T)] = np.array(coeffs)  # (M, degree+1)

    # global model: features [c^0..c^d, T, T*c, ... , T*c^d] (simple interaction)
    feats = []
    for p in range(degree + 1):
        for ci in range(M):
            feats.append((Xc[:, ci] ** p))
    # add temperature terms
    feats.append(XT)
    feats.append(XT ** 2)
    for p in range(1, degree + 1):
        feats.append(XT * (Xc.mean(axis=1) ** p))  # compact interaction proxy
    Phi = np.vstack(feats).T
    # fit each output channel with same design for simplicity
    Acoef, *_ = np.linalg.lstsq(Phi, Y_eff, rcond=None)
    pred = Phi @ Acoef
    resid = Y_eff - pred
    return per_temp, Acoef, pred, resid


def model_selection(out_dir: Path):
    Xc, XT, Y, A, dn_max = generate_dataset()
    # invert A to get effective weights target (noiseless-ish target proxy): w_hat = solve(A, y)
    # handle per-sample
    W_hat = np.linalg.solve(A, Y.T).T  # (N,M)

    N = len(Xc)
    idx = np.arange(N)
    rng = np.random.default_rng(1)
    rng.shuffle(idx)
    split = int(0.7 * N)
    tr, va = idx[:split], idx[split:]

    results = []
    all_per_temp = {}
    for deg in range(1, 7):
        per_temp, Acoef, pred, resid = fit_polynomial_per_channel(Xc[tr], XT[tr], W_hat[tr], deg)
        # validate
        # rebuild prediction on val using global fit? easier: fit global on train, eval on val
        M = W_hat.shape[1]
        def design(Xc_, XT_, d):
            feats = []
            for p in range(d + 1):
                for ci in range(M):
                    feats.append((Xc_[:, ci] ** p))
            feats.append(XT_); feats.append(XT_ ** 2)
            for p in range(1, d + 1):
                feats.append(XT_ * (Xc_.mean(axis=1) ** p))
            return np.vstack(feats).T
        Phi_tr = design(Xc[tr], XT[tr], deg)
        B, *_ = np.linalg.lstsq(Phi_tr, W_hat[tr], rcond=None)
        Phi_va = design(Xc[va], XT[va], deg)
        pred_va = Phi_va @ B
        resid_va = W_hat[va] - pred_va
        rmse_tr = float(np.sqrt(np.mean((Phi_tr @ B - W_hat[tr]) ** 2)))
        rmse_va = float(np.sqrt(np.mean(resid_va ** 2)))
        n = len(tr) * M
        k = B.size
        sse = float(np.sum((Phi_tr @ B - W_hat[tr]) ** 2))
        aic = n * math.log(max(sse / n, 1e-30)) + 2 * k
        bic = n * math.log(max(sse / n, 1e-30)) + k * math.log(n)
        all_per_temp[deg] = {str(T): per_temp[T].tolist() for T in per_temp}
        results.append({
            "degree": deg,
            "rmse_train": rmse_tr,
            "rmse_val": rmse_va,
            "aic": aic,
            "bic": bic,
            "n_params": k,
        })

    best_bic = min(results, key=lambda r: r["bic"])['degree']
    best_val = min(results, key=lambda r: r["rmse_val"])['degree']

    # coefficient change vs temperature for best degree (per-temp, material 0 as example)
    deg = best_bic
    per_temp, *_ = fit_polynomial_per_channel(Xc, XT, W_hat, deg)
    temps = sorted(per_temp.keys())
    coeff_tracks = []
    for T in temps:
        for mat in range(len(COMPOUNDS)):
            for p in range(deg + 1):
                coeff_tracks.append({
                    "degree": deg, "temperature_C": T, "material_index": mat,
                    "material": COMPOUNDS[mat].key, "power": p,
                    "coefficient": float(per_temp[T][mat, p]),
                })

    with (out_dir / "polynomial_model_selection.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(results)
    with (out_dir / "polynomial_coefficients_vs_temperature.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(coeff_tracks[0].keys()))
        w.writeheader(); w.writerows(coeff_tracks)

    # plots
    degs = [r['degree'] for r in results]
    plt.figure(figsize=(7,4))
    plt.plot(degs, [r['rmse_val'] for r in results], marker='o', label='RMSE validación')
    plt.plot(degs, [r['rmse_train'] for r in results], marker='s', label='RMSE entrenamiento')
    plt.xlabel('Grado del polinomio'); plt.ylabel('RMSE (pesos efectivos)')
    plt.title('Selección de grado polinómico (modelo no lineal con temperatura)')
    plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig(out_dir.parent / 'figures' / 'polynomial_degree_selection.png', dpi=160)
    plt.close()

    # coeff vs T for mat 0
    plt.figure(figsize=(7,4))
    for p in range(deg + 1):
        ys = [per_temp[T][0, p] for T in temps]
        plt.plot(temps, ys, marker='o', label=f'a{p} (c^{p})')
    plt.xlabel('Temperatura (°C)'); plt.ylabel('Coeficiente (material M1)')
    plt.title(f'Coeficientes polinómicos vs temperatura (grado {deg})')
    plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig(out_dir.parent / 'figures' / 'polynomial_coeffs_vs_temperature.png', dpi=160)
    plt.close()

    summary = {
        "best_degree_by_bic": best_bic,
        "best_degree_by_val_rmse": best_val,
        "selection_table": results,
        "temperatures_C": temps,
        "note": "Synthetic ground truth with temp-dependent saturating nonlinearity; coefficients fitted per temperature show drift with T. On real data, repeat with measured (c,T)->response.",
    }
    (out_dir / 'polynomial_fit_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary
