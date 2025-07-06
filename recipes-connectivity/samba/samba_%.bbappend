FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

LICENSE = "CLOSED"

SRC_URI += " \
    file://smb.conf \
    file://smb.service \
"

SYSTEMD_AUTO_ENABLE = "enable"

# Overwrite the default smb.conf file after do_rootfs.
# Overwriting smb.conf in do_install would cause unnecessary recompilation.
# smb.conf is not dependent on compiling Samba, so a recompilation can be avoided.
do_rootfs:append(){
	install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/smb.service ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/smb.conf ${D}${sysconfdir}/samba/smb.conf
}

FILES:${PN} += " \
    ${sysconfdir}/samba/smb.conf \
"

ROOTFS_POSTPROCESS_COMMAND += "set_samba_password_for_weston;"

set_samba_password_for_weston() {
    echo -e "weston\nweston\n" | chroot ${IMAGE_ROOTFS} pdbedit -a -u weston -t || true; \
}
