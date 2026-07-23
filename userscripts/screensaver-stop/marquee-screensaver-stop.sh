
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/screensaver-stop/marquee-screensaver-stop-debug.log"
rm -f "$LOGFILE"
touch &LOGFILE
echo "Stopping marquee screensaver..." >> $LOGFILE

# Notify Home Assistant
#echo "Notifying Home Assistant..." >> $LOGFILE
#python3 /rcade/share/userscripts/ha-shutdown.py shutdown

# Send shutdown command to marquee display
echo "Sending screensaver stop command to marquee display..." >> $LOGFILE
python3 /rcade/share/userscripts/simpleClient.py "SCREENSAVER-STOP"

echo "Screensaver stop complete">> $LOGFILE
