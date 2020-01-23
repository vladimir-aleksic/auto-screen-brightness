# Screen Brightness Auto-Adjuster
A python script that automatically adjusts screen brightness based on webcam data.

## Features
Automatically adjusts screen brightness based on webcam data. A threshold can be set so brightness update doesn't trigger on slight movements as that can change the amount of light webcam receives. Brightness changes can be smooth or snappy. You can also set minimum and maximum brightness.

## Installation
This will work on laptops that run Linux. Download this repository, extract it and place the extracted folder where you want, but after finishing this setup you won't be able to move the folder (the script will stop working).

### Locating backlight configuration file
You will have to find path to the configuration file that controls your screen brightness. Navigate to `/sys/class/backlight`. You will probably find a folder in there *(or a symlink)*. Enter that folder and you should see a file named brightness. Now copy the whole path `/sys/class/backlight/YOUR_FOLDER/brightness`, paste it into `screen_brightness.sh`, replacing the path that is already there. Save and exit. If you find multiple folders in `/sys/class/backlight`, try every one of them and see what works for you.

### Adjusting privileges
`set_brightness.sh` has to be run as root and to avoid typing password every time, run these commands:
```bash
sudo chown root:root ./set_brightness.sh
sudo chmod 755 ./set_brightness.sh
sudo visudo
```
Go to the **bottom** and enter:
```
YOUR_USERNAME   ALL=(root) NOPASSWD: PATH_TO_SCRIPT_FOLDER/set_brightness.sh
```
Replace `YOUR_USERNAME` with your regular username and `PATH_TO_SCRIPT_FOLDER` with the absolute path to the script folder you extracted (for example, /home/vladimir/scripts/autoscreen/set_brightness.sh). Press Ctrl+X, then Y, then Enter.

## Usage
To run the script, open up terminal, navigate to the script folder and run the following:
```bash
./auto_screen_brightness.py &
disown
```

## Licence
You can edit this code and release modifications but under the same licence and copyright notice, with the source code disclosed.

GNU GPLv3 &copy; Vladimir Aleksić