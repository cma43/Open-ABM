'''
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
'''

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from .boid import Boid


class BoidFlockers(Model):
    '''
    Flocker model class. Handles agent creation, placement and scheduling.
    '''

    def __init__(self,
                 population=100,
                 width=100,
                 height=100,
                 speed=1,
                 vision=10,
                 separation=2,
                 cohere=0.025,
                 separate=0.25,
                 match=0.04,
                 server = True,
                 num_steps = 1000):
        '''
        Create a new Flockers model.

        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives.        '''
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_agents()
        self.running = True
        self.server = server
        self.num_steps = num_steps

        #Datacollector -- default for this model is no data collection, but one can use OABM to assign one. 
        #so this is an empty DataCollector instance from MESA

        self.datacollector = DataCollector()

    def make_agents(self):
        '''
        Create self.population agents, with random positions and starting headings.
        '''
        for i in range(self.population):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            boid = Boid(i, self, pos, self.speed, velocity, self.vision,
                        self.separation, **self.factors)
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()

    def run_model(self, n = None):
        if n:
            self.num_steps = n
        if self.server == False:
            for _ in range(self.num_steps):
                self.step()
            return self
        else:
            from .server import server

            server.launch()

