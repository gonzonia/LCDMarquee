# LCDMarquee
Updated version of Passable Gamer's LCD Marquee Controller merged with Control Map generation of Texacate's Visual Retrpopie Control Maps. 

The entire project was inspired by [Way of the Wrench's video](https://youtu.be/Au9O-A2fz74?si=XJT3YeEFvu_R_Vjr). If you run into problems, watch this in case I missed a step in my instructions. My goal was to streamline the server side, but there may be something I missed for the client side. 

His version is [here on YouTube](https://youtu.be/wy0asRc0yLA?si=WObEnVR3QmIBuntf).

His version is actually an updated/modified version of [Texacate's Visual-RetroPie-Control-Maps](https://github.com/Texacate/Visual-RetroPie-Control-Maps)

You will need Texacate's client (`simpleClient.py`) to call the server. **Be sure to update the IP address in that file with the IP address of your marquee Pi.** 


To install- (this assumes you are using a user of Pi and the scripts are assuming that as well, if not, you'll need to alter everything)
1) Image a Pi with a Lite version of PiOS (Trixie was used when I did this.)
2) SSH and run updates on pi (`sudo apt update  -y && sudo apt full-upgrade  -y && sudo apt autoremove -y`)
4) Change to Auto-login at boot (in raspi-config)
5) Upload the installfiles directory
6) Run the installscript
   ```sudo python3 /home/pi/installfiles/bin/lcdmarqueesetup.py```

   This will walk through the installation of the necessary services and packages.

7) Copy over any marquees into the appropriate system folder (for RCADE the arcade collection all go into MAME).

***Changes***
**It now uses MPV to play video.** It also allows for rotating the screen if necessary. 

You can change the rotation in `display_image_rotated.sh` if you don't need it rotated (It's currently set to 270). 

To change the video rotation, edit in the service:
```
sudo systemctl edit --full MarqueeVideo
```

I've also added the ability to send a "SHUTDOWN" command and changed the Marquee to use the "SELECTED" command. "OPEN" will trigger the control map generation. If you only want the marquee, be sure to use "SELECTED" when calling the server. 

I'm using this on an RCADE system running on an AtGames Legends Ultimate cabinet, not retropie. As a result, there are some additional scripts I've created that can be triggered at events like shutting down. This way the pi shuts down gracefully when the RCADE is shutdown. I have it showing a marquee when selecting a game, and then when the game is open it shows the control map. 

To accomplish this and have the control maps match, I had to change the layout in the button map script as well.   
ORGINAL:  
Y(1) X(2) L(3)  
B(4) A(5) R(6)  

ALU:  
X(4) Y(5) Z(6)  
A(1) B(2) C(3)  

This is only set to work with mame and arcade games at the moment and they might not all be there. Feel free to let me know if something isn't working or is mising. 

I tried running on a Pi Zero W and it couldn't handle video, was also slow to start up, switch screens, and generate control maps.

I switched to a Pi 5 8GB. 
