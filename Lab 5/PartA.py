import matplotlib.pyplot as plt
import random
import numpy as np
import imageio

# Function to determine if an image would be "red"
def is_red(img):
    i = imageio.imread(img)
    red = i[:,:,0]
    min_red = np.amin(red, axis = 0)
    max_red = np.amax(np.amax(red), axis = 0)
    avg_red = np.average(np.average(red, axis = 0))
    if(np.amin(min_red) > 15):
        print("The ",img, "picture has a red tint.", end ='')
    else:
        print("The ",img, "picture does not have a red tint.", end ='')
    print("The average pixel value for red is ", int(avg_red),"and the highest value is ",max_red,".")

# Sample images
is_red('red.jpg')
is_red('pink.jpg')
is_red('blue.jpg')
