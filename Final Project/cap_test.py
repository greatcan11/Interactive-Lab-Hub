import time
import board
import busio

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
num = 0

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Banana {i} touched! ", num)
            num = num + 1
    time.sleep(0.25)  # Small delay to keep from spamming output messages.