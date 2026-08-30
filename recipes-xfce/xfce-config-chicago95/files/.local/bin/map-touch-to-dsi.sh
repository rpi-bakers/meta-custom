#!/bin/sh

DISPLAY_DSI="DSI-1-2"
DISPLAY_HDMI="HDMI-2"

find_touch_ids() {
    xinput list --short 2>/dev/null | awk -F'id=' '/11-0038 generic ft5x06|ft5x06/ { split($2, a, /[ \t]+/); if (a[1] != "") print a[1] }'
}

wait_for_output()
{
    output="$1"

    i=0
    while [ "$i" -lt 30 ]; do
            if xrandr --query | grep -q "^${output} connected"; then
                    echo "display ${output} connected!!!"
                    return 0
            fi
            echo "Wait for connection ${output}..."
            sleep 1
            i=$((i + 1))
    done

    return 1
}

sleep 3

wait_for_output "${DISPLAY_DSI}" || exit 1
wait_for_output "${DISPLAY_HDMI}" || exit 1

TOUCH_IDS=$(find_touch_ids)
echo "[map to touch] set Generic FT5x06 touchscreen ID=${TOUCH_IDS} -> ${DISPLAY_DSI}"
xinput map-to-output \
    "${TOUCH_IDS}" \
    "${DISPLAY_DSI}"

echo "[map to touch] set Tablet Pen -> ${DISPLAY_HDMI}"

xinput map-to-output \
    "OpenTabletDriver Virtual Artist Tablet Pen (0)" \
    "${DISPLAY_HDMI}"

echo "[map to touch] set display modes $DISPLAY_HDMI 0,0 - 1920x1080 | $DISPLAY_DSI 1920,600 - 800x480"
xrandr --output ${DISPLAY_HDMI} --mode 1920x1080 --pos 0x0
xrandr --output ${DISPLAY_DSI} --mode 800x480 --pos 1920x600
