from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """
    def __init__(self, height=100, width=100, density=0.65, server = True, num_steps = 1000):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density
        self.server = server
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)
        self.num_steps = num_steps

        self.datacollector = DataCollector(
            {"Fine": lambda m: self.count_type(m, "Fine"),
             "On Fire": lambda m: self.count_type(m, "On Fire"),
             "Burned Out": lambda m: self.count_type(m, "Burned Out")})

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < self.density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

    def run_model(self, n = None, export_agent_data = False, export_model_data = False):

        if self.server == False:
            if not n:
                for _ in range(self.num_steps):
                    self.step()
                if export_agent_data:
                    return self.datacollector.get_agent_vars_dataframe()
                elif export_model_data:
                    return self.datacollector.get_model_vars_dataframe()
                elif export_model_data and export_agent_data:
                    return self.datacollector.get_model_vars_dataframe, self.datacollector.get_agent_vars_dataframe
            else:
                self.num_steps = n
                for _ in range(self.num_steps):
                    self.step()
                # if export_agent_data:
                #     return self.datacollector.get_agent_vars_dataframe()
                # elif export_model_data:
                #     return self.datacollector.get_model_vars_dataframe()
                # elif export_model_data == True and export_agent_data == True:
                #     return self.datacollector.get_model_vars_dataframe, self.datacollector.get_agent_vars_dataframe
                return self
        else:
            from .server import server

            server.launch()
