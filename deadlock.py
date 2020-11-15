class DeadlockAgent:
	def __init__(self, position, adjacents, unwanted_symbols):
		self.position = position
		self.obstacles = [adjacent.position for adjacent in adjacents if adjacent.symbol in unwanted_symbols]

	def check_all_deadlocks(self):
		return any([self.deadlock_corner()])

	def deadlock_corner(self):
		x, y = self.position
		pairs = [[(x-1, y), (x, y+1)], [(x, y+1), (x+1, y)], [(x+1, y), (x, y-1)], [(x, y-1), (x-1, y)]]
		return any([all(square in self.obstacles for square in pair) for pair in pairs])

# # main function that checks for obstacles in both sides of the given square
# def opp_sides_blockage(mapa, pos, obstacles, side_info):
#     rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
#     # if has reached a place in the frame, then it is blocked
#     if in_frame(rows_lim, cols_lim, pos):
#         print(f"WARNING: {pos} is in frame!")
#         return True
    
#     print(f"[opp_side] CHECKING POS{pos}:")
#     x, y = pos[0], pos[1]
#     pos1_obst, pos2_obst, sides = [], [], []
#     if side_info == "horizontal":
#         s1, s2 = "l", "r"
#         sides = [x-1, x+1]
#     else:
#         s1, s2 = "t", "b"
#         sides = [y-1, y+1]
#     # loops through both sides
#     for side in sides:
#         if side_info == "horizontal":
#             sides_pos = [(side, y), (side, y-1), (side, y+1)]
#         else:
#             sides_pos = [(x, side), (x-1, side), (x+1, side)]

#         # loops through each obstacle for each side
#         for obst in obstacles:
#             # if obstacle is in one of the sides
#             if obst in sides_pos:
#                 # if is the first side
#                 if side == x-1:
#                     pos1_obst.append(obst)
#                 # if is the second side
#                 else:
#                     pos2_obst.append(obst)

#     print("pos1", pos1_obst)
#     print("pos2", pos2_obst)
#     # if there is atleast one obstacle on both sides
#     if len(pos1_obst) > 0 and len(pos2_obst) > 0:
#         checks1 = [side_blockage(mapa, obst, obstacles_around(mapa, obst), s1) for obst in pos1_obst]
#         checks2 = [side_blockage(mapa, obst, obstacles_around(mapa, obst), s2) for obst in pos2_obst]
#         return atleast_one_true(checks1) and atleast_one_true(checks2)
#     else:
#         return False

# # recursive function that checks for obstacles in a specific side until it hits frame or no obstacles
# def side_blockage(mapa, pos, obstacles, side_info):
#     rows_lim, cols_lim = len(mapa)-1, len(mapa[0])-1
#     # if has reached a place in the frame, then it is blocked
#     if in_frame(rows_lim, cols_lim, pos):
#         print(f"WARNING: {pos} is in frame!")
#         return True
    
#     print(f"[side] CHECKING POS{pos}:")
#     x, y = pos[0], pos[1]
#     pos_obst = []
#     if side_info == "l":
#         side = x-1
#         sides_pos = [(side, y), (side, y-1), (side, y+1)]
#     elif side_info == "t":
#         side = y-1
#         sides_pos = [(x, side), (x-1, side), (x+1, side)]
#     elif side_info == "r":
#         side = x+1
#         sides_pos = [(side, y), (side, y-1), (side, y+1)]
#     else:
#         side = y+1
#         sides_pos = [(x, side), (x-1, side), (x+1, side)]

#     for obst in obstacles:
#         # if obstacle is in one of the sides
#         if obst in sides_pos:
#             pos_obst.append(obst)
        
#     print("pos", pos_obst)

#     return atleast_one_true([side_blockage(mapa, obst, obstacles_around(mapa, obst), side_info) for obst in pos_obst])