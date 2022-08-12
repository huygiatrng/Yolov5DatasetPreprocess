import cv2
import numpy as np
import os

directory = 'inputvideo frames'             #directory of frames

for file in os.listdir(directory):
    filename = os.path.join(directory, file)

    image = cv2.imread(filename)

    ly = np.array([43,186,183])         #low value of color in BGR (not RGB) format - default Yellow
    uy = np.array([96,253,243])         #high value of color in BGR (not RGB) format - default Yellow

    gmask = cv2.inRange(image,ly,uy)
    color = cv2.bitwise_and(image,image,mask=gmask)

    pixels = cv2.countNonZero(gmask)
    if pixels > 20:                     #threshold number of pixel
        cv2.imwrite("input1 frames have yellow color/"+str(file), image)
        print("Saved "+str(file))
    else:
        print("Skipped")
