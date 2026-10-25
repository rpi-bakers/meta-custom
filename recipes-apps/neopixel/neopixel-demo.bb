SUMMARY = "NeoPixel LED lighting demo application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = " \
    file://blink.py \
    file://config_pattern.py \
    file://config.py \
    file://key_input.py \
    file://led_pattern.py \
    file://led_strip.py \
    file://time_keeper.py \
    "

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    python3-adafruit-circuitpython-neopixel-spi \
"

do_install() {
    install -d ${D}${bindir}/neopixel
    install -m 0755 ${WORKDIR}/blink.py ${D}${bindir}/neopixel/blink.py
    install -m 0755 ${WORKDIR}/config_pattern.py ${D}${bindir}/neopixel/config_pattern.py
    install -m 0755 ${WORKDIR}/config.py ${D}${bindir}/neopixel/config.py
    install -m 0755 ${WORKDIR}/key_input.py ${D}${bindir}/neopixel/key_input.py
    install -m 0755 ${WORKDIR}/led_strip.py ${D}${bindir}/neopixel/led_strip.py
    install -m 0755 ${WORKDIR}/time_keeper.py ${D}${bindir}/neopixel/time_keeper.py
}
