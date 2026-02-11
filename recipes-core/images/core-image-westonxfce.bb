SUMMARY = "A very basic Wayland image with a terminal"

IMAGE_FEATURES += "splash package-management hwcodecs weston"

LICENSE = "MIT"

inherit core-image

CORE_IMAGE_BASE_INSTALL += "gtk+3-demo"
CORE_IMAGE_BASE_INSTALL += "${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'weston-xwayland matchbox-terminal', '', d)}"

QB_MEM = "-m 512"

IMAGE_INSTALL:append = " \
    xauth \
    mono \
    mono-libs \
    dotnet \
    xterm \
    xeyes \
    xclock \
    gtk+ \
    \
"
###############################################################################
# Network services
IMAGE_INSTALL:append = " \
    wpa-supplicant iw \
    openssh openssh-sftp-server \
    wifi-config \
    samba \
"
