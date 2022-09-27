from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.TextVisualization import TextData
from mesa.visualization.ModularVisualization import ModularServer
from Covid_model_age import *





class StatusText(TextElement):                  #Inherit text element class, used to show a live variable
    def __init__(self, text, var):
        self.text=  text
        self.var = var
        pass
     
    def render(self, model):
        
        return self.text + ": " + str(getattr(model, self.var)) 



def agent_portrayal(agent):                     #function defining how the agent would look in the grid
    portrayal = {
        'Shape' : 'circle',
        'Layer' : 0,
        'r' : .8,
        'Color' : 'lightblue',
        }   

    if agent.exposed == True:                   #Different states and what colour the agents should have
    
        portrayal['Color'] = '#808080'          #Gray
        
    elif agent.infected == True:
        portrayal['Color'] = '#fc0000'          #Red
        
    elif agent.immune == True:
        portrayal['Color'] = '#00ff00'          #Green
        
    
    return portrayal



grid = CanvasGrid(agent_portrayal, w,h,700,700)       #create the gird

line_charts = ChartModule([                #Line graph
    {'Label': 'Susceptible', 'Color': 'lightblue'}, 
    {'Label': 'Exposed', 'Color': '#808080'},        #Gray
    {'Label': 'Infected', 'Color': '#fc0000'},       #Red
    {'Label': 'Recovered', 'Color': '#00ff00'}])     #Green





text_susceptible = StatusText('Susceptible', 'susceptible')     #Showing live text
text_exposed = StatusText('Exposed', 'exposed')
text_infected = StatusText('Infected', 'infected')
text_recovered = StatusText('Recovered', 'immune')


server = ModularServer(Covid_model,                              #Creating the server with the grid, chart and live text
                       [grid, line_charts,
                        text_susceptible,
                        text_exposed,
                        text_infected,
                        text_recovered
                        ],
                       'COVID Simulation Model',
                       model_params)

server.port = 8521  # default port if unspecified 
server.launch()     #lunching server

