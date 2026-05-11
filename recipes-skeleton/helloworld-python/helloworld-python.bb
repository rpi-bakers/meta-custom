SUMMARY = "Hello World Python Example"
DESCRIPTION = "A simple Hello World Python program for Yocto"
LICENSE = "CLOSED"

SRC_URI = " \
    file://helloworld-python \
    file://helloworld.py \
"

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    python3 \
"

do_install() {
    install -d ${D}${bindir}
    install -m 0644 helloworld.py ${D}${bindir}/
    install -m 0755 helloworld-python ${D}${bindir}/
}
