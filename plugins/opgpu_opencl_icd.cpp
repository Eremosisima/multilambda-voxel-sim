// ============================================================================
// Proyecto: Open Photonic GPU (OPGPU-TX-v1)
// Archivo: plugins/opgpu_opencl_icd.cpp
// Licencia: CC0 1.0 Universal (Dominio Público)
// ============================================================================

#include <CL/cl.h>
#include <CL/cl_icd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <cstring>
#include <cstdio>

#define OPGPU_IOCTL_GET_ODD _IOR('O', 1, uint32_t)

struct _cl_device_id {
    const cl_icd_dispatch* dispatch;
    uint32_t odd_descriptor;
    uint32_t compute_units;
    uint64_t global_mem_bytes;
};

static _cl_device_id opgpu_cl_device;

void opgpu_cl_init_device() {
    uint32_t odd = 0x07300111;
    int fd = open("/dev/opgpu0", O_RDONLY);
    if (fd >= 0) {
        ioctl(fd, OPGPU_IOCTL_GET_ODD, &odd);
        close(fd);
    }
    uint8_t sheets = (odd >> 8) & 0xFF;
    if (sheets == 0) sheets = 1;
    opgpu_cl_device.odd_descriptor   = odd;
    opgpu_cl_device.compute_units    = sheets * 64;
    opgpu_cl_device.global_mem_bytes = (uint64_t)sheets * 512ULL * 1024ULL * 1024ULL;
}
