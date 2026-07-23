#!/bin/bash

# ARGUMENTS, IN ORDER:
#Argument 1 = the name of the system for the selected game
#Argument 2 = the file name of the game being started without the path and without the extension
#Argument 3 = the full path to the game being started

DEBUG=false

LOGFILE="/rcade/share/userscripts/game-selected/marquee-selected-debug.log"
if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi
echo "===========================================" >> $LOGFILE
echo "Script called at: $(date)" >> $LOGFILE
echo "Number of arguments: $#" >> $LOGFILE
echo "Argument 1 (syste,): $1" >> $LOGFILE
echo "Argument 2 (filename): $2" >> $LOGFILE
echo "Argument 3 (full path): $3" >> $LOGFILE
echo "Argument 4 (empty): $4" >> $LOGFILE
echo "All arguments: $@" >> $LOGFILE

if [ -z "${3}" ]; then
  echo "Argument 3 is empty, exiting" >> $LOGFILE
  exit 0
fi

# If system argument is provided, use it; otherwise extract from path
if [ -n "${1}" ]; then
  system="${1}"
else
  # Extract system from path: /rcade/share/roms/SYSTEM/game.zip
  # Get the directory name from the full path
  rom_dir=$(dirname "${3}")
  system=$(basename "$rom_dir")
  echo "System not provided, extracted from path: $system" >> $LOGFILE
fi

# Gets the basename of the game
game=$(basename "${2}")
game=${game%.*}

echo "Processed system: $system" >> $LOGFILE
echo "Processed game: $game" >> $LOGFILE
echo "Sending command: OPEN $system $game" >> $LOGFILE

# Send game info to picture server
python3 /rcade/share/userscripts/simpleClient.py "SELECTED $system $game" >> $LOGFILE 2>&1

echo "Script completed" >> $LOGFILE