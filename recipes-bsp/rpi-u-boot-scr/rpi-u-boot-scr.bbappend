FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://boot-ramdisk.cmd.in \
"

do_configure() {
    if [ -z "${CMDLINE_ROOTFS}" ]; then
        mv ${WORKDIR}/boot-ramdisk.cmd.in ${WORKDIR}/boot.cmd.in
    fi
}
