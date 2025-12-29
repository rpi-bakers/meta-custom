SUMMARY = "OpenTabletDriver - Open source user mode tablet driver"
HOMEPAGE = "https://opentabletdriver.net/"
LICENSE = "LGPL-3.0-only"
LIC_FILES_CHKSUM = "file://LICENSE;md5=3000208d539ec061b899bce1d9ce9404"

SRC_URI = " \
    git://github.com/OpenTabletDriver/OpenTabletDriver;protocol=https;branch=master \
    file://otd-daemon.service \
"

PV = "1.0+git"
SRCREV = "1cad28e3f6bc1616d4f01fbea127b105cddc0bbe"

S = "${WORKDIR}/git"

inherit systemd

SYSTEMD_SERVICE:${PN} = "otd-daemon.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"

DEPENDS = "dotnet libx11 libxrandr libevdev gtk+3 jq"

# Install dependencies and build
do_compile() {
    export PATH="/usr/bin:$PATH"
    ./eng/linux/package.sh --package BinaryTarBall --runtime linux-arm64
}

do_install:append() {
    cp -r ${S}/dist/opentabletdriver/* ${D}
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/otd-daemon.service ${D}${systemd_system_unitdir}/
}

FILES:${PN} += " \
	/usr/local/ \
	/etc/udev/70-opentabletdriver.rules \
"

# Skip QA check for already-stripped binaries
INSANE_SKIP:${PN} += "already-stripped"
