# OPGPU Technical Diagrams - Complete Set

> **Generated:** 2026-11-19
> **Format:** SVG (Scalable Vector Graphics) - High quality, scalable, web-friendly
> **Total Diagrams:** 6 technical diagrams covering all aspects of OPGPU architecture

---

## 📊 Diagram Index

### 1. System Architecture Diagram
**File:** `diagram_01_system_architecture.svg`

**Description:** Complete disaggregated system architecture showing:
- Host system (CPU/GPU/NPU) with OpenCL driver
- Configurable OPGPU transceiver (25-75W) with 16 tunable WDM channels
- Fiber optic link (0.5-5m SMF-28)
- Remote photonic module (100-500W) with M0-M3 memory hierarchy
- Optional GPIO optical module (15-30W) with 11 ports

**Key Features Shown:**
- Data flow between components
- Power budgets for each subsystem
- Optical connector types (MPO-12/APC)
- Memory hierarchy (M0 compute, M1 PCM, M2 VO2, M3 trim)

**Use Case:** Overview presentations, system documentation, architecture reviews

---

### 2. Transceiver Internal Architecture
**File:** `diagram_02_transceiver_internal.svg`

**Description:** Detailed internal block diagram of the configurable transceiver:
- PCIe 5.0 x8/x16 interface (64 GB/s)
- Reconfigurable FPGA/SoC with 6 sub-systems:
  - Profile Manager (auto-detection)
  - Dynamic Resource Allocator
  - Memory Controller (LSU + Prefetcher)
  - Compute Scheduler
  - GPIO Controller
  - Security Enforcer
- DDR5 staging memory (8-32 GB)
- 16 tunable WDM lasers + 9 GPIO lasers
- 16 photodetectors + TIA + ADC/DAC
- 9 configuration profiles table

**Key Features Shown:**
- Resource allocation per profile (RAM/GPU/GPIO/Hybrid/Dynamic)
- 16λ distribution strategies
- Performance specs (800 Gbps, 120-525 ns, 25-75W)

**Use Case:** Hardware design reviews, FPGA development, driver development

---

### 3. GPIO Module Architecture
**File:** `diagram_03_gpio_module.svg`

**Description:** Complete GPIO optical module specification:
- 11 optical ports with wavelength assignments:
  - GPIO-0 to GPIO-3: 4x 1310nm (control, 10-100 MHz)
  - GPIO-4 to GPIO-7: 4x 850nm (sensor, 1-10 Gbps)
  - GPIO-CLK: 1x 1550nm (clock distribution, 10-40 GHz)
  - GPIO-TRIG: 1x 1310nm (trigger, 100 MHz)
  - GPIO-INTER-0/1: 2x 1550nm WDM (inter-module, 400-800 Gbps)
- 2x MPO-12/APC connectors
- PCIe 5.0 x4 interface
- OpenCL GPIO API extensions (9 functions)

**Key Features Shown:**
- Port pinout and wavelength allocation
- Performance specs (800 Gbps aggregate, <1 ps jitter)
- Use cases (lab instrumentation, multi-module sync, sensor networks)

**Use Case:** GPIO module development, API documentation, integration guides

---

### 4. Security Profile Enforcement
**File:** `diagram_04_security_profiles.svg`

**Description:** Three-stage security architecture:
1. **Module Detection:** Auto-detection of H3/G3/G2/H1/H4 modules
2. **Adaptive Security Profiles:** Strategy-specific enforcement:
   - H3 PCM: Thermal isolation, duty-cycle limits, wear-leveling
   - G2 EO: RF isolation, power limits, periodic refresh
   - G3 Hybrid: Combined PCM+EO security
   - H1 3D: Per-plane power limits, alignment monitoring
   - H4 3D Advanced: Multi-axis calibration, forced redundancy
3. **Security Enforcement Mechanisms:**
   - Thermal monitoring + interlocks
   - Access control + authentication
   - Data encryption (AES-256-XTS at rest, AES-256-GCM in transit)
   - Integrity verification (firmware signing, immutable logs)
   - Availability protection (rate limiting, watchdog timers)

**Key Features Shown:**
- Threat model (10 identified threats)
- Compliance standards (FIPS 140-3, Common Criteria, ISO 27001, SOC 2)

**Use Case:** Security reviews, compliance documentation, threat modeling

---

### 5. Performance Comparison Charts
**File:** `diagram_05_performance_comparison.svg`

**Description:** Four comparison charts vs existing technologies:

**Bandwidth (GB/s):**
- DRAM DDR5: 50-100 GB/s
- HBM3: 800 GB/s
- Optane: 10-50 GB/s
- CXL Memory: 50-100 GB/s
- **OPGPU: 100-1000 GB/s** ← 2-10x improvement

**Latency (ns) - Lower is Better:**
- DRAM: 50-100 ns
- HBM3: 10-50 ns
- Optane: 100-300 ns
- CXL: 100-300 ns
- **OPGPU: 100-500 ns** ← Comparable to CXL

**Power Efficiency (pJ/bit) - Lower is Better:**
- DRAM: 10-50 pJ/bit
- HBM3: 15-30 pJ/bit
- Optane: 10-20 pJ/bit
- NVMe SSD: 1-5 pJ/bit
- **OPGPU: 0.1-1 pJ/bit** ← 10-50x improvement

**Cost ($/GB) - Lower is Better:**
- HBM3: $50-100/GB
- Optane: $50-100/GB
- DRAM: $5-10/GB
- NVMe SSD: $0.10-0.50/GB
- **OPGPU: TBD (target $1-5/GB)** ← Competitive with DRAM

**Use Case:** Marketing materials, investor presentations, technology comparisons

---

### 6. Memory Hierarchy and Data Flow
**File:** `diagram_06_memory_hierarchy.svg`

**Description:** M0-M3 memory hierarchy with data flow:

**Memory Levels:**
- **M0 (Compute):** MZI/Crossbar tiles, 10-50 ns, volatile optical
- **M1 (Persistent):** PCM Sb2S3, 160-720 MB, 100-200 ns, non-volatile
- **M2 (Volatile Buffer):** VO2, 64-384 MB, 10-50 ns, volatile
- **M3 (Trim/Mask):** Azobenzene/Spiropyran, calibration layer, 200-500 ns

**Data Flow (RAM Profile):**
- Host → PCIe → Transceiver → Fiber → Photonic Module
- Complete latency breakdown (200-525 ns total)
- Read vs write path differences
- OpenCL API operations (create, read, write, flush, lock, migrate)

**Key Features Shown:**
- Persistent memory survives power cycles
- Wear-leveling extends PCM endurance
- OMCC thermal scheduling across levels
- Full OpenCL 3.0 compatibility

**Use Case:** Software development, memory management, API documentation

---

## 🎨 Diagram Specifications

### Format
- **Type:** SVG (Scalable Vector Graphics)
- **Resolution:** Vector (infinite scalability, no pixelation)
- **Compatibility:** All modern browsers, vector editors (Illustrator, Inkscape), documentation tools
- **File Size:** 15-25 KB per diagram (very lightweight)

### Color Scheme
- **Blue (#4a90e2):** Host system, digital/electronic components
- **Orange (#f5a623):** Optical components, transceiver
- **Green (#7ed321):** Photonic module, memory
- **Red (#d0021b):** GPIO module
- **Gray (#6c757d):** Connectors, fiber links

### Typography
- **Titles:** 22-24px, bold
- **Section headers:** 14-18px, bold
- **Box titles:** 12-14px, bold
- **Body text:** 10-11px
- **Labels:** 10px

---

## 📁 File Locations

**Local (Downloads):**
```
C:\Users\PC\Downloads\OPGPU_proyecto\04_Resultados_simulacion_y_figuras\
├── diagram_01_system_architecture.svg
├── diagram_02_transceiver_internal.svg
├── diagram_03_gpio_module.svg
├── diagram_04_security_profiles.svg
├── diagram_05_performance_comparison.svg
└── diagram_06_memory_hierarchy.svg
```

**Repository (GitHub):**
```
open-photonic-gpu/figures/
├── diagram_01_system_architecture.svg
├── diagram_02_transceiver_internal.svg
├── diagram_03_gpio_module.svg
├── diagram_04_security_profiles.svg
├── diagram_05_performance_comparison.svg
└── diagram_06_memory_hierarchy.svg
```

---

## 🖼️ Usage Recommendations

### For Presentations
- **PowerPoint/Keynote:** Insert SVG directly (maintains scalability)
- **Google Slides:** Convert to PNG first (SVG support limited)
- **Recommended size:** Full slide (16:9 aspect ratio)

### For Documentation
- **Markdown:** Use `<img src="diagram.svg">` tag
- **PDF:** Convert SVG to PDF for vector quality
- **Web:** Embed SVG directly for crisp rendering

### For Printing
- **High-resolution:** SVG scales to any size without quality loss
- **Recommended:** 300 DPI minimum for print
- **Formats:** SVG → PDF → Print (best quality chain)

---

## 📊 Diagram Coverage Matrix

| Topic | Diagram | Coverage |
|---|---|---|
| **System Overview** | #1 System Architecture | ✅ Complete |
| **Transceiver Design** | #2 Transceiver Internal | ✅ Complete |
| **GPIO Module** | #3 GPIO Module | ✅ Complete |
| **Security** | #4 Security Profiles | ✅ Complete |
| **Performance** | #5 Performance Comparison | ✅ Complete |
| **Memory System** | #6 Memory Hierarchy | ✅ Complete |
| **BOM/Cost** | (In BOM document) | ✅ Complete |
| **FTO Analysis** | (In disclosure doc) | ✅ Complete |

---

## 🔄 Updating Diagrams

To modify diagrams:
1. Open SVG file in text editor (XML format)
2. Edit text, colors, positions directly
3. Save and refresh browser to preview
4. For major changes, use vector editor (Inkscape - free, or Illustrator)

**Key SVG Elements:**
- `<rect>` - Boxes/blocks
- `<text>` - Labels and text
- `<line>` - Connections
- `<polygon>` - Custom shapes
- `<linearGradient>` - Color gradients

---

## ✅ Quality Checklist

- [x] All diagrams use consistent color scheme
- [x] Typography is legible at 100% zoom
- [x] Arrows show clear data flow direction
- [x] Labels are concise and accurate
- [x] Technical specifications match documentation
- [x] SVG format ensures scalability
- [x] Files are lightweight (<25 KB each)
- [x] Compatible with all modern browsers

---

## 📝 Notes

- All diagrams are **conceptual** and represent the architecture described in OPGPU specification documents
- Actual implementation may vary based on design optimizations and manufacturing constraints
- Color choices optimized for both light and dark backgrounds
- All text in diagrams is in **English** for international compatibility

---

*Generated: 2026-11-19 | Open Photonic GPU (OPGPU) Project | CC0 1.0 Public Domain Intent*
