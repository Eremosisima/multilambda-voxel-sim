# Open Photonic GPU v0.8 — Esquemático conceptual, acoplamiento PCIe y arquitectura "cepillo extruido" (estrategias actuales)

> **Estado:** Borrador conceptual (v0.8). No es un diseño eléctrico/mecánico/fotónico listo para fabricación ni para certificación PCIe. Requiere simulación (óptica, térmica, SI/PI en la interfaz eléctrica), validación de materiales y prototipado.  
> **Dominio público (objetivo declarado):** esquemático de uso libre para todo el mundo, publicado como **arte previo/divulgación defensiva** para dificultar apropiación registral por terceros (ver `../PUBLIC_DOMAIN_DEDICATION.md`; sin garantía absoluta).  
> **Licencias (vigentes / transición):** CERN-OHL-S v2 (hardware/diseños), CC BY-SA 4.0 (documentación), Apache-2.0 (software/firmware) en esta versión; ver plan de transición a dominio público (CC0 1.0).  
> **Actualización v0.8:** integra estrategias actuales (familias **A–G**, combinaciones **H1–H5**, priorización **H3,G2,G3,H1,H4**), control térmico fabricable, jerarquía **M0–M3/OMCC** y modularidad/aislamiento C&D. Ver [`current-strategies-schematics-and-instructions.md`](current-strategies-schematics-and-instructions.md).

## 1. Revisión de derechos de autor y procedencia (IP)

| Elemento | Origen | Estado de IP | Acción |
|---|---|---|---|
| Especificación, texto y diagramas de este repositorio | Redacción original para este proyecto (v0.1–v0.3) | Apto para publicación abierta bajo la licencia elegida, salvo indicación contraria | Mantener autoría y licencia en cabecera de cada archivo |
| Propiedades de materiales (Sb₂S₃, VO₂, azobenceno, espiropirano: longitudes de onda, transiciones, índices) | Datos proporcionados por el solicitante y hechos físicos publicados en literatura científica | Los hechos/datos no son objeto de copyright; la expresión aquí es original | Citar fuentes primarias al incorporarlas en futuras revisiones |
| Ley de Beer-Lambert y principios ópticos generales | Conocimiento científico de dominio público | Sin restricciones | N/A |
| Marcas/nombres ("PCIe", "PCI Express", "CXL", nombres comerciales de GPUs/fabricantes) | Propiedad de sus respectivos titulares | Uso nominativo/referencial únicamente | Evitar uso como marca del proyecto; cumplir especificaciones mediante implementaciones compatibles |
| Logotipos, imágenes, textos o esquemáticos de terceros | No incluidos | N/A | No incorporar sin licencia compatible y atribución |

**Conclusión de la revisión (v0.3):** no se ha identificado contenido de terceros copiado en estos documentos. Antes de cualquier publicación/upload, se debe: (a) confirmar que todos los colaboradores ceden/licencian sus aportes, (b) adjuntar archivos `LICENSE` y `NOTICE`, (c) no subir material datasheet/figuras propietarias sin permiso, y (d) ejecutar una revisión de patentes (FTO) por separado si se busca fabricación/comercialización (fuera del alcance de esta revisión de copyright).

## 2. Objetivo del diseño v0.3

- **Predominantemente óptico:** cómputo, enrutamiento y memoria en el dominio fotónico (ver v0.2).
- **Acoplamiento a host por PCIe:** tarjeta adaptadora con interfaz PCIe y transducción electro-óptica/óptico-eléctrica en el borde.
- **Topología "cepillo extruido" 3D:** arreglo de cerdas/canales ópticos extruidos, cada uno con su propio canal aislado, donde la luz es reflejada a 45° para interactuar con vóxeles ópticos.
- **Escalabilidad:** arquitectura capaz de alcanzar un número de vóxeles comparable al de las tarjetas más avanzadas del mercado mediante alta densidad areal/volumétrica, apilamiento de capas y multiplexación (espacial, espectral y por polarización).

## 3. Esquemático de alto nivel (sistema)

```text
                                 +-------------------------------+
                                 |            HOST (PC/Servidor) |
                                 |  CPU  |  Memoria  |  SW/Driver |
                                 +---------------+---------------+
                                                 | PCIe Gen5/6 x16 (eléctrico)
+--------------------------------------------------------------------------------------+
|  TARJETA ADAPTADORA (borde electrónico mínimo)                                       |
|                                                                                      |
|  [Conector PCIe edge] -> [PCIe PHY/Controller/FPGA] -> [DMA + Memoria de control]   |
|                                   |                         ^                        |
|                                   v                         |                        |
|                         [Puente E/O y O/E] <-------> [Telemetría/energía/térmica]   |
|                          | TX láseres | RX PD/TIA |                                  |
+--------------------------+------------+-----------+----------------------------------+
                           | fibras/    | guías
                           | acopladores ópticos (multicanal, MTP/MPO o interfaz óptica)
                           v
+--------------------------------------------------------------------------------------+
|  MÓDULO FOTÓNICO "CEPILLO EXTRUIDO" (principalmente óptico)                          |
|                                                                                      |
|  [Backplane óptico / interposer]                                                     |
|      | distribuye $\lambda_s$ (datos) y $\lambda_c$ (control: 365/450/520/650/800)  |
|      v                                                                               |
|  [Plano base PIC: codificación, red de distribución, control óptico]                 |
|      |                                                                               |
|      v                                                                               |
|  [Matriz de cerdas extruidas (canales verticales/3D)]  <--- ver Sección 5            |
|      |  cada cerda: guía aislada + reflector 45° + columna de vóxeles                |
|      v                                                                               |
|  [Retorno óptico / acumulación] -> [Salida O/E en borde] -> host                     |
+--------------------------------------------------------------------------------------+
```

## 4. Interfaz PCIe y transducción

### 4.1 Cadena eléctrica (borde)
- **Factor de forma:** tarjeta add-in (p. ej., FHFL) o módulo CEM, sujeto a restricciones mecánicas/térmicas PCIe.
- **Conector:** edge PCIe x16. La negociación de enlace, integridad de señal, alimentación (12V/3.3V, conectores auxiliares si aplica) y cumplimiento (SI/PI, EMI) deben seguir la especificación PCIe correspondiente (uso nominativo).
- **Controlador:** FPGA/ASIC puente con endpoint PCIe, DMA y mapas de registros para: (1) transferencia de tensores/comandos, (2) secuenciación de trenes de pulsos ópticos de control, (3) lectura de resultados convertidos, (4) calibración y monitorización.
- **Memoria electrónica de borde (mínima):** buffers de cola/comandos y staging de DMA; no almacena pesos ni estados de cómputo persistentes (residen en memoria óptica).

### 4.2 Transducción (láser / fotodetección)
- **Canal de datos host→módulo (E/O):** arreglos de láser (VCSEL/DFB según banda $\lambda_s$) modulados en intensidad/fase + drivers. Alternativa/coexistencia: moduladores externos sobre fuentes CW para mayor estabilidad.
- **Canal de datos módulo→host (O/E):** fotodetectores (PD) integrados en el borde + TIA + ADC.
- **Canales de control óptico:** fuentes dedicadas a $\lambda_c = \{365, 450, 520, 650, 800\ \text{nm}\}$ (láseres o LED/láseres combinados según potencia y ancho espectral requerido) para direccionar y conmutar Sb₂S₃, VO₂, azobenceno y espiropirano.
- **Acoplamiento:** interfaz óptica multicanal (ribbon de fibra, acopladores de rejilla/borde o interposer óptico) entre el borde y el plano fotónico. La selección del transductor concreto es un parámetro de implementación; la arquitectura fija el requisito de separar espectralmente datos y control.

## 5. Arquitectura "cepillo extruido" (matriz 3D de canales)

### 5.1 Concepto mecánico-fotónico
- **"Cepillo extruido":** cuerpo base (backplane/interposer) del que se extruyen o ensamblan verticalmente un arreglo denso de **cerdas** (pilares/guías columnares), análogas a las fibras de un cepillo.
- **Cerda = canal óptico independiente:** cada cerda es un canal confinado (guía de onda 3D o núcleo con recubrimiento de índice bajo/reflector) que evita el acoplamiento no deseado entre cerdas adyacentes (aislamiento espacial).
- **Reflexión a 45°:** en cada cerda, microespejos/facetas a 45° (o redes de acoplamiento integradas equivalentes) desvían la luz entre el plano base horizontal y el eje vertical de la cerda, y/o entre subniveles, permitiendo direccionar haces a posiciones específicas.
- **Vóxel:** región direccionable dentro de una cerda donde el haz interactúa con un material funcional, realizando almacenamiento (estado de índice/fase) o cómputo (ponderación/conmutación).

```text
Vista esquemática (corte):

   $\lambda_s,\lambda_c$  ==>>  [Plano base PIC / distribución]
                                      |  \  \  \
                                 45° /    \  \  \   (microespejos/facetas)
                                    v      v  v  v
                                  [c1]   [c2][c3][c4]   ...  cerdas extruidas (canales)
                                   |      |  |  |
                                 [v]     [v][v][v]        vóxeles apilados en z
                                 [v]     [v][v][v]
                                 [v]     [v][v][v]
                                   |      |  |  |
                                 retorno óptico / lectura (por cerda o bus común)
```

### 5.2 Mapeo de materiales a vóxeles (por cerda)

| Capa/segmento de la cerda | Material | Función | Estímulo |
|---|---|---|---|
| Segmento de cómputo/peso | **Sb₂S₃** | Vóxel de peso/MVM y celda de memoria no volátil (multinivel) | 650 nm / 300 °C |
| Segmento de conmutación/buffer | **VO₂** | Vóxel de compuerta, latch volátil y enrutamiento intra-cerda | 800 nm / 68 °C |
| Segmento de máscara/configuración | **Espiropirano** | Vóxel de selección/máscara y registro de configuración | 365 / 520 nm |
| Segmento de ajuste | **Azobenceno** | Vóxel de trim de fase/retardo y calibración | 365 / 450 nm |

Cada cerda puede ser homogénea (un tipo de vóxel a lo largo de z) o segmentada (pila funcional) para co-localizar cómputo y memoria. El direccionamiento a un vóxel $(x,y,z)$ se realiza seleccionando la cerda $(x,y)$ y el nivel $z$ mediante longitud de onda, tiempo de vuelo/retardo o conmutación por espejos 45° selectivos.

### 5.3 Aislamiento y conectividad
- **Aislamiento:** recubrimiento de bajo índice, barreras absorbentes/reflectantes o separación (pitch) suficiente entre cerdas; particionado térmico para contener los 300 °C de escritura de Sb₂S₃ lejos de VO₂ (68 °C).
- **Conectividad máxima:** el plano base actúa como red de distribución/recogida de alta densidad (crossbar óptico/WDM) que conecta todas las cerdas; las facetas a 45° maximizan el acoplamiento plano↔cerda. Conexiones laterales entre cerdas adyacentes pueden habilitarse selectivamente (ventanas de acoplamiento) cuando el algoritmo lo requiera.

## 6. Escalabilidad y presupuesto de vóxeles

Las tarjetas avanzadas del mercado (2024–2026) integran del orden de ~80×10⁹ a >200×10⁹ transistores y, en configuraciones con HBM, del orden de ~10¹¹–10¹² bits/celdas de memoria. Para un diseño fotónico 3D, el conteo objetivo de vóxeles direccionables ($N_v$) se estima como:

$$N_v = N_x \cdot N_y \cdot N_z \cdot N_\lambda \cdot N_m$$

- $N_x, N_y$: cerdas en el plano (determinadas por pitch de cerda).
- $N_z$: vóxeles apilados por cerda.
- $N_\lambda$: canales por multiplexación por longitud de onda (WDM).
- $N_m$: niveles por vóxel (p. ej., multinivel en Sb₂S₃; $N_m=1$ para binario).

**Ejemplo ilustrativo de escalado (objetivo de orden de magnitud):**

| Parámetro | Valor conservador | Valor agresivo | Nota |
|---|---:|---:|---|
| Pitch de cerda | 10 µm | 2 µm | limitado por aislamiento y fabricación 3D |
| Área activa | 30×30 mm | 50×50 mm | módulo fotónico |
| $N_x \times N_y$ (cerdas) | $3{,}0\times10^3 \times 3{,}0\times10^3 = 9\times10^6$ | $2{,}5\times10^4 \times 2{,}5\times10^4 = 6{,}25\times10^8$ | arreglo 2D |
| $N_z$ (vóxeles/cerda) | 64 | 512 | apilamiento vertical / segmentos |
| $N_\lambda$ (canales WDM) | 8 | 32 | separación espectral disponible |
| $N_m$ (niveles/vóxel) | 4 (2 bits) | 8 (3 bits) | multinivel PCM (Sb₂S₃) |
| **$N_v$ (vóxeles-equivalente)** | **~1,8×10¹⁰** | **~8,2×10¹³** | $N_x N_y N_z N_\lambda$ sitios; capacidad efectiva × $N_m$ |

> Estos valores son objetivos de arquitectura, no cifras demostradas. La viabilidad depende de pérdidas ópticas, diafonía, rendimiento de fabricación 3D, consumo energético y estabilidad térmica. El punto de diseño inicial recomendado es el escenario conservador, escalable por teselado de módulos.

## 7. Lista preliminar de subsistemas (BOM conceptual)

- **Borde PCIe:** PCB, conector edge, retimer/PHY, FPGA controladora, DDR de staging (cola), reloj, gestión de potencia (PMIC), conectores auxiliares, sensores térmicos.
- **Transducción:** arreglos láser (datos + control 365/450/520/650/800 nm), drivers, aisladores, combinadores/splitters WDM, acopladores fibra/interposer, PDs + TIAs + ADCs.
- **Plano fotónico:** oblea SiN/SiPh, guías, MZIs/crossbar, microcalentadores localizados (donde aplique), filtros.
- **Módulo cepillo:** estructura 3D extruida/ensamblada, microespejos a 45°, recubrimientos de aislamiento, integración de Sb₂S₃, VO₂, azobenceno y espiropirano por segmentos.
- **Térmico/mecánico:** disipador/cold plate, interfaz térmica, bastidor, barreras térmicas intramódulo.

## 8. Publicación en Open Hardware (preparación para upload)

> **Nota:** el upload efectivo requiere una cuenta y la aceptación de términos en la plataforma elegida. A continuación se detalla el paquete de publicación y los pasos.

### 8.1 Paquete de archivos recomendado
- `LICENSE` (CERN-OHL-S v2) y `LICENSE-docs` (CC BY-SA 4.0) si se separa.
- `README.md`: resumen, estado, advertencias de seguridad/láser.
- `docs/`: `open-photonic-gpu-v1.md` (arquitectura) y este esquemático.
- `schematics/`: esquemáticos lógicos/bloques (formatos fuente abiertos, p. ej., KiCad para el borde eléctrico; descripciones/netlists para el plano fotónico).
- `mechanical/`: modelo 3D del cepillo extruido y tarjeta (formatos abiertos, p. ej., STEP/FreeCAD).
- `simulation/`: scripts y parámetros de simulación.
- `BOM.csv`: lista de materiales con referencias.
- `NOTICE` y `CHANGELOG.md`.

### 8.2 Metadatos típicos (OSHWA / plataforma open hardware)
- **Nombre:** Open Photonic GPU (OPGPU) — Brush-Voxel Photonic Accelerator
- **Versión:** 0.3
- **Tipo:** Electrónica/Fotónica (tarjeta de expansión conceptual)
- **Licencia:** CERN-OHL-S v2
- **Documentación:** URL del repositorio público
- **Resumen:** Acelerador predominantemente óptico con memoria óptica integrada, acoplamiento PCIe por transducción láser y matriz 3D de canales tipo cepillo extruido con reflexión a 45°.

### 8.3 Pasos de upload
1. Crear repositorio público (p. ej., GitHub/GitLab) con el paquete anterior y etiquetas de versión.
2. Registrar el proyecto en oshwa.org (certificación open-source hardware) o en la plataforma de la comunidad objetivo (p. ej., OpenHardware.io / Hackaday.io según corresponda), enlazando el repositorio y la licencia.
3. Adjuntar esquemáticos/fabricables en formatos fuente abiertos y la revisión de IP (`NOTICE`).
4. Marcar claramente el estado como **conceptual/prototipo** y añadir advertencias (láser clase según fuentes, alta temperatura en zonas Sb₂S₃).

## 9. Trabajo pendiente inmediato

- Modelar una cerda unitaria (guía + reflector 45° + 1 vóxel por material) y simular acoplamiento, pérdidas y diafonía.
- Definir el protocolo de direccionamiento $(x,y,z,\lambda)$ y el presupuesto de enlace óptico (potencia, SNR) hasta el borde PCIe.
- Diseñar el esquemático eléctrico del borde PCIe (KiCad) y el mapa de registros del puente E/O.
- Seleccionar proceso de fabricación 3D para el cepillo (p. ej., litografía de dos fotones, ensamblaje de fibras, grabado profundo) y validar tolerancias del pitch.

---
*Versión 0.3 — Borrador conceptual. Requiere validación experimental y revisión de seguridad láser/térmica.*