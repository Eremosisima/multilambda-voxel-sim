=== Esquemático Integral: Transductor Electro-Óptico, Bucle Cruzado y Autodescubrimiento (ODD) ===

El siguiente diagrama detalla la interconexión completa entre la tarjeta transductora OPGPU-TX-v1 (Nivel 1), el enlace de fibra (Nivel 2) y el módulo remoto de láminas plegadas en tanque de inmersión (Nivel 3), integrando el modo de prueba por bucle cruzado y el sistema pasivo de identificación por modelo (Optical Device Descriptor - ODD):

<pre>
====================================================================================================
                                    HOST PC / SERVIDOR (CPU + RAM)
====================================================================================================
                                                 ▲
                                                 │  Bus PCIe 4.0 x16 / 5.0 x8 (CXL + SR-IOV)
                                                 ▼
+--------------------------------------------------------------------------------------------------+

|  NIVEL 1: TARJETA TRANSDUCTORA ELECTRO-ÓPTICA (OPGPU-TX-v1)                                      |
|                                                                                                  |
|  +--------------------------------------------------------------------------------------------+  |
|  | BLOQUE A: VIRTUALIZACIÓN DINÁMICA (Autoconfigurada por Descriptor ODD)                     |  |
|  |  [ Controlador PCIe / CXL ] ◄── [ Tabla de Perfiles de Modelo (Firmware Abierto) ]         |  |
|  |         ├──► Función 0: RAM Extendida (CXL.mem) -> Tamaño ajustado según SHEET_COUNT       |  |
|  |         ├──► Función 1: GPU OpenCL 3.0 (SPIR-V -> OMCC)                                    |  |
|  |         └──► Función 2: NPU/TPU OpenVINO (Plugin Extensibility)                            |  |
|  |                                        │                                                   |  |
|  |  [ Caché Local DDR4 (4-8 GB) ] ◄───────┴──► [ Motor DMA & Árbitro de Colas ]               |  |
|  +--------------------------------------------------------------------------------------------+  |
|                                                 │ (Bus Interno AXI-Stream)                       |
|                                                 ▼                                                |
|  +--------------------------------------------------------------------------------------------+  |
|  | BLOQUE B: PROCESAMIENTO DE SEÑAL ÓPTICA Y AUTODESCUBRIMIENTO (FPGA)                        |  |
|  |  [ Secuenciador OMCC ] ──► [ Generador Pulso Piloto ODD ] ──► [ SerDes 25G/50G PAM-4 ]     |  |
|  |         ▲                                                                     │            |  |
|  |         │ (Ajuste de Potencia Láser y Calibración PID)                        │            |  |
|  |  [ Decodificador Datos & Lector Firma ODD (32-bit) ] ◄── [ ADC / Comparador ] ◄───┼───┐    |  |
|  +-----------------------------------------------------------------------------------┼───┼----+  |
|                                                                                      ▼   ▲       |
|  +--------------------------------------------------------------------------------------------+  |
|  | BLOQUE C: FRONT-END ÓPTICO MODULAR (Jaulas Estándar de Telecomunicaciones)                 |  |
|  |   [ Puerto QSFP28 #1 ] (TX1 / RX1)                  [ Puerto QSFP28 #2 ] (TX2 / RX2)       |  |
|  +-----▲---------------┼---------------------------------▲---------------┼────────────────----+  |
|        │ (Fibra)       ▼ (Fibra)                         │ (Fibra)       ▼ (Fibra)               |
|  +-----┼---------------┼---------------------------------┼---------------┼────────────────----+  |
|  | BLOQUE D: MATRIZ DE CONMUTACIÓN ÓPTICA INTERNA (Cross-Loopback & Link Sense)               |  |
|  |   * MODO NORMAL (Firma ODD Válida Detectada):                                              |  |
|  |     TX1 ──► Puerto Externo A  |  Puerto Externo B ──► RX1                                  |  |
|  |     TX2 ──► Puerto Externo C  |  Puerto Externo D ──► RX2                                  |  |
|  |   * MODO PRUEBA (Sin Módulo / Puerto Abierto):                                             |  |
|  |     TX1 ══(Bucle Cruzado Interno + Atenuador 12 dB)══► RX2                                 |  |
|  |     TX2 ══(Bucle Cruzado Interno + Atenuador 12 dB)══► RX1                                 |  |
|  +-----┼---------------┼---------------------------------┼---------------┼────────────────----+  |
+--------┼───────────────┼---------------------------------┼───────────────┼───────────────────────+
         ▲               │                                 ▲               │
         │               ▼  NIVEL 2: Enlace Fibra SMF-28   │               ▼
         │         (Conectores Herméticos IP68 MPO/LC)     │               │
+--------┼───────────────┼---------------------------------┼───────────────┼───────────────────────+

|        │               ▼                                 │               ▼                       |
|  NIVEL 3: MÓDULO FOTÓNICO REMOTO (Tanque de Inmersión en Agua Desionizada + Barrera Paralelo)    |
|                                                                                                  |
|  +--------------------------------------------------------------------------------------------+  |
|  | ETIQUETA PASIVA DE IDENTIFICACIÓN (Optical EDID / ODD - 2x2 mm en Polímero)                |  |
|  |  [ Divisor 1% ] ──► [ Redes de Bragg (FBG) / Lazo de Retardo Calibrado ]                   |  |
|  |        └─► Devuelve código espectral/temporal de 32 bits (ARCH + LOGIC + SHEETS + dB, FLAGS) |  |
|  +--------------------------------------------------------------------------------------------+  |
|                                                 │ (99% Potencia Óptica Principal)                |
|                                                 ▼                                                |
|  +--------------------------------------------------------------------------------------------+  |
|  | NÚCLEO DE CÓMPUTO: LÁMINAS CONTINUAS PLEGADAS EN ACORDEÓN (1 a 32 Láminas en Paralelo)      |  |
|  |  [ Lámina 1: SU-8/PDMS ] ──► Guías de onda (pases <= 15 cm) + Membranas Fabry-Pérot (1/0/Z) |  |
|  |  [ Lámina 2..N ]         ──► Separación de 3 mm para flujo laminar de agua refrigerante    |  |
|  +--------------------------------------------------------------------------------------------+  |
+--------------------------------------------------------------------------------------------------+
</pre>

Flujo de Estados en el Esquemático (Resumen Operativo)

1. Interrogación (Bloque B → Nivel 3): Al energizar la tarjeta PCIe, el generador de pulso piloto inyecta una señal de baja potencia hacia el tanque.
2. Lectura Pasiva (Nivel 3 → Bloque B): La etiqueta ODD (grabada pasivamente en el polímero de entrada) refleja una firma espectral/temporal única de 32 bits sin requerir energía eléctrica en el tanque.
3. Configuración o Conmutación (Bloque A y D):
	* Si la firma es válida, el Bloque A ajusta dinámicamente la capacidad de memoria CXL y los núcleos OpenCL/OpenVINO según el número de modelo leído.
	* Si no hay retorno (tanque desconectado), el Bloque D cierra el bucle cruzado interno (TX1 → RX2 y TX2 → RX1) a través de un atenuador fijo para ejecutar pruebas de integridad y calibración PID en el acto.
