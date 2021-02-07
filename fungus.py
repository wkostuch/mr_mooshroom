import numpy as np
import utilities
import random
from grid import Grid
from climate import Climate

class Fungus:
    """Fungus class for simulating a particular species of Fugnus and its lifecycle"""
    
    def __init__(self, 
    name: str, 
    initial_locations: list,
    decay_regression_constants: tuple,
    functioning_temperatures: tuple,
    functioning_moistures: tuple,
    hyphal_growth_rate: float,
    hyphal_density: float ) -> None:

        self.name = name
        self.decay_regression_constants = decay_regression_constants
        self.functioning_temperatures = functioning_temperatures
        self.functioning_moistures = functioning_moistures
        self.hyphal_growth_rate = hyphal_growth_rate
        self.hyphal_density = hyphal_density

        self.locations = self.__load_initial_locations(initial_locations)
        self.dead_locations =[]
        self.all_dead = False
        

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

    def __add_location(self, location:tuple) -> None:
        """Function to add Fungus location on Grid"""

        #When a fungus first joins a location, it has consumed no substrate
        self.locations[location] = 0 

    def __decay_rate(self, temperature:float) -> float:
        """Gives the percentage of mass the fungus consumes"""

        #Calculate the decay rate based on the regression constants
        A,B = self.decay_regression_constants
        decay = A + (B * temperature)
        return decay

    def __moisture_multiplier(self, moisture: float) -> float:
        """Returns a weighted multiplier based on the moisture"""
        optimal_moisture,_,_= self.functioning_moistures

        return ((moisture - abs(optimal_moisture - moisture)) / optimal_moisture)

    def __probability_of_expansion(self) -> bool:
        """Determines whether the fungus actually expands"""

        #The probability of expansion is based on a weighted random factor based on the hyphal growth rate
        probability = np.random.rand() * (self.hyphal_growth_rate / utilities.MAX_HYPHAL_GROWTH)
        if probability > utilities.PROBABILITY_THRESHOLD:
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
            self.__add_location(expansion)

    def __kill(self, location: tuple) -> None:
        """Kills the fungus at a specified location"""
        self.dead_locations.add(location)

    def __kill_all(self) -> None:
        """Kill every fungus location"""
        

    def climate_death(self, climate: Climate) -> bool:
        """Determines if the climate has killed the fungus"""
        temperature = climate.get_climate_temperature()
        moisture = climate.get_climate_moisture()

        #unpack the maximum and minimum values of the temperatures
        _, max_fungus_temperature, min_fungus_temperature = self.functioning_temperatures
        _, max_fungus_moisture, min_fungus_moisture = self.functioning_moistures

        #A series of booleans to determine if climate death occurs
        max_temp_exceeded = temperature > (max_fungus_temperature + (utilities.TEMPERATURE_THRESHOLD_MULTIPLIER * max_fungus_temperature))
        min_temp_below = temperature < (min_fungus_temperature - (utilities.TEMPERATURE_THRESHOLD_MULTIPLIER * min_fungus_temperature))
        max_moisture_exceeded = moisture > (max_fungus_moisture + (utilities.MOISTURE_THRESHOLD_MULTIPLIER * max_fungus_moisture))
        min_moisture_below =  moisture < (min_fungus_moisture - (utilities.MOISTURE_THRESHOLD_MULTIPLIER * min_fungus_moisture))

        return max_temp_exceeded or min_temp_below or max_moisture_exceeded or min_moisture_below
        
    def __consume_substrate(self, grid: Grid, climate: Climate) -> None:
        """Consume substrate at the current Fungus locations"""

        temperature = climate.get_climate_temperature()
        moisture = climate.get_climate_moisture()

        #Loop over the keys
        for key in self.locations:
            #can't operate on dead things
            if key in self.dead_locations:
                pass
            original_substrate = grid.get_original_value(key)
            current_substrate = grid.get_current_value(key)

            consumed_substrate = original_substrate * (self.__decay_rate(temperature) * self.__moisture_multiplier(moisture))

            #If there is enough substrate, eat
            if consumed_substrate < current_substrate:
                new_substrate = current_substrate - consumed_substrate
                self.locations[key] = self.locations[key] + consumed_substrate
                grid.set_current_biomass(key, new_substrate)

                #Always trying to expand
                self.__expand(grid, key)

            #if there is not enough food, the fungus begins to die
            else:
                self.__kill(key)

    def turn(self, grid:Grid, climate:Climate) -> None:
        """Executes a turn on a Fungus"""

        #Are we already dead?
        if self.all_dead:
            return
        
        #check to see if the Fungus dies outright
        if self.climate_death(climate):
            self.__kill_all()
        #If not, it gets to eat
        else:
            self.__consume_substrate(grid, climate)