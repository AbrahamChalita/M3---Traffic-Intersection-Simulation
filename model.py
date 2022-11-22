import mesa
from mesa import Model
from agent import vehicle, semaphore, cell, wall
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from collections import deque

class street(Model):
    def __init__(self, width, height):
        self.semaphores = 4
        self.grid = MultiGrid(width, height, True)
        self.idCounter = 1       
        self.timeStep = 0 
        self.schedule = RandomActivation(self)
        self.running = True
        self.priority = deque()
        self.trafficFlow = 0
        self.crashes = 0
        
        self.totalSpawned = 0
        
        semaphore1 = semaphore(self.idCounter, self, "South")
        self.grid.place_agent(semaphore1, (15, 18))
        self.idCounter += 1
        
        semaphore2 = semaphore(self.idCounter, self, "East")
        self.grid.place_agent(semaphore2, (15, 15))
        self.idCounter += 1
        
        semaphore3 = semaphore(self.idCounter, self, "North")
        self.grid.place_agent(semaphore3, (18, 15))
        self.idCounter += 1
        
        semaphore4 = semaphore(self.idCounter, self, "West")
        self.grid.place_agent(semaphore4, (18, 18))
        self.idCounter += 1
        
        self.semaphore1 = semaphore1
        self.semaphore2 = semaphore2
        self.semaphore3 = semaphore3
        self.semaphore4 = semaphore4
        
        self.semaphores = [self.semaphore1, self.semaphore2, self.semaphore3, self.semaphore4]
        
        for i in self.semaphores:
            self.schedule.add(i)
        
        """self.schedule.add(semaphore1)
        self.schedule.add(semaphore2)
        self.schedule.add(semaphore3)
        self.schedule.add(semaphore4)"""
        
    
        cell1 = cell(self.idCounter, self, "semaphore", self.semaphore2)
        self.idCounter += 1
        cell2 = cell(self.idCounter, self, "semaphore", self.semaphore3)
        self.idCounter += 1
        cell3 = cell(self.idCounter, self, "semaphore", self.semaphore4)
        self.idCounter += 1
        cell4 = cell(self.idCounter, self, "semaphore", self.semaphore1)
        self.idCounter += 1
        
        self.schedule.add(cell1)
        self.schedule.add(cell2)
        self.schedule.add(cell3)
        self.schedule.add(cell4)
        
        self.grid.place_agent(cell1, (15, 16))
        self.grid.place_agent(cell2, (17, 15))
        self.grid.place_agent(cell3, (18, 17))
        self.grid.place_agent(cell4, (16, 18))
        
        self.listStops = [cell1, cell2, cell3, cell4]
        
        for i in range(0, 33):
            if not(i > 14 and i < 19):
                wall1 = wall(self.idCounter, self)
                self.idCounter += 1
                self.schedule.add(wall1)
                self.grid.place_agent(wall1, (i, 15))
                
                wall2 = wall(self.idCounter, self)
                self.idCounter += 1
                self.schedule.add(wall2)
                self.grid.place_agent(wall2, (i, 18))
            
            if not(i > 14 and i < 19):
                wall3 = wall(self.idCounter, self)
                self.idCounter += 1
                self.schedule.add(wall3)
                self.grid.place_agent(wall3, (15, i))
                
                wall4 = wall(self.idCounter, self)
                self.idCounter += 1
                self.schedule.add(wall4)
                self.grid.place_agent(wall4, (18, i))
        
        intersection1 = cell(self.idCounter, self, "intersection", semaphore1)
        self.idCounter += 1
        intersection2 = cell(self.idCounter, self, "intersection", semaphore2)
        self.idCounter += 1
        intersection3 = cell(self.idCounter, self, "intersection", semaphore3)
        self.idCounter += 1
        intersection4 = cell(self.idCounter, self, "intersection", semaphore4)
        self.idCounter += 1
        
        self.schedule.add(intersection1)
        self.schedule.add(intersection2)
        self.schedule.add(intersection3)
        self.schedule.add(intersection4)
        
        self.grid.place_agent(intersection1, (16, 17))
        self.grid.place_agent(intersection2, (16, 16))
        self.grid.place_agent(intersection3, (17, 16))
        self.grid.place_agent(intersection4, (17, 17))
        
        entrance1 = cell(self.idCounter, self, "entrance", semaphore1)
        self.idCounter += 1
        entrance2 = cell(self.idCounter, self, "entrance", semaphore2)
        self.idCounter += 1
        entrance3 = cell(self.idCounter, self, "entrance", semaphore3)
        self.idCounter += 1
        entrance4 = cell(self.idCounter, self, "entrance", semaphore4)
        self.idCounter += 1
        
        self.schedule.add(entrance1)
        self.schedule.add(entrance2)
        self.schedule.add(entrance3)
        self.schedule.add(entrance4)
        
        self.grid.place_agent(entrance1, (16, 28))
        self.grid.place_agent(entrance2, (4, 16))
        self.grid.place_agent(entrance3, (17, 4))
        self.grid.place_agent(entrance4, (28, 17))
        
        
        self.datacollector = mesa.DataCollector(
            model_reporters= { 'Crashes': lambda m: m.crashes,
                              'Flow': lambda m: m.trafficFlow,}
        )
            
    
    def add_vehicles(self):
        start1, start2, start3, start4 = random.choices(population=[True, False], weights=[0.1, 0.9], k=4)
        
        if(start1):
            if len(self.semaphore3.total) >= 14:
                return
            else:
                car = vehicle(self.idCounter, self, self.semaphore3, (17, 0), "North", "black")
                self.idCounter += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (17, 0))
                car.tellSemaphoreImHere()
                self.totalSpawned += 1
        if(start2):
            if len(self.semaphore4.total) >= 14:
                return
            else:
                car = vehicle(self.idCounter, self, self.semaphore4, (32, 17), "West", "blue")
                self.idCounter += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (32, 17))
                car.tellSemaphoreImHere()
                self.totalSpawned += 1
        if(start3):
            if len(self.semaphore1.total) >= 14:
                return
            else:
                car = vehicle(self.idCounter, self, self.semaphore2, (0, 16), "East", "orange")
                self.idCounter += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (0, 16))
                car.tellSemaphoreImHere()
                self.totalSpawned += 1
        if(start4):
            if len(self.semaphore2.total) >= 14:
                return
            else:
                car = vehicle(self.idCounter, self, self.semaphore1, (16, 32), "South", "purple")
                self.idCounter += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (16, 32))
                car.tellSemaphoreImHere()
                self.totalSpawned += 1
            
            
    def getHighestDensitySemaphore(self, list):
        highest = list[0]
        for i in range(1, len(list)):
            if list[i].carsInLine > highest.carsInLine:
                highest = list[i]
        return highest
    
    def countAgentsThatAreCars(self):
        agents = self.schedule.agents
        cars = 0
        
        for i in range(0, len(agents)):
            if isinstance(agents[i], vehicle):
                cars += 1
        
        return cars
    
    def checkIfCellHasVehicle(self, agents):
        for i in range(0, len(agents)):
            if isinstance(agents[i], cell):
                cars = self.grid.get_cell_list_contents([agents[i].pos])
                for i in range(0, len(cars)):
                    if isinstance(cars[i], vehicle):
                        return True
        return False    
    
    def step(self):
        self.schedule.step()
        self.add_vehicles()
        
        semWithMaxDensity = self.getHighestDensitySemaphore(self.semaphores)
        self.priority.appendleft(semWithMaxDensity.unique_id)
        
        #print the priority list
        
        flag = False
        
        flag = self.checkIfCellHasVehicle(self.listStops)
        
        if flag:
            self.timeStep += 1
        
        if self.timeStep > 9:
            self.priority.popleft()
            self.timeStep = 0
            

        for i in range(len(self.semaphores)):
            self.semaphores[i].semaphoreStep(self.priority)
            
        self.datacollector.collect(self)            
        
        print("Time step: " + str(self.timeStep))
        
        print("Total spawned: ", self.totalSpawned)    
        print("Active cars: ", self.countAgentsThatAreCars())
        print("Traffic flow: ", self.trafficFlow)
        print("Total crahses: ", self.crashes)
        print("\n")




"""model = street(33, 33)
for i in range(500):
    model.step()
    """