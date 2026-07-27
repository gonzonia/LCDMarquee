
#!/bin/bash

# DEBUG: Log all arguments to a file
#Set to true to persist log file 
DEBUG=false


LOGFILE="/rcade/share/userscripts/shutdown/marquee-shutdown-debug.log"
if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi
touch &LOGFILE

echo "Initiating arcade shutdown sequence..." >> $LOGFILE

# Send shutdown command to marquee display
echo "Sending shutdown to marquee display..." >> $LOGFILE

echo "SHUTDOWN" > /tmp/marquee-daemon.pipe


echo "Shutdown sequence complete">> $LOGFILE
