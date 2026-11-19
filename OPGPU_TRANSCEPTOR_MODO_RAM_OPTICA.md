# OPGPU Transceptor PCIe 5.0 — Modo RAM Óptica (Memory Extension)

> **Versión:** 1.0-draft (2026-11-19)
> **Estado:** especificación conceptual complementaria al documento `OPGPU_TRANSCEPTOR_PCIE5_ESTANDAR.md`.
> **Objetivo:** extender el transceptor OPGPU para que actúe también como **memoria extendida óptica** (RAM óptica) además de acelerador de cómputo, permitiendo al host usar la memoria del módulo fotónico (M1 PCM, M2 VO2) como memoria expandida con acceso directo.

---

## 1. Motivación

### 1.1 Problema
Los sistemas actuales tienen límites de memoria:
- **DRAM de host:** limitada a 512 GB-2 TB (servidores high-end), cara, consume ~5-10 W por módulo.
- **HBM (High Bandwidth Memory):** ~32-128 GB por GPU, muy cara (~$1000-3000 por stack), consume ~15-30 W.
- **Ancho de banda de memoria:** limitado por buses eléctricos (DDR5: ~100 GB/s por canal, HBM3: ~800 GB/s por stack).

### 1.2 Solución OPGPU RAM Óptica
Usar la memoria fotónica del módulo remoto (M1 PCM no volátil, M2 VO2 volátil) como **memoria extendida** del host:
- **Capacidad:** 160-720 MB por módulo (escala con más módulos).
- **Ancho de banda:** ~1-3 TB/s por módulo (WDM paralelo, acceso óptico).
- **Latencia:** ~100-500 ns (PCIe + fibra + acceso óptico), comparable a memoria remota (CXL/NUMA).
- **Persistencia:** M1 PCM es no volátil (retiene datos sin energía).
- **Eficiencia energética:** ~10-50× menor que DRAM por GB (fotones vs electrones, sin refresh en PCM).

### 1.3 Casos de uso
1. **Memoria expandida para IA:** modelos grandes (LLMs >100B params) que no caben en GPU RAM.
2. **In-memory databases:** datasets grandes que exceden DRAM del servidor.
3. **Checkpointing rápido:** guardar estado de aplicaciones en PCM (no volátil, alta velocidad).
4. **Shared memory distribuida:** múltiples hosts comparten memoria en módulos fotónicos.
5. **Persistent memory:** almacenamiento rápido con persistencia (alternativa a NVMe SSD).

---

## 2. Arquitectura de memoria

### 2.1 Jerarquía de memoria con OPGPU RAM Óptica

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOST (CPU/GPU)                                                              │
│                                                                             │
│   Registros (ns)                                                            │
│        ↓                                                                    │
│   L1/L2/L3 Cache (ns)                                                       │
│        ↓                                                                    │
│   DRAM local (DDR5, ~100 GB/s, 50-100 ns)                                   │
│        ↓                                                                    │
│   ┌────┴────────────────────────────────────────────────────────────────┐  │
│   │ CXL/PCIe 5.0 (eléctrico, <0.5 m)                                    │  │
│   └────┬────────────────────────────────────────────────────────────────┘  │
│        ↓                                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
         │
┌─────────────────────────────────────────────────────────────────────────────┐
│ TRANSCEPTOR OPGPU (modo RAM óptica)                                         │
│                                                                             │
│   [PCIe 5.0 Controller/EP: DMA, MSI-X, BARs]                               │
│        └── [Memory Controller óptico]                                       │
│               ├── Load/Store Unit (LSU): accesos directos a memoria remota  │
│               ├── Cache coherencia (opcional): snoop, directory-based       │
│               ├── Prefetcher: predicción de accesos                         │
│               └── Memory Scheduler: cola de requests, reordering            │
│                                                                             │
│   [TX E/O: láseres WDM sintonizables]                                       │
│        └── Fibra monomodo (0.5-5 m)                                         │
│             └──┐                                                             │
└─────────────────┼──────────────────────────────────────────────────────────┘
                  │
┌─────────────────┼──────────────────────────────────────────────────────────┐
│ MÓDULO FOTÓNICO OPGPU (memoria extendida)                                  │
│                                                                             │
│   [Backplane óptico: MUX/DEMUX WDM]                                         │
│        └── [Chips de memoria fotónica]                                      │
│               ├── M1: PCM (Sb2S3, no volátil, 160-720 MB, ~100 ns acceso)  │
│               └── M2: VO2 (volátil, 64-384 MB, ~10 ns acceso)              │
│                                                                             │
│   [Controlador de memoria local: FPGA/MCU]                                  │
│        ├── Arbitraje de accesos (lectura/escritura)                         │
│        ├── Wear-leveling (PCM)                                              │
│        ├── ECC/RAS (corrección de errores)                                  │
│        └── Telemetría (desgaste, temperatura, BER)                         │
│                                                                             │
│   [Refrigeración: cold plate/Fluorinert]                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Modos de operación

El transceptor OPGPU soporta **dos modos de operación** (configurable por software):

| Modo | Función | Latencia | Ancho de banda | Uso |
|---|---|---|---|---|
| **Acelerador (OpenCL)** | Ejecuta kernels fotónicos (MVM, conv, etc.) | 1-100 µs (depende de kernel) | 1-3 TB/s (interno) | Cómputo offloaded |
| **RAM Óptica (Memory Extension)** | Memoria extendida del host (load/store) | 100-500 ns | 100-500 GB/s (host↔módulo) | Almacenamiento de datos |

**Modo dual (futuro):** simultáneamente acelerador + RAM (partición dinámica de recursos).

---

## 3. Especificación de modo RAM óptica

### 3.1 Interfaz de memoria para el host

El transceptor expone la memoria del módulo remoto al host como:

1. **Memoria mapeada en espacio de direcciones (memory-mapped):**
   - El host ve la memoria del módulo como regiones de memoria física (similar a PCIe BARs).
   - Accesible vía load/store desde CPU (x86 `MOV` instrucciones) o GPU (CUDA/ROCm pointers).
   - Requiere soporte de sistema operativo (driver de memoria, page tables).

2. **Dispositivo de memoria (CXL-like):**
   - El transceptor aparece como dispositivo de memoria (similar a CXL Type 3).
   - El host usa APIs de memoria extendida (Linux `mmap`, Windows `VirtualAlloc`).
   - Soporte para coherencia de caché (opcional, depende de plataforma).

3. **API OpenCL (memoria explícita):**
   - `clCreateBuffer()` con flag `CL_MEM_USE_HOST_PTR` o `CL_MEM_ALLOC_HOST_PTR`.
   - Transferencias explícitas `clEnqueueReadBuffer()`/`clEnqueueWriteBuffer()`.
   - Menor overhead que memory-mapped, pero requiere copias explícitas.

### 3.2 Especificaciones de rendimiento

| Parámetro | M1 PCM (no volátil) | M2 VO2 (volátil) | DRAM (referencia) |
|---|---|---|---|
| **Capacidad por módulo** | 160-720 MB | 64-384 MB | 8-128 GB por módulo |
| **Latencia de lectura** | ~100-200 ns | ~10-50 ns | ~50-100 ns |
| **Latencia de escritura** | ~200-500 ns (PCM programming) | ~10-50 ns | ~50-100 ns |
| **Ancho de banda lectura** | 100-500 GB/s (por módulo) | 200-1000 GB/s (por módulo) | 50-100 GB/s por canal |
| **Ancho de banda escritura** | 50-250 GB/s | 200-1000 GB/s | 50-100 GB/s por canal |
| **Persistencia** | Sí (no volátil) | No (volátil) | No (volátil) |
| **Endurance** | ~10⁶ ciclos (PCM) | Ilimitado (VO2) | Ilimitado |
| **Consumo energético** | ~0.1-1 pJ/bit (lectura) | ~0.01-0.1 pJ/bit | ~10-50 pJ/bit |

**Latencia total (host → módulo remoto → host):**
- PCIe 5.0 round-trip: ~100-200 ns
- Fibra óptica (1-5 m): ~10-50 ns
- Acceso memoria fotónica: ~10-200 ns (depende de M1/M2)
- **Total:** ~120-450 ns (comparable a memoria remota NUMA/CXL)

### 3.3 Operaciones de memoria

#### 3.3.1 Load/Store directo (memory-mapped)

```c
// Ejemplo: acceso a memoria OPGPU desde CPU (Linux mmap)
int fd = open("/dev/opgpu_ram0", O_RDWR);
void* opgpu_ptr = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

// Leer/escribir directamente (load/store)
float* data = (float*)opgpu_ptr;
float value = data[0];  // Load desde M1/M2 (latencia ~100-500 ns)
data[0] = 42.0f;        // Store a M1/M2

// Ventaja: sin overhead de API, acceso directo desde CPU
// Desventaja: requiere coherencia de caché (snoop/invalidation)
```

#### 3.3.2 Transferencias explícitas (OpenCL)

```c
// Ejemplo: OpenCL memory transfer
cl_mem buffer = clCreateBuffer(context, CL_MEM_READ_WRITE, size, NULL, &err);

// Escribir desde host a módulo remoto (DMA)
clEnqueueWriteBuffer(queue, buffer, CL_TRUE, 0, size, host_data, 0, NULL, &event);

// Leer desde módulo remoto a host (DMA)
clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, host_data, 0, NULL, &event);

// Ventaja: control explícito, sin coherencia de caché
// Desventaja: overhead de API, copias explícitas
```

#### 3.3.3 Operaciones atómicas y sincronización

```c
// Atómicas en memoria OPGPU (OpenCL)
atomic_add(&opgpu_ptr[0], 1);  // Incremento atómico
atomic_cmpxchg(&opgpu_ptr[0], old_val, new_val);  // Compare-and-swap

// Sincronización (barreras)
clEnqueueBarrierWithWaitList(queue, 1, &event, NULL);
```

### 3.4 Coherencia de memoria

**Problema:** si el host cachea datos de memoria OPGPU, puede haber inconsistencias cuando el módulo remoto modifica los datos (o viceversa).

**Soluciones (configurables):**

1. **Sin coherencia (uncached):**
   - Host no cachea datos de OPGPU (page tables marked as uncacheable).
   - Cada load/store va directo al módulo remoto.
   - **Ventaja:** simplicidad, consistencia garantizada.
   - **Desventaja:** latencia alta para accesos repetidos.

2. **Coherencia por software (explicit flush):**
   - Host cachea datos, pero debe hacer flush/invalidation manual.
   - APIs: `clFlush()`, `clFinish()`, o instrucciones CPU (`_mm_clflush`).
   - **Ventaja:** control fino, performance para patrones predecibles.
   - **Desventaja:** complejidad para el programador.

3. **Coherencia por hardware (snoop/directory, futuro):**
   - Transceptor monitorea accesos de caché del host (snoop).
   - Invalidación automática cuando módulo remoto modifica datos.
   - **Ventaja:** transparencia para el programador.
   - **Desventaja:** overhead de hardware, complejidad.

**Recomendación v1.0:** sin coherencia (uncached) para simplicidad. Coherencia por software para performance. Coherencia por hardware como evolución futura (v2.0).

---

## 4. Extensiones OpenCL para RAM óptica

### 4.1 Extensión `cl_opgpu_ram`

```c
// Crear buffer en memoria OPGPU (M1 PCM o M2 VO2)
cl_mem clCreateBufferOPGPU(
    cl_context context,
    cl_opgpu_mem_type mem_type,  // CL_OPGPU_MEM_M1_PCM o CL_OPGPU_MEM_M2_VO2
    cl_mem_flags flags,          // CL_MEM_READ_WRITE, CL_MEM_READ_ONLY, etc.
    size_t size,
    void* host_ptr,              // NULL para alojar en OPGPU, o puntero para copiar
    cl_int* errcode_ret
);

// Ejemplo: crear buffer en M1 PCM (no volátil)
cl_mem pcm_buffer = clCreateBufferOPGPU(
    context,
    CL_OPGPU_MEM_M1_PCM,
    CL_MEM_READ_WRITE | CL_MEM_PERSISTENT,  // Persistente (no se borra al apagar)
    160 * 1024 * 1024,  // 160 MB
    NULL,
    &err
);

// Ejemplo: crear buffer en M2 VO2 (volátil, baja latencia)
cl_mem vo2_buffer = clCreateBufferOPGPU(
    context,
    CL_OPGPU_MEM_M2_VO2,
    CL_MEM_READ_WRITE,
    64 * 1024 * 1024,  // 64 MB
    NULL,
    &err
);
```

### 4.2 Propiedades de memoria OPGPU

```c
// Consultar propiedades de memoria OPGPU
clGetDeviceInfo(device, CL_OPGPU_MEM_M1_CAPACITY, sizeof(cl_ulong), &m1_cap, NULL);
clGetDeviceInfo(device, CL_OPGPU_MEM_M2_CAPACITY, sizeof(cl_ulong), &m2_cap, NULL);
clGetDeviceInfo(device, CL_OPGPU_MEM_M1_BANDWIDTH, sizeof(cl_ulong), &m1_bw, NULL);
clGetDeviceInfo(device, CL_OPGPU_MEM_M2_BANDWIDTH, sizeof(cl_ulong), &m2_bw, NULL);
clGetDeviceInfo(device, CL_OPGPU_MEM_M1_LATENCY, sizeof(cl_ulong), &m1_lat, NULL);
clGetDeviceInfo(device, CL_OPGPU_MEM_M2_LATENCY, sizeof(cl_ulong), &m2_lat, NULL);
clGetDeviceInfo(device, CL_OPGPU_MEM_PCM_WEAR, sizeof(cl_float), &pcm_wear, NULL);  // 0-100%
```

### 4.3 Operaciones específicas de memoria

```c
// Flush de buffer (forzar escritura en PCM)
clEnqueueFlushBufferOPGPU(queue, buffer, 0, size, 0, NULL, &event);

// Lock de página (evitar que se mueva entre M1/M2)
clEnqueueLockBufferOPGPU(queue, buffer, offset, size, 0, NULL, &event);

// Unlock de página
clEnqueueUnlockBufferOPGPU(queue, buffer, offset, size, 0, NULL, &event);

// Migración entre M1 y M2 (volátil → no volátil o viceversa)
clEnqueueMigrateBufferOPGPU(queue, buffer, CL_OPGPU_MEM_M1_PCM, 0, NULL, &event);
```

### 4.4 Persistent memory (M1 PCM)

La memoria M1 PCM es **no volátil**: retiene datos sin energía. Esto permite:

```c
// Crear buffer persistente (sobrevive a reinicios)
cl_mem persistent_buffer = clCreateBufferOPGPU(
    context,
    CL_OPGPU_MEM_M1_PCM,
    CL_MEM_READ_WRITE | CL_MEM_PERSISTENT | CL_MEM_USE_PERSISTENT_PTR,
    size,
    NULL,
    &err
);

// Al apagar el sistema, los datos permanecen en M1
// Al reiniciar, el host puede re-mapear el mismo buffer y acceder a los datos

// Ejemplo: checkpointing rápido
void save_checkpoint(cl_mem model_state, size_t size) {
    // Guardar estado del modelo en PCM (persistente)
    clEnqueueWriteBuffer(queue, model_state, CL_TRUE, 0, size, data, 0, NULL, NULL);
    clFinish(queue);
    // Al apagar, los datos permanecen en M1
}

void load_checkpoint(cl_mem model_state, size_t size) {
    // Cargar estado del modelo desde PCM (persistente)
    clEnqueueReadBuffer(queue, model_state, CL_TRUE, 0, size, data, 0, NULL, NULL);
    clFinish(queue);
}
```

---

## 5. Memory Controller óptico (en transceptor)

### 5.1 Funciones del Memory Controller

El transceptor incluye un **Memory Controller óptico** que gestiona accesos a memoria remota:

| Función | Descripción |
|---|---|
| **Load/Store Unit (LSU)** | Convierte requests de memoria del host (read/write) a comandos ópticos. |
| **Memory Scheduler** | Cola de requests, reordering para maximizar throughput, batching. |
| **Prefetcher** | Predicción de accesos secuenciales/patrones, prefetch proactivo. |
| **Cache coherencia** | Snoop/invalidation (opcional, futuro). |
| **ECC/RAS** | Corrección de errores (BCH/LDPC para PCM, paridad para VO2). |
| **Wear-leveling** | Distribución de escrituras PCM para maximizar endurance. |
| **Telemetría** | Monitoreo de desgaste PCM, temperatura, BER, latencia. |

### 5.2 Pipeline de acceso a memoria

```
Host CPU/GPU
    │
    ├─ Load/Store instruction (memory-mapped)
    │   └── Page fault / TLB miss
    │        └── Driver OPGPU intercepta
    │             └── Memory Controller en transceptor
    │                  ├── Lookup en tabla de mapeo (qué módulo/dirección)
    │                  ├── Prefetch (si patrón secuencial)
    │                  ├── Batch de requests (si múltiples accesos)
    │                  ├── Convierte a comando óptico (λ, timing, dirección)
    │                  └── TX E/O → fibra → módulo remoto
    │                       └── Módulo remoto ejecuta acceso (M1/M2)
    │                            └── RX O/E → dato de vuelta → host
    │                                 └── Completion interrupt (MSI-X)
    │
    └─ OpenCL API (clEnqueueReadBuffer/clEnqueueWriteBuffer)
        └── Runtime OpenCL OPGPU
             └── DMA transfer (staging DDR → módulo remoto)
                  └── TX E/O → fibra → módulo remoto
                       └── Módulo remoto ejecuta acceso (M1/M2)
                            └── RX O/E → DMA → staging DDR → host
                                 └── Completion event
```

**Latencia breakdown (ejemplo):**
- Host → Memory Controller (PCIe): ~50-100 ns
- Memory Controller → TX E/O: ~10-20 ns
- Fibra (1 m ida y vuelta): ~10 ns
- Módulo remoto acceso M1: ~100-200 ns
- Módulo remoto → RX O/E: ~10-20 ns
- RX O/E → Host (PCIe): ~50-100 ns
- **Total: ~230-450 ns** (depende de M1 vs M2, longitud de fibra)

### 5.3 Optimizaciones de rendimiento

1. **Batching:** agrupar múltiples requests pequeños en un solo comando óptico.
2. **Reordering:** reordenar requests para maximizar throughput (similar a DRAM controllers).
3. **Prefetching:** pre-cargar datos si se detecta patrón secuencial.
4. **Caching local (staging DDR):** caché de datos frecuentes en DDR5 del transceptor (reduce accesos remotos).
5. **Wear-leveling:** distribuir escrituras PCM para evitar desgaste prematuro.

---

## 6. Casos de uso de RAM óptica

### 6.1 In-memory databases (datasets grandes)

```c
// Ejemplo: base de datos en memoria OPGPU
size_t dataset_size = 10 * 1024 * 1024 * 1024;  // 10 GB
cl_mem dataset = clCreateBufferOPGPU(context, CL_OPGPU_MEM_M1_PCM,
    CL_MEM_READ_ONLY | CL_MEM_PERSISTENT, dataset_size, NULL, &err);

// Cargar dataset desde disco a OPGPU (una vez)
clEnqueueWriteBuffer(queue, dataset, CL_TRUE, 0, dataset_size, disk_data, 0, NULL, NULL);

// Queries rápidas (lectura desde OPGPU, baja latencia)
void run_query(cl_mem dataset, size_t offset, size_t size) {
    float* result = malloc(size);
    clEnqueueReadBuffer(queue, dataset, CL_TRUE, offset, size, result, 0, NULL, NULL);
    // Procesar result...
    free(result);
}
```

### 6.2 Modelos de IA grandes (LLMs >100B params)

```c
// Ejemplo: modelo LLM en memoria OPGPU
size_t model_size = 200 * 1024 * 1024 * 1024;  // 200 GB (LLM grande)
cl_mem model_weights = clCreateBufferOPGPU(context, CL_OPGPU_MEM_M1_PCM,
    CL_MEM_READ_ONLY | CL_MEM_PERSISTENT, model_size, NULL, &err);

// Cargar modelo una vez (persistente en PCM)
clEnqueueWriteBuffer(queue, model_weights, CL_TRUE, 0, model_size, weights_file, 0, NULL, NULL);

// Inferencia: leer pesos desde OPGPU, ejecutar en GPU/NPU
void inference(cl_mem model_weights, cl_mem input, cl_mem output) {
    // Transferir weights a GPU (via PCIe, más rápido que desde disco)
    clEnqueueCopyBuffer(queue, model_weights, gpu_weights, 0, 0, layer_size, 0, NULL, NULL);
    // Ejecutar capa en GPU...
}
```

### 6.3 Checkpointing rápido (persistent memory)

```c
// Ejemplo: guardar estado de aplicación en PCM (persistente)
void save_state(cl_mem app_state, size_t size) {
    cl_mem checkpoint = clCreateBufferOPGPU(context, CL_OPGPU_MEM_M1_PCM,
        CL_MEM_WRITE_ONLY | CL_MEM_PERSISTENT, size, NULL, NULL);
    clEnqueueWriteBuffer(queue, checkpoint, CL_TRUE, 0, size, app_state, 0, NULL, NULL);
    clFinish(queue);
    // Al apagar, el checkpoint persiste en PCM
}

void load_state(cl_mem app_state, size_t size) {
    cl_mem checkpoint = clCreateBufferOPGPU(context, CL_OPGPU_MEM_M1_PCM,
        CL_MEM_READ_ONLY | CL_MEM_PERSISTENT, size, NULL, NULL);
    clEnqueueReadBuffer(queue, checkpoint, CL_TRUE, 0, size, app_state, 0, NULL, NULL);
    clFinish(queue);
}
```

### 6.4 Shared memory distribuida (múltiples hosts)

```c
// Host 1: crear buffer compartido
cl_mem shared_buffer = clCreateBufferOPGPU(context, CL_OPGPU_MEM_M2_VO2,
    CL_MEM_READ_WRITE | CL_MEM_SHAREABLE, size, NULL, &err);

// Host 2: acceder al mismo buffer (vía red o PCIe switch)
// Requiere soporte de memoria compartida (futuro, CXL-like)
```

---

## 7. Comparación con tecnologías existentes

| Tecnología | Capacidad | Latencia | BW | Persistencia | Consumo | Coste |
|---|---|---|---|---|---|---|
| **DRAM (DDR5)** | 8-128 GB/módulo | 50-100 ns | 50-100 GB/s | No | ~10-50 pJ/bit | ~$5-10/GB |
| **HBM3** | 16-128 GB/stack | 10-50 ns | 800 GB/s | No | ~15-30 pJ/bit | ~$50-100/GB |
| **Optane (3D XPoint)** | 128 GB-1.5 TB | 100-300 ns | 10-50 GB/s | Sí | ~10-20 pJ/bit | ~$50-100/GB |
| **NVMe SSD** | 1-30 TB | 10-100 µs | 3-7 GB/s | Sí | ~1-5 pJ/bit | ~$0.10-0.50/GB |
| **OPGPU M1 PCM** | 160-720 MB/módulo | 100-200 ns | 100-500 GB/s | Sí | ~0.1-1 pJ/bit | TBD |
| **OPGPU M2 VO2** | 64-384 MB/módulo | 10-50 ns | 200-1000 GB/s | No | ~0.01-0.1 pJ/bit | TBD |

**Ventajas OPGPU RAM óptica:**
- Mayor ancho de banda que Optane/NVMe (100-1000 GB/s vs 10-50 GB/s).
- Menor consumo energético que DRAM/HBM (~10-50× menor pJ/bit).
- Persistencia (M1 PCM) sin costo de refresh.
- Escalabilidad: múltiples módulos en paralelo (TB/s aggregate).

**Desventajas:**
- Capacidad limitada por módulo (160-720 MB vs 8-128 GB DRAM).
- Latencia mayor que DRAM/HBM (~100-500 ns vs 10-100 ns).
- Tecnología no madura (requiere validación experimental).
- Coste TBD (depende de fabricación a escala).

---

## 8. Plan de implementación (complementario)

### Fase 1: Prototipo Memory Controller (6-12 meses, paralelo a transceptor)
1. **Memory Controller en FPGA:** LSU, scheduler, prefetcher, ECC.
2. **Driver de memoria Linux:** `mmap`, page tables, uncacheable regions.
3. **Benchmarks:** latency, bandwidth, IOPS vs DRAM/Optane.

### Fase 2: Integración con módulo fotónico (12-24 meses)
1. **Accesos M1/M2:** validar lectura/escritura en PCM/VO2 vía fibra.
2. **Wear-leveling:** implementar y validar endurance PCM.
3. **Persistent memory:** probar checkpointing/recovery.

### Fase 3: Ecosistema de software (18-30 meses)
1. **Extensiones OpenCL:** `cl_opgpu_ram`, persistent memory APIs.
2. **Librerías de aplicación:** in-memory databases, LLM serving, checkpointing.
3. **Integración con frameworks:** PyTorch, TensorFlow, Redis, etc.

### Fase 4: Optimización y escalado (24-36 meses)
1. **Coherencia de caché:** snoop/directory-based (opcional).
2. **Multi-módulo:** shared memory distribuida, memoria agregada (TB scale).
3. **CXL interop:** compatibilidad con ecosistema CXL (Intel, AMD, ARM).

---

## 9. Riesgos y mitigaciones

| Riesgo | Impacto | Prob. | Mitigación |
|---|---|---|---|
| **Latencia mayor que DRAM** | Alto | Media | Aceptar para workloads tolerance a latencia (databases, checkpointing). Usar M2 VO2 para baja latencia. |
| **Endurance PCM limitado (~10⁶ ciclos)** | Medio | Media | Wear-leveling, caché de escrituras en M2 VO2, limitar escrituras frecuentes. |
| **Capacidad limitada por módulo** | Medio | Alta | Escalar con múltiples módulos en paralelo, usar como caché/tiering vs DRAM. |
| **Coherencia de caché compleja** | Alto | Media | Empezar sin coherencia (uncached), evolucionar a software/hardware coherencia. |
| **Fabricación de memoria fotónica** | Alto | Media | Validar con foundry SiPh (AIM Photonics, TowerSemi), prototipo primero. |

---

## 10. Referencias

### 10.1 Tecnologías relacionadas
- **CXL (Compute Express Link):** estándar de memoria extendida (Intel, AMD, ARM). CXL Type 3: memory expanders.
- **Optane (3D XPoint):** memoria persistente de Intel/Micron (descontinuada 2022, pero referencia).
- **HBM (High Bandwidth Memory):** memoria apilada para GPUs (SK Hynix, Samsung, Micron).

### 10.2 Estándares
- **OpenCL 3.0:** Khronos Group, extensiones de memoria personalizada.
- **CXL 3.0:** CXL Consortium, memory expander specifications.
- **JEDEC DDR5/LPDDR5:** estándares de memoria DRAM.

### 10.3 Documentación OPGPU
- Especificación transceptor: `OPGPU_TRANSCEPTOR_PCIE5_ESTANDAR.md`
- Arquitectura disaggregated: `ARQUITECTURA_DISAGGREGATED.md`
- Análisis de riesgos: `ANALISIS_RIESGOS_POR_ESTRATEGIA.md`

---

*Especificación conceptual complementaria; no constituye asesoría legal, ni diseño listo para fabricación, ni garantía de rendimiento/FTO. Publicada con intención de dominio público (CC0 1.0) como divulgación defensiva.*
