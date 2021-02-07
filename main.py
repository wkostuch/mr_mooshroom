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
YEARS = 5

def total_food_eaten_over_time(climates: List[str], fungi: List[str], 
                        trials: int, time_limit: int):
    """Shows a graph of average food eaten by fungi over time for each climate after running the trials."""
    array_length = time_limit 
    for climate in climates:
        # Arrays for graphing
        average_times = np.zeros(array_length)
        average_biomass_eaten = np.zeros(array_length)
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
                total_food_eaten = 0
                for fungus in world.get_environment().get_fungi_list():
                    total_food_eaten += fungus.get_total_amount_of_substrate_eaten()
                biomasses[time] = total_food_eaten 
                world.increment_time()
            # Add arrays to average arrays
            average_times += times
            average_biomass_eaten += biomasses
        # Average and plot
        average_times /= trials
        average_biomass_eaten /= trials
        plt.plot(average_times, 
                average_biomass_eaten, 
                label=climate)
    plt.title(f"Total biomass decomposed by fungi vs. Time for different climates \n(trials per climate: {trials}, number of fungi: {len(fungi)}")
    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Biomass decomposed")
    plt.show()

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
    plt.title(f"Biomass vs. Time for different climates \n(trials per climate: {trials}, number of fungi: {len(fungi)}")
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

def food_eaten_by_day_per_fungi_vs_moisture(climate: str, fungi: List[str],
                                            trials: int, time_limit: int):
    """Shows a graph of food eaten per type of fungi in a given climate vs. moisture levels in that climate."""
    # Arrays to graph
    list_of_fungi = [[np.zeros(time_limit), ""] for f in fungi] # Will hold an array for each fungi that holds how much it ate that day
    average_moisture = np.zeros(time_limit)
    # Run through different trials
    for n in range(trials):
        # Arrays for specific trials
        moisture = np.zeros(time_limit)
        fungi_this_run = list()
        # Make a world and run it
        world = World(climate, (100, 100), fungi)
        # Give each fungi an array in order its made by World
        for f in world.get_environment().get_fungi_list():
            fungi_this_run.append([np.zeros(time_limit), f.name])
        # Run the world
        for i in range(time_limit):
            time = world.get_time()
            # Food per fungi type
            for index,f in enumerate(world.get_environment().get_fungi_list()):
                fungi_this_run[index][0][time] = f.get_amount_of_substrate_eaten_today()
            moisture[time] = world.get_environment().get_climate().get_climate_moisture()
            world.increment_time()
        # Data massaging
        average_moisture += moisture
        for index, fungi_info in enumerate(fungi_this_run):
            fungi_name = fungi_info[1]
            food_values = fungi_info[0]
            list_of_fungi[index][0] += food_values
            list_of_fungi[index][1] = fungi_name
    # Now average everything
    average_moisture /= trials 
    for index,fungi_data in enumerate(list_of_fungi):
        fungi_food_data = fungi_data[0] / trials
        fungi_name = fungi_data[1]
        plt.plot(fungi_food_data, average_moisture, label=f"{fungi_name}")
    plt.title("Moisture level vs. biomass consumed in one day for different fungi")
    plt.legend()
    plt.xlabel("Biomass consumed")
    plt.ylabel("Moisture levels (MPa)")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    #temperature_over_time(["Rainforest", "Tundra"], FUNGUS_NAMES[0:5], trials=1, time_limit=365*YEARS)
    #biomass_over_time(CLIMATE_NAMES, FUNGUS_NAMES, trials=5, time_limit=365*YEARS)
    food_eaten_by_day_per_fungi_vs_moisture("Rainforest", FUNGUS_NAMES[0:15], trials = 1, time_limit=365)


