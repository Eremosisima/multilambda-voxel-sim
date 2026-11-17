# Coprocesador óptico, RAM óptica compartida y mejoras de diseño (v0.8, investigación)

> Documento de extensión conceptual para OPGPU. Integra un **coprocesador con acceso directo a RAM óptica** y sintetiza mejoras basadas en investigación reciente en fotónica integrada, memorias de cambio de fase (PCM), conmutación VO₂ y arquitecturas de aceleración óptica. Estado: investigación/diseño conceptual (no validado experimentalmente).  
> **Dominio público (objetivo declarado):** uso libre para todo el mundo; publicado como **arte previo/divulgación defensiva** (ver `../PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta).

## 1. Motivación

Las versiones v0.1–v0.4 definen cómputo, memoria y enrutamiento mayoritariamente ópticos con interfaz PCIe/OpenCL y modos GPU/NPU/TPU. Sin embargo, el rendimiento y la viabilidad dependen de: (a) latencia y contención en el acceso a memoria óptica, (b) coste de programación de PCM, (c) orquestación de datos (DMA, formato, tiling), (d) calibración/fiabilidad y (e) escalabilidad (pérdidas, diafonía, térmica, endurance). Un **coprocesador dedicado** con acceso a la RAM óptica reduce la carga del host/Command Processor y habilita funciones de gestión y aceleración cercanas a los datos.

## 2. Coprocesador OMCC (Optical Memory & Control Coprocessor)

### 2.1 Rol y funciones
El OMCC es un subsistema (RTL/firmware sobre FPGA/ASIC ligero en el borde, con interfaces fotónicas de control) que opera como **agente de memoria y control** del plano fotónico:

| Función | Descripción | Beneficio |
|---|---|---|
| **Gestión de memoria óptica** | Asignación/liberación de regiones en M0–M3, traducción de direcciones lógicas (OpenCL buffers) a direcciones físicas de celdas/cerdas/tiles, protección y particionado | Aísla al host del mapa físico; permite multitarea/subdispositivos |
| **DMA y movimiento de datos** | Orquestación de transferencias host↔borde↔óptico, gather/scatter, empaquetado WDM, *double buffering* y *prefetch* hacia M2 | Oculta latencia PCIe/E-O-O-E (cuello de botella identificado en simulación v0.4) |
| **Formato y pre/post-procesado** | `im2col`/`col2im`, transposición, reordenamiento, cuantización/descuantización, escalado de bloques, empaquetado de vectores para $\lambda_s$ | Mejora utilización de tiles NPU/TPU y reduce tráfico |
| **Planificación de pulsos y térmica** | Calendariza escrituras de Sb₂S₃ (650 nm / 300 °C) y conmutaciones VO₂ (800 nm / 68 °C) evitando solapamientos térmicos; aplica límites de potencia y *duty cycle* | Mitiga crosstalk térmico y deriva |
| **Calibración y control adaptativo** | Barridos de trim (Azobenceno), ajuste de ganancias por tile, compensación de deriva, lectura de verificación post-escritura | Mejora precisión analógica efectiva |
| **Fiabilidad y RAS** | ECC/códigos de detección en tramas O/E, lecturas de verificación, *scrubbing* de estados, contabilización de ciclos (*wear*), reasignación de celdas degradadas | Aumenta endurance útil y detecta fallos |
| **Sincronización** | Barreras, fences, señales de evento/completion, arbitraje entre colas | Cumple semántica de colas/eventos OpenCL |

### 2.2 Arquitectura y acceso a RAM óptica

```text
                         ┌──────────────────────────────────────────┐
                         │               HOST / PCIe                │
                         └──────────────────┬───────────────────────┘
                                            │ TLP/DMA + MMIO
┌───────────────────────────────────────────▼──────────────────────────────────┐
│  BORDE (SoC de control)                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌───────────────┐ │
│  │ PCIe EP/DMA  │◄─►│ Command Proc │◄─►│    OMCC      │◄─►│ E/O-O/E + μSeq│ │
│  └──────────────┘   └──────────────┘   │ (coprocesador│   └───────┬───────┘ │
│                                        │  mem/ctrl)   │           │         │
│                                        └──────┬───────┘           │         │
│                         ┌─────────────────────┼───────────────────┘         │
│                         │ tabla de páginas/    │ μórdenes + direcciones     │
│                         │ regiones ópticas     │                            │
└─────────────────────────┼─────────────────────┼────────────────────────────┘
                          │                     │  buses de control/datos ópticos
                          ▼                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  PLANO FOTÓNICO (RAM óptica compartida + cómputo)                            │
│                                                                              │
│  [M0 Espiropirano: config/mapas]  <── acceso R/W de control (OMCC/CP)        │
│  [M1 Sb2S3: RAM NV / pesos]       <── acceso R/W (programación) + R (datos)  │
│  [M2 VO2: RAM volátil/buffers]    <── acceso R/W alta frecuencia (tiles)     │
│  [M3 retardos/Azobenceno: sync]   <── acceso de ajuste (OMCC)                │
│         ^              ^                    ^                                │
│         └──────────────┴────────┬───────────┘                                │
│                                 │ red de interconexión óptica conmutada    │
│                                 ▼                                            │
│                    [Tiles GPU/NPU/TPU: núcleos MVM/MAC]                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Modelo de acceso compartido:**
- **Espacio de direcciones óptico unificado:** el OMCC mantiene una tabla de mapeo `{buffer_id, offset} → {banco, cerda(x,y), nivel z, canal λ, tile}`. Los tiles acceden a M1/M2 mediante rutas establecidas en M0; el OMCC arbitra y serializa escritores en regiones compartidas.
- **Puertos:** (1) puerto de *programación* (baja frecuencia, alta energía, a 650/365/450/520/800 nm) controlado por OMCC; (2) puerto de *lectura/datos* ($\lambda_s$, alta frecuencia) usado por tiles; (3) puerto de *lectura de verificación* O/E hacia OMCC para calibración/RAS.
- **Coherencia:** modelo explícito (no caché coherente por hardware óptico): el OMCC hace *flush/commit* de buffers (asegura fin de escrituras en M1/M2) antes de exponer resultados/eventos al host o a tiles dependientes.

### 2.3 Microarquitectura del OMCC (conceptual)
- **Núcleos/engines:** motor DMA, motor de comandos, unidad de traducción de direcciones (OATU), programador de pulsos, monitor térmico/óptico, controlador de interrupciones/eventos.
- **Memoria local del OMCC (electrónica, SRAM pequeña en borde):** descriptores, tablas de mapeo, colas, contadores de desgaste, perfiles de calibración por tile.
- **Interfaz de programación:** API interna (registros + colas) expuesta al driver OpenCL; extensiones para prefetch, persistencia de pesos en M1 y consultas de salud/RAS.

### 2.4 Impacto esperado
- Reducción de *stalls* por transferencia/control (desacopla host); mejor solapamiento cómputo↔comunicación.
- Mayor vida útil efectiva de M1 mediante *wear-aware allocation* y verificación.
- Base para ejecución concurrente de múltiples kernels/subdispositivos con aislamiento.

## 3. Investigación en profundidad: mejoras propuestas

Las siguientes mejoras se derivan de resultados reportados en fotónica integrada y memorias ópticas (PCM/VO₂) y se mapean al diseño OPGPU. Las cifras citadas son valores reportados en la literatura; su aplicabilidad a este sistema requiere validación específica.

### 3.1 Memoria PCM (M1, Sb₂S₃ y alternativas)

| Mejora | Evidencia / base técnica | Aplicación en OPGPU | Impacto |
|---|---|---|---|
| **Multinivel de alta densidad (≥5–7+ bits/celda)** | Sb₂S₃ con control dinámico de pulsos ha demostrado operación de 5 bits (32 niveles) eléctricamente; optimización geométrica en PCM fotónicos ha mostrado >7.6 bits (209 estados) en condiciones específicas | Usar programación por trenes de pulsos idénticos/ajustados y calibración cerrada (OMCC) para celdas Sb₂S₃ en M1; almacenar escala por bloque | ↑ densidad efectiva y capacidad de pesos cuantizados sin aumentar $N_{x,y,z}$ |
| **Nanoestructuración/segmentación y tapering** | Segmentación y extremos en taper en PCM sobre guía reducen pérdidas y han mostrado endurance muy alta (≥10⁸ ciclos en reportes con Sb₂Se₃) y menor IL | Segmentar parches Sb₂S₃ en celdas/cerdas y aplicar transiciones adiabáticas (tapers) en interfaces guía↔PCM | ↓ pérdidas, ↑ cyclability, mejor cascadabilidad |
| **Optimización de espesor/geometría y microestructuras** | Ajuste de espesor para maximizar contraste y estructuras (p. ej. arreglos micro-cilíndricos) han mejorado contraste y endurance (hasta ~2×10⁶ ciclos reportados) con baja energía de programación | Co-diseño geométrico de celdas M1 por simulación (FDTD/FEM) y bibliotecas de celdas estándar | ↑ relación señal/contraste, ↓ energía por escritura |
| **Materiales de banda prohibida ancha / baja pérdida** | Sb₂S₃/Sb₂Se₃ presentan baja pérdida en telecomunicaciones frente a GST; selección de PCM según banda $\lambda_s$ reduce absorción en lectura | Mantener Sb₂S₃ como base (especificado) y evaluar Sb₂Se₃/GSST en variantes para $\lambda_s$ NIR con menor IL (documentar como opción compatible) | ↓ pérdidas de inserción, ↑ SNR de lectura |
| **Programación híbrida (óptica y térmica localizada)** | Escritura óptica en guía y calentadores integrados; pulsos cortos reducen energía y zona afectada | Priorizar escritura óptica (650 nm) guiada; usar microcalentadores solo donde sea necesario, con confinamiento térmico | ↓ crosstalk térmico y energía media |

### 3.2 Conmutación y memoria volátil (M2, VO₂)

| Mejora | Evidencia / base técnica | Aplicación en OPGPU | Impacto |
|---|---|---|---|
| **Endurance ultra-alta en conmutación volátil** | Memorias fotónicas VO₂/Si han demostrado ciclado muy alto (≥10⁷ ciclos) con footprint compacto y operación rápida | Usar VO₂ para M2 (latches/buffers) y conmutadores de ruta de alta frecuencia, reservando Sb₂S₃ para escrituras infrecuentes | ↑ fiabilidad en operaciones runtime |
| **Ingeniería de umbral y retención** | Control de histéresis térmica y sesgo óptico/térmico para estados estables temporales | Definir ventanas de mantenimiento (*hold*) y refresco para M2 gestionadas por OMCC | Latches volátiles predecibles |
| **Aislamiento térmico selectivo** | Diferencia de umbrales (68 °C VO₂ vs 300 °C Sb₂S₃) exige barreras y pulsos confinados | Trench/aislantes, separación espacial y *time-multiplexing* de eventos térmicos | ↓ disturb entre M1 y M2 |

### 3.3 Interconexión, cómputo y escalado

| Mejora | Evidencia / base técnica | Aplicación en OPGPU | Impacto |
|---|---|---|---|
| **WDM y particionado espectral estricto** | Separación de canales de datos/control reduce escritura espuria; WDM escala ancho de banda por guía | Plan de $\lambda$ por función (datos, 365/450/520/650/800) con filtros y guardas espectrales | ↑ throughput y ↓ crosstalk |
| **Tiles especializados y pipelining profundo** | TPUs/NPUs se benefician de datos estacionarios y tuberías; *photonic tensor cores* explotan paralelismo en longitud de onda | Mantener modos GPU/NPU/TPU con tiles configurables, *double buffering* M2 y solapamiento DMA↔cómputo (OMCC) | ↑ utilización sostenida |
| **Reducción de cuellos de botella host↔dispositivo** | Simulación v0.4 mostró transferencias como limitante en baja intensidad/reuso | Prefetch, persistencia de pesos en M1, batching, y ejecución de operadores compuestos en dispositivo | ↓ latencia efectiva, ↑ TOPS runtime |
| **Calibración en lazo cerrado** | Deriva termo-óptica y variabilidad analógica requieren corrección | Sensores (térmicos/ópticos) + ajuste fino con Azobenceno y tablas de corrección en OMCC | ↑ precisión y estabilidad |
| **Variantes de materiales fotoquímicos (M0/M3)** | Azobenceno/espiropirano ofrecen reconfiguración no volátil/biestable pero con Δn menor y fatiga fotoquímica; útiles en control y trim | Limitar a roles de baja frecuencia (config/trim) y evaluar encapsulado/aislamiento espectral para prolongar vida | Balance entre reconfigurabilidad y durabilidad |

### 3.4 Fiabilidad, fabricación y sistema

| Área | Mejora | Detalle |
|---|---|---|
| **Endurance y gestión de desgaste** | *Wear leveling* y limitación de escrituras | OMCC contabiliza ciclos por región M1; prioriza reuso de pesos estacionarios (NPU/TPU) y reubica regiones calientes |
| **Integridad de datos** | ECC/CRC y verificación | CRC en tramas DMA/O-E y lectura-verificación tras programar celdas críticas |
| **Pérdidas y presupuesto de enlace** | Diseño de enlace fotónico | Presupuesto de potencia (fuentes, acoplamiento, IL por elemento, sensibilidad PD) y márgenes por WDM |
| **Empaquetado y térmica** | Co-integración | Interposer óptico, disipación para zonas de 68–300 °C, y sensores distribuidos |
| **Software** | Runtime/driver consciente de óptica | Exposición de persistencia M1, costes de reprogramación, perfiles de precisión y telemetría (OpenCL extensions/vendor queries) |

## 4. Hoja de ruta de mejoras (priorizada)

1. **P0 (arquitectura):** especificar OMCC (ISA/colas internas, mapa de direcciones óptico, arbitraje M1/M2) y su integración con el Command Processor/PCIe.
2. **P0 (simulación):** extender `simulate_opgpu_system.py` con parámetros de OMCC (prefetch, overlap DMA, latencia de arbitraje) y modelos de coste de programación/verificación.
3. **P1 (memoria):** prototipar celdas Sb₂S₃ segmentadas/tapered con multinivel controlado y caracterizar IL, energía, retención y ciclos.
4. **P1 (térmica/crosstalk):** simulación térmica transitoria de escrituras 300 °C vs operación VO₂ 68 °C en el arreglo cepillo.
5. **P2 (sistema):** calibración en lazo cerrado, RAS (*wear leveling*, verificación) y perfiles NPU/TPU con pesos persistentes.
6. **P2 (exploración):** variantes de PCM (p. ej. Sb₂Se₃/GSST) y optimizaciones de enlace WDM según resultados experimentales.

## 5. Referencias de investigación (base consultada)

- **PCM fotónico y Sb₂S₃/Sb₂Se₃:** operación multinivel y programación eléctrica/óptica en Sb₂S₃ (p. ej. Nature Communications 2023, DOI: 10.1038/s41467-023-39180-3); memorias fotónicas optimizadas en estructura con alta densidad/contraste (Photonics/MDPI 2025, DOI: 10.3390/photonics12111130); nanoestructuración/tapering para baja pérdida y alta endurance en dispositivos PCM (arXiv 2026, 2604.08637).
- **VO₂ en fotónica de silicio:** memoria fotónica volátil de alta endurance (npj Nanophotonics 2024, DOI: 10.1038/s44310-024-00038-1).
- **CAM/arquitecturas ópticas y aceleración:** CAM óptica y búsqueda de similitud con PCM (APL Photonics/DOI: 10.1063/5.0288417; Photonics/MDPI 2026, DOI: 10.3390/photonics13030249); *photonic tensor cores* y aceleración tensorial óptica (literatura de fotónica computacional, p. ej. trabajos sobre PTC/TPU fotónica).
- **Sistemas/TPU:** organización de memoria, interconexiones y conmutación óptica a escala de sistema (documentación/arquitecturas TPU y OCS como referencia de integración sistema, uso nominativo).

> Nota: las referencias anteriores respaldan direcciones de mejora; los parámetros numéricos finales deben derivarse de caracterización del proceso y materiales específicos de OPGPU.