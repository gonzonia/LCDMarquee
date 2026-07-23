
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/screensaver-start/marquee-screensaver-start-debug.log"
rm -f "$LOGFILE"
touch &LOGFILE
echo "Initiating marquee screensaver..." >> $LOGFILE

# Notify Home Assistant
#echo "Notifying Home Assistant..." >> $LOGFILE
#python3 /rcade/share/userscripts/ha-shutdown.py shutdown

# Send shutdown command to marquee display
echo "Sending SCREENSAVER-START to marquee display..." >> $LOGFILE
python3 /rcade/share/userscripts/simpleClient.py "SCREENSAVER-START"

echo "SCREENSAVER-START sequence complete">> $LOGFILE
