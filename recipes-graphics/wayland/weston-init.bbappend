FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

# Generate TLS key and certificate for VNC server
# mkdir -p ~/.pki/CA/
# cd ~/.pki/CA
# openssl genrsa -out tls.key 2048
# openssl req -new -key tls.key -out tls.csr -subj "/CN=raspi5"
# openssl x509 -req -days 365 -in tls.csr -signkey tls.key -out tls.crt

SRC_URI += " \
    file://weston.ini \
    file://weston.service \
"

# Generate WESTONPASSWD strings by mkpasswd.
# echo "weston" | mkpasswd -m sha256crypt -S raspberry -s
WESTONPASSWD = "\$5\$raspberry\$PqNOLq8IFV/OXpTfhVfrFpVZfako2x2K0wInPIvI04A"

# Overriding the default weston user setting to set the VNC server access password.
USERADD_PARAM:${PN} = " \
    --home /home/weston \
    --shell /bin/sh \
    --user-group -G video,input,render,wayland \
    -p '${WESTONPASSWD}' \
    -u 2000 \
    weston \
"

DEPENDS:append = " openssl-native"

# Create a directory on the target device to store TLS key and certificate:
do_install:append(){
    KEY_DIR=${D}${sysconfdir}/vnc/keys/

    install -m 0755 -d ${KEY_DIR}

    openssl genrsa -out ${KEY_DIR}/tls.key 2048
    openssl req -new -key ${KEY_DIR}/tls.key -out ${KEY_DIR}/tls.csr -subj "/CN=raspi5"
    openssl x509 -req -days 365 -in ${KEY_DIR}/tls.csr -signkey ${KEY_DIR}/tls.key -out ${KEY_DIR}/tls.crt
    chmod 0600 ${KEY_DIR}/tls.crt
    chmod 0600 ${KEY_DIR}/tls.key
    chown -R weston:weston ${KEY_DIR}/*

    install -D -p -m0644 ${WORKDIR}/weston.ini ${D}${sysconfdir}/xdg/weston/weston.ini
    install -D -p -m0644 ${WORKDIR}/weston.service ${D}${systemd_system_unitdir}/weston.service
}

FILES:${PN} += "\
    ${sysconfdir}/vnc/keys \
"
