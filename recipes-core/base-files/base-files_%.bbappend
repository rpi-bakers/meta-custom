FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append:raspberrypi3 = " file://fstab.raspberrypi3"
SRC_URI:append:raspberrypi5 = " file://fstab.raspberrypi5"

do_install:append:raspberrypi3() {
	install -m 0644 ${WORKDIR}/fstab.raspberrypi3 ${D}${sysconfdir}/fstab
}

do_install:append:raspberrypi5() {
	install -m 0644 ${WORKDIR}/fstab.raspberrypi5 ${D}${sysconfdir}/fstab
}
