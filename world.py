from typing import Tuple, List
from environment import Environment


class World:
    """World class that handles running the Environment."""

    #TODO
    # - Handle Time
    # - Create an environment easily
    # - Methods for asking each part of the model for useful data

    def __init__(self, 
            climate_type: str,
            grid_size: Tuple[int, int],
            fungus_list: List[str]) -> None:
        self.time = 0
        self.environment = Environment(climate_type, 
                                        grid_size,
                                        fungus_list)

    def increment_time(self):
        """Moves the World's time forward by one day."""
        self.time += 1
        self.environment.update(self.time)


    # GETTERS

    # World GETTERS
    def get_time(self) -> int:
        """Return's the World's time."""
        return self.time

    def get_environment(self) -> Environment:
        """Return's the World's Environment."""
        return self.environment
