class Node:

    def __init__(self, symbol, position):
        self.position = position
        self.symbol = symbol
        self.previous = None 
        self.g = 0
        self.h = 0

    def eq(self, other):
        if self.position == other.position:
            if self.symbol == other.symbol:
                if self.previous == other.previous:
                    if self.h == other.h:
                        if self.g == other.g:
                            return True
        return False

    def copy(self):
        return Node(self.symbol, self.position)

# distance between each node and goal node ( manhattan distance)
def heuristics(node, goal):
    x1, y1 = node.position
    x2, y2 = goal.position
    return abs(x2 - x1) + abs(y2 - y1)