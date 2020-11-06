import asyncio
import getpass
import json
import os
import math
import websockets 
from astar import *
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

                # boxes = state['boxes']
                # print(boxes)
  
                tmap = transpose(mapa)

                #ENCONTRA O CAMINHO MAIS RAPIDO DA CAIXA AO GOAL 
                gridmap = grid(tmap)

                start, goal = 0, 0    
                rows, cols = len(gridmap), len(gridmap[0])
                deadlocks = []
                for row in range(rows):
                    for col in range(cols):
                        current_node = gridmap[row][col]
                        current_pos = current_node.position

                        if current_node.symbol == '.':
                            goal = current_node

                        # check only for squares that are not walls or in the frame of the map
                        elif current_node.symbol != '#' and not in_frame(rows, cols, current_pos) and deadlock_closeToWall(gridmap, current_pos):
                            deadlocks.append(current_node)

                            if current_node.symbol == '$':
                                start = current_node

                path = search_boxes(gridmap, start, goal) 
                # PRINTA O PATH 
                for node in path:
                    x, y = node.position
                    print(x, y) 

                # import pprint
                # pprint.pprint(state)
                
                #key = "d"

                # if state['keeper'] == [4,3]:
                #     key = "a"



                # print(Map(f"levels/{state['level']}.xsb"))
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


def transpose(mapa):
    map_pos = str(mapa).split('\n')
    return list(map(list, zip(*map_pos)))

def grid(mapa):
    # creates a grid of nodes from map
    lines = len(mapa)
    cols = len(mapa[0])
    grid = [[0 for c in range(cols)] for l in range(lines)]
    for l in range(lines):
        for c in range(cols):
            grid[l][c] = Node(mapa[l][c], (l,c))
    return grid

def deadlock_closeToWall(mapa, pos):
    print("pos", pos)
    x, y = pos[0], pos[1]
    around = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
    for square in around:
        if mapa[square[0]][square[1]].symbol == '#':
            return True
    return False
                
def in_frame(rows, cols, pos):
    return pos[0] == 0 or pos[0] == rows-1 or pos[1] == 0 or pos[1] == cols-1

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
