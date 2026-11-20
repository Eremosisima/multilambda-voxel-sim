# Esquemáticos e instrucciones — Estrategias actuales OPGPU (v0.8)

> **Estado:** documento de referencia conceptual (v0.8). Integra las estrategias actuales: familias **A–G**, combinaciones **H1–H5**, priorización **H3, G2, G3, H1, H4**, dimensiones mínimas fabricables con **control térmico factible**, jerarquía/memoria óptica **M0–M3/OMCC**, e interfaces modulares para **aislamiento C&D**.  
> **Dominio público (objetivo declarado):** esquemáticos e instrucciones destinados a **uso libre por todo el mundo**. Se publican como **arte previo/divulgación defensiva** para dificultar que terceros los registren o patenten como propios (ver `PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta; la dedicación efectiva CC0 1.0 requiere los ajustes indicados por los titulares).  
> **Avisos:** no es un diseño listo para fabricación/certificación (PCIe/OpenCL nominativos). Simulaciones y estimaciones son conceptuales, no mediciones. No garantiza FTO ni precios; consultar FTO antes de fabricar/comercializar. Requiere validación óptica, térmica 3D, SI/PI, seguridad láser (~300 °C local en Sb₂S₃, 365–800 nm) y cumplimiento.

## 1. Visión de sistema y estrategia de plataforma

```text
+-----------------------------------------------------------------------------------+
| HOST: CPU + OpenCL Runtime/Driver + Memoria del sistema                           |
+---------------------------------------+-------------------------------------------+
                                        | PCIe (x16, Gen4/5 objetivo, nominativo)
+---------------------------------------v-------------------------------------------+
| TARJETA (BORDE ELECTRÓNICO MÍNIMO)                                                |
| [Edge/Retimers/SI] -> [PCIe EP + DMA + BAR0/CSRs + MSI/MSI-X + Cmd Processor]     |
|                         |                                                         |
|                [E/O TX: drivers+láseres+mod]   [O/E RX: PD/TIA/ADC+sincro]       |
|                         \                       /                                 |
|                          \                     /    [Gestión potencia/térmica pkg] |
+---------------------------\-------------------/-----------------------------------+
                             \                 /
                   [OMCC: coherencia M0-M3, DMA/prefetch, colas/eventos,
                    arbitraje, calibración, RAS/ECC, scheduling térmico]
                             \                 /
+-----------------------------v---------------v-------------------------------------+
| PLANO FOTÓNICO (MÓDULO ELEGIDO / CANDIDATO INTERCAMBIABLE)                       |
|  Núcleo(s): cómputo por interferencia + WDM + (opcional) NV/3D                    |
|  Jerarquía: M0 registros/buffers | M1 pesos/estado | M2 estado volátil/caché      |
|             M3 memoria óptica densa | buffers/cavidades (retención temporal)       |
|  Interfaz de módulo: óptica (guías/fibras) + control/térmico + alimentación      |
+-----------------------------------------------------------------------------------+
```

**Estrategias actuales (resumen):**
- **Plataforma abierta y modular:** núcleo de referencia A1 + variantes/combos seleccionables por objetivos; repos/candidatos independientes para aislamiento ante C&D.
- **Fabricabilidad primero en térmica:** dimensionado por control térmico factible (micro-calentadores, trincheras, spreading, TEC/estabilización, secuenciado OMCC), no solo por óptica teórica.
- **Jerarquía óptica gestionada:** M0–M3/OMCC para pesos estacionarios, caché volátil, buffers y movimiento de datos con mínimos cruces E/O–O/E.
- **Priorización de candidatos:** **H3** (abierto/factible), **G2** (velocidad/capacidad), **G3** (NV+velocidad equilibrado), **H1** (NV volumétrico), **H4** (techo capacidad, alto riesgo/integración).

## 2. Familias A–G y combinaciones H1–H5 (esquemático lógico)

| Familia | Mecanismo (interferencia/estado) | Reconfig. | Estado | Rol típico |
|---|---|---|---|---|
| **A** | MZI/PCM (fase por Δn, Sb₂S₃/VO₂/fotoquímicos) | lenta-media | NV/parcial | Pesos/MVM, referencia |
| **B** | Resonante/WDM (rings, BIC, F–P selectivo) | media | sintonizable | Densidad espectral/canales |
| **C** | Electro-óptica (Pockels/índice rápido) | ps–ns | volátil | Conmutación/ajuste rápido |
| **D** | Plasmónica/ENZ/no lineal localizada | rápida | volátil | Activaciones/hotspots (opcional) |
| **E** | Todo-óptico no lineal | rápida | volátil | Funciones no lineales (emergente) |
| **F** | Difractiva/metasuperficie/3D | fija-media | pasiva/semi | Mezcla global, tensor/volumen |
| **G** | Membranas película delgada/F–P ($n·d$, interferencia de espesor) | pasiva–ns | pasiva/NV/EO | WDM vertical, filtrado, núcleos densos |

| Combo | Composición | Objetivo | Vel. | Cap. | Dens. | Fiab. | Feasib. | Precio | Rol estratégico |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **H1** | A1+G3+3D | NV volumétrico | media-alta | muy alta | muy alta | media | media | medio-alto | **P1** (escalado NV) |
| **H2** | G2+B3+C1 | Núcleo RT dinámico | muy alta | alta (NV baja) | alta | media-alta* | media-baja | alto | Alto rendimiento dinámico |
| **H3** | A1+G1+B3 | Abierto/WDM-PCM | media | media-alta | buena | media | **alta** | **bajo-medio** | **P1** (factible/accesible) |
| **H4** | G2/G3+F2+A1 | Tensor volumétrico | alta | **máxima** | alta | media | baja-media | alto | **P1** (techo capacidad) |
| **H5** | B1+G3(+D1) | Stack resonante denso | media-alta | alta | muy alta (área) | media-baja | baja | medio-alto | Exploratorio compacto |

\*Con control térmico/fase y calibración (OMCC). Valores conceptuales.

## 3. Esquemáticos por estrategia priorizada (bloques e interfaces)

### 3.1 H3 — Open WDM-PCM (prioridad: abierto/factible, P1)
```text
[Entrada WDM óptica] -> [G1: apilado pasivo λ/4n SiN/SiO2/TiO2, filtros/canales]
      -> [B3: banco microrings sintonizables + estabilización térmica/resonancia]
      -> [A1: malla MZI (guías de polímeros) + pesos PCM polymérico (diaryleténico/spiropirano, NV; programación óptica/térmica, calibración)
      -> [O/E o salida óptica]
Control: OMCC (carga pesos PCM, tuning rings, secuenciado térmico, calibración)
Térmica: calentadores localizados PCM + trincheras + spreader + TEC paquete; rings estabilizados
Interfaces modulares: [G1] <-> [B3] <-> [A1] desacoplables (óptico/ctrl/térmico)
```
- **Por qué H3:** pasivos dieléctricos conocidos + referencia A1, menor dependencia EO/RF sensible, buen perfil open/FTO relativo.
- **Fabricable (celda ref.):** ~22×79 µm pitch/long., vert. ~19.7 µm, área ~1738 µm², vol. ~34218 µm³ (con control térmico).

### 3.2 G2 — Membrana/F–P EO (prioridad: velocidad/capacidad, P1)
```text
[Entrada] -> [Cavidad/membrana multicapa dieléctrica] --(campo EO, ej. TFLN/BTO)--> [Δn -> Δ(n·d)]
      -> [Interferencia constructiva/destructiva por λ/canal] -> [Salida/WDM]
Control: drivers EO rápidos, estabilización de paquete, calibración de fase
Térmica: carga de electrodos/RF gestionada por spreading; sin escritura PCM de 300°C
Interfaces modulares: pila óptica | bloque EO/driver (sustituible) | control
```
- **Por qué G2:** reconfiguración ps–ns, alta BW/densidad, top overall conceptual; dependencia EO → aislar.
- **Fabricable:** ~11×16 µm, vert. ~6.69 µm, área ~176 µm², vol. ~1177 µm³.

### 3.3 G3 — Membrana PCM+EO híbrida (prioridad: NV+velocidad, P1)
```text
[Entrada] -> [Multicapa + capa PCM Sb2S3 (estado NV por Δn)] -> [Ajuste EO fino/rápido]
      -> [Selección espectral n·d] -> [Salida]
Control: escritura PCM (pulsada, OMCC) + tuning EO
Térmica: micro-calentadores localizados + trincheras + spreading (aislamiento escritura 300°C)
Interfaces modulares: pila dieléctrica | sub-bloque PCM | sub-bloque EO (sustituibles)
```
- **Por qué G3:** persistencia NV con ajuste rápido; equilibrio densidad/robustez conceptual.
- **Fabricable:** ~13×23 µm, vert. ~7.19 µm, área ~299 µm², vol. ~2149 µm³.

### 3.4 H1 — Membrane-Brush NV 3D (prioridad: capacidad volumétrica NV, P1)
```text
            (cerda/brush 3D, apilado axial)
[Entrada/láser] -> [segmento G3: membrana PCM+EO] -> [vóxel A1/PCM] -> ... (N segmentos)
                              | 45°/guía        | aislamiento axial 12 µm
                           [salida/reflexión]  [M1/M3 locales]
Control: OMCC (direccionamiento vóxel, pesos, secuenciado térmico 3D, RAS)
Térmica: calentadores segmentados, aislamiento vert./lat., spreader/manifold; secuencia estricta
Interfaces modulares: segmento óptico | actuador térmico/EO | plano de interconexión
```
- **Por qué H1:** alta capacidad NV volumétrica y huella por función reducida; complejidad 3D/yield/térmica.
- **Fabricable:** pitch ~22 µm, altura ~110.8 µm, área huella ~484 µm², vol. ~53604 µm³ (por elemento/cerda).

### 3.5 H4 — Volumetric Tensor Membrane (prioridad: techo de capacidad, P1)
```text
[Entradas WDM/tensor] -> [Cores G2/G3 3D: cómputo local n·d/EO-PCM]
      -> [Plano F2 difractivo/metasuperficie: mezcla global/interferencia espacial]
      -> [Bloques A1: pesos NV selectivos] -> [Salidas]
Control: drivers EO + escritura PCM + calibración de fase/alineación; estabilización activa
Térmica: calentadores/drivers distribuidos, enfriamiento de alta capacidad, spreading/manifold
Interfaces modulares: core membrana | plano difractivo | plano A1 (sustituibles/retirables)
```
- **Por qué H4:** máximo throughput/capacidad conceptual (TOPS/MB/BW); mayor carga de integración, térmica y riesgo FTO.
- **Fabricable:** pitch ~20 µm, altura ~118.1 µm, área ~400 µm², vol. ~47251 µm³.

## 4. Jerarquía de memoria óptica y mapeo (M0–M3/OMCC)

```text
M0  Registros/colas/buffers inmediatos  -> retención temporal (cavidades/rings/F-P) + latches volátiles
M1  Pesos/estado de trabajo (estacionarios) -> PCM/NV (Sb2S3) o estado persistente equivalente
M2  Caché/estado volátil -> VO2/elementos volátiles, refresco gestionado
M3  Memoria/capacidad densa -> apilados/membranas/WDM, NV donde aplique
Buffers "tipo capacitor óptico" = retención temporal de luz/energía en resonadores; != almacenamiento de carga
OMCC: acceso directo/compartido a M0-M3, DMA/prefetch, coherencia, arbitraje, RAS/ECC, calibración, scheduling térmico
```

| Capa | Función | Tecnologías típicas | Retención | Control |
|---|---|---|---|---|
| M0 | Registros, colas, staging | cavidad/ring/F–P, VO₂ | ns–µs / volátil | OMCC, timing |
| M1 | Pesos/kernel estacionarios | PCM (Sb₂S₃), fotoquímicos | NV | carga/verificación OMCC |
| M2 | Caché/estado intermedio | VO₂, buffers resonantes | volátil (refresco) | OMCC refresco/scheduling |
| M3 | Capacidad/datos densos | membranas apiladas/WDM/3D | NV o pasiva | DMA/prefetch OMCC |

Ver `hardware/optical-memory-hierarchy-l1l2l3.md`.

## 5. Dimensiones fabricables y control térmico factible

**Principio:** el límite práctico lo imponen calentadores/contactos, aislamiento (PCM ~300 °C vs VO₂ 68 °C), registro/alineación 3D, ruteo y enfriamiento, no solo λ/2n o λ/4n.

| Propuesta | Pitch lat (µm) | Long. (µm) | Vert. (µm) | Área (µm²) | Vol. (µm³) | Control térmico factible |
|---|---:|---:|---:|---:|---:|---|
| A1 | 20 | 45.0 | 16.0 | 900 | 14,400 | Micro-calentadores, trincheras, spreader, sensado, escritura pulsada OMCC |
| B3 | 28 | 44.0 | 6.0 | 1,232 | 7,392 | Tuning termo-óptico/EO, TEC/sustrato, bloqueo resonancia |
| G1 | 7.0 | 7.0 | 5.69 | 49 | 279 | Estabilización de paquete (pasivo, sin 300 °C) |
| G2 | 11.0 | 16.0 | 6.69 | 176 | 1,177 | Spreading de carga EO/RF, estabilización |
| G3 | 13.0 | 23.0 | 7.19 | 299 | 2,149 | Calentadores localizados PCM + trincheras + spreading + presupuesto EO |
| H3 | 22 | 79.0 | 19.69 | 1,738 | 34,218 | PCM heaters + tuning anillos + TEC/spreader; planificación OMCC |
| H1 | 22 | 22 | 110.75 | 484 | 53,604 | Calentadores segmentados, aislamiento 3D, spreader/manifold, secuenciado |
| H4 | 20 | 20 | 118.13 | 400 | 47,251 | Calentamiento/drivers distribuidos, enfriamiento alta capacidad, estabilización activa |

**Reglas de diseño térmico (instrucciones):**
1. Mantener margen VO₂ < 68 °C mediante aislamiento, trenched regions y separación axial/lateral.
2. Escritura PCM (Sb₂S₃ ~300 °C) solo en pulsos localizados y calendarizados por OMCC; nunca continua en celdas adyacentes sin ventana térmica.
3. Incluir heat spreading y ruta a disipador/interfaz de enfriamiento de módulo; validar con modelo térmico 3D.
4. Proveer sensado/calibración térmica y lazos de control (especialmente B3/G2/H2/H4).
5. Presupuestar overhead de empaquetado/térmica (volumen/área) desde la fase de arquitectura.

Ver `hardware/manufacturable-dimensions-and-ai-accelerators.md` y `outputs/manufacturable_dimensions.*`.

## 6. Interfaces modulares y aislamiento C&D (instrucciones de proyecto)

**Objetivo:** un bloqueo/C&D o retiro de un candidato/bloque no debe detener al resto.

```text
[Repo/candidato X] -- interfaz óptica/eléctrica/térmica/control documentada -- [Repo/candidato Y]
         |                                                                              |
   BOM/diseño propio                                                             BOM/diseño propio
   licencias/NOTICE                                                              licencias/NOTICE
   historial/DOI propio                                                          historial/DOI propio
```

**Interfaces a definir por candidato (contratos abiertos):**
- **Óptica:** longitud(es) de onda, puertos/mode-field, pérdidas/presupuesto, polarización, conectores/acoplos.
- **Eléctrica/control:** señales de driver, timing, registro/mapa OMCC, telemetría.
- **Térmica:** mapa de potencia, Tmáx por zona, puntos de sensado y ruta de extracción.
- **Datos/protocolo:** formato de tensores/pesos, comandos de configuración y calibración.

**Instrucciones operativas:**
1. Mantener cada candidato autocontenido (README, DESIGN, IP_AND_OPEN_HW, licencias, NOTICE, datos propios) y versionado independiente.
2. Declarar bloques sensibles (EO, resonador, ENZ/difractivo, material) y **alternativas sustituibles**.
3. No afirmar “libre de patentes”; publicar procedencia/fechas y recomendar FTO antes de fabricar/comercializar.
4. Ante posible C&D: pausar/retirar/ajustar solo el repo/bloque afectado, preservando evidencia; continuar los demás.
5. Priorizar publicación/avance en **H3, G2, G3, H1, H4** según perfil de riesgo/valor.

Ver `CANDIDATE_REPOS_STRATEGY.md` y `candidates/`.

## 7. Instrucciones de implementación y validación (estrategia actual)

1. **Seleccionar candidato/escenario:** H3 (acceso/factible), G2 (RT/velocidad), G3 (NV+ajuste), H1 (NV volumétrico), H4 (capacidad máxima) según restricciones de coste, FTO, térmica y madurez.
2. **Cerrar presupuesto físico:** óptico (pérdidas, fase, IL), térmico (peores casos 300 °C/68 °C, spreading/enfriamiento), eléctrico (drivers/energía), y de dimensiones fabricables (DRC de proceso objetivo).
3. **Modelar antes de fabricar:** FDTD/EM para guías/resonadores/membranas ($n·d$, MZI), FEM térmico 3D transitorio, y simulación de sistema (PCIe/OpenCL/OMCC, colas, BW).
4. **Prototipar por etapas (modular):** G1/pasivos → A1/B3 → integración EO/PCM → apilado 3D; validar interfaz por interfaz.
5. **Calibrar y operar:** tablas de fase/potencia por λ/temperatura, RAS/ECC, políticas de refresco M2, y scheduling térmico en OMCC.
6. **Cumplimiento y seguridad:** láser (clase/encapsulado), térmica, EMC/SI-PI en borde eléctrico; pruebas formales para cualquier reclamo PCIe/OpenCL.
7. **Publicar abiertamente:** fuentes editables, parámetros, scripts y resultados reproducibles bajo CERN-OHL-S v2 / Apache-2.0 / CC BY-SA 4.0 con procedencia.

## 8. Referencias internas

- `hardware/families-and-variants.md`, `hardware/family-combinations-openhw.md` (A–G, H1–H5)
- `hardware/manufacturable-dimensions-and-ai-accelerators.md`, `outputs/manufacturable_dimensions.*` (fabricable/térmica)
- `hardware/min-dimensions-analysis.md`, `outputs/min_dimensions.*` (teórico + handicap)
- `hardware/optical-memory-hierarchy-l1l2l3.md` (M0–M3/OMCC)
- `hardware/opencl-compatibility.md`, `hardware/open-photonic-gpu-v1-schematic-pcie.md`, `hardware/schematics-deep-dive.md` (interfaz/borde/detalle)
- `CANDIDATE_REPOS_STRATEGY.md`, `candidates/` (priorización y aislamiento)
- `outputs/objective_combo_analysis.md`, `outputs/families_dev_comparison.md` (comparativas)


## OEM Thermal Immersion Stabilizer (OEM)

El módulo fotónico puede sumergirse en tanques de inmersión térmicos opcionales:

**Fluidos recomendados** (por transparente a 650 nm y 1530–1565 nm + polímeros):
1. **Novec 7100/7200 (3M):** dieléctricos, transparentes en visible/NIR, baja viscosidad (~0.9–1.2 cP), ~0.5–0.7 W/mK.
2. **Agua desiacturred con inhibidores:** transparente en 650 nm (PCM write); no sirve para datos 1550 nm (alto absorción).
3. **Aceites de silicona fluidos:** transparentes, Δn ≈ 0.02–0.08.

**Control térmico:** ±0.1–0.5 °C; recirculación con bomba; sensores PTC/TC; enfriamiento por radiadores/tablero; calibration por bloque.

**Implicación para polímeros:** polímeros abiertos (PMMA, PS, Zeonex, Topas, fluorocarbohidratos) son dieléctricos; verificar compatibilidad con el fluido de inmersión antes de diseñar conexiones.

**Herramientas útiles:** Meep (FDTD, GPL), gdstk (GDSII, BSL-1.0), Simphony (alternativa).


## Bit-Slicing Óptico WDM (IA precision)
El sistema soporta compuertas ópticas ternarias (MZI+PCM) combinadas por canales WDM con ganancias calibradas beta_i = 2^i*beta_0 -> ejecutar IA de alta precision (INT8/FP16) con memorias ternarias simples. Ver `hardware/OPGPU_BITSLICING_WDM_OPTICO.md`.


## OEM Brush with Integrated Coolant Channels and Temperature Control (OEM Brush)

The H1 brush (Membrane-Brush NV 3D) integrates an OEM-scale cooling and thermal control system:

**Microfluidic through-vias for coolant flow:**
- Vertical canals inside the segments (Ø 5–8 µm, 10–25 µm spacing) forming a per-segment channel network from face to back.
- Interconnection plane between segments: continuous wider channels (5–8 µm) for manifolds.
- 2–4 inlet/outlet micro-ports (Ø 0.5–1 mm, with micro-valves) at the back face or brush ends, near the fiber connector.
- Coolant: same fluids as the OEM Thermal Immersion Stabilizer (Novec 7100/7200, etc.).

**Temperature control (per segment):**
- Segmented micro-heaters (PTC/Kapton) with 200 nm gap over PCM for efficient writing (PID).
- Integrated thermistors/RTDs (3–5 per segment) for feedback.
- Optional TEC/PTC coolers near the PCM layer for sub-30°C writing (ΔT margins vs VO2 68 °C).
- Thermal barriers: 12 µm axial gaps (as H1) + lateral barriers (ΔT < 2 °C between segments).

**Control architecture:**
- OMCC extension: thermal telemetry (T_i per segment), heater duty cycles, coolant flow rate, write scheduling (extended OMCC protocol per ARQUITECTURA).
- PID per segment: T_target from OEM Thermal Immersion Stabilizer profiles; feedback from integrated thermistors.

**Verification (design-level):**
- CFD of micro-channels: pressure drop, flow velocity.
- IR thermography: ΔT mapping between segments during write/read cycles.
- PCM retention test: continuous coolant flow at T_target.

**Notes:** margins respect VO2 threshold (68 °C) for buffers and PCM write ≤ 300 °C transient per OEM Thermal Immersion Stabilizer.
