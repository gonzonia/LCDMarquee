#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/game-end/marquee-end-debug.log"
rm -f "$LOGFILE"

touch $LOGFILE

echo "Sending command: CLOSE" >> $LOGFILE

python3 /rcade/share/userscripts/simpleClient.py "CLOSE"  >> $LOGFILE 2>&1
#echo "Sending command: OPEN all emulation_station" >> $LOGFILE

#python3 /rcade/share/userscripts/simpleClient.py "OPEN all emulation_station"  >> $LOGFILE 2>&1

echo "Script completed" >> $LOGFILE
