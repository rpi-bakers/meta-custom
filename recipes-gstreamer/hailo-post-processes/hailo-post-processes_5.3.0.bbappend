# Recipe LICENSE includes obsolete licenses LGPLv2.1
LICENSE = "LGPL-2.1-only"

# current SRCREV no longer supported options: "include_blas".
EXTRA_OEMESON:remove = "-Dinclude_blas=false"

do_install:append() {
	# Keep gsthailometa owned by libgsthailotools to avoid duplicate ownership.
	rm -f ${D}${libdir}/libgsthailometa.so*
	# Keep opencv utils owned by libgsthailotools to avoid duplicate split packages.
	rm -f ${D}${libdir}/libhailo_opencv_utils.so*
}
