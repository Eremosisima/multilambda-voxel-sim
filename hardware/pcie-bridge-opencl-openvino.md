# Electrónica de compatibilización PCIe — OPGPU (OpenCL y OpenVINO)

> **Estado:** diseño de referencia conceptual (v0.8). Define la electrónica de borde que compatibiliza el plano fotónico OPGPU con un host por **PCIe** y lo expone como acelerador para **OpenCL** y (cuando sea posible) **OpenVINO**.  
> **Dominio público (objetivo declarado):** esquemáticos e instrucciones de uso libre para todo el mundo, publicados como **arte previo/divulgación defensiva** para dificultar apropiación registral por terceros (ver `../PUBLIC_DOMAIN_DEDICATION.md`; dedicación efectiva CC0 1.0 sujeta a ajustes por titulares; sin garantía absoluta).  
> **Aviso:** no es un diseño eléctrico/mecánico listo para fabricación ni certificación (PCIe, EMC, seguridad). Requiere SI/PI, validación térmica, firmware/software, y pruebas formales. PCIe, OpenCL y OpenVINO son marcas/nombres nominativos; la conformidad/compatibilidad real depende de la implementación, CTS/conformance y del ecosistema de drivers/plugins soportado.  
> **Licencias (vigentes en esta versión):** CERN-OHL-S v2 (hardware), Apache-2.0 (firmware/software), CC BY-SA 4.0 (documentación) — ver plan de transición a dominio público.

## 1. Objetivos y alcance

- **Transporte/compatibilidad física:** endpoint PCIe robusto (Gen4 x8/x16 objetivo, con opción Gen3 para prototipo) con DMA, MSI/MSI-X y BARs MMIO.
- **Puente de dominio:** conversión y temporización entre dominio eléctrico (host/PCIe) y fotónico (E/O, O/E, microsecuenciador, OMCC).
- **Modelo OpenCL:** exponer plataforma/dispositivo, colas de comandos, memoria jerárquica (mapeada a M0–M3), eventos/IRQ y ejecución de kernels (microprogramas ópticos) vía runtime/driver.
- **Camino OpenVINO:** habilitar ejecución de redes (inferencia) a través de un **plugin/dispositivo OpenVINO** que se apoya en el driver/runtime del acelerador (directo o vía backend OpenCL), sujeto a cobertura de operadores y precisión.
- **Modularidad:** interfaz estable hacia el módulo fotónico intercambiable (H3/G2/G3/H1/H4, etc.).

## 2. Arquitectura electrónica de borde (esquemático de bloques)

```text
                                   HOST (CPU + RAM)
                                          |
                               PCIe x8/x16 (Gen3/4/5 objetivo)
                                          |
+-----------------------------------------v------------------------------------------+
|  TARJETA / BORDE ELECTRÓNICO (dominio digital + potencia + SI/PI)                 |
|                                                                                    |
|  [Conector edge PCIe] -> [Retimers/Redrivers (si aplica)] -> [PCIe PHY/SerDes]    |
|                                                                     |              |
|                                                          [PCIe Controller/EP]      |
|                                                                     | (AXI/IF)     |
|  [Flash/QSPI boot]   [DDR4/DDR5/HBM buf (opt)]   [CLK/PLL]   [Sensores T/V/I]     |
|         \                 |           |               |             /               |
|          \                v           v               v            /                |
|           +------> [SoC de control: FPGA/ASIC (+MCU) ] <---------+                |
|                     |  - DMA engines (SG)         |                                 |
|                     |  - Command Processor (CP)   |  BAR0 CSRs/MMIO, MSI/MSI-X      |
|                     |  - OMCC (mem/ctrl/RAS)      |  BAR1 aperturas M0-M3           |
|                     |  - Scheduler/colas          |  (BAR2 doorbells rápidos, opt)   |
|                     |  - Calibración/telemetría   |                                 |
|                     +----+-----------+------------+                                |
|                          |           |            |                                 |
|                    [Micro-     [TX E/O:     [RX O/E:                               |
|                     secuenc.]   DAC/drv +    PD/TIA/ADC                           |
|                          |      láseres +     + CDR/sincro]                        |
|                          |      moduladores]      ^                                 |
|                          |           |            |                                 |
+--------------------------|-----------|------------|---------------------------------+
                           |           |            |      (acoplador/interposer/fibra)
+--------------------------v-----------v------------v---------------------------------+
|  MÓDULO FOTÓNICO (intercambiable): distribución WDM/λc, tiles/celdas, M0-M3,       |
|  actuadores EO/térmicos/PCM, sensado óptico/térmico, ruta de calor                |
+------------------------------------------------------------------------------------+
  Alimentación: 12V/3.3V edge + POL -> rails (FPGA/core, SerDes, láseres/drivers, TEC)
  Térmica: spreader + disipador/cold plate + control ventilador/TEC
```

### 2.1 Opciones de implementación (prototipo a producto)

| Bloque | Prototipo (rápido) | Integración (eficiencia/coste) | Notas |
|---|---|---|---|
| PCIe + control | FPGA con PCIe hard IP (p. ej. familia Xilinx/AMD UltraScale+, Intel Agilex; uso nominativo) + soft DMA/CP/OMCC | ASIC/SoC con PCIe EP + aceleradores fijos | Prototipo prioriza flexibilidad de microsecuencias/protocolos |
| Memoria de staging | DDR4 SODIMM/on-board | DDR5/HBM2e on-package (según coste) | Buffers, colas, firmware, tablas de calibración |
| Host MCU (opcional) | MCU para bring-up/gestión | Integrado en SoC | Monitorización, arranque seguro, actualización |
| E/O-O/E | Módulos/driver eval + fotónica externa | PIC + drivers integrados/co-packaged | Depende del candidato (H3/G2/G3/H1/H4) |

## 3. Interfaz PCIe, BAR/MMIO y flujo de comandos

### 3.1 Configuración PCIe (objetivo)
- **EP** con soporte de **DMA scatter-gather**, **MSI/MSI-X** (múltiples vectores: colas, errores, telemetría), **ACS/ATS opcional** (SVM futura), **SR-IOV opcional** (multi-contexto futuro).
- **Link:** iniciar en Gen3/Gen4 x8 para bring-up; escalar a Gen4/Gen5 x16 según margen SI y necesidad de BW.
- **Resets/errores:** FLR, manejo de AER, timeouts y recuperación; telemetría expuesta por CSRs.

### 3.2 Mapa BAR/CSRs (contrato de referencia)

| Región | Tamaño (ref.) | Contenido |
|---|---:|---|
| **BAR0 (MMIO, 64-bit)** | 64 KB–1 MB | ID/capacidades, versión FW, estado/link, control reset/power, **doorbells** de colas, punteros/head-tail o índices AQL-like, MSI-X table/PBA o punteros, control de reloj/térmica, logs/telemetría, ventana de registros OMCC |
| **BAR1 (apertura, 64-bit, opt.)** | configurable | Ventana a regiones M0–M3/diagnóstico mediante ventanas deslizantes (no mapeo directo completo), acceso de depuración/calibración |
| **BAR2 (doorbells rápidos, opt.)** | 4–64 KB | Registros de submit de baja latencia para kernels pequeños/micro-batches |

**CSRs mínimos (ejemplo):**
- `DEV_ID`, `FW_VER`, `CAP0` (nº colas, nº CUs/tiles, BW, modos GPU/NPU/TPU, tamaños M0–M3, precisión soportada)
- `STATUS`, `ERR_*`, `TEMP_*`, `POWER_*`
- Por cola `q`: `Q_BASE_LO/HI`, `Q_SIZE`, `Q_HEAD`, `Q_TAIL`, `Q_DOORBELL`, `Q_CTRL`
- `OMCC_CMD/STS`, `CALIB_*`, `RAS_*` (contadores desgaste/ECC, estado verificación)

### 3.3 Modelo de colas y comandos (OpenCL-compatible)
- Colas tipo **ring buffer** en memoria host con descriptores de: transferencia DMA (H2D/D2H), carga/actualización de pesos (M1), configuración de rutas/máscaras (M0/M3), lanzamiento de kernel, barrera/evento, calibración.
- **Flujo:** runtime escribe descriptor + buffer → doorbell MMIO → CP/OMCC fetch DMA → traduce a microsecuencias ópticas/temporización → ejecución en plano fotónico → O/E + escritura de resultado/completion → **MSI-X/evento**.
- **Sincronización:** eventos y fences mapeados a puntos de commit (fin de escritura PCM/estado volátil y fin de lectura O/E) para coherencia explícita.

## 4. Cadena de señal y conversión E/O-O/E

```text
Datos host (tensores/activaciones)
   -> [DMA in + formato/tiling OMCC/CP] -> [colas de frames]
   -> [TX: serializador + DAC/driver] -> [moduladores/λs] ==óptico==> [núcleo + M0-M3]
   -> [PD] -> [TIA] -> [ADC/CDR] -> [deframing + verificación/CRC opcional]
   -> [DMA out + completion/evento] -> host

Control: [microsecuenciador] -> drivers láser/pulso (650, 800, 365/450/520, EO/térmico)
                          -> actuadores térmicos/TEC (lazos locales) + sensado
```

**Consideraciones de diseño:**
- **Reloj/temporización:** PLL/reloj de referencia común para PCIe, DMA, microsecuenciador y ADC; alineación fina por trimming (M3/azobenceno) y calibración.
- **Presupuesto de enlace:** potencia óptica, IL por elemento/acoplo, sensibilidad RX, márgenes WDM; telemetría de potencia/BER proxy.
- **Integridad:** CRC en tramas de borde, lectura de verificación post-escritura (PCM/fotoquímicos), contadores RAS.
- **Aislamiento de dominios:** fallos ópticos/térmicos no deben colgar PCIe; watchdog, quarantining de tiles/celdas y reportes de error.

## 5. Potencia, térmica y SI/PI (factibilidad electrónica)

| Dominio | Requisitos clave | Implementación de referencia |
|---|---|---|
| **Potencia** | Rails para FPGA/SoC, SerDes, DDR, láseres, drivers E/O, TEC/calentadores | 12V/3.3V desde slot/aux → POL (buck/LDO), secuenciado, telemetría I/V, protección OCP/OVP |
| **SI (PCIe/DDR/SerDes)** | Impedancia controlada, pérdidas, retorno, diafonía | Stackup controlado, routing diferencial, vías backdrill/HDI según velocidad, retimers si margen bajo, validación con simulación SI |
| **PI** | Ruido y transitorios (drivers/láseres, switching) | Plano sólido, desacoplo jerárquico, PDN target impedance, separación de dominios sensibles |
| **Térmica** | Disipación de FPGA/SerDes/drivers y, crítico, control del módulo fotónico | Spreader + heatsink/cold plate, sensores, PWM ventilador/TEC, lazos y **scheduling térmico OMCC** |
| **Seguridad** | Láser y alta temperatura local (PCM ~300 °C) | Encapsulado/clase láser, interlocks, límites firmware, sensores de temperatura |

> La viabilidad térmica del módulo fotónico (aislamiento 300 °C vs 68 °C, trincheras, spreading) es co-requisito; ver `hardware/manufacturable-dimensions-and-ai-accelerators.md`.

## 6. Stack de software para OpenCL

```text
Aplicación OpenCL
   -> [OpenCL ICD Loader]
      -> [OPGPU OpenCL ICD / Driver de usuario]
         -> [Compiler backend: OpenCL C/SPIR-V -> microprograma óptico + plan de tiling/memoria]
         -> [Runtime: colas, buffers, eventos, mapeo M0-M3, sincronización]
            -> [KMD / driver de kernel: PCIe BAR/MMIO, DMA, MSI-X, resets, memoria]
               -> [Firmware CP/OMCC en borde] -> [Plano fotónico]
```

**Componentes a implementar (Apache-2.0 recomendado para software):**
- **KMD:** descubrimiento PCIe, gestión de BARs, asignación DMA coherente, ISR/MSI-X, gestión de energía/reset, interfaz ioctl/uAPI.
- **Runtime/ICD:** objetos OpenCL (platform/device/context/queue/buffer/program/kernel/event), construcción de descriptores y submission, gestión explícita de memoria y coherencia por commit.
- **Compilador (incremental):** ingerir SPIR-V/LLVM IR, particionar ops soportadas (GEMM/GEMV/conv→im2col+GEMM, punto a punto, reducciones acotadas), asignar tiles/M1/M2, generar microprograma; **fallback** a host/CPU para kernels no soportados.
- **Telemetría/extensiones vendor:** consultas de temperatura, desgaste M1, precisión efectiva, perfiles de potencia/latencia.

**Niveles de soporte (realistas):**
1. **Nivel 1 (prototipo):** dispositivo "custom" con API propia + runtime mínimo; kernels precompilados (matmul/conv) demostrables.
2. **Nivel 2 (OpenCL funcional):** ICD que pasa subconjunto relevante de pruebas (no CTS completo inicialmente), memoria explícita, formatos cuantizados/FP16 según precisión analógica.
3. **Nivel 3 (conformidad):** trabajo de CTS, completitud de built-ins y semántica; dependiente de madurez del compilador y precisión.

## 7. Compatibilidad con OpenVINO (camino de integración)

OpenVINO ejecuta modelos (IR: `.xml/.bin`) mediante un **plugin** de dispositivo que compila/ejecuta operadores sobre un backend. Para OPGPU, opciones:

| Opción | Descripción | Viabilidad | Esfuerzo | Rendimiento |
|---|---|---|---:|---:|
| **A. Plugin OpenVINO nativo (recomendado a medio plazo)** | Implementar plugin que traduce subgrafos soportados (MatMul/Conv/FullyConnected y patrones de inferencia) a microprogramas OPGPU vía runtime propio | Alta si el runtime/driver es estable | Alto | Mejor (control directo, fusión/tiling) |
| **B. Vía backend OpenCL de OpenVINO** | Usar el plugin OpenCL existente de OpenVINO apuntando al ICD OPGPU (dispositivo OpenCL) | **Condicionada**: requiere ICD OpenCL suficientemente compatible y kernels/precisiones que el plugin OpenCL genere y que el compilador OPGPU soporte | Medio | Media (depende de genericidad) |
| **C. Heterogéneo (fallback CPU/GPU)** | OPGPU ejecuta ops soportadas; resto cae a CPU u otro dispositivo vía hetero/plugin | Alta (pragmática) | Medio | Depende de partición |
| **D. Import de red precompilada** | Cargar blobs/microprogramas ya compilados para topologías objetivo | Alta para demos | Bajo-medio | Buena en casos fijos, poca flexibilidad |

**Recomendación de ruta:**
1. **Corto plazo:** (C)+(D) para demostrar inferencia (p. ej. MLP/conv simples, INT8/FP16) con partición y blobs; validar precisión efectiva y latencia E2E.
2. **Medio plazo:** (B) si se alcanza Nivel 2 OpenCL, como puente rápido; en paralelo desarrollar (A) para operadores y cuantización nativos.
3. **Consideraciones clave:** OpenVINO asume semántica y precisión de sus backends; la naturaleza analógica/ruido/deriva de OPGPU exige cuantización calibrada, verificación y declaración clara de exactitud (no bit-exact con CPU/GPU).

## 8. Plan de implementación (electrónica + software)

1. **Especificación congelada (IF v0):** mapa BAR/CSR, formato de descriptores, protocolo de colas/eventos, interfaz módulo fotónico (eléctrica/óptica/térmica).
2. **Plataforma de prototipo:** FPGA con PCIe + DDR + mezzanine E/O-O/E; bring-up de link (LTSSM), DMA loopback y MSI-X.
3. **Firmware borde:** CP, motor DMA SG, microsecuenciador, OMCC básico (mapeo M0–M3, scheduling térmico, verificación).
4. **KMD + runtime mínimo + API propia:** ejecución de microprogramas/kernels precompilados (GEMM) end-to-end.
5. **ICD OpenCL (Nivel 1→2):** buffers/colas/eventos, compilación de subconjunto de ops, fallback host.
6. **Integración OpenVINO (C/D → B/A):** partición heterogénea y/o plugin, validación de precisión/rendimiento en modelos objetivo.
7. **Validación:** SI/PI, térmica, estrés PCIe/DMA, precisión numérica vs referencia, RAS/endurance, seguridad láser/térmica.
8. **Endurecimiento:** AER/robustez, actualizaciones seguras de firmware, telemetría, y (si aplica) camino a conformidad.

## 9. Checklist de verificación

- [ ] PCIe enumera, entrena al ancho/velocidad objetivo y pasa pruebas de DMA/estrés sin errores AER.
- [ ] MSI/MSI-X y doorbells operan bajo carga con latencia acotada.
- [ ] Ruta E2E: host → DMA → microsecuencias → E/O → cómputo óptico → O/E → DMA → host correcta.
- [ ] Control térmico mantiene VO₂/zonas sensibles < umbral y secuencia escrituras PCM (300 °C) sin disturb.
- [ ] Calibración/RAS (verificación, contadores, degradación manejada) operativos.
- [ ] Runtime/ICD ejecuta kernels soportados con coherencia de eventos/memoria.
- [ ] Demo OpenVINO (heterogénea o nativa) con métricas de exactitud y latencia reportadas.

## 10. Referencias internas

- `hardware/opencl-compatibility.md` (mapeo OpenCL/memoria/colas)
- `hardware/coprocessor-and-improvements.md` (OMCC)
- `hardware/current-strategies-schematics-and-instructions.md` (estrategias/candidatos/módulos)
- `hardware/schematics-deep-dive.md`, `hardware/open-photonic-gpu-v1-schematic-pcie.md` (esquemáticos de borde/sistema)
- `hardware/manufacturable-dimensions-and-ai-accelerators.md` (térmica/dimensiones fabricables)
- `simulate_opgpu_system.py`, `outputs/opgpu_system_*` (simulación de sistema)