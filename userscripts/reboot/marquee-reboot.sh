
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/reboot/marquee-reboot-debug.log"
rm -f "$LOGFILE"
touch &LOGFILE
echo "Initiating arcade reboot sequence..." >> $LOGFILE

# Notify Home Assistant
#echo "Notifying Home Assistant..." >> $LOGFILE
#python3 /rcade/share/userscripts/ha-shutdown.py shutdown

# Send shutdown command to marquee display
echo "Sending shutdown to marquee display..." >> $LOGFILE
python3 /rcade/share/userscripts/simpleClient.py "REBOOT"

echo "Rebooting sequence complete">> $LOGFILE
