# PhotochemCAD spectral shapes (external reference — not redistributed)

This directory **does not include third-party spectral data files** to avoid copyright/redistribution conflicts in public-domain/defensive publications of this project.

Real absorption spectra (wavelength vs molar absorptivity ε, L·mol⁻¹·cm⁻¹) were identified for spectral-shape use. Concentration `C` and path length `l` are supplied independently in Beer-Lambert calculations: `A = ε(λ)·C·l` (base-10), `α_cm(natural)=ln(10)·ε·C`.

## Referenced sources (provenance)
- **Azobenzene (trans, predominant), benzene**, 280–600 nm, ε_max 22400 @ 319 nm. PhotochemCAD J01 (Junzhong Li, 1997, Cary 3).  
  Page: https://photochemcad.com/databases/common-compounds/heterocycles/azobenzene  
  Data: https://photochemcad.com/downloads/databases/common-compounds/J01/J01.absorption.txt
- **Merocyanine 540, ethanol**, 220–700 nm, ε_max 138000 @ 559.5 nm. PhotochemCAD K17 (R. W. Wagner and J. S. Lindsey, 1995, Cary 3).  
  Page: https://photochemcad.com/databases/common-compounds/cyanine-dyes/merocyanine-540  
  Data: https://photochemcad.com/downloads/databases/common-compounds/K17/K17.absorption.txt

## How to use locally (without redistributing)
1. Download the upstream files from the links above **subject to PhotochemCAD's terms/permissions**.
2. Convert to CSV columns `wavelength_nm,epsilon_L_mol_cm` (e.g. `azobenzene_trans_benzene_J01.csv`) and place locally if your use/terms allow.
3. Load with the project helper:

```python
from pathlib import Path
from spectral_data_loader import load_epsilon_spectrum_csv, epsilon_to_alpha_per_um, normalize_shape

wl, eps = load_epsilon_spectrum_csv(Path("data/spectra/photochemcad/azobenzene_trans_benzene_J01.csv"))
shape = normalize_shape(eps)
alpha_per_um = epsilon_to_alpha_per_um(eps, concentration_mol_L=1e-3)  # example C
```

See `../../DATA_SEARCH_DOSSIER.md` for provenance, missing states/compounds, and integration notes. **Do not commit upstream data files unless redistribution rights are clearly compatible.**
