#!/bin/bash

# Immediately clear screen to black to prevent terminal text from showing
dd if=/dev/zero of=/dev/fb0 bs=1M count=1 2>/dev/null

source /home/pi/bin/imagearg.txt
echo "Starting fim with image: ${Image}"

TEMP_IMAGE="/tmp/marquee_display.png"

# Check if server already preprocessed the image
if [ -f "/tmp/marquee_preprocessed.png" ]; then
    echo "Using preprocessed image"
    cp /tmp/marquee_preprocessed.png "${TEMP_IMAGE}"
else
    echo "Processing image on the fly"
    # Resize to landscape dimensions (800x480) and rotate 270°
    convert "${Image}" -resize 800x480 -background black -gravity center -extent 800x480 -rotate 270 "${TEMP_IMAGE}"
fi

# Verify the file exists and is not empty
if [ ! -s "${TEMP_IMAGE}" ]; then
    echo "Error: Image file is empty or missing!"
    exit 1
fi

# Keep fim running - NO rotation needed since image is already rotated
(
  sleep infinity
) | /usr/bin/fim -T 1 --device /dev/fb0 -a -q --no-stat-push --autowindow "${TEMP_IMAGE}" 2>&1