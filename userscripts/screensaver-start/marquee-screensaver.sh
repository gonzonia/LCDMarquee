
#!/bin/bash

# DEBUG: Log all arguments to a file
#Set to true to persist log file 
DEBUG=false

LOGFILE="/rcade/share/userscripts/screensaver-start/marquee-screensaver-start-debug.log"

if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi

touch &LOGFILE
echo "Initiating marquee screensaver..." >> $LOGFILE

# Send Screensaver Start command to marquee display
echo "Sending SCREENSAVER-START to marquee display..." >> $LOGFILE

echo "SCREENSAVER-START" > /tmp/marquee-daemon.pipe

echo "SCREENSAVER-START sequence complete">> $LOGFILE
