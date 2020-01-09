from mesa import Model
from mesa.time import BaseScheduler, RandomActivation, SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from .agent import PDAgent


class PdGrid(Model):
    ''' Model class for iterated, spatial prisoner's dilemma model. '''

    schedule_types = {"Sequential": BaseScheduler,
                      "Random": RandomActivation,
                      "Simultaneous": SimultaneousActivation}

    # This dictionary holds the payoff for this agent,
    # keyed on: (my_move, other_move)

    payoff = {("C", "C"): 5,
              ("C", "D"): -6,
              ("D", "C"): 6,
              ("D", "D"): -5}

    def __init__(self, height=50, width=50, schedule_type="Random", payoffs=None, seed=None, server = True, num_steps = 1000):
        '''
        Create a new Spatial Prisoners' Dilemma Model.

        Args:
            height, width: Grid size. There will be one agent per grid cell.
            schedule_type: Can be "Sequential", "Random", or "Simultaneous".
                           Determines the agent activation regime.
            payoffs: (optional) Dictionary of (move, neighbor_move) payoffs.
        '''
        self.grid = SingleGrid(height, width, torus=True)
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self)
        self.server = server
        self.num_steps = num_steps
        # Create agents
        for x in range(width):
            for y in range(height):
                agent = PDAgent((x, y), self)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

        self.datacollector = DataCollector({
            "Cooperating_Agents":
            lambda m: len([a for a in m.schedule.agents if a.move == "C"])
        })

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

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
