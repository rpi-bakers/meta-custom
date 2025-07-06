FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

# mkdir -p ~/.pki/CA/private/ cd ~/.pki/CA
# openssl genrsa -out private/cakey.pem 2048
# openssl req -new -x509 -nodes -days 365000 -key private/cakey.pem -out cacert.pem
# openssl genrsa -out tls.key 2048
# openssl req -new -key tls.key -out tls.csr
# openssl req -new -key tls.key -out tls.csr -subj "/CN=raspi3"
# openssl x509 -req -days 365 -in tls.csr -out tls.crt -CA cacert.pem -CAkey private/cakey.pem -CAcreateserial

SRC_URI += " \
    file://tls.crt \
    file://tls.key \
    file://weston.ini \
"

# Set password weston (from mkpasswd -m sha256crypt) for user weston
WESTONPASSWD = "\$5\$raspberry\$PqNOLq8IFV/OXpTfhVfrFpVZfako2x2K0wInPIvI04A"
USERADD_PARAM:${PN} = " \
    --home /home/weston \
    --shell /bin/sh \
    --user-group -G video,input,render,wayland \
    -p '${WESTONPASSWD}' \
    weston \
"

# Create a directory on the target device to store TLS key and certificate:
do_install:append(){
    install -m 0755 -d ${D}${sysconfdir}/vnc/keys/
    chown weston:weston ${D}${sysconfdir}/vnc/keys/
    install -m 0644 ${WORKDIR}/tls.crt ${D}${sysconfdir}/vnc/keys/tls.crt
    install -m 0644 ${WORKDIR}/tls.key ${D}${sysconfdir}/vnc/keys/tls.key
   	install -D -p -m0644 ${WORKDIR}/weston.ini ${D}${sysconfdir}/xdg/weston/weston.ini
    install -D -p -m0644 ${WORKDIR}/weston.service ${D}${systemd_system_unitdir}/weston.service
}

FILES:${PN} += "\
    ${sysconfdir}/vnc/keys \
"
