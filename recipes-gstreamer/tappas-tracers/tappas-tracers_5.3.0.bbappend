# Recipe LICENSE includes obsolete licenses LGPLv2.1
LICENSE = "LGPL-2.1-only"

# TAPPAS source at current SRCREV no longer exposes Meson option include_blas.
EXTRA_OEMESON:remove = "-Dinclude_blas=false"

do_install:append() {
	# Keep opencv utils owned by libgsthailotools to avoid duplicate split packages.
	rm -f ${D}${libdir}/libhailo_opencv_utils.so*
}
