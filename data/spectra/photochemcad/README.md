# PhotochemCAD spectral shapes (obtained)

Real absorption spectra (wavelength vs molar absorptivity ε, L·mol⁻¹·cm⁻¹) downloaded for spectral-shape use.
Concentration `C` and path length `l` are supplied independently in Beer-Lambert calculations:
`A = ε(λ)·C·l` (base-10), `α_cm(natural)=ln(10)·ε·C`.

## Files
- `azobenzene_trans_benzene_J01.csv` (+ `.meta.json`): trans-azobenzene in benzene, 280–600 nm, ε_max 22400 @ 319 nm. Source: PhotochemCAD J01.
- `merocyanine540_ethanol_K17.csv` (+ `.meta.json`): merocyanine 540 in ethanol, 220–700 nm, ε_max 138000 @ 559.5 nm. Source: PhotochemCAD K17.

## Usage (shape + user concentration)
```python
from pathlib import Path
from spectral_data_loader import load_epsilon_spectrum_csv, epsilon_to_alpha_per_um, normalize_shape

wl, eps = load_epsilon_spectrum_csv(Path("data/spectra/photochemcad/azobenzene_trans_benzene_J01.csv"))
shape = normalize_shape(eps)
alpha_per_um = epsilon_to_alpha_per_um(eps, concentration_mol_L=1e-3)  # example C
```

See `../../DATA_SEARCH_DOSSIER.md` for provenance, missing states/compounds, and integration notes.