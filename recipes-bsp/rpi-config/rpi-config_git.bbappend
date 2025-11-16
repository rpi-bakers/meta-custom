FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

do_deploy:append:raspberrypi5() {
    if [ "${ENABLE_UART}" = "1" ] ; then
        # Append UART configuration under the Enable UART comment
        sed -i '/# Enable UART/a\dtparam=uart0_console' $CONFIG
    fi

    if [ "${ENABLE_NVME}" = "1" ] ; then
        echo "# enable PCIe and NVMe" >> $CONFIG
        echo "dtparam=pciex1" >> $CONFIG
        echo "dtparam=nvme" >> $CONFIG
    fi
}