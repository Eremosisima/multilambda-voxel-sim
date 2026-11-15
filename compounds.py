"""Compound set and physical parameters for wavelength-multiplexed photonic memory simulations.

Values are literature-inspired/plausible estimates for simulation of Article 1.
They should be replaced with measured or cited values in the manuscript.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Compound:
    key: str
    name: str
    write_nm: float
    erase_nm: float
    read_nm: float
    delta_n_max: float  # refractive-index change at read wavelength, fully switched state
    thermal_half_life_s: float
    notes: str


# 4 orthogonal photoswitches (example set). Read wavelengths chosen in telecom/NIR windows
# to minimize absorption-induced erasure; write/erase bands separated to reduce crosstalk.
COMPOUNDS = [
    Compound(
        key="M1",
        name="Diarylethene (DTE)",
        write_nm=313.0,
        erase_nm=530.0,
        read_nm=1550.0,
        delta_n_max=0.060,  # Irie-class diarylethenes: large, thermally stable index change
        thermal_half_life_s=1e7,  # effectively bistable
        notes="P-type photochromic; high thermal stability.",
    ),
    Compound(
        key="M2",
        name="Azobenzene derivative",
        write_nm=365.0,
        erase_nm=450.0,
        read_nm=1310.0,
        delta_n_max=-0.050,  # trans->cis index decrease in polymer host (order-of-magnitude)
        thermal_half_life_s=1e5,
        notes="T-type component; thermal back-relaxation non-negligible.",
    ),
    Compound(
        key="M3",
        name="Spiropyran / Merocyanine",
        write_nm=405.0,
        erase_nm=590.0,
        read_nm=980.0,
        delta_n_max=0.040,
        thermal_half_life_s=5e4,
        notes="Large polarity/photochromic change; read placed away from visible bands.",
    ),
    Compound(
        key="M4",
        name="DASA photoswitch",
        write_nm=660.0,
        erase_nm=700.0,  # often thermal; modeled here as long-wavelength/thermal erase channel
        read_nm=850.0,
        delta_n_max=-0.030,
        thermal_half_life_s=2e4,
        notes="Negative photochromism in many hosts; thermal recovery channel.",
    ),
]

LEVELS_PER_MATERIAL = 4  # 2 bits each -> 8 bits/voxel with 4 materials
BITS_PER_VOXEL = len(COMPOUNDS) * int(np.log2(LEVELS_PER_MATERIAL))


def level_fractions(levels: int = LEVELS_PER_MATERIAL) -> np.ndarray:
    """Discrete fractional states c_i in [0,1] for each material."""
    return np.linspace(0.0, 1.0, levels)


def compound_table_rows():
    rows = []
    for c in COMPOUNDS:
        rows.append(
            {
                "key": c.key,
                "compound": c.name,
                "lambda_write_nm": c.write_nm,
                "lambda_erase_nm": c.erase_nm,
                "lambda_read_nm": c.read_nm,
                "delta_n_max": c.delta_n_max,
                "thermal_half_life_s": c.thermal_half_life_s,
                "notes": c.notes,
            }
        )
    return rows
