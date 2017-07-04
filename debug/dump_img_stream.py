import asyncio
import aioredis

import subprocess

PUBSUB = 'img_pubsub'
FILENAME = 'tmp/screenshot.png'

LOOP  = asyncio.get_event_loop()

async def go():
    conn = await aioredis.create_redis(
        ('localhost', 6379))
    sub, = await conn.subscribe(PUBSUB)
    while True:
        img = await sub.get()
        if img is None:
            break
        with open(FILENAME, 'wb') as f:
            f.write(img)
        print('.. ' + FILENAME + ': ' + str(len(img)))
        subprocess.call(['display', FILENAME])

    conn.close()
    await conn.wait_closed()

LOOP.run_until_complete(go())
