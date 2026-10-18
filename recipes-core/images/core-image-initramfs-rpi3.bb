SUMMARY = "Custom initramfs image for Raspberry Pi 3"
LICENSE = "MIT"

INITRAMFS_SCRIPTS ?= "initramfs-boot-rpi3"
PACKAGE_INSTALL = " \
    ${INITRAMFS_SCRIPTS} \
    busybox \
    base-files \
"

INITRAMFS_IMAGE = ""
IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"
IMAGE_NAME_SUFFIX ?= ""
INITRAMFS_MAXSIZE = "196000"

inherit core-image
