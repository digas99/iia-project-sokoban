from mapa import Map
from astar import *
from copy import deepcopy

class Agent:

    def __init__(self, mapa):
        # boxes = state['boxes']
        # print(boxes)
        self.mapa = mapa
        self.keys = []
        self.starting_grid = None
        self.final_grid = None
        self.goals = self.get_goals(grid(mapa))

    def get_goals(self, grid):
        return [grid[l][c] for c in range(len(grid[0])) for l in range(len(grid)) if grid[l][c].symbol in ['.', '*']]

    def new_level(self, mapa):
        self.mapa = mapa
        self.starting_grid = None
        self.goals = self.get_goals(grid(mapa))

    def update(self, state):
        if self.starting_grid == None:
            self.starting_grid = grid(self.mapa)
            self.final_grid = self.final_state()

    def key(self):
        if self.keys == []:
            path = self.decision()
            for i in range(len(path)-1):
                y, x = path[i]
                y_next, x_next = path[i+1]
                if (x - x_next, y - y_next) == (1,0):
                    self.keys.insert(0, ('a', path[i+1]))
                elif (x - x_next, y - y_next) == (0,1):
                    self.keys.insert(0, ('w', path[i+1]))
                elif (x - x_next, y - y_next) == (-1,0):
                    self.keys.insert(0, ('d', path[i+1]))
                elif (x - x_next, y - y_next) == (0,-1):
                    self.keys.insert(0, ('s', path[i+1]))
        return self.keys.pop()

    def decision(self):
        ############ TESTING ######################
        root = GameStateNode(self.starting_grid, goals=self.goals)
        goal = GameStateNode(self.final_grid, goals=self.goals)
        goal.final = True
        #print(root)
        #print(goal)
        astar_boxes = Astar(root, goal)
        tree_state = astar_boxes.search()
        path = self.keeper_path(tree_state)
        return path

    def keeper_path(self, tree_state):
        path = []
        for i in range(len(tree_state)-1):
            childstate = tree_state[i]
            keeper = childstate.get_keeper()
            state = tree_state[i+1]
            boxpos, nextboxpos = state.movement
            x,y = boxpos
            x_next, y_next = nextboxpos
            box = state.gridstate[x][y]
            nextbox = state.gridstate[x_next][y_next]
            finish = state.opposite(box, nextbox)
            PathFindingNode.grid = childstate.gridstate
            astar_keeper = Astar(keeper, finish)
            aux = astar_keeper.search() 
            if aux == None:
                aux = []
            path = path + [node.position for node in aux] + [box.position] 
        # print([node.position for node in path])
        return path

    def final_state(self):
        finalstate = deepcopy(self.starting_grid)
        lines = len(finalstate)
        cols = len(finalstate[0])
        for l in range(lines):
            for c in range(cols):
                if finalstate[l][c].symbol == '.':
                    finalstate[l][c].symbol = '*'
                if finalstate[l][c].symbol == '$':
                    finalstate[l][c].symbol = '-'
        return finalstate 

def grid(mapa):
    # creates a grid of nodes from map
    mapa = str(mapa).split('\n')
    lines = len(mapa)
    cols = len(mapa[0])
    grid = [[0 for c in range(cols)] for l in range(lines)]
    for l in range(lines):
        for c in range(cols):
            grid[l][c] = PathFindingNode(mapa[l][c], (l,c))
    return grid


