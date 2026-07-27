# Import modules
import os
import time
import sys
import getpass
import pwd
import grp

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


def install_service(installfiles_dir, service_name, dest_dir, replacements):
    """Read a .service template from installfiles, substitute placeholders
    (e.g. __USER__, __GROUP__, __UID__, __HOME__), and install it to dest_dir.

    Writing goes through a temp file + 'sudo cp' since the script itself
    isn't necessarily running as root, only shelling out to sudo.
    """
    src = f"{installfiles_dir}/bin/services/{service_name}"
    with open(src, "r") as f:
        content = f.read()
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    tmp_path = f"/tmp/{service_name}"
    with open(tmp_path, "w") as f:
        f.write(content)

    dest_path = f"{dest_dir}/{service_name}"
    os.system(f"sudo cp {tmp_path} {dest_path}")
    os.system(f"sudo chmod 644 {dest_path}")
    os.remove(tmp_path)


def get_invoking_user():
    """Best-effort detection of the human running the script, even under sudo
    (where os.getlogin()/getpass.getuser() alone would report 'root')."""
    return os.environ.get("SUDO_USER") or getpass.getuser()


def query_username(default_user):
    """Ask which user this should be installed for and return the username.

    Leaving the answer blank accepts default_user. Verifies /home/<username>
    exists before accepting it, since everything else in the script is
    anchored off that directory.
    """
    while True:
        sys.stdout.write(f"Which user is this install for? [{default_user}]: ")
        username = input().strip()
        if not username:
            username = default_user
        candidate_home = f"/home/{username}"
        if not os.path.isdir(candidate_home):
            sys.stdout.write(f"'{candidate_home}' does not exist. Try again.\n")
            continue
        return username


# List of EmulationStation system folders that get a marquee subfolder.
MARQUEE_SYSTEMS = [
    "3do", "amiga", "amstradcpc", "apple2", "arcade", "atari800", "atari2600",
    "atari5200", "atari7800", "atarijaquar", "atarilynx", "atarist", "c64",
    "COCO", "coleco", "daphne", "dragon32", "dreamcast", "fba", "fds",
    "gameandwatch", "gamegear", "gb", "gba", "gbc", "gc", "intellivision",
    "macintosh", "mame", "mame-advmame", "mame-libretro", "mame-mame4all",
    "mastersystem", "megadrive", "msx", "n64", "nds", "neogeo", "nes", "ngp",
    "ngpc", "oric", "pc", "pcengine", "ps2", "psp", "psx", "samcoupe",
    "saturn", "scummvm", "sega32x", "segacd", "sg-1000", "snes", "ti99",
    "trs-80", "vectrex", "videopac", "virtualboy", "wii", "wonderswancolor",
    "zmachine", "zxspectrum",
]


# ----- Determine target user and derived paths -----
invoking_user = get_invoking_user()
username = query_username(invoking_user)
HOME_DIR = f"/home/{username}"
BIN_DIR = f"{HOME_DIR}/bin"
MARQUEES_DIR = f"{HOME_DIR}/marquees"
CONTROL_MAPS_DIR = f"{HOME_DIR}/control_maps"

# installfiles is always resolved relative to this script's own location,
# not to any user's home directory, since it ships side-by-side with it
# regardless of which user is being installed for or who ran the script.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALLFILES_DIR = f"{SCRIPT_DIR}/installfiles"

user_info = pwd.getpwnam(username)
user_uid = user_info.pw_uid
user_group = grp.getgrgid(user_info.pw_gid).gr_name

SERVICE_REPLACEMENTS = {
    "__USER__": username,
    "__GROUP__": user_group,
    "__UID__": str(user_uid),
    "__HOME__": HOME_DIR,
}

print(f"Installing for user '{username}' (uid={user_uid}, group={user_group}, home: {HOME_DIR})")
print(f"Using install files from: {INSTALLFILES_DIR}")


#Although these service are not running yet, going to try to stop them anyway.
print("***** Stopping LCD Marquee Controller Services (Services may not exist yet) *****")
os.system("sudo systemctl stop simpleServer.service")
os.system("sudo systemctl stop MarqueeImage.service")
os.system("sudo systemctl stop MarqueeVideo.service")
os.system("sudo systemctl stop HideConsole.service")
os.system("sudo systemctl stop SplashScreen.service")



#Copy original simpleServer.py.ORIGINAL file
print("***** Copy simpleServer.py.ORIGINAL file *****")
if not os.path.exists(f"{BIN_DIR}/simpleServer.py.ORIGINAL"):
    os.system(f"sudo cp {INSTALLFILES_DIR}/bin/simpleServer.py.ORIGINAL {BIN_DIR}/simpleServer.py.ORIGINAL")

#create needed directories
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)
    os.system(f"sudo chmod 777 {BIN_DIR}")

if not os.path.exists(MARQUEES_DIR):
    os.makedirs(MARQUEES_DIR)
    os.system(f"sudo chmod 777 {MARQUEES_DIR}")

if not os.path.exists(f"{MARQUEES_DIR}/arcade"):
    os.makedirs(f"{MARQUEES_DIR}/arcade")
    os.system(f"sudo chmod 777 {MARQUEES_DIR}/arcade")




#Copy new simpleServer.py file
print("***** Copy new simpleServer.py file *****")
if os.path.exists(f"{BIN_DIR}/simpleServer.py"):
    os.system(f"sudo cp {BIN_DIR}/simpleServer.py {BIN_DIR}/simpleServer.py.OLD")
    os.remove(f"{BIN_DIR}/simpleServer.py")
os.system(f"sudo cp {INSTALLFILES_DIR}/bin/simpleServer.py {BIN_DIR}/simpleServer.py")


#Copy control-map files
print("***** Copy Control Map files *****")
defaultimganswer=query_yes_no("Do you wish to replace existing control map files? (Select n if you created custom images)")
if defaultimganswer == True:
    if os.path.exists(CONTROL_MAPS_DIR):
        os.system(f"sudo mv {CONTROL_MAPS_DIR} {CONTROL_MAPS_DIR}.OLD")

    #Why were we making this earlier if only to rename it and not set permissions?
    if not os.path.exists(CONTROL_MAPS_DIR):
        os.makedirs(CONTROL_MAPS_DIR)
        os.makedirs(f"{CONTROL_MAPS_DIR}/arcade")
        os.system(f"sudo chown -R {username}:{username} {CONTROL_MAPS_DIR}/")
        os.system(f"sudo chmod -R 755 {CONTROL_MAPS_DIR}")



os.system(f"sudo cp -R {INSTALLFILES_DIR}/control_maps {HOME_DIR}/")
os.system(f"sudo chmod +x {CONTROL_MAPS_DIR}/button_map.sh")


#Ask if new default.png file should be created and if so, copy new file.
print("***** Copy new default.png file *****")
defaultimganswer=query_yes_no("Do you wish to replace default.png file? This is a default still image that can be used. (Select n if you created custom image)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/default.png"):
        os.system(f"sudo cp {MARQUEES_DIR}/default.png {MARQUEES_DIR}/default.png.OLD")
        os.remove(f"{MARQUEES_DIR}/default.png")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/default.png {MARQUEES_DIR}/default.png")

#Ask if new default.mp4 file should be created and if so, copy new file.
print("***** Copy new default.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace default.mp4 file? This is a default video that can be used.  (Select n if you created custom video)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/default.mp4"):
        os.system(f"sudo cp {MARQUEES_DIR}/default.mp4 {MARQUEES_DIR}/default.mp4.OLD")
        os.remove(f"{MARQUEES_DIR}/default.mp4")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/default.mp4 {MARQUEES_DIR}/default.mp4")
    
#Ask if new default_marquee.mp4 file should be created and if so, copy new file.
print("***** Copy new default_marquee.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace default_marquee.mp4 file? This is the default video shown on the marquee screen. (Select n if you created custom video)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/default_marquee.mp4"):
        os.system(f"sudo cp {MARQUEES_DIR}/default_marquee.mp4 {MARQUEES_DIR}/default_marquee.mp4.OLD")
        os.remove(f"{MARQUEES_DIR}/default_marquee.mp4")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/default_marquee.mp4 {MARQUEES_DIR}/default_marquee.mp4")
    
#Ask if new default_control.mp4 file should be created and if so, copy new file.
print("***** Copy new default_control.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace default_control.mp4 file? This is the default video shown on the control map screen. (Select n if you created custom video)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/default_control.mp4"):
        os.system(f"sudo cp {MARQUEES_DIR}/default_control.mp4 {MARQUEES_DIR}/default_control.mp4.OLD")
        os.remove(f"{MARQUEES_DIR}/default_control.mp4")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/default_control.mp4 {MARQUEES_DIR}/default_control.mp4")    

#Ask if new default_rotated.mp4 file should be created and if so, copy new file.
print("***** Copy new default_rotated.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace default_rotated.mp4 file? This is the default video shown on the control map screen rotated to display correctly on some screens. (Select n if you created custom video)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/default_rotated.mp4"):
        os.system(f"sudo cp {MARQUEES_DIR}/default_rotated.mp4 {MARQUEES_DIR}/default_rotated.mp4.OLD")
        os.remove(f"{MARQUEES_DIR}/default_rotated.mp4")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/default_rotated.mp4 {MARQUEES_DIR}/default_rotated.mp4")  

#Ask if new screensaver_control.mp4 file should be created and if so, copy new file.
print("***** Copy new screensaver_control.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace screensaver_control.mp4 file? This is the default screensaver video shown on the control map screen. (Select n if you created custom video)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/screensaver_control.mp4"):
        os.system(f"sudo cp {MARQUEES_DIR}/screensaver_control.mp4 {MARQUEES_DIR}/screensaver_control.mp4.OLD")
        os.remove(f"{MARQUEES_DIR}/screensaver_control.mp4")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/screensaver_control.mp4 {MARQUEES_DIR}/screensaver_control.mp4")   
    
#Ask if new screensaver_marquee.mp4 file should be created and if so, copy new file.
print("***** Copy new screensaver_marquee.mp4 file *****")
defaultimganswer=query_yes_no("Do you wish to replace screensaver_marquee.mp4 file? This is the default screensaver video shown on the marquee. (Select n if you created custom video)")
if defaultimganswer == True:
    if os.path.exists(f"{MARQUEES_DIR}/screensaver_marquee.mp4"):
        os.system(f"sudo cp {MARQUEES_DIR}/screensaver_marquee.mp4 {MARQUEES_DIR}/screensaver_marquee.mp4.OLD")
        os.remove(f"{MARQUEES_DIR}/screensaver_marquee.mp4")
    os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/screensaver_marquee.mp4 {MARQUEES_DIR}/screensaver_marquee.mp4")   
        
print("***** Copy blank.png placeholder file *****")    
os.system(f"sudo cp {INSTALLFILES_DIR}/marquees/blank.png {MARQUEES_DIR}/blank.png")  

#Install updates
print("***** Running update... *****")
os.system("sudo apt-get update --fix-missing")
#os.system("sudo apt-get upgrade -y")

#Install mpv
print("***** Installing MPV... *****")
os.system("sudo apt-get -y install mpv")

#Pause for 10 seconds
print("Pausing for 10 seconds...")
time.sleep(10)

#Run updates again
print("***** Running update... *****")
os.system("sudo apt-get update --fix-missing")
#os.system("sudo apt-get upgrade -y")

#Install imagemagick
print("***** Installing Imagemagick... *****")
os.system("sudo apt-get -y install imagemagick")

#Pause for 10 seconds
print("Pausing for 10 seconds...")
time.sleep(10)

#Run update again
print("***** Running update... *****")
os.system("sudo apt-get update --fix-missing")

#Install FIM
#print("***** Installing FIM... *****")
#os.system("sudo apt-get -y install fim")

#Copy services to appropriate places, filling in this user's info as we go
print("***** Installing LCD Marquee Services... *****")
install_service(INSTALLFILES_DIR, "MarqueeBitLCD.service", "/etc/systemd/system", SERVICE_REPLACEMENTS)
install_service(INSTALLFILES_DIR, "MarqueeBitLCDImage.service", "/etc/systemd/system", SERVICE_REPLACEMENTS)
install_service(INSTALLFILES_DIR, "MarqueeImage.service", "/lib/systemd/system", SERVICE_REPLACEMENTS)
install_service(INSTALLFILES_DIR, "MarqueeVideo.service", "/lib/systemd/system", SERVICE_REPLACEMENTS)
install_service(INSTALLFILES_DIR, "simpleServer.service", "/lib/systemd/system", SERVICE_REPLACEMENTS)

#Reload Services
print("***** Reloading Services... *****")
os.system("sudo systemctl daemon-reload")

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
    configpath = "/boot/firmware/config.txt"
    if not os.path.exists(configpath):
        configpath = "/boot/config.txt"

    if os.path.exists(configpath):
        os.system(f"sudo chmod 755 {configpath}")
        with open(configpath, "a") as myfile:
            myfile.write("disable_splash=1\n")
        print(f"{configpath} has been updated")
    else:
        print("ERROR: Could not find config.txt at /boot/firmware/ or /boot/")
else:
    print("config.txt will not be updated")

#Copy new cmdline.txt file and set permissions on new cmdline.txt file
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
        print("ERROR: Could not find cmdline.txt at /boot/firmware/ or /boot/")
else:
    print("cmdline.txt will not be updated")

# Ask to reboot device
rebootanswer=query_yes_no("Reboot is required. Do you wish to reboot now?")
if rebootanswer == True:
    os.system("sudo reboot")
