"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
from numpy.core.fromnumeric import trace
import pygame
import numpy.random as random
import matplotlib.pyplot as plt
from Drone import Drone
from Cell import Cell
from BaseStation import BaseStation
from Robot import Robot
from Weed import Weed

#Making sure each simulation is ran with the same random seed
random.seed(181)

#Functions
def addInfectedCell(cell):
    if grid[cell.xpos][cell.ypos].NumSeeds == 1 and grid[cell.xpos][cell.ypos].NumWeeds == 0:
        infectedCells.add(cell)
def YieldLossCheck():
    for row in range(GRIDSIZE):
        for column in range(GRIDSIZE):
            grid[row][column].RemoveWeed()


print('Experiment specification')
print('________________________________________________________________')
Num_good_robots = int(input('Specify number of good robots(int): '))
print('________________________________________________________________')
num_bad_robots = int(input('Specify number of bad robots(int): '))

print('________________________________________________________________')
num_drones = int(input('Specify number of drones(int): '))
print('________________________________________________________________')
GRIDSIZE = int(input('Specify size of field(m^2): '))
print('________________________________________________________________')
testname = input('Input filename for experiment: ')
print('________________________________________________________________')
print('Starting Test')
lifetime_of_weeds = []
data = []
good_bot_str = str(Num_good_robots)
bad_bot_str = str(num_bad_robots)
drone_str = str(num_drones)

GRIDSIZE_str = str(GRIDSIZE)
#Specifying field size for test

TotalYield = (GRIDSIZE-1)**2

# Colors for visualization
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 180)
YELLOW = (255,255,0)
SKYBLUE = (0,255,255)
PURPLE = (240,0,255)
GREY = (112,112,112)
ORANGE = (255,165,0)


#Parameters for visualization
WIDTH = 2
HEIGHT = 2
MARGIN = 1
WINDOWHEIGHT = HEIGHT*GRIDSIZE+GRIDSIZE
WINDOWWIDTH = WIDTH*GRIDSIZE+(GRIDSIZE*MARGIN)





 
#Creating the list of list which makes up the field
grid = []
for row in range(GRIDSIZE):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(GRIDSIZE):
        grid[row].append(Cell(row, column, lifetime_of_weeds))  # Append a cell
 

# Initialize pygame, used for visualization
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WINDOWWIDTH, WINDOWHEIGHT]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Simulation")
 
#Variable specification, and class initialization


bs = BaseStation(grid)

done = False
#Specifying parameter for good and bad robot/drone
#bad robot: 0.2 m/S movespeed, removes 1 adjacent weed
bad_robot = Robot(GRIDSIZE, bs, grid,2, 0.2)
#Good robot: 0.5 m/s movespeed, removes 2 adjacent weeds
good_robot = Robot(GRIDSIZE, bs, grid,3, 0.5)






infectedCells = set()
SimTime = 1080
old_tick = 0
sample_interval = 9999
clock = pygame.time.Clock()

#Initializes specified number of drones
drones = []
for i in range(num_drones):
    drones.append(Drone(GRIDSIZE,bs,grid,(GRIDSIZE-1)//(i+1),(GRIDSIZE-1)//(i+1),45*60,3))
   


#Initializing specifyed number of good and bad robots
good_robots = [Robot(GRIDSIZE, bs, grid,3, 0.5)for i in range(Num_good_robots)]

bad_robots = [Robot(GRIDSIZE, bs, grid,2, 0.2) for i in range(num_bad_robots)]

robots = good_robots + bad_robots



bs.registerRobots(robots)
weed = Weed(GRIDSIZE)
draw = False
count = 0
numHours = 0
# -------- Main Program Loop -----------
while not done and numHours <= SimTime:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = True  
    for drone in drones:
        grid[drone.xpos][drone.ypos].Drone = False
        drone.Update()
        distance=bs.distance_between_drones_and_basestation(drone.xpos,drone.ypos,GRIDSIZE)
        grid[drone.xpos][drone.ypos].Drone = True
       
    bs.GiveTask()
    for robot in robots:
        grid[robot.xpos][robot.ypos].Robot = False
      
        
        robot.Update()

        if robot.RemovedCell:
            if(robot.RemovedCell in infectedCells):
                infectedCells.remove(robot.RemovedCell)
            robot.RemovedCell = None
        # calculate the min distance(the amount of the energy they need) to come back to the basestation
        min_distance = bs.distance_between_robots_and_basestation(robot.xpos, robot.ypos, GRIDSIZE)
        grid[robot.xpos][robot.ypos].Robot = True

    #Weed spawns at random location
    if weed.weed_spawn():
        x = random.randint(1,GRIDSIZE-1)
        y = random.randint(1,GRIDSIZE-1)
        grid[x][y].AddSeed()
        if grid[x][y].NumSeeds == 1 and grid[x][y].NumWeeds == 0:
            infectedCells.add(grid[x][y])


    
    # only update detected cells, the rest dont change
    #Updates every 10 seconds, improving runtime
    if count % 30 == 0:
        for cell in set(infectedCells):
            cell.Update()
            if cell.NumWeeds > 0 and cell.Spread:
                if weed.weed_spread():
                    if cell.xpos >= 2:
                        grid[cell.xpos-1][cell.ypos].AddSeed()
                        addInfectedCell(grid[cell.xpos-1][cell.ypos])
                    if cell.xpos <= GRIDSIZE-3:
                        grid[cell.xpos+1][cell.ypos].AddSeed()
                        addInfectedCell(grid[cell.xpos+1][cell.ypos])
                    if cell.ypos >= 2:
                        grid[cell.xpos][cell.ypos-1].AddSeed()
                        addInfectedCell(grid[cell.xpos][cell.ypos-1])
                    if cell.ypos <= GRIDSIZE-3:
                        grid[cell.xpos][cell.ypos+1].AddSeed()
                        addInfectedCell(grid[cell.xpos][cell.ypos+1])
            if cell.NumSeeds == 0 and cell.NumWeeds == 0:
                infectedCells.remove(cell)
    #Timer, equals to 1 second
    count += 1
    #Runs check on the field every hour, saves status to data list.
    #Additionally draws the field, in order to monitor status
    if count % 3600 == 0:
        numHours += 1
        print(numHours, len(infectedCells))
        if numHours >= SimTime:
            YieldLossCheck()
        yield_loss = 0
        for row in range(GRIDSIZE):
            for column in range(GRIDSIZE):
                if grid[row][column].Alive == False:
                    yield_loss += 1
                else:
                    yield_loss += grid[row][column].Yield_loss_actual
        robotIdleTime = 0
        for robot in robots:
            robotIdleTime += robot.IdleTime
            robot.IdleTime = 0
        robotIdleTime = robotIdleTime/len(robots)          
        if lifetime_of_weeds:
            data.append([numHours,TotalYield - yield_loss, sum(lifetime_of_weeds)/len(lifetime_of_weeds), robotIdleTime])
        else:
            data.append([numHours,TotalYield - yield_loss, 0, robotIdleTime])
        lifetime_of_weeds.clear()
        screen.fill(BLACK)
        test = 0
        for row in range(GRIDSIZE):
            for column in range(GRIDSIZE): 

                color = WHITE
                for drone in drones:
                    if(row>=drone.xpos-drone.Speed and row<=drone.xpos+ drone.Speed and column >= drone.ypos-drone.ScanRadius and column<= drone.ypos+drone.ScanRadius):
                        color = ORANGE
                        
                if row == GRIDSIZE-1 or row == 0 or column == 0 or column == GRIDSIZE-1:
                    color = YELLOW
            
                
                if grid[row][column].Drone:
                    color = GREEN
                    
                elif grid[row][column].Robot:
                    color = BLUE
                elif(row == 0 and column == 0): 
                    color = SKYBLUE
                elif not grid[row][column].Alive:
                    color = BLACK
                elif grid[row][column].Detected:
                    color = PURPLE
                elif grid[row][column].NumWeeds > 0:
                    color = RED
                elif grid[row][column].NumSeeds > 0:
                    color = GREY

                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (HEIGHT + 1) * row + 1,
                                WIDTH,
                                HEIGHT])
                if grid[row][column].Robot:
                    pygame.draw.circle(screen,
                                color,
                                ((MARGIN + WIDTH) * column, (HEIGHT + 1) * row + 1),
                                5
                                )
        
                elif grid[row][column].Detected:
                    pygame.draw.circle(screen,
                                PURPLE,
                                ((MARGIN + WIDTH) * column, (HEIGHT + 1) * row + 1),
                                2
                                )
        
  
        #Pygame variable
        clock.tick(50000)
    
        # Updates the screen with what
        pygame.display.flip()


# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
import csv
import os
import matplotlib.pyplot as plt

#Saving test results to csv file
dir = os.getcwd()

path = os.path.join(dir,'TestResults')
if not os.path.exists(path):
    os.makedirs(path)
os.chdir(path)
filename = testname
# open the file in the write mode
f = open(filename, 'w')
header = ['Number of Hours','Yield loss', 'Avg lifetime of weeds', 'Robot idle time']
# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerow(header)
writer.writerows(data)


#Also creates plot instantly to gauge performance of current setup
time_x = [i+1 for i in range(numHours)]
def plot_chart(time_x, lst, y_label):
    print(len(time_x),len(lst))
    plt.scatter(time_x, lst)
    plt.title(testname)
    plt.ylabel( y_label)
    plt.xlabel ("hour") 
    plt.show()

trans_data = list(map(list, zip(*data)))
for i in range(len(trans_data)):
    plot_chart(time_x, trans_data[i], header[i])
# close the file
f.close()

pygame.quit()