import agent
from deadlock import DeadlockAgent

class Node:
    def __init__(self, symbol, position):
        self.position = position
        self.symbol = symbol
        self.previous = None 
        self.g = 0
        self.h = 0

    def is_deadlock(self, adjacents, unwanted_symbols):
        return DeadlockAgent(self.position, adjacents, unwanted_symbols).check_all_deadlocks() if self.symbol != "#" and adjacents != None else False

    def is_stuck(self):
        if self.children_boxes == []:
            return True
        else: 
            return False

class Astar:
    def __init__(self, grid, boxes, goals, keeper):
        self.grid = grid
        self.boxes = boxes
        self.goals = goals
        self.keeper = keeper

    def opposite(self, box, node):
        x_box, y_box = box.position
        x_node, y_node = node.position
        x = x_box + (x_box - x_node)
        y =  y_box + (y_box - y_node)
        return self.grid[x][y]
    
    # distance between each node and goal node (manhattan distance)
    def heuristics(self, node1, node2):
        x1, y1 = node1.position
        x2, y2 = node2.position
        return abs(x2 - x1) + abs(y2 - y1)

    def legal_move(self, box, node):
        path = self.search(self.keeper[0], self.opposite(box, node), 'keeper')
        if  path == None:    
            return False
        else:
            return True

    def children(self, node):
        x,y = node.position
        childrenlist = []
        for l in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                    childrenlist.append(self.grid[l][c])
        return childrenlist

    def children_boxes(self, node):
        return [n for n in self.children(node) if n.symbol != '#' and self.opposite(node, n).symbol != '#' and not n.is_deadlock(self.children(n), ["#"]) and self.legal_move(node, n)]    ########## AND IS_DEADLOCK?? 

    def children_keeper(self, node):
        return [n for n in self.children(node) if n.symbol == "-" or n.symbol == "@"]

    # A* algorithm
    def search(self, start, goal, type):
        #not seen nodes
        openset = set()
        #seen nodes
        closedset = set()

        curr_node = start
        curr_node.g = 0

        openset.add(curr_node)

        while openset:
            #finds the node with the lowest f function
            curr_node = min(openset, key=lambda n: n.g + n.h)

            #if node is goal box
            if curr_node is goal:
                path = []
                while curr_node != start:
                    path.append(curr_node)
                    curr_node = curr_node.previous
                path.append(start)
                return path[::-1]
        
            #if node is not goal box
            #check node as seen
            openset.remove(curr_node)
            closedset.add(curr_node)
        
            #search for children of current node 
            if type == 'boxes':
                children = self.children_boxes
            elif type == 'keeper':
                children = self.children_keeper
        
            for n in children(curr_node):
                #if its already seen, skip it
                if n in closedset:
                    continue

                if n in openset: 
                    #compare if the new path g cost is lower than the current
                    try_g = curr_node.g + 1;
                    if try_g < n.g:
                        # give the new g_cost
                        n.g = try_g
                        if n != start:
                            n.previous = curr_node
                else:
                    #calculate the g and h value for remaining nodes
                    n.g = curr_node.g + 1
                    n.h = self.heuristics(n, goal)
                    if n != start:
                        n.previous = curr_node
                    openset.add(n)


# def moves(boxes, grid):
#     possible_moves = []             # has a tuple of (node, and possible move)
#     for box in boxes:
#         children = children_boxes(box, grid)
#         x_box, y_box = box.position
#         for child in children:
#             x_child, y_child = child.position
#             if (x_box - x_child, y_box - y_child) == (1,0):
#                 possible_moves.append((box, 'left'))
#             if (x_box - x_child, y_box - y_child) == (0,1):
#                 possible_moves.append((box, 'up'))
#             if (x_box - x_child, y_box - y_child) == (-1,0):
#                 possible_moves.append((box, 'right'))
#             if (x_box - x_child, y_box - y_child) == (0,-1):
#                 possible_moves.append((box, 'down'))
#     return possible_moves


