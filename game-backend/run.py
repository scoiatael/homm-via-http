from time import sleep
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

import asyncio
import aioredis

from io import BytesIO

from config import EXEC, IMG_PUBSUB

LOOP = asyncio.get_event_loop()

class GameLoop:
    def __init__(self, disp, loop=LOOP, pubsub = IMG_PUBSUB):
        self.disp = disp
        self.loop = loop
        self.pubsub = pubsub

    async def go(self):
        self.conn = await aioredis.create_redis(
            ('localhost', 6379))

        while True:
            img = BytesIO()
            screenshot = self.disp.waitgrab()
            print('..Have screenshot of ' + str(len(screenshot.tobytes())))
            screenshot.show()
            screenshot.save(img, format = 'png')
            img.seek(0)
            raw = img.read()
            self.conn.publish(self.pubsub, raw)
            print('..Sending ' + str(len(raw)))
            sleep(1)

        self.conn.close()
        await self.conn.wait_closed()

with SmartDisplay(visible=0, bgcolor='black') as disp:
    with EasyProcess(EXEC):
       LOOP.run_until_complete(GameLoop(disp).go())
