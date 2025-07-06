FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

inherit systemd

SRC_URI += " \
    file://x11vnc.service \
"
SYSTEMD_SERVICE:${PN} = "x11vnc.service"
SYSTEMD_AUTO_ENABLE = "enable"

do_install:append(){
	install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/x11vnc.service ${D}${systemd_system_unitdir}
}

FILES:${PN} += "\
    ${systemd_system_unitdir}/x11vnc.service \
"
