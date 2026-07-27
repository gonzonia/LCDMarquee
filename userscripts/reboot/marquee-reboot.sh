
#!/bin/bash

# DEBUG: Log all arguments to a file
#Set to true to persist log file 
DEBUG=false

LOGFILE="/rcade/share/userscripts/reboot/marquee-reboot-debug.log"

if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi
touch &LOGFILE
echo "Initiating arcade reboot sequence..." >> $LOGFILE

# Notify Home Assistant
#echo "Notifying Home Assistant..." >> $LOGFILE
#python3 /rcade/share/userscripts/ha-shutdown.py shutdown

# Send shutdown command to marquee display
echo "Sending shutdown to marquee display..." >> $LOGFILE

echo "REBOOT" > /tmp/marquee-daemon.pipe

echo "Rebooting sequence complete">> $LOGFILE
