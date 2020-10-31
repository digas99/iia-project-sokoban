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

                print(type(mapa))

                # boxes = state['boxes']
                # print(boxes)

                
                map_pos = matrix(mapa)
                #print(np.array(map_pos))
                print(map_pos)
                
                #print(grid(mapa))
                gridmap = grid(mapa)
                lines = len(gridmap)
                cols = len(gridmap[0])
                start = 0
                goal = 0
                for l in range(lines):
                    for c in range(cols):
                        if gridmap[l][c].symbol == '$':
                            start = gridmap[l][c]
                        if gridmap[l][c].symbol == '.':
                            goal = gridmap[l][c]
                path = search_boxes(gridmap, start, goal)
                for node in path:
                    x, y = node.position
                    print(y, x) #transposed

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

def grid(mapa):
    # create a grid of nodes
    matrix = str(mapa).split('\n')
    lines = len(matrix)
    cols = len(matrix[0])
    grid = [[0 for c in range(cols)] for l in range(lines)]
    for l in range(lines):
        for c in range(cols):
            grid[l][c] = Node(matrix[l][c], (l,c))
    return list(map(list, zip(*grid)))

def matrix(mapa):
    map_pos = str(mapa).split('\n')
    return list(map(list, zip(*map_pos)))



# requer modificações
'''def is_deadlock(caixa, map_pos):
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

    return False '''

#será necessária?
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
