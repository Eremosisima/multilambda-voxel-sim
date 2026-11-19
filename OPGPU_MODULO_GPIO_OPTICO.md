# OPGPU Módulo GPIO Óptico — Especificación Técnica Completa

> **Versión:** 1.0-draft (2026-11-19)
> **Estado:** especificación técnica conceptual. No es diseño listo para fabricación.
> **Objetivo:** especificación completa del módulo GPIO óptico opcional para OPGPU, con cálculos de rendimiento, coste, seguridad y roadmap de implementación.

---

## 1. Visión y alcance

### 1.1 Propósito
Módulo GPIO óptico independiente que complementa el transceptor OPGPU core (datos+memoria), proporcionando puertos ópticos de propósito general para control, sensado, sincronización e interconexión entre módulos fotónicos.

### 1.2 Casos de uso objetivo
1. **Laboratorios de investigación:** control de instrumentación óptica externa (láseres, moduladores, detectores).
2. **Prototipado de estrategias:** probar nuevas arquitecturas fotónicas sin rediseñar el core.
3. **Sincronización multi-módulo:** distribuir clock óptico entre varios módulos (evita jitter eléctrico).
4. **Interconexión directa:** módulos fotónicos comunicándose entre sí (bypass del host para baja latencia).
5. **Sensores especializados:** lectura de sensores ópticos remotos (temperatura, presión, espectroscopía).

### 1.3 No-objetivos
- No reemplaza el transceptor core (datos+memoria).
- No es un dispositivo de red convencional (Ethernet, InfiniBand).
- No es un dispositivo de almacenamiento (NVMe, SSD).

---

## 2. Arquitectura del módulo GPIO

### 2.1 Diagrama de bloques

```
┌─────────────────────────────────────────────────────────────────────┐
│ MÓDULO GPIO ÓPTICO OPGPU                                            │
│ Factor forma: Low-profile, medio slot, 15-30W                       │
│                                                                     │
│   [PCIe 5.0 x4 edge connector]                                      │
│        └── [PCIe 5.0 PHY/SerDes (32 GT/s por lane)]                │
│             └── [PCIe Controller/EP: DMA, MSI-X, BARs]              │
│                  └── [FPGA/SoC: GPIO Controller]                    │
│                         ├── GPIO Scheduler (colas de requests)      │
│                         ├── Clock Generator/Distributor             │
│                         ├── Trigger Manager                         │
│                         ├── ADC/DAC (señales analógicas)            │
│                         └── Security Controller (ACLs, rate limit)  │
│                                                                     │
│   [TX E/O: láseres GPIO sintonizables]                              │
│        ├── GPIO-0 a GPIO-3: 1310 nm (control output)               │
│        ├── GPIO-4 a GPIO-7: 850 nm (sensor input)                  │
│        ├── GPIO-CLK: 1550 nm (clock distribution)                  │
│        ├── GPIO-TRIG: 1310 nm (trigger bidireccional)              │
│        └── GPIO-INTER-0/1: 1550 nm WDM (interconexión multi-módulo)│
│                                                                     │
│   [RX O/E: fotodetectores GPIO]                                     │
│        ├── GPIO-4 a GPIO-7: 850 nm (PD + TIA + ADC)                │
│        ├── GPIO-CLK: 1550 nm (clock recovery)                      │
│        ├── GPIO-TRIG: 1310 nm (PD + TIA)                           │
│        └── GPIO-INTER-0/1: 1550 nm WDM (PD + TIA + CDR)            │
│                                                                     │
│   [Interfaz óptica: 2x MPO-12/APC]                                  │
│        ├── MPO-1: GPIO-0 a GPIO-7 + GPIO-TRIG                      │
│        └── MPO-2: GPIO-CLK + GPIO-INTER-0/1 + reservado            │
│                                                                     │
│   [Seguridad: TPM 2.0, secure boot, ACLs por puerto]               │
│   [Telemetría: temperatura, potencia óptica, uso de puertos]       │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Especificaciones eléctricas y mecánicas

| Parámetro | Especificación |
|---|---|
| **Factor forma** | Low-profile, medio slot (70 mm altura, <170 mm longitud) |
| **Slot PCIe** | 1 slot (x4 eléctrico, x8 mecánico) |
| **Conector PCIe** | PCIe 5.0 edge (CEM 4.0/5.0) |
| **Alimentación** | 12V/3.3V desde slot (15-30W total) |
| **Peso** | 150-250g |
| **Material** | PCB FR4, disipador aluminio, enclosure aluminio |
| **Conectores ópticos** | 2x MPO-12/APC (cerámica) |
| **Fibra** | Monomodo SMF-28, 0.5-10 m (hasta 100 m extendido) |

### 2.3 Presupuesto de potencia

| Componente | Potencia (W) | Notas |
|---|---|---|
| **FPGA/SoC (GPIO Controller)** | 5-10W | Xilinx Zynq UltraScale+ o similar |
| **PCIe PHY/SerDes (x4)** | 2-4W | 32 GT/s por lane |
| **TX E/O (8 láseres GPIO)** | 4-8W | 0.5-1W por láser (1310/850/1550 nm) |
| **RX O/E (8 PDs + TIAs + ADCs)** | 2-4W | 0.25-0.5W por canal |
| **ADC/DAC (señales analógicas)** | 1-2W | 8-16 canales, 12-16 bits |
| **Clock Generator/Distributor** | 1-2W | PLL + buffer óptico |
| **TPM 2.0 + Security Controller** | 0.5-1W | Hardware root of trust |
| **Telemetría/sensores** | 0.5-1W | Temperatura, potencia óptica |
| **Disipador/ventilador** | 1-2W | Disipación activa |
| **Total** | **17-34W** | Objetivo: <30W típico |

---

## 3. Especificación de puertos GPIO

### 3.1 Puertos de control (GPIO-0 a GPIO-3)

| Parámetro | Especificación |
|---|---|
| **Longitud de onda** | 1310 nm ±10 nm |
| **Dirección** | Output (transceptor → externo) |
| **Tipo de señal** | Digital (on/off) o analógica (modulación) |
| **Ancho de banda** | 10-100 MHz (digital), 10-50 MHz (analógica) |
| **Potencia óptica TX** | 0 a +5 dBm (ajustable) |
| **Modulación** | OOK (digital), PAM-4 (analógica) |
| **Conector** | MPO-12/APC (4 fibras de 12) |
| **Uso típico** | Control de láseres externos, moduladores, TEC, calentadores PCM |

**Cálculo de enlace (control output):**
```
Potencia TX: +3 dBm (típico)
Pérdida fibra (5 m): <0.1 dB
Pérdida conectores (2x): 0.4-1.0 dB
Pérdida acoplamiento: 0.5-1.5 dB
Potencia RX (externo): +0.5 a +1.5 dBm
Margen enlace: >10 dB (para receptores externos con sensibilidad -10 dBm)
```

### 3.2 Puertos de sensor (GPIO-4 a GPIO-7)

| Parámetro | Especificación |
|---|---|
| **Longitud de onda** | 850 nm ±10 nm |
| **Dirección** | Input (externo → transceptor) |
| **Tipo de señal** | Digital (on/off) o analógica (modulación) |
| **Ancho de banda** | 1-10 Gbps (digital), 100-500 MHz (analógica) |
| **Sensibilidad RX** | -15 a -10 dBm (digital), -20 a -15 dBm (analógica) |
| **Ruido equivalente** | <1 pW/√Hz (TIA) |
| **ADC** | 12-16 bits, 100-500 MS/s |
| **Conector** | MPO-12/APC (4 fibras de 12) |
| **Uso típico** | Fotodetectores externos, espectrómetros, sensores de temperatura ópticos |

**Cálculo de enlace (sensor input):**
```
Potencia TX (sensor externo): 0 a +3 dBm
Pérdida fibra (5 m): <0.1 dB
Pérdida conectores (2x): 0.4-1.0 dB
Pérdida acoplamiento: 0.5-1.5 dB
Potencia RX (GPIO): -2 a +0.5 dBm
Margen enlace: >10 dB (vs sensibilidad -15 dBm)
```

### 3.3 Puerto de clock (GPIO-CLK)

| Parámetro | Especificación |
|---|---|
| **Longitud de onda** | 1550 nm ±5 nm |
| **Dirección** | Bidireccional (master/slave configurable) |
| **Tipo de señal** | Clock óptico (tono continuo modulado) |
| **Frecuencia** | 10-40 GHz (ajustable) |
| **Potencia óptica TX** | +5 a +10 dBm (alto para distribución) |
| **Sensibilidad RX** | -10 a -5 dBm (clock recovery) |
| **Jitter** | <1 ps RMS (integrado 10 kHz-10 MHz) |
| **Conector** | MPO-12/APC (1 fibra dedicada) |
| **Uso típico** | Distribución de clock entre módulos fotónicos, sincronización de sampling |

**Cálculo de distribución de clock:**
```
Potencia TX: +7 dBm
Pérdida splitter (1→4): 6 dB
Pérdida fibra (5 m): <0.1 dB
Pérdida conectores (2x): 0.4-1.0 dB
Potencia RX (cada módulo): -0.1 a +0.5 dBm
Margen enlace: >5 dB (vs sensibilidad -10 dBm para clock recovery)
Número de módulos: hasta 4 por splitter (más con amplificadores)
```

### 3.4 Puerto de trigger (GPIO-TRIG)

| Parámetro | Especificación |
|---|---|
| **Longitud de onda** | 1310 nm ±10 nm |
| **Dirección** | Bidireccional |
| **Tipo de señal** | Pulso digital (trigger) |
| **Ancho de banda** | 100 MHz (frecuencia de trigger) |
| **Duración de pulso** | 1-100 ns (ajustable) |
| **Potencia óptica TX** | +3 a +5 dBm |
| **Sensibilidad RX** | -15 a -10 dBm |
| **Conector** | MPO-12/APC (1 fibra dedicada) |
| **Uso típico** | Sincronización de adquisición, start/stop de experimentos, eventos |

### 3.5 Puertos de interconexión (GPIO-INTER-0/1)

| Parámetro | Especificación |
|---|---|
| **Longitud de onda** | 1550 nm WDM (4-8 λs) |
| **Dirección** | Bidireccional |
| **Tipo de señal** | Datos de alta velocidad (inter-módulo) |
| **Ancho de banda** | 10-100 Gbps por λ (400-800 Gbps total) |
| **Potencia óptica TX** | 0 a +5 dBm por λ |
| **Sensibilidad RX** | -15 a -10 dBm por λ |
| **Modulación** | PAM-4 (100G) o QPSK (400G) |
| **Conector** | MPO-12/APC (4-8 fibras de 12) |
| **Uso típico** | Interconexión directa entre módulos fotónicos (bypass del host) |

**Cálculo de interconexión multi-módulo:**
```
Topología: mesh o ring (hasta 8 módulos)
Ancho de banda aggregate: 400-800 Gbps por enlace
Latencia inter-módulo: <10 ns (directo) vs >100 ns (vía host)
Distancia máxima: 100 m (fibra monomodo)
Protocolo: Ethernet óptico o protocolo propietario OPGPU
```

---

## 4. API OpenCL para GPIO

### 4.1 Extensión `cl_opgpu_gpio`

```c
// Crear handle de puerto GPIO
cl_gpio_handle clCreateGPIO(
    cl_context context,
    const char* port_name,      // "GPIO-0", "GPIO-CLK", etc.
    cl_gpio_direction direction, // CL_GPIO_INPUT, CL_GPIO_OUTPUT, CL_GPIO_BIDIR
    cl_int* errcode_ret
);

// Escribir señal GPIO (digital o analógica)
cl_int clWriteGPIO(
    cl_gpio_handle gpio,
    cl_gpio_signal_type type,   // CL_GPIO_DIGITAL, CL_GPIO_ANALOG, CL_GPIO_CLOCK
    cl_float value,             // 0.0-1.0 (digital), voltaje (analógica), frecuencia (clock)
    cl_uint flags,              // CL_GPIO_IMMEDIATE, CL_GPIO_BUFFERED
    const cl_event* wait_list,
    cl_event* event
);

// Leer señal GPIO
cl_int clReadGPIO(
    cl_gpio_handle gpio,
    cl_gpio_signal_type type,
    cl_float* value,
    cl_uint flags,
    const cl_event* wait_list,
    cl_event* event
);

// Configurar propiedades de puerto GPIO
cl_int clSetGPIOProperty(
    cl_gpio_handle gpio,
    cl_gpio_property_name name, // CL_GPIO_SAMPLE_RATE, CL_GPIO_RANGE, etc.
    cl_gpio_property_value value
);

// Consultar propiedades de puerto GPIO
cl_int clGetGPIOProperty(
    cl_gpio_handle gpio,
    cl_gpio_property_name name,
    cl_gpio_property_value* value
);

// Iniciar/detener clock GPIO
cl_int clStartClock(
    cl_gpio_handle gpio,
    cl_double frequency_hz,
    cl_uint flags,
    const cl_event* wait_list,
    cl_event* event
);

cl_int clStopClock(
    cl_gpio_handle gpio,
    cl_uint flags,
    const cl_event* wait_list,
    cl_event* event
);

// Configurar trigger GPIO
cl_int clConfigureTrigger(
    cl_gpio_handle gpio,
    cl_trigger_mode mode,       // CL_TRIGGER_RISING, CL_TRIGGER_FALLING, CL_TRIGGER_BOTH
    cl_float threshold,
    cl_uint flags,
    const cl_event* wait_list,
    cl_event* event
);

// Interconexión multi-módulo (GPIO-INTER)
cl_int clSendInterModule(
    cl_gpio_handle gpio,
    const void* data,
    size_t size,
    cl_uint dest_module_id,
    cl_uint flags,
    const cl_event* wait_list,
    cl_event* event
);

cl_int clReceiveInterModule(
    cl_gpio_handle gpio,
    void* data,
    size_t size,
    cl_uint* src_module_id,
    cl_uint flags,
    const cl_event* wait_list,
    cl_event* event
);
```

### 4.2 Ejemplos de uso

#### 4.2.1 Control de láser externo

```c
// Configurar GPIO-0 para control de láser (modulación analógica)
cl_gpio_handle laser_ctrl = clCreateGPIO(context, "GPIO-0", CL_GPIO_OUTPUT, &err);
clSetGPIOProperty(laser_ctrl, CL_GPIO_SAMPLE_RATE, 100e6);  // 100 MS/s
clSetGPIOProperty(laser_ctrl, CL_GPIO_RANGE, 2.5f);          // 0-2.5V

// Modular láser a 10 MHz
for (int i = 0; i < 1000; i++) {
    float voltage = 1.25f + 1.25f * sinf(2.0f * M_PI * 10e6f * i / 100e6f);
    clWriteGPIO(laser_ctrl, CL_GPIO_ANALOG, voltage, CL_GPIO_BUFFERED, NULL, &event);
}
clFinish(queue);
```

#### 4.2.2 Lectura de sensor de temperatura óptico

```c
// Configurar GPIO-4 para lectura de sensor
cl_gpio_handle temp_sensor = clCreateGPIO(context, "GPIO-4", CL_GPIO_INPUT, &err);
clSetGPIOProperty(temp_sensor, CL_GPIO_SAMPLE_RATE, 1e6);  // 1 MS/s

// Leer temperatura cada 1 ms
float temperatures[1000];
for (int i = 0; i < 1000; i++) {
    clReadGPIO(temp_sensor, CL_GPIO_ANALOG, &temperatures[i], CL_GPIO_BUFFERED, NULL, &event);
}
clFinish(queue);

// Procesar datos
float avg_temp = 0;
for (int i = 0; i < 1000; i++) avg_temp += temperatures[i];
avg_temp /= 1000;
printf("Temperatura promedio: %.2f°C\n", avg_temp);
```

#### 4.2.3 Distribución de clock a múltiples módulos

```c
// Configurar GPIO-CLK como master
cl_gpio_handle clock_master = clCreateGPIO(context, "GPIO-CLK", CL_GPIO_OUTPUT, &err);

// Iniciar clock a 10 GHz
clStartClock(clock_master, 10e9, 0, NULL, &event);
clFinish(queue);

// Distribuir a 4 módulos (vía splitter óptico)
// Cada módulo recibe clock con <1 ps jitter
```

#### 4.2.4 Interconexión directa entre módulos

```c
// Módulo A: enviar datos a Módulo B (bypass del host)
cl_gpio_handle inter_a = clCreateGPIO(context, "GPIO-INTER-0", CL_GPIO_BIDIR, &err);
float data_to_send[1024];
// ... llenar data_to_send ...
clSendInterModule(inter_a, data_to_send, sizeof(data_to_send), 2, 0, NULL, &event);

// Módulo B: recibir datos de Módulo A
cl_gpio_handle inter_b = clCreateGPIO(context, "GPIO-INTER-0", CL_GPIO_BIDIR, &err);
float data_received[1024];
cl_uint src_module;
clReceiveInterModule(inter_b, data_received, sizeof(data_received), &src_module, 0, NULL, &event);
printf("Recibido %zu bytes del módulo %u\n", sizeof(data_received), src_module);
```

---

## 5. Perfiles de seguridad GPIO

### 5.1 Definición de perfiles

| Perfil | Restricciones | Uso recomendado |
|---|---|---|
| **GPIO-Lab** | Sin restricciones, acceso root, todos los puertos habilitados | Laboratorios de investigación, prototipado |
| **GPIO-Prod** | Rate limiting (1000 ops/s), autenticación de dispositivos conectados, logs de uso | Producción, datacenters |
| **GPIO-Safe** | Solo lectura, rangos de voltaje limitados (0-1.8V), sin control de actuadores | Entornos críticos, seguridad industrial |
| **GPIO-Disabled** | GPIO completamente deshabilitado, puertos físicamente bloqueados | Máxima seguridad, solo datos/memoria |

### 5.2 Implementación de perfiles

```c
// Seleccionar perfil de seguridad GPIO
cl_int clSetGPIOSecurityProfile(
    cl_context context,
    cl_gpio_security_profile profile,  // CL_GPIO_LAB, CL_GPIO_PROD, etc.
    const cl_gpio_profile_config* config  // Configuración específica
);

// Ejemplo: configurar perfil de producción
cl_gpio_profile_config prod_config = {
    .rate_limit = 1000,           // 1000 operaciones por segundo
    .max_voltage = 3.3f,          // Máximo 3.3V
    .auth_required = CL_TRUE,     // Autenticación obligatoria
    .logging_enabled = CL_TRUE,   // Logs habilitados
    .ports_enabled = 0xFF         // Todos los puertos habilitados
};
clSetGPIOSecurityProfile(context, CL_GPIO_PROD, &prod_config);
```

### 5.3 Autenticación de dispositivos GPIO

```c
// Registrar dispositivo GPIO autorizado
cl_int clRegisterGPIODDevice(
    cl_gpio_handle gpio,
    const cl_device_id* device_id,
    const cl_device_certificate* cert
);

// Ejemplo: registrar sensor de temperatura autorizado
cl_device_certificate sensor_cert = {
    .manufacturer = "OPGPU",
    .model = "TEMP-SENSOR-01",
    .serial = "TS001234",
    .public_key = sensor_public_key,
    .signature = sensor_signature
};
clRegisterGPIODDevice(temp_sensor, &sensor_id, &sensor_cert);
```

---

## 6. Cálculos de rendimiento y coste

### 6.1 Rendimiento de GPIO

| Métrica | Valor | Notas |
|---|---|---|
| **Latencia de control (GPIO-0 a GPIO-3)** | 100-500 ns | PCIe + FPGA + E/O + fibra + RX externo |
| **Latencia de sensor (GPIO-4 a GPIO-7)** | 100-500 ns | TX externo + fibra + O/E + FPGA + PCIe |
| **Latencia de clock (GPIO-CLK)** | <10 ns (jitter) | Distribución óptica directa |
| **Latencia de trigger (GPIO-TRIG)** | 50-200 ns | Pulso óptico directo |
| **Latencia de interconexión (GPIO-INTER)** | <10 ns | Directo entre módulos (bypass host) |
| **Ancho de banda aggregate** | 400-800 Gbps | 4-8 λs x 100 Gbps/λ |

### 6.2 Coste de fabricación (estimado)

| Componente | Coste unitario (1000 uds) | Notas |
|---|---|---|
| **PCB (4-layer, FR4)** | $15-25 | Low-profile, medio slot |
| **FPGA/SoC (Xilinx Zynq+)** | $80-150 | GPIO Controller + PCIe |
| **PCIe PHY/SerDes** | $20-40 | Integrado en FPGA o discreto |
| **Láseres GPIO (8x)** | $40-80 | 1310/850/1550 nm, 5-10 mW |
| **Fotodetectores + TIA + ADC (8x)** | $60-120 | 850/1550 nm, alta velocidad |
| **ADC/DAC (8-16 canales)** | $30-60 | 12-16 bits, 100-500 MS/s |
| **Clock Generator (PLL + buffer)** | $20-40 | 10-40 GHz |
| **TPM 2.0 + Security Controller** | $10-20 | Hardware root of trust |
| **Conectores MPO-12/APC (2x)** | $20-40 | Cerámica, alta precisión |
| **Disipador + ventilador** | $10-20 | Aluminio, 40mm fan |
| **Enclosure (aluminio)** | $15-25 | Low-profile, medio slot |
| **Ensamblaje y testing** | $30-50 | Manual + automático |
| **Total BOM** | **$350-620** | |
| **Margen (40-50%)** | $140-310 | |
| **Precio de venta** | **$490-930** | Objetivo: $600-800 |

### 6.3 Comparación con alternativas

| Solución | Coste | Latencia | Ancho de banda | Flexibilidad |
|---|---|---|---|---|
| **OPGPU GPIO Module** | $600-800 | 100-500 ns | 400-800 Gbps | Muy alta |
| **National Instruments PXIe** | $2000-5000 | 1-10 µs | 10-100 Gbps | Alta |
| **Arduino/Raspberry Pi + SFP** | $50-200 | 10-100 µs | 1-10 Gbps | Media |
| **FPGA custom + transceivers** | $1000-3000 | 100-500 ns | 100-400 Gbps | Muy alta |

**Ventaja OPGPU:** integración nativa con ecosistema OPGPU (OpenCL, módulos fotónicos), menor latencia que soluciones comerciales, mayor ancho de banda que soluciones DIY.

---

## 7. Plan de implementación

### Fase 1: Prototipo (6-12 meses)

**Objetivo:** validar arquitectura y API básica.

**Entregables:**
1. PCB prototipo (4-layer, FR4)
2. FPGA development kit (Xilinx Zynq UltraScale+)
3. 4 canales GPIO-0 a GPIO-3 (control output)
4. API OpenCL básica (`clCreateGPIO`, `clWriteGPIO`, `clReadGPIO`)
5. Perfil de seguridad GPIO-Lab

**Criterios de éxito:**
- Latencia <1 µs para control output
- Ancho de banda >10 Gbps aggregate
- API funcional con ejemplos básicos

**Coste estimado:** $50-100K (desarrollo + prototipos)

### Fase 2: Módulo completo (12-24 meses)

**Objetivo:** producto completo con todos los puertos GPIO.

**Entregables:**
1. PCB producción (4-6 layer, HDI si necesario)
2. Todos los puertos GPIO (0-7, CLK, TRIG, INTER-0/1)
3. Perfiles de seguridad GPIO-Lab/Prod/Safe/Disabled
4. API OpenCL completa (`cl_opgpu_gpio`)
5. Documentación y ejemplos

**Criterios de éxito:**
- Latencia <500 ns para todos los puertos
- Ancho de banda >400 Gbps aggregate
- Certificación de seguridad básica (IEC 62443)

**Coste estimado:** $200-400K (desarrollo + tooling + certificación)

### Fase 3: Producción y ecosistema (24-36 meses)

**Objetivo:** producción en volumen y ecosistema de software.

**Entregables:**
1. Producción en volumen (1000+ unidades/año)
2. Librerías de alto nivel (Python, C++, Rust)
3. Integración con frameworks (PyTorch, TensorFlow, ROS)
4. Certificaciones avanzadas (FIPS 140-3, Common Criteria)
5. Programa de partners (fabricantes de sensores/actuadores)

**Criterios de éxito:**
- Coste de fabricación <$400/unidad (volumen 1000+)
- Precio de venta $600-800
- 10+ partners de ecosistema

**Coste estimado:** $500K-1M (producción + marketing + partnerships)

---

## 8. Análisis de mercado y ROI

### 8.1 Tamaño de mercado objetivo

| Segmento | Tamaño (2026) | CAGR | OPGPU TAM (5 años) |
|---|---|---|---|
| **Laboratorios de investigación** | $500M | 8% | $50-100M |
| **Datacenters (interconexión óptica)** | $2B | 12% | $200-400M |
| **Industrial (sensores/control)** | $1B | 6% | $50-100M |
| **Total** | $3.5B | 9% | $300-600M |

**Suposición:** OPGPU captura 10-20% del mercado de interconexión óptica especializada en 5 años.

### 8.2 Proyección de ventas (módulo GPIO)

| Año | Unidades vendidas | Precio promedio | Ingresos | Margen bruto |
|---|---|---|---|---|
| **Año 1** | 100 | $800 | $80K | 40% |
| **Año 2** | 500 | $750 | $375K | 45% |
| **Año 3** | 2000 | $700 | $1.4M | 50% |
| **Año 4** | 5000 | $650 | $3.25M | 55% |
| **Año 5** | 10000 | $600 | $6M | 60% |

**ROI:** inversión $750K-1.5M, payback en año 3-4.

### 8.3 Bundles con transceptor core

| Bundle | Componentes | Precio | Margen | Target |
|---|---|---|---|---|
| **OPGPU-Base** | Core only | $3,600-5,800 | 50% | Inferencia IA, memoria |
| **OPGPU-Pro** | Core + GPIO | $4,500-7,000 | 55% | Investigación, prototipado |
| **OPGPU-Lab** | Core + GPIO (Lab profile) | $5,000-7,500 | 60% | Laboratorios académicos |
| **OPGPU-Cluster** | 4x Core + 2x GPIO | $18,000-28,000 | 65% | Datacenters, HPC |

---

## 9. Riesgos y mitigaciones

| Riesgo | Impacto | Prob. | Mitigación |
|---|---|---|---|
| **Latencia mayor que especificado** | Alto | Media | Optimización de FPGA, pipelines, buffers. Benchmarking continuo. |
| **Coste de fabricación alto** | Alto | Media | Negociación con foundries, diseño para manufactura (DFM), volumen. |
| **Baja adopción de GPIO** | Medio | Media | Marketing enfocado en laboratorios, bundles con core, documentación. |
| **Competencia de soluciones existentes** | Medio | Media | Diferenciación: integración OPGPU, menor latencia, API OpenCL. |
| **Problemas de seguridad en GPIO** | Crítico | Baja | Perfiles de seguridad estrictos, attestation, penetration testing. |
| **Fallos en conectores MPO** | Medio | Baja | Conectores de alta calidad (US Conec, Senko), testing de ciclo de vida. |

---

## 10. Referencias

### 10.1 Estándares relacionados
- **OpenCL 3.0:** Khronos Group, extensiones de hardware personalizado.
- **PCIe 5.0:** PCI-SIG, especificación de interconexión.
- **MPO/MTP:** IEC 61754-7, conectores de fibra multi-fibra.
- **IEC 62443:** Seguridad de sistemas de control industrial.

### 10.2 Tecnologías relacionadas
- **National Instruments PXIe:** plataforma de instrumentación modular.
- **Xilinx/AMD Zynq UltraScale+:** FPGA SoC para aplicaciones embebidas.
- **SFP/QSFP transceivers:** módulos ópticos para networking.

### 10.3 Documentación OPGPU
- Transceptor core: `OPGPU_TRANSCEPTOR_PCIE5_ESTANDAR.md`
- Modo RAM óptica: `OPGPU_TRANSCEPTOR_MODO_RAM_OPTICA.md`
- Utilidad y seguridad: `OPGPU_UTILIDAD_COMUNITARIA_Y_SEGURIDAD.md`
- Arquitectura: `ARQUITECTURA_DISAGGREGATED.md`

---

*Especificación conceptual; no constituye asesoría técnica, ni diseño listo para fabricación, ni garantía de rendimiento/FTO. Publicada con intención de dominio público (CC0 1.0) como divulgación defensiva.*
