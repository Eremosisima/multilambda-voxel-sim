# Misión y estrategia de adopción abierta (Open Hardware)

## 1. Objetivo del proyecto

Este repositorio **no** se plantea como un producto cerrado a desarrollar y comercializar por sus autores, sino como un **conjunto abierto de propuestas, modelos, datos y experimentos reproducibles** para que **terceros con capacidad técnica y capital** puedan implementar, fabricar y escalar la tecnología (OPGPU: memoria/cómputo fotónico voxelizado, interfaz PCIe/OpenCL, modos GPU/NPU/TPU, coprocesador OMCC).

La meta es **maximizar la accesibilidad y la adopción** de la tecnología mediante apertura radical del conocimiento y del diseño.

## 2. Por qué abierto: acceso y presión a la baja en precios

- **Licenciamiento recíproco del hardware (CERN-OHL-S v2):** los diseños de hardware y sus derivados, cuando se distribuyen, deben mantenerse abiertos bajo condiciones recíprocas. Esto permite que cualquier implementador estudie, modifique, fabrique y comercialice productos basados en el diseño, y que esas mejoras vuelvan a estar disponibles.
- **Competencia y ausencia de lock-in:** al no existir un diseño propietario único, múltiples actores pueden fabricar y ofrecer soluciones compatibles. La competencia, la posibilidad de segundas fuentes y la transparencia de costos/diseño tienden a **reducir márgenes y precios** frente a alternativas cerradas.
- **Reproducibilidad y reducción de riesgo:** simulaciones, parámetros, supuestos y datos (P1–P3, sistema) se publican para disminuir la barrera de entrada en I+D y permitir validación independiente.
- **Aclaración importante:** las licencias abiertas **no fijan ni imponen un precio de venta** por sí mismas, ni garantizan un precio bajo en todos los mercados. Su efecto es habilitar la replicación y la competencia; las condiciones finales dependen de costos de fabricación, cadena de suministro, regulación, certificación y mercado. El proyecto promueve explícitamente implementaciones orientadas a **costo accesible** y disponibilidad amplia.

## 3. Qué ofrece este repositorio a un implementador

| Área | Contenido | Uso para quien implemente |
|---|---|---|
| **Arquitectura y esquemáticos** | Concepto OPGPU (cepillo extruido, jerarquía M0–M3, PCIe/E-O-O-E, OpenCL, NPU/TPU, OMCC) | Base de referencia para diseño de producto y particionado sistema/fotónico |
| **Modelado y datos** | P1 (PCM multinivel, térmica/diafonía), P2 (ruido/endurance/retención), P3 (variabilidad, modos 4b/5b, refresco M2), simulación de sistema con OMCC | Parámetros iniciales, márgenes, trade-offs y respaldo para dimensionamiento |
| **Simulaciones reproducibles** | Scripts Python, salidas CSV/JSON/figuras/reportes | Verificación, exploración de escenarios y punto de partida para modelos de mayor fidelidad |
| **Contexto de publicación/propiedad** | Notas de autoría, estrategia de divulgación, revisión de procedencia, licencias | Publicación defensiva/estado del arte y marco de uso abierto |

## 4. Ruta sugerida para implementadores (con capital/capacidad)

1. **Validación de alta fidelidad:** simulación FDTD/FEM óptica y FEM térmica transitoria 3D, caracterización de materiales (Sb₂S₃, VO₂, azobenceno, espiropirano) y de procesos.
2. **Prototipado por etapas:** celda/vóxel → cerda/canal → tile (MVM/memoria) → módulo cepillo → integración con borde PCIe y transductores láser/PD.
3. **Control y software:** firmware OMCC/CP, driver/runtime compatible con el modelo OpenCL descrito, calibración en lazo cerrado y RAS.
4. **Industrialización y acceso:** optimización de BOM/proceso para costo, cumplimiento de seguridad (láser/térmica), interoperabilidad (PCIe) y estrategias de fabricación/licenciamiento que favorezcan disponibilidad y precio accesible.
5. **Retrocontribución:** publicar mejoras, datos de caracterización y derivados conforme a las licencias para fortalecer el ecosistema abierto.

## 5. Principios

- **Apertura:** diseños, datos y métodos accesibles públicamente.
- **Reproducibilidad:** supuestos, parámetros y scripts trazables.
- **Habilitación, no exclusividad:** pensado para que otros construyan y compitan.
- **Accesibilidad:** orientación explícita a reducir barreras y fomentar precios y condiciones alcanzables mediante la apertura.
- **Responsabilidad:** las implementaciones deben atender seguridad, cumplimiento normativo y revisión de propiedad intelectual (FTO/patentes) según corresponda.

## 6. Licenciamiento (resumen)

- Hardware/diseños (`hardware/`): **CERN-OHL-S v2** (`LICENSE-HARDWARE`).
- Código: **Apache-2.0** (`LICENSE`).
- Documentación: **CC BY-SA 4.0** y/o licencias indicadas por componente (`LICENSE-docs`, `README`).

Consulte `README.md`, `LICENSE*`, `NOTICE` y `AI_AUTHORSHIP_NOTE.md` para detalles. Este documento expresa la intención del proyecto y no constituye asesoría legal ni compromiso contractual de precio.