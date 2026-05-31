FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " file://0001-preview-meson-accept-qt6.patch"

# Enable GUI preview path for X11/desktop sessions.
PACKAGECONFIG:append = " qt"
