FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://0014-fix-error-hiding-a-lifetime-that-s-elided-elsewhere-.patch \
    file://0015-fix-undefined-error.patch \
    file://0016-fix-rust-1.91-no_sanitize-removal-in-crabbyavif.patch \
"

GN_ARGS:append = ' removed_rust_stdlib_libs=["unicode_width"]'
