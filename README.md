# LCDMarquee
**Disclosure: AI was used in creating/modifying this project.**

Updated version of Passable Gamer's LCD Marquee Controller merged with Control Map generation of Texacate's Visual Retrpopie Control Maps. 

The entire project was inspired by [Way of the Wrench's video](https://youtu.be/Au9O-A2fz74?si=XJT3YeEFvu_R_Vjr).  

His version is [here on YouTube](https://youtu.be/wy0asRc0yLA?si=WObEnVR3QmIBuntf).

His version is actually an updated/modified version of [Texacate's Visual-RetroPie-Control-Maps](https://github.com/Texacate/Visual-RetroPie-Control-Maps)

This is based on those projects but has been modified heavily. 

I've done my best to make the install easy and well documented, but there are a lot of assumptions being made, as this was really a custom project for **MY** setup. 

My setup (as I write this). 

[Atgames Legends Ultimate HD (HAB802D)](https://www.atgames.us/products/legends-ultimate-ce-hd) (the current version as CE, I have an older version)
Date Code: 05/2022
Manufacturer: Dichrole Cat

Running: [R-CADE](https://github.com/retro-center/rcade_releases) version 2.08 off of a [Transcend ESD310 256GB External SSD](https://a.co/d/07lLbTI6). 

[Raspberry Pi 4 Model B Rev 1.5 1GB](https://a.co/d/04jLVVZd)
-- [AtGames Legends BitLCD HD](https://www.atgames.us/products/legends-bitlcd) - Marquee Screen 
-- [Waveshare 4 inch HDMI LCD IPS Display 800x480 Resolution Resistive Touch Screen](https://a.co/d/08mbi0Ak) - Control Map Screen

## 📌 Features
Marquee Display (BitLCD)

* Shows game-specific marquee images when a game is selected
* Shows system-level marquees when browsing system menus
* Falls back to the default marquee video on startup and when returning to the menu
* Supports multiple image formats: .png, .jpg, .jpeg, .gif
* Supports multiple video formats: .mp4, .avi, .mkv
* Theme support via theme.txt - directory-based theme selection
* Images displayed at native resolution (1920x360) without scaling

Control Map Display (Waveshare)

* Shows base navigation control map when browsing menus
* Shows game-specific control maps when a game is launched
* Auto-generates control maps from CSV button mapping data using button_map.sh
* Control maps cached after the first generation for instant display on subsequent launches
* Falls back to the marquee image if control map generation fails
* Staggered 6-button layout matching physical arcade panel (X/Y/Z top row, A/B/C bottom row)
* Button colors indicate active (green) vs inactive (black) buttons

https://github.com/user-attachments/assets/e5ae25ce-5a70-4d9a-8152-19e71b1e17ed

To install-

1) Image a Pi with a current version of PiOS with Desktop (Trixie was used when I did this.)
2) SSH and run updates on pi (I like to use - `sudo apt update  -y && sudo apt full-upgrade  -y && sudo apt autoremove -y`)
4) Change to Auto-login at boot (in raspi-config)
5) Upload the installfiles directory
6) Run the install script
   ```sudo python3 /home/<USERNAME>/installfiles/lcdmarqueesetup.py```

   This will walk through the installation of the necessary services and packages.
   Since it's running as sudo and makes some system level changes I've outlined what it's doing. 
	#### LCD Marquee Setup Script Details
   
	##### Execution Flow
	
	##### A. Initialization and Environment Setup
	* Helper Functions: Initializes utility functions to handle user prompts (yes/no queries), substitute variables within `.service` configuration files, and accurately detect the executing user.
	* Path Configuration: Confirms the target username and establishes absolute paths for necessary directories, including `bin`, `marquees`, and `control_maps`.
	
	##### B. Pre-Installation Cleanup
	* Service Termination: Stops existing systemd services related to the LCD marquee (e.g., `simpleServer`, `MarqueeImage`, `MarqueeVideo`, `HideConsole`, `SplashScreen`) to prevent conflicts during installation.
	
	##### C. File and Asset Deployment
	* Directory Management: Creates required directories and assigns appropriate read, write, and execute permissions.
	* Asset Copying: Prompts for permission to copy and overwrite default control map files and default media assets (such as `default.png`, `default_marquee.mp4`, and `screensaver_marquee.mp4`) into the target directories.
	
	##### D. Dependency Installation
	* System Updates: Executes system updates via `apt-get` to refresh package repositories.
	* Package Installation: Installs required media handling software, specifically `mpv` (for video playback) and `imagemagick` (for image manipulation).
	
	##### E. System Configuration
	* Permissions: Configures passwordless `sudo` access for the target user by dynamically writing a rule to `/etc/sudoers.d/`.
	* Service Registration: Copies `.service` templates to system directories (such as `/etc/systemd/system/`), injects user-specific variables (like UID and home directory), reloads the systemd daemon, and enables `simpleServer.service` to launch automatically on boot.
	
	##### F. Boot Sequence Modifications
	* Boot File Backups: Creates backup copies of standard boot configuration files (`/boot/firmware/config.txt` and `cmdline.txt`).
	* Silent Boot Adjustments: Prompts to inject parameters into the boot files to disable the rainbow splash screen and suppress console boot text, ensuring a seamless visual startup.
	
	##### G. Finalization
	* System Reboot: Prompts to reboot the hardware to apply all system-level changes and start the newly configured services.

7) Copy over any marquees into the appropriate system folder (for R-CADE, place all of the arcade collection marquees into MAME).

I needed to pre-rotate the videos that are displayed on the Control Map Screen. If you need to change the rotation of the images, you can do that here- 
```
sudo systemctl edit --full MarqueeImage 
```
  
8) On the ALU or R-CADE machine- copy the userscripts folder into rcade/share/userscripts. This can be done over ftp or through the network share.  _See note below_

9) Update the IP address in `marquee-daemon.py` to the IP address of the Pi. 

10) Reboot both systems.
    

_Note regarding the userscripts: When booting the system runs the scripts in this order System Ready > Game Selected (last game played) > System Selected (if start is set to go to a system. What this means is that you may see a flicker on the marquee of the Last Game Played. In the marquee-daemon.py script there is a variable to try to prevent this. If this is set too high, the initial System Selected won't be sent._


Because I'm using this on an R-CADE system running on an AtGames Legends Ultimate cabinet, not Retropie,  there are some additional scripts I've created that can be triggered at events like shutting down. This way the pi shuts down gracefully when the R-CADE system is shut down or rebooted. 

To have the control maps match the ALU, I had to change the layout from the original script.

ORGINAL:  
Y(1) X(2) L(3)  
B(4) A(5) R(6)  

ALU:  
X(4) Y(5) Z(6)  
A(1) B(2) C(3)  

This is only set to work with MAME and arcade games at the moment, and there's a high likelihood that not all games are there. Feel free to let me know if something isn't working or is missing. 

Additionally, I've included files I used for a custom boot splash screen using Plymouth. 
With the two screens, the geometry wasn't what would be expected. The smaller screen is inside the geometry of the BitLCD (which is technically 1080p but only the top third is visible). 
For this to work on both screens, I had to add some additional items to my `/boot/firmware/cmdline.txt` and `/boot/firmware/config.txt`. I've included the addtitions in a `cmdline.txt` file and my entire `config.txt` in case you're having trouble getting things to work. 

[Instructions for Setting up Splashscreens](SPLASHSCREEN.md)

<BR>
***Permission was obtained to include R-CADE images in this project. R-Cade and all associated R-Cade content is legal property of Retro-Center and goverened by the R-Cade license agreement. Unauthorized distribution, duplication, or usage is prohibited.<BR>
See the LICENSE.md file at the top-level directory of the Retro-Center GitHub releases at https://github.com/retro-center/rcade_releases/blob/master/LICENSE.md***
