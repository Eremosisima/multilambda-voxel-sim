# Familias y variantes de arquitectura OPGPU (respuesta rápida e interferencia)

> Documento de exploración conceptual (v0.7). Define **familias de diseño** y variantes derivadas del concepto OPGPU para que implementadores puedan elegir rutas según velocidad, eficiencia, madurez de fabricación y costo. Énfasis en **respuesta rápida** y en el uso explícito de **interacciones aditivas y destructivas (interferencia)** para cómputo y conmutación. Estado: referencia abierta (no validada experimentalmente).

## 1. Principios ópticos comunes

### 1.1 Interferencia aditiva y destructiva como primitiva de cómputo
- **Suma/resta óptica coherente:** en un acoplador o MZI, los campos $E$ se combinan como $E_{out}\propto E_1 \pm E_2 e^{i\Delta\phi}$; la potencia/intensidad refleja interferencia constructiva (aditiva) o destructiva (sustractiva) según la fase relativa $\Delta\phi$.
- **Producto y MAC (multiply–accumulate):** un peso se codifica como transmitancia/fase $w_i$ (atenuación + desplazamiento de fase); la entrada como amplitud $x_i$. La detección coherente o interferométrica produce términos proporcionales a $w_i x_i$ y la suma se realiza por superposición en guías/acopladores (acumulación óptica).
- **Resta y signo:** se obtiene por desplazamiento de fase de $\pi$ (inversión), por salidas complementarias de un MZI (puertos bar/cross) o por **detección balanceada** ($I_+ - I_-$), cancelando términos de modo común y ruido.
- **Matrices unitarias/no unitarias:** redes de MZI (Clements/Reck) implementan transformaciones lineales por interferencia programable; combinadas con atenuación (p. ej. SVD óptica) cubren operaciones lineales generales.
- **Condición de coherencia:** las operaciones aditivas/destructivas dependen de coherencia de fase y estabilidad de camino; requieren control de fase (trim), láseres coherentes o auto-referencia según la variante.

### 1.2 Ejes de diseño
| Eje | Opciones | Impacto |
|---|---|---|
| Mecanismo de sintonía/conmutación | PCM, termo-óptico, electro-óptico (Pockels/Kerr), portadores (Si), mecánico/MEMS, líquido/fotoquímico | Velocidad, energía, no volatilidad |
| Detección | Directa, coherente, balanceada | Signo/resta, SNR, complejidad |
| Codificación | Intensidad, fase, compleja (I/Q), WDM | Densidad, robustez, aritmética |
| Volatilidad de peso | No volátil (PCM/ferroeléctrico) vs volátil (EO/portadores) | Costo de reconfiguración, latencia de carga |
| **Capacidad** | Cómputo (TOPS), memoria óptica/pesos (bits/celda, MB/módulo), ancho de banda (TB/s), 2D vs 3D | Escala de modelos/kernels, localidad de datos, throughput efectivo |

## 2. Familias de arquitectura

### 2.1 Familia A — Interferométrica coherente programable (base OPGPU, evolución)
- **Principio:** mallas MZI/crossbar donde cada celda aplica fase/atenuación; la salida es suma interferométrica (constructiva/destructiva) de contribuciones ponderadas.
- **Elementos:** divisores/combinadores, desfazadores, detectores balanceados para signo.
- **Variantes:**
  - **A1 (PCM no volátil, referencia):** pesos en Sb₂S₃ (M1), control VO₂/Espiropirano; optimizada para inferencia y pesos estacionarios. Velocidad de *inferencia* alta (propagación óptica) pero *reprogramación* lenta/costosa (térmica/óptica PCM).
  - **A2 (Híbrida PCM + EO):** pesos gruesos/persistentes en PCM y corrección/ajuste fino y rápido en moduladores EO (fase) para calibración dinámica y actualización incremental.
  - **A3 (Coherente I/Q):** codificación en fase y cuadratura para aritmética compleja y mayor densidad por portadora.
- **Fortalezas:** mapeo directo a MVM/GEMM, resta nativa por interferencia/detección balanceada. **Retos:** estabilidad de fase, pérdidas acumuladas, calibración (OMCC).

### 2.2 Familia B — Resonante de alta $Q$ (BIC / microrings / fotónica cristal)
- **Principio:** resonadores sintonizables que controlan acoplamiento y fase; la interferencia entre camino resonante y directo (tipo Fano/EIT) produce transiciones agudas de transmisión/reflexión (constructiva/destructiva en bandas estrechas).
- **Elementos:** anillos/microdiscos, cavidades BIC/quasi-BIC, guías de bus.
- **Variantes:**
  - **B1 (PCM-BIC):** parche PCM en cavidad BIC para gran contraste con baja energía de conmutación (fuerte confinamiento de campo).
  - **B2 (EO-resonante):** sintonía electro-óptica del índice en el resonador para respuesta rápida.
  - **B3 (WDM masivo):** banco de resonadores por longitud de onda para paralelismo espectral (suma sobre $\lambda$).
- **Fortalezas:** huella pequeña, alta selectividad, eficiencia energética por confinamiento. **Retos:** sensibilidad térmica/fabricación, ancho de banda limitado, control de acoplamiento.

### 2.3 Familia C — Electro-óptica ultrarrápida (Pockels / moduladores integrados)
- **Principio:** efecto Pockels (cambio de índice $\propto$ campo eléctrico, respuesta casi instantánea a escala de dispositivo) en MZI/ring para modular fase/amplitud a decenas–cientos de GHz.
- **Plataformas/materiales típicos:** LiNbO₃ en película delgada (TFLN), BaTiO₃ (BTO), PZT/PLZT, polímeros EO, híbridos Si–orgánicos (uso como opciones de plataforma para implementadores).
- **Variantes:**
  - **C1 (Malla EO volátil de alta velocidad):** pesos/operaciones dinámicas en moduladores EO; ideal para recarga rápida de kernels y señales de alta tasa (GPU/NPU tiempo-real). Requiere memoria externa/óptica para persistencia.
  - **C2 (EO no volátil emergente, p. ej. ferroeléctrico/topológico):** combina velocidad de conmutación EO y retención (pesos rápidos reconfigurables), puente entre A1 y C1.
  - **C3 (DAC óptico / ponderación rápida):** codificación de $x_i$ o $w_i$ a alta velocidad para streaming.
- **Fortalezas:** latencia de reconfiguración muy baja, gran ancho de banda. **Retos:** persistencia (salvo C2), consumo de drivers RF, integración y costo de plataforma.

### 2.4 Familia D — Plasmónica / ENZ / campo cercano (compacta y no lineal)
- **Principio:** modos plasmónicos o regímenes epsilon-near-zero concentran el campo en volúmenes sub-lambda, potenciando cambios de índice, absorción y no linealidad; la interferencia entre modos localizados y propagantes habilita conmutación/mezcla.
- **Elementos:** nanoantenas, guías híbridas dieléctrico–metal, capas TCO/ENZ (p. ej. ITO/CdO), integración con PCM/2D.
- **Variantes:**
  - **D1 (Plasmónica-PCM):** hotspot para conmutación PCM de baja energía/área.
  - **D2 (ENZ para activación/modulación):** no linealidad y sintonía rápida para funciones de activación NPU o mezcla.
  - **D3 (Metasuperficie programable):** control de frente de onda/fase local en arreglos densos.
- **Fortalezas:** extrema compacidad, interacción fuerte, respuesta potencialmente ultrarrápida. **Retos:** pérdidas óhmicas, acoplamiento a guías, gestión térmica.

### 2.5 Familia E — Todo-óptica no lineal (Kerr / portadores / materiales 2D)
- **Principio:** la luz controla la luz vía no linealidad $\chi^{(3)}$ (Kerr, portadores, saturación) o $\chi^{(2)}$ en materiales adecuados; interferencia convierte cambios de fase no lineal en modulación de intensidad.
- **Elementos:** guías SOI/SiN de alta no linealidad, cavidades, 3R-MoS₂/TMDs, semiconductores.
- **Variantes:**
  - **E1 (Conmutación Kerr/MZI):** conmutador por fase auto/cruzada en interferómetro.
  - **E2 (2D/TMD ultrarrápido):** modulación/polarización a escalas fs–ps en estructuras resonantes.
  - **E3 (Lógica/interferencia no lineal):** puertas basadas en umbrales de interferencia (constructiva→"1", destructiva→"0").
- **Fortalezas:** sin conversión O-E-O en el lazo de control, potencial ultrarrápido. **Retos:** potencia óptica requerida, diafonía, estabilidad y cascadabilidad.

### 2.6 Familia F — Espacio libre / difractiva / metasuperficie (paralelismo masivo)
- **Principio:** propagación e interferencia/difracción en 2D/3D (Fourier óptica, capas difractivas) realizan transformaciones lineales y correlaciones con alto paralelismo; la suma es interferencia en el plano de detección.
- **Variantes:**
  - **F1 (Metasuperficie programable en guía/plano):** reconfigurable (PCM/EO) para front-end tensorial.
  - **F2 (Híbrida cepillo + difractiva):** el arreglo 3D (cepillo) como banco de pesos/voxels y una etapa difractiva para mezcla global.
- **Fortalezas:** throughput y paralelismo espacial. **Retos:** alineación, precisión analógica, integración con PCIe/memoria óptica direccionable.

### 2.7 Familia G — Membranas apiladas de película delgada / cavidades Fabry–Pérot (interferencia por espesor)

- **Principio físico (análogos cotidianos):** la misma interferencia de película delgada que produce colores en **agua jabonosa** o franjas en experimentos tipo **Young/cabello** depende del espesor óptico $n d$ y la longitud de onda $\lambda$. Para una lámina/membrana, la diferencia de fase entre reflexiones (o transmisiones) es $\delta \approx \frac{4\pi n d \cos\theta}{\lambda} + \phi_r$, dando **máximos constructivos** y **mínimos destructivos** selectivos en $\lambda$. Apilando membranas de distintos espesores se obtienen respuestas espectrales/funcionales programables por capa.
- **Traslación a cómputo en “cores”/cerdas:** dentro de cada cerda o vóxel del cepillo 3D se apilan membranas dieléctricas (o cavidades Fabry–Pérot/etalon) con espesores calibrados. Cada capa actúa como selector/ponderador interferométrico (paso/bloqueo/atenuación/fase por $\lambda$), permitiendo:
  - **Paralelismo WDM en volumen reducido:** múltiples canales $\lambda$ procesados en la misma huella lateral mediante apilamiento vertical (nm–µm por membrana, muchas capas por “core”).
  - **Cómputo por interferencia constructiva/destructiva:** suma/resta y filtrado al combinar salidas de capas/cavidades (p. ej. detección diferencial, redes de etalones acoplados), análogo a los máximos/mínimos observables en la pared o en la película de jabón.
  - **Alta densidad/capacidad:** más elementos funcionales por mm³ al usar el eje vertical (complementario al cepillo extruido).
- **Elementos:** membranas multicapa (SiN/SiO₂/TiO₂/Ta₂O₅ u óxidos/dieléctricos compatibles), cavidades F–P, espaciadores de espesor controlado, acopladores a guía/fibra, opcionalmente pixeles por cerda.
- **Sintonía (para velocidad):**
  - **Índice $n$ (rápido):** electro-óptico (Pockels), portadores o materiales sintonizables para desplazar la condición de interferencia sin mover masa.
  - **Fase/estado (no volátil o latching):** PCM en capas selectivas para pesos persistentes.
  - **Espesor $d$ (MEMS/membrana deformable):** ajuste mecánico de cavidad; mayor recorrido pero típicamente más lento que EO.
- **Variantes:**
  - **G1 (Apilado pasivo WDM por espesor):** membranas de espesores fijos para bancos de filtros/ponderación espectral compactos (alta capacidad por volumen, sin reconfiguración rápida).
  - **G2 (Apilado sintonizable por índice, EO):** membranas/cavidades con control EO para reconfiguración **rápida** (ps–ns) y cómputo dinámico en espacio reducido.
  - **G3 (Híbrido PCM+EO en membranas):** pesos base persistentes (PCM/capa) y ajuste fino rápido (EO) por canal/capa.
  - **G4 (F–P/MEMS):** cavidades sintonizables por espesor efectivo para calibración o conmutación de menor tasa.
- **Fortalezas:** muy alta densidad volumétrica, paralelismo espectral natural, uso directo de interferencia constructiva/destructiva por diseño de espesor, potencial de integración vertical en el cepillo. **Retos:** tolerancias nanométricas de espesor/planitud, pérdidas por interfaces, sensibilidad angular/térmica, uniformidad entre cerdas y complejidad de fabricación/apilado.
- **Vínculo con los experimentos cotidianos:** la “franja brillante” equivale a condición constructiva (salida/peso reforzado) y la “franja/banda oscura o negra” a cancelación destructiva (bloqueo/resta), trasladadas a espesores $n d$ y longitudes de onda controladas dentro del core.

## 3. Comparativa orientativa (familias)

| Familia | Tiempo de respuesta típico (sintonía/conmutación) | No volatilidad | Interferencia aditiva/destructiva | Madurez de integración | Mejor ajuste en OPGPU |
|---|---:|---|---|---|---|
| A. Interferométrica PCM/mixta | ps–ns (inferencia); µs–ms (reprog. PCM) | Alta (A1/A2) | Nativa (MZI/balanceada) | Media | Pesos estacionarios, MVM, base actual |
| B. Resonante BIC/ring | ps–ns (EO/óptica); limitada por $Q$ | Depende del actuador | Fano/interferencia resonante | Media | Celdas densas, WDM, eficiencia |
| C. Electro-óptica (Pockels) | ps (sub-ns) | Baja (C1) / media-alta (C2) | MZI/ring | Media–alta (según plataforma) | Recarga rápida, streaming, tiles dinámicos |
| D. Plasmónica/ENZ | fs–ps (potencial) | Depende | Local + acoplada | Baja–media | Activaciones, hotspots, compacidad |
| E. Todo-óptica no lineal | fs–ps | N/A (señal) | Umbral/fase no lineal | Baja–media | Lógica/activación sin O-E-O |
| F. Difractiva/metasuperficie | ps–ns (según actuador) | Depende | Suma en campo lejano/plano | Baja–media | Pre/post-procesado paralelo |
| G. Membranas película delgada / F–P apiladas | ns–µs (MEMS/termo); ps–ns (EO/índice); pasivo fijo sin reconfig. | Depende (PCM sí, EO no, MEMS latching) | Constructiva/destructiva por espesor $n d$ y $\lambda$ | Baja–media (recubrimientos); MEMS/EO más complejo | Alta densidad volumétrica, WDM en “core”, cómputo en espacio reducido |

*Los rangos son orientativos y dependen de material, dispositivo y sistema; deben validarse por implementación.*

## 4. Variantes de producto/referencia sugeridas (para implementadores)

| Variante | Composición | Objetivo | Compromiso |
|---|---|---|---|
| **OPGPU-Ref (A1)** | MZI + Sb₂S₃/VO₂/azobenceno/espiropirano (base actual) | Inferencia con pesos persistentes, máximo aprovechamiento del diseño abierto existente | Reprogramación lenta |
| **OPGPU-FastReload (A2/C2)** | PCM persistente + capa EO rápida (fase/ajuste) | Actualización frecuente de pesos/corrección en línea con retención | Mayor complejidad y drivers |
| **OPGPU-RT (C1)** | Núcleo EO interferométrico de alta tasa + memoria óptica externa/buffers | Procesamiento de señal/streaming y kernels dinámicos | Sin persistencia intrínseca de pesos |
| **OPGPU-Dense (B1/B3)** | Celdas resonantes BIC/ring + WDM denso | Densidad y eficiencia por confinamiento | Sensibilidad y calibración fina |
| **OPGPU-Hybrid-NL (A + D/E)** | Malla lineal interferométrica + bloques ENZ/2D/no lineales | Activaciones y funciones no lineales en dominio óptico (NPU) | Madurez y pérdidas |
| **OPGPU-3D (F2 + cepillo)** | Arreglo cepillo 3D + etapa difractiva/interferométrica | Paralelismo volumétrico masivo | Integración/alineación |
| **OPGPU-Membrane (G2/G3)** | Membranas/F–P apiladas en cerda/core con sintonía EO (y opcional PCM) | Alta velocidad y alta capacidad en volumen reducido por interferencia de espesor $n d$ y WDM vertical | Tolerancias de fabricación, pérdidas y control térmico/angular |

## 5. Uso de interferencia aditiva/destructiva (patrones de diseño)

1. **MAC coherente:** $\sum_i w_i x_i$ por superposición; resta con desfase $\pi$ o salidas diferenciales.
2. **Detección balanceada:** salida útil $I_1-I_2$ cancela offset y ruido común, mejora rango dinámico.
3. **Cancelación de crosstalk:** rutas diferenciales y acoplamiento destructivo en modos parásitos.
4. **Compuertas/umbrales:** interferencia no lineal (E) o resonante (B) donde constructivo supera umbral y destructivo lo inhibe.
5. **Multiplexado:** suma de canales WDM/espaciales en un bus común con separación por filtro/interferencia.
6. **Calibración:** medición de nulos de interferencia destructiva para ajustar fase (OMCC/azobenceno).

## 6. Recomendaciones para adopción abierta
- **Modularidad:** definir interfaces entre plano de pesos (A/B), plano de modulación rápida (C/D/E) y plano de interconexión/memoria (M0–M3) para que implementadores combinen familias.
- **Documentar supuestos:** coherencia, presupuesto de pérdidas/fase, y requisitos de láser/detección por variante.
- **Ruta incremental:** partir de A1 (referencia actual) → A2/B1 (eficiencia/densidad) → C1/C2 o D/E (velocidad/no linealidad) según capacidad de proceso.
- **Costo/accesibilidad:** priorizar variantes con plataformas y procesos más disponibles (p. ej. SiN/SiPh + PCM) y publicar BOM/modelos de costo cuando existan prototipos.

## 7. Comparación cuantitativa conceptual (desarrollo)

El script `../model_families_development.py` genera una comparación multi-eje reproducible para variantes de las familias A–G y combinaciones H1–H5, con énfasis en **precio, factibilidad, velocidad, fiabilidad, dimensiones y capacidad** (cómputo TOPS, memoria/pesos efectiva y ancho de banda). Salidas: `../outputs/families_dev_comparison.{md,csv,json}` y `../figures/families_dev_{axes,speed_cost,reliability_feasibility,capacity_speed}.png`.

Para combinaciones creativas entre familias y estrategia de apertura/IP, ver [`family-combinations-openhw.md`](family-combinations-openhw.md).

> Los valores son estimaciones conceptuales de orden de magnitud (no cotizaciones ni mediciones); deben recalibrarse con datos de proceso, prototipo y cadena de suministro.

## 8. Trabajo futuro
- Modelado comparativo por familia (latencia, energía/op, IL, densidad, estabilidad de fase, capacidad efectiva) con parámetros calibrados.
- Prototipos de celda: MZI-PCM (A1), resonador BIC-PCM (B1) y modulador EO de fase (C1) para caracterización.
- Evaluación de coherencia y detección balanceada en el arreglo cepillo 3D y su impacto en precisión y capacidad efectiva.