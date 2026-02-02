# Import modules
import os
import time
import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

#Althought these service are not running yet, going to try to stop them anyway.
print("***** Stopping LCD Marquee Controller Services (Services may not exist yet) *****")
os.system("sudo systemctl stop simpleServer.service")
os.system("sudo systemctl stop MarqueeImage.service")
os.system("sudo systemctl stop MarqueeVideo.service")
os.system("sudo systemctl stop HideConsole.service")
os.system("sudo systemctl stop SplashScreen.service")



#Copy original simpleServer.py.ORIGINAL file
print("***** Copy simpleServer.py.ORIGINAL file *****")
if not os.path.exists("/home/pi/bin/simpleServer.py.ORIGINAL"):
    os.system("sudo cp /home/pi/installfiles/bin/simpleServer.py.ORIGINAL /home/pi/bin/simpleServer.py.ORIGINAL")

#create needed directories
if not os.path.exists("/home/pi/bin"):
    os.makedirs("/home/pi/bin")
    os.system("sudo chmod 777 /home/pi/bin")

if not os.path.exists("/home/pi/marquees"):
    os.makedirs("/home/pi/marquees")
    os.system("sudo chmod 777 /home/pi/marquees")    

if not os.path.exists("/home/pi/marquees/arcade"):
    os.makedirs("/home/pi/marquees/arcade")
    os.system("sudo chmod 777 /home/pi/marquees/arcade") 
          
if not os.path.exists("/home/pi/control_maps"):
    os.makedirs("/home/pi/control_maps")
    os.system("sudo chmod 777 -R /home/pi/control_maps") 


#Copy new simpleServer.py file
print("***** Copy new simpleServer.py file *****")
if os.path.exists("/home/pi/bin/simpleServer.py"):
    os.system("sudo cp /home/pi/bin/simpleServer.py /home/pi/bin/simpleServer.py.OLD")
    os.remove("/home/pi/bin/simpleServer.py")
os.system("sudo cp /home/pi/installfiles/bin/simpleServer.py /home/pi/bin/simpleServer.py")

#Copy new support file display_image_rotated.sh 
print("***** Copy new simpleServer.py file *****")
if os.path.exists("/home/pi/bin/display_image_rotated.sh"):
    os.system("sudo cp /home/pi/bin/display_image_rotated.sh /home/pi/bin/display_image_rotated.sh.OLD")
    os.remove("/home/pi/bin/display_image_rotated.sh")
os.system("sudo cp /home/pi/installfiles/bin/display_image_rotated.sh /home/pi/bin/display_image_rotated.sh")
os.system("sudo chmod +x /home/pi/bin/display_image_rotated.sh")

#Copy control-map files
print("***** Copy Control Map files *****")
defaultimganswer=query_yes_no("Do you wish to replace existing control map files? (Select n if you created custom images)")
if defaultimganswer == True:
	if os.path.exists("/home/pi/control_maps"):
    	os.system("sudo mv /home/pi/control_maps /home/pi/control_maps.OLD")
os.system("sudo cp -R /home/pi/installfiles/control_maps /home/pi/control_maps")
os.system("sudo chmod +x /home/pi/control_maps/button_map.sh")

#Ask if new default.png file should be created and if so, copy new file.
print("***** Copy new default.png file *****")
defaultimganswer=query_yes_no("Do you wish to replace default.png file? (Select n if you created custom image)")
if defaultimganswer == True:
    if os.path.exists("/home/pi/marquees/default.png"):    
        os.system("sudo cp /home/pi/marquees/default.png /home/pi/marquees/default.png.OLD")
        os.remove("/home/pi/marquees/default.png")
    os.system("sudo cp /home/pi/installfiles/marquees/default.png /home/pi/marquees/default.png")
    
    #Ask if new default.png file should be created and if so, copy new file.
print("***** Copy new default.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace default.mp4 file? (Select n if you created custom image)")
if defaultimganswer == True:
    if os.path.exists("/home/pi/marquees/default.mp4"):    
        os.system("sudo cp /home/pi/marquees/default.mp4 /home/pi/marquees/default.mp4.OLD")
        os.remove("/home/pi/marquees/default.mp4")
    os.system("sudo cp /home/pi/installfiles/marquees/default.mp4 /home/pi/marquees/default.mp4")


# Install splashscreen image
print("***** Copy new splashscreen.png file *****")
if os.path.exists("/home/pi/marquees/splashscreen.png"):
    os.system("sudo cp /home/pi/marquees/splashscreen.png /home/pi/marquees/splashscreen.png.OLD")
    os.remove("/home/pi/marquees/splashscreen.png")    
os.system("sudo cp /home/pi/installfiles/marquees/splashscreen.png /home/pi/marquees/splashscreen.png")

# Create folders for systems used to hold marquee image files
print("***** Create marquee system folders for images *****")
if not os.path.exists("/home/pi/marquees"):
    os.makedirs("/home/pi/marquees")
    os.system("sudo chmod 777 /home/pi/marquees")
if not os.path.exists("/home/pi/marquees/3do"):
    os.makedirs("/home/pi/marquees/3do")
    os.system("sudo chmod 777 /home/pi/marquees/3do")
if not os.path.exists("/home/pi/marquees/amiga"):
    os.makedirs("/home/pi/marquees/amiga")
    os.system("sudo chmod 777 /home/pi/marquees/amiga")
if not os.path.exists("/home/pi/marquees/amstradcpc"):
    os.makedirs("/home/pi/marquees/amstradcpc")
    os.system("sudo chmod 777 /home/pi/marquees/amstradcpc")
if not os.path.exists("/home/pi/marquees/apple2"):
    os.makedirs("/home/pi/marquees/apple2")
    os.system("sudo chmod 777 /home/pi/marquees/apple2")
if not os.path.exists("/home/pi/marquees/arcade"):
    os.makedirs("/home/pi/marquees/arcade")
    os.system("sudo chmod 777 /home/pi/marquees/arcade")
if not os.path.exists("/home/pi/marquees/atari800"):
    os.makedirs("/home/pi/marquees/atari800")
    os.system("sudo chmod 777 /home/pi/marquees/atari800")
if not os.path.exists("/home/pi/marquees/atari2600"):
    os.makedirs("/home/pi/marquees/atari2600")
    os.system("sudo chmod 777 /home/pi/marquees/atari2600")
if not os.path.exists("/home/pi/marquees/atari5200"):
    os.makedirs("/home/pi/marquees/atari5200")
    os.system("sudo chmod 777 /home/pi/marquees/atari5200")
if not os.path.exists("/home/pi/marquees/atari7800"):
    os.makedirs("/home/pi/marquees/atari7800")
    os.system("sudo chmod 777 /home/pi/marquees/atari7800")
if not os.path.exists("/home/pi/marquees/atarijaquar"):
    os.makedirs("/home/pi/marquees/atarijaquar")
    os.system("sudo chmod 777 /home/pi/marquees/atarijaquar")
if not os.path.exists("/home/pi/marquees/atarilynx"):
    os.makedirs("/home/pi/marquees/atarilynx")
    os.system("sudo chmod 777 /home/pi/marquees/atarilynx")
if not os.path.exists("/home/pi/marquees/atarist"):
    os.makedirs("/home/pi/marquees/atarist")
    os.system("sudo chmod 777 /home/pi/marquees/atarist")
if not os.path.exists("/home/pi/marquees/c64"):
    os.makedirs("/home/pi/marquees/c64")
    os.system("sudo chmod 777 /home/pi/marquees/c64")
if not os.path.exists("/home/pi/marquees/COCO"):
    os.makedirs("/home/pi/marquees/COCO")
    os.system("sudo chmod 777 /home/pi/marquees/COCO")
if not os.path.exists("/home/pi/marquees/coleco"):
    os.makedirs("/home/pi/marquees/coleco")
    os.system("sudo chmod 777 /home/pi/marquees/coleco")
if not os.path.exists("/home/pi/marquees/daphne"):
    os.makedirs("/home/pi/marquees/daphne")
    os.system("sudo chmod 777 /home/pi/marquees/daphne")
if not os.path.exists("/home/pi/marquees/dragon32"):
    os.makedirs("/home/pi/marquees/dragon32")
    os.system("sudo chmod 777 /home/pi/marquees/dragon32")
if not os.path.exists("/home/pi/marquees/dreamcast"):
    os.makedirs("/home/pi/marquees/dreamcast")
    os.system("sudo chmod 777 /home/pi/marquees/dreamcast")
if not os.path.exists("/home/pi/marquees/fba"):
    os.makedirs("/home/pi/marquees/fba")
    os.system("sudo chmod 777 /home/pi/marquees/fba")
if not os.path.exists("/home/pi/marquees/fds"):
    os.makedirs("/home/pi/marquees/fds")
    os.system("sudo chmod 777 /home/pi/marquees/fds")
if not os.path.exists("/home/pi/marquees/gameandwatch"):
    os.makedirs("/home/pi/marquees/gameandwatch")
    os.system("sudo chmod 777 /home/pi/marquees/gameandwatch")
if not os.path.exists("/home/pi/marquees/gamegear"):
    os.makedirs("/home/pi/marquees/gamegear")
    os.system("sudo chmod 777 /home/pi/marquees/gamegear")
if not os.path.exists("/home/pi/marquees/gb"):
    os.makedirs("/home/pi/marquees/gb")
    os.system("sudo chmod 777 /home/pi/marquees/gb")
if not os.path.exists("/home/pi/marquees/gba"):
    os.makedirs("/home/pi/marquees/gba")
    os.system("sudo chmod 777 /home/pi/marquees/gba")
if not os.path.exists("/home/pi/marquees/gbc"):
    os.makedirs("/home/pi/marquees/gbc")
    os.system("sudo chmod 777 /home/pi/marquees/gbc")
if not os.path.exists("/home/pi/marquees/gc"):
    os.makedirs("/home/pi/marquees/gc")
    os.system("sudo chmod 777 /home/pi/marquees/gc")
if not os.path.exists("/home/pi/marquees/intellivision"):
    os.makedirs("/home/pi/marquees/intellivision")
    os.system("sudo chmod 777 /home/pi/marquees/intellivision")
if not os.path.exists("/home/pi/marquees/macintosh"):
    os.makedirs("/home/pi/marquees/macintosh")
    os.system("sudo chmod 777 /home/pi/marquees/macintosh")
if not os.path.exists("/home/pi/marquees/mame"):
    os.makedirs("/home/pi/marquees/mame")
    os.system("sudo chmod 777 /home/pi/marquees/mame")    
if not os.path.exists("/home/pi/marquees/mame-advmame"):
    os.makedirs("/home/pi/marquees/mame-advmame")
    os.system("sudo chmod 777 /home/pi/marquees/mame-advmame")
if not os.path.exists("/home/pi/marquees/mame-libretro"):
    os.makedirs("/home/pi/marquees/mame-libretro")
    os.system("sudo chmod 777 /home/pi/marquees/mame-libretro")
if not os.path.exists("/home/pi/marquees/mame-mame4all"):
    os.makedirs("/home/pi/marquees/mame-mame4all")
    os.system("sudo chmod 777 /home/pi/marquees/mame-mame4all")
if not os.path.exists("/home/pi/marquees/mastersystem"):
    os.makedirs("/home/pi/marquees/mastersystem")
    os.system("sudo chmod 777 /home/pi/marquees/mastersystem")
if not os.path.exists("/home/pi/marquees/megadrive"):
    os.makedirs("/home/pi/marquees/megadrive")
    os.system("sudo chmod 777 /boot/cmdline.txt")
if not os.path.exists("/home/pi/marquees/msx"):
    os.makedirs("/home/pi/marquees/msx")
    os.system("sudo chmod 777 /home/pi/marquees/msx")
if not os.path.exists("/home/pi/marquees/n64"):
    os.makedirs("/home/pi/marquees/n64")
    os.system("sudo chmod 777 /home/pi/marquees/n64")
if not os.path.exists("/home/pi/marquees/nds"):
    os.makedirs("/home/pi/marquees/nds")
    os.system("sudo chmod 777 /home/pi/marquees/nds")
if not os.path.exists("/home/pi/marquees/neogeo"):
    os.makedirs("/home/pi/marquees/neogeo")
    os.system("sudo chmod 777 /home/pi/marquees/neogeo")
if not os.path.exists("/home/pi/marquees/nes"):
    os.makedirs("/home/pi/marquees/nes")
    os.system("sudo chmod 777 /home/pi/marquees/nes")
if not os.path.exists("/home/pi/marquees/ngp"):
    os.makedirs("/home/pi/marquees/ngp")
    os.system("sudo chmod 777 /home/pi/marquees/ngp")
if not os.path.exists("/home/pi/marquees/ngpc"):
    os.makedirs("/home/pi/marquees/ngpc")
    os.system("sudo chmod 777 /home/pi/marquees/ngpc")
if not os.path.exists("/home/pi/marquees/oric"):
    os.makedirs("/home/pi/marquees/oric")
    os.system("sudo chmod 777 /home/pi/marquees/oric")
if not os.path.exists("/home/pi/marquees/pc"):
    os.makedirs("/home/pi/marquees/pc")
    os.system("sudo chmod 777 /home/pi/marquees/pc")
if not os.path.exists("/home/pi/marquees/pcengine"):
    os.makedirs("/home/pi/marquees/pcengine")
    os.system("sudo chmod 777 /home/pi/marquees/pcengine")
if not os.path.exists("/home/pi/marquees/ps2"):
    os.makedirs("/home/pi/marquees/ps2")
    os.system("sudo chmod 777 /home/pi/marquees/ps2")
if not os.path.exists("/home/pi/marquees/psp"):
    os.makedirs("/home/pi/marquees/psp")
    os.system("sudo chmod 777 /home/pi/marquees/psp")
if not os.path.exists("/home/pi/marquees/psx"):
    os.makedirs("/home/pi/marquees/psx")
    os.system("sudo chmod 777 /home/pi/marquees/psx")
if not os.path.exists("/home/pi/marquees/samcoupe"):
    os.makedirs("/home/pi/marquees/samcoupe")
    os.system("sudo chmod 777 /home/pi/marquees/samcoupe")
if not os.path.exists("/home/pi/marquees/saturn"):
    os.makedirs("/home/pi/marquees/saturn")
    os.system("sudo chmod 777 /home/pi/marquees/saturn")
if not os.path.exists("/home/pi/marquees/scummvm"):
    os.makedirs("/home/pi/marquees/scummvm")
    os.system("sudo chmod 777 /home/pi/marquees/scummvm")
if not os.path.exists("/home/pi/marquees/sega32x"):
    os.makedirs("/home/pi/marquees/sega32x")
    os.system("sudo chmod 777 /home/pi/marquees/sega32x")
if not os.path.exists("/home/pi/marquees/segacd"):
    os.makedirs("/home/pi/marquees/segacd")
    os.system("sudo chmod 777 /home/pi/marquees/segacd")
if not os.path.exists("/home/pi/marquees/sg-1000"):
    os.makedirs("/home/pi/marquees/sg-1000")
    os.system("sudo chmod 777 /home/pi/marquees/sg-1000")
if not os.path.exists("/home/pi/marquees/snes"):
    os.makedirs("/home/pi/marquees/snes")
    os.system("sudo chmod 777 /home/pi/marquees/snes")
if not os.path.exists("/home/pi/marquees/ti99"):
    os.makedirs("/home/pi/marquees/ti99")
    os.system("sudo chmod 777 /home/pi/marquees/ti99")
if not os.path.exists("/home/pi/marquees/trs-80"):
    os.makedirs("/home/pi/marquees/trs-80")
    os.system("sudo chmod 777 /home/pi/marquees/trs-80")
if not os.path.exists("/home/pi/marquees/vectrex"):
    os.makedirs("/home/pi/marquees/vectrex")
    os.system("sudo chmod 777 /home/pi/marquees/vectrex")
if not os.path.exists("/home/pi/marquees/videopac"):
    os.makedirs("/home/pi/marquees/videopac")
    os.system("sudo chmod 777 /home/pi/marquees/videopac")
if not os.path.exists("/home/pi/marquees/virtualboy"):
    os.makedirs("/home/pi/marquees/virtualboy")
    os.system("sudo chmod 777 /home/pi/marquees/virtualboy")
if not os.path.exists("/home/pi/marquees/wii"):
    os.makedirs("/home/pi/marquees/wii")
    os.system("sudo chmod 777 /home/pi/marquees/wii")
if not os.path.exists("/home/pi/marquees/wonderswancolor"):
    os.makedirs("/home/pi/marquees/wonderswancolor")
    os.system("sudo chmod 777 /home/pi/marquees/wonderswancolor")
if not os.path.exists("/home/pi/marquees/zmachine"):
    os.makedirs("/home/pi/marquees/zmachine")
    os.system("sudo chmod 777 /home/pi/marquees/zmachine")
if not os.path.exists("/home/pi/marquees/zxspectrum"):
    os.makedirs("/home/pi/marquees/zxspectrum")
    os.system("sudo chmod 777 /home/pi/marquees/zxspectrum")

#Install updates
print("***** Running update... *****")
os.system("sudo apt-get update --fix-missing")
#os.system("sudo apt-get upgrade -y")

#Install omxplayer
print("***** Installing MPV... *****")
os.system("sudo apt-get -y install mpv")

#Pause for 10 seconds
print("Pausing for 10 seconds...")
time.sleep(10)

#Run updates again
print("***** Running update... *****")
os.system("sudo apt-get update --fix-missing")
#os.system("sudo apt-get upgrade -y")

#Install omxplayer
print("***** Installing Imagemagick... *****")
os.system("sudo apt-get -y install imagemagick")

#Pause for 10 seconds
print("Pausing for 10 seconds...")
time.sleep(10)

#Run update again
print("***** Running update... *****")
os.system("sudo apt-get update --fix-missing")
 
#Install FIM
print("***** Installing FIM... *****")
os.system("sudo apt-get -y install fim")

#Copy services to appropriate places
print("***** Installing LCD Marquee Services... *****")
os.system("sudo cp /home/pi/installfiles/bin/services/SplashScreen.service /etc/systemd/system/SplashScreen.service")
os.system("sudo cp /home/pi/installfiles/bin/services/HideConsole.service /etc/systemd/system/HideConsole.service")
os.system("sudo cp /home/pi/installfiles/bin/services/MarqueeImage.service /lib/systemd/system/MarqueeImage.service")
os.system("sudo cp /home/pi/installfiles/bin/services/MarqueeVideo.service /lib/systemd/system/MarqueeVideo.service")
os.system("sudo cp /home/pi/installfiles/bin/services/simpleServer.service /lib/systemd/system/simpleServer.service")

#Set permissions on services so they will execute
print("***** Setting permissions on LCD Marquee Services... *****")
os.system("sudo chmod 644 /etc/systemd/system/SplashScreen.service")
os.system("sudo chmod 644 /etc/systemd/system/HideConsole.service")
os.system("sudo chmod 644 /lib/systemd/system/MarqueeImage.service")
os.system("sudo chmod 644 /lib/systemd/system/MarqueeVideo.service")
os.system("sudo chmod 644 /lib/systemd/system/simpleServer.service")

#Reload Services
print("***** Reloading Services... *****")
os.system("sudo systemctl daemon-reload")

#Enable the SplashScreen service to start automatically on bootup.
print("***** Set SplashScreen service to run on bootup... *****")
os.system("sudo systemctl enable SplashScreen.service")

#Enable the Hide Consoler service to start automatically on bootup.
print("***** Set SplashScreen service to run on bootup... *****")
os.system("sudo systemctl enable HideConsole.service")

print("***** Set SimpleServer service to run on bootup... *****")
os.system("sudo systemctl enable simpleServer.service")

#Make copy of config.txt and cmdline.txt files
print("***** Backing up config.txt and cmdline.txt... *****")
os.system("sudo cp /boot/firmware/config.txt /boot/firmware/config.BACKUP")
os.system("sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.BACKUP")

#Append line to the config.txt file to disable the splash screen
print("***** Update config.txt file... *****")
print("Will now edit the config.txt file. File will be updated with line")
print("disable_splash=1 to disable rainbow splash screen at boot up.")
configanswer=query_yes_no("Do you wish to update config.txt? Requires sudo. (Select n if you already updated file)")
if configanswer == True:
    cmdpath = "/boot/firmware/config.txt"
    if not os.path.exists(cmdpath):
        cmdpath = "/boot/config.txt"
        
    os.system("sudo chmod 755 /boot/firmware/config.txt")
    with open("/boot/firmware/config.txt", "a") as myfile:
        myfile.write("disable_splash=1\n")
    myfile.close()
    print("config.txt has been updated")
else:
    print("config.txt will not be updated")
#Copy new cmdline.txt file and set permissions on new cmdline.txt file
#This might not be working!
print("***** Update cmdline.txt file... *****")
print("Will now edit the cmdline.txt file to disable all text on bootup.")
cmdlineanswer=query_yes_no("Do you wish to update cmdline.txt? Requires sudo. (Select n if you already updated file)")
if cmdlineanswer == True:
    # Determine the correct path
    cmdpath = "/boot/firmware/cmdline.txt"
    if not os.path.exists(cmdpath):
        cmdpath = "/boot/cmdline.txt"

    if os.path.exists(cmdpath):
        # 1. Read existing content
        with open(cmdpath, "r") as f:
            existline = f.read().strip()

        # 2. Split into parts and filter out empty strings and ANY existing console settings
        # This handles the replacement of console=tty1 or any other console
        parts = [p for p in existline.split(" ") if p and not p.startswith("console=")]

        # 3. Define our desired values
        # console=tty3 is added first to ensure it's in the list
        new_values = ["console=tty3", "logo.nologo", "quiet", "loglevel=3", "vt.global_cursor_default=0"]

        # 4. Add the new values only if they aren't already present
        for val in new_values:
            if val not in parts:
                parts.append(val)

        # 5. Reconstruct the line
        new_cmdline = " ".join(parts)

        # 6. Overwrite the file
        try:
            with open(cmdpath, "w") as newcmdlinefile:
                newcmdlinefile.write(new_cmdline + "\n")
            
            # Set permissions
            os.chmod(cmdpath, 0o755)
            print(f"Successfully updated {cmdpath}")
            print(f"New settings: {new_cmdline}")
        except PermissionError:
            print("ERROR: Permission denied. Please run this script with 'sudo'.")
    else:
        print(f"ERROR: Could not find cmdline.txt at /boot/firmware/ or /boot/")
else:
    print("cmdline.txt will not be updated")

# Ask to reboot device
rebootanswer=query_yes_no("Reboot is required. Do you wish to reboot now?")
if rebootanswer == True:
    os.system("sudo reboot")

