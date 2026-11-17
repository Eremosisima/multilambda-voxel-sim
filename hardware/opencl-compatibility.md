# Compatibilidad OpenCL — OPGPU v0.8 (concepto)

> Objetivo: permitir que los núcleos/celdas ópticas y el puerto PCIe/transductor se expongan a un host como un dispositivo acelerador compatible con el modelo de ejecución y memoria de **OpenCL** (uso nominativo; la conformidad requiere pasar los CTS y cumplir la especificación). Este documento define el mapeo arquitectónico y el contrato de hardware/software.  
> **Actualización v0.8:** ver [`pcie-bridge-opencl-openvino.md`](pcie-bridge-opencl-openvino.md) para el diseño electrónico de borde (PCIe EP/DMA/BAR/CSRs, cadena E/O-O/E, potencia/SI-PI/térmica), stack de software (KMD/ICD/compilador) y **camino de compatibilidad con OpenVINO** (plugin nativo, vía backend OpenCL, heterogéneo/fallback). Ver [`current-strategies-schematics-and-instructions.md`](current-strategies-schematics-and-instructions.md) para módulos/candidatos intercambiables.

## 1. Modelo de plataforma OpenCL mapeado al hardware

| Concepto OpenCL | Mapeo en OPGPU |
|---|---|
| **Platform / Device** | Tarjeta PCIe con puente E/O y plano fotónico. Se expone como un único dispositivo de tipo acelerador (con capacidades de cómputo y memoria óptica). |
| **Compute Unit (CU)** | Bloque de cómputo óptico (tile): submalla MVM/crossbar + bancos de memoria óptica locales + red de enrutamiento asociada. Un dispositivo integra $N_{CU}$ tiles direccionables. |
| **Processing Element (PE)** | Celda/vóxel óptico activo dentro de un tile (elemento de peso Sb₂S₃, compuerta/latch VO₂, o celda de cómputo en la malla). Un work-item se ejecuta sobre uno o un grupo de PEs según el kernel. |
| **Work-item / Work-group** | Un work-item corresponde a una operación elemental (p. ej. un MAC o una activación) asignada a PEs; un work-group se asigna a uno o más CUs con acceso compartido a memoria local óptica (M2/M3). |
| **Command Queue** | Cola de comandos en memoria del host/borde, consumida por el Command Processor (CP) del borde vía DMA/doorbell; los comandos se traducen a secuencias de pulsos/configuración óptica. |
| **Kernel** | Programa compilado a un **microprograma óptico**: (a) configuración de rutas/máscaras (M0, Espiropirano), (b) mapa de pesos (M1, Sb₂S₃), (c) secuencia temporal de inyección, conmutación y lectura. |
| **Event** | Señalización de finalización: interrupción MSI-X desde el borde cuando el fotodetector/ADC valida el resultado o cuando el CP marca completado un comando. |

## 2. Modelo de memoria OpenCL ↔ jerarquía óptica

| Memoria OpenCL | Mapeo físico | Material/mecanismo | Características |
|---|---|---|---|
| **Global** | Banco de memoria óptica no volátil direccionable + buffers de staging en el borde (solo tránsito) | M1: Sb₂S₃ (pesos/constantes/ tensores persistentes), direccionado por red óptica | Gran capacidad, alta latencia relativa, accesible por todos los CUs; persistente entre kernels |
| **Constant** | Región de M1 programada como solo-lectura durante la ejecución | Sb₂S₃ (estado fijado) | Cacheable en registros ópticos de configuración por CU |
| **Local** | Memoria de trabajo compartida por work-group dentro de un CU/tile | M2: VO₂ (latches/buffers volátiles) + M3 (líneas de retardo/ajuste Azobenceno) | Baja latencia, sincronización por barreras ópticas/temporización |
| **Private** | Registros/latches ópticos por PE o por lane de ejecución | VO₂ (biestables) y estado local de fase/intensidad en la celda | Ámbito de work-item, no visible externamente |
| **Host** | Memoria sistema del host | DDR del host, accedida por DMA sobre PCIe | Transferencias explícitas (buffers) o mapeo SVM según implementación |

**Coherencia:** el modelo base es de **memoria explícita** (copias host↔global, barreras local/global). La consistencia entre estado óptico y lecturas electrónicas se garantiza por puntos de commit: un resultado es visible al host solo tras conversión O/E y señalización de evento completado.

## 3. Interfaz PCIe y protocolo de comunicación

### 3.1 Componentes del borde (electrónico mínimo)
- **PCIe Endpoint/PHY:** enlace Gen4/5 x16 (objetivo) con soporte DMA, BARs y MSI/MSI-X.
- **Command Processor (CP):** microcontrolador/RTL que parsea colas OpenCL (AQL/descriptor ring propio compatible) y emite microórdenes.
- **Motor DMA:** lectura/escritura de buffers, descriptores y completion records en memoria host.
- **Puente de transducción (E/O y O/E):** convierte descriptores de datos en flujos ópticos y resultados ópticos en palabras DMA/eventos.
- **Micro-secuenciador óptico:** traduce microórdenes a trenes de pulsos por canal ($\lambda_s$, 650/800/365/450/520 nm), temporización y selección de rutas.

### 3.2 Espacios expuestos (BAR/MMIO)
| Región | Función |
|---|---|
| **BAR0 (Control/Status)** | Registros: doorbells de cola, punteros head/tail, estado del dispositivo, identificación, capacidades, interrupciones, control de reloj/energía/térmica. |
| **BAR1 (Memoria de ventana / aperturas)** | Ventana de acceso a memoria óptica direccionable (M0/M1/M2) mediante operaciones de lectura/escritura traducidas a transacciones ópticas (para depuración y configuración). |
| **BAR2 (opcional, doorbells rápidos)** | Registros de envío de bajo retardo para kernels pequeños. |

### 3.3 Flujo de ejecución (Command → Óptico → Completion)
1. **Encolado:** el runtime/driver escribe un descriptor de comando (transferencia, programación de pesos M1, lanzamiento de kernel, barrera) en la cola en memoria host y actualiza el doorbell (MMIO).
2. **Captura:** el CP obtiene el descriptor por DMA y lo valida.
3. **Configuración:** se programan M0 (máscaras/rutas, Espiropirano) y, si aplica, M1 (pesos/kernels, Sb₂S₃) mediante pulsos de control.
4. **Ejecución:** los datos de entrada se inyectan como $\lambda_s$ modulada; la malla óptica realiza el cómputo; resultados parciales se retienen en M2/M3 según el microprograma.
5. **Lectura:** fotodetectores + TIA + ADC convierten la salida; el CP escribe el resultado en el buffer host por DMA.
6. **Señalización:** se genera un completion record y una interrupción MSI-X/evento OpenCL.

```text
Host (OpenCL Runtime/Driver)
  | 1) escribe buffer + descriptor en RAM        4) lee resultado / evento
  v                                                ^
[PCIe fabric] <---- DMA R/W ----> [BAR/MMIO doorbell/CSRs]
                                        |
                                        v
                              [Command Processor + DMA]
                                        |
                                        v
                         [Micro-secuenciador / E-O bridge]
                           |      |       |       |
                        λs(data) 650nm  800nm  365/450/520
                           |      |       |       |
                           v      v       v       v
                    [Plano fotónico: M0/M1/M2/M3 + núcleos MVM + enrutamiento VO2]
                                        |
                                    O/E readout
                                        v
                              [Completion + MSI-X]
```

## 4. Compilación y mapeo de kernels

- **Frontend:** Clang/LLVM para OpenCL C/SPIR-V (uso de ecosistema estándar; no se reclama conformidad).
- **Backend OPGPU (conceptual):**
  1. **Análisis:** extrae operaciones lineales (GEMM/GEMV, convoluciones expresables como im2col+GEMM), reducciones y operaciones punto a punto.
  2. **Particionado:** asigna tiles (CUs) y particiona tensores en bloques que caben en M1/M2.
  3. **Colocación y ruteo:** mapea pesos a celdas Sb₂S₃ y rutas a conmutadores VO₂/máscaras Espiropirano.
  4. **Plan de pulsos:** genera la secuencia temporal (programación, cómputo, lectura) respetando restricciones térmicas/espectrales.
  5. **Empaquetado:** produce un binario de dispositivo con metadatos (uso de M1/M2, tamaño de work-group, latencia estimada).
- **Restricciones del modelo:** las operaciones no lineales arbitrarias se implementan como (a) aproximaciones ópticas por umbral/VO₂ cuando sea viable, (b) LUTs en M1, o (c) fallback en el borde/host; el compilador debe declarar la partición host/dispositivo.

## 5. Extensiones y capacidades del dispositivo

- Tipos: soporte preferente para `float16`/`bfloat16` y formatos enteros cuantizados (INT8/INT4) acordes a la precisión analógica efectiva de la celda.
- Atomics/barreras: barreras de work-group implementadas por sincronización temporal y latches M2; atomics globales mediante serialización en CP o regiones reservadas.
- Perfil: métricas expuestas (utilización de tiles, energía de pulsos, temperatura, errores de lectura) vía consultas de dispositivo.
- **Limitaciones:** precisión analógica dependiente de ruido/deriva; no determinismo ciclo a ciclo idéntico al digital; la "compatibilidad OpenCL" aquí es de modelo de programación/interfaz y requiere una capa de runtime/driver específica.