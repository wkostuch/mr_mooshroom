import numpy as np
from typing import List, Tuple
import random

class Grid:
    """Grid class for simulating an m x n meter environment."""

    def __init__(self, m: int, n: int, original_biomass=0, sensitivity=0) -> None:
        """Create a Grid with m rows and n columns made from Numpy arrays.
            Each cell is [original_biomass, current biomass]"""
        self.num_rows = m
        self.num_cols = n 
        self.map_grid = np.empty(shape=(m, n), dtype=object)
        # Fill array with tuples
        for r in range(m):
            for c in range(n):
                random_start_biomass = random.uniform(original_biomass - sensitivity, 
                                                        original_biomass + sensitivity)
                self.map_grid[r][c] = [random_start_biomass, random_start_biomass]
                
    def __str__(self) -> str:
        """Returns a pretty string representing the Grid's values."""
        return f"Rows: {self.num_rows}\nColumns: {self.num_cols}\n{self.map_grid}"


    # UTILITY METHODS used by setters and getters
    def __is_valid_row(self, r: int) -> bool:
        """Boolean on whether the given row exists."""
        return 0 <= r <= self.num_rows - 1

    def __is_valid_col(self, c: int) -> bool:
        """Bollean on whether the given column exists."""
        return 0 <= c <= self.num_cols - 1


    # GETTER METHODS
    def get_original_biomass_at_location(self, location: tuple) -> float:
        """Returns the original biomass at location (x, y)."""
        return self.get_value_tuple(location)[0]

    def get_current_biomass_at_location(self, location: tuple) -> float:
        """Returns the current biomass at location (x, y)."""
        return self.get_value_tuple(location)[1]

    def get_value_tuple_at_x_y(self, x: int, y: int) -> tuple:
        """Returns the value in the Grid at the given x and y location."""
        if self.__is_valid_row(x) and self.__is_valid_col(y):
            return self.map_grid[x][y]
        else:
            print(f"Location ({x}, {y}) is not a valid location.")
        
    def get_value_tuple(self, location: tuple) -> tuple:
        """Returns the value in the Grid at location (x, y)."""
        return self.get_value_tuple_at_x_y(location[0], location[1])

    def grid_size(self) -> tuple:
        """Returns a (x, y) tuple where x is the number of rows 
            and y is the number of columns of the Grid."""
        return (self.num_rows, self.num_cols)

    def get_neighbors(self, location: tuple) -> List[Tuple[int, int]]:
        """Returns a list of (x, y) tuples surrounding location while
            being aware of out-of-bounds requests."""
        # Unpack location
        x, y = location
        neighbors = list()
        # Loop through row above, current row, and row below
        for row in range(-1, 2):
            # Loop through col to the left, current col, and col to the right
            for col in range(-1, 2):
                # Skip the given location
                if row is 0 and col is 0:
                    continue
                # Make sure the proposed location is valid the Grid
                elif self.__is_valid_row(x + row) and self.__is_valid_col(y + col):
                    neighbors.append((x + row, y + col))
        return neighbors

    def generate_random_locations(self, location_num: int) -> List[Tuple[int, int]]:
        """Generates location_num locations in the Grid and puts them in a list."""
        locations = list()
        for i in range(location_num):
            rows, cols = self.grid_size()
            new_place = (random.randint(0, rows-1), random.randint(0, cols-1))
            if new_place not in locations:
                locations.append(new_place)
        return locations

    def average_biomass(self) -> float:
        """Returns the average current biomass of the Grid."""
        average = 0
        rows, cols = self.grid_size()
        for r in range(rows):
            for c in range(cols):
                average += self.get_current_biomass_at_location((r, c))
        average = average / (self.num_cols * self.num_rows)
        return average

    # SETTER METHODS
    def set_value_tuple_at_x_y(self, x: int, y: int, val: tuple):
        """Sets the value at location (x, y) in the Grid to val."""
        if self.__is_valid_row(x) and self.__is_valid_col(y):
            self.map_grid[x][y] = val

    def set_value_tuple(self, location: tuple, val: tuple):
        """Sets the value at location (x, y) in the Grid to val."""
        self.set_value_tuple_at_x_y(location[0], location[1], val)

    def set_current_biomass(self, location: tuple, val: float):
        """Sets the current biomass at (x, y) location to val."""
        original_biomass, current_biomass = self.get_value_tuple(location)
        self.set_value_tuple(location, (original_biomass, val))

    # ADDING METHODS
    def add_value_at_location(self, location: tuple, val: float):
        """Adds val to the current_biomass at (x, y) location."""
        self.set_current_biomass(location, 
                                val + self.get_current_biomass_at_location(location))

    def add_value_everywhere(self, val: float):
        """Adds val to every location in the Grid."""
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.map_grid[r][c] = [self.map_grid[r][c][0], 
                                        self.map_grid[r][c][1] + val]

    # REDUCING METHODS
    def reduce_value_at_location(self, location: tuple, val: float):
        """Reduces the number at (x, y) location by val."""
        self.set_current_biomass(location, 
                                self.get_current_biomass_at_location(location) - val)
