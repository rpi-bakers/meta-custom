FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# Enable XInput support for tablet devices
EXTRA_OECONF += " --with-xinput=yes"
