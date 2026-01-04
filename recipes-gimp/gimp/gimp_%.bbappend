FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += " \
    file://.config/ \
"

do_install:append(){
    # Copy the configuration file for tablet support
    install -d ${D}${HOME}/.config
    cp -r ${WORKDIR}/.config ${D}/${HOME}/
    chown -R ${USER}:${USER} ${D}/${HOME}/.config/

	# gimptool-2.0 is a development helper for building plug-ins.
	# In this build it embeds TMPDIR paths and triggers do_package_qa [buildpaths].
	# Remove it from the target package to keep QA clean.
	rm -f ${D}${bindir}/gimptool-2.0
}

FILES:${PN} += " \
    ${HOME}/.config/ \
"
