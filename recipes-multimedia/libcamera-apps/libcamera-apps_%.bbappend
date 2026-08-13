FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " \
    file://0001-fix-build-error-and-warnings.patch \
	file://HailoRT.pc_template \
    file://hailo-tappas-core.pc_template \
"

# Enable GUI preview path for X11/desktop sessions and enable Hailo/OpenCV
# by default via PACKAGECONFIG so meson receives the correct -D flags.
# Enable GUI preview path for X11/desktop sessions and enable Hailo/OpenCV
# by default via PACKAGECONFIG so meson receives the correct -D flags.
PACKAGECONFIG:append = " qt hailo opencv"

PACKAGECONFIG[hailo] = "-Denable_hailo=enabled, -Denable_hailo=disabled, libhailort "

# Ensure recipe build-time ordering so the Hailo CMake export and OpenCV
# libraries are present in the sysroot for meson to find. Meson requires
# CMake to be available to consume Hailo's CMake config, so add cmake-native
# for configure-time.
DEPENDS += " libhailort hailo-post-processes libgsthailotools opencv "

# Help Meson discover the upstream CMake exports when pkg-config is missing
# (point Meson/CMake to the installed HailoRT CMake config in the sysroot).
#MESON_ARGS:append = " -DHailoRT_DIR=${STAGING_DIR}/usr/lib/cmake/HailoRT"

HAILO_TAPPAS_CORE_VERSION ?= "3.31.0"
HAILO_TAPPAS_WORKSPACE ?= "/usr"
HAILORT_VERSION ?= "4.24.0"

#do_install:append() {
#    # Install hailo post process file.
#    #install -d ${D}${datadir}/rpicam-apps/assets
#    #install -m 0644 ${S}/assets/hailo_*.json ${D}${datadir}/rpicam-apps/assets/
#}

#FILES:${PN} += "${datadir}/rpicam-apps/assets/hailo_*.json"
FILES:${PN}:append = " ${datadir}/hailo-models"

# Package hailo post-processing shared objects that get installed under
# /usr/lib/hailo-post-processes so they are not left installed-but-unshipped.
FILES:${PN}:append = " ${libdir}/hailo-post-processes"

# Provide pkg-config fallbacks in the sysroot for HailoRT and tappas core
# from templates during configure-time.
do_configure:prepend() {
	# Ensure native cmake from recipe-sysroot-native is on PATH so Meson can
	# execute CMake for dependency discovery when needed.
	export PATH="${STAGING_DIR_NATIVE}/usr/bin:${PATH}"

	# Make any generated or staged .pc files visible to pkg-config during
	# meson configure (we create a minimal HailoRT.pc below as a fallback).
	export PKG_CONFIG_PATH="${RECIPE_SYSROOT}${libdir}/pkgconfig:${PKG_CONFIG_PATH}"

	pcdir="${RECIPE_SYSROOT}${libdir}/pkgconfig"
	mkdir -p "${pcdir}"

	# Generate HailoRT.pc from template.
	sed "s|^prefix=.*|prefix=/usr|; \
		 s|^libdir=.*|libdir=${libdir}|; \
		 s|^includedir=.*|includedir=${includedir}/hailort|; \
		 s|^Version:.*|Version: ${HAILORT_VERSION}|" \
		 "${WORKDIR}/HailoRT.pc_template" > "${pcdir}/HailoRT.pc"

	# Generate hailo-tappas-core.pc from template, following tappas upstream
	# pkg_config_setup.sh substitution style.
	case "${TARGET_ARCH}" in
		x86|x86_64)
			tappas_arch="x86_64"
			;;
		rpi5|rockchip|aarch64|rpi|arm*)
			tappas_arch="aarch64"
			;;
		*)
			tappas_arch="${TARGET_ARCH}"
			;;
	esac

	sed "s|tappas_workspace=|tappas_workspace=${HAILO_TAPPAS_WORKSPACE}|; \
		 s|arch=|arch=${tappas_arch}|; \
		 s|Version:|Version: ${HAILO_TAPPAS_CORE_VERSION}|; \
		 s|^tappas_libdir=.*|tappas_libdir=${RECIPE_SYSROOT}${libdir}|" \
		 "${WORKDIR}/hailo-tappas-core.pc_template" > "${pcdir}/hailo-tappas-core.pc"

	# Provide compatibility symlinks so Meson can find tappas post-processing
	# libraries regardless of directory naming (post-process / post_processes
	# vs hailo-post-processes).
	libdir_real="${RECIPE_SYSROOT}${libdir}"
	if [ -d "${libdir_real}/hailo-post-processes" ]; then
		ln -snf hailo-post-processes "${libdir_real}/post_processes"
	fi
}
