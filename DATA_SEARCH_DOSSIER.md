# Dossier de búsqueda de datos espectroscópicos (forma espectral y cuantitativos)

**Estado:** se identificaron **formas espectrales reales (ε(λ), shape)** en PhotochemCAD para 2 especies/condiciones; **los archivos de datos de terceros no se redistribuyen en este repositorio** (para evitar conflictos de derechos/redistribución en publicaciones de dominio público/defensivas) — ver `data/spectra/photochemcad/README.md` para enlaces de procedencia y descarga externa sujeta a los términos de la fuente. Faltan estados/conformeros y compuestos clave del set objetivo. La concentración `C` (y espesor/camino `l` cuando aplique) se aporta de forma independiente y se aplica por Beer-Lambert (`A=εCl`, `α_cm=ln(10)·ε·C`). Búsqueda web/NIST en vivo limitada en este entorno.

## 0. Espectros identificados (referencia externa, no incluidos)

| Compuesto/estado | Condición | Rango λ (nm) | Pico | Fuente (procedencia/descarga) |
|---|---|---:|---:|---|
| Azobenceno, trans (predominante) | benceno, 12/11/1997 (J. Li), Cary 3, PhotochemCAD J01 | 280–600 | ε=22400 L·mol⁻¹·cm⁻¹ @ 319 nm | [página](https://photochemcad.com/databases/common-compounds/heterocycles/azobenzene), [txt](https://photochemcad.com/downloads/databases/common-compounds/J01/J01.absorption.txt) |
| Merocianina 540 | etanol, 6/13/1995 (R. W. Wagner, J. S. Lindsey), Cary 3, PhotochemCAD K17 | 220–700 | ε=138000 L·mol⁻¹·cm⁻¹ @ 559.5 nm | [página](https://photochemcad.com/databases/common-compounds/cyanine-dyes/merocyanine-540), [txt](https://photochemcad.com/downloads/databases/common-compounds/K17/K17.absorption.txt) |

- Columnas esperadas (si se descargan localmente, conforme a términos): `wavelength_nm, epsilon_L_mol_cm` (forma espectral). Uso: normalizar forma o combinar con `C`/`l` externos (`spectral_data_loader.load_epsilon_spectrum_csv`, `epsilon_to_alpha_per_um`).
- **Nota:** Merocianina 540 es referencia de forma espectral de merocianina, no necesariamente el par SP/MC (6-nitroBIPS) del set; azobenceno es estado trans, falta cis/PSS.

## 1. Hallazgos de la consulta realizada

- **NIST Chemistry WebBook (azobenceno, CAS 103-33-3, UV/Vis):** https://webbook.nist.gov/cgi/cbook.cgi?ID=C103333&Mask=400 — espectro disponible en imagen/JCAMP, pero la página indica que **no hay información de concentración** para ese espectro, por lo que no se puede derivar absortividad molar directamente desde esa entrada. Útil para forma espectral/λ, no para `ε` cuantitativo.
- **NIST (otras entradas azo/aromáticas consultadas):** patrón similar frecuente ("molar absorptivity values cannot be derived"). Conclusión: NIST es útil para identificación/forma, pero para `ε` y cuantificación suele requerirse literatura primaria o bases con calibración.
- **Búsquedas específicas (DTE abierto/cerrado, 6-nitroBIPS SP/MC, DASA coloreada/ciclada, azobenceno cis en tabla digital):** no retornaron archivos de espectro crudos/digitales procesables en esta sesión; abundan figuras/SI en PDF. Se listan abajo fuentes y estrategias directas.

## 2. Parámetros objetivo (extraer por estado/conformero y condiciones)

Para cada compuesto/material `M*` y estado/conformero `s` (A/B, y sub-isómeros si aplica, p. ej. MC transoides):

| Dato | Símbolo | Unidades | Uso |
|---|---|---|---|
| Espectro de absorción calibrado | `ε(λ)` o `α(λ)` | L·mol⁻¹·cm⁻¹ o cm⁻¹ | Beer-Lambert, selectividad, cuantificación de concentración |
| Máximos y colas | `λ_max`, forma de banda | nm | Ortogonalidad escritura/borrado/lectura |
| Concentración y camino óptico (de la medición) | `C`, `l` | mol·L⁻¹, cm/µm | Validar `A=εCl`, convertir a α en película |
| Rendimiento cuántico | `Φ_{A→B}(λ)`, `Φ_{B→A}(λ)` | — | Fotoestacionario, dosis de escritura/borrado |
| Cinética térmica | `t1/2(T)`, `k(T)`, `Ea` | s, s⁻¹, J·mol⁻¹ | Retención, modelo dependiente de T |
| Fotoestacionario (PSS) | composición A/B a λ | fracción/% | Poblaciones reales de conformeros |
| Índice/termo-óptica | `Δn(λ,c)`, `dn/dT` | RIU, K⁻¹ | Fase y deriva |
| Matriz y condiciones | solvente/polímero, T | — | Transferencia a dispositivo |

## 3. Fuentes prioritarias por compuesto (dónde buscar datos cuantitativos)

### M1 — Diariletenos (DAE/DTE)
- **Irie, M. et al.** (2000) *Chem. Rev.* 100, 1685–1716. DOI: 10.1021/cr980069d — tablas de propiedades fotocrómicas (λ_max, ε, Φ) para múltiples derivados.
- **Irie, M. et al.** (2014) *Chem. Rev.* 114, 12174–12277. DOI: 10.1021/cr500249p — revisión actualizada, fatiga y aplicaciones.
- **Datos a extraer:** `ε_open(λ_max)`, `ε_closed(λ_max)` (típicamente 10³–10⁴ L·mol⁻¹·cm⁻¹ en visible para forma cerrada según derivado), Φ de ciclación/cicloreversión, espectros completos en SI.
- **Derivados concretos a priorizar:** 1,2-bis(2,4-dimethyl-5-phenyl-3-thienyl)perfluorocyclopentene; 1,2-bis(2-methyl-5-phenyl-3-thienyl)perfluorocyclopentene (buscar por nombre + "absorption spectrum epsilon").
- **Bases:** PhotochemCAD (http://www.photochemcad.com/) — espectros y ε para cromóforos seleccionados; buscar si hay entradas de diariletenos específicos.

### M2 — Azobenceno y derivados
- **Bandara, H. M. D., & Burdette, S. C.** (2012) *Chem. Soc. Rev.* 41, 1809–1825. DOI: 10.1039/C1CS15179G — valores representativos de ε y cinética térmica por clase de azobenceno.
- **Referencia clásica:** valores a menudo reportados para trans-azobenceno (π–π*, ~320 nm, ε alto) y cis (n–π*, ~440 nm, ε menor) en etanol/hexano — **extraer valores y condiciones exactas** del artículo/tabla original (no asumir sin cita).
- **NIST:** forma espectral en https://webbook.nist.gov/cgi/cbook.cgi?ID=C103333&Mask=400 (sin concentración) — combinar con ε de literatura.
- **Datos a extraer:** `ε_trans(λ)`, `ε_cis(λ)` o espectro del PSS; Φ; `t1/2(T)` y Ea; dependencia de solvente/matriz.

### M3 — Espiropirano / Merocianina
- **Klajn, R.** (2014) *Chem. Soc. Rev.* 43, 148–184. DOI: 10.1039/C3CS60181A — compendio de propiedades SP/MC, efectos de entorno.
- **Compuesto ancla:** 6-nitroBIPS (CAS 1498-88-0) — ampliamente cuantificado; buscar "6-nitroBIPS molar extinction coefficient merocyanine 540 nm" y tablas en artículos/tesis/SI (ε de MC frecuentemente reportado en el orden de 10⁴ L·mol⁻¹·cm⁻¹, **confirmar valor y solvente exactos**).
- **Datos a extraer:** `ε_SP(λ)`, `ε_MC(λ)` (y isómeros si distinguen), cinética MC→SP `k(T)`/`t1/2(T)`, Φ, influencia de polaridad/matriz.

### M4 — DASA (Donor–Acceptor Stenhouse Adducts)
- **Helmy, S. et al.** (2014) *JACS* 136, 8169–8172. DOI: 10.1021/ja503016b — primera generación, espectros/ε y conmutación.
- **Lerch, M. M. et al.** (2018) *Chem. Soc. Rev.* 47, 1910–1937. DOI: 10.1039/C7CS00772H — revisión de generaciones, cinética y entorno.
- **Datos a extraer:** `ε_coloreado(λ_max)` (alto en visible, orden 10⁴–10⁵ en algunos reportes — **confirmar**), espectro de forma ciclada, `t1/2(T)` en matriz sólida, PSS.

### M5–M9 (alternativas)
- **Fulgidas/fulgimidas:** Yokoyama, Y. (2000) *Chem. Rev.* 100, 1717–1740. DOI: 10.1021/cr980070c; buscar ε y Φ por derivado (Aberchrome 670, etc.).
- **Dihidropirenos/naftopiranos/oxazinas:** buscar revisiones y SI por nombre de compuesto + "molar absorptivity UV-Vis".

## 4. Estrategia de búsqueda (recomendaciones prácticas)

1. **Búsqueda por identificador:** usar nombre IUPAC, CAS o SMILES/InChIKey del compuesto específico + términos: `"molar extinction coefficient"`, `"molar absorptivity"`, `"ε"`, `"UV-Vis spectrum"`, `"quantitative"`, `"concentration"`.
2. **Material suplementario (SI):** muchos artículos incluyen tablas CSV/Excel de espectros (`λ, A, ε`) — revisar SI de los DOIs listados y de citas recientes.
3. **Bases de datos:**
   - **NIST WebBook:** https://webbook.nist.gov/chemistry/ (forma espectral, fase gas/condensada; ε no siempre disponible).
   - **PhotochemCAD:** http://www.photochemcad.com/ (espectros y ε descargables para compuestos incluidos).
   - **PubChem:** https://pubchem.ncbi.nlm.nih.gov/ (enlaces a espectros/literatura por compuesto).
   - **SpectraBase / repositorios institucionales:** cuando estén disponibles.
4. **Tesis y reportes:** búsquedas en repositorios universitarios con "UV-Vis characterization of [compound]" suelen contener espectros calibrados y concentraciones.
5. **Cálculo inverso cuando falte ε:** si se reporta absorbancia `A`, concentración `C` y camino `l`, calcular `ε = A/(C·l)`; si se reporta en película, registrar `α`/espesor y condiciones.

## 5. Plantilla para consolidar datos encontrados

Crear/llenar `data/extracted_spectra_values.csv` con filas por medición:

```csv
material,compound_name,state_conformer,lambda_nm,epsilon_L_mol_cm,alpha_per_cm,absorbance,concentration_mol_L,path_cm,temperature_C,matrix,phi,source_doi,source_note
M1,"1,2-bis(... )perfluorocyclopentene",closed,520,,,,,,25,"hexane",,"10.1021/cr500249p","tabla/fig X"
M2,"azobenzene",trans,316,,,,,,25,"ethanol",,"10.1039/C1CS15179G","valor representativo"
M3,"6-nitroBIPS",MC,540,,,,,,25,"toluene",,"10.1039/C3CS60181A","confirmar"
M4,"DASA gen1 ...",colored,,,,,,,25,"toluene",,"10.1021/ja503016b",""
```

Y espectros completos en `data/spectra/<material>_<state>.csv` (ver `data/spectra/README.md`, `DATA_ACQUISITION_PLAN.md`).

## 6. Faltantes para el set objetivo (obtener forma espectral por estado)

| Material objetivo | Estados necesarios | Estado actual | Fuentes prioritarias a extraer/digitalizar |
|---|---|---|---|
| M1 DTE/DAE | abierto y cerrado (mismo derivado) | **Faltan ambos** | Irie 2000/2014 (SI/tablas ε(λ), Φ); buscar derivado concreto en PhotochemCAD o digitalizar figuras |
| M2 Azobenceno | trans y cis (o PSS) en condiciones comparables | **trans obtenido** (J01, benceno); falta cis/PSS | Bandara & Burdette 2012 (espectros/citas de ε); Vetráková 2017 (cis puro, metodología) |
| M3 6-nitroBIPS SP/MC | SP y MC (+isómeros si aplica) | **Merocianina 540 como referencia de forma**; faltan SP/MC del mismo par | Klajn 2014; SI de estudios cuantitativos 6-nitroBIPS (ε(λ), C,l o tablas) |
| M4 DASA | coloreada y ciclada | **Faltan ambos** | Helmy 2014, Lerch 2018 (espectros en SI/figuras; digitalizar) |

## 7. Integración en el modelo (shape + concentración independiente)
- Guardar por especie: `data/spectra/<material>_<estado>.csv` con `wavelength_nm,epsilon_L_mol_cm` (o `alpha_*`).
- Cargar forma: `load_epsilon_spectrum_csv`; aplicar `C` (y `l`) del usuario: `alpha_per_um = epsilon_to_alpha_per_um(eps, C_mol_L)` → usar en `spectral_beer_lambert`/mezclas.
- Para activar espectros reales en `spectral_beer_lambert.build_spectral_library`, proveer `M1_A.csv..M4_B.csv` con `concentration_mol_L` (en archivo o argumento) y datos utilizables como α.
- `spectral_data_loader.summarize_available` ya detecta recursivamente espectros en `data/spectra/` (incluye los obtenidos en `photochemcad/`).

## 8. Próximos pasos recomendados
- Digitalizar/extractar SI de los DOIs sección 3 para completar pares A/B (prioridad: un derivado concreto por familia en matriz sólida si existe).
- Cuando estén los 4 pares, regenerar: selectividad/crosstalk Beer-Lambert, matriz `A` efectiva, y análisis no lineal/térmico con parámetros trazables (`run_simulations.py` + módulos espectrales).
