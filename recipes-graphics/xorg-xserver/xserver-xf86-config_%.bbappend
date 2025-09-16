FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append:raspberrypi5 = " \
    file://xorg.conf.d/99-vc4.conf \
"

do_install:append:raspberrypi5 (){
    install -d ${D}${sysconfdir}/X11/xorg.conf.d/
    install -m 0644 ${WORKDIR}/xorg.conf.d/99-vc4.conf ${D}${sysconfdir}/X11/xorg.conf.d/
}

FILES:${PN}:append:raspberrypi5 = " ${sysconfdir}/X11/xorg.conf.d/*"
