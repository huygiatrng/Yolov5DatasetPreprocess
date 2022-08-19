import cv2
import os
# from imutils.video import VideoStream
import torch
import numpy as np

INPUT_IMAGES = "E:\dataXin\Collect data from video\inputimages"

ANNOTATED_PATH_LABELS = r"E:\dataXin\Collect data from video\labels"
ANNOTATED_PATH_IMAGES = r"E:\dataXin\Collect data from video\images"
UNANNOTATED_PATH_LABELS = r"E:\dataXin\Collect data from video\Unlabels"
UNANNOTATED_PATH_IMAGES = r"E:\dataXin\Collect data from video\Unimages"

model = torch.hub.load(r'E:\dataXin\Collect data from video\yolov5-master', 'custom',
                       path=r'E:\dataXin\Collect data from video\best2.pt', source='local')
model.conf = 0.73

scale = 1.0
count = 0
currentframe = 0

# def saveFrame(img, count):
#     filename = ANNOTATED_PATH_IMAGES + "\\"+ "img_" + str(count) + "_frame.jpg"
#     cv2.imwrite(filename, img)
#     print("saved " + filename)
#
# def saveLabels(label, count):
#     filename = ANNOTATED_PATH_LABEL + "\\"  + "img_" + str(count) + "_frame.txt"
#     with open(filename, 'w') as f:
#         f.write(str(label))
#
# def saveUnnotated(img,label,count):
#     filename = UNANNOTATED_PATH_IMAGES + "\\" + "img_" + str(count) + "_frame.jpg"
#     cv2.imwrite(filename, img)
#     print("saved "+filename+" as unannotated")
#     filename = UNANNOTATED_PATH_LABELS + "\\" + "img_" + str(count) + "_frame.txt"
#     with open(filename, 'w') as f:
#         f.write(str(label))
#     print("saved " + filename + " as unannotated")
#     pass


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


#
# while True:
#     ret, frame = video.read()
#     cropped_frame = frame[220:860, 640:1280]
#     screenshot = np.array(cropped_frame)
#     results = model(screenshot, size=640)
#     df = results.pandas().xyxy[0]
#     if not df.empty:
#         if df.iloc[0, 4]>=0.8:
#             xmin = int(df.iloc[0, 0])
#             ymin = int(df.iloc[0, 1])
#             xmax = int(df.iloc[0, 2])
#             ymax = int(df.iloc[0, 3])
#             head_level = (int(xmin + (xmax - xmin) / 2), int(ymin + (ymax - ymin) / 8))
#             cv2.circle(screenshot, head_level, 4, (0, 255, 0), thickness=-1)
#             cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
#
#             blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
#
#             x_center = round((float(xmin+xmax))/1920,6)
#             y_center = round((float(ymin+ymax))/1920,6)
#             width = round(float(xmax-xmin)/960,6)
#             height = round(float(ymax-ymin)/960,6)
#             result = "0 "+str(x_center)+" "+str(y_center)+" "+str(width)+" "+str(height)
#             cv2.imshow("Video", screenshot)
#             print(df)
#             inputPressed = cv2.waitKey(0)
#             if inputPressed == ord('s'):
#                 print("saved")
#                 filename = ANNOTATED_PATH_IMAGES + "\\" + VIDEO_FILE[0:-4] + "_" + str(count) + "_frame.jpg"
#                 cv2.imwrite(filename, cropped_frame)
#                 print("saved " + filename)
#                 filename = ANNOTATED_PATH_LABELS + "\\" + VIDEO_FILE[0:-4] + "_" + str(count) + "_frame.txt"
#                 with open(filename, 'w') as f:
#                     f.write(str(result))
#                 print("saved " + filename)
#                 count += 1
#             if inputPressed == ord('d'):
#                 print("deleted")
#             if inputPressed == ord('q'):
#                 break
#         else:
#             print("Looking for object greater confidence")
#     else:
#         print("Nothing to check")
#
# cv2.destroyAllWindows()
