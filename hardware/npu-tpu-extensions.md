# Extensiones NPU y TPU — OPGPU v0.4 (concepto)

> Este documento extiende la arquitectura OPGPU para operar como **NPU** (inferencia/redes neuronales) y **TPU-like** (aceleración tensorial/sistólica en dominio óptico), reutilizando el mismo plano fotónico, jerarquía de memoria óptica y interfaz PCIe/OpenCL.

## 1. Visión común: modos de configuración

| Modo | Objetivo principal | Mapeo dominante | Materiales clave |
|---|---|---|---|
| **GPU (general)** | Álgebra lineal general, kernels paralelos | MVM/crossbar reconfigurable por work-group | Sb₂S₃ (pesos), VO₂ (control), Espiropirano (rutas) |
| **NPU (inferencia)** | Capas NN: conv/dense, activaciones, normalización, pooling, atención (bloques) | Tiles especializados con pesos estacionarios y tuberías de activación | Sb₂S₃ (pesos persistentes), VO₂ (umbral/activación, gating), Azobenceno (calibración) |
| **TPU-like (tensor)** | GEMM/matmul de alto rendimiento, acumulación en bloques | Arreglo sistólico/weight-stationary óptico o MVM por bloques con acumulación en M2 | Sb₂S₃ (matrices), VO₂ (buffers/latches de parciales), M3 (alineación temporal) |

La selección de modo es una **configuración de microprograma** (M0) y de particionado de tensores, no un cambio físico del chip.

## 2. NPU: aceleración de inferencia neuronal

### 2.1 Bloques funcionales
- **Tiles de capas densas/conv:** núcleos MVM con pesos en M1 (Sb₂S₃). Las convoluciones se mapean como GEMM (im2col óptico/digital en borde) o mediante desplazamiento/retardo óptico (M3) para reutilización espacial.
- **Unidad de activación no lineal:** 
  - *Óptica:* respuesta de transmisión dependiente de intensidad y conmutación por umbral mediante **VO₂** (transición aislante↔metal) configurada en regiones de operación casi-saturada; aproxima ReLU/step y funciones sigmoideas por tramos.
  - *Híbrida de borde:* para activaciones de alta precisión o no soportadas, conversión O/E → LUT/ALU en el borde → E/O (ruta de fallback declarada por el compilador).
- **Cuantización y formatos:** pesos/activaciones en INT8/INT4/FP16 (o escalas analógicas discretizadas por niveles multinivel de Sb₂S₃, $N_m$). Parámetros de escala/zero-point almacenados en M1 o registros de borde.
- **Pooling y normalización:** pooling por conmutación/selección (VO₂/Espiropirano) y reducción óptica; normalización típicamente en borde por requerir estadísticas globales, con soporte de acumuladores en M2.
- **Fusión de operadores:** el compilador fusiona secuencias (p. ej. GEMM + bias + activación) en un único microprograma para minimizar conversiones O/E y accesos.

### 2.2 Flujo de inferencia
1. Carga única (o infrecuente) de pesos a M1 (no volátil).
2. Streaming de activaciones de entrada por $\lambda_s$ (posible WDM para lotes/canales).
3. Ejecución por capas en pipeline a través de tiles, con parciales en M2/M3.
4. Salida final O/E al host o a buffer de siguiente etapa.

### 2.3 Métricas objetivo (conceptuales)
- Alta eficiencia energética (pJ/MAC) al mantener pesos estacionarios en Sb₂S₃ y minimizar tráfico electrónico.
- Latencia determinista por pipeline óptico; throughput escalable por replicación de tiles y WDM.

## 3. TPU-like: aceleración tensorial sistólica óptica

### 3.1 Organización
- **Arreglo sistólico óptico:** matriz de celdas MAC donde los datos fluyen temporalmente sincronizados (M3/retardos + Azobenceno para alineación) entre celdas adyacentes, análogo a un systolic array pero con propagación de ondas ópticas.
- **Weight-stationary:** una matriz (o bloque) de pesos reside fija en M1 (Sb₂S₃) mientras flujos de activaciones atraviesan el arreglo; adecuada para GEMM recurrentes con pesos constantes.
- **Output-stationary (alternativa):** los acumuladores parciales permanecen en M2 (VO₂) mientras pesos/activaciones se inyectan secuencialmente.
- **Tiling:** matrices grandes se descomponen en bloques; el CP orquesta doble buffering óptico/electrónico en borde para solapar carga y cómputo.

### 3.2 Operaciones soportadas
- **GEMM / batched matmul:** núcleo primario ($C = A\times B$).
- **Convoluciones:** como GEMM o por mapeo espacial directo en tiles.
- **Atención (bloques):** $QK^T$ y $AV$ como secuencias de matmul con manejo de softmax en borde (o aproximación), sujeto a precisión.
- **Acumulación:** suma óptica por acoplamiento/interferencia y acumulación temporal en M2; reducción final O/E.

### 3.3 Control de precisión y acumulación
- Calibración por tile (Azobenceno) para igualar ganancias.
- Acumulación parcial digital opcional en borde para mitigar ruido en sumas largas (modo mixto).
- Representación por bloques con reescalado (análoga a técnicas de cuantización por bloque).

## 4. Integración con OpenCL y con el host

- **Dispositivo unificado:** GPU/NPU/TPU se exponen como el mismo dispositivo OpenCL con **perfiles/capacidades** (kernels tensoriales, formatos soportados, tamaño de tile, precisión efectiva).
- **Colas:** colas de cómputo (kernels) y colas de transferencia (DMA) independientes, sincronizadas por eventos/barreras.
- **Subdispositivos:** particionado en tiles para ejecución concurrente de múltiples inferencias o kernels.
- **Runtime:** selecciona modo (NPU/TPU) según el grafo de operadores; reporta particiones que requieren fallback a host/borde.

## 5. Esquemático lógico de un tile NPU/TPU

```text
                  (control M0: rutas/máscaras, Espiropirano)
                                   |
        λs (activaciones/entradas) v
  [Inyección + WDM] -> [Buffers M3/Azobenceno (alineación)] -> [Malla/Array MAC]
                                                                |  ^  |
                                                     pesos M1   |  | parciales M2
                                                     (Sb2S3)    |  (VO2)
                                                                |  |
                                                     [Unidad no lineal VO2]
                                                                |
                                                         [Salida / O-E]
```

## 6. Consideraciones de diseño
- **Reutilización de pesos:** crítica en NPU/TPU; favorece Sb₂S₃ no volátil para minimizar reprogramaciones (costo energético/temporal alto a 300 °C o pulsos 650 nm).
- **Gestión térmica:** operación sostenida de VO₂ (68 °C) y escrituras ocasionales de Sb₂S₃ requieren aislamiento y planificación de pulsos.
- **Verificación:** comparar salidas contra referencia digital (tolerancias por cuantización/ruido analógico) en el simulador y en pruebas de bring-up.