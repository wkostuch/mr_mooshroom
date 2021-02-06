import numpy as np
from grid import Grid
import random

class Fungus:
    """Fungus class for simulating a particular species of Fugnus and its lifecycle"""
    
    def __init__(self, 
    name: str, 
    initial_locations: list,
    substrate_threshold: float, 
    decay_regression_constants: tuple,
    functioning_temperatures: tuple,
    functioning_moistures: tuple,
    hyphal_growth_rate: float,
    hyphal_density: float ) -> None:

        self.name = name
        self.substrate_threshold = substrate_threshold
        self.decay_regression_constants = decay_regression_constants
        self.functioning_temperatures = functioning_temperatures
        self.functioning_moistures = functioning_moistures
        self.hyphal_growth_rate = hyphal_growth_rate
        self.hyphal_density = hyphal_density

        self.locations = self.__load_initial_locations(initial_locations)
        self.probability_threshold = 0.32


    def __load_initial_locations(self, initial_locations: tuple) -> dict:
        """Loads the initial locations of the Fungus in the grid"""

        #Dictionary to hold the locations of the grid
        #if they key exits, the Fungus is at that location
        #maps location to the amount of substrate the fungus has consumed at that location
        locations = {}
        for location in initial_locations:
            #Initial substrate consumption is 0
            locations[location] = 0

        return locations

    def add_location(self, location:tuple) -> None:
        """Function to add Fungus location on Grid"""

        #When a fungus first joins a location, it has consumed no substrate
        self.locations[location] = 0 

    def decay_rate(self, temperature:float) -> float:
        """Gives the percentage of mass the fungus consumes"""

        #Calculate the decay rate based on the regression constants
        A,B = self.decay_regression_constants
        decay = A + (B * temperature)

        return decay



    def consume_substrate(self, grid: Grid, climate: Climate) -> None:
        """Consume substrate at the current Fungus locations"""

        temperature = climate.get_temperature()

        #Loop over the keys
        for key in self.locations:
            original_substrate = grid.get_original_value(key)
            current_substrate = grid.get_current_value(key)

            consumed_substrate = original_substrate * self.decay(temperature)

            #If there is enough substrate, eat
            if consumed_substrate < current_substrate:
                new_substrate = current_substrate - consumed_substrate
                self.locations[key] = self.locations[key] + consumed_substrate
                grid.set_value(key, new_substrate)

                #If the expansion threshold has been reached, seek expansion
                if  self.locations[key] >= self.substrate_threshold:
                    self.__expand(grid, key)

            #if there is not enough food, the fungus begins to die
            else:
                self.__death()

    def __probability_of_expansion(self) -> bool:
        """Determines whether the fungus actually expands"""

        #The probability of expansion is based on a weighted random factor based on the hyphal growth rate
        probability = np.random.rand() * (self.hyphal_growth_rate / MAX_HYPHAL_GROWTH)
        if probability > self.probability_threshold:
            return True
        else:
            return False

    def __expand(self, grid: Grid, location: tuple) -> None:
        """Hadles the expansion of the fungus through the grid"""
        if self.__probability_of_expansion:
            neighbors = grid.get_neighbors(location)

            #Make sure we are not already there
            eligible_neighbors = [x for x in neighbors if x not in self.locations]

            #from the eligible neighbors, select one at random
            expansion = random.choice(eligible_neighbors)

            #Add the expanded location to the list 
            self.add_location(expansion)

    def __death(self):
        pass
        
        
