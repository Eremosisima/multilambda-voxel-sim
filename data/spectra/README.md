# Spectral data (measured/cited)

Place one CSV per species/state, e.g. `M1_A.csv`, `M1_B.csv` (state/conformer A/B).

## Accepted columns (flexible names)
- `wavelength_nm` (or `lambda_nm`, `nm`, `wl_nm`)
- Absorption in one of these forms:
  - `alpha_per_um` (preferred for this repo's Beer-Lambert module)
  - `alpha_per_cm` (converted to 1/um)
  - `epsilon_L_mol_cm` (or `epsilon`) plus `concentration_mol_L` (converted via `alpha_cm = ln(10)*epsilon*C`)

Optional metadata columns: `temperature_C`, `source`, `conditions`, `notes`.

When real spectra files are added, use `spectral_data_loader.py` to load/interpolate them and replace illustrative bands in `spectral_beer_lambert.py`.
