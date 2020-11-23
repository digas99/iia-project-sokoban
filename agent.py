#from backtracking import *
from mapa import Map
from astar import *

class Agent:

    def __init__(self, mapa):
        # boxes = state['boxes']
        # print(boxes)
        self.tmap = transpose(mapa)

    def update(self, state):
        self.state = state
        self.gridmap = grid(self.tmap)
        self.goals = self.get_goals()
        self.keeper = self.get_keeper()
        self.boxes = self.get_boxes()

    def key(self):
        path = self.decision()
        keys = []
        for i in range(len(path)-1):
            x, y = path[i].position 
            x_next, y_next = path[i+1].position
            if (x - x_next, y - y_next) == (1,0):
                keys.append('a')
            if  (x - x_next, y - y_next) == (0,1):
                keys.append('w')
            if  (x - x_next, y - y_next) == (-1,0):
                keys.append('d')
            if  (x - x_next, y - y_next) == (0,-1):
                keys.append('s')
        return keys

    def decision(self):
        solution = False  
        PathFindingNode.grid = self.gridmap  
                                           
        ############ TESTING #########################
        a = Astar(self.keeper[0], self.goals[0])
        path = a.search()
        

        return path


    # def move(self, box, nextpos_box): 
    #     box.gridmap = deepcopy(self.gridmap)
    #     #keeper.symbol = '-'
    #     #nextpos_keeper = '@'
    #     if nextpos_box.symbol == '-':
    #         if  box.symbol == '$':
    #             nextpos_box.symbol = '$'
    #             box.symbol == '-'
    #         elif box.symbol == '*':
    #             box.symbol = '.'
    #             nextpos_box.symbol = '$'
    #     elif nextpos_box.symbol == '.':
    #         if box.symbol == '$':
    #             nextpos_box.symbol = '*' 
    #             box.symbol = '-'
    #         elif box.symbol == '*':
    #             nextpos_box.symbol = '*' 
    #             box.symbol = '.'
    #     box.nextpos_box.gridmap = deepcopy(self.gridmap)

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
            grid[l][c] = PathFindingNode(mapa[l][c], (l,c))
    return grid
