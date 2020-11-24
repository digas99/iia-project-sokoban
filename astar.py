import agent
from copy import deepcopy

class PathFindingNode:                      

    grid = []

    def __init__(self, symbol, position):
        self.position = position
        self.symbol = symbol
        self.previous = None 
        self.g = 0
        self.h = 0
    
    def __eq__(self, other):
        if self.position == other.position and self.symbol == other.symbol:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.position, self.symbol))

    def children(self):
        x,y = self.position
        childrenlist = []
        for l in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                    childrenlist.append(self.grid[l][c])
        return [n for n in childrenlist if n.symbol in ['-', '@', '.', '+']]

    #distance between each node and goal node (manhattan distance)
    def heuristics(self, node):
        x1, y1 = self.position
        x2, y2 = node.position
        return abs(x2 - x1) + abs(y2 - y1)

class GameStateNode:
    def __init__(self, gridstate=None, movement=None):
        self.gridstate = deepcopy(gridstate)
        self.movement = movement
        if movement != None:
            boxpos, nextboxpos = movement
            self.move(boxpos, nextboxpos, self.get_keeper())

        self.previous = None
        self.g = 0
        self.h = 0
        self.final = False

    def __eq__(self, other):
        if self.final or other.final:
            return self.get_boxes() == other.get_boxes()
        return self.movement == other.movement and self.gridstate == other.gridstate
    
    def __hash__(self):
        return hash((self.movement, str(self.gridstate)))

    def __str__(self):
        string = ""
        lines = len(self.gridstate)
        cols = len(self.gridstate[0])
        for l in range(lines):
            for c in range(cols):
                string += self.gridstate[l][c].symbol
            string += "\n"
        return string
    
    def opposite(self, box, node):
        x_box, y_box = box.position
        x_node, y_node = node.position
        x = x_box + (x_box - x_node)
        y =  y_box + (y_box - y_node)
        return self.gridstate[x][y]

    def get_keeper(self):
        lines = len(self.gridstate)
        cols = len(self.gridstate[0])
        for l in range(lines):
            for c in range(cols):
                if self.gridstate[l][c].symbol == '@' or self.gridstate[l][c].symbol == '+':
                    return self.gridstate[l][c]
    
    def get_boxes(self):
        boxes = []
        lines = len(self.gridstate)
        cols = len(self.gridstate[0])
        for l in range(lines):
            for c in range(cols):
                if self.gridstate[l][c].symbol == '$' or self.gridstate[l][c].symbol == '*':
                    boxes.append(self.gridstate[l][c])
        return boxes

    def legal_move(self, box, node):
        a = Astar(self.get_keeper(), self.opposite(box, node))
        if a.search() == None:
            return False
        else:
            return True

    def children(self):

        PathFindingNode.grid = self.gridstate

        result = []
        
        for box in self.get_boxes():
            aux = []
            x,y = box.position
            for l in range(len(self.gridstate)):
                for c in range(len(self.gridstate[0])):
                    if self.gridstate[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                        aux.append(self.gridstate[l][c])   
            ###### ATUALIZAÇÃO DO GRIDSTATE #######
            childrenlist = [n for n in aux if n.symbol not in ['#', '$', '*'] and self.opposite(box, n).symbol != '#' and self.legal_move(box, n)] 
            for child in childrenlist:
                new_gamestate = GameStateNode(self.gridstate, (box.position, child.position))
                result.append(new_gamestate)
        
        return result

    def move(self, posbox, poschild, keeper):
        #keeper
        if keeper.symbol == '+':
            keeper.symbol = '.'
        elif keeper.symbol == '@':
            keeper.symbol = '-'
        # boxes
        x_box, y_box = posbox
        x_child, y_child = poschild
        node_box = self.gridstate[x_box][y_box]
        node_child = self.gridstate[x_child][y_child]
        if node_child.symbol == '-':

            if node_box.symbol == '$':
                node_child.symbol = '$'
                node_box.symbol = '@'

            elif node_box.symbol == '*':
                node_box.symbol = '+'
                node_child.symbol = '$'

        elif node_child.symbol == '.':

            if node_box.symbol == '$':
                node_child.symbol = '*' 
                node_box.symbol = '@'

            elif node_box.symbol == '*':
                node_child.symbol = '*' 
                node_box.symbol = '+'

    def heuristics(self, node):
        return 0

class Astar:
    def __init__(self, start, goal):
        self.start = start 
        self.goal = goal

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
                    n.h = n.heuristics(self.goal)
                    if n != self.start:
                        n.previous = curr_node
                    openset.add(n)




