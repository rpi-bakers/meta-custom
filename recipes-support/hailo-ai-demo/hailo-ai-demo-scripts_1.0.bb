SUMMARY = "Hailo + rpicam AI smoke test scripts"
DESCRIPTION = "Installs helper scripts to validate Hailo runtime and Raspberry Pi camera post-process workflows"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    file://hailo-ai-smoke-test \
"

S = "${WORKDIR}"

SHELL = "/bin/bash"

RDEPENDS:${PN} += " \
    libcamera-apps \
"

H8L_HEFS = "\
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov5m_wo_spp.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov8m.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov11n.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov11s.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov8s.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov6n.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/scdepthv3.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov8s_pose.hef \
https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.14.0/hailo8l/yolov5n_seg.hef\
"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/hailo-ai-smoke-test ${D}${bindir}/hailo-ai-smoke-test


    # download HAILO8L models if the device architecture is HAILO8L

    # Set the resource directory
    RESOURCE_DIR="${D}${datadir}/hailo-models"
    mkdir -p "$RESOURCE_DIR"

    echo "Downloading HAILO8L models..."
    for url in ${H8L_HEFS}; do
        file_name=$(basename "$url")

        # Check if the file is for H8L and rename it accordingly (POSIX-safe)
        case "$url" in
        *hailo8l*|*h8l_rpi*)
            case "$url" in
            *barcode*) ;;
            *) file_name="${file_name%.hef}_h8l.hef" ;;
            esac
            ;;
        esac

        file_path="$RESOURCE_DIR/$file_name"

        bbnote "Downloading $file_name..."
        wget -q --show-progress "$url" -O "$file_path"
    done
}


FILES:${PN} += " \
    ${bindir}/hailo-ai-smoke-test \
"
FILES:${PN} += " \
    ${datadir}/hailo-models \
"
