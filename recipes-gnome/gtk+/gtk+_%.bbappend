FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

EXTRA_OECONF += " --with-xinput=yes"
