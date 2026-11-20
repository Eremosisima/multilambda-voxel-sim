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
