# Open Photonic GPU (OPGPU) — Especificación y Código Base (CC0 1.0)

Arquitectura abierta y arte previo defensivo (*Prior Art*) de acelerador fotónico desagregado capaz de operar como **RAM Óptica, GPU, NPU y TPU** mediante láminas poliméricas plegadas sumergidas en agua destilada, lógica ternaria por membranas Fabry-Pérot (`+1`, `-1`, `0`) y transductor PCIe basado en FPGA con puertos QSFP28.

## Estructura del Repositorio
* `rtl/`: Controlador en Verilog (`opgpu_odd_controller.v`) y testbench (`tb_opgpu_odd_controller.v`) para lectura del descriptor óptico pasivo (`ODD` de 32 bits) y conmutación automática a modo de prueba por bucle cruzado (*Cross-Loopback*).
* `driver/`: Driver PCIe base para el kernel de Linux (`opgpu_pci_drv.c`).
* `plugins/`: Integración nativa en C++ para **OpenVINO Runtime** (`opgpu_openvino_plugin.cpp`) y puente **OpenCL 3.0 ICD** (`opgpu_opencl_icd.cpp`).
* `sim/`: Suite de simulación física y validación independiente por rol (`opgpu_multi_role_bench.py`).
* `docs/`: Especificación técnica en formato MediaWiki (`OPGPU_Wikipedia.wiki`).

## Licencia y Arte Previo
Publicado bajo **CC0 1.0 Universal (Dominio Público)**. Constituye divulgación pública y arte previo defensivo (*Prior Art*) para garantizar la Libertad de Operación (*FTO*) y evitar patentes restrictivas.
