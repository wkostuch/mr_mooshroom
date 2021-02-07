from grid import Grid
from climate import Climate, Desert, Tundra, Shrubland, Grassland, \
    TemperateDeciduousForest, ConiferousForest, Rainforest
from environment import Environment
from utilities import rainfall_inches_to_mPa
from world import World


e = Environment("Rainforest", (2, 2), ["Phellinus robiniae"])
print(e.fungus_list[0].locations)
for i in range(1000):
    e.update(i)
print(e.fungus_list[0].locations)
