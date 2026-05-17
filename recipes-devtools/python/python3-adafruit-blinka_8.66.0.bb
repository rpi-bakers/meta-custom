SUMMARY = "CircuitPython APIs for non-CircuitPython versions of Python such as CPython on Linux and MicroPython."
HOMEPAGE = "https://github.com/adafruit/Adafruit_Blinka"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fccd531dce4b989c05173925f0bbb76c"

SRC_URI = "git://github.com/adafruit/Adafruit_Blinka.git;branch=main;protocol=https"
SRCREV = "ff8087595a74d27b9083cf17498439b5d9845fe3"

S = "${WORKDIR}/git"

inherit setuptools3

DEPENDS += "python3-setuptools-scm-native"

do_install:append() {
    # Upstream ships prebuilt pulseio helpers for several boards/arches.
    # They are not built by this recipe and can fail objcopy/split-debug on target arch switches.
    find ${D}${PYTHON_SITEPACKAGES_DIR}/adafruit_blinka/microcontroller -type f -name "libgpiod_pulsein*" -delete || true
}

RDEPENDS:${PN} += " \
    libgpiod \
    python3-adafruit-platformdetect \
    python3-adafruit-pureio \
    python3-core \
"

RDEPENDS:${PN}:append:rpi = " rpi-gpio"

COMPATIBLE_HOST:libc-musl:class-target = "null"

