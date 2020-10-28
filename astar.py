
class Node:

    def __init__(self, symbol, position):
        self.position = position
        self.symbol = symbol
        self.n_next = None 
        self.g = 0
        self.h = 0

    def move_cost(self, other)

# def grid(matrix):
#     lines = len(matrix)
#     columns = len(matrix[0])
#     grid = matrix
#     for l in range(lines):
#         for c in range(columns):
#             grid[l][c] = Node(None,None)

#     return grid

def children(node, grid):
    x,y = node.position
    childrenlist = []
    for n in grid:
        if n.position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
            childrenlist.append(n)
    return [n for n in childrenlist if n.symbol != '#']


def search_boxes(grid, start, goal):
    #not seen nodes
    openset = set()
    #seen nodes
    closedset = set()

    curr_node = start
    openset.add(curr_node)
    
    while openset:
        #finds the the node with the lowest f function
        curr_node = min(openset, key=lambda n: n.g + n.h)

        #if node is goal box
        if curr_node == goal:
            path = []
            while curr_node.n_next:
                path.append(curr_node)
                curr_node = curr_node.n_next
            path.append(curr_node)
            return path[::-1]
        
        #if node is not goal box
        #check node as seen
        openset.remove(curr_node)
        closedset.add(curr_node)

        for n in children(curr_node, grid):
            #if its already seen skip it
            if n in closedset:
                continue

            if n in openset: 
                pass
    

        


    