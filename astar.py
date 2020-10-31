
class Node:

    def __init__(self, symbol, position):
        self.position = position
        self.symbol = symbol
        self.previous = None 
        self.g = 0
        self.h = 0

# distance between each node and goal node ( manhattan distance)
def heuristics(node, goal):
    x1, y1 = node.position
    x2, y2 = goal.position
    return abs(x2 - x1) + abs(y2 - y1)

# 4 children nodes for each node
def children(node, grid):
    x,y = node.position
    childrenlist = []
    for l in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                childrenlist.append(grid[l][c])
    return [n for n in childrenlist if n.symbol != '#']

# A* algorithm
def search_boxes(grid, start, goal):
    #not seen nodes
    openset = set()
    #seen nodes
    closedset = set()

    curr_node = start
    openset.add(curr_node)
    
    while openset:
        #finds the node with the lowest f function
        curr_node = min(openset, key=lambda n: n.g + n.h)

        #if node is goal box
        if curr_node == goal:
            path = []
            while curr_node.previous:
                path.append(curr_node)
                curr_node = curr_node.previous
            path.append(curr_node)
            return path[::-1]
        
        #if node is not goal box
        #check node as seen
        openset.remove(curr_node)
        closedset.add(curr_node)

        # search for children of current node 
        for n in children(curr_node, grid):
            #if its already seen, skip it
            if n in closedset:
                continue

            if n in openset: 
                #compare if the new path g cost is lower than the current
                try_g = curr_node.g + 1;
                if try_g < n.g:
                    # give the new g_cost
                    n.g = try_g
                    n.previous = curr_node
            else:
                #calculate the g and h value for remaining nodes
                n.g = curr_node.g + 1
                n.h = heuristics(n, goal)
                n.previous = curr_node
                openset.add(n)
        
        


    