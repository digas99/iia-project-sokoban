class DeadlockAgent:
	def __init__(self, position, adjacents, unwanted_symbols, gamestate):
		self.position = position
		self.adjacents = adjacents
		self.unwanted_symbols = unwanted_symbols
		self.obstacles = [adjacent for adjacent in adjacents if adjacent.symbol in unwanted_symbols]
		self.gamestate = gamestate
		
	def set_unwanted_symbols(self, unwanted_symbols):
		self.unwanted_symbols = unwanted_symbols
		self.obstacles = [adjacent for adjacent in self.adjacents if adjacent.symbol in unwanted_symbols]

	def get_unwanted_symbols(self):
		return self.unwanted_symbols

	def check_all_deadlocks(self):
		#return any([function(self) for name, function in DeadlockAgent.__dict__.items() if callable(function) and name not in ["__init__", "check_all_deadlocks", "set_unwanted_symbols", "get_unwanted_symbols"]])
		if self.deadlock_corner():
			return True
		
		if self.deadlock_next_to_walls_no_goal_in_path():
			return True
		
		return False

	def deadlock_corner(self):
		x, y = self.position
		pairs = [[(x-1, y), (x, y+1)], [(x, y+1), (x+1, y)], [(x+1, y), (x, y-1)], [(x, y-1), (x-1, y)]]
		return any([all(square in [obstacle.position for obstacle in self.obstacles] for square in pair) for pair in pairs])
	
	def deadlock_next_to_walls_no_goal_in_path(self):
		x, y = self.position
		mapa = self.gamestate.gridstate
		map_limits = len(mapa)-1, len(mapa[0])-1
		checks = []
		for obstacle in self.obstacles:
			xo, yo = obstacle.position
			direction = "vertical" if yo != y else "horizontal"

			if direction == "horizontal":
				if any([goal.position[0] == x for goal in self.gamestate.goals]):
					return False
			else:
				if any([goal.position[1] == y for goal in self.gamestate.goals]):
					return False

			checks.append(sides_are_walls(self, obstacle, map_limits, obstacle.children(True), direction))
		return any(checks)

def sides_are_walls(parent, current, map_limits, adjacents, direction):
	x, y = current.position
	sides = [(x-1,y), (x+1,y)] if direction == "vertical" else [(x,y-1), (x,y+1)]
	sides_nodes = [adjacent for adjacent in adjacents if adjacent.position in sides] 
	return all([side_is_wall(current, side, map_limits, side.children(True), direction) for side in sides_nodes])

def side_is_wall(parent, current, map_limits, adjacents, direction):
	rows_lim, cols_lim = map_limits
	frame_direction = "vertical" if direction == "horizontal" else "horizontal"
	if in_frame(rows_lim, cols_lim, current.position, frame_direction):
		return True
	
	x, y = current.position
	# index 0 of tuple is the direction to go if curr is wall, index 1 is if curr is not wall
	sides = ([(x-1,y), (x+1,y)], [(x,y-1), (x,y+1)]) if direction == "vertical" else ([(x,y-1), (x,y+1)], [(x-1,y) , (x+1,y)])

	if current.symbol != "#":
		if parent.symbol != "#":
			return False

		obstacles = [adjacent.position for adjacent in adjacents if adjacent.symbol == "#"]
		if all([side not in obstacles for side in sides[1]]):
			return False

	# choose side oposite to parent
	side = [side for side in sides[0] if side != parent.position][0]
	# get node
	adjacent = [adjacent for adjacent in adjacents if adjacent.position == side][0]
	return side_is_wall(current, adjacent, map_limits, adjacent.children(True), direction)
	
def in_frame(rows_lim, cols_lim, pos, frame_direction):
	x, y = pos
	#print("CHECK IF INFRAME: ",pos)
	checks = [y==0, y==cols_lim] if frame_direction == "vertical" else [x==0, x==rows_lim]
	return any(checks)