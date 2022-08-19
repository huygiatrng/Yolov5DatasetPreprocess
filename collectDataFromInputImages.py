import cv2
import os
import torch
import numpy as np

# Input images directory
INPUT_IMAGES = "inputimages"

ANNOTATED_PATH_LABELS = "labels"
ANNOTATED_PATH_IMAGES = "images"
UNANNOTATED_PATH_LABELS = "Unlabels"
UNANNOTATED_PATH_IMAGES = "Unimages"

dir_path = os.path.dirname(os.path.realpath(__file__))
outputDir = [ANNOTATED_PATH_LABELS,ANNOTATED_PATH_IMAGES,UNANNOTATED_PATH_LABELS,UNANNOTATED_PATH_IMAGES]
for dir in outputDir:
  dirPath = os.path.join(dir_path,dir)
  if os.path.exists(dirPath):
    os.mkdir(dirPath)   

# Load existing model
model = torch.hub.load(r'yolov5-master', 'custom',
                       path=r'best.pt', source='local') 
# Confidence setting
model.conf = 0.73

scale = 1.0
count = 0
currentframe = 0

for filename in os.listdir(INPUT_IMAGES):
    f = os.path.join(INPUT_IMAGES, filename)
    img = cv2.imread(f)
    screenshot = np.array(img)
    results = model(screenshot, size=640)

    df = results.pandas().xyxy[0]
    if not df.empty:
        result = ""
        for i in range(df.shape[0]):
            xmin = int(df.iloc[i, 0])
            ymin = int(df.iloc[i, 1])
            xmax = int(df.iloc[i, 2])
            ymax = int(df.iloc[i, 3])
            x_center = round(float(xmin + xmax)/1280, 6)
            y_center = round(float(ymin+ymax)/1280,6)
            width = round(float(xmax-xmin)/640,6)
            height = round(float(ymax-ymin)/640,6)
            result += "0 "+str(x_center)+" "+str(y_center)+" "+str(width)+" "+str(height) +"\n"

        filename = ANNOTATED_PATH_IMAGES + "\\" + "img_" + str(count) + "_frame.jpg"
        cv2.imwrite(filename, screenshot)
        print("saved " + filename + " as annotated")

        filename = ANNOTATED_PATH_LABELS + "\\" + "img_" + str(count) + "_frame.txt"
        with open(filename, 'w') as fn:
            fn.write(str(result))
        print("saved " + filename + " as annotated")
        count += 1
    else:
        filename = UNANNOTATED_PATH_IMAGES + "\\" +  "img_" + str(count) + "_frame.jpg"
        cv2.imwrite(filename, screenshot)
        print("saved " + filename + " as unannotated")

        filename = UNANNOTATED_PATH_LABELS + "\\" + "img_" + str(count) + "_frame.txt"
        with open(filename, 'w') as fn:
            fn.write("")
        print("saved " + filename + " as unannotated")
        count += 1
