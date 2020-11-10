import asyncio
import getpass
import json
import os
import math
import websockets 
from astar_box import *
from astar_sokoban import *
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
                        if current_node.symbol == '.':
                            goal = current_node
                        if current_node.symbol == '$':
                            start = current_node

                path_caixa = search_boxes(gridmap, start, goal)
                
                # PRINTA O PATH 
                for node in path_caixa:
                    x, y = node.position
                    print(x, y) 

                for i in range(0, len(path_caixa)-1):
                    print(i)
                    if i == 0:
                        x,y = state['keeper']
                        start_sokoban = gridmap[x][y]
                    else: 
                        start_sokoban = path_caixa[i-1]

                    obj_caixa = path_caixa[i+1]
                    caixa = path_caixa[i]
                    node = oposite(gridmap, caixa, obj_caixa)
                    print("Start")
                    print(start_sokoban.position)
                    print(start_sokoban.symbol)
                    print("Oposite")
                    print(node.position)
                    print(node.symbol)

                    path_sokoban = search_path(gridmap, start_sokoban, node)

                    # PRINTA O PATH 
                    print("Acabou!!!!!!!!!!!")
                    if path_sokoban != None:
                        for node in path_sokoban:
                            x, y = node.position
                            print(x, y)     


                # PRINTA O PATH 
                for node in path_caixa:
                    x, y = node.position
                    print(x, y) 

                print("\n\nTESTEEEEEEE")
                pos = (1,4)
                direction = "vertical"
                print(f"Checking: {direction}\nPosition {pos} has blockage in both sides:",opp_sides_blockage(gridmap, pos, obstacles_around(gridmap, pos), direction))
                
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

def obstacles_around(mapa, pos):
    rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
    if not in_frame(rows_lim, cols_lim, pos):
        #print(f"obstacles around {pos}")
        x, y = pos[0], pos[1]
        unwanted_symbols = ['#', '$', '*']
        around = [(x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1)]
        return [square for square in around if mapa[square[0]][square[1]].symbol in unwanted_symbols]

# main function that checks for obstacles in both sides of the given square
def opp_sides_blockage(mapa, pos, obstacles, side_info):
    rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
    # if has reached a place in the frame, then it is blocked
    if in_frame(rows_lim, cols_lim, pos):
        print(f"WARNING: {pos} is in frame!")
        return True
    
    print(f"[opp_side] CHECKING POS{pos}:")
    x, y = pos[0], pos[1]
    pos1_obst, pos2_obst, sides = [], [], []
    if side_info == "horizontal":
        s1, s2 = "l", "r"
        sides = [x-1, x+1]
    else:
        s1, s2 = "t", "b"
        sides = [y-1, y+1]
    # loops through both sides
    for side in sides:
        if side_info == "horizontal":
            sides_pos = [(side, y), (side, y-1), (side, y+1)]
        else:
            sides_pos = [(x, side), (x-1, side), (x+1, side)]

        # loops through each obstacle for each side
        for obst in obstacles:
            # if obstacle is in one of the sides
            if obst in sides_pos:
                # if is the first side
                if side == x-1:
                    pos1_obst.append(obst)
                # if is the second side
                else:
                    pos2_obst.append(obst)

    print("pos1", pos1_obst)
    print("pos2", pos2_obst)
    # if there is atleast one obstacle on both sides
    if len(pos1_obst) > 0 and len(pos2_obst) > 0:
        checks1 = [side_blockage(mapa, obst, obstacles_around(mapa, obst), s1) for obst in pos1_obst]
        checks2 = [side_blockage(mapa, obst, obstacles_around(mapa, obst), s2) for obst in pos2_obst]
        return atleast_one_true(checks1) and atleast_one_true(checks2)
    else:
        return False

# recursive function that checks for obstacles in a specific side until it hits frame or no obstacles
def side_blockage(mapa, pos, obstacles, side_info):
    rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
    # if has reached a place in the frame, then it is blocked
    if in_frame(rows_lim, cols_lim, pos):
        print(f"WARNING: {pos} is in frame!")
        return True
    
    print(f"[side] CHECKING POS{pos}:")
    x, y = pos[0], pos[1]
    pos_obst = []
    if side_info == "l":
        side = x-1
        sides_pos = [(side, y), (side, y-1), (side, y+1)]
    elif side_info == "t":
        side = y-1
        sides_pos = [(x, side), (x-1, side), (x+1, side)]
    elif side_info == "r":
        side = x+1
        sides_pos = [(side, y), (side, y-1), (side, y+1)]
    else:
        side = y+1
        sides_pos = [(x, side), (x-1, side), (x+1, side)]

    for obst in obstacles:
        # if obstacle is in one of the sides
        if obst in sides_pos:
            pos_obst.append(obst)
        
    print("pos", pos_obst)

    return atleast_one_true([side_blockage(mapa, obst, obstacles_around(mapa, obst), side_info) for obst in pos_obst])

def atleast_one_true(lista):
    return [e for e in lista if e] != []  

def in_frame(rows_lim, cols_lim, pos):
    return pos[0] == 0 or pos[0] == rows_lim or pos[1] == 0 or pos[1] == cols_lim

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
