FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " file://.config/ "

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
