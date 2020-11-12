from astar import *

class Approach:
    def __init__(self, gridmap, astate):            
        self.gridmap = gridmap
        self.astate = astate

    def set(self, boxes, goals):
        pass

    def has_solution(self):
        pass

    def get_solution(self):
        pass

class DeadLock(Approach): 
    def __init__(self, gridmap, astate):
        super().__init__(gridmap, astate)
        
        # Verificação de solução possivel
        self.search_solution = True
        self.solution = []
        self.is_possible = False
        
        # Máquina de estados
        self.__state = self.search_state
        
        # Histórico de modificação ao gridmap
        self.gridmap_history = []

    def set(self, boxes, goals):    
        self.box_priority = boxes # for now it goes first for boxes out of goal and after for boxes on top of goal 
        self.goal_priority = goals # for now it goes first for empty goals and after for goals with box on top

    def has_solution(self):
        while(self.search_solution):
            status = self.__state()
            self.next_state(status)

        return self.is_possible        

    def get_solution(self):
        return self.solution

    def next_state(self, status):
        if self.__state == self.search_state:
            if status == False:
                #if len()>=0:
                    #state = traceback
                #else:
                self.__state = self.unstuck_state
            else:
                self.search_solution = False
                self.is_possible = False # deve ser true

        elif self.__state == self.unstuck_state:
            self.__state = self.search_state
                
        #elif state is traceback_state:
        #    if traceback == None:
        #        state = unstuck_state
        #     else: 
        #         state = search_state 

    def search_state(self):
        for i in range(0, len(self.box_priority)):
            box = self.box_priority[i]
            goal = self.goal_priority[i]
            path = search(self.gridmap, box, goal, 'boxes')
            print("Goal")
            print(goal.position)
            print("Caixa")
            print(box.position)
            print("PATH Caixa")
            for node in path:
                x, y = node.position
                print(x, y)

            path_keeper = None
            for i in range(0, len(path)-2):
                if i == 0:
                    x,y = self.astate['keeper']
                    keeper = self.gridmap[x][y]
                else: 
                    keeper = path[i-1]
                
                obj_box = path[i+1]
                box = path[i]
                node = oposite(self.gridmap, box, obj_box)
                path_keeper = search(self.gridmap, keeper, node, 'keeper')

                if path_keeper:
                    self.refresh(box, obj_box, keeper, node)
                    box = obj_box
                    print("PATH KEEPER")
                    for node in path_keeper:
                        x, y = node.position
                        print(x, y)
                else:
                    print("Stuck")
                    print("Keeper")
                    print(keeper.position)
                    print("Box")
                    print(box.position)
                    break
        
        return True

    #def traceback_state():

    def unstuck_state(self):
        pass

    def refresh(self, box, obj_box, keeper, obj_keeper):
        # guardar modificação ao gridmap
        modification_keeper = (box, obj_box)
        modification_box = (keeper, obj_keeper)
        self.gridmap_history.append([modification_keeper, modification_box])

         # modificar keeper gridmap
        tmp = keeper.symbol
        keeper.symbol = obj_keeper.symbol
        obj_keeper.symbol = tmp

        # modificar box gridmap
        tmp = box.symbol
        box.symbol = obj_box.symbol
        obj_box.symbol = tmp