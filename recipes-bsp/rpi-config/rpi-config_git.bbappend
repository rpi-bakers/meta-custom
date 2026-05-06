FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

ENABLE_DSI_DISPLAY ??= "0"
ENABLE_DSI_PRIMARY ??= "1"
DSI_OVERLAY ??= "vc4-kms-dsi-7inch"
DSI_PORT ??= ""

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

    # DSI + HDMI multi display on Raspberry Pi 5
    if [ "${ENABLE_DSI_DISPLAY}" = "1" ] ; then
        echo "# enable DSI + HDMI multi display" >> $CONFIG
        echo "display_auto_detect=1" >> $CONFIG
        echo "max_framebuffers=1" >> $CONFIG

        if [ "${ENABLE_DSI_PRIMARY}" = "1" ] ; then
            echo "display_default_lcd=1" >> $CONFIG
        fi

        # Ensure KMS is explicitly enabled when multi display is requested.
        if ! grep -q '^dtoverlay=vc4-kms-v3d' $CONFIG ; then
            echo "dtoverlay=vc4-kms-v3d" >> $CONFIG
        fi

        if [ -n "${DSI_PORT}" ] ; then
            echo "dtoverlay=${DSI_OVERLAY},${DSI_PORT}" >> $CONFIG
        else
            echo "dtoverlay=${DSI_OVERLAY}" >> $CONFIG
        fi
    fi
}
