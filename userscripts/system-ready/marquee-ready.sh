#!/bin/bash

#Set to true to persist log file 

DEBUG=false

LOGFILE="/rcade/share/userscripts/system-ready/marquee-ready-debug.log"

if [ "$DEBUG" != "true" ]; then
  rm -f "$LOGFILE"
fi

echo "Script called at: $(python3 -c 'from datetime import datetime; print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])')" >> $LOGFILE

# Write startup timestamp so daemon knows to ignore early commands
echo "$(date +%s%3N)" > /tmp/marquee-startup-time

# Start the daemon if not already running
if [ ! -f /tmp/marquee-daemon.pid ] || ! kill -0 $(cat /tmp/marquee-daemon.pid) 2>/dev/null; then
    echo "Starting marquee daemon..." >> $LOGFILE
    python3 /rcade/share/userscripts/marquee-daemon.py &
    echo $! > /tmp/marquee-daemon.pid
    sleep 1
    echo "Daemon started with PID $(cat /tmp/marquee-daemon.pid)" >> $LOGFILE
else
    echo "Daemon already running" >> $LOGFILE
fi

echo "Script completed" >> $LOGFILE