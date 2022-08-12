import cv2
import os
import keyboard
from imutils.video import VideoStream
import torch
import numpy as np

PATH_LABELS = "H:\Collect data from video\labels"
PATH_IMAGES = "H:\Collect data from video\images"
model = torch.hub.load(r'H:\Collect data from video\yolov5-master', 'custom',
                       path=r'H:\Collect data from video\best.pt', source='local')
VIDEO_FILE = "4.mkv"
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
    cropped_frame = frame[240:1200, 800:1760]
    screenshot = np.array(cropped_frame)
    results = model(screenshot, size=640)
    df = results.pandas().xyxy[0]
    if not df.empty:
        if df.iloc[0, 4]>=0.8:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            head_level = (int(xmin + (xmax - xmin) / 2), int(ymin + (ymax - ymin) / 8))
            cv2.circle(screenshot, head_level, 4, (0, 255, 0), thickness=-1)
            cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

            blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)

            x_center = round((float(xmin+xmax))/1920,6)
            y_center = round((float(ymin+ymax))/1920,6)
            width = round(float(xmax-xmin)/960,6)
            height = round(float(ymax-ymin)/960,6)
            result = "0 "+str(x_center)+" "+str(y_center)+" "+str(width)+" "+str(height)
            cv2.imshow("Video", screenshot)
            print(df)
            inputPressed = cv2.waitKey(0)
            if inputPressed == ord('s'):
                print("saved")
                filename = PATH_IMAGES + "\\" + VIDEO_FILE[0:-4] + "_" + str(count) + "_frame.jpg"
                cv2.imwrite(filename, cropped_frame)
                print("saved " + filename)
                filename = PATH_LABELS + "\\" + VIDEO_FILE[0:-4] + "_" + str(count) + "_frame.txt"
                with open(filename, 'w') as f:
                    f.write(str(result))
                print("saved " + filename)
                count += 1
            if inputPressed == ord('d'):
                print("deleted")
            if inputPressed == ord('q'):
                break
        else:
            print("Looking for object greater confidence")
    else:
        print("Nothing to check")

cv2.destroyAllWindows()
