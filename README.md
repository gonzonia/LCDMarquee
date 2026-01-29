# LCDMarquee
Updated version of Passable Gamer's LCD Marquee Controller

The entire project was inspired by [Way of the Wrench's video](https://youtu.be/Au9O-A2fz74?si=XJT3YeEFvu_R_Vjr). If you run into problems, watch this in case I missed a step in my instructions. My goal was to streamline the server side, but there may be something I missed for the client side. 

His version is [here on YouTube](https://youtu.be/wy0asRc0yLA?si=WObEnVR3QmIBuntf).

His version is actually an updated/modified version of [Texacate's Visual-RetroPie-Control-Maps](https://github.com/Texacate/Visual-RetroPie-Control-Maps)

This version doesn't need Texacate's server installed first. 
You will need Texacate's client (simpleClient.py) to call the server. Be sure to update the IP address in that file with the IP address of your marquee Pi. 


To install- (this assume you are using a user of Pi and the scripts are assuming that as well)
1) Image a Pi with a Lite version of PiOS (Trixie was used when I did this.)
2) SSH and run updates on pi (sudo apt update  -y && sudo apt full-upgrade  -y && sudo apt autoremove -y)
4) Change to Auto-login at boot (in raspi-config)
5) Create directories
  ```
  mkdir bin
  mkdir marquees
  mkdir marquees/arcade
  ```
5) Upload installfiles directory
6) Run Installscript
   ```sudo /usr/bin/python3 /home/pi/installfiles/bin/lcdmarqueesetup.py```

   This will walk through the installation of the necessary services and packages.


***Changes***
The main change is it now uses MPV to play video. It also allows for rotating the screen if necessary. 
You can change the rotation in display_image_rotated.sh if you don't need it rotated (It's currently set to 270). 
To change the video rotation, edit in the service:
```
sudo systemctl edit --full MarqueeVideo
```
I've also added the ability to send a Shutdown command. 
I'm using this on an RCADE system running on an AtGames Legends Ultimate cabinet. not retropie. As a result, there are some additional scripts I've created that can be triggered at events like shutting down. This way the pi shuts down gracefully when the RCADE is shutdown. 

Notes: Tested originally on Pi5 8GB and videos ran smooth. 
Running on a Pi Zero W and it couldn't handle video, was also slow to start up and switch screens.

