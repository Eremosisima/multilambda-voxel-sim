# OPGPU v0.5+ System Simulation Report (OMCC + P1-calibrated PCM/thermal)

## Configurations
- **OPGPU-GPU64 (GPU, OMCC off, P1 off)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-NPU64 (NPU, OMCC off, P1 off)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-TPU128 (TPU, OMCC off, P1 off)**: peak 33554.43 TOPS, PCIe 48.00 GB/s eff, tiles 128, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-NPU64-OMCC (NPU, OMCC on, P1 off)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-TPU128-OMCC (TPU, OMCC on, P1 off)**: peak 33554.43 TOPS, PCIe 48.00 GB/s eff, tiles 128, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-NPU64-OMCC-P1 (NPU, OMCC on, P1 on, PCM 5b IL 0.123dB margin 41.6C)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-TPU128-OMCC-P1 (TPU, OMCC on, P1 on, PCM 5b IL 0.123dB margin 41.6C)**: peak 33554.43 TOPS, PCIe 48.00 GB/s eff, tiles 128, WDM 8, M1 2.0 GB, M2 64.0 MB

## OpenCL queue model
- baseline: avg queue 8.214 ms, p95 16.369 ms, avg turnaround 8.888 ms, makespan 23.172 ms
- OMCC: avg queue 6.156 ms, p95 12.422 ms, avg turnaround 6.725 ms, makespan 18.841 ms

## Workload results
- OPGPU-GPU64/GEMV_4k: latency 1.6762 ms, util 0.6, runtime TOPS 0.02, energy 283.588 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-GPU64/GEMM_1024: latency 0.1230 ms, util 0.65, runtime TOPS 17.457, energy 909.342 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-GPU64/Conv_infer_batch1: latency 0.0212 ms, util 0.65, runtime TOPS 57.015, energy 491.573 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-GPU64/Attention_block: latency 0.0417 ms, util 0.65, runtime TOPS 12.88, energy 231.55 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64/GEMV_4k: latency 1.6762 ms, util 0.5, runtime TOPS 0.02, energy 280.233 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-NPU64/GEMM_1024: latency 0.1230 ms, util 0.72, runtime TOPS 17.457, energy 694.593 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64/Conv_infer_batch1: latency 0.0212 ms, util 0.72, runtime TOPS 57.015, energy 370.777 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64/Attention_block: latency 0.0417 ms, util 0.72, runtime TOPS 12.88, energy 177.863 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-TPU128/GEMV_4k: latency 1.6762 ms, util 0.45, runtime TOPS 0.02, energy 278.555 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-TPU128/GEMM_1024: latency 0.1230 ms, util 0.78, runtime TOPS 17.457, energy 587.219 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-TPU128/Conv_infer_batch1: latency 0.0212 ms, util 0.78, runtime TOPS 57.015, energy 310.379 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-TPU128/Attention_block: latency 0.0417 ms, util 0.78, runtime TOPS 12.88, energy 151.02 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64-OMCC/GEMV_4k: latency 0.5275 ms, util 0.5, runtime TOPS 0.064, energy 280.029 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-NPU64-OMCC/GEMM_1024: latency 0.0450 ms, util 0.72, runtime TOPS 47.712, energy 674.377 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-NPU64-OMCC/Conv_infer_batch1: latency 0.0149 ms, util 0.72, runtime TOPS 80.882, energy 358.907 uJ, bottleneck optical_compute, M1_persist True
- OPGPU-NPU64-OMCC/Attention_block: latency 0.0145 ms, util 0.72, runtime TOPS 37.043, energy 172.914 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-TPU128-OMCC/GEMV_4k: latency 0.4396 ms, util 0.45, runtime TOPS 0.076, energy 278.351 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-TPU128-OMCC/GEMM_1024: latency 0.0389 ms, util 0.78, runtime TOPS 55.238, energy 567.002 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-TPU128-OMCC/Conv_infer_batch1: latency 0.0074 ms, util 0.78, runtime TOPS 164.336, energy 298.509 uJ, bottleneck output_transfer, M1_persist True
- OPGPU-TPU128-OMCC/Attention_block: latency 0.0124 ms, util 0.78, runtime TOPS 43.195, energy 146.07 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-NPU64-OMCC-P1/GEMV_4k: latency 0.5454 ms, util 0.502, runtime TOPS 0.062, energy 278.419 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-NPU64-OMCC-P1/GEMM_1024: latency 0.0426 ms, util 0.724, runtime TOPS 50.462, energy 663.639 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-NPU64-OMCC-P1/Conv_infer_batch1: latency 0.0147 ms, util 0.724, runtime TOPS 82.021, energy 352.867 uJ, bottleneck optical_compute, M1_persist True
- OPGPU-NPU64-OMCC-P1/Attention_block: latency 0.0137 ms, util 0.724, runtime TOPS 39.281, energy 170.229 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-TPU128-OMCC-P1/GEMV_4k: latency 0.4675 ms, util 0.452, runtime TOPS 0.072, energy 276.741 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-TPU128-OMCC-P1/GEMM_1024: latency 0.0377 ms, util 0.784, runtime TOPS 57.038, energy 556.265 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-TPU128-OMCC-P1/Conv_infer_batch1: latency 0.0072 ms, util 0.784, runtime TOPS 166.669, energy 292.469 uJ, bottleneck output_transfer, M1_persist True
- OPGPU-TPU128-OMCC-P1/Attention_block: latency 0.0120 ms, util 0.784, runtime TOPS 44.679, energy 143.386 uJ, bottleneck input_transfer, M1_persist True

## Interpretation
- OMCC overlap/prefetch and M1 weight persistence reduce exposed transfer/programming overhead, improving effective TOPS and latency on reuse-heavy workloads.
- P1-calibrated configs incorporate PCM multilevel/IL and thermal scheduling margins (from P1 modeling), showing the performance/energy envelope under thermally-aware operation.
- Low-intensity or non-persistent cases remain limited by transfers/control; arbitration/verification add small overheads but enable RAS and correctness.
