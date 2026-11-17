# OPGPU v0.5 System Simulation Report (with OMCC)

## Configurations
- **OPGPU-GPU64 (GPU, OMCC off)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-NPU64 (NPU, OMCC off)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-TPU128 (TPU, OMCC off)**: peak 33554.43 TOPS, PCIe 48.00 GB/s eff, tiles 128, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-NPU64-OMCC (NPU, OMCC on)**: peak 8388.61 TOPS, PCIe 48.00 GB/s eff, tiles 64, WDM 8, M1 2.0 GB, M2 64.0 MB
- **OPGPU-TPU128-OMCC (TPU, OMCC on)**: peak 33554.43 TOPS, PCIe 48.00 GB/s eff, tiles 128, WDM 8, M1 2.0 GB, M2 64.0 MB

## OpenCL queue model
- baseline: avg queue 8.214 ms, p95 16.369 ms, avg turnaround 8.888 ms, makespan 23.172 ms
- OMCC: avg queue 6.156 ms, p95 12.422 ms, avg turnaround 6.725 ms, makespan 18.841 ms

## Workload results
- OPGPU-GPU64/GEMV_4k: latency 0.6522 ms, util 0.6, runtime TOPS 0.051, energy 283.588 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-GPU64/GEMM_1024: latency 0.1230 ms, util 0.65, runtime TOPS 17.466, energy 909.342 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-GPU64/Conv_infer_batch1: latency 0.0212 ms, util 0.65, runtime TOPS 57.018, energy 491.573 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-GPU64/Attention_block: latency 0.0416 ms, util 0.65, runtime TOPS 12.909, energy 231.55 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64/GEMV_4k: latency 0.6522 ms, util 0.5, runtime TOPS 0.051, energy 280.233 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-NPU64/GEMM_1024: latency 0.1230 ms, util 0.72, runtime TOPS 17.466, energy 694.593 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64/Conv_infer_batch1: latency 0.0212 ms, util 0.72, runtime TOPS 57.018, energy 370.777 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64/Attention_block: latency 0.0416 ms, util 0.72, runtime TOPS 12.909, energy 177.863 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-TPU128/GEMV_4k: latency 0.6522 ms, util 0.45, runtime TOPS 0.051, energy 278.555 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-TPU128/GEMM_1024: latency 0.1230 ms, util 0.78, runtime TOPS 17.466, energy 587.219 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-TPU128/Conv_infer_batch1: latency 0.0212 ms, util 0.78, runtime TOPS 57.018, energy 310.379 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-TPU128/Attention_block: latency 0.0416 ms, util 0.78, runtime TOPS 12.909, energy 151.02 uJ, bottleneck input_transfer, M1_persist False
- OPGPU-NPU64-OMCC/GEMV_4k: latency 0.1958 ms, util 0.5, runtime TOPS 0.171, energy 280.029 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-NPU64-OMCC/GEMM_1024: latency 0.0450 ms, util 0.72, runtime TOPS 47.712, energy 674.377 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-NPU64-OMCC/Conv_infer_batch1: latency 0.0149 ms, util 0.72, runtime TOPS 80.882, energy 358.907 uJ, bottleneck optical_compute, M1_persist True
- OPGPU-NPU64-OMCC/Attention_block: latency 0.0145 ms, util 0.72, runtime TOPS 37.043, energy 172.914 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-TPU128-OMCC/GEMV_4k: latency 0.1631 ms, util 0.45, runtime TOPS 0.206, energy 278.351 uJ, bottleneck weight_transfer, M1_persist False
- OPGPU-TPU128-OMCC/GEMM_1024: latency 0.0389 ms, util 0.78, runtime TOPS 55.238, energy 567.002 uJ, bottleneck input_transfer, M1_persist True
- OPGPU-TPU128-OMCC/Conv_infer_batch1: latency 0.0074 ms, util 0.78, runtime TOPS 164.336, energy 298.509 uJ, bottleneck output_transfer, M1_persist True
- OPGPU-TPU128-OMCC/Attention_block: latency 0.0124 ms, util 0.78, runtime TOPS 43.195, energy 146.07 uJ, bottleneck input_transfer, M1_persist True

## Interpretation
- OMCC overlap/prefetch and M1 weight persistence reduce exposed transfer/programming overhead, improving effective TOPS and latency on reuse-heavy workloads.
- Low-intensity or non-persistent cases remain limited by transfers/control; arbitration/verification add small overheads but enable RAS and correctness.
- NPU/TPU modes benefit most when weights are stationary in optical RAM (M1) and pipelines are kept full via OMCC scheduling.
