NOTICE - Third-Party References and Attributions
==================================================

Project: Open Photonic GPU (OPGPU)
Repository: https://github.com/Eremosisima/multilambda-voxel-sim
Date: 2026-11-19

This project contains original work dedicated to the public domain under CC0 1.0.
The following third-party technologies, standards, and references are mentioned
nominatively for identification and compatibility purposes only.

===============================================================================
STANDARDS AND SPECIFICATIONS (Public Domain / Open Standards)
===============================================================================

1. PCI Express (PCIe) 5.0
   - Owner: PCI-SIG
   - Type: Open standard (specification publicly available)
   - Usage: Interface specification for host-device communication
   - Reference: PCI-SIG, "PCI Express Base Specification Revision 5.0", 2019
   - Note: "PCIe" and "PCI Express" are trademarks of PCI-SIG (nominative use)

2. OpenCL 3.0
   - Owner: Khronos Group
   - Type: Open standard (royalty-free)
   - Usage: Programming interface for heterogeneous computing
   - Reference: Khronos Group, "OpenCL Specification", 2020
   - Note: "OpenCL" is a trademark of Khronos Group (nominative use)

3. Wavelength Division Multiplexing (WDM)
   - Owner: ITU-T (standards body)
   - Type: International standard
   - Usage: Optical multiplexing specification
   - Reference: ITU-T G.694.1, "Spectral grids for WDM applications", 2020

4. Optical Fiber Specifications
   - Owner: IEC (standards body)
   - Type: International standard
   - Usage: Fiber optic cable specifications
   - Reference: IEC 60793-2-50, "Optical fibres - Class B single-mode fibres", 2019

===============================================================================
TRADEMARKS AND PRODUCT NAMES (Nominative Use Only)
===============================================================================

The following trademarks and product names are mentioned for compatibility
identification and reference purposes only. Their mention does not imply
endorsement, affiliation, or sponsorship.

1. FPGA/SoC Platforms:
   - Xilinx/AMD UltraScale+, Zynq UltraScale+: Advanced Micro Devices, Inc.
   - Intel Agilex: Intel Corporation
   - Note: Used as reference implementations for FPGA-based transceivers

2. GPU/Accelerator Products (for comparison purposes):
   - NVIDIA H100, A100: NVIDIA Corporation
   - Note: Specifications cited from public datasheets for benchmarking

3. Memory Technologies (for comparison purposes):
   - HBM3: SK Hynix, Samsung, Micron (industry standard)
   - Optane/3D XPoint: Intel Corporation (discontinued 2022, public specs)
   - DDR5: JEDEC standard (public specification)

4. Manufacturing/Foundry References:
   - AIM Photonics: Academic/industry consortium (public programs)
   - TowerSemi: Tower Semiconductor Ltd. (public foundry services)
   - Note: Mentioned as potential manufacturing partners, no affiliation

5. Software Tools (for simulation/validation):
   - COMSOL Multiphysics: COMSOL AB (commercial FEM software)
   - ANSYS: Ansys, Inc. (commercial simulation software)
   - Lumerical: Ansys Lumerical (commercial photonic simulation)
   - MEEP: MIT Electromagnetic Equation Propagation (open-source, MIT license)
   - Note: Mentioned as validation tools, not included in project

6. Programming Frameworks (for integration):
   - CUDA: NVIDIA Corporation (proprietary, mentioned for interop)
   - OpenVINO: Intel Corporation (open-source, Apache 2.0)
   - SYCL: Khronos Group (open standard, royalty-free)
   - PyTorch: Meta Platforms (open-source, BSD license)
   - TensorFlow: Google LLC (open-source, Apache 2.0)
   - Note: Mentioned for compatibility, not included in project

===============================================================================
SCIENTIFIC AND TECHNICAL REFERENCES
===============================================================================

The following scientific facts and technical data are referenced from public
literature. Scientific facts and data are not subject to copyright.

1. Phase-Change Materials (PCM):
   - Sb2S3 (Antimony Trisulfide) optical properties
   - Reference: Wuttig et al., "Phase-change materials for non-volatile photonic
     applications", Nature Photonics, 2017, DOI: 10.1038/nphoton.2017.126
   - Note: Material properties are scientific facts (not copyrightable)

2. Thermochromic Materials:
   - VO2 (Vanadium Dioxide) phase transition at ~68°C
   - Reference: Public domain scientific literature
   - Note: Physical properties are scientific facts (not copyrightable)

3. Photoswitchable Materials:
   - Azobenzene, Spiropyran photoisomerization
   - Reference: Irie et al., Bandara & Burdette 2012, Klajn 2014 (public literature)
   - Note: Chemical properties are scientific facts (not copyrightable)

4. Photonic Computing Concepts:
   - Mach-Zehnder Interferometer (MZI) weight banks
   - Reference: Feldmann et al., 2019 (public academic publications)
   - Note: Concepts and architectures are not copyrightable

===============================================================================
ORIGINAL WORK DECLARATION
===============================================================================

All specifications, architectures, calculations, code examples, and technical
descriptions in this project are original works created specifically for the
Open Photonic GPU project. To the extent possible under law, the authors have
dedicated all copyright and related rights to these works to the public domain
worldwide under CC0 1.0 Universal.

Original contributions include:
- Transceiver architecture (disaggregated, configurable)
- Optical memory hierarchy (M0-M3) specifications
- GPIO optical interface specifications
- Security profiles and threat models
- Performance calculations and simulations
- API designs (cl_opgpu_* extensions)
- System integration specifications

===============================================================================
NO THIRD-PARTY CODE OR CONTENT INCLUDED
===============================================================================

This project does NOT include:
- Third-party source code (all code examples are original)
- Third-party datasets (all data are calculations or public scientific facts)
- Third-party images or diagrams (all diagrams are original ASCII/text art)
- Third-party proprietary specifications (only public standards referenced)
- Trademarked logos or branding (only nominative text references)

===============================================================================
LICENSE SUMMARY
===============================================================================

- Original works: CC0 1.0 Universal (Public Domain Dedication)
- Third-party standards: Respective owners (nominative reference only)
- Scientific facts: Public domain (not copyrightable)
- Trademarks: Respective owners (nominative use only)

For questions about licensing or attributions, contact:
- Repository: https://github.com/Eremosisima/multilambda-voxel-sim
- Authors: eremosisima; Contreras, Francisco Javier

===============================================================================
END OF NOTICE
===============================================================================
