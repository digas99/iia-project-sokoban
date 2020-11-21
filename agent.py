#from backtracking import *
from mapa import Map
from astar import *
from copy import deepcopy

class Agent:

    def __init__(self, mapa):
        # boxes = state['boxes']
        # print(boxes)
        self.tmap = transpose(mapa)

    def update(self, state):
        self.state = state
        self.gridmap = grid(self.tmap) # 1.trocar aqui em 1
        self.goals = self.get_goals()
        self.keeper = self.get_keeper()
        self.boxes = self.get_boxes()

    def key(self):
        path = self.decision()
        # substituir aqui quando completo
        return 'S'

    def decision(self):
        solution = False                                        ## MUDAR
        a = Astar(self.gridmap, self.boxes, self.goals, self.keeper)  
        ############ TESTING #########################
        # for box in self.boxes:
        #     for goal in self.goals:
        #         if goal.symbol == '*' and box.symbol == '$':
        #             continue    # ignora este tipo de goal porque está ocupado
        children = a.children_boxes(self.boxes[0])
        for child in children:
            a.children_boxes(child)
        return []

        #print([node.position for node in path_options])
        # print([node.position for node in final_path])
        # while not solution:            
        #     #approach = self.options.pop()
        #     # avalia prioridades
            
        #     # verifica solução
        #     # solution = approach.has_solution()
        #     # # obtem solução
        #     # path = approach.get_solution()


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
