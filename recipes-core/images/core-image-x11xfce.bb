SUMMARY = "A very basic X11 image with a terminal + xfce"

IMAGE_FEATURES += "splash package-management x11-base"

LICENSE = "MIT"

inherit core-image features_check

REQUIRED_DISTRO_FEATURES = "x11"

QB_MEM = '${@bb.utils.contains("DISTRO_FEATURES", "opengl", "-m 512", "-m 256", d)}'

###################################################################

###############################################################################
# Japanese language support
IMAGE_LINGUAS ?= "ja-jp ja-jp.euc-jp"
GLIBC_GENERATE_LOCALES = "ja_JP.UTF-8 ja_JP.EUC-JP"
###############################################################################
# ssh server settings
IMAGE_FEATURES:append = " ssh-server-openssh"

# change sshd mode from socket activation to service mode
PACKAGECONFIG:pn-openssh = "systemd-sshd-service-mode"

IMAGE_INSTALL:append = " \
    wpa-supplicant iw \
    openssh openssh-sftp-server \
    wifi-config \
    x11vnc \
    \
    xauth \
    \
    xeyes \
    xclock \
    samba \
    xterm \
    \
    mono \
    mono-libs \
    dotnet \
    gtk+ \
    \
    xfce4-session \
    xfce4-terminal \
    xfwm4 \
    xfce4-settings \
    xfce4-panel \
    thunar \
    thunar-volman \
    xfdesktop \
    xfce4-notifyd \
    exo \
    \
    xfce4-panel-plugin-actions \
    xfce4-panel-plugin-applicationsmenu \
    xfce4-panel-plugin-clock \
    xfce4-panel-plugin-directorymenu \
    xfce4-panel-plugin-launcher \
    xfce4-panel-plugin-pager \
    xfce4-panel-plugin-separator \
    xfce4-panel-plugin-showdesktop \
    xfce4-panel-plugin-systray \
    xfce4-panel-plugin-tasklist \
    xfce4-panel-plugin-windowmenu \
    \
    xfce4-whiskermenu-plugin \
    xfce4-datetime-plugin \
    chicago95 \
    xfce-config-chicago95 \
    \
    ibus \
    anthy \
    ibus-anthy \
    \
    ttf-vlgothic \
    ttf-sazanami-gothic \
    ttf-sazanami-mincho \
    setxkbmap \
    \
"

###############################################################################
# splash screen settings
PREFERRED_PROVIDER_virtual/psplash = "plymouth"

IMAGE_INSTALL:append = " \
    plymouth \
"
