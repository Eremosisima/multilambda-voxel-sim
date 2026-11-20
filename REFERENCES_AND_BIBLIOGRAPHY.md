# Referencias bibliográficas sugeridas (para confirmar/refutar supuestos del modelo)

> **Nota:** Esta lista se compiló como guía técnica a partir de literatura ampliamente conocida en el área (la búsqueda web en vivo no estuvo disponible en esta sesión). **Verifica metadatos, DOI, cifras y conclusiones en las fuentes originales** antes de citarlas en un manuscrito. Se indica cómo cada referencia se relaciona con los supuestos del proyecto (soporte, matiz o posible refutación).

## 1. Conmutadores moleculares y Δn / almacenamiento óptico multinivel

| Referencia | Por qué es relevante | Qué puede apoyar | Qué puede matizar/refutar |
|---|---|---|---|
| Irie, M., Fukaminato, T., Matsuda, K., & Kobatake, S. (2014). Photochromism of diarylethene molecules and crystals: memories, switches, and actuators. *Chemical Reviews*, 114(24), 12174–12277. DOI: 10.1021/cr500249p | Revisión fundamental de diariletenos (estabilidad térmica de estados, fatiga, respuesta fotoquímica). | Viabilidad de conmutación estable y potencial de estados distinguibles; base para asumir Δn apreciable en algunas familias. | No garantiza linealidad de Δn vs dosis/estado ni ausencia de saturación/fatiga; valores de Δn dependen fuertemente de derivado/matriz/λ. |
| Irie, M. (2000). Diarylethenes for memories and switches. *Chemical Reviews*, 100(5), 1685–1716. DOI: 10.1021/cr980069d | Fundamentos tempranos y aplicaciones en memoria. | Motiva uso de diariletenos en memoria óptica. | Condiciones de película/dispositivo reales pueden diferir de ejemplos moleculares/cristalinos. |
| Bandara, H. M. D., & Burdette, S. C. (2012). Photoisomerization in different classes of azobenzene. *Chemical Society Reviews*, 41(5), 1809–1825. DOI: 10.1039/C1CS15179G | Fotoisomerización y relajación térmica de azobencenos. | Apoya posibilidad de modulación óptica/índice inducida por fotoisomerización. | **Desafía** estabilidad a largo plazo sin aporte de energía: la relajación térmica cis→trans es sensible a temperatura/sustituyentes/matriz; linealidad y retención deben demostrarse. |
| Klajn, R. (2014). Spiropyran-based dynamic materials. *Chemical Society Reviews*, 43(1), 148–184. DOI: 10.1039/C3CS60181A | Espiropiranos/merocianinas: conmutación, entorno, estabilidad. | Apoya grandes cambios de propiedades (potencial Δn) y respuesta sintonizable. | **Desafía** estabilidad térmica, fatiga y reproducibilidad; la cinética y el estado dependen del entorno (polaridad, matriz), afectando linealidad y retención. |
| Helmy, S., Leibfarth, F. A., Oh, S., Poelma, J. E., Hawker, C. J., & Read de Alaniz, J. (2014). Photoswitching using visible light: a new class of organic photochromic molecules. *Journal of the American Chemical Society*, 136(23), 8169–8172. DOI: 10.1021/ja503016b | Introducción de DASA (conmutación con luz visible). | Apoya diversidad espectral/ortogonalidad potencial (activación en visible). | **Desafía** reversión térmica y estabilidad según derivados/condiciones; requiere caracterización de Δn y cinética para memoria multinivel. |
| Lerch, M. M., Szymański, W., & Feringa, B. L. (2018). The (photo)chemistry of Stenhouse photoswitches: guiding principles and system design. *Chemical Society Reviews*, 47(6), 1910–1937. DOI: 10.1039/C7CS00772H | Mecanismos y diseño de DASA/Stenhouse. | Guía para ajustar cinética/absorción (útil para ortogonalidad y temperatura). | Subraya sensibilidad a entorno/temperatura/solvente, reforzando necesidad de modelo dependiente de condiciones. |

## 2. Memoria óptica/fotónica multinivel y lectura por fase (contexto de arquitectura)

| Referencia | Por qué es relevante | Qué puede apoyar | Qué puede matizar/refutar |
|---|---|---|---|
| Ríos, C., Stegmaier, M., Hosseini, P., Wang, D., Scherer, T., Wright, C. D., Bhaskaran, H., & Pernice, W. H. P. (2015). Integrated all-photonic non-volatile multi-level memory. *Nature Photonics*, 9, 725–732. DOI: 10.1038/nphoton.2015.182 | Memoria fotónica integrada multinivel no volátil (PCM) con lectura óptica. | **Apoya** la viabilidad conceptual de memoria fotónica multinivel y lectura óptica en guías; referencia clave de estado del arte. | Mecanismo distinto (cambio de fase GST, respuesta no lineal/cristalización) — no valida directamente Δn lineal en fotoswitches; sugiere que la no linealidad y calibración son comunes. |
| Feldmann, J., Youngblood, N., Wright, C. D., Bhaskaran, H., & Pernice, W. H. P. (2019). All-optical spiking neurosynaptic networks with self-learning capabilities. *Nature*, 569, 208–214. DOI: 10.1038/s41586-019-1157-8 | Pesos ópticos/sinápticos integrados (contexto fotónico). | Apoya interés en pesos/estados ópticos y co-integración. | Enfatiza retos de control, variabilidad y acumulación — coherente con necesidad de calibración y control térmico. |
| Wuttig, M., Bhaskaran, H., & Taubner, T. (2017). Phase-change materials for non-volatile photonic applications. *Nature Photonics*, 11, 465–476. DOI: 10.1038/nphoton.2017.126 | Materiales de cambio de fase para fotónica. | Contexto de modulación de índice/absorción grande y no volátil. | Refuerza que respuestas fuertes suelen ser no lineales y dependientes de historial/temperatura. |

## 3. Temperatura: termo-óptica, deriva de fase y estabilidad térmica

| Referencia | Por qué es relevante | Qué puede apoyar | Qué puede matizar/refutar |
|---|---|---|---|
| Bogaerts, W., & Chrostowski, L. (2018). Silicon photonics circuit design: methods, tools and challenges. *Laser & Photonics Reviews*, 12(4), 1700237. DOI: 10.1002/lpor.201700237 (y literatura asociada de fotónica integrada) | Sensibilidad térmica en circuitos fotónicos (derivas, necesidad de control). | **Apoya** que la temperatura debe considerarse en lectura de fase/interferómetros. | Magnitudes de dn/dT y estrategias dependen de plataforma (Si, SiN, polímero); el valor usado en el modelo es ilustrativo. |
| Arbabi, A., & Goddard, L. L. (2013). Measurements of the refractive indices and thermo-optic coefficients of Si3N4 and SiOx using microring resonances. *Optics Letters*, 38(19), 3878–3881. DOI: 10.1364/OL.38.003878 | Medición de dn/dT en SiN/SiOx (orden ~10⁻⁵ K⁻¹ típico en SiN, según condiciones). | Permite anclar órdenes de magnitud para deriva termo-óptica en guías. | **Matiza** el parámetro: dn/dT efectivo del stack fotosensible + guía puede diferir del SiN puro. |
| Dong, P., et al. (índices de trabajos sobre control térmico en MZI/microrings, p. ej. IEEE J. Sel. Top. Quantum Electron., varios años) | Control y compensación térmica en interferómetros integrados. | Apoya necesidad de estabilización/compensación de fase. | Implica costo de potencia/complejidad que debe incluirse en modelos de sistema. |
| Eyring/Arrhenius aplicado a fotoquímicos (p. ej. discusiones en Bandara & Burdette 2012; Klajn 2014; y estudios cinéticos específicos de cada familia) | Dependencia de tasas de retorno térmico con T. | **Apoya** modelar retención con cinética dependiente de temperatura (Arrhenius como primera aproximación). | **Desafía** el uso de una Ea única: Ea/tasas son específicas de molécula, matriz y mecanismo; pueden no ser Arrhenius simples en todo rango. |

## 4. No linealidad, saturación y calibración multinivel

| Referencia | Por qué es relevante | Qué puede apoyar | Qué puede matizar/refutar |
|---|---|---|---|
| Parthenopoulos, D. A., & Rentzepis, P. M. (1989). Three-dimensional optical storage memory. *Science*, 245(4920), 843–845. DOI: 10.1126/science.245.4920.843 (y trabajos posteriores de almacenamiento multinivel fotoquímico) | Antecedentes de almacenamiento óptico multinivel en medios fotoactivos. | Apoya la idea de múltiples niveles distinguibles. | Históricamente muestra sensibilidad a dosis, saturación y estabilidad, implicando calibración. |
| Literatura de grabación multinivel en medios ópticos/fotocromos y en PCM (p. ej. esquemas de niveles en Ríos 2015 y trabajos de multilevel cell en almacenamiento) | Práctica de niveles discretos con márgenes. | Apoya discretización y necesidad de márgenes de SNR. | **Desafía** asumir respuesta lineal: la relación escritura→estado→lectura suele requerir curvas de calibración/LUT y control de deriva. |

## 5. Cómo usar estas referencias en el proyecto (guía rápida)

- **Para apoyar:** viabilidad de conmutación fotoquímica y de memoria fotónica multinivel (Irie, Ríos) como motivación y contexto.
- **Para acotar/refutar supuestos fuertes:** linealidad perfecta (sustituir por respuesta caracterizada/calibrada), retención independiente de T (incluir cinética/Arrhenius medido), y deriva de fase despreciable (incluir dn/dT y control térmico).
- **Acción recomendada:** extraer de las fuentes originales valores/rangos de Δn(λ), t½(T), Ea, dn/dT y condiciones experimentales; incorporarlos en `compounds.py`/modelos con cita explícita y actualizar los análisis de sensibilidad/no linealidad/temperatura con esos parámetros.

## Artefactos del proyecto relacionados
- Modelo lineal y matriz: `model.py`, `outputs/response_matrix_A.csv`
- Comparación lineal vs no lineal y temperatura: `nonlinear_temperature_analysis.py`, `outputs/nonlinear_model_comparison.csv`, `outputs/nonlinear_temperature_report.md`
- Ajuste polinómico y coeficientes vs T: `polynomial_temperature_fit.py`, `outputs/polynomial_model_selection.csv`, `outputs/polynomial_coefficients_vs_temperature.csv`, `figures/polynomial_*`
- Sensibilidad/SNR/crosstalk: `outputs/sensitivity_*`, `outputs/snr_budget.*`, `outputs/*crosstalk*`


## 9. Herramientas de diseño y simulación útiles (public domain)

- **Meep (GPL-2.0):** EM/FDTD para guías, resonadores (MZI/crossbar); import GDSII vía gdstk.
- **gdstk (BSL-1.0):** GDSII/OASIS toolkit para diseño de layout.
- **Simphony:** alternativa de diseño photonics (sParameters).
