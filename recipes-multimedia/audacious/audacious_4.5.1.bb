SUMMARY = "Audacious is an open-source audio player"
LICENSE = "BSD-2-Clause & BSD-3-Clause & CC-BY-SA-4.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=50aa88e96d568f26b6cc1d09ef4f6465"

SRC_URI = "git://github.com/audacious-media-player/audacious.git;protocol=https;branch=master \
           file://.config \
"

# Modify these as desired
PV = "audacious-4.5.1"
SRCREV = "354946d0fe96d9a477f1b0c76a374667a155d1af"

S="${WORKDIR}/git"

DEPENDS = " \
    gtk+3 glib-2.0 gtk+ libarchive \
    qtbase qtsvg qtbase-native \
    dbus glib-2.0-native \
"

RDEPENDS:${PN} = " \
    audacious-plugins \
"

# This software is not capable of being built in a separate build directory.
# So autotools-brokensep is used as autotools.
inherit pkgconfig gettext mime-xdg autotools-brokensep

# "make clean" in this tree is fragile, so just skip it.
CLEANBROKEN = "1"

# Specify any options you want to pass to the configure script using EXTRA_OECONF:
EXTRA_OECONF = ""

# Ensure Qt tools (rcc etc.) are found from the native recipe sysroot
# rcc is installed into ${RECIPE_SYSROOT_NATIVE}/usr/libexec
EXTRA_OEMAKE += " QT_BINPATH=${RECIPE_SYSROOT_NATIVE}/usr/libexec"

USER = "root"
HOME = "/${USER}"

do_install:append() {
    # Copy the configuration file to the image
    install -d ${D}${HOME}/.config
    cp -r ${WORKDIR}/.config ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/.config/
}

# Ship application icons installed under /usr/share/icons
FILES:${PN} += " \
    ${datadir}/icons/hicolor/48x48/apps/audacious.png \
    ${datadir}/icons/hicolor/scalable/apps/audacious.svg \
    ${HOME}/.config/ \
"
