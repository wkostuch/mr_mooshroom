"""
Authors: Therese Aglialoro, Cameron Nottingham, and William Kostuch
2021 MCM, Problem A: Fungi
"""
import matplotlib.pyplot as plt 
import numpy as np

from world import World


CLIMATE_NAMES = ["Desert", "Tundra", "Grassland", "Shrubland",  
                "TemperateDeciduousForest", "ConiferousForest",
                "Rainforest"]

FUNGUS_NAMES = ["Phellinus robiniae"]


if __name__ == "__main__":
    worlds = []
    for climate in CLIMATE_NAMES:
        # Arrays for holding values to graph
        time_array = np.zeros(365)
        temp_array = np.zeros(365)

        # Make a World and run it for a year
        world = World(climate, (100, 100), ["Phellinus robiniae"])
        for i in range(365):
            time = world.get_time()
            time_array[time] = time 
            temp_array[time] = world.get_environment().get_climate().get_climate_temperature()
            world.increment_time()
        plt.plot(time_array, temp_array, label=climate)
    plt.title("Temperature vs. Time for different climates")
    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Temperature (degrees C)")
    plt.show()

        
