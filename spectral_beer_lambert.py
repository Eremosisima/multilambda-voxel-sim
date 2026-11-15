"""Spectral Beer-Lambert model for mixtures with state/conformer-specific absorption.

Models each photoswitch material as having (at least) two stable states/conformers with
distinct absorption spectra ε(λ). Total attenuation follows Beer-Lambert:
    A(λ)=l * Σ_{i,s} ε_{i,s}(λ) * C_{i,s}  (base-10 form) or
    I/I0 = exp(-l * Σ_{i,s} α_{i,s}(λ)) with α_{i,s}=ln(10)*ε_{i,s}*C_{i,s}.

This module estimates wavelength selectivity and parasitic absorption (crosstalk) in a
mixed/conformer-populated voxel. Parameters are illustrative approximations.
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


def gaussian_band(lam_nm, center_nm, sigma_nm, amplitude):
    """Spectral band shape (amplitude in absorption-coefficient units, e.g. 1/cm or 1/um scaled)."""
    return amplitude * np.exp(-0.5 * ((lam_nm - center_nm) / sigma_nm) ** 2)


class SpeciesSpectrum:
    def __init__(self, material_key: str, state: str, bands):
        self.material_key = material_key
        self.state = state  # e.g. 'A','B' (conformers/states)
        self.bands = bands  # list of (center_nm, sigma_nm, amplitude_alpha_per_um)

    def alpha_per_um(self, lam_nm):
        a = np.zeros_like(np.asarray(lam_nm, dtype=float))
        for c, s, amp in self.bands:
            a = a + gaussian_band(np.asarray(lam_nm, dtype=float), c, s, amp)
        return a


def build_spectral_library():
    """Illustrative spectra per material state/conformer.

    Amplitudes in 1/um (so that alpha*path_um is dimensionless in exp). Chosen to give
    plausible strong absorption at write/erase bands and low residual at read bands.
    Each material modeled with two states: state A (initial) and state B (switched).
    """
    lib = []
    for m in COMPOUNDS:
        # State A: absorbs mainly at write wavelength
        lib.append(SpeciesSpectrum(m.key, 'A', [
            (m.write_nm, max(20.0, 0.08 * m.write_nm), 2.0),
            (m.read_nm, 60.0, 0.002),  # residual in read channel
        ]))
        # State B (conformer/product): absorbs mainly at erase wavelength, different spectrum
        lib.append(SpeciesSpectrum(m.key, 'B', [
            (m.erase_nm, max(25.0, 0.10 * m.erase_nm), 1.6),
            (m.write_nm, 40.0, 0.15),  # possible overlap/back-conversion band
            (m.read_nm, 60.0, 0.001),
        ]))
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


def selectivity_analysis(out_dir: Path):
    lib = build_spectral_library()
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
    summary = {
        'model': 'Beer-Lambert spectral mixture with two states/conformers per material (illustrative Gaussian bands)',
        'assumptions': 'alpha in 1/um scaled; path 1 um; concentration_scale 0.5; spectra are approximations not measured data',
        'mean_write_selectivity_all_state_A': float(np.mean([r['selectivity_intended_over_absorbed'] for r in write_rows if r['selectivity_intended_over_absorbed'] is not None])),
        'max_read_absorbed_fraction': float(np.max([r['absorbed_fraction_total'] for r in read_rows])),
        'note': 'Explicit ε(λ) and conformer populations enable quantitative selectivity/crosstalk; replace with measured spectra for real compounds.'
    }
    (out_dir / 'beer_lambert_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary
