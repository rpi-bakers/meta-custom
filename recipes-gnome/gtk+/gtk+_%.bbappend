FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

EXTRA_OECONF += " --with-xinput=yes"
