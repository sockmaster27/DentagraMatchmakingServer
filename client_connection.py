import asyncio
import websockets

import secrets
import time
import math

import tls
import game_server_connection


# token length does not include timestamp
token_length = 64
timeout = 10

NO_MATCH = 4000


unpaired_socket = None


async def new_connection(websocket, path):
    global unpaired_socket

    print("New client connected")

    if unpaired_socket is not None:
        timestamp = math.floor(time.time()).to_bytes(4, "big")
        token1 = secrets.token_bytes(token_length)
        token2 = secrets.token_bytes(token_length)

        await unpaired_socket.send(token1 + timestamp)
        await websocket.send(token2 + timestamp)

        game_server_found = await game_server_connection.send(token1 + token2 + timestamp)

        if game_server_found:
            print("Two clients paired \n")
        else:
            print("No game servers available \n")

        unpaired_socket = None

    else:
        unpaired_socket = websocket
        await asyncio.sleep(timeout)

        if unpaired_socket is websocket:
            unpaired_socket = None
            await websocket.close(code=NO_MATCH)
            print("Client disconnected \n")


ssl = tls.generate_ssl_context()
start = websockets.serve(new_connection, "localhost", 2093, ssl=ssl)
