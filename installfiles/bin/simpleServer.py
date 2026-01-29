#===================================================================================================
# Title: LCD Marquee Controller Program
# Program Name: simpleServer.py
# Purpose: This program will wait for information to be passed from another script on a RPi running RetroPie.
#          When information is passed, it will change the image on the display to match the name of the game
#          that was selected in RetroPie.
# NOTE: This original program was provided by user Texacate and other in the RetroPie community for use to create a 
#       screen shot of the control panel button layout. I have altered the code to be used as a LCD Marquee controller.
#       The original code is located in the same folder as this program and is called simpleServer.ORIGINAL, if you 
#       wish to reference the orginal code.
#       For more inforamtion on origial project, you can goto the original forum post below:
#       https://retropie.org.uk/forum/topic/21464/show-control-panel-layout-before-game-starts-in-retropie-just-like-arcade1up-does/76?_=1581179183756
#       For the original code and files other than simpleServer.py, you can visit Texacate GitHub site below:
#       https://github.com/Texacate/Visual-RetroPie-Control-Maps
# Version: 2.01 (Current Version)- Added line in setupServer function that stops the SplashScreen service.
#          2.0 - Added support to play default video or default image in /home/pi/marquees folder.
#              - Services are now used to display images and videos. MarqueeImage service is used to display image (using FIM) and MarqueeVideo service is used to play video 
#                (omxplayer). These two services MUST be added for the program to function properly.
#              - FBI is no longer used to display images on the screen. The program FIM is used in its place, as FBI would not work when running as a service.
#              - Code has been added to function setupServer os default video or image that is in the /home/pi/marquees folder will display or play automatically on when service is started.
#                If /home/pi/marquees/default.mp4 exists, then default.mp4 video will play. If /home/pi/marquees/default.mp4 does not exists and 
#                /home/pi/marquees/default.png exists, then default.png image will be displayed.
#              - Added support to play video or default image in /home/pi/marquees/system folder. This operates exactly like the default video and image 
#                for /home/pi/marquees, except in /home/pi/marquees/system.
#              - Added new function openVideo to handle starting video.
#              - Added additional code to function dataTransfer OPEN section to start function openVideo if file ends with MP4 or start function openImage
#                if file ends with PNG.
#          1.1 - Fixed issue with image files with spaces in name not displaying.
#          1.0 - Initial Version
#=====================================================================================================

# Import the modules to be used in the program.
import os
import socket
import subprocess
import time

# Set univeral variables that will be used throughout the program:
# host - Host name or IP address for the host. This is not used and can remain blank.
# port - Port to use for the server connection.
# image_dir - Location to marquee image files
# image_type - The extension used for the image files.
# video_type - The extension used for the video files.
host = ''
port = 5561
image_dir  = "/home/pi/marquees"
image_types = [".png", ".jpg", ".jpeg", ".gif"]  # List of image extensions to try
video_types = [".mp4", ".avi", ".mkv"]   # List of video extensions to try

def setupServer():
    #=================================================================================================
    # Function name: setupServer
    # Purpose: To setup socket connection
    # Accepts: path - The path were the new image file to be displayed is located at.
    # Result:  The image file on the display is changed.
    #=================================================================================================

    # set socket and print on screen that socket was created.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")

    # Try and bind the socket. If there is an error, display error message, otherwise display that socket
    # bind was complete
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")

    #Set paths to the default image and video. Also set command to run video or image to nothing.
    initvideo = image_dir + "/default" + video_types[0]
    initimage = image_dir + "/default" + image_types[0]
    initcmd = "nothing"

    # Delete the video arguments file, if it exists, and then create a new one with the Video path
    # pointing to /home/pi/marquees/default.mp4.
    if os.path.exists("/home/pi/bin/videoarg.txt"):
        os.remove("/home/pi/bin/videoarg.txt")
    vidnewfile=open("/home/pi/bin/videoarg.txt","w+")
    vidnewfile.write("Video=" + initvideo + "\n")
    vidnewfile.close

    # Set full permissiones to the video arguments file.
    proc = os.system("sudo chmod 777 /home/pi/bin/videoarg.txt")

    # Delete the image arguments file, if it exists, and then create a new one with the Image path
    # pointing to /home/pi/marquees/default.png.
    if os.path.exists("/home/pi/bin/imagearg.txt"):
        os.remove("/home/pi/bin/imagearg.txt")
    imgnewfile=open("/home/pi/bin/imagearg.txt","w+")
    imgnewfile.write("Image=" + initimage + "\n")
    imgnewfile.close()

    # Set full permissiones to the image arguments file.
    proc = os.system("sudo chmod 777 /home/pi/bin/imagearg.txt")

    # If the file /home/pi/marquees/default.mp4 exists, then set the initcmd variable to
    # start the MarqueeVideo service.
    if (os.path.isfile(initvideo)):
        initcmd = "sudo systemctl start MarqueeVideo"
    
    # If the file /home/pi/marquees/default.png exists, then set the initcmd variable to
    # start the MarqueeVideo service.
    if not (os.path.isfile(initvideo)):
        initcmd = "sudo systemctl start MarqueeImage"

    #If initcmd variable has video or image command, run it.
    #Will pause for 2 seconds so that the command prompt
    #does not overwrite the image.
    if initcmd != 'nothing':
        os.system("sudo systemctl stop SplashScreen")
        time.sleep(2)
        proc = os.system(initcmd)

    # Return the result
    return s

def setupConnection():
    #=================================================================================================
    # Function name: setupConnection
    # Purpose: Allows connection to the server.
    # Result:  Allows connection to the server.
    #=================================================================================================
    # Listen on the connection and then print to screen where the connection came from.
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connection from: " + address[0] + ":" + str(address[1]))

    # Return connection
    return conn

def pathBuilder(sysrom):
    print("pathBuilder(" + sysrom + ")")

    args = sysrom.split(' ', 1)
    sys = args[0]
    rom = args[1]

    # 1. Look for game-specific image (try all image types)
    path = None
    for ext in image_types:
        test_path = image_dir + "/" + sys + "/" + rom + ext
        if os.path.isfile(test_path):
            path = test_path
            break
    
    # 2. If not found, look for system default image
    if not path:
        for ext in image_types:
            test_path = image_dir + "/" + sys + "/default" + ext
            if os.path.isfile(test_path):
                path = test_path
                break
    
    # 3. If no system default image, look for system default video
    if not path:
        for ext in video_types:
            test_path = image_dir + "/" + sys + "/default" + ext
            if os.path.isfile(test_path):
                path = test_path
                break
   
    # 4. If no system files, use generic default image
    if not path:
        for ext in image_types:
            test_path = image_dir + "/default" + ext
            if os.path.isfile(test_path):
                path = test_path
                break
   
    # 5. Only if no default image exists, use default video
    if not path:
        for ext in video_types:
            test_path = image_dir + "/default" + ext
            if os.path.isfile(test_path):
                path = test_path
                break
  
    # 6. If nothing exists, show error
    if not path:
       path = "Video or Image not found."
    
    print("Built: "+ path)
    return path
    
    
def openImage(path):
    #=================================================================================================
    # Function name: openImage
    # Purpose: To change the image file that is displayed when a new game is selected.
    # Accepts: path - The path were the new image file to be displayed is located at.
    # Result:  The image file on the display is changed.
    #=================================================================================================
    # Print on screen what function is being run and image that will be loaded.
    print("openImage (" + path + ")")

    # Store the status of the MarqueeImage service in a variable
    imgservicerun = os.system("sudo systemctl is-active MarqueeImage")

    # Check if image enviornoment file exists, image environement file is used for the MarqueeImage service
    # and contains the path to the image file to load. If the image environment file exists, store the previous 
    # image path into a variable and then delete and rebuild with the new path to the image file 
    if os.path.exists("/home/pi/bin/imagearg.txt"):
       existfile=open("/home/pi/bin/imagearg.txt","r")
       existline=(existfile.readline())
       existfile.close
       os.remove("/home/pi/bin/imagearg.txt")
       currentpath=existline.split("=", 1)    
    newfile=open("/home/pi/bin/imagearg.txt","w+")
    newfile.write("Image=" + path + "\n")
    newfile.close()

    time.sleep(0.5)

    # Set rights to image environment file so everyone has access to it.
    proc = os.system("sudo chmod 777 /home/pi/bin/imagearg.txt")

    # Set command to stop and start the MarqueeImage service and stop the MarqueeVideo service to unload and load the image.
    cmdimagestop = "sudo systemctl stop MarqueeImage"
    cmdimagestart = "sudo systemctl start MarqueeImage"
    cmdvideostop = "sudo systemctl stop MarqueeVideo"

    # Print on screen MarqueeVideo service is going to be stopped and the stop the service.
    print("cmdvideostop(" + cmdvideostop + ")")
    proc = os.system(cmdvideostop)
    
    # If the current path and the new path are not the same OR the MarqueeImage service is not running,
    # then stop and start the MarqueeImage service.
    if True:
       
    # Print on screen MarqueeImage service is going to be stopped and then stop the service.
       print("cmdimagestop(" + cmdimagestop + ")")
       proc = os.system(cmdimagestop)

    # Print on screen MarqueeImage service is going to be started and then start the service.
       print("cmdimagestart(" + cmdimagestart + ")")
       proc = os.system(cmdimagestart)

    # Return error code for MarqueeImage service.
       return proc

def openVideo(path):
    #=================================================================================================
    # Function name: openVideo
    # Purpose: To change the video that is played when a new system is selected.
    # Accepts: path - The path were the new video file to be played is located at.
    # Result:  The video file playing is changed.
    #=================================================================================================
    # Print on screen what function is being run and image that will be loaded.
    print("openVideo (" + path + ")")

    vidservicerun = os.system("sudo systemctl is-active MarqueeVideo")

    # Check if video enviornoment file exists, video environement file is used for the MarqueeVideo service
    # and contains the path to the video file to load. If the video environment file exists, store the previous 
    # video path into a variable and then delete and rebuild with the new path to the video file 
    if os.path.exists("/home/pi/bin/videoarg.txt"):
       existfile=open("/home/pi/bin/videoarg.txt","r")
       existline=(existfile.readline())
       existfile.close
       os.remove("/home/pi/bin/videoarg.txt")
       currentpath=existline.split("=", 1)   
    newfile=open("/home/pi/bin/videoarg.txt","w+")
    newfile.write("Video=" + path)
    newfile.close

    # Set rights to video environment file so everyone has access to it.
    proc = os.system("sudo chmod 777 /home/pi/bin/videoarg.txt")

    # Set command to stop and start the MarqueeImage service and stop the MarqueeVideo service to unload and load the image.
    cmdimagestop = "sudo systemctl stop MarqueeImage"
    cmdvideostart = "sudo systemctl start MarqueeVideo"
    cmdvideostop = "sudo systemctl stop MarqueeVideo"

    # Print on screen MarqueeImage service is going to be stopped and the stop the service.
    print("cmdimagestop(" + cmdimagestop + ")")
    proc = os.system(cmdimagestop)
    
    # If the current path and the new path are not the same OR the MarqueeVideo service is not running,
    # then stop and start the MarqueeImage service.
    if path != currentpath[1].strip() or vidservicerun != 0:
      
    # Print on screen MarqueeVideo service is going to be stopped and the stop the service.
       print("cmdvideostop(" + cmdvideostop + ")")
       proc = os.system(cmdvideostop)

    # Print on screen MarqueeVideo service is going to be stopped and the stop the service.
       print("cmdvideostart(" + cmdvideostart + ")")
       proc = os.system(cmdvideostart)

    # Return error code for MarqueeImage service.
       return proc


def closeImage():
    #=================================================================================================
    # Function name: closeImage
    # Purpose: To close any image that is running.
    # Result:  The image file playing is stopped.
    #=================================================================================================
    # Print on screen what function is being run and image that will be loaded.
    print("closeImage()")

    # Set command to stop MarqueeImage service.
    cmdimagestop = "sudo systemctl stop MarqueeImage"

    # Print on screen MarqueeImage service is going to be stopped and the stop the service.
    print("cmdimagestop(" + cmdimagestop + ")")
    proc = os.system(cmdimagestop)

    # Set return variable that function is done and return the value.
    out = "Done"
    return out

def closeVideo():
    #=================================================================================================
    # Function name: closeVideo
    # Purpose: To close any video that is running.
    # Result:  The video file playing is stopped.
    #=================================================================================================
    # Print on screen what function is being run and image that will be loaded.
    print("closeVideo()")

    # Set command to stop MarqueeImage and MarqueeVideo service.
    cmdvideostop = "sudo systemctl stop MarqueeVideo"
    
    # Print on screen MarqueeVideo service is going to be stopped and the stop the service.
    print("cmdvideostop(" + cmdvideostop + ")")
    proc = os.system(cmdvideostop)

    # Set return variable that function is done and return the value.
    out = "Done"
    return out

def GET():
    #print("Command: GET")
    reply = storedValue
    return reply

def REPEAT(dataMessage):
    #print("Command : REPEAT " + dataMessage[1])
    reply = dataMessage[1]
    return reply

def dataTransfer(conn):
    #=================================================================================================
    # Function name: dataTransfer
    # Purpose: Will run a command depending on what was sent from the client.
    # Accepts: conn - Info received from the client. Data is separated by spaces and will be split:
    #          First part is the command to perform
    #          Second part is the system being used
    #          Third part is the rom being run.
    #=================================================================================================
    # A big loop that sends/receives data until told not to
    while True:

    # Receive the data
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')

    # Split the data such that you separate the command
    # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]

    # If the command sent from the client is GET, then print the command on screen and run
    # the GET function.
        if command == 'GET':
            print("Command: GET")
            reply = GET()

    # If the command sent is PATH, then print the command on screen and run the pathBuilder function
    # to build the path to the video or image.
        elif command == 'PATH':
            print("Command: PATH" +  " / Data: " + dataMessage[1])
            reply = pathBuilder(dataMessage[1])

    # If the command sent is OPEN, then print the command on screen run openVideo or openImage function depending
    # on if the path to file has an extension .mp4 or .png.
        elif command == 'OPEN':
            print("Command: OPEN" +  " / Data: " + dataMessage[1])

        # Get the path to the image or video by running the pathBuilder function.
            path = pathBuilder(dataMessage[1])

        # Get the last the characters of the path. This should be the extention of the video or image file. Print
        # the results on the screen.
            path_file_ext = path[-3:]
            print("Path = " + path)
            print("Extention = " + path_file_ext)

        # If the extension ends with mp4, then run the openVideo function to play the video, else run the openImage
        # function to display the image.
            if path_file_ext == 'mp4':
                proc = openVideo(path)
                reply = "Opened Video: " + path
            else:
                proc = openImage(path)
                reply = "Opened Image: " + path

    # If the command sent is CLOSE, the print the command on the screen and run the closeImage and closeVideo function.
        elif command == 'CLOSE':
            print("Command: CLOSE")
            #closeImage()
            #closeVideo()
            reply = "Closed Image"

    # If the command sent is REPEAT, then print the command on the screen and run the REPEAT function.
        elif command == 'REPEAT':
            print("Command: REPEAT" +  " / Data: " + dataMessage[1])
            reply = REPEAT(dataMessage)

    # If the command sent is EXIT, then print the command on the screen and end the loop.
        elif command == 'EXIT':
            print("Command: EXIT")
            print("Our client has left us")
            break

    # If the command sent is KILL, then print the command on the screen and close the program.
        elif command == 'KILL':
            print("Command: KILL")
            print("Our server is shutting down.")
            s.close()
            break
    # If the command sent is SHUTDOWN, shutdown the system
        elif command == 'SHUTDOWN':
            print("Command: SHUTDOWN")
            print("Shutting down the system...")
            reply = "System shutdown initiated"
            conn.sendall(str.encode(reply))
            conn.close()
            time.sleep(1)  # Give time for reply to be sent
            os.system("sudo shutdown -h now")
            break        

    # If the command cannot be found, then print the command could not be found set the reply variable to unknown command
        else:
            print("Unknown command: " + command)
            reply = 'Unknown command. Valid commands are GET, REPEAT <string>, EXIT, KILL, SHUTDOWN'

    # Send the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")

    # Close the connection
    conn.close()

# Run the setupServer function.
s = setupServer()

# While the server program is running, keep the connection open and keep checking for data being received from the client.
while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break

