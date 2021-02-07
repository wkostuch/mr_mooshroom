import numpy as np
import utilities
import random
from grid import Grid
from climate import Climate

class Fungus:
    """Fungus class for simulating a particular species of Fungus and its lifecycle"""
    
    def __init__(self, 
    initial_locations: list,
    name: str, 
    decay_regression_constants: tuple,
    functioning_temperatures: tuple,
    functioning_moistures: tuple,
    hyphal_growth_rate: float,
    hyphal_density: float,
    competitive_ranking: float) -> None:

        self.name = name
        self.decay_regression_constants = decay_regression_constants
        self.functioning_temperatures = functioning_temperatures
        self.functioning_moistures = functioning_moistures
        self.hyphal_growth_rate = hyphal_growth_rate
        self.hyphal_density = hyphal_density

        self.locations = self.__load_initial_locations(initial_locations)
        self.dead_locations =[]
        self.competitive_ranking = competitive_ranking
        self.all_dead = False
        self.day = 0
        self.amount_eaten_today = 0
        

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
        optimal_moisture,_= self.functioning_moistures

        return abs((moisture - abs(optimal_moisture - moisture)) / optimal_moisture)

    def __probability_of_expansion(self) -> bool:
        """Determines whether the fungus actually expands"""

        #The probability of expansion is based on a weighted random factor based on the hyphal growth rate
        probability = np.random.rand() 
        print(probability)
        if probability < utilities.probability_thresholds[self.name]:
            return True
        else:
            return False

    def __expand(self, grid: Grid, location: tuple, eligible_neighbors:tuple) -> tuple:
        """Hadles the expansion of the fungus through the grid"""
        if self.__probability_of_expansion():
            
            #from the eligible neighbors, select one at random
            expansion = random.choice(eligible_neighbors)
            return expansion
            
        return None

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
        optimal_moisture, moisture_width = self.functioning_moistures

        #A series of booleans to determine if climate death occurs
        max_temp_exceeded = temperature > (max_fungus_temperature + (utilities.TEMPERATURE_THRESHOLD_MULTIPLIER * max_fungus_temperature))
        min_temp_below = temperature < (min_fungus_temperature - (utilities.TEMPERATURE_THRESHOLD_MULTIPLIER * min_fungus_temperature))
        max_moisture_exceeded = moisture > (optimal_moisture + (utilities.MOISTURE_THRESHOLD_MULTIPLIER * moisture_width))
        min_moisture_below =  moisture < (optimal_moisture - (utilities.MOISTURE_THRESHOLD_MULTIPLIER * moisture_width))

        return max_temp_exceeded or min_temp_below or max_moisture_exceeded or min_moisture_below
        
    def __consume_substrate(self, grid: Grid, climate: Climate) -> None:
        """Consume substrate at the current Fungus locations"""

        temperature = climate.get_climate_temperature()
        moisture = climate.get_climate_moisture()
        
        expansions = []
        killed =[]
        #Loop over the keys
        for key in self.locations.keys():
            #can't operate on dead things
            if key in self.dead_locations:
                continue
            original_substrate = grid.get_original_biomass_at_location(key)
            current_substrate = grid.get_current_biomass_at_location(key)

            consumed_substrate = original_substrate * (self.__decay_rate(temperature) * self.__moisture_multiplier(moisture))

            #If there is enough substrate, eat
            if consumed_substrate < current_substrate:
                self.amount_eaten_today += consumed_substrate
                new_substrate = current_substrate - consumed_substrate
                self.locations[key] = self.locations[key] + consumed_substrate
                grid.set_current_biomass(key, new_substrate)

                #Always trying to expand
                
                neighbors = grid.get_neighbors(key)

                #Make sure we are not already there
                eligible_neighbors = [x for x in neighbors if x not in self.locations]

                #from the eligible neighbors, select one at random
                if len(eligible_neighbors) != 0 and self.day % utilities.DAYS_UNTIL_EXPANSION == 0:
                   
                    expansion = self.__expand(grid, key, eligible_neighbors)
                    if expansion != None:
                     
                        expansions.append(expansion)

            #if there is not enough food, the fungus begins to die
            else:
                killed.append(key)

        for location in expansions:
            self.__add_location(location)

        for died in killed:
            self.__kill(died)
    
    def get_number_of_fungal_cells(self) -> int:
        """Returns the number of cells the fugnus took over"""
        return len(self.locations)
    
    def get_number_of_deaths(self) -> int:
        """Return the number of fungal cells that died"""
        if self.all_dead:
            return self.get_number_of_fungal_cells()
        else:
            return len(self.dead_locations)

    def get_total_amount_of_substrate_eaten(self) -> float:
        """Returns the total amount that the fungus has eaten"""
        amount = 0
        for key in self.locations:
            amount += self.locations[key]
    
    def get_amount_of_substrate_eaten_today(self) -> float:
        """Returns the amount of substrate eaten after a turn"""
        return self.amount_eaten_today

    def turn(self, grid:Grid, climate:Climate) -> None:
        """Executes a turn on a Fungus"""

        self.day += 1
        self.amount_eaten_today = 0
        #Are we already dead?
        if self.all_dead:
            return
        
        #check to see if the Fungus dies outright
        if self.climate_death(climate):
            self.__kill_all()
        #If not, it gets to eat
        else:
            self.__consume_substrate(grid, climate)

class Fungus1(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Phellinus robiniae", 
                decay_regression_constants = (-0.16844262333333337, 0.016441256833333334), 
                functioning_temperatures = (29.45,32.3,20.25), 
                functioning_moistures = (-0.625, 1.505), 
                hyphal_growth_rate = 2.22, 
                hyphal_density = 0.095,
                competitive_ranking = 0.16216216216216218) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus2(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Phellinus hartigii", 
                decay_regression_constants = (-0.0759836070000001, 0.01030737708333334), 
                functioning_temperatures = (19.1,28.2,9.6), 
                functioning_moistures = (-0.65,1.57), 
                hyphal_growth_rate = 1.54, 
                hyphal_density = 1.8,
                competitive_ranking = 0.24324324324324326) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus3(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Phellinus gilvus", 
                decay_regression_constants = (-0.22144808700000043, 0.025232240416666694), 
                functioning_temperatures = (31.5,35.3,16.7), 
                functioning_moistures = (-0.06,1.4), 
                hyphal_growth_rate = 4.04, 
                hyphal_density = 0.03,
                competitive_ranking = 0.21621621621621623) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus4(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Armillaria tabescens", 
                decay_regression_constants = (-0.06484426300000005, 0.0067759563333333345), 
                functioning_temperatures = (26.15,32.7,15.7), 
                functioning_moistures = (-0.445,2.375), 
                hyphal_growth_rate = 0.785, 
                hyphal_density = 0.35,
                competitive_ranking = 0.06756756756756757) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus5(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Porodisculus pendulus", 
                decay_regression_constants = (0.006557377666666621, 0.001195355166666671), 
                functioning_temperatures = (26.4, 31.7, 16.7), 
                functioning_moistures = (-0.64, 1.24), 
                hyphal_growth_rate = 4.06, 
                hyphal_density = 0.32,
                competitive_ranking = 0.21621621621621623) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus6(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Schizophyllum commune", 
                decay_regression_constants = (-0.04494535400000012, 0.0059904370833333345), 
                functioning_temperatures = (32.55, 36.4, 19.75), 
                functioning_moistures = (-0.775, 2.26), 
                hyphal_growth_rate = 1.785, 
                hyphal_density = 0.56,
                competitive_ranking = 0.391891891891891915) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus7(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Hyphodontia crustosa", 
                decay_regression_constants = (-0.016475410333333527, 0.006372950833333347), 
                functioning_temperatures = (23.2,25.6, 30.3), 
                functioning_moistures = (-0.23, 1.19), 
                hyphal_growth_rate = 1.96, 
                hyphal_density = 0.12,
                competitive_ranking = 0.32432432432432434) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus8(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Phlebia rufa", 
                decay_regression_constants = (0.09685792299999989, 0.0029371584999999976), 
                functioning_temperatures = (27.15, 30.85, 12.7), 
                functioning_moistures = (-0.475, 1.235), 
                hyphal_growth_rate = 8.63, 
                hyphal_density = 0.205,
                competitive_ranking = 0.97297297297297295) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus9(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Hyphoderma setigerum", 
                decay_regression_constants = (-0.10240437133333334, 0.011031420750000007), 
                functioning_temperatures = (26.75, 29.05, 17.95), 
                functioning_moistures = (-0.41, 1.285), 
                hyphal_growth_rate = 4.405, 
                hyphal_density = 0.06,
                competitive_ranking =  0.44594594594594592) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus10(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Laetiporus conifericola", 
                decay_regression_constants = (0.024398907333333168, 0.00362704916666667), 
                functioning_temperatures = (27.1, 29.6, 17.5), 
                functioning_moistures = (-0.56, 1.22), 
                hyphal_growth_rate = 5.16, 
                hyphal_density = 0.04,
                competitive_ranking = 0.08108108108108109) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus11(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Tyromyces chioneus", 
                decay_regression_constants = (-0.11937158433333334, 0.01619535516666666), 
                functioning_temperatures = (30.6, 33.6, 19), 
                functioning_moistures = (-0.22, 1.19), 
                hyphal_growth_rate = 3.88, 
                hyphal_density = 0.06,
                competitive_ranking = 0.6486486486486487 ) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus12(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Lentinus crinitus", 
                decay_regression_constants = (-0.05841530033333329, 0.008565573749999996), 
                functioning_temperatures = (33.8, 40.2, 22.4), 
                functioning_moistures = (-0.31, 1.55), 
                hyphal_growth_rate = 6.38, 
                hyphal_density = 0.05,
                competitive_ranking = 0.32432432432432434) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus13(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Fomes fomentarius", 
                decay_regression_constants = (-0.18691256833333292, 0.02515710383333332), 
                functioning_temperatures = (27.3, 30.1, 20.8), 
                functioning_moistures = (-0.24, 1.19), 
                hyphal_growth_rate = 4.71, 
                hyphal_density = 0.002375,
                competitive_ranking = 0.08108108108108109) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)

class Fungus14(Fungus):
    def __init__(self, initial_locations: list, 
                name = "Xylobolus subpileatus", 
                decay_regression_constants = (-0.02008196733333318, 0.0043579234999999925), 
                functioning_temperatures = (22.2, 33.6, 5.1), 
                functioning_moistures = (-0.88, 4.96), 
                hyphal_growth_rate = 0.77, 
                hyphal_density = 1.74,
                competitive_ranking = 0.24324324324324326) -> None:
        super().__init__(initial_locations, 
                name, 
                decay_regression_constants, 
                functioning_temperatures, 
                functioning_moistures, 
                hyphal_growth_rate, 
                hyphal_density,
                competitive_ranking)
