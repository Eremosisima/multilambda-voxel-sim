# Jerarquía de memoria óptica (RAM / L3 / L2 / L1) y “capacitores ópticos” (v0.8, conceptual)

> Análisis conceptual que mapea la jerarquía de memoria de la OPGPU a niveles tipo **RAM–L3–L2–L1–registros**, incorporando mecanismos fotónicos de almacenamiento/retención temporal de luz (cavidades resonantes, anillos, película delgada/F–P, luz lenta) y aclarando el término “capacitor óptico”. Estado: simulación/diseño de referencia abierto (no validado experimentalmente).

## 1. Aclaración: “capacitor óptico” y fenómenos relacionados

| Concepto | Qué es realmente | ¿Almacena “datos/luz” como memoria? | Relevancia para OPGPU |
|---|---|---|---|
| **“Capacitor óptico” optoelectrónico** (carga inducida por luz) | Dispositivo dieléctrico que separa carga y genera voltaje al iluminarse (efecto fotoeléctrico/ desplazamiento) | Almacena **energía/carga eléctrica** transitoriamente, no bits ópticos direccionables por contenido de señal | Potencial en sensado, autoalimentación de nodos o umbrales, pero **no** como celda de RAM/L1; distinto de almacenar fotones |
| **Condensador óptico (óptica clásica)** | Lente/sistema de lentes que concentra y colima luz (microscopio/proyector) | No almacena; condiciona el haz | Útil para acoplamiento/iluminación, no para jerarquía de memoria |
| **Cavidad resonante / Fabry–Pérot (etalon)** | Dos reflectores (o película delgada/membrana) atrapan luz por rebotes e **interferencia constructiva** a resonancias; la energía permanece un tiempo de vida fotónico $\tau \approx Q/\omega$ | **Retención temporal de fotones/energía óptica** (buffer volátil muy rápido, capacidad limitada por modos/energía) | Excelente como buffer L0/L1, línea de retardo resonante o celda de selección por $n d$ (familias B/G) |
| **Resonador de anillo (micro-ring)** | Guía cerrada; la luz circula por reflexión interna total/acoplamiento resonante | Retención temporal (ns típicos según $Q$), sintonizable | Buffers/colas cortas, conmutación y almacenamiento WDM denso (familia B), útil en L1/L2 local |
| **Luz lenta / EIT (almacenamiento coherente)** | Reduce velocidad de grupo en medios atómicos/controlados para “detener” pulsos | Retiene información del pulso brevemente (ms en condiciones específicas) con alta complejidad | Interés a largo plazo para buffers; hoy baja factibilidad en chip de computación general (criogenia/átomos/coherencia) |
| **Memoria material no volátil (PCM, fotoquímica)** | Cambia estado del material ($n$, fase, isómero) que modula señales futuras | Almacena **estado/pesos/bits** persistentes (no fotones en vuelo) | Base de M1/M0 (RAM óptica NV / configuración) |

**Conclusión práctica:** para una jerarquía tipo RAM/caché en OPGPU, los “equivalentes” útiles al *almacenamiento temporal de luz* son **cavidades/anillos/F–P/membranas** (buffers volátiles ultrarrápidos) y, para *almacenamiento de datos*, las memorias materiales (**PCM Sb₂S₃, VO₂, fotoquímicos**) ya definidas.

## 2. Jerarquía propuesta (mapeo a RAM / L3 / L2 / L1)

La jerarquía combina **estado en material** (pesos/datos direccionables) y **fotones en tránsito/retención** (latencia, buffering), gestionada por el **OMCC** (arbitraje, DMA/prefetch, coherencia explícita, RAS).

| Nivel (análogo) | Rol en OPGPU | Mecanismo físico (familias) | Volatilidad / retención | Capacidad típica (conceptual) | Latencia / acceso | Observaciones |
|---|---|---|---|---|---:|---|
| **Registros / PE-private** | Operandos inmediatos, acumuladores locales, estado de celda/MAC | Latches/bistables **VO₂** (M2), estado de fase/intensidad en MZI/celda, microcavidades integradas | Volátil (ns–µs, hold/refresco) | muy baja (bits–KB por tile) | ps–ns | Máxima cercanía al cómputo (A/B/C/G) |
| **L1 (por tile/core/cerda)** | Buffers de trabajo, colas cortas, reuse inmediato, alineación fina | **Micro-rings** (B), cavidades **F–P/membranas apiladas** (G), líneas de retardo + **Azobenceno** (M3), VO₂ local | Volátil, retención por $\tau$ fotónico o estado mantenido | KB–MB por tile | ns (propagación/vida de cavidad) | Interferencia constructiva/destructiva en resonancia/espesor $n d$ para retener/seleccionar; alta velocidad en espacio reducido |
| **L2 (compartida en módulo/tile-cluster)** | Búfer compartido de work-group, staging, *double buffering* | Bancos **VO₂** (M2), matrices de anillos/cavidades, buffers WDM | Volátil | MB–decenas de MB | ns–decenas de ns | Gestionada por OMCC (prefetch, solapamiento DMA↔cómputo) |
| **L3 / RAM óptica en chip (NV o cuasi-estática)** | Pesos, tensores persistentes, tablas, memoria global del dispositivo | **PCM Sb₂S₃** (M1) en celdas/membranas/cerdas; opcional PCM en membranas G3; configuración **Espiropirano** (M0) | **No volátil** (M1/M0), reprog. µs–ms (PCM) | decenas de MB–GB+ (según escala/3D, p. ej. H1/H4/A1-3D) | lectura rápida (óptica) / escritura lenta-cara | “RAM óptica” principal de pesos/datos persistentes; wear-leveling y verificación por OMCC |
| **RAM de host (sistema)** | Buffers host, datasets grandes, SO/runtime | DDR/HBM del host vía **PCIe + DMA** y transducción E/O-O/E | Volátil (host) | GB–TB (host) | µs+ (PCIe y conversiones) | Cuello de botella si hay poco reuso; mitigar con persistencia en M1 y batching |

> Nota: los rangos son orientativos y dependen de $Q$, pérdidas, escala, tecnología y diseño; no son especificaciones garantizadas.

## 3. Rol de cada mecanismo fotónico en la jerarquía

### 3.1 Cavidades Fabry–Pérot y membranas apiladas (familia G)
- **Como buffer (L1):** el tiempo de confinamiento $\tau$ actúa como retardo/almacenamiento temporal de energía óptica (análogo a un “capacitor” de fotones). Apilados en cerdas/cores dan múltiples “celdas” de retención por longitud de onda en **volumen muy reducido**.
- **Como memoria de estado (L3/M1 cuando hay PCM):** el mismo apilado con capas PCM fija estados por $n d$ (constructivo/destructivo por $\lambda$), almacenando pesos/canales de forma **no volátil** con alta densidad.
- **Ventaja:** combina almacenamiento temporal (resonancia) y de estado (espesor/índice) en la misma geometría compacta.

### 3.2 Micro-anillos resonantes (familia B)
- **L1/L2:** buffers y conmutación WDM densa; retención temporal por resonancia y sintonía (EO/termo/PCM) para dirigir o mantener señales.
- **Integración:** bancos de anillos por cerda/tile para colas locales y *reuse* de datos.

### 3.3 PCM Sb₂S₃ (M1) y VO₂ (M2)
- **M1/L3-RAM NV:** alta densidad (multinivel) y retención para pesos/constantes; escritura costosa → usar para datos estacionarios (NPU/TPU) y persistencia.
- **M2/L1-L2 volátil:** conmutación rápida y latches para resultados intermedios; requiere *hold*/gestión térmica.

### 3.4 Líneas de retardo y ajuste (M3, Azobenceno)
- **L1/sincronización:** alineación temporal (FIFO óptico), compensación de skew y trim de fase; capacidad pequeña, crítica para coherencia de cómputo interferométrico.

### 3.5 Luz lenta / EIT
- **Perspectiva:** mayor retención controlable, pero exigencias de medio/coherencia limitan su factibilidad actual como L1/L2 en un acelerador integrado; se considera **exploratoria** frente a cavidades/anillos/membranas.

## 4. Implicaciones por eje (precio, factibilidad, velocidad, fiabilidad, dimensiones, capacidad)

| Elección de jerarquía | Velocidad | Capacidad | Dimensiones | Fiabilidad | Factibilidad | Precio |
|---|---|---|---|---|---|---|
| L1 basado en **anillos/F–P/membranas EO** (B/G2) | muy alta | media (buffer) | muy compacta | media (térmica/fase) | media-baja | medio-alto |
| L1/L2 en **VO₂ + retardos** (M2/M3) | alta | media | compacta | media (endurance/hold) | media | medio |
| L3/RAM NV en **PCM Sb₂S₃** (M1, A1/G3/H1) | lectura alta / escritura lenta | **alta–muy alta** (3D/multinivel) | eficiente en volumen | media (ciclos/retención) | media | medio |
| **H3 (pasivos G1 + A1 + B3)** | media | media-alta | buena | media | **alta** | **bajo-medio** |
| **H1/H4 (3D membrana+PCM)** | media-alta | **máxima** | muy alta densidad vol. | media | baja-media | alto |

## 5. Recomendaciones de diseño (abiertas)
- **Jerarquía explícita y gestionada por OMCC:** exponer L1/L2/L3 como regiones con políticas de *placement/prefetch/evict/persist* (análogo a scratchpad + caché gestionada), evitando suposiciones de coherencia hardware opaca.
- **Maximizar reuso en L1/L2 fotónica:** tiling y kernels fusionados para reducir tráfico a M1/host (principal ahorro de latencia/energía).
- **Combinar retención de fotones y estado material:** cavidades/anillos/membranas para buffering rápido (L1) y PCM/membranas PCM para capacidad NV (L3) en la misma cerda (H1/G3).
- **Ruta incremental:** L3/M1 PCM + L1/L2 VO₂/anillos (base A1/B3/H3) → añadir membranas F–P apiladas (G) para densidad/velocidad → sintonía EO (G2/H2) según madurez.
- **Documentación abierta:** modelos de $\tau$, $Q$, IL, energía de escritura y capacidad por nivel para que implementadores dimensionen su jerarquía (ver `simulate_opgpu_system.py`, `model_families_development.py` y salidas en `outputs/`).

## 6. Relación con documentos del proyecto
- Arquitectura base y niveles M0–M3: `open-photonic-gpu-v1.md`, `opencl-compatibility.md`.
- Gestión/arbitraje de memoria óptica: `coprocessor-and-improvements.md` (OMCC).
- Familias/variantes y combinaciones (incl. G membranas, B anillos, H1–H5): `families-and-variants.md`, `family-combinations-openhw.md`.
- Modelado: `model_reliability_p2.py`, `model_variability_p3.py`, `simulate_opgpu_system.py`, `model_families_development.py`.