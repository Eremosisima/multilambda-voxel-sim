# P1 Modeling Report: Sb2S3 Segmented/Tapered Multilevel PCM Cell

- Material: Sb2S3, n_a=2.7, n_c=3.3, read λ=1550.0 nm, L=10.0 µm, segments=8
- Levels: 32 (5.0 bits), phase range 8.5127 rad (2.710 π)
- Mean/min phase step: 0.274603 / 0.274603 rad
- Insertion loss range: 0.1050–0.1400 dB
- Segmentation (mid-state IL est.): mono 0.0225 dB vs seg/taper 0.0825 dB

## Assumptions
- Linear mixing of effective index/absorption vs crystallinity fraction (first-order).
- Mode overlap and loss coefficients are design-estimate placeholders to be calibrated by FDTD/FEM and measurement.
- Energy estimates are normalized conceptual values proportional to effective switched volume and fraction.
- Material indices from project spec: Sb2S3 amorphous 2.70, crystalline 3.30; read at 1550 nm conceptually.

## Reference context
- Sb2S3 multilevel electrical control (Nat. Commun. 2023, 10.1038/s41467-023-39180-3)
- High-density/optimized PCM photonic memory (Photonics 2025, 10.3390/photonics12111130)
- Nanostructured/tapered PCM for low loss and endurance (arXiv 2604.08637)
