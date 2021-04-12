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
NO_SERVER = 4001


unpaired_socket = None


async def new_connection(websocket, path):
    global unpaired_socket

    print("New client connected")

    if unpaired_socket is not None:
        timestamp = math.floor(time.time()).to_bytes(length=4, byteorder="little", signed=False)
        token1 = secrets.token_bytes(token_length)
        token2 = secrets.token_bytes(token_length)

        game_server_found, address = await game_server_connection.send(token1 + token2 + timestamp)

        if not game_server_found:
            print("No game servers available \n")

            await unpaired_socket.close(code=NO_SERVER)
            await websocket.close(code=NO_SERVER)
        else:
            print("Two clients paired \n")

            address_bytes = address.encode("utf-8")

            await unpaired_socket.send(token1 + timestamp + address_bytes)
            await websocket.send(token2 + timestamp + address_bytes)

        unpaired_socket = None

    else:
        unpaired_socket = websocket
        await asyncio.sleep(timeout)

        if unpaired_socket is websocket:
            unpaired_socket = None
            await websocket.close(code=NO_MATCH)
            print("Client disconnected \n")


def create_server(host: str, port: int):
    ssl = tls.generate_ssl_context()
    return websockets.serve(new_connection, host, port, ssl=ssl)
