# Dimensiones mínimas fabricables (OPGPU) y dimensiones de aceleradores de IA actuales

> Documento de referencia conceptual y comparativa (v0.8).  
> **Parte A:** dimensiones *fabricables* estimadas para propuestas OPGPU, considerando restricciones de procesos fotónicos y **control térmico factible**.  
> **Parte B:** dimensiones/capacidades típicas de **GPU, TPU y NPU** actuales para actividades avanzadas de IA.  
> **Aviso:** las estimaciones OPGPU son conceptuales (no diseños validados ni DRC de fundición). Las cifras de productos comerciales son aproximadas, dependen de variante/fuente y se citan con fines comparativos.

## Parte A — Dimensiones mínimas fabricables en propuestas OPGPU

### A.1 De teórico a fabricable (qué cambia)

Las dimensiones teóricas (`outputs/min_dimensions.md`) parten de confinamiento ($\lambda/2n$), capas $\lambda/4n$, longitud de fase y límites térmicos ideales (P1). En fabricación real dominan:

| Factor fabricable / térmico | Efecto típico | Supuesto usado (conceptual) |
|---|---|---|
| Litografía y geometría PIC (SiPh/SiN, 193 nm DUV) | Feature práctico > límite óptico; guías ~0.4–0.5 µm, gaps ~200 nm | Feature práctico **150 nm**, guía 500 nm |
| Calentadores/actuadores (doped/PIN, termo-óptico) | Gran huella por elemento activo y contactos | **50 µm** largo calentador, **6 µm** keepout lateral |
| Aislamiento térmico (PCM 300 °C, VO₂ < 68 °C) | Trincheras/espaciado, separación axial, spreading | Pitch PCM **20 µm**, separación axial **12 µm**, trinchera **3 µm**, margen 10 µm |
| Registro/alineación multicapa y 3D | Aumenta área/volumen y reduce rendimiento | **0.5 µm** por capa + margen de alineación |
| Ruteo eléctrico/óptico y acceso (vías, pads) | Keepout por celda | **5 µm** por lado (celdas complejas) |
| Radio de curvatura (anillos) | Fija huella mínima resonante | **8 µm** (SiPh) / **15 µm** (SiN, conservador) |
| Gestión térmica de módulo | Disipador/spreader/TIM, interfaz de enfriamiento | Overhead volumen enfriamiento **×1.4**, spreading **×1.25** |
| Rendimiento/empaquetado/IO | Redundancia, scribe, óptica/drivers/enclosure | **×1.3** (rendimiento/empaque) + overhead módulo |

### A.2 Dimensiones mínimas fabricables por celda/elemento (con control térmico factible)

Fuente: `outputs/manufacturable_dimensions.{csv,json,md}`, `model_manufacturable_dimensions.py`.

| Propuesta | Composición | Pitch lat (µm) | Long. activa (µm) | Espesor capa (nm) | Pitch vert (µm) | **Área celda (µm²)** | **Volumen celda (µm³)** | Control térmico factible | Nota fabricable |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **A1** | MZI + Sb₂S₃/VO₂ (ref) | 20 | 45.0 | 194 | 16.0 | **900** | **14,400** | Micro-calentadores doped/PIN para Sb₂S₃, trincheras de aislamiento, heat spreader, sensado local; escritura pulsada y calendarizada (OMCC) | Aislamiento térmico y contactos dominan; 300 °C local viable con trincheras+spreading manteniendo VO₂ < 68 °C |
| **B3** | Banco WDM microrings | 28 | 44.0 | 194 | 6.0 | **1,232** | **7,392** | Sintonía termo-óptica o EO, estabilización (TEC/sustrato), bloqueo de resonancia | Radio de curvatura y huella de sintonizador/calentador dominan; requiere estabilidad térmica |
| **G1** | Membranas pasivas WDM (λ/4n) | 7.0 | 7.0 | 194 | 5.69 | **49** | **279** | Sin calentamiento activo del apilado; solo estabilización térmica a nivel paquete | Espesor nm factible por depósito; lateral por registro/aperturas de acoplo |
| **G2** | Membranas/F–P EO | 11.0 | 16.0 | 176 | 6.69 | **176** | **1,177** | Carga térmica de electrodos/RF gestionada por spreading; estabilización de paquete | Electrodos y registro dominan; sintonía rápida con interfaces añadidas |
| **G3** | Membranas PCM+EO híbridas | 13.0 | 23.0 | 144 | 7.19 | **299** | **2,149** | Micro-calentadores localizados para capas PCM, trincheras, spreading; presupuesto térmico EO | Calor de escritura PCM exige aislamiento incluso en capas delgadas |
| **H3** | Open WDM-PCM (A1+G1+B3) | 22 | 79.0 | 194 | 19.69 | **1,738** | **34,218** | Calentadores PCM + sintonía de anillos + TEC/spreader de paquete; planificación térmica OMCC | Híbrido avanzado más práctico: combina necesidades térmicas PCM con apilado pasivo y control resonante |
| **H1** | Membrane-Brush NV 3D (A1+G3) | 22 | 22 | 144 | 110.75 | **484** | **53,604** | Calentadores segmentados por vóxel, aislamiento vertical/lateral, spreader/manifold integrado; secuenciado estricto | 3D fabricable solo con empaquetado/térmica avanzados (vías térmicas/microfluidos); rendimiento y extracción de calor dominan |
| **H4** | Tensor volumétrico (G2/G3+F2+A1) | 20 | 20 | 176 | 118.13 | **400** | **47,251** | Calentadores/drivers distribuidos, spreading/enfriamiento de alta capacidad, estabilización activa | Mayor carga de integración/térmica; requiere empaquetado 3D y enfriamiento agresivos |

**Lectura:** el control térmico factible (calentadores localizados, trincheras, spreading, estabilización TEC/sustrato y secuenciado OMCC) es el principal multiplicador frente al mínimo teórico en propuestas con PCM/actuación térmica (A1, G3, H1, H3, H4). Las membranas pasivas (G1) permanecen más compactas a nivel celda; los anillos (B3) quedan limitados por radio y sintonía.

### A.3 Tamaño estimado de módulo OPGPU para IA “decente” (conceptual, manufacturable)

Objetivos ilustrativos (no especificaciones): **Edge 50 TOPS / 8 GB**, **Workstation 300 TOPS / 48 GB**, **Datacenter 800 TOPS / 96 GB** por acelerador. Incluye factores conservadores de densidad fabricable, rendimiento/empaque (×1.3) y enfriamiento (×1.4). “Huella 2D equiv.” es el área activa equivalente; el volumen incluye gestión térmica/empaque.

| Propuesta | Clase | Objetivo | Área activa est. (cm²) | Volumen módulo est. (cm³) | Huella 2D equiv. | Forma de referencia |
|---|---|---|---:|---:|---:|---|
| **A1** | Edge | 50 TOPS / 8 GB | 130 | 728 | ~11.4×11.4 cm | módulo/tarjeta |
| **A1** | Workstation | 300 TOPS / 48 GB | 780 | 4,368 | ~27.9×27.9 cm | tarjeta/módulo |
| **A1** | Datacenter | 800 TOPS / 96 GB | 2,080 | 8,736 | ~45.6×45.6 cm | módulo OAM/SXM-class |
| **B3** | Edge | 50 TOPS / 8 GB | 81 | 364 | ~9.0×9.0 cm | módulo/tarjeta |
| **B3** | Datacenter | 800 TOPS / 96 GB | 1,300 | 4,368 | ~36.1×36.1 cm | módulo |
| **G1** | Edge | 50 TOPS / 8 GB | 108 | 485 | ~10.4×10.4 cm | módulo/tarjeta |
| **G2** | Edge | 50 TOPS / 8 GB | 54 | 485 | ~7.4×7.4 cm | módulo/tarjeta |
| **G2** | Datacenter | 800 TOPS / 96 GB | 867 | 5,824 | ~29.4×29.4 cm | módulo |
| **G3** | Edge | 50 TOPS / 8 GB | 59 | 243 | ~7.7×7.7 cm | módulo/tarjeta |
| **G3** | Workstation | 300 TOPS / 48 GB | 355 | 1,456 | ~18.8×18.8 cm | tarjeta/módulo |
| **G3** | Datacenter | 800 TOPS / 96 GB | 946 | 2,912 | ~30.7×30.7 cm | módulo |
| **H3** | Edge | 50 TOPS / 8 GB | 72 | 291 | ~8.5×8.5 cm | módulo/tarjeta |
| **H3** | Workstation | 300 TOPS / 48 GB | 433 | 1,747 | ~20.8×20.8 cm | tarjeta/módulo |
| **H3** | Datacenter | 800 TOPS / 96 GB | 1,156 | 3,494 | ~34.0×34.0 cm | módulo |
| **H1** | Edge | 50 TOPS / 8 GB | 43 | 121 | ~6.6×6.6 cm | módulo/tarjeta |
| **H1** | Workstation | 300 TOPS / 48 GB | 260 | 728 | ~16.1×16.1 cm | tarjeta/módulo |
| **H1** | Datacenter | 800 TOPS / 96 GB | 693 | 1,456 | ~26.3×26.3 cm | módulo |
| **H4** | Edge | 50 TOPS / 8 GB | 36 | 104 | ~6.0×6.0 cm | módulo/tarjeta |
| **H4** | Workstation | 300 TOPS / 48 GB | 217 | 624 | ~14.7×14.7 cm | tarjeta/módulo |
| **H4** | Datacenter | 800 TOPS / 96 GB | 578 | 1,248 | ~24.0×24.0 cm | módulo |

> **Interpretación:** bajo supuestos conservadores de fabricación/térmica, H1/H4 ofrecen la menor huella/volumen *si* se resuelve integración 3D y extracción de calor; G3/H3 son compromisos más plausibles; A1/B3/G1 resultan más voluminosos para el mismo objetivo. Estas cifras son extrapolaciones conceptuales (no validadas) y dependen críticamente de densidad efectiva, pérdidas, potencia y empaquetado óptico-eléctrico.

## Parte B — Dimensiones y escala de NPU, TPU y GPU actuales (IA avanzada)

Valores orientativos (variantes/configuraciones cambian por generación y SKU). “IA avanzada” implica desde LLMs/inferencia multimodal local hasta entrenamiento/servicio a gran escala.

### B.1 GPU (datacenter, alto rendimiento)

| Ejemplo | Proceso / die | Memoria | Cómputo (referencia) | Potencia | Factor de forma / escala física |
|---|---|---|---|---|---|
| NVIDIA H100 SXM | TSMC 4N, **~814 mm²** (límite retícula ~858 mm²) | 80 GB HBM3 (3.35 TB/s) | hasta ~989 TFLOPS BF16 (tensor, sparsity) / 67 TF FP32 | ~700 W (SXM) | Módulo SXM + placa base; die ~814 mm²; enfriamiento líquido/aire en servidor |
| NVIDIA H100 PCIe / NVL | ~814 mm² | 80–94 GB HBM | similar clase tensor | 350–400 W | Tarjeta PCIe FHFL (estándar largo ~267 mm) o NVL |
| NVIDIA H200 | clase Hopper, ~814 mm² | 141 GB HBM3e (4.8 TB/s) | similar/ajustada | hasta ~700 W | SXM/módulo |
| NVIDIA B200/GB200 (Blackwell) | multi-die / paquete avanzado | hasta 192 GB HBM3e por GPU (B200) | superior a Hopper (gen. siguiente) | hasta ~1000 W (módulo) | Módulos SXM/placas de alto TDP |

*Fuentes orientativas:* especificaciones NVIDIA, análisis de die (TechInsights/medios), documentación de plataforma. Para entrenamiento/inferencia avanzada a gran escala se usan sistemas multi-GPU (NVLink/NVSwitch) en racks.

### B.2 TPU (ASIC de Google, escala chip a pod)

| Ejemplo | Cómputo por chip (ref.) | HBM por chip | BW / ICI / potencia (ref.) | Escala física |
|---|---|---|---|---|
| TPU v4 | 275 TFLOPS bf16/int8 | 32 GB HBM2 (1.2 TB/s) | ~170 W, 3D torus, 6 enlaces ICI | Die <600 mm² (7 nm); 4 chips/host, 4096 chips/pod (racks, refrigeración líquida) |
| TPU v5p | 459 TFLOPS bf16 (918 int8 equiv. en tablas) | 95 GB HBM (2.765 TB/s) | ICI 1.2 TB/s/chip, 3D torus | 4 chips/host (VM 208 vCPU/448 GB); slices hasta 6144 chips, pod 8960; escala rack/supercomputadora |
| TPU v5e / v6e (Trillium) | 197 / 918 TFLOPS bf16 por chip | 16 / 32 GB HBM | 2D torus, pods menores (256 chips) | Módulos 1T/4T/8T (4–8 chips/host) |
| TPU7x (Ironwood) | 2307 TFLOPS bf16 por chip | 192 GB HBM (7.38 TB/s) | 3D torus, 4 chips/host | Pod 9216 chips |

*Fuentes orientativas:* Google Cloud TPU docs, TPU system architecture papers (ISCA), resúmenes públicos. Dimensiones exactas de paquete por chip no siempre son públicas; la unidad operativa “decente” para IA avanzada suele ser un **slice/pod** (múltiples hosts/racks), mientras el chip es comparable en clase a aceleradores de ~centenares de mm² y cientos de W.

### B.3 NPU (edge, PC/móvil y datacenter)

| Clase / ejemplo | Cómputo (INT8, ref.) | Memoria | Potencia | Dimensiones / forma |
|---|---:|---|---|---|
| **Edge integrado (SoC IoT/premium)** — Qualcomm QCS8550 | 48 TOPS (Hexagon) | LPDDR5x externa (SoC) | nivel SoC (bajo-medio W) | SoC **15.6 × 14.0 mm** (218 mm², 4 nm), CPU+GPU+NPU+DSP integrados |
| **Edge/industrial alto** — Qualcomm QCS9075 / IQ9 | 100 TOPS densos (200 sparse) | hasta 36 GB LPDDR5X | nivel SoC | SoC/módulo embebido; plataforma de largo ciclo de vida |
| **PC/móvil (integrada)** — Apple ANE (M4) / NPUs PC (Intel/AMD/Qualcomm X-series) | ~38–50+ TOPS | unificada/compartida (hasta 128 GB en M4 Max) | 15–54 W (paquete/plataforma) | NPU como bloque dentro del SoC/paquete (mm² dentro del die) |
| **Acelerador edge discreto** — Hailo-8 (módulo) | 26 TOPS | on-chip (sin DRAM externa propia) | 2.5 W típico | Módulo M.2 / mini-PCIe **~22 × 30 mm**; también PCIe |
| **NPU datacenter (tarjeta)** — Qualcomm Cloud AI 100 Ultra | 870 TOPS | 128 GB LPDDR4x | ~150 W | Tarjeta PCIe (formato servidor FHHL/FHFL según SKU) |

*Fuentes orientativas:* documentación de Qualcomm/Intel/AMD/Apple/Hailo, resúmenes de productos y benchmarks públicos. Las NPUs integradas comparten área con el SoC; las discretas van desde módulos de pocos cm² (edge) a tarjetas PCIe completas (datacenter).

### B.4 Rangos de “dimensiones decentes” para IA avanzada (resumen práctico)

| Segmento | Cómputo típico | Memoria típica | Potencia típica | Tamaño físico típico |
|---|---|---|---|---|
| **Edge/embebido avanzado** | 10–50 TOPS INT8 (hasta ~100) | 4–32 GB | 2–30 W | SoC 100–300 mm² o módulo 20×30 mm a tarjeta pequeña |
| **PC/workstation local (LLM/inferencia multimodal)** | 40–100+ TOPS NPU + GPU integrada/discreta; o GPU 100–300+ TOPS/TFLOPS efectivos | 16–128 GB (unificada o VRAM) | 30–300 W | Paquete SoC/laptop o GPU discreta/tarjeta PCIe |
| **Datacenter (entrenamiento/servicio gran escala)** | cientos de TFLOPS–PFLOPS por chip; clusters/pods para frontera | 32–192 GB HBM por acelerador; TB+ agregado | 150–1000 W por acelerador; kW–MW por sistema | Die ~600–850+ mm², paquete OAM/SXM o tarjeta PCIe; racks/pods |

## Parte C — Conclusiones y próximos pasos

- **Fabricabilidad y térmica:** en OPGPU, el paso de mínimo teórico a fabricable lo dominan calentadores/contactos, aislamiento (PCM 300 °C/VO₂ 68 °C), registro multicapa y extracción de calor. G1/G2 escalan mejor en celda; H1/H4 prometen densidad/volumen pero exigen empaquetado 3D y enfriamiento avanzados.
- **Realismo de módulo:** para prestaciones “decentes” (50–800 TOPS, 8–96 GB) las estimaciones conceptuales sitúan módulos OPGPU desde ~6–11 cm (huella equiv., edge, H1/H4/G2/G3/H3) hasta decenas de cm en datacenter, sujetos a densidad real, pérdidas y potencia.
- **Comparación:** GPUs/TPUs datacenter actuales concentran gran cómputo/memoria en dies de ~600–815 mm² y paquetes de alta potencia; NPUs cubren desde mm² en SoC hasta tarjetas PCIe. OPGPU apunta a ventajas potenciales en interferencia/WDM/memoria óptica, pero requiere validación de rendimiento, energía y térmica.
- **Próximos pasos:** cerrar DRC por proceso (SiN/SiPh/BEOL PCM), modelos térmicos 3D con solución de enfriamiento concreta, presupuesto de pérdidas/potencia (TOPS/W) y prototipos de celda/módulo; mantener enfoque open-hardware y modular (ver `CANDIDATE_REPOS_STRATEGY.md`).

*Fuentes consultadas (orientativas):* Google Cloud TPU docs y arquitectura TPU v4/v5p; especificaciones públicas NVIDIA (H100/H200/Blackwell); documentación Qualcomm/Apple/Hailo/Intel/AMD; IPSR-I Silicon Photonics (2024); literatura de integración PCM/fotónica de silicio y phase shifters térmicos (Nature/Optica/AIP, 2024). Ver `outputs/manufacturable_dimensions.json` y `outputs/min_dimensions.json` para supuestos numéricos OPGPU.