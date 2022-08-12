import cv2
import numpy as np
import os

directory = 'input1 frames'

for file in os.listdir(directory):
    filename = os.path.join(directory, file)
    # fileImage = "input2 frames/frame479.jpg"

    image = cv2.imread(filename)

    # img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    ly = np.array([43,186,183])
    uy = np.array([96,253,243])

    gmask = cv2.inRange(image,ly,uy)
    color = cv2.bitwise_and(image,image,mask=gmask)

    pixels = cv2.countNonZero(gmask)
    if pixels > 20:
        cv2.imwrite("input1 frames have yellow/"+str(file), image)
        print("saved "+str(file))
    else:
        print("Nope")
