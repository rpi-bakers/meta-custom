FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += " \
    file://.config/ \
"

do_install:append(){
    # Copy the configuration file for tablet support
    install -d ${D}${HOME}/.config
    cp -r ${WORKDIR}/.config ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/.config/
}

FILES:${PN} += " \
    ${HOME}/.config/ \
"
