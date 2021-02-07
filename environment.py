from typing import List, Tuple
from grid import Grid
from fungus import * 
from climate import Climate, Desert, Tundra, Shrubland, Grassland, \
    TemperateDeciduousForest, ConiferousForest, Rainforest

NUM_LOCATIONS = 1


class Environment:
    """Environment class for containing Climate, Grid, and Fungi."""

    # Dictionary for mapping strings to creation of Climates
    climate_map = {"Desert": Desert(), 
                    "Tundra": Tundra(),
                    "Shrubland": Shrubland(),
                    "Grassland": Grassland(),
                    "TemperateDeciduousForest": TemperateDeciduousForest(),
                    "ConiferousForest": ConiferousForest(),
                    "Rainforest": Rainforest()}
    # Dictionary for mapping strings to Fungus objects
    fungus_map = {"Phellinus robiniae"          : Fungus1,
                    "Phellinus hartigii"        : Fungus2,
                    "Phellinus gilvus"          : Fungus3,
                    "Armillaria tabescens"      : Fungus4,
                    "Porodisculus pendulus"     : Fungus5,
                    "Schizophyllum commune"     : Fungus6,
                    "Hyphodontia crustosa"      : Fungus7,
                    "Phlebia rufa"              : Fungus8,
                    "Hyphoderma setigerum"      : Fungus9,
                    "Laetiporus conifericola"   : Fungus10,
                    "Tyromyces chioneus"        : Fungus11,
                    "Lentinus crinitus"         : Fungus12,
                    "Fomes fomentarius"         : Fungus13,
                    "Xylobolus subpileatus"     : Fungus14}

    def __init__(self, 
                climate_type: str,
                grid_size: Tuple[int, int],
                fungus_list: List[str]) -> None:
        # Substantiate the Climate, Grid, and Fungus objects for the Environment
        self.climate = self.climate_map.get(climate_type)
        self.grid = Grid(grid_size[0], grid_size[1], 
                        self.climate.get_climate_biomass_density(), 
                        sensitivity=0.15)
        self.fungus_list = [self.fungus_map.get(new_fungus)(self.grid.generate_random_locations(NUM_LOCATIONS)) 
                            for new_fungus in fungus_list]

    def update(self, time: int):
        """Update's the Environment using time."""
        # Update the Climate
        self.climate.update_climate_per_day(time)
        new_biomass = self.climate.get_inbound_biomass(time)
        # Update the Grid
        self.grid.add_value_everywhere(new_biomass)
        # Update the Fungi
        for fungalicious in self.fungus_list:
            fungalicious.turn(self.grid, self.climate)


    # GETTER methods

    def get_climate(self) -> Climate:
        """Return's the Environment's Climate."""
        return self.climate

    def get_grid(self) -> Grid:
        """Return's the Environment's Grid."""
        return self.grid

    def get_fungi_list(self) -> List[Fungus]:
        """Return's a list of Fungus in the Environment."""
        return self.fungus_list

