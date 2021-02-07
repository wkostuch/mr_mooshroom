from grid import Grid
from climate import Climate, Desert, Tundra, Shrubland, Grassland, \
    TemperateDeciduousForest, ConiferousForest, Rainforest
from environment import Environment
from utilities import rainfall_inches_to_mPa
from world import World


e = Environment("Rainforest", (3, 3), ["Phellinus robiniae",
                                        "Hyphodontia crustosa",
                                        "Phlebia rufa",
                                        "Hyphoderma setigerum",
                                        "Laetiporus conifericola",])
for f in e.get_fungi_list():
    print(f.name)
print("~**~*~*~*~~**~*~~*")
for i in range(1000):
    e.update(i)
for f in e.get_fungi_list():
    print(f.name)
