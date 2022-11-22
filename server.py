import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from model import *

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    
    if(isinstance(agent, vehicle)):
        portrayal["Color"] = agent.color
        portrayal["Layer"] = 1
    
    if(isinstance(agent, semaphore)):
        portrayal["Color"] = agent.color
        portrayal["Layer"] = 0
        portrayal["r"] = 1
        
    if(isinstance(agent, cell)):
        if agent.cellType == "semaphore":
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
            portrayal["r"] = 0
        elif agent.cellType == "intersection":
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
            portrayal["r"] = 0
        elif agent.cellType == "entrance":
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
            portrayal["r"] = 0
    
    if(isinstance(agent, wall)):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        
    return portrayal
        


grid = CanvasGrid(agent_portrayal, 33, 33, 600, 600)
chart_currents = ChartModule([{"Label": "Crashes", "Color": "Red"}], data_collector_name='datacollector')
chart_flow = ChartModule([{"Label": "Flow", "Color": "Blue"}], data_collector_name='datacollector')
server = ModularServer(street, [grid, chart_currents, chart_flow], "Street", {"width": 33, "height": 33})
server.port = 8521 # The default


server.launch()