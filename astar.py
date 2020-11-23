import agent
#from deadlock import DeadlockAgent

class PathFindingNode:                      

    grid = []

    def __init__(self, symbol, position):
        self.position = position
        self.symbol = symbol
        self.previous = None 
        self.g = 0
        self.h = 0
    
    def __eq__(self, other):
        if self.position == other.position and self.symbol == other.symbol and self.previous == other.previous and self.g == other.g and self.h == other.h:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.position, self.symbol, self.previous, self.g, self.h))

    def children(self):
        x,y = self.position
        childrenlist = []
        for l in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                    childrenlist.append(self.grid[l][c])
        return [n for n in childrenlist if n.symbol == "-" or n.symbol == "@" or n.symbol == '.']


    # def is_deadlock(self, adjacents, unwanted_symbols):
    #     return DeadlockAgent(self.position, adjacents, unwanted_symbols).check_all_deadlocks() if self.symbol != "#" and adjacents != None else False

    # def is_stuck(self):
    #     if self.children_boxes == []:
    #         return True
    #     else: 
    #         return False    

class GameStateNode:
    def __init__(self, move):
        self.move = move
        self.gridstate = None
        self.previous = None
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        if self.move == other.move and self.gridstate == other.gridstate and self.previous == other.previous and self.g == other.g and self.h == other.h:
            return True
        else:
            return False
    
    def __hash__(self):
        return hash((self.move, self.gridstate, self.previous, self.g, self.h))
    
    def opposite(self, box, node):
        x_box, y_box = box.position
        x_node, y_node = node.position
        x = x_box + (x_box - x_node)
        y =  y_box + (y_box - y_node)
        return self.gridstate[x][y]

    def children(self):
        x,y = self.position
        childrenlist = []
        for l in range(len(self.gridstate)):
            for c in range(len(self.gridstate[0])):
                if self.gridstate[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                    childrenlist.append(self.gridstate[l][c])   
        return [n for n in childrenlist if n.symbol != '#' and self.opposite(self, n).symbol != '#'] 


class Astar:
    def __init__(self, start, goal):
        self.start = start 
        self.goal = goal

    #distance between each node and goal node (manhattan distance)
    def heuristics(self, node1, node2):
        x1, y1 = node1.position
        x2, y2 = node2.position
        return abs(x2 - x1) + abs(y2 - y1)

    # A* algorithm
    def search(self):
        #not seen nodes
        openset = set()
        #seen nodes
        closedset = set()

        curr_node = self.start
        curr_node.g = 0

        openset.add(curr_node)

        while openset:
            #finds the node with the lowest f function
            curr_node = min(openset, key=lambda n: n.g + n.h)

            #if node is goal box
            if curr_node == self.goal:
                path = []
                while curr_node != self.start:
                    path.append(curr_node)
                    curr_node = curr_node.previous
                path.append(self.start)
                return path[::-1]
        
            #if node is not goal box
            #check node as seen
            openset.remove(curr_node)
            closedset.add(curr_node)
            children_list = curr_node.children()
    
            for n in children_list:
                #if its already seen, skip it
                if n in closedset:
                    continue

                if n in openset: 
                    #compare if the new path g cost is lower than the current
                    try_g = curr_node.g + 1
                    if try_g < n.g:
                        # give the new g_cost
                        n.g = try_g
                        if n != self.start:
                            n.previous = curr_node
                else:
                    #calculate the g and h value for remaining nodes
                    n.g = curr_node.g + 1
                    n.h = self.heuristics(n, self.goal)
                    if n != self.start:
                        n.previous = curr_node
                    openset.add(n)

    


    # def children_boxes(self, node):                                                                                       #not n.is_deadlock(self.children(n), ["#"])  
    #     return [n for n in node.children() if n.symbol != '#' and self.opposite(node, n).symbol != '#' and self.legal_move(node, n)]    ########## AND IS_DEADLOCK?? 

    # def children_keeper(self):
    #     return [n for n in node.children() if n.symbol == "-" or n.symbol == "@"]



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

    # def get_move(self, move):
    #     if move == 'a':     #left
    #         return (1,0)
    #     if move == 'w':     #up
    #         return (0,1)
    #     if move == 'd':     #right
    #         return (-1, 0)
    #     if move == 's':     # down
    #         return (0,-1)


