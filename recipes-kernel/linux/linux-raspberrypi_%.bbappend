# Disable in-tree Hailo PCIe driver from linux-raspberrypi.
# We use meta-hailo's out-of-tree hailo-pci recipe to keep driver and HailoRT versions aligned.

FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append = " file://disable-in-tree-hailo.cfg"
