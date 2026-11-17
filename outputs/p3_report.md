# P3 Modeling Report: Variability, 4/5-bit Modes, and M2 Refresh

- Combined sigma (5b/4b context): read 0.06, spatial 0.03, drift 0.01 rad
- 5b: step 0.274613 rad, SNR 1.35 dB, SER 0.038281, eff bits 4.992
- 4b: step 0.567533 rad, SNR 7.66 dB, SER 0.000000, eff bits 4.000
- Recommendation: **4b**

## M2 (VO2) refresh policy (conceptual)
- Hold 0.01 s, rate 100.0 Hz, overhead ~0.20% per 1ms window, energy ~0.050 uJ/window (example 1000000 cells)
- Policy: OMCC-scheduled background refresh with batched VO2 hold/restore; prioritize compute windows

## Assumptions
- Spatial variability modeled as per-cell Gaussian phase offset plus read/drift noise.
- Effective-bits proxy is conservative (not channel capacity).
- M2 refresh modeled as periodic hold maintenance for VO2 volatile state; rates/energy are conceptual.
- Targets: SER <= 1% (5b) or <= 0.1% (4b) as design goals.
