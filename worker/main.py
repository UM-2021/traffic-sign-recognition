import cv2 
import numpy as np
import os
from PIL import Image
from joblib import load
import identify_red
import time
import asyncio
import websockets
import urllib.request
import requests

def internet_on():
    try:
        urllib.request.urlopen('http://google.com') #maybe change this after to our server
        return True
    except:
        return False


async def send_sign(sign):
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        print(sign)
        await websocket.send(sign)

async def send_detection(sign, coords):
    pload = {'sign': sign, 'coordinates': coords}
    requests.post('https://179.27.97.57/signs',data = pload)

async def handle_detection(sign, coords):
    if internet_on():
        print("Internet connection established")
        with open('todo_requests.txt') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for line in lines:
                values = line.split(',')
                if len(values) == 3 and values[0].isnumeric() and values[1].isnumeric() and values[2].isnumeric():
                    await send_sign(line)
                    #await send_detection(values[0], [values[1], values[2]])
        open('todo_requests.txt', 'w').close()
        if sign.isnumeric() and len(coords) == 2 and coords[0].isnumeric() and coords[1].isnumeric():
            print("Ready to send sign...", sign)
            await send_sign(sign)
            #await send_detection(sign, coords)
    else:
        print("No Internet connection")
        with open('todo_requests.txt', 'a') as the_file:
            the_file.write(sign + ','+ coords[0] + ',' + coords[1] + '\n')

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
        #print("\n\nRESULTS:")

        if result_red and predict_prob_red > 0.6: # and predict_prob_red > predict_prob_yellow:
            print("PROB RED PREDICTION: ", predict_prob_red)
            print("RED PREDICTION: ", predict_red)
            # cv2.imshow("image", result_resize_red)
            # cv2.waitKey(0)
            if predict_red== 'PARE':
                asyncio.run(handle_detection('1', ['-4' , '-5']))
            if predict_red == 'CEDA EL PASO':
                print('HERE')
                asyncio.run(handle_detection('2', ['-4' , '-55']))
            if predict_red:
                asyncio.run(handle_detection('2', ['-4' , '-55']))



cam.release()
cv2.destroyAllWindows()
