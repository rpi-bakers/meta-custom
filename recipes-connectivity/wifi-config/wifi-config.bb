SUMMARY = "Preconfigure Wi-Fi for Raspberry Pi 3 (wpa_supplicant)"
LICENSE = "CLOSED"
SRC_URI += " \
    file://wpa_supplicant-wlan0.conf.in \
    file://wlan0.network \
"

# wpa_supplicant-wlan0.conf.in is a template that will be processed to include the actual Wi-Fi password
# you can set the password in your environment before building in .bashrc or similar:
# .bashrc
# export WIFI_PASSWORD="your_secret_password"
# export BB_ENV_PASSTHROUGH_ADDITIONS="$BB_ENV_PASSTHROUGH_ADDITIONS WIFI_PASSWORD"
do_install() {
    # wpa_supplicant config
    install -d ${D}${sysconfdir}/wpa_supplicant
    install -Dm0644 ${WORKDIR}/wpa_supplicant-wlan0.conf.in \
                    ${D}${sysconfdir}/wpa_supplicant/wpa_supplicant-wlan0.conf
    sed -i 's|%%WIFI_PASSWORD%%|${WIFI_PASSWORD}|g' \
            "${D}${sysconfdir}/wpa_supplicant/wpa_supplicant-wlan0.conf"

    # systemd-networkd config
    install -d ${D}${sysconfdir}/systemd/network
    install -m 0644 ${WORKDIR}/wlan0.network ${D}${sysconfdir}/systemd/network/wlan0.network

    # Enable wpa_supplicant@wlan0 service
    install -d ${D}${sysconfdir}/systemd/system/multi-user.target.wants
    ln -sf /lib/systemd/system/wpa_supplicant@.service \
            ${D}${sysconfdir}/systemd/system/multi-user.target.wants/wpa_supplicant@wlan0.service
}

FILES:${PN} += " \
    ${sysconfdir}/wpa_supplicant/wpa_supplicant-wlan0.conf \
    ${sysconfdir}/systemd/network/wlan0.network \
    ${sysconfdir}/systemd/system/multi-user.target.wants/wpa_supplicant@wlan0.service \
    ${sysconfdir}/weston/certs \
"
