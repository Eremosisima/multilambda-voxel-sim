# Plan de adquisición de datos para robustecer el modelo (Beer-Lambert, no linealidad, temperatura)

Objetivo: reemplazar supuestos ilustrativos por **valores medidos o citados** (con fuente, condiciones y unidades) para espectros `ε(λ,T)`, cinética, `Δn` y parámetros térmicos.

## 1. Datos mínimos por material y por estado/conformero

Para cada material `i` (M1–M4) y cada estado/conformero estable `s` (p. ej. A = abierto/trans/spiro/incoloro; B = cerrado/cis/mero/coloreado — según familia), recolectar:

| Parámetro | Símbolo / forma | Unidades sugeridas | Uso en el modelo | Notas |
|---|---|---|---|---|
| Espectro de absorción | `ε_{i,s}(λ)` o `α_{i,s}(λ)` | L·mol⁻¹·cm⁻¹ o cm⁻¹ (indicar) | Beer-Lambert `A(λ)=l Σ εC`, selectividad/crosstalk | Ideal: tabla λ–ε (nm, valor) por estado; incluir T |
| Longitudes de máximo | `λ_max,abs` | nm | Definir bandas de escritura/borrado/lectura | Reportar hombros/colas (importa para solapamiento) |
| Rendimiento cuántico | `Φ_{A→B}(λ)`, `Φ_{B→A}(λ)` | adimensional | Tasas de fotoconversión y fotoestacionario | Dependiente de λ y entorno |
| Cinética térmica | `k(T)` o `t1/2(T)` | s⁻¹ o s | Retención/estabilidad | Medir a varias T |
| Energía de activación | `Ea` (si aplica Arrhenius) | J·mol⁻¹ o eV | `k(T)=A·exp(-Ea/RT)` | Especificar rango de validez |
| Cambio de índice | `Δn_{i}(λ, estado o c)` | RIU | Fase `Δφ=(2π/λ)ΓΔnL`, matriz `A` | Indicar λ de lectura y grado de conversión |
| Coef. termo-óptico | `dn/dT` (material/stack) | K⁻¹ | Deriva de fase con T | Depende de guía/matriz efectiva |
| Concentración / densidad | `C` o fracción másica/vol | mol·L⁻¹, %wt, etc. | Conversión ε↔α y mezcla | Incluir espesor de película `l` |
| Espesor / camino óptico | `l`, `L`, `Γ` | µm, adimensional | Beer-Lambert y fase | `Γ` confinamiento modal efectivo |
| Condiciones | solvente/matriz, T, atmósfera | — | Comparabilidad | Crítico para cinética y espectros |

## 2. Fuentes recomendadas (por familia) y qué extraer

> Verificar DOI/condiciones en la fuente original. Priorizar datos en **matriz sólida/película** si el dispositivo es en estado sólido.

| Familia (candidato) | Fuentes de partida sugeridas | Extraer |
|---|---|---|
| **Diariletenos (DTE, M1)** | Irie et al., *Chem. Rev.* 2014 (10.1021/cr500249p) y 2000 (10.1021/cr980069d); tablas de ε, Φ, fatiga en derivados específicos | `ε_open/closed(λ)`, Φ_cyc/Φ_rev, estabilidad térmica (usualmente muy alta en cerrados), ejemplos de modulación de n |
| **Azobencenos (M2)** | Bandara & Burdette, *Chem. Soc. Rev.* 2012 (10.1039/C1CS15179G); datos de derivados y polímeros azo | `ε_trans/cis(λ)` (π–π*, n–π*), Φ, `t1/2(T)` y Ea de relajación térmica, Δn en películas |
| **Espiropirano/Merocianina (M3)** | Klajn, *Chem. Soc. Rev.* 2014 (10.1039/C3CS60181A); estudios en PMMA/películas | `ε_SP/MC(λ)`, cinética térmica MC→SP vs T, efectos de matriz/polaridad |
| **DASA (M4)** | Helmy et al., *J. Am. Chem. Soc.* 2014 (10.1021/ja503016b); Lerch et al., *Chem. Soc. Rev.* 2018 (10.1039/C7CS00772H) | `ε(λ)` abierto/coloreado-cerrado, `t1/2(T)`, dependencia fuerte de entorno/temperatura |
| **Termo-óptica / fotónica** | Arbabi & Goddard, *Opt. Lett.* 2013 (10.1364/OL.38.003878) para SiN/SiOx; Bogaerts & Chrostowski, 2018 (10.1002/lpor.201700237) | `dn/dT` del stack, sensibilidad térmica de MZI/guías |
| **Contexto multinivel/fotónica** | Ríos et al., *Nature Photonics* 2015 (10.1038/nphoton.2015.182) | Niveles, márgenes, calibración/no linealidad (mecanismo distinto pero útil) |

**Bases/recursos complementarios:** Photochromism Database (bases académicas), datos suplementarios de artículos (CSV/espectros), repositorios de autores, PhotochemCAD (cuando aplique), NIST Chemistry WebBook (propiedades generales; espectros específicos según disponibilidad).

## 3. Formato recomendado para ingresar datos al repositorio

### 3.1 Espectros (un archivo por especie o tabla larga)
Archivo sugerido: `data/spectra/<material>_<state>.csv`
```csv
wavelength_nm,epsilon_L_mol_cm,alpha_per_cm,temperature_C,source,notes
300,12000,,25,"Autor et al. 20XX DOI:...","matriz PMMA"
...
```
- Usar `epsilon_L_mol_cm` o `alpha_per_cm` (indicar cuál); incluir concentración/espesor si se reporta α efectivo.

### 3.2 Parámetros de cinética y fotoquímica
Archivo sugerido: `data/kinetics.csv`
```csv
material,state_from,state_to,parameter,value,units,temperature_C,wavelength_nm,source,conditions
M1,A,B,phi,0.5,,25,313,"DOI:...","película"
M2,B,A,t_half,3600,s,25,,"DOI:...","..."
M2,B,A,Ea,95000,J/mol,,,"DOI:...","ajuste Arrhenius 20-60C"
```

### 3.3 Índice y termo-óptica
Archivo sugerido: `data/refractive_index.csv`
```csv
material,state_or_c,wavelength_nm,delta_n,dn_dT_per_K,confinement_gamma,source,conditions
M1,B,1550,0.04,,0.35,"DOI:...","..."
stack,effective,1550,,1.0e-5,,"DOI:...","SiN+polímero"
```

## 4. Integración en el código (cuando haya datos)

- `spectral_beer_lambert.py`: reemplazar `build_spectral_library()`/bandas gaussianas por un cargador que lea `data/spectra/*.csv` (interpolación a la malla de λ) y construya `α_{i,s}(λ,T)`.
- `compounds.py`: actualizar `delta_n_max`, λ y notas con valores citados.
- `polynomial_temperature_fit.py` / `nonlinear_temperature_analysis.py`: ajustar modelos con curvas medidas `(c,T)->Δn` o `(c,T)->φ`.
- Registrar siempre: **fuente (DOI), condiciones (matriz, T, λ), incertidumbre/rango**.

## 5. Criterios de aceptación de datos
- Trazables a una fuente primaria o dataset publicado.
- Unidades y condiciones explícitas.
- Para mezcla: compatibilidad de solvente/matriz y ausencia (o cuantificación) de interacciones que alteren espectros/cinética.
- Distinguir datos en solución vs película sólida (preferir los representativos del dispositivo).

## 6. Estado actual
- El repositorio usa **espectros y parámetros ilustrativos** para demostrar el método (ver `outputs/beer_lambert_summary.json`, `REFERENCES_AND_BIBLIOGRAPHY.md`). Este plan define el camino para sustituirlos por datos reales y recalcular selectividad, márgenes y modelos no lineales/ térmicos.
