#!/bin/bash
echo "Script called at: $(date)" >> $LOGFILE

# DEBUG: Log all arguments to a file
#Set to true to persist log file 
DEBUG=false
LOGFILE="/rcade/share/userscripts/game-end/marquee-end-debug.log"


if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi
touch $LOGFILE

echo "Sending command: CLOSE" >> $LOGFILE

echo "CLOSE" > /tmp/marquee-daemon.pipe


echo "Script completed" >> $LOGFILE
