FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " file://client.conf"

do_install:append() {
    # Modify client.conf to enable autospawn
    # autospawn = yes
    # allow-autospawn-for-root = yes
    install -d ${D}${sysconfdir}/pulse
    cp -r ${WORKDIR}/client.conf ${D}${sysconfdir}/pulse/
}

FILES:${PN} += " \
    ${sysconfdir}/pulse/ \
"
