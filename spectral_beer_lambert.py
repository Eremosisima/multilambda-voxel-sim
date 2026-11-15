"""Spectral Beer-Lambert model for mixtures with state/conformer-specific absorption.

Models each photoswitch material as having (at least) two stable states/conformers with
distinct absorption spectra ε(λ). Total attenuation follows Beer-Lambert:
    A(λ)=l * Σ_{i,s} ε_{i,s}(λ) * C_{i,s}  (base-10 form) or
    I/I0 = exp(-l * Σ_{i,s} α_{i,s}(λ)) with α_{i,s}=ln(10)*ε_{i,s}*C_{i,s}.

This module estimates wavelength selectivity and parasitic absorption (crosstalk) in a
mixed/conformer-populated voxel. Uses illustrative Gaussian bands by default; if real
spectra are provided under data/spectra/ (per material/state) they can be loaded via
spectral_data_loader.py with user-supplied concentrations.
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
from spectral_data_loader import (
    load_spectrum_csv,
    load_epsilon_spectrum_csv,
    epsilon_to_alpha_per_um,
    interpolate_alpha,
    available_spectra,
)


def gaussian_band(lam_nm, center_nm, sigma_nm, amplitude):
    """Spectral band shape (amplitude in absorption-coefficient units, e.g. 1/cm or 1/um scaled)."""
    return amplitude * np.exp(-0.5 * ((lam_nm - center_nm) / sigma_nm) ** 2)


class SpeciesSpectrum:
    def __init__(self, material_key: str, state: str, bands=None, tabulated=None, source: str | None = None):
        self.material_key = material_key
        self.state = state  # e.g. 'A','B' (conformers/states)
        self.bands = bands or []  # list of (center_nm, sigma_nm, amplitude_alpha_per_um)
        self.tabulated = tabulated  # optional (wavelength_nm, alpha_per_um) arrays
        self.source = source

    def alpha_per_um(self, lam_nm):
        lam = np.asarray(lam_nm, dtype=float)
        if self.tabulated is not None:
            wl, a = self.tabulated
            return interpolate_alpha(wl, a, lam)
        a = np.zeros_like(lam)
        for c, s, amp in self.bands:
            a = a + gaussian_band(lam, c, s, amp)
        return a


def _load_real_state_spectrum(material_key: str, state: str, data_dir: Path, concentration_mol_L: float | None = None):
    """Try to load a real spectrum for material/state from data/spectra/.

    Looks for files named like M1_A.csv, M1_B.csv (anywhere under data/spectra/).
    If epsilon-only, concentration_mol_L must be provided.
    Returns (wavelength_nm, alpha_per_um, path_str) or None.
    """
    spec_dir = data_dir / "spectra"
    if not spec_dir.exists():
        return None
    candidates = [spec_dir / f"{material_key}_{state}.csv"]
    candidates += list(spec_dir.rglob(f"{material_key}_{state}.csv"))
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        return None
    try:
        wl, a = load_spectrum_csv(path, concentration_mol_L=concentration_mol_L)
        return wl, a, str(path)
    except Exception:
        if concentration_mol_L is None:
            # keep epsilon shape unusable as alpha; caller may handle
            return None
        return None


def build_spectral_library(data_dir: Path | None = None, concentration_mol_L: float | None = None):
    """Build spectra per material state/conformer.

    If data_dir is provided (or default data/ exists) and per-state CSVs named
    M{n}_A.csv / M{n}_B.csv are found with usable alpha (or epsilon+concentration),
    they are used; otherwise illustrative Gaussian bands are generated.
    """
    if data_dir is None:
        data_dir = Path(__file__).parent / "data"
    lib = []
    for m in COMPOUNDS:
        for state in ("A", "B"):
            real = _load_real_state_spectrum(m.key, state, data_dir, concentration_mol_L=concentration_mol_L)
            if real is not None:
                wl, a, src = real
                lib.append(SpeciesSpectrum(m.key, state, tabulated=(wl, a), source=src))
                continue
            if state == "A":
                bands = [(m.write_nm, max(20.0, 0.08 * m.write_nm), 2.0), (m.read_nm, 60.0, 0.002)]
            else:
                bands = [(m.erase_nm, max(25.0, 0.10 * m.erase_nm), 1.6), (m.write_nm, 40.0, 0.15), (m.read_nm, 60.0, 0.001)]
            lib.append(SpeciesSpectrum(m.key, state, bands=bands, source="illustrative"))
    return lib


def populations_from_state(c):
    """Map conversion state c_i in [0,1] to conformer populations (C_A, C_B) fractions summing to 1 per material."""
    c = np.asarray(c, dtype=float)
    pops = {}
    for i, m in enumerate(COMPOUNDS):
        pops[(m.key, 'A')] = 1.0 - c[i]
        pops[(m.key, 'B')] = c[i]
    return pops


def mixture_absorption(lam_nm, c, lib, path_um=1.0, concentration_scale=1.0):
    """Compute total alpha and per-species alpha contributions.

    concentration_scale represents effective concentration/packing (dimensionless factor).
    Returns dict with totals and per-species fractions.
    """
    pops = populations_from_state(c)
    lam_nm = np.asarray(lam_nm, dtype=float)
    alpha_species = {}
    alpha_total = np.zeros_like(lam_nm, dtype=float)
    for sp in lib:
        frac = pops[(sp.material_key, sp.state)]
        a = sp.alpha_per_um(lam_nm) * frac * concentration_scale
        alpha_species[(sp.material_key, sp.state)] = a
        alpha_total = alpha_total + a
    absorbed_total = 1.0 - np.exp(-alpha_total * path_um)
    # fraction of absorbed photons attributed to each species (for alpha_total>0)
    contrib = {}
    with np.errstate(divide='ignore', invalid='ignore'):
        for k, a in alpha_species.items():
            frac_abs = np.where(alpha_total > 1e-30, (a / alpha_total) * absorbed_total, 0.0)
            contrib[k] = frac_abs
    return {
        'lambda_nm': lam_nm,
        'alpha_total_per_um': alpha_total,
        'absorbed_fraction_total': absorbed_total,
        'alpha_species_per_um': alpha_species,
        'absorbed_fraction_species': contrib,
    }


def selectivity_analysis(out_dir: Path, data_dir: Path | None = None, concentration_mol_L: float | None = None):
    if data_dir is None:
        data_dir = Path(__file__).parent / "data"
    lib = build_spectral_library(data_dir=data_dir, concentration_mol_L=concentration_mol_L)
    lambdas = np.linspace(300, 1700, 1401)
    # scenarios: all in state A (c=0), all in state B (c=1), mixed
    scenarios = {
        'all_state_A': np.zeros(len(COMPOUNDS)),
        'all_state_B': np.ones(len(COMPOUNDS)),
        'mixed_half': np.full(len(COMPOUNDS), 0.5),
    }
    rows = []
    # evaluate at key write/erase/read wavelengths
    key_lams = []
    for m in COMPOUNDS:
        key_lams += [('write', m.key, m.write_nm), ('erase', m.key, m.erase_nm), ('read', m.key, m.read_nm)]

    for sname, c in scenarios.items():
        for kind, target, lam in key_lams:
            res = mixture_absorption(np.array([lam]), c, lib, path_um=1.0, concentration_scale=0.5)
            absorbed_total = float(res['absorbed_fraction_total'][0])
            # intended species depends on operation
            if kind == 'write':
                intended = (target, 'A')
            elif kind == 'erase':
                intended = (target, 'B')
            else:  # read - ideally minimal absorption by any
                intended = None
            intended_abs = float(res['absorbed_fraction_species'][intended][0]) if intended else 0.0
            parasitic = absorbed_total - intended_abs if intended else absorbed_total
            selectivity = (intended_abs / absorbed_total) if (intended and absorbed_total > 1e-15) else None
            rows.append({
                'scenario': sname,
                'operation': kind,
                'target_material': target,
                'lambda_nm': lam,
                'absorbed_fraction_total': absorbed_total,
                'absorbed_fraction_intended': intended_abs if intended else None,
                'absorbed_fraction_parasitic': parasitic,
                'selectivity_intended_over_absorbed': selectivity,
            })

    # spectra for plotting (mixed case)
    c = scenarios['mixed_half']
    plt.figure(figsize=(9, 4.5))
    for sp in lib:
        a = sp.alpha_per_um(lambdas) * (0.5 if sp.state in ('A','B') else 1.0) * 0.5
        plt.plot(lambdas, a, label=f"{sp.material_key}-{sp.state}", alpha=0.7)
    # mark key wavelengths
    for m in COMPOUNDS:
        plt.axvline(m.write_nm, color='k', alpha=0.08)
    plt.xlabel('Longitud de onda (nm)')
    plt.ylabel('Contribución α (1/µm, ilustrativa)')
    plt.title('Espectros de absorción ilustrativos por especie/conformero (mezcla 50/50)')
    plt.legend(ncol=4, fontsize=8)
    plt.tight_layout()
    plt.savefig(out_dir.parent / 'figures' / 'beer_lambert_spectra_conformers.png', dpi=160)
    plt.close()

    # selectivity summary at write wavelengths
    plt.figure(figsize=(7,4))
    sw = [r for r in rows if r['scenario']=='all_state_A' and r['operation']=='write']
    labels = [r['target_material'] for r in sw]
    vals = [r['selectivity_intended_over_absorbed'] if r['selectivity_intended_over_absorbed'] is not None else 0 for r in sw]
    plt.bar(labels, vals, color='#4C72B0')
    plt.ylim(0,1.05)
    plt.ylabel('Selectividad (absorción destinada / total)')
    plt.title('Selectividad espectral en escritura (Beer-Lambert, mezcla ilustrativa)')
    plt.tight_layout()
    plt.savefig(out_dir.parent / 'figures' / 'beer_lambert_write_selectivity.png', dpi=160)
    plt.close()

    with (out_dir / 'beer_lambert_selectivity.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    # quick summary metrics
    write_rows = [r for r in rows if r['operation']=='write' and r['scenario']=='all_state_A']
    read_rows = [r for r in rows if r['operation']=='read']
    sources = sorted({sp.source for sp in lib if sp.source})
    uses_real = any(sp.source and sp.source != 'illustrative' for sp in lib)
    summary = {
        'model': 'Beer-Lambert spectral mixture with two states/conformers per material',
        'assumptions': 'alpha in 1/um scaled; path 1 um; concentration_scale 0.5; per-state spectra illustrative unless replaced by real CSVs (M{n}_A/B) with concentration',
        'uses_real_spectra': uses_real,
        'spectral_sources': sources,
        'available_spectra_files': {k: str(v) for k, v in available_spectra(data_dir).items()},
        'mean_write_selectivity_all_state_A': float(np.mean([r['selectivity_intended_over_absorbed'] for r in write_rows if r['selectivity_intended_over_absorbed'] is not None])),
        'max_read_absorbed_fraction': float(np.max([r['absorbed_fraction_total'] for r in read_rows])),
        'note': 'Explicit ε(λ) and conformer populations enable quantitative selectivity/crosstalk; replace with measured spectra and user-supplied concentrations for real compounds.'
    }
    (out_dir / 'beer_lambert_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary
