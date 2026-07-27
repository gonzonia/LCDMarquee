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
#
# Gonzonia- 
# Version  5.0  I'm jumping a version here because I've had to split Image and Video into seperate services for both screens to prevent memory issues that were showing up on boot and still allow for the swap from video to image and back. 
# Version  4.2  Catch only single argument passed for changes to use daemon on client side
# Version  4.1  Added per-screen default file resolution (default_control/default_marquee priority chains).
# Version  4.0  Changed to work with Wayland when using a desktop version of PiOS.
# Version  3.1 (current)  Added control map images
# Version  3.0   Fixed for trixie. Switched to fim and mpv
# Version: 2.01  Added line in setupServer function that stops the SplashScreen service.
#          2.0 - Added support to play default video or default image in /home/pi/marquees folder.
#              - Services are now used to display images and videos. MarqueeImage service is used to display image (using FIM) and MarqueeVideo service is used to play video 
#                (omxplayer). These two services MUST be added for the program to function properly.
#              - FBI is no longer used to display images on the screen. The program FIM is used in its place, as FBI would not work when running as a service.
#              - Code has been added to function setupServer os default video or image that is in the /home/pi/marquees folder will display or play automatically on when service is started.
#                If /home/pi/marquees/default.mp4 exists, then default.mp4 video will play. If /home/pi/marquees/default.mp4 does not exists and 
#                /home/pi/marquees/default.png exists, then the default.png image will be displayed.
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
import threading
from datetime import datetime

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
            
# Global flag to control the clock thread
clock_running = False

def resolveDefaultControl():
    """Return the best available default file for the Waveshare/control screen.
    Priority: default_control.mp4 -> default.mp4 -> default_control.png -> default.png"""
    candidates = [
        image_dir + "/default_rotated.mp4",
        image_dir + "/default.mp4",
        image_dir + "/default_control.png",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None

def resolveDefaultMarquee():
    """Return the best available default file for the BitLCD/marquee screen.
    Priority: default_marquee.mp4 -> default_marquee.png -> default.png"""
    candidates = [
        image_dir + "/default_marquee.mp4",
        image_dir + "/default_marquee.png",
        image_dir + "/default.png",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None

def restoreDefaults():
    """Restore both screens to their best available default file."""
    control_path = resolveDefaultControl()
    if control_path:
        print(f"Restoring control screen: {control_path}")
        if control_path.endswith(tuple(video_types)):
            openVideo(control_path)
        else:
            openImage(control_path)
    else:
        print("No default file found for control screen.")

    marquee_path = resolveDefaultMarquee()
    if marquee_path:
        print(f"Restoring marquee screen: {marquee_path}")
        showOnBitLCD(marquee_path)
    else:
        print("No default file found for marquee screen.")

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
    
    # Stop all display services on startup
    os.system("sudo systemctl stop MarqueeImage")
    os.system("sudo systemctl stop MarqueeVideo")
    os.system("sudo systemctl stop MarqueeBitLCD")
    os.system("sudo systemctl stop MarqueeBitLCDImage")

    # Resolve best default files for each screen independently
    control_path = resolveDefaultControl()
    marquee_path = resolveDefaultMarquee()

    # Resolve best default files for each screen independently
    control_path = resolveDefaultControl()
    marquee_path = resolveDefaultMarquee()

    # Write arg files with resolved paths (fall back to legacy defaults if nothing found)
    videoarg_path = control_path if control_path and control_path.endswith(tuple(video_types)) else image_dir + "/default_rotated.mp4"
    imagearg_path = control_path if control_path and not control_path.endswith(tuple(video_types)) else image_dir + "/default.png"
    marqueearg_path = control_path if control_path and control_path.endswith(tuple(video_types)) else image_dir + "/default_marquee.mp4"
    marqueeImgarg_path = control_path if control_path and not control_path.endswith(tuple(video_types)) else image_dir + "/default.png"
		
    if os.path.exists("/home/pi/bin/videoarg.txt"):
        os.remove("/home/pi/bin/videoarg.txt")
    vidnewfile = open("/home/pi/bin/videoarg.txt", "w+")
    vidnewfile.write("Video=" + videoarg_path + "\n")
    vidnewfile.close()
    os.system("sudo chmod 777 /home/pi/bin/videoarg.txt")

    if os.path.exists("/home/pi/bin/imagearg.txt"):
        os.remove("/home/pi/bin/imagearg.txt")
    imgnewfile = open("/home/pi/bin/imagearg.txt", "w+")
    imgnewfile.write("Image=" + imagearg_path + "\n")
    imgnewfile.close()
    os.system("sudo chmod 777 /home/pi/bin/imagearg.txt")
    
     # Remove marqueearg.txt so MarqueeBitLCD uses its built-in default
      # Remove marqueearg.txt so MarqueeBitLCD uses its built-in default
    if os.path.exists("/home/pi/bin/marqueearg.txt"):
        os.remove("/home/pi/bin/marqueearg.txt")
     
    if os.path.exists("/home/pi/bin/marqueearg_img.txt"):
        os.remove("/home/pi/bin/marqueearg_img.txt") 
    marqueeimgnewfile = open("/home/pi/bin/marqueearg_img.txt", "w+")
    marqueeimgnewfile.write("Image=" + marqueeImgarg_path + "\n")
    marqueeimgnewfile.close()
    os.system("sudo chmod 777 /home/pi/bin/marqueearg_img.txt")
	
    # Start services if any default files were found
    if control_path or marquee_path:
    	#not used anymore
        #os.system("sudo systemctl stop SplashScreen")
        #time.sleep(2)

        # Start control screen service based on file type
        #Temporarily test nothing on
        if control_path:
            print(f"Starting control screen with: {control_path}")
            #if control_path.endswith(tuple(video_types)):
            print("Starting MarqueeVideo.Service")
            os.system("sudo systemctl start MarqueeVideo")
            time.sleep(2)
            #Start MarqueeImage service for image overlay layer (Waveshare)
            os.system("sudo systemctl start MarqueeImage")
            time.sleep(2)
   
           # Hide the image layer so video shows through
            if control_path and control_path.endswith(tuple(video_types)):
                if os.path.exists("/tmp/mpv-image.sock"):
                    print("Stopping image layer on startup")
                    os.system(f'echo \'{{"command": ["stop"]}}\' | socat - /tmp/mpv-image.sock')

        # Start BitLCD service (it will load its own default via MarqueeBitLCD service)
        if marquee_path:
            print(f"Starting marquee screen with: {marquee_path}")
            os.system("sudo systemctl start MarqueeBitLCD")
            time.sleep(2)
            os.system("sudo systemctl start MarqueeBitLCDImage")
            time.sleep(2)
            
            # Hide the image layer so video shows through
            if marquee_path.endswith(tuple(video_types)):
                if os.path.exists("/tmp/mpv-bitlcd-image.sock"):
                    print("Stopping BitLCD image layer on startup")
                    os.system(f'echo \'{{"command": ["stop"]}}\' | socat - /tmp/mpv-bitlcd-image.sock')            
    
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
    sys = args[0].lower().strip()
    rom = args[1].lower().strip() if len(args) > 1 else ""

    print("system=" + sys)
    print("rom=" + rom)
    
	 # Read current theme
    theme = "default"
    if os.path.exists("/home/pi/bin/theme.txt"):
        with open("/home/pi/bin/theme.txt", "r") as f:
            theme = f.read().strip()
    print("theme=" + theme)
    
    theme_dir =  "/themes/" + theme
    
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
   
   	# 4. If not system default, check for a top-level system theme image
    if not path:
        for ext in image_types:
            test_path = image_dir + theme_dir + "/" + sys + ext
            if os.path.isfile(test_path):
                path = test_path
                break   	
                
   	# 5. If not system default, check for a top-level system theme video
    if not path:
        for ext in video_types:
            test_path = image_dir + theme_dir + "/" + sys + ext
            if os.path.isfile(test_path):
                path = test_path
                break   	              
   	
    # 6. If no system files, use generic default image
    if not path:
        for ext in image_types:
            test_path = image_dir + "/default" + ext
            if os.path.isfile(test_path):
                path = test_path
                break
   
    # 7. Only if no default image exists, use default video
    if not path:
        for ext in video_types:
            test_path = image_dir + "/default" + ext
            if os.path.isfile(test_path):
                path = test_path
                break
  
    # 8. If nothing exists, show error
    if not path:
       path = "Video or Image not found."
    
    print("Built: "+ path)
    return path
    
    
def openImage(path):
    print("openImage (" + path + ")")

    if os.path.exists("/home/pi/bin/imagearg.txt"):
       existfile=open("/home/pi/bin/imagearg.txt","r")
       existline=(existfile.readline())
       existfile.close
       os.remove("/home/pi/bin/imagearg.txt")
       currentpath=existline.split("=", 1)
    else:
       currentpath = ["Image", ""]

    newfile=open("/home/pi/bin/imagearg.txt","w+")
    newfile.write("Image=" + path + "\n")
    newfile.close()
    os.system("sudo chmod 777 /home/pi/bin/imagearg.txt")

    time.sleep(0.5)

    # Send to image mpv instance (sits on top of video)
    if os.path.exists("/tmp/mpv-image.sock"):
        print(f"Sending image to mpv-image: {path}")
        cmd = f'echo \'{{"command": ["loadfile", "{path}", "replace"]}}\' | socat - /tmp/mpv-image.sock'
        os.system(cmd)
    else:
        print("mpv-image socket not found, restarting MarqueeImage service")
        os.system("sudo systemctl restart MarqueeImage")

    return 0


def openVideo(path):
    print("openVideo (" + path + ")")

    if os.path.exists("/home/pi/bin/videoarg.txt"):
       existfile=open("/home/pi/bin/videoarg.txt","r")
       existline=(existfile.readline())
       existfile.close
       os.remove("/home/pi/bin/videoarg.txt")
       currentpath=existline.split("=", 1)
    else:
       currentpath = ["Video", ""]

    newfile=open("/home/pi/bin/videoarg.txt","w+")
    newfile.write("Video=" + path + "\n")
    newfile.close()
    os.system("sudo chmod 777 /home/pi/bin/videoarg.txt")

    # First hide the image layer
    if os.path.exists("/tmp/mpv-image.sock"):
        print("Stopping image layer")
        cmd = f'echo \'{{"command": ["stop"]}}\' | socat - /tmp/mpv-image.sock'
        os.system(cmd)

    # Send video to video mpv instance
    if os.path.exists("/tmp/mpv-video.sock"):
        print(f"Sending video to mpv-video: {path}")
        cmd = f'echo \'{{"command": ["loadfile", "{path}", "replace"]}}\' | socat - /tmp/mpv-video.sock'
        os.system(cmd)
    else:
        print("mpv-video socket not found, restarting MarqueeVideo service")
        os.system("sudo systemctl restart MarqueeVideo")

    return 0

def showOnBitLCD(path):
    """Send an image or video to the BitLCD marquee display"""
    print(f"showOnBitLCD ({path})")
    
    is_video = path.endswith(tuple(video_types))
    
    if is_video:
        # Hide the image layer so video shows through
        if os.path.exists("/tmp/mpv-bitlcd-image.sock"):
            print("Stopping BitLCD image layer")
            cmd = f'echo \'{{"command": ["stop"]}}\' | socat - /tmp/mpv-bitlcd-image.sock'
            os.system(cmd)

        # Load the video
        if os.path.exists("/tmp/mpv-bitlcd.sock"):
            cmd = f'echo \'{{"command": ["loadfile", "{path}", "replace"]}}\' | socat - /tmp/mpv-bitlcd.sock'
            os.system(cmd)
            print(f"Sent video to BitLCD: {path}")
        else:
            print("BitLCD video mpv socket not found, restarting service...")
            os.system("sudo systemctl restart MarqueeBitLCD")
    else:
        # Load the image (it will automatically pop over the video)
        if os.path.exists("/tmp/mpv-bitlcd-image.sock"):
            cmd = f'echo \'{{"command": ["loadfile", "{path}", "replace"]}}\' | socat - /tmp/mpv-bitlcd-image.sock'
            os.system(cmd)
            print(f"Sent image to BitLCD: {path}")
        else:
            print("BitLCD image mpv socket not found, restarting service...")
            os.system("sudo systemctl restart MarqueeBitLCDImage")


def clock_thread():
    """Background loop that updates the time on the BitLCD every second"""
    while clock_running:
        current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
        
        cmd_vid = f'echo \'{{"command": ["show-text", "{current_time}", 1100]}}\' | socat - /tmp/mpv-bitlcd.sock'
        cmd_img = f'echo \'{{"command": ["show-text", "{current_time}", 1100]}}\' | socat - /tmp/mpv-bitlcd-image.sock'
        
        if os.path.exists("/tmp/mpv-bitlcd.sock"):
            os.system(cmd_vid)
        if os.path.exists("/tmp/mpv-bitlcd-image.sock"):
            os.system(cmd_img)
            
        time.sleep(1)

def showBitLCDClock():
    """Formats the OSD and starts the clock thread"""
    global clock_running
    print("showBitLCDClock()")
    
    # Format OSD for both layers
    for sock in ["/tmp/mpv-bitlcd.sock", "/tmp/mpv-bitlcd-image.sock"]:
        if os.path.exists(sock):
            os.system(f'echo \'{{"command": ["set_property", "osd-align-x", "left"]}}\' | socat - {sock}')
            os.system(f'echo \'{{"command": ["set_property", "osd-align-y", "top"]}}\' | socat - {sock}')
            os.system(f'echo \'{{"command": ["set_property", "osd-font-size", 40]}}\' | socat - {sock}')
        
    if not clock_running:
        clock_running = True
        # Start the thread in the background so it doesn't block the rest of simpleServer.py
        threading.Thread(target=clock_thread, daemon=True).start()

def hideBitLCDClock():
    """Stops the clock thread and clears the screen"""
    global clock_running
    print("hideBitLCDClock()")
    
    clock_running = False # This tells the background thread to stop looping
    
    # Wipe the clock off both screens
    for sock in ["/tmp/mpv-bitlcd.sock", "/tmp/mpv-bitlcd-image.sock"]:
        if os.path.exists(sock):
            cmd = f'echo \'{{"command": ["show-text", ""]}}\' | socat - {sock}'
            os.system(cmd)
                    
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

  # If the command sent is SELECTED, then show the marquee for the selected game
        elif command == 'SELECTED':
            print("Command: SELECTED" +  " / Data: " + dataMessage[1])
            hideBitLCDClock()
            path = pathBuilder(dataMessage[1])
            path_file_ext = path[-3:]
            print("Path = " + path)
            print("Extension = " + path_file_ext)
            # Show marquee on BitLCD
            showOnBitLCD(path)
            
             # Show base control map on Waveshare when browsing
            base_control_map = "/home/pi/control_maps/base_control_map.png"
            if os.path.isfile(base_control_map):
                openImage(base_control_map)
            reply = "Selected: " + path
            
        # If the command sent is OPEN, then generate and show the control mapping for the game
        elif command == 'OPEN':
            print("Command: OPEN" +  " / Data: " + dataMessage[1])

            # Parse the system and rom
            args = dataMessage[1].split(' ', 1)
            sys = args[0]
            rom = args[1]
            
            # Path to the control map generator
            generator_dir = "/home/pi/control_maps"
            generated_map = f"{generator_dir}/arcade/{rom}.png"
            loading_image = f"{generator_dir}/loading.png"

            # Ensure required directories exist
            os.makedirs(f"{generator_dir}/arcade", exist_ok=True)
            os.makedirs(f"{generator_dir}/tmp", exist_ok=True)
            os.system(f"sudo chmod 777 {generator_dir}/arcade {generator_dir}/tmp")

            # Check if control map already exists
            if os.path.isfile(generated_map):
                print(f"Control map already exists, displaying: {generated_map}")
                control_path = generated_map
            else:
                # Show loading screen while generating
                print("Displaying loading screen...")
                if os.path.isfile(loading_image):
                    openImage(loading_image)
                
                print(f"Generating control map for {rom}")
                
                try:
                    print(f"Running: {generator_dir}/button_map.sh {rom}")
                    print(f"Working directory: {generator_dir}")
                    
                    result = subprocess.run(
                        [f"{generator_dir}/button_map.sh", rom],
                        cwd=generator_dir,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    print(f"Return code: {result.returncode}")
                    print(f"Generator output: {result.stdout}")
                    if result.stderr:
                        print(f"Generator errors: {result.stderr}")
                    
                    if os.path.isfile(generated_map):
                        print(f"Control map generated successfully: {generated_map}")
                        control_path = generated_map
                    else:
                        print(f"Control map generation failed, falling back to marquee")
                        control_path = pathBuilder(dataMessage[1])
                        
                except subprocess.TimeoutExpired:
                    print("Control map generation timed out, falling back to marquee")
                    control_path = pathBuilder(dataMessage[1])
                except Exception as e:
                    print(f"Error generating control map: {e}")
                    control_path = pathBuilder(dataMessage[1])
            
            print("Control map path = " + control_path)
            proc = openImage(control_path)
            reply = "Opened Control Map: " + control_path

    # If the command sent is CLOSE, the print the command on the screen and run the closeImage and closeVideo function.
        elif command == 'CLOSE':
            print("Command: CLOSE")
            hideBitLCDClock()
            restoreDefaults()
            reply = "Closed - returned to default state"

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
    # If the command sent is REBOOT, reboot the system
        elif command == 'REBOOT':
            print("Command: REBOOT")
            print("Rebooting the system...")
            reply = "System reboot initiated"
            conn.sendall(str.encode(reply))
            conn.close()
            time.sleep(1)  # Give time for reply to be sent
            os.system("sudo reboot")
            break                     
        elif command == 'SCREENSAVER-START':
            print("Command: SCREENSAVER-START")
            screensaver_control_path = image_dir + "/screensaver_control.mp4"
            screensaver_marquee_path = image_dir + "/screensaver_marquee.mp4"
            
            if os.path.isfile(screensaver_marquee_path) and os.path.isfile(screensaver_control_path):
                print(f"Starting screensavers: {screensaver_marquee_path}, {screensaver_control_path}")
                showOnBitLCD(screensaver_marquee_path)
                openVideo(screensaver_control_path)
                
                time.sleep(0.5) # Give mpv a half-second to load the video
                showBitLCDClock() 

                
                reply = "Screensavers started: " + screensaver_marquee_path + "," + screensaver_control_path
            else:
                print(f"One of the screensaver files not found: {screensaver_marquee_path} or {screensaver_control_path}")
                reply = "One of the screensaver files not found: " + screensaver_marquee_path + " or " + screensaver_control_path
        elif command == 'SCREENSAVER-STOP':
            print("Command: SCREENSAVER-STOP")
            hideBitLCDClock()
            restoreDefaults()
            reply = "Screensaver stopped - returned to default state"
            # If the command cannot be found, then print the command could not be found set the reply variable to unknown command
        else:
            print("Unknown command: " + command)
            reply = 'Unknown command. Valid commands are GET, REPEAT <string>, SELECTED, OPEN, CLOSE, EXIT, KILL, SHUTDOWN, SCREENSAVER-START, SCREENSAVER-STOP'
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

