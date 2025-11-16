FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append:raspberrypi5 = " \
    file://xorg.conf.d/99-vc4.conf \
"

do_install:append:raspberrypi5 (){
    install -d ${D}${sysconfdir}/X11/xorg.conf.d/
    install -m 0644 ${WORKDIR}/xorg.conf.d/99-vc4.conf ${D}${sysconfdir}/X11/xorg.conf.d/
}

FILES:${PN}:append:raspberrypi5 = " ${sysconfdir}/X11/xorg.conf.d/*"

###############################################################################
# XP-PEN touch screen Support
# MatchProduct: Hanvon Ugee Artist 13 (2nd Gen)
#
SRC_URI:append = " \
    file://xorg.conf.d/99-calibration-xppen-Artist13-2ndGen.conf \
"
do_install:append () {
    install -d ${D}${sysconfdir}/X11/xorg.conf.d/
    install -m 0644 ${WORKDIR}/xorg.conf.d/99-calibration-xppen-Artist13-2ndGen.conf \
                    ${D}${sysconfdir}/X11/xorg.conf.d/99-calibration.conf
}

FILES:${PN}:append = " ${sysconfdir}/X11/xorg.conf.d/*"
