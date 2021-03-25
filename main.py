import websockets
import asyncio

import secrets
import time
import math


# token length does not include timestamp
token_length = 64
timeout = 10


unpaired_socket = None


async def hello(websocket, path):
    global unpaired_socket

    if unpaired_socket is not None:

        timestamp = bytes(math.floor(time.time()))
        token1 = secrets.token_bytes(token_length)
        token2 = secrets.token_bytes(token_length)

        await unpaired_socket.send(token1 + timestamp)
        await websocket.send(token2 + timestamp)
        # TODO: game_server.send(token1 + token2 + timestamp)

        unpaired_socket = None

    else:
        unpaired_socket = websocket
        await asyncio.sleep(timeout)
        if unpaired_socket == websocket:
            unpaired_socket = None


start_server = websockets.serve(hello, "localhost", 2093)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
