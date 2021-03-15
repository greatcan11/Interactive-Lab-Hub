import time
from time import strftime, sleep
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

pressed = False
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0,0,255))
    print(pressed)
    if not buttonB.value:
        pressed = True
    if not pressed and int(time.time())%2 == 0:
        print("draw red")
        draw.rectangle((0, 0, width, height), outline=0, fill= (255,0,0))  # red
        pressed = True
    # if pressed > 0:
    #     print("draw black")
    #     draw.rectangle((0, 0, width, height), outline=0, fill=0) #black
    #     pressed = 0
    print("after this: ",pressed,"--------------------")
    # Extract Date and Time
    DATE = strftime("%m/%d/%Y")
    TIME = strftime("%H:%M:%S")
    # Write four lines of text.
    y = top
    draw.text((x, y), DATE, font=font, fill="#FFFFFF")
    draw.text((x, y+20), TIME, font=font, fill="#FFFFFF")
    draw.text((x, y+80), str(pressed), font=font, fill="#FFFFFF")
    # time.sleep(1)

    if buttonA.value:
        draw.text((x, y+40), "GO TO SLEEP!", font=font_big, fill="#FFFFFF")
        draw.rectangle((0, 0, width, height), outline=0, fill= (255,0,0)) 
    
    # Display image.
    disp.image(image,rotation)
    time.sleep(1)
