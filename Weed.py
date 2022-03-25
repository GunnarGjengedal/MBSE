import numpy.random as random

#Weed class: Probability calculations for spawning and spreading of weeds
class Weed:
    random.seed(10)
  
    def __init__(self, GRIDSIZE):
        self.SpawnRate = (GRIDSIZE**2)/10000000
        self.SpreadRate = 0.05

   

    def weed_spawn(self):
        return (random.random() < self.SpawnRate)
  

    def weed_spread(self):
        return random.randint(0, 1000) < 100*self.SpreadRate

    