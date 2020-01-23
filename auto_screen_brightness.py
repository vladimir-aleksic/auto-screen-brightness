#!/usr/bin/env python3

import os
import sys
import math
from time import sleep
from PIL import Image, ImageStat

CHECK_INTERVAL = 10         # update brightness every CHECK_INTERVAL seconds
STEP = 1                    # amount to increase brightness in every smoothing cycle
SMOOTH = True               # enable gradual change to new brightness
SMOOTH_CYCLE = 0.015        # how long does every smoothing cycle last
THRESHOLD = 10              # how much brightness has to change to trigger an update
 
IMAGE_NAME = ".image.jpeg"  # image from webcam that's analyzed
MIN_VAL = 35.0              # min screen brightness [0-255]
MAX_VAL = 255.0             # max screen brightness [0-255]
SCALING_FACTOR = 1.3        # an arbitrary scaling factor used for adjusting the brightness
current_brightness = 0


def screen_auto_brightness():
    try:
        while True:
            os.system("streamer -f jpeg -o {} 2> /dev/null".format(IMAGE_NAME))
            brightness = get_img_brigthness(IMAGE_NAME)
            brightness *= SCALING_FACTOR
            
            if SMOOTH:
                smooth_duration = smooth(brightness)
                if smooth_duration < CHECK_INTERVAL:
                    sleep(CHECK_INTERVAL - smooth_duration)
            else:
                no_smooth(brightness)
                sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        pass

    os.remove(IMAGE_NAME)


# Slowly transition to new brightness
def smooth(new_brightness):
    global current_brightness
    new_brightness = constraint(new_brightness)
    duration = 0

    # do we have to increase or decrease current brightness?
    step = int(math.copysign(abs(STEP), new_brightness - current_brightness))

    # brightness fluctuation caused by slight movements are possible
    # check if we should even change brightness depending on the THRESHOLD
    if abs(new_brightness - current_brightness) < THRESHOLD:
        return 0

    if step == 0:
        return 0

    while True:        
        # increasing brightness finished?
        if step > 0 and current_brightness >= new_brightness:
            break

        # decreasing brightness finished?
        if step < 0 and current_brightness <= new_brightness:
            break

        current_brightness = constraint(current_brightness + step)
        set_brightness(current_brightness)
        
        sleep(SMOOTH_CYCLE)
        duration += SMOOTH_CYCLE

    return duration


# Change the brightness without any smoothing
def no_smooth(new_brightness):
    global current_brightness
    new_brightness = constraint(new_brightness)

    if abs(new_brightness - current_brightness) < THRESHOLD:
        return 0

    current_brightness = new_brightness
    set_brightness(current_brightness)


def set_brightness(num):
    os.system("sudo ./set_brightness.sh {} > /dev/null".format(int(num)))


# Keep val in range [MIN_VAL, MAX_VAL]
def constraint(val):
    return int(max(min(MAX_VAL, int(val)), MIN_VAL))


# Calculate brightness of the image taken by the webcam
def get_img_brigthness(img_file):
   im = Image.open(img_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))


if __name__ == "__main__":        
    screen_auto_brightness()
