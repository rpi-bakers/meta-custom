# Recipe LICENSE includes obsolete licenses LGPLv2.1
LICENSE = "LGPL-2.1-only"

# TAPPAS source at current SRCREV no longer exposes Meson option include_blas.
EXTRA_OEMESON:remove = "-Dinclude_blas=false"
