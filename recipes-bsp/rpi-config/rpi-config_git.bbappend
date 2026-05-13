FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

ENABLE_DSI_DISPLAY ??= "0"
DSI_OVERLAY ??= "vc4-kms-dsi-7inch"
DSI_PORT ??= ""
ENABLE_DUAL_DISPLAY ??= "0"

do_deploy:append:raspberrypi5() {
    if [ "${ENABLE_UART}" = "1" ] ; then
        # Append UART configuration under the Enable UART comment
        sed -i '/# Enable UART/a\dtparam=uart0_console' $CONFIG
    fi

    if [ "${ENABLE_NVME}" = "1" ] ; then
        echo "# enable PCIe and NVMe" >> $CONFIG
        echo "dtparam=nvme" >> $CONFIG
    fi

    # DSI + HDMI multi display on Raspberry Pi 5
    if [ "${ENABLE_DSI_DISPLAY}" = "1" ] ; then
        echo "# enable DSI + HDMI multi display" >> $CONFIG
        echo "display_auto_detect=1" >> $CONFIG
        if [ "${ENABLE_DUAL_DISPLAY}" = "1" ] ; then
            echo "max_framebuffers=2" >> $CONFIG
        else
            # Keep single framebuffer in DSI-only mode to avoid touch/click mapping issues.
            echo "max_framebuffers=1" >> $CONFIG
        fi
        echo "dtoverlay=${DSI_OVERLAY}" >> $CONFIG
    fi
}
