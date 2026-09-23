#!/bin/sh

export PATH=/sbin:/bin:/usr/sbin:/usr/bin

mount -t devtmpfs devtmpfs /dev
mount -t proc proc /proc
mount -t sysfs sysfs /sys

# wait for the kernel log output.
sleep 3

echo
echo "============================================================================="
echo "Raspberry Pi 3 FIT initramfs"
uname -a
echo "-----------------------------------------------------------------------------"
echo "Environment variables:"
env
echo "============================================================================="
echo

# UART :login skip
setsid getty -L -n -l /bin/sh ttyS0 115200 vt100 &

# DSI :login skip
setsid getty -L -n -l /bin/sh tty1 0 vt100 &

# PID 1 must stay alive
while true
do
    sleep 3600
done
