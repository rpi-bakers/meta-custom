SUMMARY = "Chicago95 config of xfce4"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI += " \
    file://.config/ \
"

HOME = "/root"

do_install:append() {
    # Copy the configuration file to the image
    install -d ${D}/${HOME}/.config
    cp -r ${WORKDIR}/.config ${D}/${HOME}/
    chown -R root:root ${D}/${HOME}/.config/
}

FILES:${PN} += " \
    ${HOME}/.config/ \
"

