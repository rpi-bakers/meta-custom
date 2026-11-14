FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://boot-ramdisk.cmd.in \
    file://boot.cmd.in \
"

do_configure() {
    if [ "${USE_RAMFS}" = "1" ]; then
        mv ${WORKDIR}/boot-ramdisk.cmd.in ${WORKDIR}/boot.cmd.in
    fi

}
