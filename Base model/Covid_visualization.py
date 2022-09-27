from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.TextVisualization import TextData
from mesa.visualization.ModularVisualization import ModularServer
from Covid_model import *





class StatusText(TextElement):
    def __init__(self, text, var):
        self.text=  text
        self.var = var
        pass
    
    def render(self, model):
        
        return self.text + ": " + str(getattr(model, self.var))

def agent_portrayal(agent):
    portrayal = {
        'Shape' : 'circle',
        'Layer' : 0,
        'r' : .8,
        'Color' : 'lightblue',
        }   

        
        
    if agent.exposed == True:
        portrayal['Color'] = '#ff9191'
        
    elif agent.infected == True:
        portrayal['Color'] = '#fc0000'
        
    elif agent.immune == True:
        portrayal['Color'] = '#00ff00'
        
    
    return portrayal



grid = CanvasGrid(agent_portrayal, w,h,700,700)

line_charts = ChartModule([
    {'Label': 'Susceptible', 'Color': 'lightblue'}, 
    {'Label': 'Exposed', 'Color': '#ff9191'},
    {'Label': 'Infected', 'Color': '#fc0000'},
    {'Label': 'Recovered', 'Color': '#00ff00'}])



text_susceptible = StatusText('Susceptible', 'susceptible')
text_exposed = StatusText('Exposed', 'exposed')
text_infected = StatusText('Infected', 'infected')
text_recovered = StatusText('Recovered', 'immune')


server = ModularServer(Covid_model,
                       [grid, line_charts,
                        text_susceptible,
                        text_exposed,
                        text_infected,
                        text_recovered],
                       'COVID Simulation Model',
                       model_params)

server.port = 8521  # default port if unspecified
server.launch()

