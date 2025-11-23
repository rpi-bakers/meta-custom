FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

do_deploy:append:raspberrypi5() {
    if [ "${ENABLE_UART}" = "1" ] ; then
        # Append UART configuration under the Enable UART comment
        sed -i '/# Enable UART/a\dtparam=uart0_console' $CONFIG
    fi

    # PCIe speed configuration
    # Gen2 dtparam=pciex1
    # Gen3 dtparam=pciex1_gen=3
    if [ "${ENABLE_NVME}" = "1" ] ; then
        echo "# enable PCIe and NVMe" >> $CONFIG
        echo "dtparam=pciex1_gen=3" >> $CONFIG
        echo "dtparam=nvme" >> $CONFIG
    fi
}