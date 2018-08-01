#!/usr/bin/env python

# Imports
from dotenv import load_dotenv, find_dotenv
import time
import Adafruit_SSD1306
import RPi.GPIO as GPIO
from PIL import Image,ImageFont,ImageDraw
import os

load_dotenv(find_dotenv())

FONT_PATH = os.getenv("FONT_PATH")

# Functions
# Default Functions
def clear_display():
    draw.rectangle((0,0,width,height), outline=0, fill=0)

def display_custom(text, size):
    # Clear image buffer by drawing a black filled box
    clear_display()

    # Set font type and size
    fontsize = size if size else 8 
    font = ImageFont.truetype(FONT_PATH, fontsize)
        
    # Position SSID
    x_pos = (width/2) - (string_width(font,text)/2)
    y_pos = (height/2) - (8/2)

    # Draw SSID
    draw.text((x_pos, y_pos), text, font=font, fill=255)

    # Draw the image buffer
    disp.image(image)
    disp.display()

def string_width(fonttype,string):
    string_width = 0

    for i, c in enumerate(string):
        char_width, char_height = draw.textsize(c, font=fonttype)
        string_width += char_width

    return string_width

# Display Functions
def display_time():
    # Get the Current date and time
    if (time_format):
        current_time = time.strftime("%H:%M")
    else:
        current_time = time.strftime("%I:%M")

    current_date = time.strftime("%a %m/%d/%Y")

    # Empty screen
    clear_display()

    # Font and Size
    font = ImageFont.truetype(FONT_PATH, 16)

	# Position time
    x_pos = (disp.width/1.5)-(string_width(font,current_time))
    y_pos = 2 + (disp.height-2)/2 - (35/2)

    # Draw Time
    draw.text((x_pos, y_pos), current_time, font=font, fill=255)

	# Set font type and size
    font = ImageFont.truetype(FONT_PATH, 8)

	# Position date
    x_pos = (disp.width/2)-(string_width(font,current_date)/2)
    y_pos = disp.height-10

	# Draw date
    draw.text((x_pos, y_pos), current_date, font=font, fill=255)

	# Draw the image buffer
    disp.image(image)
    disp.display()

def display_network():
    # Collect network information by parsing command line outputs
    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    netmask = os.popen("ifconfig wlan0 | grep 'Mask' | awk -F: '{print $4}'").read()
    gateway = os.popen("route -n | grep '^0.0.0.0' | awk '{print $2}'").read()
    ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()

    clear_display()

    # Begin SSID
    font = ImageFont.truetype(FONT_PATH, 12)

    # Position SSID
    x_pos = 2
    y_pos = 2

    # Draw SSID
    draw.text((x_pos, y_pos), ssid, font=font, fill=255)
	
    # Set font type and size
    font = ImageFont.truetype(FONT_PATH, 8)

    # End SSID
    # Begin IP

    # Position IP
    y_pos += 12 + 10 
        
    # Draw IP
    draw.text((x_pos, y_pos), "IP: "+ipaddress, font=font, fill=255)

    # End IP
    # Begin Network Mask

	# Position NM
    y_pos += 10 

	# Draw NM
    draw.text((x_pos, y_pos), "NM: "+netmask, font=font, fill=255)

    # End Network Mask
    # Begin Gateway

	# Position GW
    y_pos += 10

	# Draw GW
    draw.text((x_pos, y_pos), "GW: "+gateway, font=font, fill=255)
	
    # End Gateway

	# Draw the image buffer
    disp.image(image)
    disp.display()

# End Functions

# GPIO Setup
# Set up GPIO with internal pull-up
GPIO.setmode(GPIO.BCM)	
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 128x32 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_32(rst=24)

# Initialize Display
disp.begin()

# Get display width and height
width = disp.width
height = disp.height

# Clear display
disp.clear()
disp.display()

# Create image buffer with mode '1' for 1-bit color
image = Image.new('1', (width, height))

# Load default font
font = ImageFont.load_default()

# Create drawing object
draw = ImageDraw.Draw(image)

prev_millis = 0
display = 0
time_format = True

# Program Loop
while True:
    millis = int(round(time.time() * 1000))

	# Software debouncing
    if((millis - prev_millis) > 250):
        # Cycle through different displays
        if(not GPIO.input(12)):
            display += 1
            if(display > 2):
                display = 0
            prev_millis = int(round(time.time() * 1000))

	# Trigger action based on current display
        elif(not GPIO.input(16)):
            if(display == 0):
	    # Toggle between 12/24h format
                time_format = not time_format
                time.sleep(0.01)
            elif(display == 1):
	    # Reconnect to network
                display_custom("reconnecting wifi ...")
                os.popen("sudo ifdown wlan0; sleep 5; sudo ifup --force wlan0")
                time.sleep(0.01)
            prev_millis = int(round(time.time() * 1000))


    if(display == 0):
        display_time()
    elif(display == 1):
        display_network()
    elif(display == 2):
        display_custom("chicken dinner", 14)

    time.sleep(0.1)
