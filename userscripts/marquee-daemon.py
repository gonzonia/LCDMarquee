#!/usr/bin/env python3
import socket
import os
import sys
import time
import logging
import threading

# Config
SERVER_HOST = '192.168.99.10'
SERVER_PORT = 5561
PIPE_PATH = '/tmp/marquee-daemon.pipe'
STARTUP_IGNORE_MS = 4000  # Ignore SELECTED for 3 seconds after startup

logging.basicConfig(
    filename="/rcade/share/userscripts/marquee-daemon.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class MarqueeDaemon:
    def __init__(self):
        logging.info("Starting init")
        self.sock = None
        self.lock = threading.Lock()
        self.connect()

    def connect(self):
        """Establish connection to marquee server"""
        logging.info("Connecting")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((SERVER_HOST, SERVER_PORT))
            logging.info("Connected to marquee server")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            self.sock = None

    def send_command(self, command):
        """Send command to server, reconnect if needed"""
        with self.lock:
            for attempt in range(2):
                try:
                    if self.sock is None:
                        self.connect()
                    if self.sock is None:
                        return "ERROR: Not connected"
                    
                    self.sock.send(str.encode(command))
                    reply = self.sock.recv(1024).decode('utf-8')
                    logging.info(f"Sent: {command} | Reply: {reply}")
                    return reply
                except Exception as e:
                    logging.warning(f"Send failed (attempt {attempt+1}): {e}")
                    self.sock = None
                    time.sleep(0.1)
            return "ERROR: Failed to send"
            
    def run(self):
        """Listen for commands on named pipe"""
        # Remove old pipe if exists
        if os.path.exists(PIPE_PATH):
            os.unlink(PIPE_PATH)
        
        os.mkfifo(PIPE_PATH)
        os.chmod(PIPE_PATH, 0o777)
        logging.info(f"Listening on pipe: {PIPE_PATH}")
        
        while True:
            try:
                # Open pipe - blocks until writer connects
                with open(PIPE_PATH, 'r') as pipe:
                    for line in pipe:
                        command = line.strip()
                        if command:
                            # Ignore SELECTED during startup window
                            if command.startswith('SELECTED') and self.is_startup_window():
                                logging.info(f"Ignoring SELECTED during startup window: {command}")
                                continue
                            
                            logging.info(f"Received command: {command}")
                            reply = self.send_command(command)
                            logging.info(f"Reply: {reply}")
            except Exception as e:
                logging.error(f"Pipe error: {e}")
                time.sleep(0.1)

    def is_startup_window(self):
        """Check if we're still in the startup ignore window"""
        try:
            with open('/tmp/marquee-startup-time', 'r') as f:
                start_time = int(f.read().strip())
            current_time = int(time.time() * 1000)
            elapsed = current_time - start_time
            return elapsed < STARTUP_IGNORE_MS
        except:
            return False             

if __name__ == '__main__':
    daemon = MarqueeDaemon()
    daemon.run()