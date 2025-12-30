SUMMARY = "Chicago95 config of xfce4"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI += " \
    file://.config/ \
    file://Desktop/ \
    file://.local/ \
"
USER = "root"
HOME = "/${USER}"

do_install:append() {
    # Copy the configuration file to the image
    install -d ${D}${HOME}/.config
    cp -r ${WORKDIR}/.config ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/.config/

    # Copy the Desktop files to the image
    install -d ${D}${HOME}/Desktop
    cp -r ${WORKDIR}/Desktop ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/Desktop

    # Copy the .local files to the image
    # 'share/gvfs-metadata/home' has Desktop shortcut's metadata.
    install -d ${D}${HOME}/.local
    cp -r ${WORKDIR}/.local ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/.local
}

FILES:${PN} += " \
    ${HOME}/.config/ \
    ${HOME}/Desktop/ \
    ${HOME}/.local/ \
"
