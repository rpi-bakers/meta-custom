SUMMARY = "InfluxDB client"
HOMEPAGE = "https://github.com/influxdb/influxdb-python"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=f61c0d3948045e1c8ebe3d70cc888003"

SRC_URI = "git://github.com/influxdata/influxdb-python.git;protocol=https;branch=master"

PV = "1.0+git"
SRCREV = "37ff905fbefe33bc321e619ea970d015ccd8b434"

S = "${WORKDIR}/git"

inherit setuptools3

DEPENDS += "python3-setuptools-scm-native"

# WARNING: the following rdepends are determined through basic analysis of the
# python sources, and might not be 100% accurate.
# RDEPENDS:${PN} += "　\
#     python3-compression \
#     python3-core \
#     python3-datetime \
#     python3-io \
#     python3-json \
#     python3-math \
#     python3-numbers \
#     python3-pytz \
#     python3-requests \
#     python3-six \
#     python3-unittest \
#     python3-urllib3 \
# "

# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    dateutil.parser
#    distutils.spawn
#    mock
#    msgpack
#    nose.tools
#    numpy
#    pandas
#    pandas.util.testing
#    requests_mock
#    six.moves
#    six.moves.urllib.parse
#python3-nose \
#python3-distutils \
#
RDEPENDS:${PN} += " \
    python3-dateutil \
    python3-mock \
    python3-msgpack \
    python3-numpy \
    python3-pandas \
    python3-requests \
    python3-six \
    influxdb \
    curl \
"