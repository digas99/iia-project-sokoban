import numpy as np


class Node:

    def __init__(self, current, parent):
        self.current = current
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

def grid(matrix):
    lines = len(matrix)
    columns = len(matrix[0])
    grid = matrix
    for l in range(lines):
        for c in range(columns):
            grid[l][c] = Node(None,None)

    return grid


def search_boxes(grid, start, goal):
    open_set = []
    closed_set = []

    startnode = Node(start, None) 
    goalnode =  Node(goal, None)

    open_set.append(startnode)


        


    