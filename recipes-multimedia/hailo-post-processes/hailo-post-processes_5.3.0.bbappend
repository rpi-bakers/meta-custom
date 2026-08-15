
# hailo-post-processes error
do_install:append() {
    # cp: cannot create directory 'image/usr/include/hailo/tappas/general/': No such file or directory
    install -d "${D}${includedir}/hailo/tappas"
}

# libcamera-apps error.
do_install:append() {
    # post_processing_stages/hailo/hailo_yolo_inference.cpp:22:10: fatal error: detection/yolo_hailortpp.hpp: No such file or directory
    # post_processing_stages/hailo/hailo_postprocessing_stage.hpp:21:10: fatal error: hailo_objects.hpp: No such file or directory
    cp -a "${S}/general/." "${D}${includedir}/hailo/tappas/general/"

    #../git/post_processing_stages/hailo/hailo_yolo_inference.cpp:22:10: fatal error: detection/yolo_hailortpp.hpp: No such file or directory
    cp -a "${S}/libs/postprocesses/." "${D}${includedir}/hailo/tappas/"

    # FileExistsError: [Errno 17] File exists:
    #  'hailo-post-processes/usr/lib/pkgconfig/gsthailometa.pc'
    #  -> 'libcamera-apps/1.9.0/recipe-sysroot/usr/lib/pkgconfig/gsthailometa.pc'
    rm -f "${D}${libdir}/pkgconfig/gsthailometa.pc"
}
