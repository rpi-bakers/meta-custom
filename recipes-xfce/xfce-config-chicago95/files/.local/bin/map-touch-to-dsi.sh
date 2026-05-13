#!/bin/sh

# Keep FT5x06 touch input mapped to a DSI output only.
# This avoids click/coordinate drift when HDMI is connected.

if ! command -v xinput >/dev/null 2>&1; then
    exit 0
fi

if ! command -v xrandr >/dev/null 2>&1; then
    exit 0
fi

find_dsi_output() {
    xrandr --query 2>/dev/null | awk '/^DSI-[0-9]+ connected/ { print $1; exit }'
}

find_touch_ids() {
    xinput list --short 2>/dev/null | awk -F'id=' '/11-0038 generic ft5x06|ft5x06/ { split($2, a, /[ \t]+/); if (a[1] != "") print a[1] }'
}

apply_map() {
    output="$(find_dsi_output)"
    [ -n "$output" ] || return 0

    find_touch_ids | while IFS= read -r id; do
        [ -n "$id" ] || continue
        xinput map-to-output "$id" "$output" >/dev/null 2>&1 || true
    done
}

connected_state() {
    xrandr --query 2>/dev/null | awk '/ connected/ { print $1":"$2 }' | tr '\n' ' '
}

# Give X a moment to finish enumerating devices/outputs.
sleep 3
apply_map

last_state="$(connected_state)"
while :; do
    sleep 2
    now_state="$(connected_state)"
    if [ "$now_state" != "$last_state" ]; then
        sleep 1
        apply_map
        last_state="$now_state"
    fi
done
