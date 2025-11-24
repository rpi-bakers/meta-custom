SUMMARY = "It is a Japanese input engine for IBus."
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=751419260aa954499f7abaabaa882bbe"

SRC_URI = " \
    git://github.com/ibus/ibus-anthy.git;branch=main;protocol=https \
"

SRCREV = "901fdec1208d11c293e43add60fe5c143f0817a7"
SRC_URI[md5sum] = "<md5>"
SRC_URI[sha256sum] = "<sha256>"

# | NOTE: make -j 12 ANTHY_INCLUDEDIR=/home/user/poky/build/tmp/work/
#         cortexa7t2hf-neon-vfpv4-poky-linux-gnueabi/ibus-anthy/1.0/recipe-sysroot/usr/include
# | make: *** No targets specified and no makefile found.  Stop.
inherit autotools

# | ../git/configure: line 18372: syntax error near unexpected token `ANTHY,'
inherit pkgconfig

# ERROR: ibus-anthy-1.0-r0 do_configure: QA Issue:
#        AM_GNU_GETTEXT used but no inherit gettext [configure-gettext]
# ERROR: ibus-anthy-1.0-r0 do_configure: Fatal QA errors were found, failing task.
inherit gettext

# ERROR: ibus-anthy-1.0-r0 do_package: QA Issue:
#        ibus-anthy: Files/directories were installed but not shipped in any package:
#  /usr/share/icons
#  /usr/share/icons/hicolor
#  /usr/share/icons/hicolor/scalable
#  /usr/share/icons/hicolor/scalable/apps
#  /usr/share/icons/hicolor/scalable/apps/ibus-anthy.svg
# Please set FILES such that these items are packaged.
# Alternatively if they are unneeded, avoid installing them or delete them within do_install.
# ibus-anthy: 5 installed and not shipped files. [installed-vs-shipped]
# ERROR: ibus-anthy-1.0-r0 do_package: Fatal QA errors were found, failing task.
FILES:${PN} += "${datadir}/icons/"
# or inherit gtk-icon-cache

#REQUIRED_DISTRO_FEATURES = "x11"

S = "${WORKDIR}/git"

###############################################################################
# Dependencies
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Directly: anthy, ibus
# -----------------------------------------------------------------------------
# Indirect
# python3-pygobject-native -> _giscanner.so
# qemu-native -> qemu-arm
# -----------------------------------------------------------------------------
DEPENDS = " \
    anthy \
    ibus \
    python3-pygobject-native \
    qemu-native \
"

###############################################################################
# runtime error:
# -----------------------------------------------------------------------------
# python3-pygobject -> gi
#
# Traceback (most recent call last):
# File "/usr/share/ibus/setup/main.py", line 33, in <module>
# File "/usr/share/ibus-anthy/engine/main.py", line 31, in <module>
#   from gi import require_version as gi_require_version
# ModuleNotFoundError: No module named 'gi'
RDEPENDS:${PN} = " \
    anthy \
    ibus \
    python3-pygobject \
"

###############################################################################
# ERROR: ibus-anthy-1.0-r0 do_package_qa: QA Issue:
# File /usr/lib/libanthygobject-1.0.so.5.0.517 in package
# ibus-anthy doesn't have GNU_HASH (didn't pass LDFLAGS?) [ldflags]
# -----------------------------------------------------------------------------
LDFLAGS="-L${STAGING_LIBDIR}"
TARGET_CC_ARCH += "${LDFLAGS}"

###############################################################################
# fix required file './ABOUT-NLS' not found
# fix No module named 'giscanner._giscanner
# -----------------------------------------------------------------------------
do_configure:prepend() {
    touch ${S}/ABOUT-NLS
    ln -sf ${STAGING_LIBDIR_NATIVE}/gobject-introspection/giscanner/_giscanner.cpython-312-x86_64-linux-gnu.so \
            ${STAGING_LIBDIR_NATIVE}/gobject-introspection/giscanner/_giscanner.so
}

###############################################################################
#| make[2]: *** No rule to make target '/usr/include/anthy/anthy.h', needed by 'Anthy-9000.gir'.  Stop.
#| make[1]: *** [Makefile:524: all-recursive] Error 1
# -----------------------------------------------------------------------------
do_compile() {
    oe_runmake \
        ANTHY_INCLUDEDIR="${STAGING_INCDIR}"
}

###############################################################################
# | /home/user/poky/build/tmp/hosttools/install: cannot create regular file
# '/usr/share/locale/ca/LC_MESSAGES/ibus-anthy.mo': Permission denied
#
# | make[1]: *** No rule to make target '/usr/include/anthy/anthy.h', needed by 'Anthy-9000.gir'.  Stop.
# | make: *** [Makefile:524: install-recursive] Error 1
# -----------------------------------------------------------------------------
do_install() {
    oe_runmake install \
        DESTDIR=${D} \
        ANTHY_INCLUDEDIR="${STAGING_INCDIR}"
}

###############################################################################
# fix run-time error:
# python3 path is setuped yocto build environment path.
# ibus-setup is required general schema included in org.freedesktop.ibus.gschema.xml
# -----------------------------------------------------------------------------
do_install:append() {
    sed -e "s|${HOSTTOOLS_DIR}/python3|/usr/bin/python3|g" \
        -i ${D}${libexecdir}/ibus-engine-anthy

    sed -e "s|${HOSTTOOLS_DIR}/python3|/usr/bin/python3|g" \
        -i ${D}${libexecdir}/ibus-setup-anthy

    cp ${STAGING_DATADIR}/glib-2.0/schemas/org.freedesktop.ibus.gschema.xml \
           ${D}${datadir}/glib-2.0/schemas/org.freedesktop.ibus.gschema.xml

    ${STAGING_BINDIR_NATIVE}/glib-compile-schemas ${D}${datadir}/glib-2.0/schemas

    # Set ibus environment variables.
    install -d ${D}${sysconfdir}/profile.d
    echo 'export GTK_IM_MODULE=ibus'            >> ${D}${sysconfdir}/profile.d/ibus.sh
    echo 'export QT_IM_MODULE=ibus'             >> ${D}${sysconfdir}/profile.d/ibus.sh
    echo 'export XMODIFIERS="@im=ibus"'         >> ${D}${sysconfdir}/profile.d/ibus.sh
    echo 'exec /usr/bin/ibus-daemon -rxRd &'    >> ${D}${sysconfdir}/profile.d/ibus.sh
}

###############################################################################
# ERROR: ibus-anthy-1.0-r0 do_package: QA Issue: ibus-anthy:
#        Files/directories were installed but not shipped in any package
# Please set FILES such that these items are packaged.
# Alternatively if they are unneeded, avoid installing them or delete them within do_install.
# -----------------------------------------------------------------------------
FILES:${PN} += " \
    ${libdir}/girepository-1.0/Anthy-9000.typelib \
    ${datadir}/metainfo/org.freedesktop.ibus.engine.anthy.metainfo.xml \
    ${datadir}/gir-1.0/Anthy-9000.gir \
    ${datadir}/ibus \
    ${datadir}/ibus/component/anthy.xml \
    ${datadir}/glib-2.0/schemas/org.freedesktop.ibus.engine.anthy.gschema.xml \
    ${datadir}/glib-2.0/schemas/org.freedesktop.ibus.gschema.xml \
    ${datadir}/glib-2.0/schemas/gschemas.compiled \
"
