import time
import datetime
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

while True:
    start_time = 0
    end_time = 0
    swipe_time_sec = 0
    swipe_time = datetime.datetime.now()
    print("A",swipe_time)
    while(not(swipe_time_sec>1 and swipe_time_sec<3)):
        if mpr121[0].value:
            # start_time = datetime.datetime.now()
        while mpr121[0].value:
            pass
        if mpr121[0].value:
            end_time = datetime.datetime.now()
        swipe_time = end_time - start_time
        print("B",swipe_time)
        swipe_time_sec = swipe_time.total_seconds()
        print("swiped for ", swipe_time_sec)
    print("done")
    time.sleep(0.25)  # Small delay to keep from spamming output messages.