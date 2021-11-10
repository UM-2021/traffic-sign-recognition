import cv2
import asyncio
import websockets
import requests
import urllib.request
from requests.structures import CaseInsensitiveDict
import numpy as np
import time

import ssar_tsd
import gpscoordenadas


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
    print(headers)
    pload = {'sign': sign, 'coordinates': coords}
    resp = requests.post(
        'http://179.27.97.57:3000/api/signs/locations', json=pload, headers=headers)
    print(resp.status_code)


async def handle_detection(sign, coords):
    if internet_on():
        print("Internet connection established")
        with open('../todo_requests.txt') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for line in lines:
                values = line.split(',')
                if len(values) == 3 and values[0].isnumeric() and values[1].isnumeric() and values[2].isnumeric():
                    await send_sign(line)
                    await send_detection(values[0], [values[1], values[2]])
        open('todo_requests.txt', 'w').close()
        if sign.isnumeric():
            print("Ready to send sign...", sign)
            # await send_sign(sign)
            await send_detection(sign, coords)
    else:
        print("No Internet connection")
        with open('todo_requests.txt', 'a') as the_file:
            the_file.write(sign + ',' + coords[0] + ',' + coords[1] + '\n')

detector = ssar_tsd.TrafficSignDetector()
vidcap = cv2.VideoCapture(0)
labelNames = open("signnames.csv").read().strip().split("\n")[1:]
labelNames = {int(l.split(",")[0]): l.split(",")[1] for l in labelNames}
predictions = np.array([])

print('Predicting...')

detections = np.array([])

while True:
    # print('-------------------------------------------------------------------------')
    time.sleep(0.5)
    success, frame = vidcap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    predictions = np.array(detector.predict(frame))
    print('PREDICTIONS', [p for p in predictions if p in labelNames.keys()])
    print('DETECTIONS', detections)
    detections = np.concatenate([detections, [p for p in predictions if p in labelNames.keys()]])

    # if len(predictions) > 0 and predictions[0] in labelNames.keys():
    #     print(labelNames[predictions[0]])
    # if len(predictions) > 1 and predictions[1] in labelNames.keys():
    #     print(labelNames[predictions[1]])
    # if len(predictions) > 2 and predictions[2] in labelNames.keys():
    #     print(labelNames[predictions[2]])

    # cv2.putText(frame, predictions[0] if len(predictions) > 0 else None, (5, 15), cv2.FONT_HERSHEY_SIMPLEX,
    #             0.5, (255, 0, 255), 2)
    # cv2.imshow('Imagetest', frame)

    if len(predictions) > 0 and all(item in labelNames.keys() for item in predictions):
        lat, lng = gpscoordenadas.getCoords()
        print(lat,lng)

        for p in predictions:
            if p in labelNames.keys() and (detections == p).sum() >= 8:
                print('Send request')
                print(detections)
                print('Send request')
                asyncio.run(handle_detection("1", [0, 0]))
                detections = np.array([])

    predictions = []

    if cv2.waitKey(1) != -1:
        break

vidcap.release()
cv2.destroyAllWindows()
