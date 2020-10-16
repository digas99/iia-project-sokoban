
class Node():

    def _init_(self, parent=None, coords=None):
        self.parent = parent
        self.coords = coords

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, node):
        return node.coords == node.coords
    
    def astar(map, box_coords, goal):
        start_node = Node(Node, box_coords)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(Node, goal)
        goal_node.g = goal.node.h = goal_node.f = 0

        #lists
        


    