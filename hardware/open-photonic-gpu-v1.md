# Open Photonic GPU v0.2 (Concepto de Hardware Abierto, mayoritariamente óptico)

> **Estado:** Propuesta conceptual / prototipo de investigación (v0.2).  
> **Aviso:** Este documento describe una arquitectura de cómputo y memoria predominantemente fotónica. No es un diseño listo para fabricación. Requiere validación por simulación electromagnética/térmica y prototipado de fotónica integrada.

## 1. Objetivo

Definir una primera versión de una unidad de procesamiento paralelo **mayoritariamente óptica** (cómputo, enrutamiento y memoria) que utilice materiales conmutables para ejecutar operaciones tipo GPU, priorizando:

- **Cómputo óptico**: multiplicación matriz-vector (MVM), acumulación y enrutamiento de señales en el dominio fotónico.
- **Memoria óptica integrada**: almacenamiento de pesos, instrucciones/configuración y estados intermedios en elementos fotónicos (no volátiles y volátiles), minimizando buffers electrónicos.
- **Control óptico**: escritura, borrado y selección de rutas mediante estímulos ópticos en longitudes de onda dedicadas.
- **Plataforma abierta:** especificación, modelos y flujos de simulación publicables bajo licencias abiertas.

La electrónica se restringe a funciones de borde: alimentación, gestión térmica global, generación/modulación de fuentes láser y conversión electro-óptica/óptico-eléctrica únicamente en la interfaz con el host.

## 2. Materiales funcionales y rol en la arquitectura

| Compuesto | Estímulo de conmutación | Tipo de transición | Índice de refracción (estados) | Rol óptico propuesto |
|---|---|---|---|---|
| **Sb₂S₃** (trisulfuro de antimonio) | Óptico: 650 nm; Térmico: 300 °C | Cambio de fase amorfo ↔ cristalino | Amorfo: 2,70; Cristalino: 3,30 | **Memoria óptica no volátil** (pesos y almacenamiento persistente) y elementos de fase/atenuación programables en guías de onda. Alto contraste de índice para celdas multinivel (analógicas) en resonadores o tramos de guía. |
| **VO₂** (dióxido de vanadio) | Óptico: 800 nm; Térmico: 68 °C | Transición aislante ↔ metal (MIT) | Aislante: 2,50; Metal: 2,00 | **Conmutación y memoria óptica volátil rápida** (latches/buffers ópticos), compuertas de enrutamiento y elementos de umbral para control de flujo de señales. |
| **Azobenceno** | 365 nm (trans→cis); 450 nm (cis→trans) | Isomerización E/Z | Trans: 1,56; Cis: 1,54 | **Ajuste fino óptico** (trim) de fase/acoplamiento y elementos de retardo sintonizable para sincronización y calibración del plano fotónico. |
| **Espiropirano** | 365 nm (cerrado→abierto); 520 nm (abierto→cerrado) | Isomerización con ruptura de enlace C–O | Cerrado: 1,54; Abierto: 1,60 | **Memoria óptica reconfigurable** (registros de configuración, mapas de enrutamiento, bit-masks) y compuertas de acceso a bancos de memoria/cómputo. |

> **Nota:** Las longitudes de onda listadas son estímulos de conmutación. La(s) longitud(es) de onda de la señal de datos ($\lambda_s$) deben elegirse en bandas donde los materiales sean estables (sin escritura accidental) y con pérdidas aceptables, separadas espectralmente de los canales de control (650, 800, 365, 450, 520 nm).

## 3. Arquitectura de alto nivel (predominantemente óptica)

```text
+----------------------------------------------------------------------------------+
|                          Host (interfaz electro-óptica mínima)                  |
|                Serializador/Deserializador óptico  |  Gestión energía/térmica    |
+----------------------------------+-------------------------------+---------------+
                                   | $\lambda_{IO}$                |
                                   v                               v (control global)
+----------------------------------------------------------------------------------+
|                         PLANO FOTÓNICO INTEGRADO (PIC)                          |
|                                                                                  |
|  [Fuentes láser + buses ópticos] --$\lambda_s$--> [Codificación óptica de entrada]|
|                                                      (modulación por luz/VO2)     |
|                                                              |                    |
|                                                              v                    |
|   +----------------------- MEMORIA ÓPTICA JERÁRQUICA -------------------------+  |
|   | [Registros/config. ópticos: Espiropirano]  (mapas, máscaras, microcódigo)  |  |
|   | [Memoria no volátil: Sb2S3]                (pesos, kernels, constantes)    |  |
|   | [Buffers/latches volátiles: VO2]           (operandos, resultados parc.)    |  |
|   | [Líneas de retardo + ajuste: Azobenceno]   (sincronización/alineación)     |  |
|   +---------------------------+-------------------------------+-----------------+  |
|                               | pesos/operandos               | control           |
|                               v                               v                   |
|                    [NÚCLEO DE CÓMPUTO ÓPTICO MVM / CROSSBAR]                     |
|                    (guías + celdas Sb2S3 + conmutación VO2)                      |
|                               |                                                   |
|                               v                                                   |
|                [Red de enrutamiento óptico y compuertas]                          |
|                    (VO2 conmutación + Espiropirano selección)                     |
|                               |                                                   |
|                               v                                                   |
|              [Acumulación/realimentación óptica] -> [Salida óptica]              |
|                  (buffers VO2, realimentación)         hacia host $\lambda_{IO}$  |
+----------------------------------------------------------------------------------+
```

## 4. Subsistemas ópticos

### 4.1 Núcleo de cómputo óptico (Tensor/Matrix Core)
- **Topología:** malla de interferómetros Mach–Zehnder (MZI) o crossbar de guías de onda con acopladores direccionales.
- **Pesos:** cada celda de ponderación integra un parche de **Sb₂S₃** acoplado evanescentemente a la guía. El estado amorfo/cristalino (programado por pulsos a 650 nm o térmicos localizados a 300 °C) modifica el índice efectivo y, por tanto, la transmisión/fase, codificando el peso.
- **Operación:** un vector de entrada óptico $x$ (intensidades/fases en $\lambda_s$) se propaga por la red, donde es ponderado y combinado ópticamente para producir $y = W \cdot x$ (MVM) en el dominio fotónico.
- **No linealidad/umbral:** etapas basadas en **VO₂** (transición aislante↔metal, 800 nm / 68 °C) proporcionan conmutación dependiente de intensidad/estado para funciones de umbral, compuertas lógicas ópticas y control de saturación.

### 4.2 Jerarquía de memoria óptica (en chip)

| Nivel | Función | Material / mecanismo | Persistencia | Acceso típico |
|---|---|---|---|---|
| **M0 – Configuración** | Mapas de ruta, máscaras, selección de bancos, microconfiguración del núcleo | **Espiropirano** (cerrado/abierto, 365/520 nm, Δn=0,06) en celdas de conmutación/acoplamiento | No volátil (fotoestable entre escrituras) | Reconfiguración esporádica |
| **M1 – Memoria principal no volátil** | Pesos, kernels, matrices, constantes, tablas de búsqueda ópticas | **Sb₂S₃** (amorfo/cristalino, 650 nm, Δn=0,60) en arreglos de micro-resonadores o tramos de guía PCM | No volátil, alta retención | Lectura frecuente, escritura por lotes/kernels |
| **M2 – Memoria de trabajo volátil** | Operandos temporales, resultados parciales, buffers de pipeline, latches | **VO₂** (aislante/metal, 800 nm / 68 °C, Δn=0,50) en celdas biestables ópticas o interruptores con retención térmica controlada | Volátil (requiere mantenimiento de estado) | Lectura/escritura en tiempo de ejecución |
| **M3 – Sincronización/retardo** | Alineación temporal, buffers FIFO ópticos, compensación de skew | Líneas de retardo de guía + ajuste fino con **Azobenceno** (365/450 nm, Δn=0,02) | Reconfigurable lento | Ajuste de fase/tiempo |

- **Direccionamiento óptico:** la selección de celdas/bancos se realiza mediante una red de decodificación y conmutación óptica (árboles de conmutadores **VO₂** y máscaras **Espiropirano**) controlada por señales ópticas de dirección en longitudes de onda de control.
- **Lectura:** no destructiva en $\lambda_s$ (sondeo de transmisión/fase a baja potencia dentro del rango lineal/estable del material).

### 4.3 Red de interconexión y control óptico
- **Enrutamiento:** crossbars y conmutadores basados en **VO₂** para establecer caminos entre memoria, núcleo de cómputo y salida.
- **Selección y protección:** elementos de **Espiropirano** actúan como compuertas que aíslan bancos durante escritura (evitando perturbación por señales de datos o de programación adyacentes).
- **Calibración:** **Azobenceno** en regiones de acoplamiento para corrección estática o de baja frecuencia de errores de fase debidos a fabricación y deriva térmica.

## 5. Modelo de ejecución (pipeline óptico)

1. **Carga de configuración (óptica):** se programan mapas de ruta y selección de bancos en M0 (Espiropirano, 365/520 nm).
2. **Carga de pesos/kernels:** se escriben matrices en M1 (Sb₂S₃, 650 nm / 300 °C) de forma no volátil.
3. **Entrada de datos:** el host envía vectores/activaciones por el enlace óptico; se almacenan temporalmente en M2 (VO₂) si se requiere alineación.
4. **Cómputo:** los datos fluyen por el núcleo MVM; los productos parciales se combinan ópticamente.
5. **Acumulación/buffering:** resultados intermedios se realimentan o retienen en M2/M3 para operaciones encadenadas (p. ej., capas sucesivas o reducción por bloques).
6. **Salida:** el resultado final se entrega al host por el bus óptico de salida (con conversión O/E solo en el borde si el host es electrónico).

## 6. Diseño físico y gestión espectral/térmica

- **Plataforma base:** fotónica de nitruro de silicio (SiN) recomendada para soportar visible/NIR y reducir pérdidas; silicio (SiPh) como alternativa según $\lambda_s$.
- **Plano espectral (ejemplo de asignación, a refinar por simulación):**
  - $\lambda_s$ (datos): banda de operación estable (p. ej., NIR) fuera de resonancias de escritura.
  - 650 nm: escritura/programación de **Sb₂S₃**.
  - 800 nm: control/conmutación de **VO₂**.
  - 365 nm: conmutación trans→cis (**Azobenceno**) y cerrado→abierto (**Espiropirano**).
  - 450 nm: cis→trans (**Azobenceno**); 520 nm: abierto→cerrado (**Espiropirano**).
- **Aislamiento:** filtros espectrales integrados, multiplexores por división de longitud de onda (WDM) y separación espacial para evitar escritura cruzada y diafonía.
- **Gestión térmica:** barreras térmicas y microzonas aisladas; los eventos de 300 °C (Sb₂S₃) deben confinarse para no disparar VO₂ (68 °C). Se prioriza escritura óptica de Sb₂S₃ donde sea posible para reducir carga térmica. Sincronización temporal de pulsos para evitar solapamientos térmicos.
- **Integración de materiales:** parches de Sb₂S₃ y VO₂ sobre/acoplados a guías con encapsulado; azobenceno/espiropirano en recubrimientos poliméricos funcionalizados en regiones de campo evanescente.
- **Electrónica mínima de borde:** drivers de láser, controladores térmicos globales, y transceptores E/O–O/E en la interfaz host; sin SRAM/DRAM on-chip para datos de cómputo o almacenamiento de pesos.

## 7. Interfaz con el host y software abierto

- **Interfaz:** enlace óptico (fibra/acoplador) con protocolo de framing para vectores, matrices y comandos de configuración; conversión a PCIe/CXL en el lado host mediante tarjeta adaptadora.
- **Modelo de memoria expuesto:** espacios direccionables para M0 (config), M1 (pesos no volátiles) y M2 (buffers volátiles), accesibles mediante comandos ópticos.
- **Pila de software (propuesta):**
  - Compilador/mapeador: grafos de operadores lineales → configuración de malla, asignación de bancos de memoria y plan de pulsos de control.
  - Runtime/driver: gestión de transferencia óptica, secuencias de escritura/borrado y verificación.
  - Simulación abierta: modelos de celdas PCM/fotoquímicas/VO₂ y de la red fotónica (p. ej., herramientas basadas en gdstk/Meep/Simphony u equivalentes abiertos).

## 8. Hoja de ruta v0.2

1. **Modelado de celdas:** caracterizar ópticamente (Δn efectivo, pérdidas, retención, ciclos, energía por bit) celdas de memoria Sb₂S₃, Espiropirano y latches VO₂.
2. **Memoria óptica integrada:** demostrar un banco M1 (no volátil) y M2 (volátil) direccionables por red de conmutación óptica.
3. **Núcleo MVM:** prototipo de malla pequeña (p. ej., 4×4) con pesos Sb₂S₃ y enrutamiento VO₂.
4. **Integración sistema:** pipeline óptico completo (carga → cómputo → realimentación → salida) sin buffers electrónicos intermedios.
5. **Evaluación:** capacidad de memoria óptica (bits/celdas), precisión efectiva, latencia, throughput óptico, eficiencia energética (pJ/op) y endurance.

## 9. Riesgos y trabajo futuro

- **Densidad y escalabilidad:** las celdas fotónicas son mayores que las electrónicas; explorar multinivel (Sb₂S₃) y WDM para aumentar capacidad.
- **Pérdidas y cascadabilidad:** acumulación de pérdidas en redes profundas; requiere diseño de bajo loss y, si es necesario, regeneración óptica.
- **Crosstalk térmico/óptico:** interferencia entre umbrales (68 °C, 300 °C) y entre canales de control/datos.
- **Endurance y estabilidad:** ciclos de Sb₂S₃/VO₂ y fatiga/retención de azobenceno y espiropirano bajo operación continua.
- **Precisión analógica:** ruido, deriva y resolución efectiva; posibles esquemas de corrección y cómputo híbrido de precisión.

## 10. Licencia y apertura (sugerencia)

- **Documentación y diseños hardware:** CERN-OHL-S v2.
- **Modelos, netlists fotónicas y scripts de simulación:** CERN-OHL-S v2 o CC BY-SA 4.0.
- **Software/firmware de interfaz:** Apache-2.0 o GPL-3.0.
- Publicar resultados de caracterización, procedimientos de calibración y archivos de diseño (layout GDS, parámetros de proceso) en un repositorio abierto.

---
*Versión 0.2 — Borrador conceptual orientado a cómputo y memoria predominantemente ópticos. Contribuciones bienvenidas.*