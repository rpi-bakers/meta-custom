SUMMARY = "SL(1): Cure your bad habit of mistyping"
DESCRIPTION = "SL (Steam Locomotive) runs across your terminal \
				when you type 'sl' as you meant to type 'ls'. \
				It's just a joke command, and not useful at all."
HOMEPAGE = "https://github.com/mtoyoda/sl"
LICENSE = "Toyoda"
LIC_FILES_CHKSUM = "file://LICENSE;md5=74e9dd589a0ab212a9002b15ef2b82f0"

SRC_URI = "git://github.com/mtoyoda/sl.git;protocol=https;branch=master"

SRCREV = "923e7d7ebc5c1f009755bdeb789ac25658ccce03"

S = "${WORKDIR}/git"

DEPENDS += "ncurses"

do_compile () {
	${CC} ${CPPFLAGS} ${CFLAGS} -o sl sl.c ${LDFLAGS} -lncurses
}

do_install () {
	install -d ${D}${bindir}
	install -m 0755 sl ${D}${bindir}/sl
}
