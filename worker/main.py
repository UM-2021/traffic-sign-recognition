import cv2 
import numpy as np
import os
from PIL import Image
from joblib import load
import identify_red
import time
import asyncio
import websockets

async def send_sign(sign):
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        signdetected = sign
        await websocket.send(signdetected)

# Time (seconds) to wait to extract the frames
TIME_WINDOW = 1

# Craetes a directory to store frames, relative to the script path. 
cwd = os.path.dirname(os.path.realpath(__file__))
image_directory = cwd + '/image-directory'
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# Initialize the video
cam = cv2.VideoCapture(0)

# Extracting process
start_time = time.process_time()
while True:
    ret, image = cam.read()
    cv2.imshow('Imagetest', image)
    k = cv2.waitKey(1)
    if k != -1:
        break

    time_difference = time.process_time() - start_time
    if time_difference > TIME_WINDOW:
        start_time = time.process_time()
        cv2.imwrite(image_directory + '/image-to-process.jpg', image)
        result_red = identify_red.identify(image)
        if result_red:
            result_resize_red = result_red[0]
            predict_prob_red= result_red[1]
            predict_red= result_red[2]
        print("\n\nRESULTS:")

        if result_red and predict_prob_red > 0.5: # and predict_prob_red > predict_prob_yellow:
            print("PROB RED PREDICTION: ", predict_prob_red)
            print("RED PREDICTION: ", predict_red)
            # cv2.imshow("image", result_resize_red)
            # cv2.waitKey(0)
            if predict_red == 'PARE':
                asyncio.run(send_sign())
            if predict_red == 'CEDA EL PASO':
                asyncio.run(send_sign())

cam.release()
cv2.destroyAllWindows()
