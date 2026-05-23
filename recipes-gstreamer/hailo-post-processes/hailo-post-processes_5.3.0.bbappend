# Recipe LICENSE includes obsolete licenses LGPLv2.1
LICENSE = "LGPL-2.1-only"

# TAPPAS source at current SRCREV no longer exposes Meson option include_blas.
EXTRA_OEMESON:remove = "-Dinclude_blas=false"

# Some dependency chains reference hailo-post-processes-dev explicitly.
# Keep provider available even if no dev payload is produced by this SRCREV.
ALLOW_EMPTY:${PN}-dev = "1"

do_install:append() {
	# Keep gsthailometa owned by libgsthailotools to avoid duplicate ownership.
	rm -f ${D}${libdir}/libgsthailometa.so*
	# Keep opencv utils owned by libgsthailotools to avoid duplicate split packages.
	rm -f ${D}${libdir}/libhailo_opencv_utils.so*
}
