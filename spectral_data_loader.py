"""Loader and helpers for measured/cited spectral data (Beer-Lambert).

If CSV spectra are provided under data/spectra/, they can be loaded and interpolated.
Otherwise, illustrative Gaussian spectra from spectral_beer_lambert are used.

Expected CSV columns (flexible): wavelength_nm and one of alpha_per_um, alpha_per_cm, epsilon_L_mol_cm.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
import numpy as np


def _to_float(row, *keys, default=None):
    for k in keys:
        if k in row and row[k] not in (None, ""):
            try:
                return float(row[k])
            except ValueError:
                pass
    return default


def load_spectrum_csv(path: Path):
    """Load a spectrum CSV and return (wavelength_nm_sorted, alpha_per_um)."""
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    wl, alpha = [], []
    for r in rows:
        w = _to_float(r, "wavelength_nm", "lambda_nm", "nm", "wl_nm")
        if w is None:
            continue
        a_um = _to_float(r, "alpha_per_um")
        a_cm = _to_float(r, "alpha_per_cm")
        eps = _to_float(r, "epsilon_L_mol_cm", "epsilon", "molar_absorptivity")
        conc = _to_float(r, "concentration_mol_L", "concentration_M", default=None)
        if a_um is None and a_cm is not None:
            a_um = a_cm / 1e4  # 1/cm -> 1/um
        if a_um is None and eps is not None and conc is not None:
            # alpha (1/cm, natural log base) = ln(10) * epsilon * C
            a_cm_calc = math.log(10) * eps * conc
            a_um = a_cm_calc / 1e4
        if a_um is None:
            continue
        wl.append(w)
        alpha.append(a_um)
    if not wl:
        raise ValueError(f"No usable spectral data in {path}")
    order = np.argsort(wl)
    return np.array(wl, dtype=float)[order], np.array(alpha, dtype=float)[order]


def interpolate_alpha(wl_nm, alpha_per_um, query_wl_nm):
    query = np.asarray(query_wl_nm, dtype=float)
    return np.interp(query, wl_nm, alpha_per_um, left=0.0, right=0.0)


def available_spectra(data_dir: Path):
    """Return dict mapping (material_key,state) or filename stem info to path if present."""
    spec_dir = data_dir / "spectra"
    if not spec_dir.exists():
        return {}
    found = {}
    for p in spec_dir.glob("*.csv"):
        found[p.stem] = p
    return found


def summarize_available(data_dir: Path):
    found = available_spectra(data_dir)
    return {
        "data_dir": str(data_dir),
        "spectra_files": {k: str(v) for k, v in found.items()},
        "count": len(found),
    }
