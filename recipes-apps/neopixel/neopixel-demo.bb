SUMMARY = "NeoPixel LED lighting demo application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = " \
    file://blink.py \
    file://led_pattern.py \
    "

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    python3-adafruit-circuitpython-neopixel-spi \
"

do_install() {
    install -d ${D}${bindir}/neopixel
    install -m 0755 ${WORKDIR}/blink.py ${D}${bindir}/neopixel/blink.py
    install -m 0755 ${WORKDIR}/led_pattern.py ${D}${bindir}/neopixel/led_pattern.py
}
