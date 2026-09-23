SUMMARY = "Custom initramfs image for Raspberry Pi 3"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
SRC_URI = "file://init-boot.sh"

S = "${WORKDIR}"

do_install() {
        install -m 0755 ${WORKDIR}/init-boot.sh ${D}/init
}

FILES:${PN} += "/init"
