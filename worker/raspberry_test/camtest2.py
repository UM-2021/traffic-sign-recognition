#!/usr/bin/env python3

import cv2
import math

videoFile = "capture.avi"
imagesFolder = "/home/pi/tsr/worker/images"
cap = cv2.VideoCapture("/home/pi/Videos/vlc-record-2021-09-06-18h55m12s-Converting v4l2___-.avi")
#cap = cv2.VideoCapture(0)
frameRate = cap.get(5) #frame rate
while (cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
        cv2.imwrite(filename, frame)
cap.release()
print("Done!")