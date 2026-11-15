# Dossier de búsqueda de datos espectroscópicos cuantitativos (para concentración, Beer-Lambert y cinética)

**Estado:** búsqueda web/NIST en vivo limitada en este entorno (p. ej. NIST WebBook suele mostrar espectros UV-Vis sin información de concentración, por lo que no siempre permite derivar `ε`). Este documento recopila **fuentes concretas, rutas de búsqueda y parámetros objetivo** para obtener datos utilizables en `data/` y en los modelos.

## 1. Hallazgos de la consulta realizada

- **NIST Chemistry WebBook (azobenceno, CAS 103-33-3, UV/Vis):** https://webbook.nist.gov/cgi/cbook.cgi?ID=C103333&Mask=400 — espectro disponible en imagen/JCAMP, pero la página indica que **no hay información de concentración** para ese espectro, por lo que no se puede derivar absortividad molar directamente desde esa entrada. Útil para forma espectral/λ, no para `ε` cuantitativo.
- **NIST (otras entradas azo/aromáticas consultadas):** patrón similar frecuente ("molar absorptivity values cannot be derived"). Conclusión: NIST es útil para identificación/forma, pero para `ε` y cuantificación suele requerirse literatura primaria o bases con calibración.
- **Búsquedas específicas (diariletenos, 6-nitroBIPS/MC, DASA, ε cuantitativo):** no retornaron resultados procesables en esta sesión; se listan abajo fuentes y estrategias directas.

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

## 6. Próximos pasos recomendados
- Acceder a los SI/PDF de los DOIs en la sección 3 y extraer tablas numéricas de `ε(λ)` o espectros digitalizables.
- Priorizar **un derivado concreto por familia** (con datos en película o matriz sólida si es posible) para cerrar un set ortogonal de 4 con números trazables.
- Una vez ingresados en `data/`, ejecutar `py -3 run_simulations.py` y recalcular con `spectral_data_loader.py` para obtener selectividad, márgenes y modelos con parámetros reales.
