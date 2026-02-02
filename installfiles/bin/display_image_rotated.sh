#!/bin/bash

# Immediately clear screen to black to prevent terminal text from showing
dd if=/dev/zero of=/dev/fb0 bs=1M count=1 2>/dev/null

source /home/pi/bin/imagearg.txt
echo "Starting fim with image: ${Image}"

# Create a temporary resized image
TEMP_IMAGE="/tmp/marquee_resized.png"

# Resize image to fit 800px width (landscape width after rotation), maintaining aspect ratio
convert "${Image}" -resize 800x480 -background black -gravity center -extent 800x480 "${TEMP_IMAGE}"

# Keep fim running by feeding it commands via stdin
(
  sleep infinity
) | /usr/bin/fim -T 1 --device /dev/fb0 -a -q --no-stat-push --autowindow -c rotate270 "${TEMP_IMAGE}" 2>&1