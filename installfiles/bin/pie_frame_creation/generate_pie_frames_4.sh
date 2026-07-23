#!/bin/bash
# Generate 101 frames (0-100) using a padded source image

OUTPUT_DIR="/usr/share/plymouth/themes/dual-splash"
#OUTPUT_DIR="/home/pi/creation/dual-splash"
#mkdir -p "$OUTPUT_DIR"

# --- Source Image ---
SUN_IMG="Synthwave-Sun.png" # Ensure this image is in the same folder as the script
PADDED_SUN="padded_sun_temp.png"

# --- Dimensions ---
SUN_SIZE=200
CANVAS_SIZE=240
CENTER_X=120  # Half of CANVAS_SIZE
CENTER_Y=120  # Half of CANVAS_SIZE
MASK_RADIUS=150 # Must be large enough to cover the corners of the sun
FRAMES=100

# ==========================================
# --- VISUAL TWEAKS ---
# ==========================================

# 1. Empty Track (Background Ghosting)
# 1.0 = fully visible (progress is shown only by the glow turning on). 
# 0.5 = half visible. 0.0 = completely invisible until filled.
BG_OPACITY=0.0

# 2. Outer Glow Effect
# The color and spread of the neon bloom radiating from the filled sun.
GLOW_COLOR="#FF00FF"    # Hex Magenta
GLOW_BLUR="0x8"         # Slightly increased from 6 to 8 for a smoother bloom in the larger canvas


echo "Pre-processing sun image to add glow padding..."
# This pads the 200x200 sun into the center of a 240x240 transparent canvas
convert "$SUN_IMG" -resize ${SUN_SIZE}x${SUN_SIZE}\! -background transparent -gravity center -extent ${CANVAS_SIZE}x${CANVAS_SIZE} "$PADDED_SUN"

echo "Generating 0 to $FRAMES frames..."

for i in $(seq 0 $FRAMES); do
    # Calculate angle in degrees and radians (3.6 degrees per 1%)
    degrees=$(echo "scale=4; $i * 3.6" | bc)
    radians=$(echo "scale=4; $degrees * 3.14159 / 180" | bc -l)

    if [ "$i" -eq 0 ]; then
        # 0% - Just the background sun
        convert -size ${CANVAS_SIZE}x${CANVAS_SIZE} xc:transparent \
            \( "$PADDED_SUN" -channel A -evaluate multiply $BG_OPACITY +channel \) -composite \
            "${OUTPUT_DIR}/progress-${i}.png"
            
    elif [ "$i" -eq 100 ]; then
        # 100% - Full sun, full glow
        convert -size ${CANVAS_SIZE}x${CANVAS_SIZE} xc:transparent \
            \( "$PADDED_SUN" -channel A -evaluate multiply $BG_OPACITY +channel \) -composite \
            \( "$PADDED_SUN" -fill "$GLOW_COLOR" -colorize 100% -blur $GLOW_BLUR \) -composite \
            "$PADDED_SUN" -composite \
            "${OUTPUT_DIR}/progress-${i}.png"
            
    else
        # 1% to 99% - Masked pie slice
        large_arc_flag=0
        if [ $(echo "$degrees > 180" | bc) -eq 1 ]; then
            large_arc_flag=1
        fi
        
        # Calculate arc end point for the mask
        end_x=$(echo "$CENTER_X + $MASK_RADIUS * s($radians)" | bc -l)
        end_y=$(echo "$CENTER_Y - $MASK_RADIUS * c($radians)" | bc -l)
        
        # Define the invisible cookie-cutter path
        PATH_CMD="path 'M $CENTER_X,$CENTER_Y L $CENTER_X,$((CENTER_Y - MASK_RADIUS)) A $MASK_RADIUS,$MASK_RADIUS 0 $large_arc_flag,1 $end_x,$end_y Z'"

        # Composite stack
        # 1. Base transparent canvas
        # 2. Add faint background sun
        # 3. Create the pie slice mask, apply to padded sun, and save the sharp slice to memory
        # 4. RESET compose mode to Over (Crucial fix for the edge glow!)
        # 5. Pull slice from memory, dye it magenta, blur it (creates glow on ALL edges), composite
        # 6. Pull sharp slice from memory, composite on top
        convert -size ${CANVAS_SIZE}x${CANVAS_SIZE} xc:transparent \
            \( "$PADDED_SUN" -channel A -evaluate multiply $BG_OPACITY +channel \) -composite \
            \( "$PADDED_SUN" \( -size ${CANVAS_SIZE}x${CANVAS_SIZE} xc:transparent -fill white -draw "$PATH_CMD" \) -alpha set -compose DstIn -composite -write mpr:slice +delete \) \
            -compose Over \
            \( mpr:slice -fill "$GLOW_COLOR" -colorize 100% -blur $GLOW_BLUR \) -composite \
            \( mpr:slice \) -composite \
            "${OUTPUT_DIR}/progress-${i}.png"
    fi
    
    echo -ne "Frame $i/$FRAMES\r"
done

# Clean up the temporary padded file
rm -f "$PADDED_SUN"

echo -e "\nDone! Generated 101 padded synthwave frames in $OUTPUT_DIR"