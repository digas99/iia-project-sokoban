# 4 children nodes for each node
from node import *

def children_path(node, grid):
    x,y = node.position
    childrenlist = []
    for l in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[l][c].position in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
                childrenlist.append(grid[l][c])
    return [n for n in childrenlist if n.symbol == "-" or n.symbol == "@"]

# A* algorithm
def search_pathkeeper(grid, start, goal):
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
        if curr_node.eq(goal):
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
        
        # search for children of current node 
        for n in children_path(curr_node, grid):
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
                n.h = heuristics(n, goal)
                if n != start:
                    n.previous = curr_node
                openset.add(n)
            
        
        


    