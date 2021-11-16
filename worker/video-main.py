import cv2
import os
import identify_red
import time
import asyncio
import websockets
import requests
import urllib.request

from utils import gpscoordenadas
import time
from requests.structures import CaseInsensitiveDict


def internet_on():
    try:
        # maybe change this after to our server
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False


async def send_sign(sign):
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        # print(sign)
        await websocket.send(sign)


async def send_detection(sign, coords):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxN2UxYjQ2YjNkY2U4YTFlMjE1NDRlMiIsImlhdCI6MTYzNjM5OTQyNCwiZXhwIjoxNjQ0MTc1NDI0fQ.gsff9f7Vh6Ff1OFchK-Gp-2zXbhj1cN-OAsyip1353Y"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"
    pload = {'sign': sign, 'coordinates': coords}
    resp = requests.post(
        'http://179.27.97.57:3000/api/signs/locations', data=pload, headers=headers)
    print(resp.status_code)


async def handle_detection(sign, coords):
    if internet_on():
        print("Internet connection established")
        with open('todo_requests.txt') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for line in lines:
                values = line.split(',')
                if len(values) == 3 and values[0].isnumeric() and values[1].isnumeric() and values[2].isnumeric():
                    # await send_sign(line)
                    await send_detection(values[0], [values[1], values[2]])
        open('todo_requests.txt', 'w').close()
        if sign.isnumeric():
            print("Ready to send sign...", sign)
            await send_sign(sign)
            await send_detection(sign, coords)
    else:
        print("No Internet connection")
        with open('todo_requests.txt', 'a') as the_file:
            the_file.write(sign + ',' + coords[0] + ',' + coords[1] + '\n')

# Time (seconds) to wait to extract the frames
TIME_WINDOW = 1

# Craetes a directory to store frames, relative to the script path.
cwd = os.path.dirname(os.path.realpath(__file__))
image_directory = cwd + '/image-directory'
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# Initialize the video
cam = cv2.VideoCapture('./data/my_test_set/v-ejemplo.mp4')  # /home/pi/traffic-sign-recognition/worker/data/my_test_set/v-ejemplo.mp4

try:
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

# if not created then raise error
except OSError:
    print('Error: Creating directory of data')

currentframe = 0

# Extracting process
start_time = time.process_time()
while True:
    ret, image = cam.read()
    # cv2.imshow('Imagetest', image)
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
            predict_prob_red = result_red[1]
            predict_red = result_red[2]
        print("\n\nRESULTS:")

        # and predict_prob_red > predict_prob_yellow:
        if result_red and predict_prob_red > 0.6:
            print("PROB RED PREDICTION: ", predict_prob_red)
            print("RED PREDICTION: ", predict_red)
            cv2.imshow("image", result_resize_red)
            cv2.waitKey(0)
            if False: # Dead code for now.
                if predict_red == 'PARE':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('1', [lat, lng]))
                if predict_red == 'CEDA EL PASO':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('2', [lat, lng]))
                if predict_red == 'SEÑAL DE VELOCIDAD DE 30 km/h':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('1', [lat, lng]))
                if predict_red == 'SEÑAL DE VELOCIDAD DE 60 km/h':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('3', [lat, lng]))
                if predict_red == 'SEÑAL DE VELOCIDAD DE 90 km/h':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('6', [lat, lng]))
                if predict_red == 'SEÑAL DE VELOCIDAD DE 110 km/h':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('7', [lat, lng]))
                if predict_red == '_NO SOBREPASAR':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('8', [lat, lng]))
                if predict_red == 'CONTRAMANO':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('12', [lat, lng]))
                if predict_red == 'TERRENO RESBALADIZO':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('21', [lat, lng]))
                if predict_red == 'CIERRE CARRIL':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('22', [lat, lng]))
                if predict_red == 'CUIDADO BICICLETAS':
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('26', [lat, lng]))
                if predict_red:
                    lat, lng = gpscoordenadas.getCoords()
                    # print(lat,lng)
                    asyncio.run(handle_detection('2', [lat, lng]))


cam.release()
cv2.destroyAllWindows()
