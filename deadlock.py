class DeadlockAgent:
	def __init__(self, position, adjacents, unwanted_symbols):
		self.position = position
		self.adjacents = adjacents
		self.unwanted_symbols = unwanted_symbols
		self.obstacles = [adjacent.position for adjacent in adjacents if adjacent.symbol in unwanted_symbols]

	def set_unwanted_symbols(self, unwanted_symbols):
		self.unwanted_symbols = unwanted_symbols
		self.obstacles = [adjacent.position for adjacent in self.adjacents if adjacent.symbol in unwanted_symbols]

	def get_unwanted_symbols(self):
		return self.unwanted_symbols

	def check_all_deadlocks(self):
		return any([function(self) for name, function in DeadlockAgent.__dict__.items() if callable(function) and name not in ["__init__", "check_all_deadlocks", "set_unwanted_symbols", "get_unwanted_symbols"]])

	def deadlock_corner(self):
		x, y = self.position
		pairs = [[(x-1, y), (x, y+1)], [(x, y+1), (x+1, y)], [(x+1, y), (x, y-1)], [(x, y-1), (x-1, y)]]
		return any([all(square in self.obstacles for square in pair) for pair in pairs])