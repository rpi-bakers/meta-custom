SUMMARY = "Hailo + rpicam AI smoke test scripts"
DESCRIPTION = "Installs helper scripts to validate Hailo runtime and Raspberry Pi camera post-process workflows"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    file://hailo-ai-smoke-test \
"

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    libcamera-apps \
"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/hailo-ai-smoke-test ${D}${bindir}/hailo-ai-smoke-test
}

FILES:${PN} += " \
    ${bindir}/hailo-ai-smoke-test \
"
