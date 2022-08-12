import cv2
import os
import keyboard
from imutils.video import VideoStream
import torch
import numpy as np

PATH_LABELS = "\labels" #path for labels
PATH_IMAGES = "\images" #path for images
model = torch.hub.load(r'\yolov5-master', 'custom',
                       path=r'H:\Collect data from video\best.pt', source='local') #Path of your yolov5 master directory + path of your existing (trained) model.
VIDEO_FILE = "4.mkv"    #video you want to apply your model to get dataset
model.cf = 0.25         #setting confidence threshold
model.iou = 0.45        #setting IoU threshold

video = VideoStream(VIDEO_FILE).start()
scale = 1.0
count = 0

def saveFrame(img, count):
    filename = PATH_IMAGES + "\\" +VIDEO_FILE + "_" + str(count) + "_frame.jpg"
    cv2.imwrite(filename, img)
    print("saved " + filename)

def saveLabels(label, count):
    filename = PATH_LABELS + "\\" + VIDEO_FILE + "_" + str(count) + "_frame.txt"
    with open(filename, 'w') as f:
        f.write(str(label))

try:
    if not os.path.exists('pet'):
        os.makedirs('pet')
except OSError:
    print('Error')
currentframe = 0
frame_width = int(cv2.VideoCapture(VIDEO_FILE).get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cv2.VideoCapture(VIDEO_FILE).get(cv2.CAP_PROP_FRAME_HEIGHT))

video = cv2.VideoCapture(VIDEO_FILE)
while True:
    ret, frame = video.read()
    cropped_frame = frame[240:1200, 800:1760]     #Crop video if it's needed
    screenshot = np.array(cropped_frame)
    results = model(screenshot, size=640)         #size should match with model.
    #You can get more information about size at github.com/ultralytics/yolov5
    df = results.pandas().xyxy[0]
    if not df.empty:
        if df.iloc[0, 4]>=0.8:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            #receive bounding box data from the most confidence data from dataframe
            cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            #draw bounding box with received data

            blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
            
            #calculate received data to save as labels
            x_center = round((float(xmin+xmax))/1920,6)
            y_center = round((float(ymin+ymax))/1920,6)
            width = round(float(xmax-xmin)/960,6)
            height = round(float(ymax-ymin)/960,6)
            result = "0 "+str(x_center)+" "+str(y_center)+" "+str(width)+" "+str(height)
            cv2.imshow("Video", screenshot)
            #print(df)  #Optinal: showing predicted data in terminal
           
            inputPressed = cv2.waitKey(0)
            if inputPressed == ord('s'):  #save label of frame if pressing 'S'
                print("saved")
                filename = PATH_IMAGES + "\\" + VIDEO_FILE[0:-4] + "_" + str(count) + "_frame.jpg"
                cv2.imwrite(filename, cropped_frame)
                print("saved " + filename)
                filename = PATH_LABELS + "\\" + VIDEO_FILE[0:-4] + "_" + str(count) + "_frame.txt"
                with open(filename, 'w') as f:
                    f.write(str(result))
                print("saved " + filename)
                count += 1
            if inputPressed == ord('d'):  #skip labeling of frame if pressing 'D'
                print("skip")
            if inputPressed == ord('q'):  #exit by pressing 'Q'
                break
        else:
            print("Looking for object greater confidence")
    else:
        print("Nothing to check")

cv2.destroyAllWindows()
