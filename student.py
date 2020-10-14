import asyncio
import getpass
import json
import os
import math

import websockets
from mapa import Map

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg)

        # You can create your own map representation or use the game representation:
        mapa = Map(game_properties["map"])
        print(mapa)

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game state, this must be called timely or your game will get out of sync with the server

                print(state)

                print(type(mapa))

                boxes = state['boxes']
                print(boxes)

                map_pos = map_matrix(mapa)

                print(map_pos)

                print(is_dead_end([1,5], map_pos))

                # import pprint
                # pprint.pprint(state)
                
                key = "d"

                if state['keeper'] == [4,3]:
                    key = "a"

                # print(Map(f"levels/{state['level']}.xsb"))
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

def map_matrix(mapa):
    map_pos = []
    map_rows = str(mapa).split('\n')
    length = len(map_rows[0])
    for i in range(length):
        map_row = []
        for row in map_rows:
            map_row.append(row[i])
        map_pos.append(map_row)
    return map_pos

def is_dead_end(caixa, map_pos):
    caixa_x = caixa[0]
    caixa_y = caixa[1]
    wall_counter = 0

    if map_pos[caixa_x-1][caixa_y] == "#" and map_pos[caixa_x][caixa_y+1] == "#":
        print(map_pos[caixa_x-1][caixa_y],  map_pos[caixa_x][caixa_y+1])
        return True

    if map_pos[caixa_x-1][caixa_y] == "#" and map_pos[caixa_x][caixa_y-1] == "#":
        print(map_pos[caixa_x-1][caixa_y], map_pos[caixa_x][caixa_y-1])
        return True

    if map_pos[caixa_x+1][caixa_y] == "#" and map_pos[caixa_x][caixa_y+1] == "#":
        print(map_pos[caixa_x+1][caixa_y], map_pos[caixa_x][caixa_y+1])
        return True

    if map_pos[caixa_x+1][caixa_y] == "#" and map_pos[caixa_x][caixa_y-1] == "#":
        print(map_pos[caixa_x+1][caixa_y], map_pos[caixa_x][caixa_y-1])
        return True

    return False 

def distance(p1, p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
