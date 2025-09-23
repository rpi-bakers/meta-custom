SUMMARY = "A pure Python implementation of adafruit_pixelbuf for smaller boards."
HOMEPAGE = "https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=78a287ed9ac9062fc1aa26a863e5c39d"

SRC_URI = "git://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf.git;protocol=https;branch=main"
SRCREV = "dc4391ba0770e35e28a7e868aadd3f72e8ced45d"
S = "${WORKDIR}/git"

inherit python_setuptools_build_meta

DEPENDS += "python3-setuptools-scm-native"

RDEPENDS:${PN} += " \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-adafruit-blinka \
"
