import time
from time import strftime, sleep
import datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image,rotation)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

# setup backlight and buttons
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Get bedtime from user input
month, day, year = map(int, time.strftime("%m %d %Y").split())
bedtime_hr, bedtime_min = input('Type in your bedtime: ').split(":")
bedtime = datetime.datetime(year, month, day, int(bedtime_hr), int(bedtime_min), 0)

# Store some value in time user has gone to sleep temporarily 
sleeptime = bedtime

# Store whether "Cleart Alter" button has been pressed
pressed = False

while True:
    # Update variables once "Clear Alert" has been pressed
    if not buttonB.value:
        pressed = True
        sleeptime = datetime.datetime()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0,0,0))

    # Flash red if alert hasn't been cleared
    if not pressed and int(time.time())%2 == 0:
        draw.rectangle((0, 0, width, height), outline=0, fill= (255,0,0))  # red
        
    # Extract Date and Time
    DATE = strftime("%m/%d/%Y")
    TIME = strftime("%H:%M:%S")

    # Calculate difference in times for timer
    difference = bedtime - datetime.datetime.now()
    difference_split = divmod(difference.total_seconds(),60)
    if difference_split[0]>=0:
        DIFFERENCE = str(int(difference_split[1])) + " sec till bedtime"
    else:
        new_difference = datetime.datetime.now() - bedtime
        new_difference_split = divmod(new_difference.total_seconds(),60)
        DIFFERENCE = str(int(new_difference_split[1])) + " sec after bedtime"


    # Write other text
    y = top
    draw.text((x, y), DATE, font=font, fill=(255,255,255))
    draw.text((x+110, y), TIME, font=font_big, fill=(255,255,255))

    # After clearing alert (and going to sleep)
    if pressed:
        sleep_difference = datetime.datetime.now() - sleeptime
        sleep_split = divmod(sleep_difference.total_seconds(),60)
        draw.text((x+75, y), SLEEP, font=font, fill=(255,255,255))
        SLEEP = str(int(new_difference_split[1])) + " sec of sleeping"
        draw.text((x+75, y), SLEEP, font=font, fill=(255,255,255))

    # Before bedtime
    else:
        difference = bedtime - datetime.datetime.now()
        difference_split = divmod(difference.total_seconds(),60)
        if difference_split[0]>=0:
            DIFFERENCE = str(int(difference_split[1])) + " sec till bedtime"

        # After bedtime (but before sleeping)
        else:
            new_difference = datetime.datetime.now() - bedtime
            new_difference_split = divmod(new_difference.total_seconds(),60)
            DIFFERENCE = str(int(new_difference_split[1])) + " sec after bedtime"
            draw.text((x, y+95), "<-- Clear Alert", font=font, fill=(255,255,255))   
            if buttonA.value:
                draw.text((x, y+25), "<-- Show Alert", font=font, fill=(255,255,255))
            else:
                draw.text((x, y+40), "GO TO SLEEP!", font=font_big, fill=(255,255,255))
        
        draw.text((x+75, y), DIFFERENCE, font=font, fill=(255,255,255))
    
    # Display image.
    disp.image(image,rotation)
    time.sleep(1)
