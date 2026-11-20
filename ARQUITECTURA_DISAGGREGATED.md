# OPGPU — Arquitectura Disaggregated: Transceptor PCIe + Módulo Fotónico Remoto

> **Fecha:** 2026-11-19 (v0.9-disaggregated)
> **Estado:** conceptual/simulado. No es diseño listo para fabricación.
> **Cambio estratégico:** de "tarjeta PCIe con todo integrado" a "transceptor PCIe compacto + módulo fotónico remoto conectado por fibra con refrigeración líquida".

---

## 1. Motivación

La arquitectura original (tarjeta PCIe con módulo fotónico integrado) enfrenta riesgos críticos:
- **Térmica:** duty-cycle PCM limitado a ~0.12 en peor caso (margen VO2 68°C).
- **Factor forma:** restricción de espacio (75W slot o 300W con aux), limita disipación.
- **Yield:** chips grandes en 3D tienen yield bajo.
- **Acoplamiento fibra-chip:** requiere alineación <1 µm en tarjeta PCIe.

**Arquitectura disaggregated resuelve:**
- **Térmica:** módulo remoto puede usar refrigeración líquida (Fluorinert, cold plates), duty-cycle factible sube a **0.5–1.0**.
- **Factor forma:** módulo remoto puede ser rack-mount o standalone, sin restricciones PCIe.
- **Yield:** módulos 2.5D más grandes o múltiples chips pequeños interconectados ópticamente.
- **Acoplamiento:** con espacio para lentes/GRIN, margen de alineación ±5 µm (IL 0.5–1.5 dB vs 2–5 dB).

---

## 2. Arquitectura de sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOST (CPU + RAM)                                                            │
│   └── PCIe Gen4/5 x8/x16 (eléctrico, <0.5 m)                               │
│        └──┐                                                                  │
└───────────┼─────────────────────────────────────────────────────────────────┘
            │
┌───────────┼─────────────────────────────────────────────────────────────────┐
│ TRANSCEPTOR PCIe-to-Optical (tarjeta compacta o módulo SFF)                 │
│                                                                             │
│   [Conector PCIe edge]                                                      │
│        └── [PCIe PHY/SerDes + Controller/EP]                                │
│               └── [FPGA/SoC: DMA, Command Processor, Scheduler]             │
│                      ├── [Memoria staging: DDR4/DDR5]                       │
│                      ├── [TX E/O: láseres WDM + moduladores]                │
│                      └── [RX O/E: PDs + TIA + ADC]                          │
│                                                                             │
│   Factor forma: tarjeta low-profile o módulo SFF (ej. OCP NIC 3.0)         │
│   Potencia: 25–75W (sin límite de slot completo)                           │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            │ Fibra óptica (monomodo, 0.5–5 m)
            │ Pérdida: <0.01 dB/m + conectores (0.2–0.5 dB c/u)
            │ Latencia: ~5 ns/m (ida y vuelta: 10 ns/m)
            │
┌───────────┼─────────────────────────────────────────────────────────────────┐
│ MÓDULO FOTÓNICO REMOTO (rack/standalone, refrigeración líquida opcional)   │
│                                                                             │
│   [Backplane óptico: MUX/DEMUX WDM, splitters, acopladores]                 │
│        └── [Chips fotónicos 2.5D/3D: tiles MZI, PCM, EO, resonadores]      │
│               ├── [M0: MZI/crossbar (cómputo)]                              │
│               ├── [M1: PCM (pesos NV)]                                      │
│               ├── [M2: VO2 (buffer volátil)]                                │
│               └── [M3: azobenceno/espiropirano (trim/máscara)]              │
│                                                                             │
│   [Control local: FPGA/MCU para calibración autónoma, OMCC, telemetría]    │
│   [Sensores: temperatura, potencia óptica, BER proxy]                       │
│   [Actuadores: TEC, calentadores PCM, drivers EO]                           │
│                                                                             │
│   Factor forma: módulo rack (1U–4U) o standalone con cold plate            │
│   Potencia: 100–500W (con refrigeración líquida)                           │
│   Refrigeración: aire (ventiladores) o líquida (Fluorinert, cold plate)    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Transceptor PCIe (diseño actualizado)

### 3.1 Función
Convertir señales eléctricas PCIe (datos de host) a ópticas (WDM) y viceversa. **No contiene el módulo fotónico de cómputo.**

### 3.2 Componentes clave

| Bloque | Función | Implementación |
|---|---|---|
| **PCIe Controller/EP** | Endpoint PCIe, DMA, MSI-X | FPGA (Xilinx/AMD UltraScale+, Intel Agilex) o ASIC futuro |
| **Command Processor (CP)** | Interpretar descriptores de cola, generar microsecuencias | Lógica en FPGA/SoC |
| **Memoria staging** | Buffers de colas, pesos temporales, firmware | DDR4/DDR5 SODIMM o on-board (4–16 GB) |
| **TX E/O** | Convertir datos a óptica (WDM) | Láseres DFB/VCSEL + moduladores (MZI o EO) + drivers |
| **RX O/E** | Convertir óptica a eléctrica | Fotodetectores + TIA + ADC + CDR |
| **MUX/DEMUX WDM** | Multiplexar/desmultiplexar λs | Arrayed Waveguide Grating (AWG) o filtros sintonizables |
| **Interfaz fibra** | Conectores fibra (LC/APC o MPO) | Lentes/GRIN para acoplamiento tolerante (±5 µm) |
| **Control/telemetría** | Sensores T/V/I, gestión de energía | MCU integrado o lógica en FPGA |

### 3.3 Especificaciones objetivo

| Parámetro | Valor objetivo | Notas |
|---|---|---|
| **PCIe** | Gen4 x8 (bring-up), Gen4/5 x16 (producción) | BW: 16 GB/s (Gen4 x8), 64 GB/s (Gen5 x16) |
| **WDM canales** | 8–16 λs | Depende de candidato (H3/G3/G2) |
| **Potencia óptica TX** | 0–10 dBm por λ | Depende de IL del módulo remoto |
| **Sensibilidad RX** | -20 a -10 dBm | Depende de ER y ruido |
| **Latencia transceptor** | <100 ns | Incluye DMA, E/O, O/E, colas |
| **Potencia eléctrica** | 25–75W | Depende de número de λs y drivers |
| **Factor forma** | Low-profile o SFF (OCP NIC 3.0) | Cabe en slot estándar o módulo externo |

### 3.4 Interfaz con host (OpenCL/OpenVINO)

El transceptor expone al host un **dispositivo acelerador** vía:

1. **Driver de kernel (KMD):** gestiona PCIe BARs, DMA, MSI-X, resets.
2. **Runtime OpenCL:** expone plataforma/dispositivo, colas, memoria, eventos.
3. **Plugin OpenVINO (opcional):** traduce subgrafos soportados a microsecuencias OPGPU.

**Flujo de comando:**
```
App OpenCL/OpenVINO
   └── Runtime/Plugin
        └── Descriptor de comando (GEMM, conv, etc.)
             └── DMA a memoria staging del transceptor
                  └── Doorbell MMIO → Command Processor
                       └── Microsecuencias ópticas → TX E/O
                            └── Fibra → Módulo remoto
                                 └── Cómputo fotónico
                                      └── RX O/E → DMA → Host
                                           └── Evento/IRQ → App
```

**Modelo de memoria:**
- **M0 (cómputo):** en módulo remoto (MZI/crossbar).
- **M1 (pesos NV):** en módulo remoto (PCM).
- **M2 (buffer volátil):** en módulo remoto (VO2) + staging en transceptor (DDR).
- **M3 (trim/máscara):** en módulo remoto (azobenceno/espiropirano).

El host ve **memoria unificada** (API OpenCL) pero físicamente está en el módulo remoto. El transceptor gestiona transferencias DMA H2D/D2H de forma transparente.

---

## 4. Módulo fotónico remoto (diseño actualizado)

### 4.1 Función
Ejecutar cómputo fotónico (MVM, conv, activaciones) con memoria integrada (M0–M3). **No tiene interfaz PCIe directa.**

### 4.2 Arquitectura interna

| Submódulo | Función | Tecnología |
|---|---|---|
| **Backplane óptico** | Distribución WDM, acopladores, splitters | SiPh (SiN/Si) |
| **Tiles MZI (M0)** | Cómputo (MVM, conv) | MZIs con PCM/EO |
| **Celdas PCM (M1)** | Pesos NV (Sb2S3) | PCM fotónica |
| **Celdas VO2 (M2)** | Buffer volátil, gating | VO2 térmico |
| **Celdas trim (M3)** | Calibración, máscaras | Azobenceno/espiropirano |
| **Control local** | OMCC, calibración autónoma, telemetría | FPGA/MCU + firmware |
| **Refrigeración** | Disipación térmica | Cold plate + Fluorinert o aire forzado |

### 4.3 Interfaz óptica con transceptor

- **Entrada:** fibra monomodo con λs de datos (ej. 1550 nm C-band) y λs de control (365/450/520/650/800 nm).
- **MUX/DEMUX:** separa λs de datos y control, distribuye a tiles.
- **Acopladores:** lentes/GRIN para margen de alineación ±5 µm (IL 0.5–1.5 dB).

### 4.4 Refrigeración

| Opción | Capacidad disipación | Complejidad | Coste |
|---|---|---|---|
| **Aire forzado** | 100–200W | Baja | $50–200 |
| **Cold plate (agua)** | 200–500W | Media | $200–1000 |
| **Inmersión (Fluorinert)** | 500–1000W | Alta | $1000–5000 |

**Recomendación:** cold plate para prototipo (balance coste/complejidad). Inmersión para producción si duty-cycle PCM >0.5.

### 4.5 Control local autónomo

El módulo remoto tiene su propio **FPGA/MCU** que ejecuta:
- **OMCC:** scheduling térmico, wear-leveling, re-mapeo.
- **Calibración en lazo cerrado:** ajusta actuadores (TEC, calentadores PCM, EO) sin intervención del host.
- **Telemetría:** reporta temperatura, potencia óptica, BER proxy, desgaste PCM al transceptor cada N ms.

**Ventaja:** reduce latencia de control (no necesita ida y vuelta por fibra para cada ajuste).

---

## 5. Impacto en candidatos

| Candidato | Cambio con disaggregated | Prob. éxito anterior | Prob. éxito nueva |
|---|---|---|---|
| **H3** 2.5D | Térmica resuelta (refrigeración líquida), yield alto (chip grande o múltiples pequeños) | 55–70% | **70–85%** |
| **G3** 2.5D | Térmica resuelta, pero co-integración PCM+EO sigue siendo reto | 45–65% | **60–75%** |
| **G2** 2.5D | Ya era bueno en térmica (EO), beneficio menor | 50–65% | **55–70%** |
| **H1** 3D | 3D sigue siendo reto, pero menos urgente (puedes usar múltiples H3 en paralelo) | 25–45% | **35–55%** |
| **H4** 3D | Similar a H1 | 15–35% | **25–45%** |

---

## 6. Nuevos riesgos de arquitectura disaggregated

| # | Riesgo | Impacto | Prob. | Mitigación |
|---|---|---|---|---|
| D1 | **Latencia de fibra** (~10 ns/m ida y vuelta) | Medio | Baja | Negligible vs latencia E2E (0.16–12 ms). Control local en módulo remoto para lazos rápidos. |
| D2 | **Pérdidas de conectores** (0.2–0.5 dB c/u, 2–4 conexiones) | Bajo-Medio | Media | Total 0.4–2 dB. Conectores APC/UPC de baja pérdida, limpieza estricta. |
| D3 | **Fiabilidad mecánica de fibra** (suciedad, doblez, vibración) | Bajo | Media | Conectores con latch, cable management, inspección periódica. |
| D4 | **Coste de fibra + transceptores** | Bajo | Baja | $200–2000 adicional (vs $3600–12000 del módulo). <20% del coste total. |
| D5 | **Sincronización host-módulo** | Medio | Baja | Protocolos PTP/SyncE o diseño asíncrono con buffers. |
| D6 | **Complejidad de dos subsistemas** | Medio | Media | Transceptor + módulo remoto requieren integración y pruebas separadas. |

---

## 7. Plan de implementación actualizado

### Fase 1: Transceptor PCIe (6–12 meses)
1. **Especificación:** mapa BAR/CSR, formato descriptores, protocolo colas.
2. **Plataforma FPGA:** PCIe Gen4 x8, DMA, DDR4, MSI-X.
3. **E/O-O/E:** módulos eval con láseres WDM + PDs.
4. **Firmware:** Command Processor, DMA scatter-gather, colas.
5. **Driver/Runtime:** KMD Linux, runtime OpenCL mínimo.

### Fase 2: Módulo fotónico remoto (12–24 meses)
1. **Backplane óptico:** MUX/DEMUX WDM, acopladores.
2. **Chips fotónicos 2.5D:** tiles MZI + PCM (H3) o PCM+EO (G3).
3. **Control local:** FPGA/MCU con OMCC, calibración autónoma.
4. **Refrigeración:** cold plate + sensores térmicos.
5. **Integración:** transceptor + fibra + módulo remoto.

### Fase 3: Sistema completo (18–30 meses)
1. **End-to-end:** host → transceptor → fibra → módulo → host.
2. **OpenCL/OpenVINO:** ICD OpenCL funcional, plugin OpenVINO (heterogéneo o nativo).
3. **Validación:** SI/PI, térmica, precisión numérica, RAS, estrés PCIe/DMA.
4. **Optimización:** duty-cycle PCM, calibración, yield.

---

## 8. Presupuesto de enlace actualizado

Con arquitectura disaggregated:

| Componente | IL (dB) | Notas |
|---|---|---|
| Acoplador transceptor → fibra | 0.5–1.5 | Lentes/GRIN, ±5 µm |
| Fibra (1–5 m) | <0.01–0.05 | Monomodo, baja pérdida |
| Conectores (2–4) | 0.4–2.0 | APC/UPC |
| MUX/DEMUX en módulo | 1.0–3.0 | AWG o filtros |
| Ruta óptica en módulo (H3) | 8.0–10.0 | MZIs + PCM + cruces |
| **Total IL (H3)** | **10.0–16.5** | vs 10.4 dB original (tarjeta integrada) |
| **Margen enlace (H3)** | **8.6–14.6 dB** | vs 10.6 dB original (sigue siendo >3 dB) |

**Conclusión:** IL aumenta 0–6 dB por conectores/fibra/MUX, pero margen sigue siendo suficiente (>3 dB). Si IL >14 dB, aumentar potencia láser o mejorar acopladores.

---

## 9. Recomendaciones

1. **Adoptar arquitectura disaggregated como diseño base.**
2. **Priorizar H3 2.5D** con módulo remoto y refrigeración líquida (probabilidad de éxito 70–85%).
3. **Desarrollar transceptor PCIe primero** (6–12 meses, menor riesgo, valida interfaz host).
4. **Módulo remoto en paralelo** (12–24 meses, mayor riesgo, requiere fotónica madura).
5. **Posponer 3D (H1/H4)** hasta validar 2.5D disaggregated.
6. **Búsqueda FTO específica** antes de fabricación (transceptor + módulo fotónico).

---

*Documento conceptual; no constituye asesoría legal, ni diseño listo para fabricación, ni garantía de rendimiento/FTO.*


## 5. OEM Thermal Immersion Stabilizer (OEM: Optical Engine Module)

Basado en la arquitectura desagregada, el módulo fotónico puede sumergirse en un tanque de inmersión para estabilizar térmicamente su operación. El transceptor (Nivel 1, electrónico) se referencia de forma convencional dentro del servidor; el módulo óptico (Nivel 3) se sumerge. El módulo es puramente pasivo/óptico: el calor se genera en:
1. Escritura de memoria y calibración (pulso de calor al estado PCM/VO2).
2. El flujo de datos produce cambios de n mínimos, pero la deriva térmica de guías poliméricas (dn/dT alta) puede desalibrar MZI.

### Requisitos técnicos del tanque de inmersión

| Parámetro | Requisito | Notas |
|---|---|---|
| Transparencia óptica | ≥99% a 650 nm (PCM write) y 1530–1565 nm (datos), 800/365/450/520 nm (control/trim) | Novec 7100/7200: transparentes en visible/NIR; agua desiacturred: transparente en 650 nm, no en 1550 nm. |
| Dieléctrico | σ < 10⁻⁴ S/m (idealmente >10⁵ Ω·cm) | Sin cortocircuitos por condensación. |
| Viscosidad | ≤ 2 cP | Baja para enfriamiento efectivo. |
| Conductividad térmica | ≥ 0.6 W/mK | (Novec 7100/7200 ~0.5–0.7 W/mK). |
| Compatibilidad con polímeros | Δn frente a guías (PMMA, PS, Zeonex, Topas, fluorocarbohidratos) | Verificar antes de diseñar conexiones; fluidos fluorados: Δn ≈ 0. |
| Temperatura operativa | Módulo: 10–50 °C (Sb2S3/VO2; VO2 68 °C); ±0.1–0.5 °C estabilidad | Setpoint según perfil. |
| Disipación | Control PID: velocidad de recirculación + potencia de calentadores | Valores objetivo: 3-8 W/mod est. ρPTC. |
| Environmental | N2 blanket opcional; filtros secos | Reducir absorción de agua en juntas. |

Candidatos (verificar especificaciones en fuentes):
- **3M Novec 7100/7200:** dieléctricos, transparentes en visible/NIR, baja viscosidad (~0.9–1.2 cP), ~0.5–0.7 W/mK.
- **Agua desiacturred + inhibidores (módulos sin láseres 1550 nm en immersion):** transparente en 650 nm (PCM write).
- **Aceites de silicona fluidos:** transparentes, Δn ≈ 0.02–0.08 (dar margen).

### Control térmico

1. **Margen operativo:** módulo a 10–50 °C; ±0.1–0.5 °C de estabilidad del parámetro.
2. **Sensores:** RTD/TC enchufados en el tanque; bucle PID con velocidad de recirculación + caldera.
3. **Conexiones ópticas herméticas:** conectores MPO/APC sellados; ninguna gota de líquido en juntas ópticas.
4. **Termodrenado:** ventiladores de tanque; radiadores de radiación; sensor de temperatura ambiente.
5. **Protocolos de calibración:** estado de la memoria PCM (M1) verificado periódicamente; reseteo si desviación >5%.

### Interfaz de operación

1. **Datos ópticos:** ritmo 0.5–5 m; fusiones: 90–95% - varía con fluido.
2. **Perfiles térmicos:** parámetros de punto de referencia conectables (logging perfil de cada modo, ±0.5 °C calibrado).
3. **Alertas:** telemetría remota (temperatura del módulo, caudal, descalibración de fase), interfaz de calibración.
