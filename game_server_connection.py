import websockets
import os

import tls


game_servers = []


def connection_closed(websocket):
    game_servers.remove(websocket)
    print(f"Game server disconnected. {len(game_servers)} game server(s) currently connected. \n")


async def new_connection(websocket, path):
    game_servers.append(websocket)
    print(f"New game server connected. {len(game_servers)} game server(s) currently connected. \n")

    try:
        await websocket.recv()
    except websockets.exceptions.ConnectionClosed:
        connection_closed(websocket)


async def send(data: bytes) -> bool:
    if len(game_servers) == 0:
        return False
    else:
        # Her ville den optimale server skulle findes
        await game_servers[0].send(data)
        return True

client_cert = os.path.join("TLS", "game_server_cert.pem")
# TODO: godkend kun servere med dette certifikat
ssl = tls.generate_ssl_context()
start = websockets.serve(new_connection, "localhost", 2094, ssl=ssl)
