import matplotlib.pyplot as plt
import random
import numpy as np
import imageio

# Function to determine if an image would be "red"
def is_red(img):
    i = imageio.imread(img)
    min_R = np.amin(i[:,:,0], axis = 0)
    if(np.amin(min_R) > 15):
        print("The ",img, "picture has red.")
    else:
        print("The ",img, "picture does not have red.")

# Sample images
is_red('red.jpg')
is_red('pink.jpg')
is_red('blue.jpg')
