"""Loader and helpers for measured/cited spectral data (Beer-Lambert).

If CSV spectra are provided under data/spectra/, they can be loaded and interpolated.
Otherwise, illustrative Gaussian spectra from spectral_beer_lambert are used.

Expected CSV columns (flexible): wavelength_nm and one of alpha_per_um, alpha_per_cm,
or epsilon_L_mol_cm (molar absorptivity, spectral shape). When only epsilon is provided,
concentration/path must be supplied independently to obtain absorbance/alpha via Beer-Lambert:
    A = epsilon * C * l,  alpha_cm(natural) = ln(10) * epsilon * C.
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


def load_spectrum_csv(path: Path, concentration_mol_L: float | None = None):
    """Load a spectrum CSV and return (wavelength_nm_sorted, alpha_per_um).

    If absorption is given as epsilon_L_mol_cm, concentration_mol_L (argument or row)
    is required to compute alpha_per_um. For shape-only use, call load_epsilon_spectrum_csv.
    """
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
        conc = _to_float(r, "concentration_mol_L", "concentration_M", default=concentration_mol_L)
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
        raise ValueError(f"No usable alpha spectral data in {path} (epsilon-only? provide concentration or use load_epsilon_spectrum_csv)")
    order = np.argsort(wl)
    return np.array(wl, dtype=float)[order], np.array(alpha, dtype=float)[order]


def load_epsilon_spectrum_csv(path: Path):
    """Load a spectrum CSV and return (wavelength_nm_sorted, epsilon_L_mol_cm) shape.

    Use with user-supplied concentration/path for Beer-Lambert: A = epsilon*C*l (base-10),
    alpha_cm(natural)=ln(10)*epsilon*C.
    """
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    wl, epsv = [], []
    for r in rows:
        w = _to_float(r, "wavelength_nm", "lambda_nm", "nm", "wl_nm")
        eps = _to_float(r, "epsilon_L_mol_cm", "epsilon", "molar_absorptivity")
        if w is None or eps is None:
            continue
        wl.append(w)
        epsv.append(eps)
    if not wl:
        raise ValueError(f"No usable epsilon spectral data in {path}")
    order = np.argsort(wl)
    return np.array(wl, dtype=float)[order], np.array(epsv, dtype=float)[order]


def epsilon_to_alpha_per_um(epsilon_L_mol_cm, concentration_mol_L):
    """Beer-Lambert (natural-log alpha): alpha_cm = ln(10)*epsilon*C, return 1/um."""
    eps = np.asarray(epsilon_L_mol_cm, dtype=float)
    return (math.log(10) * eps * float(concentration_mol_L)) / 1e4


def normalize_shape(values):
    """Return values normalized by max(abs(values)) for shape-only comparison."""
    v = np.asarray(values, dtype=float)
    m = np.nanmax(np.abs(v))
    if m == 0 or not np.isfinite(m):
        return v.copy()
    return v / m


def interpolate_alpha(wl_nm, alpha_per_um, query_wl_nm):
    query = np.asarray(query_wl_nm, dtype=float)
    return np.interp(query, wl_nm, alpha_per_um, left=0.0, right=0.0)


def available_spectra(data_dir: Path):
    """Return dict mapping relative stem/id to path for CSV spectra under data/spectra/ (recursive)."""
    spec_dir = data_dir / "spectra"
    if not spec_dir.exists():
        return {}
    found = {}
    for p in sorted(spec_dir.rglob("*.csv")):
        rel = p.relative_to(spec_dir).with_suffix("").as_posix()
        found[rel] = p
        # also keep plain stem for convenience if unique-ish
        found.setdefault(p.stem, p)
    return found


def summarize_available(data_dir: Path):
    found = available_spectra(data_dir)
    # de-duplicate values for reporting
    uniq = {}
    for k, v in found.items():
        uniq.setdefault(str(v), set()).add(k)
    return {
        "data_dir": str(data_dir),
        "spectra_files": {next(iter(names)): path for path, names in uniq.items()},
        "count": len(uniq),
    }
