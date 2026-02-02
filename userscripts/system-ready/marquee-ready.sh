
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/system-ready/marquee-ready-debug.log"
rm -f "$LOGFILE"


echo "Sending command: OPEN all emulation_station" >> $LOGFILE

python3 /rcade/share/userscripts/simpleClient.py "OPEN all emulation_station"  >> $LOGFILE 2>&1

echo "Script completed" >> $LOGFILE
