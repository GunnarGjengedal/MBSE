class Cell:
    #Cell class: Holding a crop, and handling its state
    def __init__(self, xpos, ypos, Lifetime):
        self.GrowthSpeed = 1
        self.Health = 100
        
        self.NumWeeds = 0
      
        self.Nc = 5 # Crops per. square
        self.bc0 = 6.18 # Intercept
       
        self.a0 = 134.7 #Competition metric between Maize and Echinochloa weed.
        self.bcw = 2 # measure interspecific  competition  effects  between  the  species
        self.a = self.bcw/self.a0 #Yield loss caused by a single weed in crop during a growth cycle
        
        self.yield_loss = 0
        self.yield_loss_previous = 0
        self.Yield_loss_actual = 0
        self.Alive = True
        self.Drone = False
        self.Robot = False
        self.Detected = False
        self.xpos = xpos
        self.ypos = ypos
        self.NumSeeds = 0
        self.Germination = 0
        self.WeedGrowth = 0
        self.ToDays = 43200
        self.GerminationRate = 7 #15
        self.GrowthRate = 5 #7
        self.Spread = False
        self.WeedLifetime = 0
        self.Lifetime = Lifetime
    #Checks if cell state has changed
    def Update(self):
        if self.NumSeeds > 0:
            self.Germination += 30
            if self.Germination >= self.GerminationRate * self.ToDays:
                self.NumWeeds += 1 * self.NumSeeds
                self.Germination = 0
                self.NumSeeds = 0
        
        if self.NumWeeds > 0:
            self.WeedLifetime += 30
            self.WeedGrowth += 30
            if self.WeedGrowth >= self.GrowthRate * self.ToDays:
                self.Spread = True
                self.WeedGrowth = 0
            if self.yield_loss_previous > 0:
                self.yield_loss = self.yield_loss_previous + self.a * self.NumWeeds / (1 + self.a * self.NumWeeds) #Yield loss calculation
            else:
                self.yield_loss = self.a * self.NumWeeds / (1 + self.a * self.NumWeeds) #Yield loss calculation
            if self.yield_loss > 0.89:
                self.Alive = False
          
            
    #Weed removal function, also updates the cell with its current yield loss
    def RemoveWeed(self):
        
        self.Lifetime.append(self.WeedLifetime)
        if self.yield_loss_previous > 0:
            self.yield_loss = self.yield_loss_previous + self.a * self.NumWeeds / (1 + self.a * self.NumWeeds)
        else:
            self.yield_loss = self.a * self.NumWeeds / (1 + self.a * self.NumWeeds) 
        
        self.yield_loss_previous = self.yield_loss
        self.Yield_loss_actual = self.yield_loss*(self.WeedLifetime/(43200*120))
        self.NumWeeds = 0
        self.Detected = False
        
    #Simple functions to add weeds, end check for weeds
    def AddSeed(self):
        self.NumSeeds += 1
    

    def CanWeeding(self):
        return self.NumWeeds > 0
    