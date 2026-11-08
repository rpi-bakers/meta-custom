# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=57d76440fc5c9183c79d1747d18d2410"

SRC_URI = "git://github.com/rpi-bakers/neopixelctl.git;protocol=https;branch=main"

# Modify these as desired
PV = "1.0+git"
SRCREV = "be5cee4efb414a03f536f4ed7334b953d9d39530"

S = "${WORKDIR}/git"

DEPENDS += " \
    dotnet-native \
"

RDEPENDS:${PN} += " \
    dotnet \
"

do_configure () {
    :
}

do_compile () {
    cd ${PN}
    dotnet publish -c Release -r linux-arm --self-contained true -p:PublishSingleFile=true -p:PublishTrimmed=true -o ${S}/publish
}

do_install () {
    install -d ${D}${bindir}/neopixel
    install -m 0755 ${S}/publish/* ${D}${bindir}/neopixel/
}

INSANE_SKIP:${PN} += "already-stripped"
