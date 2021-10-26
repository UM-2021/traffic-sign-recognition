# WS client example

import asyncio
import websockets
import urllib.request

async def send_sign():
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        sign = "2"
        await websocket.send(sign)

# asyncio.run(send_sign())



def internet_on():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False
print (internet_on())
