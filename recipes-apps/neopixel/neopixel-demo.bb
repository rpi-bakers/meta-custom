SUMMARY = "NeoPixel LED lighting demo application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = " \
    file://neopixel-demo/ \
    "

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    python3-adafruit-circuitpython-neopixel-spi \
"

do_install() {
    install -d ${D}${bindir}/neopixel
    install -m 0755 ${WORKDIR}/neopixel-demo/*.py ${D}${bindir}/neopixel/
}
