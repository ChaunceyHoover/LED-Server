# WS server that sends messages at random intervals

import asyncio
import websockets
import json
import time
import threading

from rpi_ws281x import Color, PixelStrip, ws

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.SK6812W_STRIP
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

async def socket(websocket, path):
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        col = Color(int(data[1]), int(data[2]), int(data[3]), int(data[4]))
        strip.setPixelColor(int(data[0]), col)

def updateLEDs():
    while True:
        strip.show()

start_server = websockets.serve(socket, "0.0.0.0", 5678)
print('serving on port 5678')

threading.Thread(target=updateLEDs).start()
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()