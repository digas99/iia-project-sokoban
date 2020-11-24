#from backtracking import *
from mapa import Map
from astar import *
from copy import deepcopy

class Agent:

    def __init__(self, mapa):
        # boxes = state['boxes']
        # print(boxes)
        self.mapa = mapa

    def update(self, state):
        self.starting_grid = grid(self.mapa)
        self.final_grid = self.final_state()


    def key(self):
        moves = self.decision()

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
        ############ TESTING ######################
        root = GameStateNode(self.starting_grid)
        goal = GameStateNode(self.final_grid)
        goal.final = True
        #print(root)
        #print(goal)
        a = Astar(root, goal)
        path = a.search()
        for step in path:
            print(step)
        return [step.movement for step in path]

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


