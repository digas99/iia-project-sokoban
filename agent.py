from backtracking import *
from mapa import Map

class Agent:

    def __init__(self, mapa):
        # boxes = state['boxes']
        # print(boxes)
        self.tmap = transpose(mapa) # 1. talvez redundante; retirar?

    def update(self, state):
        self.state = state
        self.gridmap = grid(self.tmap) # 1.trocar aqui em 1
        self.goals = self.get_goals()
        self.keeper = self.get_keeper()
        self.boxes = self.get_boxes()
        #self.approaches = [Approach(self.gridmap, state)]

    def key(self):
        path = self.decision()
        # substituir aqui quando completo
        return 'S'

    def decision(self):
        solution = False                                        ## MUDAR
        path_options = []
        for box in self.boxes:
            path_options = path_options + children_boxes(box, self.gridmap)
            #path = permutations(children_boxes(box, self.gridmap))
        print([node.position for node in path_options])
        final_path = permutations(path_options)
        print([node.position for node in final_path])
        # while not solution:            
        #     #approach = self.approaches.pop()
        #     # avalia prioridades
            
        #     # verifica solução
        #     # solution = approach.has_solution()
        #     # # obtem solução
        #     # path = approach.get_solution()
        return [] 

    ######## Funções de update ########
    def get_goals(self):
        return self.__get_nodes('.') + self.__get_nodes('*')

    def get_keeper(self):
        return self.__get_nodes('@')

    def get_boxes(self):
        return self.__get_nodes('$') + self.__get_nodes('*')

    def __get_nodes(self, symbol):
        # cria lista de nodes vazia
        nodes = []
        # obter coordenadas do array de arrays
        rows, cols = len(self.gridmap), len(self.gridmap[0]) # eliminar isto?
        # percorre array
        for row in range(rows):
            # percorre duplo array
            for col in range(cols):
                current_node = self.gridmap[row][col]
                if current_node.symbol == symbol:
                    nodes.append(current_node)                   
        return nodes

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

# def obstacles_around(mapa, pos):
#     rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
#     if not in_frame(rows_lim, cols_lim, pos):
#         #print(f"obstacles around {pos}")
#         x, y = pos[0], pos[1]
#         unwanted_symbols = ['#', '$', '*']
#         around = [(x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1)]
#         return [square for square in around if mapa[square[0]][square[1]].symbol in unwanted_symbols]

# # main function that checks for obstacles in both sides of the given square
# def opp_sides_blockage(mapa, pos, obstacles, side_info):
#     rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
#     # if has reached a place in the frame, then it is blocked
#     if in_frame(rows_lim, cols_lim, pos):
#         print(f"WARNING: {pos} is in frame!")
#         return True
    
#     print(f"[opp_side] CHECKING POS{pos}:")
#     x, y = pos[0], pos[1]
#     pos1_obst, pos2_obst, sides = [], [], []
#     if side_info == "horizontal":
#         s1, s2 = "l", "r"
#         sides = [x-1, x+1]
#     else:
#         s1, s2 = "t", "b"
#         sides = [y-1, y+1]
#     # loops through both sides
#     for side in sides:
#         if side_info == "horizontal":
#             sides_pos = [(side, y), (side, y-1), (side, y+1)]
#         else:
#             sides_pos = [(x, side), (x-1, side), (x+1, side)]

#         # loops through each obstacle for each side
#         for obst in obstacles:
#             # if obstacle is in one of the sides
#             if obst in sides_pos:
#                 # if is the first side
#                 if side == x-1:
#                     pos1_obst.append(obst)
#                 # if is the second side
#                 else:
#                     pos2_obst.append(obst)

#     print("pos1", pos1_obst)
#     print("pos2", pos2_obst)
#     # if there is atleast one obstacle on both sides
#     if len(pos1_obst) > 0 and len(pos2_obst) > 0:
#         checks1 = [side_blockage(mapa, obst, obstacles_around(mapa, obst), s1) for obst in pos1_obst]
#         checks2 = [side_blockage(mapa, obst, obstacles_around(mapa, obst), s2) for obst in pos2_obst]
#         return atleast_one_true(checks1) and atleast_one_true(checks2)
#     else:
#         return False

# # recursive function that checks for obstacles in a specific side until it hits frame or no obstacles
# def side_blockage(mapa, pos, obstacles, side_info):
#     rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
#     # if has reached a place in the frame, then it is blocked
#     if in_frame(rows_lim, cols_lim, pos):
#         print(f"WARNING: {pos} is in frame!")
#         return True
    
#     print(f"[side] CHECKING POS{pos}:")
#     x, y = pos[0], pos[1]
#     pos_obst = []
#     if side_info == "l":
#         side = x-1
#         sides_pos = [(side, y), (side, y-1), (side, y+1)]
#     elif side_info == "t":
#         side = y-1
#         sides_pos = [(x, side), (x-1, side), (x+1, side)]
#     elif side_info == "r":
#         side = x+1
#         sides_pos = [(side, y), (side, y-1), (side, y+1)]
#     else:
#         side = y+1
#         sides_pos = [(x, side), (x-1, side), (x+1, side)]

#     for obst in obstacles:
#         # if obstacle is in one of the sides
#         if obst in sides_pos:
#             pos_obst.append(obst)
        
#     print("pos", pos_obst)

#     return atleast_one_true([side_blockage(mapa, obst, obstacles_around(mapa, obst), side_info) for obst in pos_obst])

# def atleast_one_true(lista):
#     return [e for e in lista if e] != []  

# def in_frame(rows_lim, cols_lim, pos):
#     return pos[0] == 0 or pos[0] == rows_lim or pos[1] == 0 or pos[1] == cols_lim