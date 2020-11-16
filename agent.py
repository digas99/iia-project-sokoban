#from backtracking import *
from mapa import Map
from astar import *

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
        #self...

    def key(self):
        path = self.decision()
        # substituir aqui quando completo
        return 'S'

    def decision(self):
        solution = False                                        ## MUDAR
        path_options = []
            #path_options += children_boxes(box, self.gridmap)
            #print([box.position for box in self.boxes])
        print([(tup[0].position, tup[1]) for tup in moves(self.boxes, self.gridmap)])
        for box in self.boxes:
            print([(tup[0].position, tup[1]) for tup in moves(children_boxes(box, self.gridmap), self.gridmap)])
        #print([node.position for node in path_options])
        # print([node.position for node in final_path])
        # while not solution:            
        #     #approach = self.options.pop()
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

# def obstacles_around(mapa, node):
#     #print(pos)
#     rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
#     #if not in_frame(rows_lim, cols_lim, pos):
#     x, y = node.pos
#     around = [(x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1)]
#     return [square for square in around if mapa[square[0]][square[1]].symbol in ['#', '$', '*']]

# def in_frame(rows_lim, cols_lim, pos):
#     return pos[0] == 0 or pos[0] == rows_lim or pos[1] == 0 or pos[1] == cols_lim