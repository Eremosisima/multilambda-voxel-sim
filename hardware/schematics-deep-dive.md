# Esquemáticos y diseño detallado — OPGPU v0.8 (GPU/NPU/TPU óptico, estrategias actuales)

> Esquemáticos conceptuales (bloques, señales y flujos). No sustituyen netlists/GDS/PCB finales; sirven como base para simulación y prototipado.  
> **Dominio público (objetivo declarado):** uso libre para todo el mundo, publicado como **arte previo/divulgación defensiva** para dificultar apropiación registral por terceros (ver `../PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta).  
> **Actualización v0.8 (estrategias actuales):** alineado con familias **A–G**, combinaciones **H1–H5** y candidatos priorizados **H3, G2, G3, H1, H4**; incorpora control térmico fabricable, jerarquía **M0–M3/OMCC** e interfaces modulares (aislamiento C&D). Ver documento integrador: [`current-strategies-schematics-and-instructions.md`](current-strategies-schematics-and-instructions.md), [`manufacturable-dimensions-and-ai-accelerators.md`](manufacturable-dimensions-and-ai-accelerators.md), [`optical-memory-hierarchy-l1l2l3.md`](optical-memory-hierarchy-l1l2l3.md), y [`../CANDIDATE_REPOS_STRATEGY.md`](../CANDIDATE_REPOS_STRATEGY.md).

## 0. Selección de estrategia (plano fotónico intercambiable)

```text
[OMCC + borde E/O-O/E + interfaz de módulo]
                 |
    +------------+------------+------------+------------+
    v            v            v            v            v
 [H3 A1+G1+B3] [G2 EO-FP] [G3 PCM+EO] [H1 3D NV] [H4 Tensor 3D]
 factible/     rápido/    NV+rápido   NV volum.  capacidad máx.
 abierto       BW alto    equilibrado  (3D/aisl.) (3D/térm. alta)

Módulo = {núcleo óptico, M0-M3 local, actuadores (EO/térmico/PCM), sensado, ruta térmica}
Interfaz común: puertos λ/WDM, mapa control/telemetría, presupuesto térmico/potencia, protocolo OMCC
Regla: candidato/bloque sustituible o retirable sin afectar a los demás (modular/C&D)
```

## 1. Vista de sistema (tarjeta PCIe + módulo fotónico)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOST: CPU + OpenCL Runtime/Driver + Memoria                                 │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │ PCIe (x16, Gen4/5 objetivo)
┌───────────────────────────────▼─────────────────────────────────────────────┐
│ TARJETA (BORDE ELECTRÓNICO MÍNIMO)                                          │
│                                                                             │
│  [Edge PCIe]─[Retimers/SI]─[PCIe Endpoint + DMA Engine]                     │
│                                   │                                         │
│                         ┌─────────┴─────────┐                               │
│                         │ BAR0 CSRs/DB      │  BAR1 Apertura mem óptica     │
│                         │ IRQ/MSI-X         │                               │
│                         └─────────┬─────────┘                               │
│                                   │                                         │
│                         [Command Processor / Scheduler]                     │
│                                   │                                         │
│                         [Micro-secuenciador de pulsos]                      │
│                           │    │    │    │    │                             │
│                        [TX λs][TX650][TX800][TX365/450/520]  [RX PD/TIA/ADC]│
│                           │    │    │    │    │                 ▲           │
└───────────────────────────┼────┼────┼────┼────┼─────────────────┼───────────┘
                            │    │    │    │    │    acoplador/fibra/interposer
┌───────────────────────────▼────▼────▼────▼────▼─────────────────┴───────────┐
│ MÓDULO FOTÓNICO (PLANO BASE + CEPILLO EXTRUIDO)                             │
│  [Distribución WDM/guías] -> [Red de control óptico] -> [Tiles/CU ópticos]  │
│                                      │                        │             │
│                               [M0 Espiropirano]        [M1 Sb2S3 pesos]    │
│                                      │                        │             │
│                               [VO2 switches] <--------> [M2 VO2 buffers]    │
│                                      │                        │             │
│                               [M3 retardos/Azobenceno] -> [Array MVM/MAC]  │
│                                                               │             │
│                                                        [Salida O/E borde]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2. Esquemático del borde PCIe/transductor (detalle lógico)

```text
PCIe lanes <==> [PHY/SerDes] <==> [Controller/Endpoint]
                                      |
                     +----------------+----------------+
                     |                                 |
              [DMA Engine]                      [Register File]
           (RD/WR host mem)                    (doorbell,status,cap,
                     |                          queue ptrs, config)
                     +----------------+----------------+
                                      |
                              [Command Processor]
                               |      |       |
                        fetch desc  sched  completion
                               |      |       |
                           [Queue Manager] [IRQ/MSI-X gen]
                                      |
                          [Optical Micro-sequencer]
                                      |
                 +----------+---------+---------+----------+
                 |          |         |         |          |
            [DAC/Drv]  [DAC/Drv] [DAC/Drv] [DAC/Drv]   [ADC/TIA]
                 |          |         |         |          ^
             Laser λs   Laser 650  Laser 800  UV/Vis    Photodiodes
           (datos E/O)  (Sb2S3)     (VO2)    365/450/520  (O/E datos)
                 \          \         \         /          /
                  \          \         \       /          /
                   +------ [Multiplexor/Acoplador Óptico] --+
                                      |
                               al plano fotónico
```

**Funciones clave:**
- **Doorbell → ejecución:** la escritura MMIO despierta al CP; no hay interpretación de instrucciones en el plano óptico, solo microsecuencias deterministas.
- **Aislamiento de dominios:** el dominio eléctrico maneja protocolo/fiabilidad (TLPs, retries, CRC a nivel PCIe); el dominio óptico maneja transporte de datos/señales de control con su propio esquema de integridad (tramas, CRC óptico opcional en borde, verificación por lectura).
- **Reloj/temporización:** referencia común (PLL) para secuenciador y muestreo ADC; la alineación fina en dominio óptico se ajusta con M3/Azobenceno.

## 3. Esquemático de un Compute Unit (tile) óptico

```text
                 +------------------- M0 (Espiropirano) -------------------+
                 |  registro de ruta | máscara de banco | modo GPU/NPU/TPU  |
                 +------------------------------+--------------------------+
                                                | configura
   Entrada λs (vector/bloque)                   v
        |                         [Conmutadores VO2 / crossbar de ruta]
        v                                     |
 [Pre-buffer M3/Azobenceno]                   +--> a banco seleccionado
        |                                     |
        v                                     v
 [Inyector de filas/columnas] ----λs----> [Núcleo MVM/MAC]
                                              |   \
                                              |    \ pesos (lectura evanescente)
                                       parciales     [Banco M1: matriz Sb2S3]
                                          |                 (no volátil)
                                          v
                                   [Acumulador M2: VO2]
                                          |
                                   (opcional) [No lineal VO2]
                                          |
                                   [Salida tile] -> red de retorno -> O/E
```

**Parámetros de tile (ejemplo conceptual):** tamaño de bloque MVM (p. ej. 64×64 o 256×256 celdas efectivas), profundidad de M2 para $k$ acumulaciones, canales WDM por tile, y latencia de tubería (propagación + conmutación + conversión).

## 4. Cerda del "cepillo extruido" (canal/vóxel)

```text
Sección longitudinal de una cerda (canal aislado):

   Plano base ======┓  (guía horizontal, distribución λs/λc)
                    ╲ 45°
                     ╲  microespejo/faceta
                      ▼
                    ┌───┐  z3  [Vóxel VO2]      (latch/conmutación, 800 nm)
                    ├───┤  z2  [Vóxel Sb2S3]    (peso/memoria NV, 650 nm)
                    ├───┤  z1  [Vóxel Espirop.] (máscara/config, 365/520 nm)
                    ├───┤  z0  [Vóxel Azobenc.] (trim/retardo, 365/450 nm)
                    └─┬─┘
                      │ retorno/lectura (reflexión 45° o guía de bajada)
                      ▼
   Plano base <======┛

Aislamiento lateral: recubrimiento de bajo índice / barrera absorbente (anti-crosstalk).
Confinamiento térmico: micro-barreras alrededor de regiones de 300 °C (escritura Sb2S3).
```

## 5. Mapa de señales y longitudes de onda

| Señal | λ / estímulo | Dirección | Función |
|---|---|---|---|
| Datos $\lambda_s$ | Banda de operación (p. ej. NIR, estable) | Host→módulo→host (loop) | Vectores/activaciones/resultados |
| Prog. Sb₂S₃ | 650 nm (óptico) / 300 °C (térmico) | Control → M1 | Escritura de pesos/memoria NV |
| Control VO₂ | 800 nm / 68 °C | Control → M2/conmutadores | Conmutación, latches, umbral |
| Control Espiropirano | 365 nm (abrir) / 520 nm (cerrar) | Control → M0 | Rutas, máscaras, configuración |
| Control Azobenceno | 365 nm (t→c) / 450 nm (c→t) | Control → M3/trim | Calibración de fase/retardo |

## 6. Pipeline temporal (ejecución de un kernel)

```text
Tiempo →
[DMA in / fetch desc] [cfg M0/M1] [inyectar λs] [propagar+MAC] [acumular M2] [O/E + DMA out] [IRQ]
        |                  |            |              |              |             |
      borde             control       datos         óptico         óptico        borde
                         (pulsos)       in                             out

Solapamiento: doble buffer (mientras tile A computa, tile B carga datos/pesos siguientes).
```

## 7. Consideraciones para implementación óptima
- **Particionado:** maximizar localidad en M1/M2 para reducir reprogramaciones de Sb₂S₃ y conversiones O/E.
- **WDM:** multiplexar canales $\lambda_s$ para aumentar throughput por cerda/tile.
- **Térmica:** calendarizar escrituras de 300 °C y operación de VO₂ para evitar deriva; sensores térmicos en borde con realimentación al scheduler.
- **Calibración:** rutina de arranque que barre Azobenceno/ganancias y almacena coeficientes de corrección por tile.
- **Fiabilidad:** detección de errores (CRC en tramas, lecturas de verificación post-escritura en Sb₂S₃/Espiropirano) y reporte vía registros de estado.