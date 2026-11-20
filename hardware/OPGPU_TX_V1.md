# OPGPU-TX-V1 — Transductor Electro-Óptico PCIe (Nivel 1, FPGA + QSFP28/QSFP-DD)

> **Versión:** 1.0 — 2026-11-19
> **Estado:** especificación conceptual. No es diseño listo para fabricación.
> **Licencia del proyecto:** CC0 1.0 — arte previo defensivo.
> **Estatus:** conponentes accesibles, BOM ~$280–590 USD (fácil de replicar: FPGA + transceptores estándar de telecomunicaciones).

Arquitectura accesible y económica: FPGA de gama media + transceptores ópticos estándar (QSFP28/QSFP-DD). Permite emular/acelerar RAM, GPU, TPU y NPU con OpenCL 3.0 + OpenVINO (Apache 2.0).

---

## 1. Arquitectura interna del transductor (OPGPU-TX-v1)

Diseño interno en 4 bloques lógicos dentro de la FPGA:

### 1.1 Interfaz Host y Virtualización PCIe (Camaleón)
- Controlador PCIe 4.0 x16 o PCIe 5.0 x8 expone **múltiples funciones virtuales (SR-IOV)**:
  - Función 0 (CXL / BAR de Memoria): mapea el módulo óptico remoto como un bloque de **RAM extendida direccionable por bytes** (CXL sobre PCIe).
  - Función 1 (Acelerador OpenCL / GPU): expone colas de comandos paralelos (SIMT) para gráficos y cómputo general.
  - Función 2 (Dispositivo OpenVINO / NPU-TPU): expone un motor sistólico para inferencia de redes neuronales y multiplicación de tensores.

### 1.2 Motor de Microsecuencias Ópticas (OMCC) + Bit-Slicing
- Traduce los tipos de datos (FP16, INT8, INT4 de OpenVINO/OpenCL) en trenes de pulsos ópticos (PAM-4 o NRZ) divididos por longitudes de onda (WDM).
- Lazo de calibración dinámica (PID digital): lee la potencia de retorno de la fibra óptica y ajusta automáticamente los sesgos para compensar ruido analógico (ver `hardware/OPGPU_BITSLICING_WDM_OPTICO.md`).

### 1.3 Buffer Caché Local (SRAM / DDR4-DDR5 Económica)
- Memoria electrónica estándar en la tarjeta (ej. 4 GB u 8 GB de DDR4/DDR5 barata): buffer L1/L2 para absorber ráfagas antes de enviar por fibra, ocultando latencia del enlace.

### 1.4 Front-End Óptico Modular (Jaulas QSFP28 / QSFP-DD)
-puertos estándar QSFP28 (100 Gbps c/u) o QSFP-DD (400 Gbps) en lugar de soldar láseres/fotodetectores caros.
- Módulos ópticos comerciales de telecomunicaciones (CWDM4 / LR4, 1550 nm) fabricados por millones ($30–80 c/u).
- Transceptores ópticos E/O-O/E en la jaula (láseres + fotodetectores integrados).

---

## 2. Soporte OpenCL y OpenVINO sin monopolios

### OpenCL 3.0 (GPU y Cómputo General)
- Compilador: PoCL (Portable Computing Language) o Rusticl (de Mesa 3D), código abierto.
- Flujo: OpenCL C/C++ → LLVM → SPIR-V → backend personalizado OPGPU (comandos binarios a la FPGA).

### OpenVINO (NPU y TPU)
- OpenVINO (Apache 2.0): plugin de hardware de terceros via OpenVINO Extensibility API / Plugin Interface.
- Plugin OPGPU: intercepta capas pesadas (convoluciones, MatMul), cuantiza a INT8/INT4 y las envía por fibra a las membranas interferométricas; capas ligeras (ReLU/Softmax) quedan en la FPGA o CPU.

---

## 3. Lista de Materiales (BOM) Estimada (Prototipo Accesible)

| Componente | Especificación recomendada (Accesible) | Rol en el Transductor | Costo estimado (USD) |
|---|---|---|---|
| Chip Principal (FPGA) | AMD Xilinx Kintex UltraScale+ o Intel Agilex / Stratix (o Lattice Avant para gama baja) | Control PCIe, motor OMCC, DSPs y calibración | $150 – $350 |
| Memoria Caché Local | 2x Chips DDR4 (4 GB – 8 GB total) | Buffer rápido para modo RAM / GPU | $20 – $35 |
| Puertos Ópticos | 2x Jaulas QSFP28 (200 Gbps agregados) | Interfaz mecánica/eléctrica hacia fibra | $10 – $15 |
| Transceptores Ópticos | 2x Módulos QSFP28 100G CWDM4 / LR4 (1310–1550 nm) | Conversión E/O y O/E | $60 – $120 (el par) |
| PCB y Alimentación | PCB de 10–12 capas, impedancia controlada + VRM | Tarjeta PCIe estándar | $40 – $70 |
| **Total BOM (Producción lote)** | — | **Tarjeta completa lista para conectar fibra** | **~$280 – $590 USD** |

> **Nota:** Rango $400–$600 originalmente proyectado; ahora construible 100% con piezas comerciales accesibles.

---

## 4. Diagnóstico de Fabricación y Uso

- **No se fabrica un ASIC desde cero:** el costo de un chip ASIC suele ser millones; la FPGA reduce a pocos cientos.
- **Replanetarabilidad:** la misma tarjeta actúa como RAM, GPU, TPU o NPU según lo que pida el software.
- **Transceptor comercial:** Jaulas QSFP28/QSFP-DD están diseñadas para redes de internet; reutilizarlas para tensores analógicos/cuantizados es parte del diseño (ver sección 4.1).

---

## 5. Blindaje en la documentación defensiva (Prior Art)

1. **Jaulas estándar QSFP28/QSFP-DD desacopladas de su protocolo Ethernet original:** usar transceptores ópticos de telecomunicaciones para transmitir tensores matemáticos analógicos/cuantizados y direcciones de memoria CXL directamente hacia un procesador pasivo de láminas poliméricas.
2. **Virtualización multifunción PCIe (SR-IOV + CXL):** partición dinámica del ancho de banda óptico para que el sistema operativo vea simultáneamente un dispositivo de memoria (RAM), un dispositivo OpenCL (GPU) y un dispositivo OpenVINO (NPU/TPU).
3. **Puente de software libre (SPIR-V → OMCC y plugin OpenVINO):** arquitectura del compilador abierto que traduce grafos de redes neuronales en secuencias de modulación óptica.

---

## 6. Datos de sistema
- Transceptor: PCIe 5.0 x8/x16, 800 Gbps agregados (ver `ARQUITECTURA_DISAGGREGATED.md`).
- Módulo remoto: máquinas OEM Brush (H1) + Láminas Continuas Plegadas; banda C-band 1530–1565 nm.
- Software: OpenCL 3.0 base; OpenVINO como complemento para IA.

## 4. Esquem\u00e1tico de Bloques del Transductor (OPGPU-TX-v1)

```text
====================================================================================================
                                    HOST PC / SERVIDOR (CPU + RAM)
====================================================================================================
                                                 \u25b2
                                                 \u2502  Bus PCIe 4.0 x16 / 5.0 x8 (CXL + SR-IOV)
                                                 \u25bc
+--------------------------------------------------------------------------------------------------+
|  TARJETA TRANSDUCTORA ELECTRO-\u00d3PTICA (OPGPU-TX-v1)                                               |
|                                                                                                  |
|  +--------------------------------------------------------------------------------------------+  |
|  | BLOQUE A: VIRTUALIZACI\u00d3N Y MEMORIA LOCAL                                                   |  |
|  |  [ Controlador PCIe / CXL ] \u2500\u2500\u25b2\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 Funci\u00f3n 0: RAM Extendida (CXL.mem)                      |  |
|  |                               \u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 Funci\u00f3n 1: GPU OpenCL 3.0 (SPIR-V -> OMCC)              |  |
|  |                               \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 Funci\u00f3n 2: NPU/TPU OpenVINO (Plugin Extensibility)      |  |
|  |                                        \u2502                                                   |  |
|  |  [ Cach\u00e9 Local DDR4 (4-8 GB) ] \u25c4\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 [ Motor DMA & \u00c1rbitro de Colas ]               |  |
|  +--------------------------------------------------------------------------------------------+  |
|                                                 \u2502                                                |
|                                                 \u25bc (Bus Interno AXI-Stream)                       |
|  +--------------------------------------------------------------------------------------------+  |
|  | BLOQUE B: PROCESAMIENTO DE SE\u00d1AL \u00d3PTICA (FPGA)                                             |  |
|  |  [ Secuenciador OMCC ] \u2500\u2500\u25b6 [ Codificador Bit-Slicing WDM ] \u2500\u2500\u25b6 [ SerDes 25G/50G PAM-4 ]    |  |
|  |         \u25b2                                                                                    \u2502            |  |
|  |         \u2502 (Lazo de Calibraci\u00f3n PID y Autodiagn\u00f3stico)                                             |  |
|  |  [ Decodificador & Correcci\u00f3n de Error ] \u25c4\u2500\u2500 [ Comparador Anal\u00f3gico/ADC ] \u25c4\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 \u2502  |  |
|  +----------------------------------------------------------------------------------------\u2500\u2500\u2500\u2500\u25b6          |
|                                                                                                  |
|                                    (Carriles de Alta Velocidad - PAM-4)                          |
|  +--------------------------------------------------------------------------------------------+  |
|  | BLOQUE C: FRONT-END \u00d3PTICO MODULAR (Jaulas Est\u00e1ndar)                                       |  |
|  |                                                                                            |  |
|  |   [ Puerto QSFP28 #1 ] (TX1 / RX1)                  [ Puerto QSFP28 #2 ] (TX2 / RX2)       |  |
|  +--------------------------------------------------------------------------------------------+  |
|                                                                                                  |
|  BLOQUE D: MATRIZ DE CONMUTACI\u00d3N \u00d3PTICA INTERNA (Cross-Connect & Loopback)                     |
|                                                                                                  |
|     \u25b6\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510 (Atenuaci\u00f3n Muestra Interna x10%)                                            |
|     \u2502           \u25bc                                                                            |
|     \u2502 \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510                                                    |
|     \u2502 \u2502  CONMUTADOR \u00d3PTICO 2x2 (Modo Normal vs Modo Prueba)     \u2502                                               |
|     \u2502 \u2502  \u2502                                                         \u2502                                               |
|     \u2502 \u2502  \u2502  * ESTADO NORMAL (M\u00f3dulo Externo Detectado):       \u2502                                               |
|     \u2502 \u2502  \u2502    TX1 \u2500\u2500\u2500\u2500\u25b6 Puerto Externo A | Puerto Externo B \u2500\u2500\u2500\u2500\u25b6 RX1    \u2502                                               |
|     \u2502 \u2502  \u2502    TX2 \u2500\u2500\u2500\u2500\u25b6 Puerto Externo C | Puerto Externo D \u2500\u2500\u2500\u2500\u25b6 RX2    \u2502                                               |
|     \u2502 \u2502  \u2502                                                         \u2502                                               |
|     \u2502 \u2502  \u2502  * ESTADO PRUEBA (Sin M\u00f3dulo / Autodiagn\u00f3stico):       \u2502                                               |
|     \u2502 \u2502  \u2502    TX1 \u2550\u2550(Bucle Cruzado Interno + Atenuador)\u2550\u2550\u25b6 RX2     \u2502                                               |
|     \u2502 \u2502  \u2502    TX2 \u2550\u2550(Bucle Cruzado Interno + Atenuador)\u2550\u2550\u25b6 RX1     \u2502                                               |
|     \u2502 \u2502  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518                                               |
|     \u2502 \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  |
|     \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  |
|                                                                                                  |
|            (Fibra SMF-28 hacia/desde OEM Brush - Nivel 3, acorde\u00f3n de l\u00e1minas plegadas)      |
+--------------------------------------------------------------------------------------------------+
```


## 5. Funcionamiento del Modo de Prueba por Interconexión Cruzada Interna (Cross-Loopback)

Esta característica convierte a la tarjeta en una herramienta de desarrollo autónoma y facilita el control de calidad en fábrica o laboratorio sin necesitar el tanque de líquido:

**A. Detección Automática de Presencia (Optical Link Sense):**
1. Al encender, el Secuenciador OMCC envía un pulso piloto de baja potencia por TX1 y TX2.
2. Si el tanque externo (Nivel 3) está conectado, la luz viaja por fibra externa, atraviesa las láminas poliméricas y regresa por RX1/RX2. La FPGA detecta la firma de retorno y activa el Modo de Operación Normal.
3. Si los puertos externos están desconectados (o no hay retorno en 5 ms), la FPGA activa automáticamente el Modo de Prueba por Interconexión Cruzada.

**B. Cómo se realiza el Bucle Cruzado Interno (dos opciones económicas):**
- **Opción 1 — Cable Puente Pasivo (Loopback Plug):** Conector plástico que se enchufa en los puertos frontales, cruzando físicamente TX1 → RX2 y TX2 → RX1, con un tramo de fibra enrollada con atenuación fija ($5 USD).
- **Opción 2 — Conmutador Óptico Interno 2x2 (On-Board):** Interruptor óptico MEMS o sólido (de dominio público) entre salidas QSFP28 y panel trasero; cruza TX1 → RX2 y TX2 → RX1 con atenuación integrada fija de 12–15 dB.

**C. ¿Qué permite validar este Modo de Prueba?**
1. **Integridad de láseres y fotodetectores (BER Test):** BER a 50/100 Gbps para verificar transceptores QSFP28 y canales ópticos-eléctricos de la PCB.
2. **Calibración del Lazo PID y Bit-Slicing:** Ajustar niveles de potencia de los láseres WDM antes de conectar módulos de láminas; guardar perfiles de calibración.
3. **Emulación de Hardware (HIL):** Ejecutar OpenCL/OpenVINO con datos reales al dominio óptico, sin núcleo fotónico aún.

## 6. Blindaje Defensivo de esta Arquitectura (Prior Art)

1. **Topología de Conmutación Cruzada (Cross-Loopback) con Atenuación Simulada:** Bucle óptico cruzado interno (TX_A → RX_B) con atenuación calibrada para emular la pérdida de inserción de un coprocesador fotónico pasivo remoto durante pruebas sin carga.
2. **Desacoplamiento de Protocolo en Transceptores QSFP:** Transceptores ópticos estándar de telecomunicaciones operando fuera de la capa MAC Ethernet, inyectando tramas analógicas/multinivel (PAM-4) generadas por OMCC.
3. **Multiplexación de Roles PCIe (CXL + OpenCL + OpenVINO):** Exposición simultánea de un mismo enlace óptico como memoria direccionable (RAM/CXL) y acelerador vectorial/matricial (GPU/NPU) mediante arbitraje dinámico de colas en FPGA.
