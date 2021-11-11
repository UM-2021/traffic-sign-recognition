import numpy as np
import os
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
        await websocket.send(sign)

async def send_detection(sign, coords):
    pload = {'sign': sign, 'coordinates': coords}
    requests.post('https://179.27.97.57/signs/location',data = pload)

async def handle_detection(sign, coords):
    if internet_on():
        print("Internet connection established")
        with open('todo_requests.txt') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for line in lines:
                values = line.split(',')
                if values.len() == 3 and values[0].isnumeric() and values[1].isnumeric() and values[2].isnumeric():
                    await send_sign(line)
                    await send_detection(values[0], [values[1], values[2]])
        open('todo_requests.txt', 'w').close()
        if sign.isnumeric() and coords.len() == 2 and coords[0].isnumeric() and coords[1].isnumeric():
            await send_sign(sign)
            await send_detection(sign, coords)
    else:
        print("No Internet connection")
        with open('todo_requests.txt', 'a') as the_file:
            the_file.write(sign + ','+ coords[0] + ',' + coords[1] + '\n')


asyncio.run(handle_detection('2', -4 , -55)) 