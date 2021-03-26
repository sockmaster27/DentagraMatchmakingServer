import websockets
import ssl
import asyncio

import secrets
import time
import math
import os


# token length does not include timestamp
token_length = 64
timeout = 10

NO_MATCH = 4000

certificate_path = os.path.join("TLS", "tls_certificate.pem")
key_path = os.path.join("TLS", "tls_key.key")


unpaired_socket = None


def generate_ssl_context() -> ssl.SSLContext:
    if not os.path.exists(key_path):
        raise OSError(
            f"{key_path} does not exist. Please generate new certificate, or request a copy from project owners."
        )

    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certificate_path, key_path)
        return ssl_context


async def hello(websocket, path):
    global unpaired_socket

    if unpaired_socket is not None:
        timestamp = math.floor(time.time()).to_bytes(4, "big")
        token1 = secrets.token_bytes(token_length)
        token2 = secrets.token_bytes(token_length)

        await unpaired_socket.send(token1 + timestamp)
        await websocket.send(token2 + timestamp)
        # TODO: game_server.send(token1 + token2 + timestamp)

        unpaired_socket = None

    else:
        unpaired_socket = websocket
        await asyncio.sleep(timeout)

        if unpaired_socket is websocket:
            unpaired_socket = None
            await websocket.close(code=NO_MATCH)

ssl = generate_ssl_context()
start_server = websockets.serve(hello, "localhost", 2093, ssl=ssl)


if __name__ == "__main__":
    print("Server started")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
