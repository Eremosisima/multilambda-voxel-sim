# ============================================================================
# Proyecto: Open Photonic GPU (OPGPU-TX-v1)
# Archivo: sim/opgpu_multi_role_bench.py
# Licencia: CC0 1.0 Universal (Dominio Público / Prior Art)
# ============================================================================

import numpy as np

class OPGPUPhysicalCore:
    def __init__(self, sheets=4, temp_c=25.0, fiber_len_m=2.0):
        self.sheets = sheets
        self.temp_c = temp_c
        self.fiber_len_m = fiber_len_m
        self.n_su8 = 1.57
        self.wdm_channels = 16
        self.channel_rate_gbps = 50.0
        self.link_loss_db = 3.5 + (0.25 * 15.0) + (0.0002 * fiber_len_m)
        self.n_eff = self.n_su8 + (-1.8e-4 * (self.temp_c - 25.0))

    def optical_time_of_flight_ns(self):
        c_m_s = 2.9979e8
        t_fiber = (self.fiber_len_m * 2 * 1.468) / c_m_s
        t_sheet = (0.15 * self.n_eff) / c_m_s
        t_eo_oe = 4.5e-9
        return (t_fiber + t_sheet + t_eo_oe) * 1e9

    def apply_membrane_physics(self, ternary_matrix, input_matrix):
        phase_error = abs(self.n_eff - self.n_su8) * 150.0
        efficiency = np.clip(1.0 - phase_error, 0.5, 1.0)
        raw_out = np.dot(ternary_matrix, input_matrix) * efficiency
        noise = np.random.normal(0, 0.008, size=raw_out.shape)
        return raw_out + noise

def test_optical_ram(core):
    print("\n--- [1/4] SIMULACIÓN: RAM ÓPTICA (CXL.mem) ---")
    capacity_mb = core.sheets * 512
    data_tx = np.random.randint(0, 2, size=4096 * 8, dtype=np.uint8)
    bit_flip_prob = 1e-12 if abs(core.temp_c - 25.0) < 1.0 else 1e-3
    data_rx = np.bitwise_xor(data_tx, np.random.binomial(1, bit_flip_prob, size=data_tx.shape))
    print(f"Capacidad: {capacity_mb} MB | Latencia: {core.optical_time_of_flight_ns():.2f} ns | Errores: {np.sum(data_tx != data_rx)}")

def test_optical_gpu(core):
    print("\n--- [2/4] SIMULACIÓN: GPU ÓPTICA (OpenCL 3.0) ---")
    transform_tern = np.array([[1, -1, 0, 1], [1, 1, 0, -1], [0, 0, 1, 0], [0, 0, 0, 1]])
    vertices = np.random.uniform(-1.0, 1.0, size=(4, 16384))
    max_error = np.max(np.abs(np.dot(transform_tern, vertices) - core.apply_membrane_physics(transform_tern, vertices)))
    print(f"Compute Units: {core.sheets * 64} | Rendimiento: {core.sheets * 32.0:.1f} TOPS | Error max: {max_error:.4f}")

def test_optical_npu(core):
    print("\n--- [3/4] SIMULACIÓN: NPU ÓPTICA (OpenVINO) ---")
    k_tern = np.array([[-1, -1, -1, -1, 1, -1, -1, -1, -1]])
    patches = np.random.uniform(0, 1, size=(9, 900))
    mse = np.mean((np.dot(k_tern, patches) - core.apply_membrane_physics(k_tern, patches)) ** 2)
    print(f"Plugin: OpenVINO MatMul/Conv | MSE: {mse:.6f}")

def test_optical_tpu(core):
    print("\n--- [4/4] SIMULACIÓN: TPU ÓPTICA (Arreglo Sistólico) ---")
    w = np.random.choice([-1, 0, 1], size=(128, 128))
    x = np.random.uniform(-1.0, 1.0, size=(128, 32))
    out_opt = core.apply_membrane_physics(w, x)
    out_ref = np.dot(w, x)
    cos_sim = np.sum(out_opt * out_ref) / (np.linalg.norm(out_opt) * np.linalg.norm(out_ref))
    print(f"Similitud Coseno: {cos_sim:.5f} | Eficiencia: {(core.sheets * 32.0)/35.0:.2f} TOPS/W")

if __name__ == "__main__":
    core = OPGPUPhysicalCore(sheets=4, temp_c=25.0, fiber_len_m=2.0)
    test_optical_ram(core)
    test_optical_gpu(core)
    test_optical_npu(core)
    test_optical_tpu(core)
