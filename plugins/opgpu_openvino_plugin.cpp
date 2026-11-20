// ============================================================================
// Proyecto: Open Photonic GPU (OPGPU-TX-v1)
// Archivo: plugins/opgpu_openvino_plugin.cpp
// Licencia: CC0 1.0 Universal (Dominio Público)
// ============================================================================

#include <openvino/runtime/iplugin.hpp>
#include <openvino/op/matmul.hpp>
#include <openvino/op/convolution.hpp>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <vector>

struct __attribute__((packed)) omcc_tensor_cmd {
    uint32_t opcode;
    uint32_t rows;
    uint32_t cols;
    uint64_t weights_addr;
    uint64_t input_addr;
    uint64_t output_addr;
};

#define OPGPU_IOCTL_GET_ODD   _IOR('O', 1, uint32_t)
#define OPGPU_IOCTL_EXEC_OMCC _IOW('O', 2, struct omcc_tensor_cmd)

class OPGPUPlugin : public ov::IPlugin {
private:
    int dev_fd;
    uint32_t odd_descriptor;
public:
    OPGPUPlugin() {
        set_device_name("OPGPU");
        dev_fd = open("/dev/opgpu0", O_RDWR);
        if (dev_fd >= 0) ioctl(dev_fd, OPGPU_IOCTL_GET_ODD, &odd_descriptor);
        else odd_descriptor = 0x07300111;
    }
    ~OPGPUPlugin() override { if (dev_fd >= 0) close(dev_fd); }

    ov::SupportedOpsMap query_model(const std::shared_ptr<const ov::Model>& model,
                                    const ov::AnyMap& properties) const override {
        ov::SupportedOpsMap res;
        for (const auto& op : model->get_ops()) {
            if (ov::is_type<ov::op::v0::MatMul>(op) || ov::is_type<ov::op::v1::Convolution>(op)) {
                res[op->get_friendly_name()] = get_device_name();
            }
        }
        return res;
    }

    static std::vector<uint8_t> quantize_to_membrane_states(const float* weights, size_t count, float threshold) {
        std::vector<uint8_t> packed((count + 3) / 4, 0);
        for (size_t i = 0; i < count; ++i) {
            uint8_t state = 0b00;
            if (weights[i] > threshold) state = 0b01;
            else if (weights[i] < -threshold) state = 0b10;
            packed[i / 4] |= (state << ((i % 4) * 2));
        }
        return packed;
    }
};
OV_DEFINE_PLUGIN_CREATE_FUNCTION(OPGPUPlugin)
