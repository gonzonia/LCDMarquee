import socket
import sys
import logging

# Configure logging to show INFO level and above
logging.basicConfig(
    filename="/rcade/share/userscripts/simpleClient.log",
    filemode="w",  # Overwrites the file each time; use 'a' to append
    level=logging.WARNING,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

host = '<IP OF HOST>'
port = 5561

def setupSocket():
    logging.info("Setup Socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def sendReceive(s, message):
    logging.info("SendRecieve")
    s.send(str.encode(message))
    reply = s.recv(1024)
    logging.info("received a reply")
   # print("We have received a reply")
    logging.info("Sending Close")
    s.send(str.encode("EXIT"))
    logging.info("Closing")
    s.close()
    reply = reply.decode('utf-8')
    logging.info("Return Reply")
    return reply

def transmit(message):
    logging.info("Transmit")
    s = setupSocket()
    response = sendReceive(s, message)
    logging.info("Return Response")
    return response

#print("This is the name of the script: " + sys.argv[0])
#print("Number of arguments: " + str(len(sys.argv)))
#print("The arguments are: " + str(sys.argv))
command = str(sys.argv[1])
#print("Sending command to server: " + command)
try:
    logging.info("Sending command to server: ", command)
    response = transmit(command)
except KeyboardInterrupt:
    print("Ctrl-C")

#print("Response: " + response )
