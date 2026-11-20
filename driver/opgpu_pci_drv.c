// ============================================================================
// Proyecto: Open Photonic GPU (OPGPU-TX-v1)
// Archivo: driver/opgpu_pci_drv.c
// Licencia: CC0 1.0 / Dual MIT-GPL
// ============================================================================

#include <linux/module.h>
#include <linux/pci.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

#define OPGPU_VENDOR_ID 0x10EE
#define OPGPU_DEVICE_ID 0x903F
#define REG_SYS_STATUS  0x00
#define REG_ODD_DESC    0x04

struct opgpu_dev {
    struct pci_dev *pdev;
    void __iomem *bar0;
    u32 odd_raw;
    u8 arch_family;
    u8 logic_type;
    u8 sheet_count;
    u8 cap_flags;
};

static void opgpu_parse_odd(struct opgpu_dev *dev) {
    u32 status = ioread32(dev->bar0 + REG_SYS_STATUS);
    dev->odd_raw = ioread32(dev->bar0 + REG_ODD_DESC);

    dev->arch_family = (dev->odd_raw >> 0)  & 0x0F;
    dev->logic_type  = (dev->odd_raw >> 4)  & 0x0F;
    dev->sheet_count = (dev->odd_raw >> 8)  & 0xFF;
    dev->cap_flags   = (dev->odd_raw >> 24) & 0xFF;

    dev_info(&dev->pdev->dev, "OPGPU Status: 0x%X | ODD: 0x%08X | Laminas: %u\n",
             status, dev->odd_raw, dev->sheet_count);
}

static int opgpu_probe(struct pci_dev *pdev, const struct pci_device_id *id) {
    struct opgpu_dev *dev;
    int err;

    dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
    if (!dev) return -ENOMEM;

    dev->pdev = pdev;
    pci_set_drvdata(pdev, dev);

    err = pci_enable_device(pdev);
    if (err) return err;

    err = pci_request_regions(pdev, "opgpu_drv");
    if (err) goto err_disable;

    dev->bar0 = pci_iomap(pdev, 0, 0);
    if (!dev->bar0) {
        err = -ENOMEM;
        goto err_release;
    }

    opgpu_parse_odd(dev);
    return 0;

err_release:
    pci_release_regions(pdev);
err_disable:
    pci_disable_device(pdev);
    return err;
}

static void opgpu_remove(struct pci_dev *pdev) {
    struct opgpu_dev *dev = pci_get_drvdata(pdev);
    pci_iounmap(pdev, dev->bar0);
    pci_release_regions(pdev);
    pci_disable_device(pdev);
}

static const struct pci_device_id opgpu_ids[] = {
    { PCI_DEVICE(OPGPU_VENDOR_ID, OPGPU_DEVICE_ID) },
    { 0, }
};
MODULE_DEVICE_TABLE(pci, opgpu_ids);

static struct pci_driver opgpu_driver = {
    .name     = "opgpu_pci",
    .id_table = opgpu_ids,
    .probe    = opgpu_probe,
    .remove   = opgpu_remove,
};

module_pci_driver(opgpu_driver);
MODULE_LICENSE("Dual MIT/GPL");
