import numpy as np
#Basestation class: essentially in charge of taskplanning, and keeping track of field state
class BaseStation:
    def __init__(self,grid):
        self.TreatedCells = []
        self.HasTasks = False
        self.grid = grid
        self.WeedLocations = [[] for i in range(len(grid)) ]
        
        self.occupiedColumns = [False for i in range(len(grid))]
        self.weed_columns = [[] for i in range(len(grid)) ]

    def registerRobots(self, robots_list):
        self.robots_list = robots_list
        
#Gives task if there is known weedlocations not being treated, Treats the oldest detected weed
    def GiveTask(self):
        for robot in self.robots_list:
            if self.getMaxWeedNotOccupied(robot) == 0:
                return 
            if robot.ReadyForNewTasks():
                col = self.getMaxWeedNotOccupied(robot)
                if robot.occupiedCol:
                    self.occupiedColumns[robot.occupiedCol] = False
                self.occupiedColumns[col] = True
                robot.SetWeedList(col)

    def appendWeedLoc(self, weedCoord):
        x_coord = weedCoord[0]
        y_coord = weedCoord[1]
        self.WeedLocations[x_coord].append(weedCoord)
        self.weed_columns[y_coord].append(weedCoord)


    def removeWeedLoc(self, weedCoord):
        x_coord = weedCoord[0]
        y_coord = weedCoord[1]
        self.weed_columns[y_coord].remove(weedCoord)
        self.WeedLocations[x_coord].remove(weedCoord)
        


    def getMaxWeedNotOccupied(self, robot):
        maximum = 0
        max_col = 0
        list_len = [len(i) for i in self.weed_columns]
        for i in range(len(self.occupiedColumns)):
            if self.occupiedColumns[i] == False or robot.ypos == i:
                if list_len[i] > maximum:
                    maximum = list_len[i]
                    max_col = i


        return max_col

        
    #The energy required for robots to go home
    def distance_between_robots_and_basestation(self,target_x,target_y,gridsize):
        distance1 = target_x
        distance2 = gridsize-target_x
        if(distance1<=distance2):
            mindistance = distance1+target_y
            way=1
        else:
            mindistance = distance2+target_y+gridsize
            way=2
        return mindistance,way
    ##The energy required for drones to go home
    def distance_between_drones_and_basestation(self, target_x, target_y, gridsize):
        #The drone walks diagonally
        if(target_x<=target_y):
            distance=target_x*2+(target_y-target_x)
            way=1
        else:
            distance=target_y*2+(target_x-target_y)
            way=2
        return distance,way
