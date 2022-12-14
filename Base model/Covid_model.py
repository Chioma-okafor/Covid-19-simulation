import pandas as pd
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.visualization.UserParam import UserSettableParameter                                               


w = 50                          #definig width and height
h = 50



def prob(probability):          #function that returns True or Flase depending on a probability value
    return bool(np.random.rand() < probability)





model_params = {                                  #Paramaters for the model 
    'no_agents': UserSettableParameter( 'number', 'Number of agents', 100,10,10000,5),
    'width':w,
    'height':h,
    'exposed_prob': UserSettableParameter('slider', 'Percentage of exposed agents', 0.1,0,1,0.05),
    'infected_prob': UserSettableParameter('slider', 'Percentage of infected agents', 0.2,0,1,0.05),
    'exposed_tran': UserSettableParameter('slider', 'Transmission probability of exposed', 0.4,0,1,0.05),
    'infected_tran': UserSettableParameter('slider', 'Transmission probability of infected', 0.6,0,1,0.05),
    'masked_prob': UserSettableParameter('slider', 'percentage of agents using masks', 0.2,0,1,0.05),
    'vaccinated_prob': UserSettableParameter('slider', 'percentage of vaccinated agents', 0.4,0,1,0.05),
    'masked_dec': UserSettableParameter('slider', 'percentage decrease of using mask', 0.05,0,1,0.05),
    'vaccinated_dec': UserSettableParameter('slider', 'percentage decrease of being vaccinated', 0.3,0,1,0.05),
    'exposed_period_max': UserSettableParameter('slider', 'Max of steps in exposed state', 21, 1, 50, 1),
    'exposed_period_min': UserSettableParameter('slider', 'Min of steps in exposed state', 5, 1, 50, 1),
    'infected_period_max': UserSettableParameter('slider', 'Max of steps in infected state', 35, 1, 50, 1),
    'infected_period_min': UserSettableParameter('slider', 'Min of steps in infected state', 10, 1, 50, 1),
    'immunity_period_max': UserSettableParameter('slider', 'Max of steps in immune state', 180, 10, 500, 10), 
    'immunity_period_min': UserSettableParameter('slider', 'Min of steps in immune state', 80, 10, 500, 10), 
   
   
}











class Agent(Agent):    #class for the agent
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model) #Initial the agent in the model
        
        self.exposed_countdown = 0
        self.infected_countdown = 0
        self.immunity_countdown = 0
        self.immune  = False
        self.masked = prob(self.model.masked_prob)
        self.vaccinated = prob(self.model.vaccinated_prob)
        self.infected = False
        self.exposed = prob(self.model.exposed_prob)
        if self.exposed ==True:
 
            self.exposed_countdown = np.random.randint(1, self.model.exposed_period_max + 1)   #give random countdown to exposed agents
        else:
            infected_prob = self.model.infected_prob / (1-self.model.exposed_prob)      #adjust the probability of infected so it takes the exposed into consideration
            self.infected = prob(infected_prob)
            if self.infected ==True:
                self.infected_countdown = np.random.randint(1, self.model.infected_period_max + 1)#give random countdown to infected agents
    
    
    def move(self): #get current position and one cell horrizontally and veritacally 
        x, y = self.pos
        new_x = min(max(np.random.choice([-1, 0, 1]) + x, 0), self.model.grid.height - 1)   #move left or right with a max and min constrant so the agent doesn't move outside the grid
        new_y = min(max(np.random.choice([-1, 0, 1]) + y, 0), self.model.grid.height - 1)  #move up or down a max and min constrant so the agent doesn't move outside the grid
        self.model.grid.move_agent(self, (new_x, new_y))
        
    def transmission(self):  #Checl the current cell if it has any infected or exposed and calculate the transmission probability
        if self.exposed | self.infected | self.immune:
            return None
        pos = tuple([int(self.pos[0]), int(self.pos[1])])
        
        cell_agents = self.model.grid.get_cell_list_contents(pos) # List of agents in the same grid cell
        
        exposed_agents = any(a.exposed for a in cell_agents)
        tran_probablity = 0
        if exposed_agents:
            tran_probablity = self.model.exposed_prob
            if self.masked:
                tran_probablity *=(1-self.model.masked_dec)     #decrease transmission if the agent wears a mask
            
            if self.vaccinated:
                tran_probablity *= (1-self.model.vaccinated_dec)    #decrease transmission if the agent is vaccinated

        self.exposed = prob(tran_probablity)    #run function to see if agent becomes exposed
        
        if self.exposed == False:
            infected_agents = any(a.infected for a in cell_agents)
            tran_probablity = 0
            if infected_agents:
                tran_probablity = self.model.infected_prob
                if self.masked:
                    tran_probablity *=(1-self.model.masked_dec)
                
                if self.vaccinated:
                    tran_probablity *= (1-self.model.vaccinated_dec)

            self.exposed = prob(tran_probablity)   #run function to see if agent becomes exposed
        
        
          
        
        if self.exposed:    #if the agents becomes exposed then give it a random countdown
            self.exposed_countdown = np.random.randint(self.model.exposed_period_min, self.model.exposed_period_max + 1)
            
            
    def update_exposed(self):      #countdown ticks down by one until it reaches zero then the agent stops being exposed and becomes infected
        if self.exposed_countdown ==0:
            self.exposed = False
            self.infected = True
            self.infected_countdown = np.random.randint(self.model.infected_period_min, self.model.infected_period_max + 1)
        else:
            self.exposed_countdown -= 1
            
    def update_infected(self):  #countdown ticks down by one until it reaches zero then the agent stops being infected and becomes immune
        if self.infected_countdown ==0:
            self.infected = False
            self.immune = True
            self.immunity_countdown = np.random.randint(self.model.immunity_period_min, self.model.immunity_period_max + 1)      

        else:
            self.infected_countdown -=1
            
    def update_immune(self):    #countdown ticks down by one until it reaches zero then the agent stops being immune
        if self.immunity_countdown ==0:
            self.immune = False
        else:
            self.immunity_countdown -=1
            
    def step(self):         #runs each step in the model, make agent move, check for transmission and update it's status if it's exposed, infected or immune
        self.move()
        if self.immune:
            self.update_immune()

        if self.exposed:
            self.update_exposed()
        if self.infected:
            self.update_infected()
        
        self.transmission()
        
        
        
     
    
class Covid_model(Model):      #Class that define how the model behaves
    
    def __init__(self, no_agents, width, height, 
                 exposed_prob, infected_prob, exposed_tran, infected_tran,
                 masked_prob, vaccinated_prob, masked_dec, vaccinated_dec,
                 exposed_period_max, exposed_period_min , infected_period_max,infected_period_min, immunity_period_max, immunity_period_min):
        

        self.no_agents = int(no_agents)
        self.grid = MultiGrid(int(width), int(height), True)    #multigrid allows for more than one agent to occupy the same grid
        self.exposed_prob = exposed_prob
        self.infected_prob = infected_prob
        self.exposed_tran= exposed_tran
        self.infected_tran = infected_tran
        self.masked_prob = masked_prob 
        self.vaccinated_prob = vaccinated_prob
        self.masked_dec = masked_dec
        self.vaccinated_dec = vaccinated_dec        
        self.exposed_period_max = exposed_period_max        
        self.exposed_period_min = exposed_period_min
        
        self.infected_period_max  = infected_period_max
        self.infected_period_min  = infected_period_min
        self.immunity_period_max = immunity_period_max
        self.immunity_period_min = immunity_period_min
        
        self.schedule = RandomActivation(self)
        self.running = True
        
        for i in range(self.no_agents):    #loop that creates agents and places them randomely in the grid
            a = Agent(i,self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            
            
        self.datacollector = DataCollector({     # data collector collects live data when the model is running
            'Susceptible' : 'susceptible',
            'Exposed' : 'exposed',
            'Infected' : 'infected',
            'Recovered' : 'immune'            
            })



     #Different propreties that will be collected for the model 
    @property 
    def susceptible(self):
        agents = self.schedule.agents
        susceptible = [not(a.immune | a.infected | a.exposed) for a in agents]
        return int(np.sum(susceptible))
    
    @property
    def exposed(self):
        agents = self.schedule.agents
        exposed = [a.exposed for a in agents]
        return int(np.sum(exposed))
    
    @property
    def infected(self):
        agents = self.schedule.agents
        infected = [a.infected for a in agents]
        return int(np.sum(infected))

    @property
    def immune(self):
        agents = self.schedule.agents
        immune = [a.immune for a in agents]
        return int(np.sum(immune))
    
    def step(self):     #the step function for the model
        self.datacollector.collect(self)
        self.schedule.step()
        
        
        
    