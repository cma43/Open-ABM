from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import HexGrid
from mesa.datacollection import DataCollector
from .cell import Cell


class HexSnowflake(Model):
    '''
    Represents the hex grid of cells. The grid is represented by a 2-dimensional array of cells with adjacency rules specific to hexagons.
    '''

    def __init__(self, height=50, width=50, server = True, num_steps = 1000):
        '''
        Create a new playing area of (height, width) cells.
        '''

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)
        self.num_steps = num_steps
        # Use a hexagonal grid, where edges wrap around.
        self.grid = HexGrid(height, width, torus=True)
        self.server = server
        # Place a dead cell at each location.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        # activate the center(ish) cell.
        centerishCell = self.grid[width // 2][height // 2]

        centerishCell.state = 1
        for a in centerishCell.neighbors:
            a.isConsidered = True

        self.running = True
        
        #Datacollector -- default for this model is no data collection, but one can use OABM to assign one. 
        #so this is an empty DataCollector instance from MESA

        self.datacollector = DataCollector()

    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
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
