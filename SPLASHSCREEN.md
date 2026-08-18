These files are for a Plymouth dual-screen splash screen with a custom synthwave theme
* BitLCD shows horizontal marquee splash image
* Waveshare shows vertical control map splash image
* Animated progress circle in the overlap zone between displays


https://github.com/user-attachments/assets/30cc3333-d8f2-4143-8955-b015cfc9aaa3




# Plymouth Theme Installation Guide
Follow these steps to install and configure the custom boot splash theme.

## 1. Install Plymouth Prerequisites
Make sure the base Plymouth packages are installed.
    
```
sudo apt update
sudo apt install plymouth plymouth-themes
```

## 2. Transfer the Theme Files
Copy the theme folder (`dual-splash`) into the system's Plymouth themes directory. The folder name should exactly match the name of the `.plymouth` configuration file inside it.

```
sudo cp -r /home/<USERNAME>/installfiles/bin/plymouth/themes/dual-splash /usr/share/plymouth/themes/
```

## 3. Set the Theme and Rebuild initramfs
Use the Plymouth command-line tool to set the new theme as the default. The `-R` flag is critical as it rebuilds the initial ramdisk (initramfs) to include your theme assets during early boot.

```
sudo plymouth-set-default-theme -R dual-splash
```

## 4. Configure the Boot Parameters
The Raspberry Pi needs specific boot parameters to suppress standard text output and trigger Plymouth. 
    
Depending on the OS version, this file is located at `/boot/firmware/cmdline.txt` (Bookworm and newer) or `/boot/cmdline.txt` (Bullseye and older). Open the file in a text editor:

```
sudo nano /boot/firmware/cmdline.txt
```

Append the following parameters to the **end of the existing line**. It must remain a single, unbroken line of text (it may already be there in a different order):
    
```
splash quiet plymouth.ignore-serial-consoles
```
    
Save and exit (in Nano, press `Ctrl+O`, `Enter`, then `Ctrl+X`).

## 5. Reboot to Test
Restart the Raspberry Pi to verify the custom splash screen renders correctly during the boot sequence.

```
sudo reboot
```

---
[Back to main Readme](README.md)
