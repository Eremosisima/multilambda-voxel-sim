# Divulgación defensiva / arte previo — OPGPU v0.8 (consolidada)

- **Título:** Open Photonic GPU (OPGPU) — Estrategias, esquemáticos, instrucciones y diseño de memoria/cómputo fotónico (A–G, H1–H5, M0–M3/OMCC, PCIe/OpenCL/OpenVINO)
- **Versión/estado:** v0.8.0-research (conceptual/simulado), commit `cd58339` (base `ed4b8fe`), [FECHA]: ____  
- **Autores/titulares (derechos sobre la obra original):** [COMPLETAR: nombres, ORCID/afiliación, consentimiento de dedicación] / “Open Photonic GPU contributors” (provisional)  
- **Repositorio fuente:** https://github.com/Eremosisima/multilambda-voxel-sim (`open-photonic-gpu/`)  
- **Identificadores:** Concept DOI [ ], DOI versión [ ], ip.com ID [ ], Wayback [ ]
- **Licencia/dedicación:** Objetivo **dominio público (CC0 1.0)** para uso libre universal y **divulgación defensiva/arte previo** de lo divulgado, en la medida permitida por la ley y sujeto a consentimiento de titulares. Estado vigente del snapshot: licencias mixtas (Apache-2.0 código, CERN-OHL-S v2 hardware, CC BY-SA 4.0 docs) hasta transición (ver `PUBLIC_DOMAIN_DEDICATION.md`). Sin garantía; sin FTO; marcas nominativas.

## 1. Propósito y naturaleza de la divulgación
Divulgación técnica **habilitante** y pública de arquitecturas, estrategias, esquemáticos, instrucciones, parámetros, variantes y resultados de simulación de una unidad de cómputo/memoria predominantemente óptica (OPGPU), con interfaz PCIe y compatibilidad OpenCL/OpenVINO. Se publica para: (a) permitir uso, estudio, fabricación y mejora por cualquier persona, y (b) constituir **arte previo** que dificulte la apropiación registral/patentamiento por terceros de lo aquí descrito. **No** es un dispositivo fabricado ni validado experimentalmente.

## 2. Principio de funcionamiento (resumen habilitante)
- **Cómputo óptico:** operaciones tipo MVM/MAC y tensores mediante interferencia constructiva/destructiva coherente ($E_{out}\propto E_1 \pm E_2 e^{i\Delta\phi}$), modulando amplitud/fase/polarización/longitud de onda (MZI, mallas, resonadores, película delgada/F–P, difracción/metasuperficies).
- **Memoria/estado óptico:** pesos/estado en PCM (p.ej. Sb₂S₃, no volátil, multinivel), conmutación/buffer rápido (p.ej. VO₂), elementos fotoquímicos/sintonía (azobenceno, espiropirano) y almacenamiento/retardo por resonancia/cavidades/anillos/F–P (M0–M3).
- **Modos:** GPU (MVM paralelo general), NPU (inferencia, pesos estacionarios, activaciones), TPU-like (GEMM/sistólico/tensorial por bloques).
- **Interfaz:** host PCIe (EP) + DMA/BAR/CSRs + command processor + cadena E/O–O/E; exposición como acelerador tipo OpenCL y rutas de ejecución OpenVINO (plugin nativo, vía backend OpenCL, heterogéneo/fallback).
- **Gestión:** coprocesador OMCC con acceso/arbitraje a memoria óptica (M0–M3), colas, calibración/RAS.

## 3. Arquitectura de sistema y esquemático (nivel plataforma)

```text
HOST (CPU) ── PCIe Gen4/5 x8/x16 ── [EP PCIe + DMA/Bridge + BAR/CSRs + Cmd Processor + OMCC]
                                              │ control/config/colas        │ datos
                                       [TX: SerDes→modulación E/O (λ/WDM)]
                                              │  guías/fibras  (dominio óptico)
        ┌────────────────────────  PLANO FOTÓNICO INTERCAMBIABLE  ────────────────────────┐
        │  Red WDM/broadcast + Malla/tiles de cómputo (A–G / H1–H5) + Memoria M0–M3       │
        │  Control térmico/bias/actuación + sensado/telemetría                             │
        └──────────────────────────────────────────┬───────────────────────────────────────┘
                                              │  guías/fibras
                                       [RX: fotodetección O/E→ADC/TIA→buffers]
                                              │ DMA/IRQ/eventos → HOST
```

Interfaz de módulo: óptica (guías/fibras/acopladores), control/térmico, alimentación. Plano fotónico sustituible por candidato (aislamiento modular).

## 4. Estrategias y familias (A–G) y combinaciones (H1–H5)

**Familias base (principio):** A1 MZI/PCM no volátil (pesos por fase), A2 MZI termo-óptico, B1/B3 resonadores/anillos (WDM, densidad), C1 fotoquímico, D1/D2 VO₂/plasmónico (conmutación rápida), E1 redes coherentes/MZI-mesh, F1/F2 difractiva/metasuperficie, G1/G2/G3 membranas/cavidades de película delgada (F–P, interferencia por espesor óptico $n\cdot d$, variantes pasiva/EO/PCM+EO).

**Combinaciones candidatas:** H1 Membrane-Brush NV (A1+G3+3D, capacidad NV volumétrica), H2 RT Membrane-WDM (G2+B3+D1, reconfiguración rápida), H3 Open WDM-PCM (A1+G1+B3, abierto/factible), H4 Volumetric Tensor Membrane (G2/G3+F2+A1, techo capacidad, alto riesgo), H5 Dense Resonant Stack (G1+B1, pasivo denso).

**Priorizadas (P1):** H3 (abierto/factible), G2 (velocidad/BW), G3 (NV+velocidad), H1 (escalado NV 3D), H4 (techo capacidad, aislar).

## 5. Esquemáticos por candidato priorizado (bloques e instrucciones)

### H3 — Open WDM-PCM (A1 + G1 + B3)
```text
λ1..λn ─ MUX/WDM ─┬─ banco microrings/filtros (B3, selectivo) ─┐
                  └─ celdas MZI-PCM Sb₂S₃ (A1, peso/retención) ─┤─ combinador ─ PD/TIA (O/E)
Filtros/membranas pasivas de espesor fijo (G1, n·d) proveen selección/estabilización.
Control: escritura PCM (pulsos), sesgo térmico, calibración; lectura coherente.
```
Instrucciones: calibrar mapa fase-peso PCM multinivel; operar pesos estacionarios NV; priorizar procesos dieléctricos pasivos; aislamiento C&D por módulo.

### G2 — Membrana EO rápida (G2, F–P apilada sintonizada por índice EO)
```text
Entrada óptica/WDM → pila de membranas/cavidades F–P (espesor d, n ajustable por EO)
                  → interferencia selectiva (constructiva/destructiva por n·d, λ)
                  → salida/PD. Driver EO + control de fase por canal.
```
Instrucciones: definir apilado (d,n) por canal, bias EO, gestión térmica/RF, desacoplar driver EO como bloque sustituible.

### G3 — Membrana PCM+EO híbrida
```text
Entrada → cavidades F–P (n·d): capa/estado base PCM (NV) + ajuste fino EO (rápido) → salida/PD.
Modos: base NV (PCM) + reconfiguración dinámica (EO); control térmico para PCM.
```
Instrucciones: particionar estado NV (PCM) vs ajuste EO; secuenciar escritura PCM para limitar crosstalk térmico.

### H1 — Membrane-Brush NV 3D (A1 + G3 + cepillo)
```text
       ┌─ capa membrana G3 (canales por n·d) ─┐
λ/WDM ─┼─ capa MZI-PCM A1 (pesos NV)        ├─ apilado 3D tipo cepillo/cerdas ─ vías ópticas ─ O/E
       └─ capa(s) repetidas, partición térmica ┘
```
Instrucciones: partición térmica entre capas, pitch/guardas de crosstalk, redundancia (spares) y calibración por plano.

### H4 — Volumetric Tensor Membrane (G2/G3 + F2 + A1)
```text
Entrada → apilado 3D de membranas (G2/G3) → etapa difractiva/metasuperficie F2 (mezcla global)
       → celdas A1 PCM donde convenga (NV) → salida/PD. Integración/alineación 3D estricta.
```
Instrucciones: tratar como candidato de alto riesgo; aislar completamente; validar alineación, pérdidas y yield antes de escalar.

## 6. Jerarquía de memoria óptica y mapeo (M0–M3/OMCC)
```text
M0 (análogo/estado inmediato, ps–ns): coherencia/campo en guías, retardo/resonancia.
M1 (buffer rápido, ns–µs): cavidades/anillos, VO₂/latches ópticos, “capacitores ópticos” como retención temporal.
M2 (working set, µs–ms, volatilidad media): estados conmutables (VO₂/fotoquímicos) y buffers resonantes.
M3 (no volátil, pesos/config): PCM (Sb₂S₃) multinivel, retención larga. OMCC: arbitraje, DMA, coherencia, RAS.
```
Capacidades/latencias dependientes de tecnología y validación; ver `hardware/optical-memory-hierarchy-l1l2l3.md`.

## 7. Electrónica de borde, PCIe y compatibilidad OpenCL/OpenVINO
- **PCIe:** Endpoint (Gen4/5 x8/x16 objetivo), BARs (control/estado/colas/doorbells), DMA descriptor-based, MSI/MSI-X, resets/telemetría.
- **Cadena:** SerDes/PHY host ↔ bridge/FPGA/ASIC ↔ moduladores láser/ drivers (E/O) y TIA/ADC/fotodetectores (O/E).
- **Software:** KMD (colas, memoria, interrupciones) + UMD/ICD OpenCL (platform/device/queue/buffer/kernel NDRange) + compilador/ lowering de kernels soportados; rutas OpenVINO: plugin nativo EP, backend OpenCL del dispositivo, o partición heterogénea CPU/GPU/NPU + fallback.
- **Potencia/SI-PI/térmica:** PDN con regulación para óptica/drivers, integridad de señal SerDes, sensores y control térmico (operación dentro de márgenes de fase/retención). Detalle en `hardware/pcie-bridge-opencl-openvino.md`.

## 8. Dimensiones fabricables, térmica y fiabilidad (orientativo, simulado)
- Escala de features guiada por confinamiento/interferencia ($\sim\lambda/2n$, $\lambda/4n$, longitud de interacción); tiles/celdas y pitch con guardas de crosstalk, alineación y redundancia (spares) según `hardware/manufacturable-dimensions-and-ai-accelerators.md` y `hardware/min-dimensions-analysis.md`.
- Térmica: presupuestos de potencia por escritura PCM/VO₂, aislamiento y extracción de calor; secuenciación para limitar diafonía.
- Fiabilidad (P1–P3): niveles PCM multinivel, ruido/precisión efectiva, endurance/retención, variabilidad espacial y política 4b/5b + refresco M2 (datos en `outputs/*p1*`, `*reliability_p2*`, `*p3*`).

## 9. Simulaciones de viabilidad (S1–S4, conceptuales)
- **S1 (enlace/térmico):** márgenes de fase/pérdida y ventana térmica (`model_s1_link_thermal.py`, `outputs/s1_link_thermal.*`).
- **S2 (sistema):** perfiles M0–M3/OMCC y throughput/latencia (`simulate_opgpu_system.py`, `outputs/opgpu_system_*`).
- **S3 (PCIe/OpenVINO):** latencia extremo-a-extremo y cobertura de operadores/rutas (`model_s3_pcie_openvino.py`, `outputs/s3_pcie_*`).
- **S4 (variabilidad/yield):** Monte Carlo de variación y yield relativo (`model_s4_variability_yield.py`, `outputs/s4_variability_yield.*`).
- Roadmap: `FEASIBILITY_SIMULATION_ROADMAP.md` (S1–S4 antes de E1–E4). Resultados no son mediciones.

## 10. Variantes, instrucciones de reproducción y uso
- Variantes: barridos de $n,d,\lambda$, niveles PCM, WDM por canal, partición M0–M3, tamaño de tile, topologías (malla/MZI, resonante, F–P, difractiva), y partición heterogénea OpenVINO.
- Reproducción: Python 3.10+ (`numpy`, `matplotlib`); ejecutar `run_simulations.py`, `simulate_opgpu_system.py`, `model_feasibility_roadmap.py`, `model_s1_link_thermal.py`, `model_s3_pcie_openvino.py`, `model_s4_variability_yield.py`, `objective_combo_analysis.py`, etc. (ver `README.md`).
- Seguridad: láseres UV/visible/NIR y gradientes térmicos localizados (PCM) requieren controles de seguridad y cumplimiento en cualquier prototipo.

## 11. Declaración de dominio público y defensiva
Los titulares declaran la intención de dedicar las obras originales aquí descritas al **dominio público (CC0 1.0)** y publicarlas como **arte previo/divulgación defensiva** para impedir, en la medida de lo posible, la apropiación registral por terceros y permitir fabricación/uso libre por cualquiera. Esta divulgación se realiza de buena fe, con fecha verificable y contenido habilitante. No constituye licencia de patente, garantía, ni asesoría legal.
