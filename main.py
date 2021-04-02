import asyncio

import game_server_connection
import client_connection


print("Server started \n")

asyncio.get_event_loop().run_until_complete(client_connection.start)
asyncio.get_event_loop().run_until_complete(game_server_connection.start)
asyncio.get_event_loop().run_forever()
