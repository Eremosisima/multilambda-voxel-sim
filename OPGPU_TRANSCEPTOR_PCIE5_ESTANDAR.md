# OPGPU Transceptor PCIe 5.0 — Estándar Abierto para Aceleradores Fotónicos

> **Versión:** 1.0-draft (2026-11-19)
> **Estado:** especificación conceptual. No es diseño listo para fabricación.
> **Objetivo:** definir un estándar abierto para transceptores PCIe 5.0 que permitan comunicación entre hosts (CPU/GPU/NPU) y módulos fotónicos OPGPU reconfigurables vía fibra óptica.
> **Base estándar:** OpenCL 3.0 (Khronos) para compatibilidad multi-vendor y aceleradores heterogéneos.
> **Dominio público (intención CC0 1.0):** especificación abierta para facilitar adopción y dificultar apropiación registral.

---

## 1. Visión y alcance

### 1.1 Propósito
Definir una interfaz estándar para **transceptores PCIe 5.0** que actúen como puente entre hosts electrónicos (CPU/GPU/NPU convencionales) y **módulos fotónicos OPGPU reconfigurables**. El estándar permite:

- **Interoperabilidad:** cualquier host con driver OpenCL puede comunicarse con cualquier módulo fotónico OPGPU compatible.
- **Reconfiguración:** cambiar el módulo fotónico (H3, G3, G2, H1, H4) sin modificar el host o el driver.
- **Escalabilidad:** soportar desde módulos pequeños (edge) hasta grandes (datacenter) con la misma interfaz.
- **Evolución:** versiones futuras pueden añadir capacidades (PCIe 6.0, más canales WDM, nuevos materiales fotónicos) manteniendo compatibilidad hacia atrás.

### 1.2 Casos de uso
1. **Aceleración de inferencia IA:** host ejecuta pre/post-procesamiento, módulo fotónico ejecuta MVM/convolución.
2. **Computación científica:** simulaciones numéricas (álgebra lineal, PDEs) offloaded al módulo fotónico.
3. **Procesamiento de señales:** FFT, filtrado, correlación en dominio óptico.
4. **Prototipado rápido:** investigadores cambian módulos fotónicos para evaluar diferentes estrategias (H3, G3, etc.) con el mismo host.

### 1.3 No-objetivos
- No define la implementación interna del módulo fotónico (eso lo define cada estrategia OPGPU).
- No define el software de aplicación (eso lo define el ecosistema OpenCL/OpenVINO).
- No define la fabricación de chips fotónicos (eso lo define cada foundry).

---

## 2. Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOST (CPU/GPU/NPU electrónico)                                              │
│   └── Aplicación OpenCL                                                     │
│        └── OpenCL Runtime (ICD Loader)                                      │
│             └── Driver OPGPU (KMD + UMD)                                    │
│                  └── PCIe 5.0 x8/x16 (eléctrico, <0.5 m)                    │
│                       └──┐                                                   │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────────────────┐
│ TRANSCEPTOR OPGPU (estándar abierto)                                        │
│                                                                             │
│   [Conector PCIe 5.0 edge]                                                  │
│        └── [PCIe 5.0 PHY/SerDes (32 GT/s por lane)]                        │
│             └── [PCIe Controller/EP: DMA, MSI-X, BARs]                      │
│                  └── [FPGA/SoC reconfigurable]                              │
│                         ├── Command Processor (CP)                          │
│                         ├── Scheduler/colas                                 │
│                         ├── Memoria staging (DDR5 8-32 GB)                  │
│                         ├── TX E/O: láseres WDM sintonizables              │
│                         └── RX O/E: PDs + TIA + ADC                         │
│                                                                             │
│   [Interfaz óptica estándar: conectores LC/APC o MPO]                      │
│        └── Fibra monomodo (0.5-5 m)                                         │
│             └──┐                                                             │
└─────────────────┼──────────────────────────────────────────────────────────┘
                  │
┌─────────────────┼──────────────────────────────────────────────────────────┐
│ MÓDULO FOTÓNICO OPGPU (reconfigurable, estrategia H3/G3/G2/H1/H4)         │
│                                                                             │
│   [Interfaz óptica estándar: conectores LC/APC o MPO]                      │
│        └── [Backplane óptico: MUX/DEMUX WDM, acopladores]                  │
│             └── [Chips fotónicos: MZI, PCM, EO, resonadores]              │
│                  └── [Control local: FPGA/MCU, OMCC, calibración]         │
│                       └── [Refrigeración: cold plate/Fluorinert]           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Especificación PCIe 5.0

### 3.1 Interfaz eléctrica

| Parámetro | Especificación | Notas |
|---|---|---|
| **Versión PCIe** | 5.0 (compatible con 4.0/3.0 hacia atrás) | 32 GT/s por lane (64 GB/s x16) |
| **Ancho de enlace** | x8 (bring-up), x16 (producción) | Negociación automática LTSSM |
| **Conector** | PCIe edge (CEM 4.0/5.0) | Low-profile o full-height según factor forma |
| **Alimentación** | 12V/3.3V desde slot, 6-pin aux opcional | 25-75W transceptor, módulo remoto tiene fuente externa |
| **Señalización** | NRZ (128b/130b encoding) | PAM4 opcional para PCIe 6.0 futuro |
| **Latencia PHY** | <10 ns | Incluye SerDes, PHY, controller |

### 3.2 Barra de direcciones (BARs) y registros

| BAR | Tamaño | Contenido |
|---|---|---|
| **BAR0 (MMIO, 64-bit)** | 1 MB | ID/capacidades, versión FW, estado/link, doorbells, punteros de colas, MSI-X table, control térmico/potencia, telemetría, ventana de registros de módulo remoto |
| **BAR1 (apertura, 64-bit)** | Configurable (hasta 4 GB) | Ventana a memoria staging DDR5 (para transferencias DMA directas) |
| **BAR2 (doorbells rápidos, opcional)** | 64 KB | Registros de submit de baja latencia para micro-batches |

**Registros CSR mínimos (BAR0):**

| Registro | Offset (ejemplo) | Descripción |
|---|---|---|
| `DEV_ID` | 0x000 | ID de dispositivo, versión hardware |
| `FW_VER` | 0x004 | Versión firmware transceptor |
| `CAP0` | 0x008 | Capacidades: nº colas, nº CUs/tiles, BW, modos GPU/NPU/TPU, tamaños M0-M3, precisión soportada |
| `STATUS` | 0x010 | Estado del link PCIe, errores, módulo conectado (sí/no), tipo de módulo (H3/G3/etc.) |
| `ERR_*` | 0x020-0x030 | Contadores de errores PCIe, DMA, ópticos |
| `TEMP_*` | 0x040-0x050 | Temperatura transceptor y módulo remoto |
| `POWER_*` | 0x060-0x070 | Potencia transceptor y módulo remoto |
| `Q_BASE_LO/HI` | 0x100+q*0x20 | Base de cola q (dirección física en staging DDR) |
| `Q_SIZE` | 0x108+q*0x20 | Tamaño de cola q (nº descriptores) |
| `Q_HEAD` | 0x110+q*0x20 | Puntero head de cola q (write-only desde host) |
| `Q_TAIL` | 0x118+q*0x20 | Puntero tail de cola q (read-only para host) |
| `Q_DOORBELL` | 0x120+q*0x20 | Doorbell para notificar nuevos descriptores |
| `Q_CTRL` | 0x128+q*0x20 | Control de cola q (enable, interrupt mode, priority) |
| `OMCC_CMD/STS` | 0x200-0x210 | Comando/estado para control de módulo remoto (calibración, wear-leveling) |
| `CALIB_*` | 0x220-0x240 | Parámetros de calibración del módulo remoto |
| `RAS_*` | 0x250-0x270 | Contadores de desgaste PCM, ECC, estado de verificación |

### 3.3 DMA y colas

- **DMA scatter-gather:** listas de descriptores en memoria staging DDR5.
- **Modelo de colas:** ring buffers con descriptores de:
  - Transferencia DMA (H2D/D2H): tensores de entrada/salida.
  - Carga/actualización de pesos (M1): escribir en PCM del módulo remoto.
  - Configuración de rutas/máscaras (M0/M3): programar MZIs/filtros.
  - Lanzamiento de kernel: ejecutar microprograma óptico.
  - Barrera/evento: sincronización.
  - Calibración: ajustar actuadores del módulo remoto.

**Flujo de comando:**
1. Host escribe descriptor en cola (staging DDR) → doorbell MMIO.
2. Command Processor (CP) en FPGA fetch descriptor → traduce a microsecuencias ópticas.
3. Microsecuencias → TX E/O → fibra → módulo remoto.
4. Módulo remoto ejecuta cómputo fotónico → RX O/E → DMA → staging DDR.
5. CP escribe completion en cola → MSI-X/evento → host.

### 3.4 Interrupciones (MSI-X)

- **Vectores MSI-X:** 8-32 vectores (configurable).
  - Vector 0: colas (completion de comandos).
  - Vector 1: errores PCIe/DMA.
  - Vector 2: telemetría (temperatura, potencia, BER).
  - Vector 3: eventos de módulo remoto (calibración completada, desgaste PCM).
  - Vectores 4-31: reservados para扩展/futuro.

---

## 4. Interfaz óptica estándar

### 4.1 Conectores y fibra

| Parámetro | Especificación | Notas |
|---|---|---|
| **Conector transceptor** | LC/APC (1-16 canales) o MPO (12/24 fibras) | APC para baja reflectancia (<-60 dB) |
| **Conector módulo remoto** | LC/APC o MPO (matching con transceptor) | Mismo tipo en ambos extremos |
| **Fibra** | Monomodo (SMF-28 o equivalente) | Baja pérdida (<0.2 dB/km @1550 nm) |
| **Longitud** | 0.5-5 m (estándar), hasta 100 m (extendido) | Latencia ~10 ns/m (ida y vuelta) |
| **Pérdida de enlace** | <0.5 dB (fibra) + 0.2-0.5 dB/conector | Total típico: 1-3 dB para 5 m |
| **Acoplamiento** | Lentes/GRIN en transceptor y módulo | Margen de alineación ±5 µm |

### 4.2 Longitudes de onda (WDM)

| Banda | λs (nm) | Uso | Canales |
|---|---|---|---|
| **C-band (datos)** | 1530-1565 | Datos de alta velocidad (host ↔ módulo) | 8-16 canales (spacing 100/200 GHz) |
| **650 nm** | 650 ±10 | Escritura/lectura PCM (Sb2S3) | 1-4 canales |
| **800 nm** | 800 ±10 | Conmutación VO2 | 1-2 canales |
| **365/450/520 nm** | 365/450/520 ±5 | Trim/calibración (azobenceno/espiropirano) | 1 canal c/u |

**Nota:** el transceptor debe tener láseres sintonizables o múltiples láseres fijos para soportar diferentes estrategias OPGPU (H3 usa PCM+WDM, G2 usa EO, etc.).

### 4.3 Presupuesto de enlace óptico

| Componente | IL (dB) | Notas |
|---|---|---|
| Acoplador transceptor → fibra | 0.5-1.5 | Lentes/GRIN, ±5 µm |
| Fibra (1-5 m) | <0.01-0.05 | Monomodo, baja pérdida |
| Conectores (2-4) | 0.4-2.0 | APC/UPC |
| MUX/DEMUX en módulo | 1.0-3.0 | AWG o filtros |
| Ruta óptica en módulo (H3) | 8.0-10.0 | MZIs + PCM + cruces |
| **Total IL (H3)** | **10.0-16.5** | Depende de estrategia y longitud |
| **Margen enlace (H3)** | **8.6-14.6 dB** | vs sensibilidad RX -20 a -10 dBm |

**Potencia óptica TX:** 0-10 dBm por λ (ajustable según IL del módulo remoto).

---

## 5. Reconfiguración de módulos fotónicos

### 5.1 Detección automática de módulo

Cuando se conecta un módulo fotónico, el transceptor debe:

1. **Detectar conexión:** sensor óptico/eléctrico en interfaz fibra.
2. **Leer identidad del módulo:** el módulo remoto tiene EEPROM/registro que expone:
   - Tipo de estrategia (H3, G3, G2, H1, H4).
   - Capacidades: nº tiles MZI, capacidad PCM (MB), canales WDM soportados, precisión (INT8/FP16).
   - Parámetros de calibración: IL típico, potencia óptica recomendada, duty-cycle PCM máximo.
3. **Cargar perfil de configuración:** el driver OpenCL carga el perfil correspondiente (nº colas, tamaños de buffers, microprogramas soportados).
4. **Notificar al host:** el driver expone el dispositivo OpenCL con capacidades actualizadas.

### 5.2 Perfiles de módulos (ejemplo)

| Estrategia | Tipo | M0 (cómputo) | M1 (pesos NV) | M2 (buffer) | M3 (trim) | λs datos | λs control | Duty PCM máx. |
|---|---|---|---|---|---|---|---|---|
| **H3** | Open WDM-PCM | MZI + WDM | Sb2S3 (160 MB) | VO2 (64 MB) | Azobenceno | C-band 8-16 λs | 650/800/365/450/520 nm | 0.5-1.0 |
| **G3** | PCM+EO híbrido | MZI + EO | Sb2S3 (256 MB) | VO2 (128 MB) | Azobenceno | C-band 8-16 λs | 650/800/365/450/520 nm + EO drivers | 0.5-1.0 |
| **G2** | EO puro | MZI + EO | N/A (volátil) | VO2 (192 MB) | Azobenceno | C-band 8-16 λs | 800/365/450/520 nm + EO drivers | N/A (sin PCM) |
| **H1** | 3D NV | MZI 3D + PCM | Sb2S3 (640 MB) | VO2 (256 MB) | Azobenceno | C-band 8-16 λs | 650/800/365/450/520 nm | 0.3-0.8 |
| **H4** | 3D tensor | MZI 3D + difractiva | Sb2S3 (720 MB) | VO2 (384 MB) | Azobenceno | C-band 8-16 λs | 650/800/365/450/520 nm | 0.3-0.8 |

### 5.3 Hot-swap (opcional)

- **Soporte hot-swap:** apagar módulo remoto, desconectar fibra, conectar nuevo módulo, encender.
- **Requisitos:** detección de desconexión, shutdown graceful (flush de colas, guardado de estado), reinicio de calibración.
- **Tiempo de reconfiguración:** <10 s (detección + carga de perfil + calibración inicial).

---

## 6. Estándar de software: OpenCL 3.0

### 6.1 Por qué OpenCL (vs OpenVINO)

**OpenCL 3.0 (Khronos) es más apropiado como base del estándar porque:**

1. **Madurez y adopción:** estándar desde 2008, soporte multi-vendor (AMD, Intel, ARM, NVIDIA via CUDA interop, Qualcomm, Imagination).
2. **Modelo de memoria explícita:** adecuado para arquitectura disaggregated (host y módulo remoto tienen memorias separadas).
3. **Flexibilidad:** soporta cómputo general (no solo inferencia IA), útil para scientific computing, signal processing, etc.
4. **Ecosistema de herramientas:** compiladores (LLVM/SPIR-V), profilers (CodeXL, VTune), debuggers.
5. **Extensibilidad:** extensiones vendor-specific para características OPGPU (telemetría, calibración, precisión analógica).

**OpenVINO es complementario pero no base del estándar porque:**
- Es específico para inferencia IA (no cómputo general).
- Está atado a hardware Intel (aunque soporta plugins de terceros).
- Asume semántica bit-exact (difícil con hardware analógico/fotónico).

### 6.2 Modelo de dispositivo OpenCL OPGPU

```c
// Plataforma OPGPU
cl_platform_id platform; // "OPGPU OpenCL Platform"
cl_device_id device;     // "OPGPU Photonic Accelerator (H3/G3/etc.)"

// Propiedades del dispositivo (clGetDeviceInfo)
CL_DEVICE_NAME: "OPGPU H3 Open WDM-PCM"
CL_DEVICE_VENDOR: "OPGPU Project"
CL_DEVICE_VERSION: "OpenCL 3.0 OPGPU v1.0"
CL_DRIVER_VERSION: "1.0.0"
CL_DEVICE_MAX_COMPUTE_UNITS: 64  // nº tiles MZI
CL_DEVICE_GLOBAL_MEM_SIZE: 160*1024*1024  // M1 PCM (bytes)
CL_DEVICE_LOCAL_MEM_SIZE: 64*1024*1024    // M2 VO2 (bytes)
CL_DEVICE_MAX_CLOCK_FREQUENCY: 2000  // MHz (optical clock)
CL_DEVICE_EXTENSIONS: "cl_opgpu_telemetry cl_opgpu_calibration"

// Colas de comandos
cl_command_queue queue = clCreateCommandQueue(context, device, CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE, &err);
```

### 6.3 Extensiones OPGPU propuestas

**Extensión `cl_opgpu_telemetry`:**
```c
// Consultar telemetría del módulo remoto
clGetDeviceInfo(device, CL_OPGPU_TEMPERATURE, sizeof(float), &temp, NULL);
clGetDeviceInfo(device, CL_OPGPU_POWER, sizeof(float), &power, NULL);
clGetDeviceInfo(device, CL_OPGPU_PCM_WEAR, sizeof(float), &wear, NULL);  // 0-100%
clGetDeviceInfo(device, CL_OPGPU_BER_PROXY, sizeof(float), &ber, NULL);
```

**Extensión `cl_opgpu_calibration`:**
```c
// Ejecutar calibración en módulo remoto
clEnqueueOPGPUCalibration(queue, CL_OPGPU_CALIBRATE_THERMAL, 0, NULL, &event);
clEnqueueOPGPUCalibration(queue, CL_OPGPU_CALIBRATE_PHASE, 0, NULL, &event);
clWaitForEvents(1, &event);
```

**Extensión `cl_opgpu_module_info`:**
```c
// Información del módulo conectado
clGetDeviceInfo(device, CL_OPGPU_MODULE_TYPE, sizeof(cl_int), &module_type, NULL);  // H3/G3/etc.
clGetDeviceInfo(device, CL_OPGPU_MODULE_WDM_CHANNELS, sizeof(cl_int), &wdm_ch, NULL);
clGetDeviceInfo(device, CL_OPGPU_MODULE_PCM_CAPACITY, sizeof(cl_ulong), &pcm_cap, NULL);
```

### 6.4 Flujo de ejecución OpenCL

```c
// 1. Crear contexto y cola
cl_context context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
cl_command_queue queue = clCreateCommandQueue(context, device, 0, &err);

// 2. Crear buffers (memoria explícita: host ↔ módulo remoto)
cl_mem buffer_input = clCreateBuffer(context, CL_MEM_READ_ONLY, size, NULL, &err);
cl_mem buffer_output = clCreateBuffer(context, CL_MEM_WRITE_ONLY, size, NULL, &err);
cl_mem buffer_weights = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, weights_size, weights, &err);

// 3. Transferir pesos a M1 (PCM) del módulo remoto
clEnqueueWriteBuffer(queue, buffer_weights, CL_TRUE, 0, weights_size, weights, 0, NULL, &event_write);

// 4. Ejecutar kernel (MVM/conv)
cl_kernel kernel = clCreateKernel(program, "matmul", &err);
clSetKernelArg(kernel, 0, sizeof(cl_mem), &buffer_input);
clSetKernelArg(kernel, 1, sizeof(cl_mem), &buffer_weights);
clSetKernelArg(kernel, 2, sizeof(cl_mem), &buffer_output);
clEnqueueNDRangeKernel(queue, kernel, 2, NULL, global_size, local_size, 0, NULL, &event_exec);

// 5. Leer resultado
clEnqueueReadBuffer(queue, buffer_output, CL_TRUE, 0, size, output, 0, NULL, &event_read);
clFinish(queue);

// 6. Consultar telemetría
float temp, power, wear;
clGetDeviceInfo(device, CL_OPGPU_TEMPERATURE, sizeof(float), &temp, NULL);
clGetDeviceInfo(device, CL_OPGPU_POWER, sizeof(float), &power, NULL);
clGetDeviceInfo(device, CL_OPGPU_PCM_WEAR, sizeof(float), &wear, NULL);
printf("Temp: %.1f°C, Power: %.1fW, PCM Wear: %.1f%%\n", temp, power, wear);
```

### 6.5 Compilador OpenCL → microprogramas ópticos

El compilador OPGPU convierte kernels OpenCL (SPIR-V/LLVM IR) a microprogramas ópticos:

1. **Frontend:** ingiere SPIR-V (desde OpenCL C/C++).
2. **Análisis:** identifica ops soportadas (GEMM, conv, punto a punto, reducciones).
3. **Partición:** asigna ops a tiles MZI del módulo remoto.
4. **Tiling/memoria:** mapea tensores a M0/M1/M2, genera transferencias DMA.
5. **Generación de microprogramas:** secuencias de pulsos ópticos (λs, timing, potencia).
6. **Fallback:** ops no soportadas → host CPU/GPU.

**Ops soportadas (nivel 1):**
- `clBLAS`-like: `clSgemm`, `clDgemm`, `clHgemm` (FP16).
- Convolución: `clConv2D` (im2col + GEMM).
- Punto a punto: suma, resta, multiplicación, ReLU, sigmoid.
- Reducciones: suma, max, min (acotadas).

**Ops futuras (nivel 2-3):**
- Attention (transformers): softmax, GEMM batched.
- FFT: `clFFT` integration.
- Sparse: SpMV, SpGEMM.

---

## 7. Especificaciones eléctricas, térmicas y mecánicas

### 7.1 Factor forma del transceptor

| Parámetro | Low-profile | Full-height |
|---|---|---|
| **Longitud** | <170 mm | <170 mm |
| **Altura** | 70 mm | 110 mm |
| **Slots** | 1 slot | 1-2 slots |
| **Conectores** | 1x LC/APC (datos) + 1x LC/APC (control) | 1x MPO (12/24 fibras) |
| **Potencia** | 25-50W | 50-75W |
| **Refrigeración** | Disipador pasivo + ventilador slot | Disipador pasivo + ventilador slot |

### 7.2 Especificaciones eléctricas

| Rail | Voltaje | Corriente máx. | Potencia |
|---|---|---|---|
| **12V (slot)** | 12V ±5% | 6A (75W) | 72W |
| **3.3V (slot)** | 3.3V ±5% | 2A | 6.6W |
| **6-pin aux (opcional)** | 12V ±5% | 6A (75W) | 72W |
| **Total transceptor** | - | - | 25-75W |

**Módulo remoto (fuente externa):**
| Rail | Voltaje | Corriente máx. | Potencia |
|---|---|---|---|
| **12V/48V (fuente externa)** | 12V o 48V ±5% | 10-20A | 120-960W |
| **Total módulo remoto** | - | - | 100-500W (típico) |

### 7.3 Especificaciones térmicas

| Componente | Temperatura operación | Temperatura almacenamiento |
|---|---|---|
| **Transceptor (FPGA/SerDes)** | 0-70°C | -20-85°C |
| **Módulo remoto (fotónica)** | 10-50°C (ambiente) | -20-85°C |
| **PCM (local en módulo)** | - | 300°C (escritura puntual) |
| **VO2 (local en módulo)** | - | 68°C (umbral conmutación) |

**Refrigeración módulo remoto:**
- **Aire forzado:** 100-200W, ventiladores 40-80mm.
- **Cold plate (agua):** 200-500W, flujo 1-2 L/min, temperatura entrada 20-30°C.
- **Inmersión (Fluorinert):** 500-1000W, tanque sellado.

### 7.4 Especificaciones mecánicas

**Transceptor:**
- Material: PCB FR4, disipador aluminio/cobre.
- Conectores: PCIe edge (oro), LC/APC (cerámica).
- Peso: 200-400g.

**Módulo remoto:**
- Material: chasis aluminio, backplane óptico SiPh, chips fotónicos Si/SiN.
- Conectores: LC/APC o MPO (cerámica).
- Peso: 2-10 kg (según factor forma y refrigeración).
- Factor forma: 1U-4U rack o standalone (desktop).

---

## 8. Plan de implementación

### Fase 1: Prototipo transceptor (6-12 meses)
1. **Especificación congelada:** este documento v1.0.
2. **Plataforma FPGA:** PCIe 5.0 x8, DDR5, MSI-X (Xilinx/AMD Alveo o Intel Agilex).
3. **E/O-O/E:** módulos eval con láseres WDM sintonizables + PDs.
4. **Firmware:** Command Processor, DMA scatter-gather, colas, detección de módulo.
5. **Driver OpenCL (nivel 1):** KMD Linux, runtime mínimo, kernels precompilados (GEMM).

### Fase 2: Módulo fotónico H3 (12-24 meses)
1. **Backplane óptico:** AWG comercial + splitters.
2. **Chips fotónicos 2.5D:** tiles MZI + PCM (Sb2S3).
3. **Control local:** FPGA con OMCC, calibración autónoma, telemetría.
4. **Refrigeración:** cold plate + agua.
5. **Integración:** transceptor + fibra + módulo H3.

### Fase 3: Ecosistema OpenCL (18-30 meses)
1. **ICD OpenCL (nivel 2):** buffers/colas/eventos, compilación de subconjunto de ops, fallback host.
2. **Extensiones OPGPU:** telemetría, calibración, información de módulo.
3. **Herramientas:** profiler, debugger, documentación.
4. **Certificación:** Khronos OpenCL conformance (opcional).

### Fase 4: Estándar abierto (24-36 meses)
1. **Publicar especificación:** este documento como estándar abierto (CC0 1.0).
2. **Registro en organismos:** Khronos, OCP (Open Compute Project), IEEE.
3. **Adopción multi-vendor:** foundries SiPh, fabricantes de transceptores, desarrolladores de software.
4. **Certificación de compatibilidad:** programa de certificación "OPGPU Compatible".

---

## 9. Compatibilidad con otros estándares

### 9.1 OpenVINO (complementario)
- **Plugin OpenVINO para OPGPU:** traduce subgrafos de inferencia (MatMul/Conv/Attention) a kernels OpenCL OPGPU.
- **Ventaja:** ecosistema Intel, modelos pre-entrenados, optimizaciones específicas de IA.
- **Desventaja:** atado a inferencia, no cómputo general.

### 9.2 CUDA (interop)
- **CUDA interop via OpenCL:** NVIDIA soporta interop OpenCL-CUDA (compartir buffers).
- **Ventaja:** ecosistema NVIDIA maduro, muchas aplicaciones CUDA existentes.
- **Desventaja:** atado a hardware NVIDIA, no estándar abierto.

### 9.3 SYCL (alternativa futura)
- **SYCL (Khronos):** estándar C++ para aceleradores heterogéneos (basado en OpenCL).
- **Ventaja:** más moderno, abstracción de mayor nivel, soporte multi-backend (OpenCL, CUDA, HIP).
- **Desventaja:** adopción aún limitada vs OpenCL.

**Recomendación:** base OpenCL 3.0 + extensiones OPGPU, con puente a OpenVINO para IA y SYCL como evolución futura.

---

## 10. Propiedad intelectual y dominio público

### 10.1 Intención CC0 1.0
Esta especificación se publica con intención de dominio público (CC0 1.0) para:
- Facilitar adopción amplia sin barreras de licencias.
- Dificultar apropiación registral por terceros (divulgación defensiva).
- Permitir que cualquier fabricante implemente transceptores/módulos compatibles.

### 10.2 Patentes
- **No garantías FTO:** la divulgación no garantiza libertad de operación frente a patentes de terceros.
- **Búsqueda FTO recomendada:** antes de fabricación comercial, realizar búsqueda de patentes en PCIe, WDM, PCM fotónica, MZI weight banks.
- **Defensive publication:** esta especificación crea prior art para dificultar patentes futuras sobre los conceptos aquí descritos.

### 10.3 Marcas
- "PCIe", "PCI Express" son marcas de PCI-SIG (uso nominativo).
- "OpenCL" es marca de Khronos Group (uso nominativo).
- "OpenVINO" es marca de Intel (uso nominativo).
- "OPGPU" es nombre del proyecto (sin registro de marca intención).

---

## 11. Referencias y recursos

### 11.1 Estándares relacionados
- **PCIe 5.0:** PCI-SIG, "PCI Express Base Specification Revision 5.0", 2019.
- **OpenCL 3.0:** Khronos Group, "OpenCL Specification", 2020.
- **WDM:** ITU-T G.694.1, "Spectral grids for WDM applications", 2020.
- **Fibra óptica:** IEC 60793-2-50, "Optical fibres - Part 2-50: Product specifications - Class B single-mode fibres", 2019.

### 11.2 Implementaciones de referencia
- **Transceptor:** Xilinx/AMD Alveo U50 (PCIe 5.0, OpenCL), Intel Agilex FPGA Development Kit.
- **Módulo fotónico:** AIM Photonics (SiPh foundry), TowerSemi (SiPh + PCM).
- **Herramientas:** Lumerical FDTD (óptica), COMSOL (térmica), Vivado/Quartus (FPGA).

### 11.3 Documentación del proyecto OPGPU
- Repositorio: https://github.com/Eremosisima/multilambda-voxel-sim
- Especificaciones de estrategias: `hardware/current-strategies-schematics-and-instructions.md`
- Análisis de riesgos: `ANALISIS_RIESGOS_POR_ESTRATEGIA.md`
- Arquitectura disaggregated: `ARQUITECTURA_DISAGGREGATED.md`

---

*Especificación conceptual; no constituye asesoría legal, ni diseño listo para fabricación, ni garantía de rendimiento/FTO. Publicada con intención de dominio público (CC0 1.0) como divulgación defensiva.*
