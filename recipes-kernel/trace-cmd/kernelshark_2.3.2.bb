SUMMARY = "Graphical trace viewer for Ftrace"

LICENSE = "GPL-2.0-only & LGPL-2.1-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=751419260aa954499f7abaabaa882bbe \
                    file://kernel-shark.c;beginline=6;endline=8;md5=2c22c965a649ddd7973d7913c5634a5e"
PV = "2.3.2"

SRC_URI = " \
    git://git.kernel.org/pub/scm/linux/kernel/git/rostedt/trace-cmd.git;branch=trace-cmd-stable-v2.3 \
    file://0001-trace-cmd-Fix-build-with-gcc-10.patch \
    "
SRCREV = "79e08f8edb38c4c5098486caaa87ca90ba00f547"

DEPENDS = "gtk+"

inherit pkgconfig

S = "${WORKDIR}/git"

do_install() {
    ${MAKE} NO_PYTHON=1 prefix=${prefix} plugin_dir=${libdir}/trace-cmd/plugins DESTDIR=${D} install_gui
    ${MAKE} NO_PYTHON=1 prefix=${prefix} plugin_dir=${libdir}/trace-cmd/plugins DESTDIR=${D} install
}

FILES:${PN} += "${libdir}/trace-cmd/plugins/*.so"
FILES:${PN}-dbg += "${libdir}/trace-cmd/plugins/.debug/"
