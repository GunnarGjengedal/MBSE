import numpy.random as random
#Drone class: Flying over the field and scanning for weeds
class Drone:

    random.seed(181)
    
    def __init__(self, GRIDSIZE, BaseStation, grid, xpos, ypos, BatteryCapacity, Speed):
        self.xpos = xpos
        self.ypos = ypos
        self.GRIDSIZE = GRIDSIZE
        self.grid = grid
        self.Memory = []
        self.BaseStation = BaseStation
        self.BatteryCapacity = BatteryCapacity
        self.BatteryLife = self.BatteryCapacity
      
        self.detectRange = 1
        self.DetectionRate = 0.95
        self.Movement = 0
        self.Speed = Speed
        self.Return = False
        self.Home = False
        self.GoingHome = False
        self.ScanRadius = self.Speed -self.Speed//2
   

        self.GoingBack = False
        self.GoBehind=True
        self.GoLeft=False
        self.GoAhead = True
        self.GoRight = False
        self.GoBackLocation=[]

        self.energy_back_to_basestation= self.BaseStation.distance_between_drones_and_basestation(self.xpos,self.ypos,self.GRIDSIZE)
    #Updating drone state, moving it across the field
    def Update(self):
        self.BatteryLife -= 1
        if((self.xpos == self.GRIDSIZE-1 and self.ypos == self.GRIDSIZE-1) or (self.BatteryLife<=self.energy_back_to_basestation[0] and self.GoingHome == False)):
            if (self.BatteryLife<=self.energy_back_to_basestation[0]):
                self.GoBackLocation.append(self.xpos)
                self.GoBackLocation.append(self.ypos)
            else:
                self.GoBackLocation.append(0)
                self.GoBackLocation.append(0)
            self.GoingHome = True
            
        if(self.xpos == 0 and self.ypos == 0 and self.GoingHome == True): 
            self.GoingHome = False
        if(self.GoingHome):
            self.GoHome()
            return
        elif (self.GoingBack):
            self.GoBackToWork()
            return
        elif(self.GRIDSIZE-1 -self.xpos <= self.Speed and self.GRIDSIZE-1 -self.ypos <= self.Speed):
            if self.xpos == self.GRIDSIZE -1:
                self.ypos += 1
            else:
                self.xpos += 1    

        elif(self.xpos <= self.GRIDSIZE-1 and self.ypos%2 == 0 and self.Return == False):
            
            if(self.xpos == self.GRIDSIZE-1):
                self.ypos += self.Speed
            elif self.xpos >= self.GRIDSIZE-self.Speed-1:
                self.xpos += self.GRIDSIZE-1-self.xpos
            else:
                self.xpos += self.Speed
            
        elif(self.xpos <= self.GRIDSIZE-1 and self.ypos%2 == 1 and self.Return == False):
            if(self.xpos == 0):
                self.ypos += self.Speed
            elif self.xpos <= self.Speed+1:
                self.xpos-= self.xpos
            
            else:
                self.xpos -= self.Speed

        self.ScanCell()
    #Function for going home. Drone flyes, so it can move diagonally across the field. 
    #Going home as fast as possible
    def GoHome(self):
        if self.xpos == 0:
            if self.ypos <= self.Speed:
                self.ypos -= 1
            else:
                self.ypos -= self.Speed
        elif self.ypos == 0:
            if self.xpos <= self.Speed:
                self.xpos -= 1
            else:
                self.xpos -= self.Speed
        elif(self.GoBehind):
            if self.xpos <= self.Speed:
                self.xpos -= self.xpos
            else:
                self.xpos -= self.Speed
            if (self.ypos != 0):
                self.GoBehind=False
                self.GoLeft=True
        elif (self.GoLeft):
            if self.ypos <= self.Speed:
                self.ypos -= self.ypos
            else:
                self.ypos -= self.Speed
            if (self.xpos != 0):
                self.GoLeft = False
                self.GoBehind =True
        if (self.xpos == 0 and self.ypos == 0):
        
            self.GoingHome = False
            self.GoingBack = True
            self.GoBehind=True
            self.GoLeft=False
            self.BatteryLife = self.BatteryCapacity
       
    #Drone goes back to the last "searched" location
    def GoBackToWork(self):
        if (self.xpos == self.GoBackLocation[0] and self.ypos == self.GoBackLocation[1]):
            self.GoingBack = False
            self.GoAhead = True
            self.GoRight = False
            self.GoBackLocation=[]
        elif (self.GoAhead):
            if self.GoBackLocation[0] - self.xpos <= self.Speed:
                self.xpos += 1
            else:
                self.xpos += self.Speed
            if (self.ypos != self.GoBackLocation[1]):
                self.GoAhead=False
                self.GoRight=True
        elif (self.GoRight):
            if self.GoBackLocation[1] - self.ypos <= self.Speed:
                self.ypos += 1
            else:
                self.ypos += self.Speed
            if (self.xpos != self.GoBackLocation[0]):
                self.GoRight = False
                self.GoAhead =True
        


    #Weed detection
    def ScanCell(self):
        for xpos in range(self.xpos-self.ScanRadius-1,self.xpos+self.ScanRadius+1):
            if xpos >=0 and xpos < self.GRIDSIZE:
                for ypos in range(self.ypos-self.ScanRadius-1,self.ypos+self.ScanRadius+1):
                    if ypos >=0 and ypos < self.GRIDSIZE:
                        if self.CanDetectWeed() and self.grid[xpos][ypos].CanWeeding():
                            if self.grid[xpos][ypos].Detected == False:
                                weedCoord = (xpos, ypos)
                                self.BaseStation.appendWeedLoc(weedCoord)
                                self.grid[xpos][ypos].Detected = True
    #Calculation on wether or not weed is detected
    def CanDetectWeed(self):
        return (random.randint(0, 100) < 100*self.DetectionRate)

    