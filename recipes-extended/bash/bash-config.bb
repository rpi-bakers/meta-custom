SUMMARY = "bash configuration files"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI += " \
    file://.bashrc \
    file://.xprofile \
"

DEPENDS = "chicago95 ibus "

USER = "root"
HOME = "/${USER}"


do_install:append() {
    # Copy the configuration file to the image
    install -d ${D}${HOME}/
    cp ${WORKDIR}/.bashrc ${D}${HOME}/
    cp ${WORKDIR}/.xprofile ${D}${HOME}/
    chown -R ${USER}:${USER} ${D}${HOME}/.bashrc
    chown -R ${USER}:${USER} ${D}${HOME}/.xprofile

    # DOS prompt like settings from chicago95
    echo "source ${datadir}/extras/DOSrc" >> ${D}${HOME}/.bashrc

    # IBus environment variables
    echo 'exec /usr/bin/ibus-daemon -rxRd &' >> ${D}${HOME}/.bashrc

    # root home settings
    # nvme directory link
    ln -s /srv/apps ${D}${HOME}/apps
}

FILES:${PN} += " \
    ${HOME}/.bashrc \
    ${HOME}/.xprofile \
    ${HOME}/apps \
"

