import numpy as np
from typing import List, Tuple

class Grid:
    """Grid class for simulating an m x n meter environment."""

    def __init__(self, m: int, n: int, biomass=0) -> None:
        """Create a Grid with m rows and n columns made from Numpy arrays."""
        self.num_rows = m
        self.num_cols = n 
        self.map_grid = np.zeros(shape=(m, n)) + biomass
    
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
    def get_value_at_x_y(self, x: int, y: int) -> float:
        """Returns the value in the Grid at the given x and y location."""
        if self.__is_valid_row(x) and self.__is_valid_col(y):
            return self.map_grid[x][y]
        
    def get_value(self, location: tuple) -> float:
        """Returns the value in the Grid at location (x, y)."""
        return self.get_value_at_x_y(location[0], location[1])

    def get_grid_size(self) -> tuple:
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


    # SETTER METHODS
    def set_value_at_x_y(self, x: int, y: int, val: float):
        """Sets the value at location (x, y) in the Grid to val."""
        if self.__is_valid_row(x) and self.__is_valid_col(y):
            self.map_grid[x][y] = val

    def set_value(self, location: tuple, val: float):
        """Sets the value at location (x, y) in the Grid to val."""
        self.set_value_at_x_y(location[0], location[1], val)

    # ADDING METHODS
    def add_value_at_location(self, location: tuple, val: float):
        """Adds val to the number at (x, y) location."""
        self.set_value(location, val + self.get_value(location))

    def add_value_everywhere(self, val: float):
        """Adds val to every location in the Grid."""
        self.map_grid += val

    # REDUCING METHODS
    def reduce_value_at_location(self, location: tuple, val: float):
        """Reduces the number at (x, y) location by val."""
        self.set_value(location, self.get_value(location) - val)
