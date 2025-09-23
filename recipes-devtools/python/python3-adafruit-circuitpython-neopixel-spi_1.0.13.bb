SUMMARY = "SPI driven CircuitPython driver for NeoPixels."
HOMEPAGE = "https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel_SPI"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2d3e4e95e1116127154de8a3d894f3a5"

SRC_URI = "git://github.com/adafruit/Adafruit_CircuitPython_NeoPixel_SPI.git;protocol=https;branch=main"
SRCREV = "32df3ec8aff816d0d5724546ac1711553cce6108"
S = "${WORKDIR}/git"

inherit python_setuptools_build_meta

DEPENDS += "python3-setuptools-scm-native"

RDEPENDS:${PN} += " \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-adafruit-blinka \
    python3-adafruit-circuitpython-busdevice \
    python3-adafruit-circuitpython-pixelbuf \
"
