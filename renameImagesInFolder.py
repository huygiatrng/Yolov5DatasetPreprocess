import cv2
import numpy as np
import os

directory = 'inputvideo frames have yellow'
directory2 = 'inputvideo frames have yellow'
directoryOutput = 'inputvideo frames have yellow after named'
count = 0

for file in os.listdir(directory):
    oldname = os.path.join(directory, file)
    newname = os.path.join(directory, str(count)+".jpg")
    os.rename(oldname, newname)
    count+=1
    print("DONE")

for file in os.listdir(directory2):
    oldname = os.path.join(directory2, file)
    newname = os.path.join(directory2, str(count)+".jpg")
    os.rename(oldname, newname)
    count+=1
    print("DONE")
