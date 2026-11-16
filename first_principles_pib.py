"""First-principles (simplified) estimates using particle-in-a-box models.

Estimates electronic transition wavelengths for conjugated systems via:
- 1D particle in an infinite potential well: E_n = n^2 h^2 / (8 m L^2)
- 2D rectangular infinite well: E_{nx,ny} = h^2/(8m) * (nx^2/Lx^2 + ny^2/Ly^2)

These are order-of-magnitude/trend estimates (free-electron model for π systems). They do
not replace measured spectra or ab initio calculations, but provide physics-based anchors
for absorption wavelengths and conjugation effects between conformers/states.

Assumptions:
- m = electron mass (free electron approximation)
- L (effective conjugation length) estimated from typical bond lengths and conjugated path
- N_pi electrons fill levels with 2 electrons per level (spin), HOMO = N_pi/2, LUMO = HOMO+1
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

# Physical constants (SI)
h = 6.62607015e-34       # J*s
hbar = h / (2 * math.pi)
m_e = 9.1093837015e-31   # kg
c = 299792458.0          # m/s
eV = 1.602176634e-19     # J
nm = 1e-9
angstrom = 1e-10


def energy_1d_J(n: int, L_m: float) -> float:
    return (n ** 2) * (h ** 2) / (8 * m_e * (L_m ** 2))


def transition_1d(N_pi: int, L_m: float):
    """HOMO-LUMO transition for N_pi electrons in 1D box of length L."""
    n_homo = max(1, N_pi // 2)
    n_lumo = n_homo + 1
    dE = energy_1d_J(n_lumo, L_m) - energy_1d_J(n_homo, L_m)
    lam = h * c / dE if dE > 0 else float("inf")
    return {
        "model": "1D_box",
        "N_pi_electrons": N_pi,
        "n_homo": n_homo,
        "n_lumo": n_lumo,
        "L_m": L_m,
        "L_angstrom": L_m / angstrom,
        "deltaE_J": dE,
        "deltaE_eV": dE / eV,
        "lambda_m": lam,
        "lambda_nm": lam / nm,
    }


def energy_2d_J(nx: int, ny: int, Lx_m: float, Ly_m: float) -> float:
    return (h ** 2 / (8 * m_e)) * ((nx ** 2) / (Lx_m ** 2) + (ny ** 2) / (Ly_m ** 2))


def transition_2d(N_pi: int, Lx_m: float, Ly_m: float):
    """Fill 2D box states by energy to get HOMO-LUMO gap (approximate)."""
    # generate levels
    levels = []
    nmax = max(12, N_pi)
    for nx in range(1, nmax + 1):
        for ny in range(1, nmax + 1):
            levels.append((energy_2d_J(nx, ny, Lx_m, Ly_m), nx, ny))
    levels.sort(key=lambda x: x[0])
    n_homo_idx = max(0, N_pi // 2 - 1)
    n_lumo_idx = n_homo_idx + 1
    if n_lumo_idx >= len(levels):
        n_lumo_idx = len(levels) - 1
    E_h, nxh, nyh = levels[n_homo_idx]
    E_l, nxl, nyl = levels[n_lumo_idx]
    dE = max(E_l - E_h, 1e-30)
    lam = h * c / dE
    return {
        "model": "2D_box",
        "N_pi_electrons": N_pi,
        "homo_state": [nxh, nyh],
        "lumo_state": [nxl, nyl],
        "Lx_m": Lx_m,
        "Ly_m": Ly_m,
        "Lx_angstrom": Lx_m / angstrom,
        "Ly_angstrom": Ly_m / angstrom,
        "deltaE_J": dE,
        "deltaE_eV": dE / eV,
        "lambda_m": lam,
        "lambda_nm": lam / nm,
    }


def build_species_parameters():
    """Effective conjugation parameters per material state/conformer (illustrative, first-principles-inspired).

    L_eff estimated as conjugated path length ~ (number of conjugated bonds) * ~1.4 A.
    N_pi as number of pi electrons in that conjugated system.
    Two states per material: A (one conformer/state) and B (other conformer/state).
    These are simplified assignments to enable estimation and must be refined with molecular structure.
    """
    return [
        # M1 Diarylethene: open (A) broken conjugation / shorter segments, closed (B) extended conjugation
        {"material": "M1", "compound": "Diarylethene (DTE)", "state": "A_open", "N_pi": 12, "L1_A": 7.0, "Lx_A": 7.0, "Ly_A": 3.0,
         "note": "Open-ring form: less extended conjugation (shorter effective path).", "target_band": "write ~313 nm region (UV)"},
        {"material": "M1", "compound": "Diarylethene (DTE)", "state": "B_closed", "N_pi": 18, "L1_A": 12.0, "Lx_A": 12.0, "Ly_A": 3.5,
         "note": "Closed-ring form: extended conjugation across backbone.", "target_band": "erase/read-visible shift; longer λ"},

        # M2 Azobenzene: trans (A) more planar/extended, cis (B) twisted/shorter effective conjugation
        {"material": "M2", "compound": "Azobenzene derivative", "state": "A_trans", "N_pi": 14, "L1_A": 9.5, "Lx_A": 9.5, "Ly_A": 3.0,
         "note": "Trans: planar, extended π conjugation.", "target_band": "strong π-π* (UV/blue)"},
        {"material": "M2", "compound": "Azobenzene derivative", "state": "B_cis", "N_pi": 14, "L1_A": 7.5, "Lx_A": 7.0, "Ly_A": 4.0,
         "note": "Cis: twisted geometry reduces effective conjugation length.", "target_band": "n-π* / shifted absorption"},

        # M3 Spiropyran (A, closed) vs Merocyanine (B, open zwitterionic, extended conjugation)
        {"material": "M3", "compound": "Spiropyran / Merocyanine", "state": "A_spiro", "N_pi": 12, "L1_A": 7.0, "Lx_A": 6.5, "Ly_A": 3.5,
         "note": "Spiropyran closed: orthogonal rings, limited conjugation.", "target_band": "UV"},
        {"material": "M3", "compound": "Spiropyran / Merocyanine", "state": "B_mero", "N_pi": 18, "L1_A": 12.5, "Lx_A": 12.0, "Ly_A": 3.5,
         "note": "Merocyanine open: extended conjugated polymethine-like system.", "target_band": "visible"},

        # M4 DASA: elongated colored (A/open in DASA context) vs cyclic/colorless (B)
        {"material": "M4", "compound": "DASA photoswitch", "state": "A_colored", "N_pi": 16, "L1_A": 11.0, "Lx_A": 11.0, "Ly_A": 3.5,
         "note": "Extended triene/enamine conjugation (colored form).", "target_band": "visible (~530-650 nm region)"},
        {"material": "M4", "compound": "DASA photoswitch", "state": "B_cyclized", "N_pi": 10, "L1_A": 6.0, "Lx_A": 6.0, "Ly_A": 3.5,
         "note": "Cyclized form: disrupted conjugation.", "target_band": "UV/bleached"},
    ]


def run_estimates(out_dir: Path):
    params = build_species_parameters()
    rows = []
    for p in params:
        L1 = p["L1_A"] * angstrom
        Lx = p["Lx_A"] * angstrom
        Ly = p["Ly_A"] * angstrom
        r1 = transition_1d(p["N_pi"], L1)
        r2 = transition_2d(p["N_pi"], Lx, Ly)
        row = {
            "material": p["material"],
            "compound": p["compound"],
            "state_conformer": p["state"],
            "N_pi_electrons": p["N_pi"],
            "L1D_A": p["L1_A"],
            "Lx_A": p["Lx_A"],
            "Ly_A": p["Ly_A"],
            "lambda_1D_nm": r1["lambda_nm"],
            "deltaE_1D_eV": r1["deltaE_eV"],
            "lambda_2D_nm": r2["lambda_nm"],
            "deltaE_2D_eV": r2["deltaE_eV"],
            "homo_2D": str(r2["homo_state"]),
            "lumo_2D": str(r2["lumo_state"]),
            "note": p["note"],
            "target_band": p["target_band"],
        }
        rows.append(row)

    # comparison to assumed operating wavelengths in compounds.py (qualitative mapping)
    assumed = {
        "M1": {"write_nm": 313.0, "erase_nm": 530.0, "read_nm": 1550.0},
        "M2": {"write_nm": 365.0, "erase_nm": 450.0, "read_nm": 1310.0},
        "M3": {"write_nm": 405.0, "erase_nm": 590.0, "read_nm": 980.0},
        "M4": {"write_nm": 660.0, "erase_nm": 700.0, "read_nm": 850.0},
    }
    for r in rows:
        r.update(assumed.get(r["material"], {}))

    with (out_dir / "first_principles_pib_estimates.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # plot
    labels = [f"{r['material']}\n{r['state_conformer'].split('_',1)[1]}" for r in rows]
    l1 = [r["lambda_1D_nm"] for r in rows]
    l2 = [r["lambda_2D_nm"] for r in rows]
    x = np.arange(len(rows))
    width = 0.35
    plt.figure(figsize=(11, 4.5))
    plt.bar(x - width/2, l1, width, label="1D caja (PIB)")
    plt.bar(x + width/2, l2, width, label="2D caja (PIB)")
    # show assumed write/erase refs per material group (approx)
    for i, r in enumerate(rows):
        plt.plot([i-width/2, i+width/2], [r.get("write_nm", np.nan)]*2, 'k_', alpha=0.3)
    plt.xticks(x, labels, fontsize=8)
    plt.ylabel("λ estimada (nm)")
    plt.title("Estimación de transición electrónica (primeros principios simplificados: caja 1D/2D)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir.parent / "figures" / "first_principles_pib_wavelengths.png", dpi=160)
    plt.close()

    summary = {
        "method": "Particle-in-a-box (free-electron) 1D and 2D infinite potential well",
        "purpose": "Order-of-magnitude/trend estimates of HOMO-LUMO transition wavelengths vs conjugation length/state",
        "limitations": [
            "Ignores electron-electron interactions, exchange/correlation, and real molecular potential",
            "Effective box lengths and N_pi are approximate; substituents/heteroatoms/solvent/matrix not modeled",
            "Oscillator strengths and full ε(λ) lineshapes not predicted; use measured spectra for quantitative Beer-Lambert",
        ],
        "rows": len(rows),
    }
    (out_dir / "first_principles_pib_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return rows, summary
