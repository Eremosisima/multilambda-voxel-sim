# DivulgaciÃ³n defensiva / arte previo â€” OPGPU v0.8 (consolidada)

- **TÃ­tulo:** Open Photonic GPU (OPGPU) â€” Estrategias, esquemÃ¡ticos, instrucciones y diseÃ±o de memoria/cÃ³mputo fotÃ³nico (Aâ€“G, H1â€“H5, M0â€“M3/OMCC, PCIe/OpenCL/OpenVINO)
- **VersiÃ³n/estado:** v0.8.0-research (conceptual/simulado), commit `cd58339` (base `ed4b8fe`), [FECHA de preparación/actualización]: 2026-11-19 (base v0.8: 2026-11-17)  
- **Autores/titulares (derechos sobre la obra original):** [COMPLETAR: nombres, ORCID/afiliaciÃ³n, consentimiento de dedicaciÃ³n] / â€œOpen Photonic GPU contributorsâ€ (provisional)  
- **Repositorio fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`open-photonic-gpu/`)  
- **Identificadores:** Concept DOI [ ], DOI versiÃ³n [ ], ip.com ID [ ], Wayback [ ]
- **Licencia/dedicaciÃ³n:** Objetivo **dominio pÃºblico (CC0 1.0)** para uso libre universal y **divulgaciÃ³n defensiva/arte previo** de lo divulgado, en la medida permitida por la ley y sujeto a consentimiento de titulares. Estado vigente del snapshot: licencias mixtas (Apache-2.0 cÃ³digo, CERN-OHL-S v2 hardware, CC BY-SA 4.0 docs) hasta transiciÃ³n (ver `PUBLIC_DOMAIN_DEDICATION.md`). Sin garantÃ­a; sin FTO; marcas nominativas.

## 1. PropÃ³sito y naturaleza de la divulgaciÃ³n
DivulgaciÃ³n tÃ©cnica **habilitante** y pÃºblica de arquitecturas, estrategias, esquemÃ¡ticos, instrucciones, parÃ¡metros, variantes y resultados de simulaciÃ³n de una unidad de cÃ³mputo/memoria predominantemente Ã³ptica (OPGPU), con interfaz PCIe y compatibilidad OpenCL/OpenVINO. Se publica para: (a) permitir uso, estudio, fabricaciÃ³n y mejora por cualquier persona, y (b) constituir **arte previo** que dificulte la apropiaciÃ³n registral/patentamiento por terceros de lo aquÃ­ descrito. **No** es un dispositivo fabricado ni validado experimentalmente.

## 2. Principio de funcionamiento (resumen habilitante)
- **CÃ³mputo Ã³ptico:** operaciones tipo MVM/MAC y tensores mediante interferencia constructiva/destructiva coherente ($E_{out}\propto E_1 \pm E_2 e^{i\Delta\phi}$), modulando amplitud/fase/polarizaciÃ³n/longitud de onda (MZI, mallas, resonadores, pelÃ­cula delgada/Fâ€“P, difracciÃ³n/metasuperficies).
- **Memoria/estado Ã³ptico:** pesos/estado en PCM (p.ej. Sbâ‚‚Sâ‚ƒ, no volÃ¡til, multinivel), conmutaciÃ³n/buffer rÃ¡pido (p.ej. VOâ‚‚), elementos fotoquÃ­micos/sintonÃ­a (azobenceno, espiropirano) y almacenamiento/retardo por resonancia/cavidades/anillos/Fâ€“P (M0â€“M3).
- **Modos:** GPU (MVM paralelo general), NPU (inferencia, pesos estacionarios, activaciones), TPU-like (GEMM/sistÃ³lico/tensorial por bloques).
- **Interfaz:** host PCIe (EP) + DMA/BAR/CSRs + command processor + cadena E/Oâ€“O/E; exposiciÃ³n como acelerador tipo OpenCL y rutas de ejecuciÃ³n OpenVINO (plugin nativo, vÃ­a backend OpenCL, heterogÃ©neo/fallback).
- **GestiÃ³n:** coprocesador OMCC con acceso/arbitraje a memoria Ã³ptica (M0â€“M3), colas, calibraciÃ³n/RAS.

## 3. Arquitectura de sistema y esquemÃ¡tico (nivel plataforma)

```text
HOST (CPU) â”€â”€ PCIe Gen4/5 x8/x16 â”€â”€ [EP PCIe + DMA/Bridge + BAR/CSRs + Cmd Processor + OMCC]
                                              â”‚ control/config/colas        â”‚ datos
                                       [TX: SerDesâ†’modulaciÃ³n E/O (Î»/WDM)]
                                              â”‚  guÃ­as/fibras  (dominio Ã³ptico)
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  PLANO FOTÃ“NICO INTERCAMBIABLE  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚  Red WDM/broadcast + Malla/tiles de cÃ³mputo (Aâ€“G / H1â€“H5) + Memoria M0â€“M3       â”‚
        â”‚  Control tÃ©rmico/bias/actuaciÃ³n + sensado/telemetrÃ­a                             â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                              â”‚  guÃ­as/fibras
                                       [RX: fotodetecciÃ³n O/Eâ†’ADC/TIAâ†’buffers]
                                              â”‚ DMA/IRQ/eventos â†’ HOST
```

Interfaz de mÃ³dulo: Ã³ptica (guÃ­as/fibras/acopladores), control/tÃ©rmico, alimentaciÃ³n. Plano fotÃ³nico sustituible por candidato (aislamiento modular).

## 4. Estrategias y familias (Aâ€“G) y combinaciones (H1â€“H5)

**Familias base (principio):** A1 MZI/PCM no volÃ¡til (pesos por fase), A2 MZI termo-Ã³ptico, B1/B3 resonadores/anillos (WDM, densidad), C1 fotoquÃ­mico, D1/D2 VOâ‚‚/plasmÃ³nico (conmutaciÃ³n rÃ¡pida), E1 redes coherentes/MZI-mesh, F1/F2 difractiva/metasuperficie, G1/G2/G3 membranas/cavidades de pelÃ­cula delgada (Fâ€“P, interferencia por espesor Ã³ptico $n\cdot d$, variantes pasiva/EO/PCM+EO).

**Combinaciones candidatas:** H1 Membrane-Brush NV (A1+G3+3D, capacidad NV volumÃ©trica), H2 RT Membrane-WDM (G2+B3+D1, reconfiguraciÃ³n rÃ¡pida), H3 Open WDM-PCM (A1+G1+B3, abierto/factible), H4 Volumetric Tensor Membrane (G2/G3+F2+A1, techo capacidad, alto riesgo), H5 Dense Resonant Stack (G1+B1, pasivo denso).

**Priorizadas (P1):** H3 (abierto/factible), G2 (velocidad/BW), G3 (NV+velocidad), H1 (escalado NV 3D), H4 (techo capacidad, aislar).

## 5. EsquemÃ¡ticos por candidato priorizado (bloques e instrucciones)

### H3 â€” Open WDM-PCM (A1 + G1 + B3)
```text
Î»1..Î»n â”€ MUX/WDM â”€â”¬â”€ banco microrings/filtros (B3, selectivo) â”€â”
                  â””â”€ celdas MZI-PCM Sbâ‚‚Sâ‚ƒ (A1, peso/retenciÃ³n) â”€â”¤â”€ combinador â”€ PD/TIA (O/E)
Filtros/membranas pasivas de espesor fijo (G1, nÂ·d) proveen selecciÃ³n/estabilizaciÃ³n.
Control: escritura PCM (pulsos), sesgo tÃ©rmico, calibraciÃ³n; lectura coherente.
```
Instrucciones: calibrar mapa fase-peso PCM multinivel; operar pesos estacionarios NV; priorizar procesos dielÃ©ctricos pasivos; aislamiento C&D por mÃ³dulo.

### G2 â€” Membrana EO rÃ¡pida (G2, Fâ€“P apilada sintonizada por Ã­ndice EO)
```text
Entrada Ã³ptica/WDM â†’ pila de membranas/cavidades Fâ€“P (espesor d, n ajustable por EO)
                  â†’ interferencia selectiva (constructiva/destructiva por nÂ·d, Î»)
                  â†’ salida/PD. Driver EO + control de fase por canal.
```
Instrucciones: definir apilado (d,n) por canal, bias EO, gestiÃ³n tÃ©rmica/RF, desacoplar driver EO como bloque sustituible.

### G3 â€” Membrana PCM+EO hÃ­brida
```text
Entrada â†’ cavidades Fâ€“P (nÂ·d): capa/estado base PCM (NV) + ajuste fino EO (rÃ¡pido) â†’ salida/PD.
Modos: base NV (PCM) + reconfiguraciÃ³n dinÃ¡mica (EO); control tÃ©rmico para PCM.
```
Instrucciones: particionar estado NV (PCM) vs ajuste EO; secuenciar escritura PCM para limitar crosstalk tÃ©rmico.

### H1 â€” Membrane-Brush NV 3D (A1 + G3 + cepillo)
```text
       â”Œâ”€ capa membrana G3 (canales por nÂ·d) â”€â”
Î»/WDM â”€â”¼â”€ capa MZI-PCM A1 (pesos NV)        â”œâ”€ apilado 3D tipo cepillo/cerdas â”€ vÃ­as Ã³pticas â”€ O/E
       â””â”€ capa(s) repetidas, particiÃ³n tÃ©rmica â”˜
```
Instrucciones: particiÃ³n tÃ©rmica entre capas, pitch/guardas de crosstalk, redundancia (spares) y calibraciÃ³n por plano.

### H4 â€” Volumetric Tensor Membrane (G2/G3 + F2 + A1)
```text
Entrada â†’ apilado 3D de membranas (G2/G3) â†’ etapa difractiva/metasuperficie F2 (mezcla global)
       â†’ celdas A1 PCM donde convenga (NV) â†’ salida/PD. IntegraciÃ³n/alineaciÃ³n 3D estricta.
```
Instrucciones: tratar como candidato de alto riesgo; aislar completamente; validar alineaciÃ³n, pÃ©rdidas y yield antes de escalar.

## 6. JerarquÃ­a de memoria Ã³ptica y mapeo (M0â€“M3/OMCC)
```text
M0 (anÃ¡logo/estado inmediato, psâ€“ns): coherencia/campo en guÃ­as, retardo/resonancia.
M1 (buffer rÃ¡pido, nsâ€“Âµs): cavidades/anillos, VOâ‚‚/latches Ã³pticos, â€œcapacitores Ã³pticosâ€ como retenciÃ³n temporal.
M2 (working set, Âµsâ€“ms, volatilidad media): estados conmutables (VOâ‚‚/fotoquÃ­micos) y buffers resonantes.
M3 (no volÃ¡til, pesos/config): PCM (Sbâ‚‚Sâ‚ƒ) multinivel, retenciÃ³n larga. OMCC: arbitraje, DMA, coherencia, RAS.
```
Capacidades/latencias dependientes de tecnologÃ­a y validaciÃ³n; ver `hardware/optical-memory-hierarchy-l1l2l3.md`.

## 7. ElectrÃ³nica de borde, PCIe y compatibilidad OpenCL/OpenVINO
- **PCIe:** Endpoint (Gen4/5 x8/x16 objetivo), BARs (control/estado/colas/doorbells), DMA descriptor-based, MSI/MSI-X, resets/telemetrÃ­a.
- **Cadena:** SerDes/PHY host â†” bridge/FPGA/ASIC â†” moduladores lÃ¡ser/ drivers (E/O) y TIA/ADC/fotodetectores (O/E).
- **Software:** KMD (colas, memoria, interrupciones) + UMD/ICD OpenCL (platform/device/queue/buffer/kernel NDRange) + compilador/ lowering de kernels soportados; rutas OpenVINO: plugin nativo EP, backend OpenCL del dispositivo, o particiÃ³n heterogÃ©nea CPU/GPU/NPU + fallback.
- **Potencia/SI-PI/tÃ©rmica:** PDN con regulaciÃ³n para Ã³ptica/drivers, integridad de seÃ±al SerDes, sensores y control tÃ©rmico (operaciÃ³n dentro de mÃ¡rgenes de fase/retenciÃ³n). Detalle en `hardware/pcie-bridge-opencl-openvino.md`.

## 8. Dimensiones fabricables, tÃ©rmica y fiabilidad (orientativo, simulado)
- Escala de features guiada por confinamiento/interferencia ($\sim\lambda/2n$, $\lambda/4n$, longitud de interacciÃ³n); tiles/celdas y pitch con guardas de crosstalk, alineaciÃ³n y redundancia (spares) segÃºn `hardware/manufacturable-dimensions-and-ai-accelerators.md` y `hardware/min-dimensions-analysis.md`.
- TÃ©rmica: presupuestos de potencia por escritura PCM/VOâ‚‚, aislamiento y extracciÃ³n de calor; secuenciaciÃ³n para limitar diafonÃ­a.
- Fiabilidad (P1â€“P3): niveles PCM multinivel, ruido/precisiÃ³n efectiva, endurance/retenciÃ³n, variabilidad espacial y polÃ­tica 4b/5b + refresco M2 (datos en `outputs/*p1*`, `*reliability_p2*`, `*p3*`).

## 9. Simulaciones de viabilidad (S1â€“S4, conceptuales)
- **S1 (enlace/tÃ©rmico):** mÃ¡rgenes de fase/pÃ©rdida y ventana tÃ©rmica (`model_s1_link_thermal.py`, `outputs/s1_link_thermal.*`).
- **S2 (sistema):** perfiles M0â€“M3/OMCC y throughput/latencia (`simulate_opgpu_system.py`, `outputs/opgpu_system_*`).
- **S3 (PCIe/OpenVINO):** latencia extremo-a-extremo y cobertura de operadores/rutas (`model_s3_pcie_openvino.py`, `outputs/s3_pcie_*`).
- **S4 (variabilidad/yield):** Monte Carlo de variaciÃ³n y yield relativo (`model_s4_variability_yield.py`, `outputs/s4_variability_yield.*`).
- Roadmap: `FEASIBILITY_SIMULATION_ROADMAP.md` (S1â€“S4 antes de E1â€“E4). Resultados no son mediciones.

## 10. Variantes, instrucciones de reproducciÃ³n y uso
- Variantes: barridos de $n,d,\lambda$, niveles PCM, WDM por canal, particiÃ³n M0â€“M3, tamaÃ±o de tile, topologÃ­as (malla/MZI, resonante, Fâ€“P, difractiva), y particiÃ³n heterogÃ©nea OpenVINO.
- ReproducciÃ³n: Python 3.10+ (`numpy`, `matplotlib`); ejecutar `run_simulations.py`, `simulate_opgpu_system.py`, `model_feasibility_roadmap.py`, `model_s1_link_thermal.py`, `model_s3_pcie_openvino.py`, `model_s4_variability_yield.py`, `objective_combo_analysis.py`, etc. (ver `README.md`).
- Seguridad: lÃ¡seres UV/visible/NIR y gradientes tÃ©rmicos localizados (PCM) requieren controles de seguridad y cumplimiento en cualquier prototipo.

## 11. DeclaraciÃ³n de dominio pÃºblico y defensiva
Los titulares declaran la intenciÃ³n de dedicar las obras originales aquÃ­ descritas al **dominio pÃºblico (CC0 1.0)** y publicarlas como **arte previo/divulgaciÃ³n defensiva** para impedir, en la medida de lo posible, la apropiaciÃ³n registral por terceros y permitir fabricaciÃ³n/uso libre por cualquiera. Esta divulgaciÃ³n se realiza de buena fe, con fecha verificable y contenido habilitante. No constituye licencia de patente, garantÃ­a, ni asesorÃ­a legal.

