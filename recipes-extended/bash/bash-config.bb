SUMMARY = "bash configuration files"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI += " \
    file://.bashrc \
"

DEPENDS = "chicago95 ibus "

USER = "root"
HOME = "/${USER}"


do_install:append() {
    # Copy the configuration file to the image
    install -d ${D}${HOME}/
    cp -r ${WORKDIR}/.bashrc ${D}${HOME}/
    chown -R ${USER}:${USER} ${D}${HOME}/.bashrc

    # DOS prompt like settings from chicago95
    echo "source ${datadir}/extras/DOSrc" >> ${D}${HOME}/.bashrc

    # IBus environment variables
    echo 'exec /usr/bin/ibus-daemon -rxRd &' >> ${D}${HOME}/.bashrc
}

FILES:${PN} += " \
    ${HOME}/.bashrc \
"

