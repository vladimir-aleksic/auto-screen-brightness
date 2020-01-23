#!/bin/bash

if [ "$1" -gt 0 ] && [ "$1" -lt 256 ]
then
	echo "$1" | sudo tee /sys/class/backlight/radeon_bl0/brightness > /dev/null
fi
