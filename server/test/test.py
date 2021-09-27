#!C:\Users\jpalg\OneDrive\Desktop\PC\Facultad\TIC5\traffic-sign-recognition\server\test\venv\Scripts\python.exe

# WS client example

import asyncio
import websockets


async def send_sign():
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        sign = "2"
        await websocket.send(sign)

asyncio.run(send_sign())
