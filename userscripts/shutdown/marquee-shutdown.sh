
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/shutdown/marquee-shutdown-debug.log"
rm -f "$LOGFILE"
touch &LOGFILE
echo "Initiating arcade shutdown sequence..." >> $LOGFILE

# Send shutdown command to marquee display
echo "Sending shutdown to marquee display..." >> $LOGFILE
python3 /rcade/share/userscripts/simpleClient.py "SHUTDOWN"


echo "Shutdown sequence complete">> $LOGFILE
