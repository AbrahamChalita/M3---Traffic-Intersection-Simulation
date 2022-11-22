from mesa import Agent, Model, model
from collections import deque
import random

class vehicle(Agent):
    
    def __init__(self, unique_id, model, semaphore, start_position, direction, color = None):
        super().__init__(unique_id, model)
        self.semaphore = semaphore
        self.start_position = start_position
        self.action = random.choices(population=["forward", "right", "left"], weights=[0.8, 0.1, 0.1], k=1)[0]
        self.end_position = self.chooseExit(self.action)
        self.direction = direction
        self.color = color
        self.histeria = 0
        self.speed = 1
        self.state = "Normal"
        
    def determineSanity(self, histeria) -> None:
        if histeria > 10:
            self.state = "Insane"
        else:
            self.state = "Normal"
        
    def chooseExit(self, action) -> tuple:
        if self.start_position == (17, 0):
            if action == "forward":
                return (17, 32)
            elif action == "right":
                return (32, 16)
            elif action == "left":
                return (0, 17)
        elif self.start_position == (32, 17):
            if action == "forward":
                return (0, 17)
            elif action == "right":
                return (17, 32)
            elif action == "left":
                return (16, 0)
        elif self.start_position == (0, 16):
            if action == "forward":
                return (32, 16)
            elif action == "right":
                return (16, 0)
            elif action == "left":
                return (17, 32)
        elif self.start_position == (16, 32):
            if action == "forward":
                return (16, 0)
            elif action == "right":
                return (0, 17)
            elif action == "left":
                return (32, 16)
        
    def move(self, next_position) -> None:
        self.model.grid.move_agent(self, next_position)
        
        # Cambiar direccion de giro
        if self.direction == "North" or self.direction == "South":
            if self.pos[1] == self.end_position[1]:
                if self.pos[0] < self.end_position[0]:
                    self.direction = "East"
                elif self.pos[0] > self.end_position[0]:
                    self.direction = "West"
        elif self.direction == "East" or self.direction == "West":
            if self.pos[0] == self.end_position[0]:
                if self.pos[1] < self.end_position[1]:
                    self.direction = "North"
                elif self.pos[1] > self.end_position[1]:
                    self.direction = "South"
                    
    def nextPosition(self, speed) -> tuple:
        if self.direction == "North":
            return (self.pos[0], self.pos[1] + speed)
        elif self.direction == "South":
            return (self.pos[0], self.pos[1] - speed)
        elif self.direction == "East":
            return (self.pos[0] + speed, self.pos[1])
        elif self.direction == "West":
            return (self.pos[0] - speed, self.pos[1])

    def tellSemaphoreImHere(self) -> None:
        self.semaphore.carsInLine += 1
        self.semaphore.total.append(self)
        
        
    def verifyStep(self) -> bool:
        followUp = self.nextPosition(self.speed)
        neighbours_nextCell = self.model.grid.get_cell_list_contents(followUp)
        
        flag = True
        
        for i in neighbours_nextCell:
            if isinstance(i, vehicle):
                flag = False
            
            if isinstance(i, cell):
                if i.cellType == "semaphore":
                    if i.sema.color == "red":
                        self.histeria += 1
                        flag = False
                    elif i.sema.color == "green":
                        flag = True
                        #self.histeria = 0
                elif i.cellType == "intersection":
                    if self.semaphore == i.sema:
                        #self.histeria = 0
                        i.sema.carsInLine -= 1
                        if(self in i.sema.total):
                            i.sema.total.remove(self)
                        flag = True
        return flag
    
    def verifyInsane(self) -> bool:
        followUp = self.nextPosition(self.speed)
        neighbours_nextCell = self.model.grid.get_cell_list_contents(followUp)
        
        flag = True
        
        for i in neighbours_nextCell:
            if isinstance(i, vehicle):
                print("VOY A CHOCAAAAAAAAAAAAAAR, " + self.semaphore.location, "tengo id " + str(self.unique_id))
                flag = True
            
            if isinstance(i, cell):
                if i.cellType == "semaphore":
                    if i.sema.color == "red":
                        self.histeria += 1
                        print("ME VOY A PASAR EL SEMAFOROOOOOOOOOOOOOO", self.semaphore.location, "tengo id " + str(self.unique_id))
                        flag = True
                    elif i.sema.color == "green":
                        flag = True
                elif i.cellType == "intersection":
                    if self.semaphore == i.sema:
                        i.sema.carsInLine -= 1
                        if(self in i.sema.total):
                            i.sema.total.remove(self)
                        flag = True
        return flag
                

    def countAgentCarsInCell(self, cell) -> int:
        count = 0
        for i in cell:
            if isinstance(i, vehicle):
                count += 1
        return count
    
    def step(self) -> None:
        if(self.pos == self.end_position):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.trafficFlow += 1
            print("Reached destination, I have id " + str(self.unique_id))
            return
        
        
        if(self.state == "Normal"):
            if(self.verifyStep()):
                self.move(self.nextPosition(self.speed))
        elif(self.state == "Insane"):
            if(self.verifyInsane()):
                self.move(self.nextPosition(self.speed))
        
        self.determineSanity(self.histeria)
            
        currentCell = self.model.grid.get_cell_list_contents(self.pos)
        if self.countAgentCarsInCell(currentCell) > 1:
            print("CRASH DETECTED between " + str(self.unique_id) + " and " + str(currentCell[1].unique_id))
            
            self.model.crashes += 1
            
            for i in currentCell:
                if isinstance(i, vehicle):
                    self.model.grid.remove_agent(i)
                    self.model.schedule.remove(i)
                    #print("Removed agent " + str(i.unique_id))
            

                
class cell(Agent):
    def __init__(self, unique_id, model, cellType, sema= None):
        super().__init__(unique_id, model)
        self.cellType = cellType
        self.sema = sema
        
    
    def step(self):
        pass

class wall(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass

class semaphore(Agent):
    
    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.carsInLine = 0
        self.color = "yellow"
        self.active = False
        self.location = location   
        self.total = []
    
    def semaphoreStep(self, priority):
        #print("Semáforo en: ", self.location, " con cars in line: ", len(self.total))
        #print("Length of total: ", len(self.total), " semaphore: ", self.location)
        # print waiting time of first car in line
        
        if(len(self.total) > 0):
            print("Waiting time first, on", self.location , " with id: ", self.total[0].unique_id, "and histeria: ", self.total[0].histeria, "---> Sanity: ", self.total[0].state)

        
        if priority:
            self.active = priority[0] == self.unique_id
        else:
            self.active = False
            
        if self.active:
            self.color = "green"
        else:
            self.color = "red"
    
    
    
    def step(self):
        pass
        