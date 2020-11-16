from astar import *

class Backtracking:
    def __init__(self, gridmap, state):
        self.gridmap = gridmap
        self.state = state
        self.boxes = state['boxes']         # refreshes every frame 
        self.keeper = state['keeper']

    def backtracking():
        visited = []
        options = []
        #solution = []
        for box in self.boxes:
            options = children_boxes(box, self.grimap)
            for option in options:
                if visited != []:
                    refresh_map()
                    visited.append(option)
                    options.pop()
                else:
                    if search(self.gridmap, self.keeper, oposite(self.grid, box, option), 'keeper') != []: # verifica se o path do keeper é possivel até à caixa
                    #se for possivel
                       # é deadlock?
                       visited.append(optionq)
                    else: 
                        # proxima caixa
                        options.pop()
                    













    #     # Verificação de solução possivel
    #     self.search_solution = True
    #     self.solution = []
    #     self.is_possible = False
        
    #     # Máquina de estados
    #     self.__state = self.search_state
        
    #     # Histórico de modificação ao gridmap
    #     self.gridmap_history = []

    # def set(self, boxes, goals):    
    #     self.box_priority = boxes # for now it goes first for boxes out of goal and after for boxes on top of goal 
    #     self.goal_priority = goals # for now it goes first for empty goals and after for goals with box on top

    # def has_solution(self):
    #     while(self.search_solution):
    #         status = self.__state()
    #         self.next_state(status)

    #     return self.is_possible        

    # def get_solution(self):
    #     return self.solution

    # def next_state(self, status):
    #     if self.__state == self.search_state:
    #         if status == False:
    #             #if len()>=0:
    #                 #state = traceback
    #             #else:
    #             self.__state = self.unstuck_state
    #         else:
    #             self.search_solution = False
    #             self.is_possible = True

    #     elif self.__state == self.unstuck_state:
    #         if status == True:
    #             self.__state = self.search_state
    #         else:
    #             self.search_solution = False
    #             self.is_possible = False
                
    #     #elif state is traceback_state:
    #     #    if traceback == None:
    #     #        state = unstuck_state
    #     #     else: 
    #     #         state = search_state 

    # def search_state(self):
    #     for i in range(0, len(self.box_priority)):
    #         box = self.box_priority[i]
    #         goal = self.goal_priority[i]
    #         path = search(self.gridmap, box, goal, 'boxes')
    #         print("Goal")
    #         print(goal.position)
    #         print("Caixa")
    #         print(box.position)
    #         print("PATH Caixa")
    #         for node in path:
    #             x, y = node.position
    #             print(x, y)

    #         path_keeper = None
    #         for j in range(0, len(path)-2):
    #             if j == 0:
    #                 x,y = self.astate['keeper']
    #                 keeper = self.gridmap[x][y]
    #             else: 
    #                 keeper = path[j-1]
                
    #             obj_box = path[j+1]
    #             box = path[j]
    #             node = oposite(self.gridmap, box, obj_box)
    #             path_keeper = search(self.gridmap, keeper, node, 'keeper')

    #             if path_keeper:
    #                 self.refresh_gridmap(box, obj_box, keeper, node)
    #                 box = obj_box
    #                 print("PATH KEEPER")
    #                 for node in path_keeper:
    #                     x, y = node.position
    #                     print(x, y)
    #             else:
    #                 print("Stuck")
    #                 print("Keeper")
    #                 print(keeper.position)
    #                 print("Box")
    #                 print(box.position)
                    
    #                 # obtem o caminho passando pela caixa existente
    #                 box = self.box_priority[1] if i == 0 else self.box_priority[0]
    #                 tmp = box.symbol 
    #                 box.symbol = '-'
    #                 self.desired_kpath = search(self.gridmap, keeper, node, 'keeper')
    #                 box_symbol = tmp

    #                 return False
        
    #     return True

    # #def traceback_state():

    # def unstuck_state(self):
    #     self.reset_gridmap()
    #     self.box_priority.reverse()
    #     self.goal_priority.reverse()
        
    #     box = self.box_priority[0]

    #     print("Nodes")   
    #     for n in children_boxes(box, self.gridmap):
    #         if n.position not in self.desired_kpath:    
    #             print("Objetivo")
    #             print(n.position)
    #             node = oposite(self.gridmap, box, n)
    #             path_keeper = search(self.gridmap, keeper, node, 'keeper')
    #             self.solution += path_keeper
    #             if path_keeper:
                    
    #                 return True

    #     return False

    # def refresh_gridmap(self, box, obj_box, keeper, obj_keeper):
    #     # guardar modificação ao gridmap
    #     modification_keeper = (keeper, obj_keeper)
    #     modification_box = (box, obj_box)
    #     self.gridmap_history.insert(0, [modification_keeper, modification_box])
        
    #     self.__trade_position(box, obj_box, keeper, obj_keeper)

    # def reset_gridmap(self):
    #     for move in self.gridmap_history:
    #         obj_keeper, keeper,  = move[0]
    #         obj_box, box  = move[1]
            
    #         self.__trade_position(box, obj_box, keeper, obj_keeper)

    # def __trade_position(self, box, obj_box, keeper, obj_keeper):
    #     # modificar keeper gridmap
    #     tmp = keeper.symbol
    #     keeper.symbol = obj_keeper.symbol
    #     obj_keeper.symbol = tmp

    #     # modificar box gridmap
    #     if box.symbol == '*':           
    #         box.symbol = '.'
    #         obj_box.symbol = '$'
    #     elif box.symbol == '.':
    #         box.symbol = '-'
    #         obj_box.symbol = '*'
    #     else:
    #         tmp = box.symbol
    #         box.symbol = obj_box.symbol
    #         obj_box.symbol = tmp
