from grid import Grid
from climate import Climate, Desert, Tundra, Shrubland, Grassland, \
    TemperateDeciduousForest, ConiferousForest, Rainforest
from environment import Environment
from utilities import rainfall_inches_to_mPa
from world import World


e = Environment("Rainforest", (100, 100), ["Xylobolus subpileatus"])
print(e.fungus_list[0].locations)
for i in range(365):
    e.update(i)
print(len(e.fungus_list[0].locations.keys()))
