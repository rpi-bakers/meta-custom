# Stage Hailo post-processing C++ headers for downstream builds (e.g. libcamera-apps hailo postproc).

do_install:append() {
    install -d ${D}${includedir}/hailo/tappas
    install -d ${D}${includedir}/hailo/tappas/general

    # Base headers used directly by libcamera-apps hailo sources.
    cp -a ${S}/general/. ${D}${includedir}/hailo/tappas/general/

    # Postprocess headers are included as "detection/...", "common/...", etc.
    # Keep that layout directly under ${includedir}/hailo/tappas.
    cp -a ${S}/libs/postprocesses/. ${D}${includedir}/hailo/tappas/

    # libgsthailotools also installs this .pc; keep a single provider to avoid
    # do_prepare_recipe_sysroot file collisions.
    rm -f ${D}${libdir}/pkgconfig/gsthailometa.pc

    # gsthailometa headers must also come from a single provider.
    rm -rf ${D}${includedir}/gsthailometa
}
