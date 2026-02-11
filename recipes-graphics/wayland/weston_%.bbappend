# Enable Xwayland for x11 applications
PACKAGECONFIG:append: = " xwayland"

# Enable VNC support
PACKAGECONFIG:append: = " vnc"
FILES:${PN}:append: = " ${sysconfdir}/pam.d/weston-remote-access"
