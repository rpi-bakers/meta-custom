SUMMARY = "Hello World Java Example"
DESCRIPTION = "A simple Hello World Java program for Yocto"
LICENSE = "CLOSED"

SRC_URI = " \
    file://helloworld-java \
    file://HelloWorld.java \
"

S = "${WORKDIR}"

DEPENDS += "openjdk-25-jdk-native"
RDEPENDS:${PN} += "openjdk-25-jre"

do_compile() {
    # Compile java code.
    javac HelloWorld.java

    # Make Java archive. |Create|File|Entrypoint|
    jar cfe helloworld.jar HelloWorld HelloWorld.class
}

do_install() {
    install -d ${D}${bindir}
    install -m 0644 helloworld.jar ${D}${bindir}/
    install -m 0755 helloworld-java ${D}${bindir}/
}
