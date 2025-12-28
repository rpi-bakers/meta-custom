# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: verify that the following LICENSE and LIC_FILES_CHKSUM values
# are complete and correct for your usage.
# audacious core itself is 2-clause BSD, with bundled libguess under
# 3-clause BSD and some icons under CC-BY-SA-4.0.
LICENSE = "BSD-2-Clause & BSD-3-Clause & CC-BY-SA-4.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=50aa88e96d568f26b6cc1d09ef4f6465"

SRC_URI = "git://github.com/audacious-media-player/audacious.git;protocol=https;branch=master"

# Modify these as desired
PV = "audacious-4.5.1"
SRCREV = "354946d0fe96d9a477f1b0c76a374667a155d1af"

S="${WORKDIR}/git"

# NOTE: the following prog dependencies are unknown, ignoring: gdbus-codegen
# NOTE: unable to map the following pkg-config dependencies: Qt6Widgets Qt5Widgets Qt6Gui Qt6Core Qt6Svg Qt5Core Qt5Svg Qt5Gui
#       (this is based on recipes that have previously been built and packaged)
DEPENDS = " \
    gtk+3 glib-2.0 gtk+ libarchive \
    qtbase qtsvg qtbase-native \
    dbus glib-2.0-native \
"

# NOTE: if this software is not capable of being built in a separate build directory
# from the source, you should replace autotools with autotools-brokensep in the
# inherit line
inherit pkgconfig gettext mime-xdg autotools-brokensep

# Specify any options you want to pass to the configure script using EXTRA_OECONF:
EXTRA_OECONF = ""

# Ensure Qt tools (rcc etc.) are found from the native recipe sysroot
# rcc is installed into ${RECIPE_SYSROOT_NATIVE}/usr/libexec
EXTRA_OEMAKE += " QT_BINPATH=${RECIPE_SYSROOT_NATIVE}/usr/libexec"

# Ship application icons installed under /usr/share/icons
FILES:${PN} += " \
    ${datadir}/icons/hicolor/48x48/apps/audacious.png \
    ${datadir}/icons/hicolor/scalable/apps/audacious.svg \
"
