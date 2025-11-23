SUMMARY = "Chicago95 GTK Windows 95 like"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""


BRANCH = "master"
SRCREV = "6b6ef76c58e2078c913420278b5e17e0aa566374"

SRC_URI = "git://github.com/grassmunk/Chicago95.git;branch=master;protocol=https"

S = "${WORKDIR}/git"

USER = "root"
HOME = "/${USER}"

RDEPENDS:${PN} += "bash"

inherit allarch

do_install() {
    install -d ${D}${datadir}/themes
    install -d ${D}${datadir}/icons
    install -d ${D}${datadir}/fonts
    install -d ${D}${datadir}/extras
    install -d ${D}${datadir}/plymouth/themes
    cp -r ${S}/Theme/Chicago95 ${D}${datadir}/themes/
    cp -r ${S}/Icons/* ${D}${datadir}/icons/
    cp -r ${S}/Cursors/* ${D}${datadir}/icons/
    cp -r ${S}/Extras/* ${D}${datadir}/extras/
    cp -v ${S}/Fonts/vga_font/LessPerfectDOSVGA.ttf ${D}${datadir}/fonts/
    cp -r ${S}/Fonts/bitmap/cronyx-cyrillic ${D}${datadir}/fonts/
    cp -r ${S}/Plymouth/Chicago95 ${D}${datadir}/plymouth/themes/
    cp -r ${S}/Plymouth/RetroTux ${D}${datadir}/plymouth/themes/
}

FILES:${PN} += " \
    ${datadir}/themes/Chicago95 \
    ${datadir}/icons/ \
    ${datadir}/fonts/ \
    ${datadir}/extras/ \
    ${datadir}/plymouth/themes/ \
"
