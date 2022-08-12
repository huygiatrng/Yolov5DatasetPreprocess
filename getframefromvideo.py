import cv2

vidcap = cv2.VideoCapture('inputvideo.mp4')
success,image = vidcap.read()
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
count = 0
countToName = 0
while success:
  if count >=10 :
#     cropped_frame = image[220:860,640:1280] #Optional: Crop frame if needed
    cv2.imwrite("input2 frames/frame%d.jpg" % countToName, cropped_frame)     # save frame as JPEG file
    print('Progress: '+str(countToName)+"/"+str(int(length/10)))
    countToName += 1
    count = 0
  success, image = vidcap.read()
  count += 1
  print(count)
