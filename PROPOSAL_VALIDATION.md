# Validación de la propuesta y evidencia de literatura (apoyo/refutación)

> **Alcance:** evaluación técnica de la estrategia propuesta a partir de los modelos/simulaciones de este repositorio y de literatura científica establecida. No es una prueba experimental ni una garantía de viabilidad de dispositivo. Las referencias citadas son ampliamente conocidas; **verificar DOI, cifras y condiciones en las fuentes originales** antes de usarlas en manuscritos.

## 1. Resumen de la propuesta evaluada

Estrategia: memoria óptica multinivel en un voxel mediante **multiplexado por longitud de onda** de 4 fotoswitches (tratando estados/conformeros como especies con espectros distintos), modelo de índice efectivo `Δn_i = c_i·Δn_{i,max}` y `y = A c + e` con lectura interferométrica por fase e inversión de matriz, escalable en niveles/bits, con análisis de crosstalk, temperatura/no linealidad y publicación abierta/defensiva.

## 2. Validación técnica con los resultados del repositorio

| Elemento de la propuesta | Qué muestran los modelos/simulaciones | Estado (bajo supuestos) | Riesgos / condiciones |
|---|---|---|---|
| Superposición lineal `Δn_total = Σ c_i Δn_{i,max}` | Consistente matemáticamente; matriz `A` bien condicionada en escenario base (`cond≈1.196`), 256/256 estados decodificables sin ruido. | **Válido como primera aproximación** | Requiere régimen sin saturación y con respuesta estable; Δn real depende de λ, matriz y grado de conversión. |
| Lectura por fase e inversión `c = A^{-1}y` | Pasos de fase ~2.6–3.0 rad/nivel (caso base) dan márgenes amplios; MC con incertidumbre mantiene exactitud alta en ese régimen. | **Válido si se logran Δn·L·Γ y calibración** | Sensible a caída de Δn/L/Γ, ruido real (RIN/NEP/visibilidad), deriva y error de calibración; la calibración experimental de `A` es clave. |
| Ortogonalidad espectral / baja diafonía (Beer-Lambert en mezcla) | Modelo espectral con 2 estados/conformeros por material: selectividad media de escritura ~0.792 y absorción parásita/lectura no nula (ej. máx. ~7.8e-2 en casos evaluados, ilustrativo). | **Parcial / condicionado** | La ortogonalidad real depende de `ε_{i,s}(λ,T)` medidos, colas de absorción, concentraciones y rendimientos cuánticos; sin datos reales no se garantiza baja diafonía. |
| Multinivel (4 niveles, 8 bits/voxel) y escalado | Escalado de niveles muestra caída de margen (grado 4→8→16 reduce margen de medio paso y exige menor σ; p. ej. σ_3σ ~0.467, 0.200, 0.093 rad). | **Factible en principio, exigente al escalar** | Más niveles incrementan requisitos de SNR, linealidad y control térmico. |
| No linealidad de respuesta | Ajustes y comparación: respuesta saturante + decodificador lineal degrada severamente (exactitud ~0.058 en prueba), recuperable con inversa/calibración no lineal; ajuste polinómico con T sugiere grado ~4 (BIC/RMSE) y coeficientes dependientes de T. | **El lineal puro no basta en general** | Es necesaria caracterización `Δn_eff(c,λ,T,historial)` y calibración (LUT/inversa). |
| Influencia de temperatura | Deriva termo-óptica (modelo) consume margen de fase; cinética tipo Arrhenius muestra caída fuerte de retención con T (ej. factores ×8.14 a +20 K, ×51.5 a +40 K, ×264 a +60 K, ilustrativo). | **Debe incluirse** | `dn/dT`, Ea y tasas reales son específicos de material/matriz; requiere gestión/compensación térmica y calibración en T. |
| Crosstalk térmico/óptico y escalado en arreglo | Separación térmica ≥~4.11 µm (modelo 1D); crosstalk agregado en arreglo crece con vecinos (margen proxy decrece). | **Cualitativamente razonable** | Modelos de primer orden; falta validación EM/térmica 3D y efectos de layout real. |
| Estimación por primeros principios (PIB 1D/2D) | Capta tendencia cualitativa: mayor conjugación → λ mayor entre conformeros. | **Apoyo cualitativo** | No cuantitativo para `ε(λ)`/Δn; requiere estructura real o TD-DFT/espectros medidos. |
| Afirmaciones de energía/CO₂ | Cálculos aritméticos consistentes como **escenarios** (mismo trabajo útil, eficiencia relativa). | **Válido como escenario** | No es desempeño medido; depende de eficiencia de sistema, PUE, utilización y mix. |

**Conclusión de validación (modelo):** la propuesta es **conceptualmente coherente y matemáticamente demostrable en un régimen idealizado**, pero su viabilidad práctica depende críticamente de (i) ortogonalidad espectral real y baja absorción parásita, (ii) `Δn` alcanzable y estable, (iii) linealidad/calibración efectiva, y (iv) control de temperatura y ruido. Sin caracterización experimental, no debe afirmarse como desempeño logrado.

## 3. Referencias: apoyo y refutación por elemento de la estrategia

> Verificar detalles en las fuentes originales. Lista orientativa (ver también `REFERENCES_AND_BIBLIOGRAPHY.md`).

### 3.1 Memoria fotónica multinivel y lectura óptica (apoyo conceptual, mecanismo distinto)
- **Ríos, C. et al. (2015).** *Integrated all-photonic non-volatile multi-level memory.* Nature Photonics, 9, 725–732. DOI: 10.1038/nphoton.2015.182  
  - **Apoya:** viabilidad de memoria fotónica integrada, multinivel y no volátil con lectura óptica.  
  - **Matiza/Refuta (parcial):** usa cambio de fase (GST) con respuesta fuertemente no lineal y dependiente de historia térmica; no valida linealidad en fotoswitches ni ortogonalidad por multiplexado espectral de moléculas.
- **Feldmann, J. et al. (2019).** *All-optical spiking neurosynaptic networks...* Nature, 569, 208–214. DOI: 10.1038/s41586-019-1157-8  
  - **Apoya:** interés en pesos/estados ópticos integrados.  
  - **Matiza:** variabilidad, control y acumulación exigen calibración y gestión térmica.
- **Wuttig, M., Bhaskaran, H., & Taubner, T. (2017).** *Phase-change materials for non-volatile photonic applications.* Nature Photonics, 11, 465–476. DOI: 10.1038/nphoton.2017.126  
  - **Apoya:** modulación óptica no volátil.  
  - **Matiza:** respuestas grandes suelen ser no lineales y sensibles a temperatura/historial.

### 3.2 Materiales fotoswitch (Δn, espectros, conformeros/estados)
- **Irie, M. et al. (2014).** *Photochromism of diarylethene molecules and crystals...* Chemical Reviews, 114(24), 12174–12277. DOI: 10.1021/cr500249p (y Irie 2000, DOI: 10.1021/cr980069d)  
  - **Apoya:** diariletenos con alta estabilidad térmica (en muchas formas cerradas), fatiga variable pero mejorable, y cambios de propiedades ópticas útiles para memoria/conmutación; justifica tratar estados como especies espectrales distintas.  
  - **Matiza/Refuta:** Δn y linealidad dependen de derivado/matriz/λ; saturación y fatiga pueden limitar multinivel ideal.
- **Bandara, H. M. D., & Burdette, S. C. (2012).** *Photoisomerization in different classes of azobenzene.* Chemical Society Reviews, 41, 1809–1825. DOI: 10.1039/C1CS15179G  
  - **Apoya:** fotoisomerización y cambios espectrales (trans/cis) como base de modulación.  
  - **Refuta/Desafía:** relajación térmica cis→trans significativa y dependiente de T/sustituyentes/matriz → amenaza retención "sin energía" y estabilidad multinivel si no se controla.
- **Klajn, R. (2014).** *Spiropyran-based dynamic materials.* Chemical Society Reviews, 43, 148–184. DOI: 10.1039/C3CS60181A  
  - **Apoya:** grandes cambios SP↔MC (especies con espectros muy distintos), útil para contraste.  
  - **Refuta/Desafía:** estabilidad, fatiga y fuerte dependencia del entorno/cinética térmica complican operación estable y lineal.
- **Helmy, S. et al. (2014).** *Photoswitching using visible light: a new class of organic photochromic molecules.* JACS, 136(23), 8169–8172. DOI: 10.1021/ja503016b; **Lerch, M. M. et al. (2018).** *The (photo)chemistry of Stenhouse photoswitches...* Chem. Soc. Rev., 47, 1910–1937. DOI: 10.1039/C7CS00772H  
  - **Apoya:** activación en visible y diversidad espectral (potencial ortogonalidad).  
  - **Refuta/Desafía:** reversión térmica y sensibilidad a entorno/T; requiere caracterización específica para memoria.

### 3.3 Temperatura, termo-óptica y estabilidad
- **Arbabi, A., & Goddard, L. L. (2013).** *Measurements of the refractive indices and thermo-optic coefficients of Si3N4 and SiOx...* Optics Letters, 38(19), 3878–3881. DOI: 10.1364/OL.38.003878  
  - **Apoya:** necesidad de incluir `dn/dT` (orden ~10⁻⁵ K⁻¹ típico en plataformas integradas) en lectura de fase.  
  - **Matiza:** el valor efectivo depende del stack/modo completo.
- **Bogaerts, W., & Chrostowski, L. (2018).** *Silicon photonics circuit design...* Laser & Photonics Reviews, 12(4), 1700237. DOI: 10.1002/lpor.201700237  
  - **Apoya:** sensibilidad térmica inherente en fotónica integrada y necesidad de control/compensación.  
  - **Matiza:** implica compromisos de potencia y complejidad a nivel sistema.

### 3.4 No linealidad y calibración multinivel
- **Ríos et al. (2015)** y práctica en almacenamiento multinivel (p. ej. esquemas de niveles discretos con calibración en medios ópticos/PCM, y antecedentes como Parthenopoulos & Rentzepis, 1989, Science 245:843, DOI: 10.1126/science.245.4920.843)  
  - **Apoya:** viabilidad de multinivel con márgenes definidos.  
  - **Refuta/Desafía:** la linealidad ideal rara vez se cumple; se requieren curvas de calibración, control de dosis/historial y gestión de deriva.

## 4. Veredicto estratégico (síntesis)

- **Fortalezas de la estrategia:** marco matemático claro (superposición + inversión de matriz), descomposición por especies/conformeros compatible con Beer-Lambert, y alineación conceptual con evidencia de memoria fotónica multinivel.
- **Debilidades/condicionantes principales:** (1) ortogonalidad espectral real no demostrada con datos medidos; (2) no linealidad/saturación/fatiga probables; (3) retención y fase dependientes de temperatura; (4) desempeño energético solo a nivel de escenario.
- **Estrategia científicamente defendible si:** se presenta como modelo/simulación con supuestos explícitos, se incorporan `ε(λ,T)`, `Φ`, `t1/2/Ea`, `Δn(λ,T)` y `dn/dT` medidos/citados, se adopta decodificación/calibración no lineal dependiente de T, y se validan márgenes con caracterización experimental.
- **Estrategia refutable en su forma fuerte (hoy):** afirmar alta densidad/eficiencia/retención sin pérdidas de forma práctica sin evidencia de ortogonalidad, linealidad efectiva y estabilidad térmica en el sistema integrado.

## 5. Recomendaciones inmediatas
1. Parametrizar con datos medidos/citados (`data/` + `spectral_data_loader.py`) y recalcular selectividad Beer-Lambert y `A`.
2. Usar modelos de decodificación calibrados/no lineales y dependientes de T (extender ajustes polinómicos a datos reales).
3. Incluir presupuesto completo de ruido/pérdidas y, si es posible, validación EM/térmica.
4. En publicaciones, separar claramente **resultado simulado** de **hipótesis pendiente de verificación** y citar las referencias anteriores según apoyo/refutación.
