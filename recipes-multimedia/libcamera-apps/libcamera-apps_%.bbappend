FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " file://0001-preview-meson-accept-qt6.patch"

# Enable GUI preview path for X11/desktop sessions.
PACKAGECONFIG:append = " qt"

do_install:append() {
    # Install hailo post process file.
    install -d ${D}${datadir}/rpicam-apps/assets
    install -m 0644 ${S}/assets/hailo_*.json ${D}${datadir}/rpicam-apps/assets/
}

FILES:${PN} += "${datadir}/rpicam-apps/assets/hailo_*.json"
