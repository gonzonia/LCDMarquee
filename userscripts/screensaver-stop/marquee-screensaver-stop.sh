
#!/bin/bash

# DEBUG: Log all arguments to a file

#Set to true to persist log file 
DEBUG=false

LOGFILE="/rcade/share/userscripts/screensaver-stop/marquee-screensaver-stop-debug.log"
if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi
touch &LOGFILE


echo "Stopping marquee screensaver..." >> $LOGFILE

# Send screensaver stop command to marquee display
echo "Sending screensaver stop command to marquee display..." >> $LOGFILE

echo "SCREENSAVER-STOP" > /tmp/marquee-daemon.pipe

echo "Screensaver stop complete">> $LOGFILE
