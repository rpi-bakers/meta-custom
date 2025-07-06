
PACKAGECONFIG:append: = " xwayland vnc"
FILES:${PN}:append: = " ${sysconfdir}/pam.d/weston-remote-access"
