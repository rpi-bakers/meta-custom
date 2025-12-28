# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: verify that the following LICENSE and LIC_FILES_CHKSUM values
# are complete and correct for your usage.
# audacious core itself is 2-clause BSD, with bundled libguess under
# 3-clause BSD and some icons under CC-BY-SA-4.0.
LICENSE = "BSD-2-Clause & BSD-3-Clause & CC-BY-SA-4.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=7480b0a3c1b6f0fef60e60288ce36e9f"

SRC_URI = "git://github.com/audacious-media-player/audacious-plugins.git;protocol=https;branch=master"

# Modify these as desired
PV = "audacious-plugins-4.5.1"
SRCREV = "bc68ac4d54d1c9d8b71bd083459a26ac8b9392a6"

S="${WORKDIR}/git"

# NOTE: the following prog dependencies are unknown, ignoring: gdbus-codegen
# NOTE: unable to map the following pkg-config dependencies: Qt6Widgets Qt5Widgets Qt6Gui Qt6Core Qt6Svg Qt5Core Qt5Svg Qt5Gui
#       (this is based on recipes that have previously been built and packaged)
DEPENDS = " \
    audacious \
    json-glib \
    flac \
    libogg \
    libvorbis \
    mpg123 \
"

# NOTE: if this software is not capable of being built in a separate build directory
# from the source, you should replace autotools with autotools-brokensep in the
# inherit line
inherit pkgconfig gettext autotools-brokensep

# Opus (opusfile), WavPack, and Neon (HTTP/HTTPS) libraries are not
# currently available in this build, so disable those plugins to allow
# configure to succeed. Also disable the Qt OpenGL spectrum analyzer
# (qtglspectrum), which relies on Qt OpenGL APIs not present in this
# Qt6 configuration.
EXTRA_OECONF += " --disable-opus --disable-wavpack --disable-neon --disable-qtglspectrum"

# Ensure Qt tools (rcc etc.) are found from the native recipe sysroot
# rcc is installed into ${RECIPE_SYSROOT_NATIVE}/usr/libexec
#EXTRA_OEMAKE += " QT_BINPATH=${RECIPE_SYSROOT_NATIVE}/usr/libexec"

# Ship all audacious plugins and bundled skins
FILES:${PN} += " \
    ${libdir}/audacious \
    ${datadir}/audacious \
"
