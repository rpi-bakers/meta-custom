SUMMARY = "Chicago95 config of xfce4"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI += " \
    file://.config/ \
"
USER = "root"
HOME = "/${USER}"

do_install:append() {
    # Copy the configuration file to the image
    install -d ${D}${HOME}/.config
    cp -r ${WORKDIR}/.config ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/.config/
}

FILES:${PN} += " \
    ${HOME}/.config/ \
"
