import numpy.random as random
#Robot class: In charge of removing detected weeds
class Robot:
    def __init__(self, GRIDSIZE, BaseStation, grid, RemovalRange,Speed):
        self.xpos = 0
        self.ypos = 0
        self.GRIDSIZE = GRIDSIZE
        self.grid = grid
        self.ChanceOfRemoval = 0.95
        self.Memory = []
        self.BaseStation = BaseStation
        self.Speed = Speed
        self.RemovalRange = RemovalRange
        self.Movement = 0
        self.GoingHome = False
        self.occupied = False
        self.recharging = False
        self.RemovedCell = None
        self.IdleTime = 0
        
        self.Target = None
        self.occupiedCol = None

        self.working_modes = ["recharging", "working", "going_home"]
        self.current_working_mode = "working"
      
        self.BatteryCap = 60*60*10
        self.BatteryLife = self.BatteryCap
        self.power_consumption_move = 1
        self.power_consumption_removal = 30
        self.power_recharge = 40

        self.energy_back_to_basestation,self.way = self.BaseStation.distance_between_robots_and_basestation(self.xpos, self.ypos, self.GRIDSIZE)
    #Updating robot state
    def Update(self):
        #Checks if robot is able to work, and has a target
        if self.current_working_mode == "working" and not self.Target:
            self.IdleTime += 1
        if(self.Movement < 1):
            self.Movement += self.Speed
        elif(self.Movement >= 1):
            self.SwitchWorkingMode()
            self.Movement -= 1
    #Updating robot state, Checks for battery life
    def SwitchWorkingMode(self):
        if self.current_working_mode == "recharging":
            if self.BatteryLife == self.BatteryCap:
                self.current_working_mode = "working"
                return


            self.Recharge()
        
        elif self.current_working_mode == "working":
            if not self.EnoughPowerGoingHome():
                self.current_working_mode = "going_home"
                return
            self.Working()

        elif self.current_working_mode == "going_home":
            if(self.xpos == 0 and self.ypos == 0): 
                self.current_working_mode = "recharging"
                return

            self.GoHome()
    #Function for movement of robot, only moves if it has a target
    def Working(self):
        if self.Target != None:
            if(self.ypos != self.Target[1]):
                if(self.xpos == 0 or self. xpos == self.GRIDSIZE-1):
                    if self.ypos < self.Target[1]:
                        self.ypos += 1
                    else:
                        self.ypos -=1 
                elif(self.xpos != 0 and self.xpos != self.GRIDSIZE-1):
                    if((self.GRIDSIZE-1) - self.xpos > self.GRIDSIZE//2):
                        self.xpos -=1
                    else:
                        self.xpos += 1
            elif self.ypos == self.Target[1]:
                if self.xpos < self.Target[0]:
                    self.xpos +=1
                else:
                    self.xpos -=1        
                                
            elif(self.xpos <= self.GRIDSIZE-1 and self.ypos%2 == 1):
                if(self.xpos == 0):
                    self.ypos += 1
                else:
                    self.xpos -= 1  
        
            self.PowerConsume(self.power_consumption_move)
                
            self.RemoveWeed()      

    #Robot going back for recharge. Shortest way possible     
    def GoHome(self):
        if(self.xpos > 0):
            if self.way == 1:
                self.xpos -= 1
            else:
                self.ypos +=1
        elif(self.ypos > 0):
            self.ypos -= 1
     #Checks batterylife, if robot can go home   
    def BatteryCheck(self):
        if((self.xpos + self.ypos) <= self.BatteryLife):
            self.GoingHome = True
    #Calculating whether or not robot fails in removing weed
    def CanRemove(self):
        return (random.randint(0, 100) < 100*self.ChanceOfRemoval)
    #Weed removal, robot removes weeds from specified number of cells
    #Also updates the basestation on location of removed weeds
    def RemoveWeed(self):
        if (self.xpos,self.ypos) == self.Target:
            if self.CanRemove():
                self.grid[self.xpos][self.ypos].RemoveWeed()
                self.BaseStation.removeWeedLoc(self.Target)
                self.RemovedCell = self.grid[self.xpos][self.ypos]
                self.Target = None
                
                
                for i in range(1,self.RemovalRange):
                    if self.ypos + i >= self.GRIDSIZE or self.ypos - i  < 0:
                        continue
                    self.grid[self.xpos][self.ypos+i].RemoveWeed()
                    self.grid[self.xpos][self.ypos-i].RemoveWeed()
                    self.grid[self.xpos][self.ypos+i].Detected = False
                    self.grid[self.xpos][self.ypos-i].Detected = False 
                    if(self.xpos in self.BaseStation.WeedLocations and self.ypos-i in self.BaseStation.weed_columns):
                        self.BaseStation.removeWeedLoc((self.xpos,self.ypos-i))
                        print('1')
                    if(self.xpos in self.BaseStation.WeedLocations and self.ypos+i in self.BaseStation.weed_columns):
                        self.BaseStation.removeWeedLoc((self.xpos,self.ypos+i))
                        print('2')
                
                    
                self.Target = None
            
                            
                  
        

            if len(self.BaseStation.weed_columns[self.occupiedCol]) > 0:
                self.Target = self.BaseStation.weed_columns[self.occupiedCol][0]
            else:
                self.Target = None
            self.PowerConsume(self.power_consumption_removal)
        else:
            self.RemovedCell = None
    #Robot consumes the ammount of battery its actions demand
    def PowerConsume(self, amount):
        self.BatteryLife -= amount
        
    #Robot recharges its batteries
    def Recharge(self):
        self.BatteryLife = min(self.BatteryLife + self.power_recharge, self.BatteryCap)
           
    #Makes sure robot has enough powe to get back to base
    def EnoughPowerGoingHome(self):
        distance,way =  self.BaseStation.distance_between_robots_and_basestation(self.xpos, self.ypos, self.GRIDSIZE)
        power_to_home = self.power_consumption_move * distance
        
        remain_power = self.BatteryLife - self.power_consumption_removal

        return remain_power > power_to_home
    #Defines whether robot is ready for new task, and tells basestation the current column.
    #Ensuring two robots arent assigned weeds in same column
    def ReadyForNewTasks(self):
        if self.current_working_mode != "working" :
            return False
        if self.Target == None:
            return True
        if self.occupiedCol:
            return len(self.BaseStation.weed_columns[self.occupiedCol]) == 0
        
            

    def SetWeedList(self,  col):
        self.occupied = True
        self.occupiedCol = col
        self.Target = self.BaseStation.weed_columns[self.occupiedCol][0]

   
             
    