# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=57d76440fc5c9183c79d1747d18d2410"

SRC_URI = " \
    git://github.com/rpi-bakers/neopixelctl.git;protocol=https;branch=main \
    file://neopixelctl/neopixelctl \
"

# Modify these as desired
PV = "1.0+git"
SRCREV = "be5cee4efb414a03f536f4ed7334b953d9d39530"

S = "${WORKDIR}/git"

DEPENDS += " \
    dotnet-native \
"

RDEPENDS:${PN} += " \
    dotnet \
    fontconfig \
    zlib \
"

do_configure () {
    :
}

do_compile () {
    cd ${PN}

dotnet publish \
    -c Release \
    -r linux-arm64 \
    --self-contained true \
    -p:PublishSingleFile=true \
    -p:PublishTrimmed=false \
    -p:DebugType=None \
    -p:DebugSymbols=false \
    -p:Deterministic=true \
    -p:ContinuousIntegrationBuild=true \
    -p:PathMap=${WORKDIR}=${bindir}/neopixel/ \
    -o ${S}/publish

}

do_install() {
    install -d ${D}${libdir}/neopixelctl
    install -d ${D}${bindir}/neopixel
    install -m 0755 ${S}/publish/* ${D}${libdir}/neopixelctl/
    install -m 0755 ${WORKDIR}/neopixelctl/neopixelctl ${D}${bindir}/neopixel/
}

#FILES:${PN} += " \
#    ${libdir}/neopixelctl \
#    ${bindir}/neopixelctl \
#"

INSANE_SKIP:${PN} += "already-stripped"
