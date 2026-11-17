# P2 Modeling Report: Reliability (Noise, Endurance, Retention)

- Levels: 32, phase range: 8.513 rad, step: 0.274613 rad
- Read noise sigma: 0.06 rad -> SER 0.020500, within±1 1.000000, SNR_step 2.42 dB, effective bits (proxy) 4.897

## Endurance knee cycles (conceptual)
- M1 Sb2S3: 1.00e+06, M2 VO2: 1.00e+07, M0 Spiropyran: 1.00e+04, M0 Azobenzene: 1.00e+05

## Retention characteristic (s, conceptual)
- M1 Sb2S3: 1.00e+08, M2 VO2 volatile hold: 1.00e-02, M0 Spiropyran: 1.00e+05, M0 Azobenzene: 1.00e+04

## Assumptions
- Noise model: Gaussian phase/readout noise mapped to nearest-level decisions over P1 phase range/levels.
- Endurance/retention use parametric curves (contrast knee, exponential/accelerated retention) informed by reported trends; not device-measured.
- M2 (VO2) treated as volatile/hold element requiring refresh/bias in sustained operation.
- Photochromic materials (azobenzene/spiropyran) modeled for lower-frequency config/trim roles with fatigue considerations.

## Reference context
- Sb2S3 multilevel/endurance trends (e.g. Nat. Commun. 2023 10.1038/s41467-023-39180-3)
- VO2 photonic memory endurance (npj Nanophotonics 2024 10.1038/s44310-024-00038-1)
- Nanostructured PCM endurance/loss improvements (arXiv 2604.08637)
- Photonic memory/cycling reviews (e.g. MRS Bulletin/Science Bulletin PCM photonics literature)
