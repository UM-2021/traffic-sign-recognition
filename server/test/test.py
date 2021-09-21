#!C:\Users\jpalg\OneDrive\Desktop\PC\Facultad\TIC5\traffic-sign-recognition\server\test\venv\Scripts\python.exe

# WS client example

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

asyncio.run(hello())
