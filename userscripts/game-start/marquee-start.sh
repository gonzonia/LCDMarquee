#!/bin/bash

# ARGUMENTS, IN ORDER:
#Argument 1 = the full path to the game being started
#Argument 2 = the file name of the game being started without the path and without the extension
#Argument 3 = the name of the game being started
#Argument 4 = the name of the system for the game being started (may be empty)

# DEBUG: Log all arguments to a file

#Set to true to persist log file 
DEBUG=false

LOGFILE="/rcade/share/userscripts/game-start/marquee-start-debug.log"

if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi

#LOGFILE= "/dev/null"
echo "===========================================" >> $LOGFILE
echo "Script called at: $(date)" >> $LOGFILE
echo "Number of arguments: $#" >> $LOGFILE
echo "Argument 1 (full path): $1" >> $LOGFILE
echo "Argument 2 (filename): $2" >> $LOGFILE
echo "Argument 3 (game name): $3" >> $LOGFILE
echo "Argument 4 (system): $4" >> $LOGFILE
echo "All arguments: $@" >> $LOGFILE

if [ -z "${3}" ]; then
  echo "Argument 3 is empty, exiting" >> $LOGFILE
  exit 0
fi

# If system argument is provided, use it; otherwise extract from path
if [ -n "${4}" ]; then
  system="${4}"
else
  # Extract system from path: /rcade/share/roms/SYSTEM/game.zip
  # Get the directory name from the full path
  rom_dir=$(dirname "${1}")
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
echo "OPEN $system $game" > /tmp/marquee-daemon.pipe

echo "Script completed" >> $LOGFILE
