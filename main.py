import asyncio

import game_server_connection
import client_connection


print("Server started \n")

IP = "192.168.87.120"

asyncio.get_event_loop().run_until_complete(client_connection.create_server(IP, 2093))
asyncio.get_event_loop().run_until_complete(game_server_connection.create_server(IP, 2094))
asyncio.get_event_loop().run_forever()
