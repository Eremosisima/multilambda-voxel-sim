# Open Photonic GPU (OPGPU) — Brush-Voxel Photonic Accelerator

Concepto de hardware abierto (v0.3) para un acelerador **predominantemente óptico** con memoria óptica integrada, acoplamiento a host mediante interfaz PCIe (transducción electro-óptica/óptico-eléctrica en el borde) y una matriz 3D tipo **"cepillo extruido"** (cerdas/canales ópticos con reflexión a 45° hacia vóxeles direccionables).

> **Estado:** borrador conceptual / investigación. No es un diseño listo para fabricación, certificación PCIe ni uso seguro sin validación.

## Documentación
- [`docs/open-photonic-gpu-v1.md`](docs/open-photonic-gpu-v1.md): arquitectura v0.2 (cómputo, enrutamiento y jerarquía de memoria mayoritariamente ópticos).
- [`docs/open-photonic-gpu-v1-schematic-pcie.md`](docs/open-photonic-gpu-v1-schematic-pcie.md): esquemático conceptual v0.3 (revisión de IP, acoplamiento PCIe, diseño cepillo extruido, escalabilidad de vóxeles y preparación de publicación).

## Materiales funcionales considerados
| Compuesto | Conmutación | Índices (estados) | Rol |
|---|---|---|---|
| Sb₂S₃ | 650 nm / 300 °C (amorfo↔cristalino) | 2,70 / 3,30 | Pesos y memoria óptica no volátil |
| VO₂ | 800 nm / 68 °C (aislante↔metal) | 2,50 / 2,00 | Conmutación y memoria/buffers volátiles |
| Azobenceno | 365/450 nm (E/Z) | 1,56 / 1,54 | Ajuste fino de fase/retardo |
| Espiropirano | 365/520 nm (abierto/cerrado) | 1,54 / 1,60 | Configuración/máscaras y memoria reconfigurable |

## Avisos de seguridad y cumplimiento
- **Láser:** el diseño contempla fuentes en UV/visible/NIR; requiere clasificación, encerramiento y controles conforme a normas de seguridad láser aplicables.
- **Térmica:** la programación de Sb₂S₃ puede involucrar hasta ~300 °C localmente; requiere gestión y aislamiento térmico.
- **PCIe:** el uso de PCIe es nominativo; cualquier implementación debe cumplir la especificación y pruebas de interoperabilidad correspondientes.

## Licencia
- Hardware y diseños: **CERN-OHL-S v2** (ver `LICENSE`).
- Documentación: **CC BY-SA 4.0** (ver `LICENSE-docs`).
- Software/firmware (cuando aplique): **Apache-2.0** (indicar en cada componente).

Consulte `NOTICE` para atribución y notas de procedencia.
