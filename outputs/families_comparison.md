# Families Comparison (Conceptual)

| Key | Family | Inference (ps) | Reconfig (s) | Energy/op (pJ) | IL (dB) | NV | Interference | Maturity |
|---|---|---:|---:|---:|---:|---|---|---|
| A1 | Interferometric PCM (ref) | 10 | 2.0e-05 | 0.8 | 1.0 | yes | strong | medium |
| A2 | Interferometric PCM+EO hybrid | 10 | 1.0e-09 | 0.9 | 1.2 | partial | strong | medium |
| B1 | Resonant BIC/PCM | 50 | 5.0e-06 | 0.4 | 0.8 | yes | strong | medium |
| C1 | Electro-optic Pockels mesh | 5 | 5.0e-12 | 1.5 | 1.5 | no | strong | medium |
| C2 | EO nonvolatile/ferroelectric | 8 | 1.0e-09 | 1.0 | 1.3 | partial | strong | low |
| D1 | Plasmonic/ENZ hybrid | 1 | 1.0e-06 | 0.6 | 3.0 | depends | medium | low |
| E1 | All-optical nonlinear (Kerr/2D) | 0.5 | 1.0e-12 | 2.0 | 2.5 | no | medium | low |
| F1 | Diffractive/metasurface | 20 | 1.0e-06 | 0.5 | 1.5 | depends | strong | low |

## Notes
- Conceptual order-of-magnitude estimates for comparison only; not measured device data.
- Inference latency refers to signal propagation/modulation scale; system latency also includes I/O, memory and detection.
- Interference-native capability indicates suitability for additive/destructive (coherent) operations.
- Reconfiguration time ranges from EO/optical (fast) to PCM thermal programming (slow).

## Recommended incremental path
- A1 as open reference baseline (persistent weights, MVM).
- A2/B1 for efficiency/density with interference-native compute.
- C1/C2 for fast reload/streaming; D1/E1 for nonlinear/activation blocks; F1 for spatial parallelism.
