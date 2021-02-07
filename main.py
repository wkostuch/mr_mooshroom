"""
Authors: Therese Aglialoro, Cameron Nottingham, and William Kostuch
2021 MCM, Problem A: Fungi
"""
import matplotlib.pyplot as plt 
import numpy as np
from typing import List

from world import World


CLIMATE_NAMES = ["Desert", "Tundra", "Grassland", "Shrubland",  
                "TemperateDeciduousForest", "ConiferousForest",
                "Rainforest"]

FUNGUS_NAMES = ["Phellinus robiniae",
                    "Phellinus hartigii",
                    "Phellinus gilvus",
                    "Armillaria tabescens",
                    "Porodisculus pendulus",
                    "Schizophyllum commune",
                    "Hyphodontia crustosa",
                    "Phlebia rufa",
                    "Hyphoderma setigerum",
                    "Laetiporus conifericola",
                    "Tyromyces chioneus",
                    "Lentinus crinitus",
                    "Fomes fomentarius",
                    "Xylobolus subpileatus"]
COLLECTION_INTERVAL = 10
YEARS = 1

def biomass_over_time(climates: List[str], fungi: List[str], 
                        trials: int, time_limit: int):
    """Shows a graph of average biomass over time for each climate after running the trials."""
    array_length = time_limit 
    for climate in climates:
        # Arrays for graphing
        average_times = np.zeros(array_length)
        average_biomass = np.zeros(array_length)
        for n in range(trials):
            # Arrays for holding the values
            times = np.zeros(array_length)
            biomasses = np.zeros(array_length)
            # Make a World and run it for a time
            world = World(climate, (100,100), fungi)
            # Loop through stuff
            for i in range(time_limit):
                time = world.get_time() 
                times[time] = time
                biomasses[time] = world.get_environment().get_grid().average_biomass()
                world.increment_time()
            # Add arrays to average arrays
            average_times += times
            average_biomass += biomasses
        # Average and plot
        average_times /= trials
        average_biomass /= trials
        plt.plot(average_times, 
                average_biomass, 
                label=climate)
    plt.title("Biomass vs. Time for different climates")
    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Biomass")
    plt.show()

def temperature_over_time(climates: List[str], fungi: List[str], 
                        trials: int, time_limit: int):
    """Shows a graph of average temperature over time for each climate after running the trials."""
    array_length = time_limit 
    for climate in climates:
        # Arrays for graphing
        average_times = np.zeros(array_length)
        average_temps = np.zeros(array_length)
        for n in range(trials):
            # Arrays for holding the values
            times = np.zeros(array_length)
            temps = np.zeros(array_length)
            # Make a World and run it for a time
            world = World(climate, (100,100), fungi)
            # Loop through stuff
            for i in range(time_limit):
                time = world.get_time() 
                times[time] = time
                temps[time] = world.get_environment().get_climate().get_climate_temperature()
                world.increment_time()
            # Add arrays to average arrays
            average_times += times
            average_temps += temps
        # Average and plot
        average_times /= trials
        average_temps /= trials
        plt.plot(average_times, 
                average_temps, 
                label=climate)
    plt.title("Temperature vs. Time for different climates")
    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Temperature (degrees C)")
    plt.show()



if __name__ == "__main__":
    worlds = []
    #temperature_over_time(["Rainforest", "Tundra"], FUNGUS_NAMES[0:5], 
     #                   trials=1, time_limit=365*YEARS)
    biomass_over_time(["Rainforest", "Tundra"], FUNGUS_NAMES, 
                        trials=1, time_limit=365*YEARS)


