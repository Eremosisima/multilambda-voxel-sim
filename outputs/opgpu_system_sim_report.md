# OPGPU v0.4 System Simulation Report

## Configurations
- **OPGPU-GPU64 (GPU)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-NPU64 (NPU)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-TPU128 (TPU)**: peak 33554.43 TOPS, PCIe 48.00 GB/s eff, tiles 128, WDM 8, M1 2.0 GB, M2 64.0 MB

## OpenCL queue model
- avg queue: 8.214 ms, p95: 16.369 ms, avg turnaround: 8.888 ms, makespan: 23.172 ms

## Workload results
- OPGPU-GPU64/GEMV_4k: latency 0.6527 ms, util 0.6, runtime TOPS 0.051, energy 283.588 uJ, bottleneck weight_transfer
- OPGPU-GPU64/GEMM_1024: latency 0.1400 ms, util 0.65, runtime TOPS 15.342, energy 909.342 uJ, bottleneck input_transfer
- OPGPU-GPU64/Conv_infer_batch1: latency 0.0309 ms, util 0.65, runtime TOPS 39.126, energy 491.573 uJ, bottleneck input_transfer
- OPGPU-GPU64/Attention_block: latency 0.0460 ms, util 0.65, runtime TOPS 11.662, energy 231.55 uJ, bottleneck input_transfer
- OPGPU-NPU64/GEMV_4k: latency 0.6527 ms, util 0.5, runtime TOPS 0.051, energy 280.233 uJ, bottleneck weight_transfer
- OPGPU-NPU64/GEMM_1024: latency 0.1399 ms, util 0.72, runtime TOPS 15.346, energy 694.593 uJ, bottleneck input_transfer
- OPGPU-NPU64/Conv_infer_batch1: latency 0.0309 ms, util 0.72, runtime TOPS 39.154, energy 370.777 uJ, bottleneck input_transfer
- OPGPU-NPU64/Attention_block: latency 0.0460 ms, util 0.72, runtime TOPS 11.665, energy 177.863 uJ, bottleneck input_transfer
- OPGPU-TPU128/GEMV_4k: latency 0.6525 ms, util 0.45, runtime TOPS 0.051, energy 278.555 uJ, bottleneck weight_transfer
- OPGPU-TPU128/GEMM_1024: latency 0.1274 ms, util 0.78, runtime TOPS 16.859, energy 587.219 uJ, bottleneck input_transfer
- OPGPU-TPU128/Conv_infer_batch1: latency 0.0238 ms, util 0.78, runtime TOPS 50.785, energy 310.379 uJ, bottleneck input_transfer
- OPGPU-TPU128/Attention_block: latency 0.0429 ms, util 0.78, runtime TOPS 12.519, energy 151.02 uJ, bottleneck input_transfer

## Interpretation
- NPU/TPU modes benefit high weight-reuse/intensity workloads (stationary weights in M1, pipelined optical MACs).
- Low-intensity cases are limited by PCIe/E-O-O-E and control overhead.
- Sb2S3 programming cost is amortized when weights persist across many reuses; VO2 switching supports fast runtime control.
