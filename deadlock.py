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
		#print("goals", self.gamestate.goals)

		# not deadlock if goal in path
		if any([goal.position[0] == x or goal.position[1] == y for goal in self.gamestate.goals]):
			return False

		mapa = self.gamestate.gridstate
		map_limits = len(mapa)-1, len(mapa[0])-1
		checks = []
		# print("POS: ", self.position)
		# print("obstacles: ", [o.position for o in self.obstacles])
		for obstacle in self.obstacles:
			xo, yo = obstacle.position
			direction = "vertical" if yo != y else "horizontal"
			# print(direction)
			checks.append(sides_are_walls(obstacle.position, map_limits, [child for child in obstacle.children(True) if child.symbol == "#"], direction))
		
		#print(checks)
		return any(checks)

def sides_are_walls(pos, map_limits, obstacles, direction):
	rows_lim, cols_lim = map_limits
	frame_direction = "vertical" if direction == "horizontal" else "horizontal"
	if in_frame(rows_lim, cols_lim, pos, frame_direction):
		#print("in frame")
		return True

	x, y = pos
	sides = [x-1, x+1] 	if direction == "horizontal" else [y-1, y+1]

	sides_obstacles = [obstacle for obstacle in obstacles if obstacle.position in sides]

	# if both sides are obstacles
	if len(sides_obstacles) == 2:
		return all([sides_are_walls(obstacle.pos, map_limits, [child for child in obstacle.children(True) if child.symbol == "#"], direction) for obstacle in sides_obstacles])

	return False
	
def in_frame(rows_lim, cols_lim, pos, frame_direction):
	x, y = pos
	checks = [x==0, x==rows_lim] if frame_direction == "vertical" else [y==0, y==cols_lim]
	return any(checks)